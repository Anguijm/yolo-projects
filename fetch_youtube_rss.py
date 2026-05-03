#!/usr/bin/env python3
"""Fetch YouTube RSS feeds for Phase 4 channels and output new videos as JSON.

Usage: python3 fetch_youtube_rss.py [--since YYYY-MM-DD]

Outputs JSON array of new videos to stdout. Compares against experiments.json
to skip already-processed videos.
"""
import json
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

CHANNELS = {
    # Kept from original roster
    "@NateBJones": "UC0C-17n9iuUQPylguM1d-lQ",
    "@MLOps": "UCG6qpjVnBTTT8wLGBygANOQ",
    "@DavidOndrej": "UCPGrgwfbkjTIgPoOh2q1BAg",
    "[un]prompted": "UC5GCrYGsm7EHQzQZj65A-5w",
    "@NateHerk": "UC2ojq-nuP8ceeHqiroeKhBA",
    # Added — council-evaluated, signal 8-10/10
    "@swyx": "UC50YKpKY_2Y86Qo4DZY3mMQ",
    "@GregKamradt": "UC7mHKIdjuKTJVamHqR5JTRg",
    "@AIJasonZ": "UCrXSVX9a1mj8l0CMLwKgMVw",
    "@echohive": "UCL7przoMtZTmiQMhc9ifIww",
    "@ShawTalebi": "UCa9gErQ9AE5jT2DZLjXBIdA",
    "@Mark_Kashef": "UCHkzp52CldSPZqU5T49mOnA",
    # Added 2026-04-30 — primary source instead of reactor commentary.
    # Verified ID via /channel/ redirect from /@AndrejKarpathy.
    "@AndrejKarpathy": "UCXUPKJO5MZQN11PqgIvyuvQ",
}

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={}"

TRANSCRIPT_CACHE = Path(__file__).parent / "phase4_cache" / "transcripts"
TRANSCRIPT_HEAD_CHARS = 6000
TRANSCRIPT_TAIL_CHARS = 4000


def _strip_vtt(vtt: str) -> str:
    """Strip VTT timestamps and headers, returning plain text."""
    out_lines = []
    for line in vtt.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        # Skip cue timing lines like "00:00:01.000 --> 00:00:04.000"
        if "-->" in stripped:
            continue
        # Skip cue identifier lines (numeric or short alphanumerics on their own)
        if re.fullmatch(r"\d+", stripped):
            continue
        # Strip inline cue tags like <c> </c> and <00:00:01.000>
        cleaned = re.sub(r"<[^>]+>", "", stripped)
        out_lines.append(cleaned)
    # Auto-captions repeat each phrase (rolling karaoke). Dedupe consecutive duplicates.
    deduped = []
    for line in out_lines:
        if not deduped or deduped[-1] != line:
            deduped.append(line)
    return " ".join(deduped)


def truncate_transcript(text: str, head: int = TRANSCRIPT_HEAD_CHARS, tail: int = TRANSCRIPT_TAIL_CHARS) -> str:
    """Keep the first `head` chars + last `tail` chars; drop the middle.

    The hook + intro tend to live in the head; "what we built / try this"
    callouts tend to live in the tail. The middle is mostly mid-roll filler.
    """
    if len(text) <= head + tail:
        return text
    head_part = text[:head]
    tail_part = text[-tail:]
    return f"{head_part}\n\n[... transcript truncated, {len(text) - head - tail} chars elided ...]\n\n{tail_part}"


def _snippets_to_text(texts: list[str]) -> str:
    """Join transcript snippet text fragments and dedupe consecutive duplicates.

    Auto-captions sometimes have rolling-karaoke repeats; collapse those.
    Non-consecutive duplicates (the same word in different sentences) survive.
    """
    cleaned = []
    for raw in texts:
        line = raw.strip().replace("\n", " ")
        if not line:
            continue
        if cleaned and cleaned[-1] == line:
            continue
        cleaned.append(line)
    return " ".join(cleaned)


SUPADATA_ENDPOINT = "https://api.supadata.ai/v1/youtube/transcript"


def _fetch_via_supadata(video_id: str, api_key: str, timeout: int = 30) -> list[dict] | None:
    """Fetch transcript via supadata.ai; returns list of {text, start, duration} or None.

    Supadata proxies through residential IPs and is not blocked by YouTube's
    datacenter-IP filtering. Free tier: 100 transcripts/month.

    Response shape (without `text=true`): {
      "content": [{"text": "...", "offset": 0, "duration": 1500, "lang": "en"}, ...],
      "lang": "en",
      "availableLangs": [...]
    }
    Note: `offset` and `duration` are in MILLISECONDS in supadata's response.
    """
    url = f"{SUPADATA_ENDPOINT}?videoId={video_id}&lang=en"
    req = Request(url, headers={"x-api-key": api_key, "User-Agent": "yolo-projects-phase4/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        # 404 = no transcript; 401/403 = bad key; 429 = quota; 5xx = upstream issue
        body_preview = ""
        try:
            body_preview = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            pass
        print(f"  WARN: supadata HTTP {e.code} for {video_id}: {body_preview}", file=sys.stderr)
        return None
    except (URLError, TimeoutError) as e:
        print(f"  WARN: supadata network error for {video_id}: {type(e).__name__}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  WARN: supadata unexpected error for {video_id}: {type(e).__name__}: {str(e)[:140]}", file=sys.stderr)
        return None

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        print(f"  WARN: supadata returned non-JSON for {video_id}: {body[:200]}", file=sys.stderr)
        return None

    content = data.get("content")
    if not isinstance(content, list) or not content:
        return None

    # Normalize to {text, start, duration} in seconds (matches youtube-transcript-api shape).
    snippets = []
    for c in content:
        text = c.get("text", "")
        if not text:
            continue
        offset_ms = c.get("offset", 0) or 0
        duration_ms = c.get("duration", 0) or 0
        snippets.append({
            "text": text,
            "start": offset_ms / 1000.0,
            "duration": duration_ms / 1000.0,
        })
    return snippets or None


def _fetch_via_youtube_transcript_api(video_id: str) -> list[dict] | None:
    """Fetch transcript via youtube-transcript-api; returns list of {text, start, duration} or None.

    Used as the fallback when SUPADATA_API_KEY is not set, or alongside it
    for local dev. Almost always blocked by YouTube on datacenter IPs
    (verified 0/14 in CI 2026-05-03), but harmless to keep as a secondary
    path in case YouTube ever stops blocking.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError:
        return None

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US", "en-GB"])
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except VideoUnavailable as e:
        print(f"  WARN: video unavailable {video_id}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  WARN: youtube-transcript-api failed for {video_id}: {type(e).__name__}: {str(e)[:140]}", file=sys.stderr)
        return None

    snippets = list(fetched)
    if not snippets:
        return None
    return [{"text": s.text, "start": s.start, "duration": s.duration} for s in snippets]


def fetch_transcript(video_id: str, timeout: int = 30) -> str | None:
    """Fetch auto-captions; return plain text or None on any failure.

    Strategy (verified-best-first):
      1. JSON cache hit at phase4_cache/transcripts/<video_id>.json.
      2. supadata.ai if SUPADATA_API_KEY env var is set (residential-IP proxied
         endpoint that bypasses YouTube's datacenter-IP block).
      3. youtube-transcript-api as a fallback (almost always blocked from
         datacenter IPs but cheap to try once).
      4. None if everything fails — caller falls back to title-only generation.

    Cache schema: list of {text, start, duration}. Times in seconds.
    """
    TRANSCRIPT_CACHE.mkdir(parents=True, exist_ok=True)
    cache_file = TRANSCRIPT_CACHE / f"{video_id}.json"

    if cache_file.exists() and cache_file.stat().st_size > 0:
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return _snippets_to_text([s["text"] for s in data])
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            pass  # fall through and re-fetch

    snippets: list[dict] | None = None
    api_key = os.environ.get("SUPADATA_API_KEY")
    if api_key:
        snippets = _fetch_via_supadata(video_id, api_key, timeout=timeout)
    if snippets is None:
        snippets = _fetch_via_youtube_transcript_api(video_id)
    if not snippets:
        return None

    try:
        cache_file.write_text(json.dumps(snippets), encoding="utf-8")
    except OSError as e:
        print(f"  WARN: cannot cache transcript for {video_id}: {e}", file=sys.stderr)

    return _snippets_to_text([s["text"] for s in snippets])


def fetch_feed(channel_id):
    """Fetch RSS feed XML, return as string or None on failure."""
    url = RSS_URL.format(channel_id)
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (URLError, TimeoutError, Exception) as e:
        print(f"  WARN: Failed to fetch {channel_id}: {e}", file=sys.stderr)
        return None


def parse_entries(xml_text):
    """Extract video entries from RSS XML."""
    entries = []
    for match in re.finditer(r"<entry>(.*?)</entry>", xml_text, re.DOTALL):
        entry = match.group(1)
        video_id = re.search(r"<yt:videoId>(.*?)</yt:videoId>", entry)
        title = re.search(r"<title>(.*?)</title>", entry)
        published = re.search(r"<published>(.*?)</published>", entry)
        link = re.search(r'<link rel="alternate" href="(.*?)"', entry)
        if video_id and title and published:
            entries.append({
                "video_id": video_id.group(1),
                "title": title.group(1),
                "published": published.group(1)[:10],
                "url": link.group(1) if link else f"https://www.youtube.com/watch?v={video_id.group(1)}",
            })
    return entries


def get_known_video_ids():
    """Get video IDs already in experiments.json."""
    exp_file = Path(__file__).parent / "experiments.json"
    if not exp_file.exists():
        return set()
    try:
        exps = json.loads(exp_file.read_text())
        ids = set()
        for e in exps:
            url = e.get("source", {}).get("video_url", "")
            vid_match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
            if vid_match:
                ids.add(vid_match.group(1))
        return ids
    except (json.JSONDecodeError, KeyError):
        return set()


def main():
    since = None
    if "--since" in sys.argv:
        idx = sys.argv.index("--since")
        if idx + 1 < len(sys.argv):
            since = sys.argv[idx + 1]

    if not since:
        since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

    with_transcripts = "--with-transcripts" in sys.argv

    known_ids = get_known_video_ids()
    results = {
        "scan_time_utc": datetime.utcnow().isoformat() + "Z",
        "since": since,
        "channels_scanned": len(CHANNELS),
        "feeds_successful": 0,
        "feeds_failed": 0,
        "with_transcripts": with_transcripts,
        "transcripts_fetched": 0,
        "transcripts_missing": 0,
        "new_videos": [],
    }

    for channel_name, channel_id in CHANNELS.items():
        xml = fetch_feed(channel_id)
        if xml is None:
            results["feeds_failed"] += 1
            continue
        results["feeds_successful"] += 1

        entries = parse_entries(xml)
        for entry in entries:
            if entry["published"] < since:
                continue
            if entry["video_id"] in known_ids:
                continue
            entry["channel"] = channel_name
            if with_transcripts:
                transcript = fetch_transcript(entry["video_id"])
                if transcript:
                    entry["transcript"] = truncate_transcript(transcript)
                    entry["transcript_full_chars"] = len(transcript)
                    results["transcripts_fetched"] += 1
                else:
                    entry["transcript"] = None
                    results["transcripts_missing"] += 1
            results["new_videos"].append(entry)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

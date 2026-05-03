#!/usr/bin/env python3
"""Fetch YouTube RSS feeds for Phase 4 channels and output new videos as JSON.

Usage: python3 fetch_youtube_rss.py [--since YYYY-MM-DD]

Outputs JSON array of new videos to stdout. Compares against experiments.json
to skip already-processed videos.
"""
import json
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

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


def fetch_transcript(video_id: str, timeout: int = 30) -> str | None:
    """Fetch auto-captions via youtube-transcript-api; return plain text or None.

    Originally used yt-dlp, but YouTube blocks yt-dlp aggressively from
    GitHub Actions IP ranges (verified 2026-05-03: 0/18 fetched).
    youtube-transcript-api uses the same endpoint youtube.com itself uses
    to render the transcript panel — much less blocked.

    Cache: phase4_cache/transcripts/<video_id>.json with raw snippets.
    `timeout` kept for signature compatibility but the library does not
    expose per-call timeouts; failures bubble up via exceptions instead.
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

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError:
        print(f"  WARN: youtube-transcript-api not installed for {video_id}", file=sys.stderr)
        return None

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US", "en-GB"])
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except VideoUnavailable as e:
        print(f"  WARN: video unavailable {video_id}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        # Network failures, parser errors, IP blocks all reach here.
        print(f"  WARN: transcript fetch failed for {video_id}: {type(e).__name__}: {str(e)[:140]}", file=sys.stderr)
        return None

    snippets = list(fetched)
    if not snippets:
        return None

    try:
        cache_file.write_text(
            json.dumps([{"text": s.text, "start": s.start, "duration": s.duration} for s in snippets]),
            encoding="utf-8",
        )
    except OSError as e:
        print(f"  WARN: cannot cache transcript for {video_id}: {e}", file=sys.stderr)

    return _snippets_to_text([s.text for s in snippets])


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

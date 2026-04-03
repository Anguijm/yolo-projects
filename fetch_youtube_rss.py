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
    "@NateBJones": "UC0C-17n9iuUQPylguM1d-lQ",
    "@MLOps": "UCG6qpjVnBTTT8wLGBygANOQ",
    "@DavidOndrej": "UCPGrgwfbkjTIgPoOh2q1BAg",
    "[un]prompted": "UC5GCrYGsm7EHQzQZj65A-5w",
    "@NateHerk": "UC2ojq-nuP8ceeHqiroeKhBA",
    "@TwoMinutePapers": "UCbfYPyITQ-7l4upoX8nvctg",
    "@Fireship": "UCsBjURrPoezykLs9EqgamOA",
}

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={}"


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

    known_ids = get_known_video_ids()
    results = {
        "scan_time_utc": datetime.utcnow().isoformat() + "Z",
        "since": since,
        "channels_scanned": len(CHANNELS),
        "feeds_successful": 0,
        "feeds_failed": 0,
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
            results["new_videos"].append(entry)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

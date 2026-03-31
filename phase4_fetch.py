#!/usr/bin/env python3
"""Phase 4: Fetch new videos from monitored YouTube channels.

Checks @NateBJones (daily) and @MLOps (weekly) for new uploads.
Diffs against already-processed video IDs in experiments.json.
Appends new video URLs to phase4_queue.json for processing.

Usage: python3 phase4_fetch.py
Designed to run via daily cron.
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
EXPERIMENTS = ROOT / "experiments.json"
QUEUE = ROOT / "phase4_queue.json"

CHANNELS = {
    "@NateBJones": {
        "url": "https://www.youtube.com/@NateBJones/videos",
        "check_count": 3,  # daily poster — check last 3
    },
    "@MLOps": {
        "url": "https://www.youtube.com/@MLOps/videos",
        "check_count": 2,  # weekly poster — check last 2
    },
    "@DavidOndrej": {
        "url": "https://www.youtube.com/@DavidOndrej/videos",
        "check_count": 3,  # ~2-3 per week — check last 3
    },
    "[un]prompted": {
        "url": "https://www.youtube.com/channel/UC5GCrYGsm7EHQzQZj65A-5w/videos",
        "check_count": 3,  # conference talks — batch uploads
    },
    "@NateHerk": {
        "url": "https://www.youtube.com/@NateHerk/videos",
        "check_count": 3,  # ~2-3 per week — AI workflows, Claude Code
    },
}


def get_processed_ids():
    """Get all video IDs already in experiments.json."""
    if not EXPERIMENTS.exists():
        return set()
    data = json.loads(EXPERIMENTS.read_text())
    ids = set()
    for exp in data:
        url = exp.get("source", {}).get("video_url", "")
        if "watch?v=" in url:
            ids.add(url.split("watch?v=")[1].split("&")[0])
        # Also check also_mentioned_in
        for extra in exp.get("source", {}).get("also_mentioned_in", []):
            if "watch?v=" in extra:
                ids.add(extra.split("watch?v=")[1].split("&")[0])
    return ids


def get_queued_ids():
    """Get video IDs already in the queue."""
    if not QUEUE.exists():
        return set()
    data = json.loads(QUEUE.read_text())
    return {item["video_id"] for item in data}


def fetch_recent(channel_name, channel_url, count):
    """Fetch the N most recent video IDs and titles from a channel."""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--flat-playlist",
                f"--playlist-end={count}",
                "--print", "%(id)s\t%(title)s",
                channel_url,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        videos = []
        for line in result.stdout.strip().split("\n"):
            if "\t" in line:
                vid_id, title = line.split("\t", 1)
                videos.append({"video_id": vid_id, "title": title, "channel": channel_name})
        return videos
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  Error fetching {channel_name}: {e}", file=sys.stderr)
        return []


def main():
    processed = get_processed_ids()
    queued = get_queued_ids()
    known = processed | queued

    # Load existing queue
    queue = json.loads(QUEUE.read_text()) if QUEUE.exists() else []

    new_count = 0
    for name, cfg in CHANNELS.items():
        print(f"Checking {name}...")
        videos = fetch_recent(name, cfg["url"], cfg["check_count"])
        for v in videos:
            if v["video_id"] not in known:
                entry = {
                    "video_id": v["video_id"],
                    "video_url": f"https://www.youtube.com/watch?v={v['video_id']}",
                    "title": v["title"],
                    "channel": v["channel"],
                    "fetched_date": datetime.now().strftime("%Y-%m-%d"),
                    "processed": False,
                }
                queue.append(entry)
                known.add(v["video_id"])
                new_count += 1
                print(f"  NEW: {v['title'][:60]}")
            else:
                print(f"  skip: {v['title'][:60]} (already known)")

    QUEUE.write_text(json.dumps(queue, indent=2))
    print(f"\nDone. {new_count} new video(s) queued. Total in queue: {len([q for q in queue if not q['processed']])}")


if __name__ == "__main__":
    main()

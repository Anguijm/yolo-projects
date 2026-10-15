#!/usr/bin/env python3
"""Fetch every Phase 4 channel's YouTube RSS feed from this machine and write
one JSON snapshot that the Daily YouTube Research workflow reads instead of
fetching the feeds from a GitHub-hosted runner.

Why: since 2026-10-06 YouTube has answered GitHub's runners with HTTP 404 and
500 for feeds that return 200 from the home network (see the phase4_run.json
history). This script runs on the MS-S1 at home from cron (06:00 and 10:00
JST, via scripts/snapshot_feeds.sh) and the result is pushed to the branch
feeds/snapshot; fetch_youtube_rss.py uses it when it is under 8 hours old.

Usage: python3 scripts/fetch_feeds_snapshot.py [--out PATH]

The file holds, per channel, the fetch time, the HTTP status, the entries
(video_id, title, published, url: the same shape fetch_youtube_rss.py's
parse_entries produces) and an error string when the fetch failed. Zero
entries with HTTP 200 is recorded as such; an exception is recorded as the
error, never swallowed.

Exit codes: 0 when at least half the channels fetched (HTTP 200), 2
otherwise. The file is written either way so the record of what failed
survives.
"""
import json
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from fetch_youtube_rss import CHANNELS, FEED_USER_AGENT, RSS_URL, parse_entries  # noqa: E402

DEFAULT_OUT = ROOT / "data" / "feeds" / "snapshot.json"
ATTEMPTS = 3
RETRY_DELAYS = (5, 15)  # seconds between attempts 1->2 and 2->3
TIMEOUT = 20


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def fetch_one(channel_name, channel_id):
    rec = {
        "channel_id": channel_id,
        "fetched_at_utc": now_utc(),
        "http_status": None,
        "attempts": 0,
        "error": None,
        "entry_count": 0,
        "entries": [],
    }
    url = RSS_URL.format(channel_id)
    for attempt in range(1, ATTEMPTS + 1):
        rec["attempts"] = attempt
        try:
            req = Request(url, headers={"User-Agent": FEED_USER_AGENT})
            with urlopen(req, timeout=TIMEOUT) as resp:
                rec["http_status"] = resp.status
                xml = resp.read().decode("utf-8", errors="replace")
            rec["entries"] = parse_entries(xml)
            rec["entry_count"] = len(rec["entries"])
            rec["error"] = None
            return rec
        except HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")[:200].replace("\n", " ")
            except Exception:
                pass
            rec["http_status"] = e.code
            rec["error"] = f"HTTP {e.code} {e.reason}; body[:200]={body!r}"
        except Exception as e:
            rec["http_status"] = None
            rec["error"] = f"{type(e).__name__}: {e}"
        if attempt < ATTEMPTS:
            delay = RETRY_DELAYS[min(attempt - 1, len(RETRY_DELAYS) - 1)]
            print(
                f"  WARN: {channel_name} attempt {attempt}/{ATTEMPTS} failed ({rec['error']}); retrying in {delay}s",
                file=sys.stderr,
            )
            time.sleep(delay)
    return rec


def main(argv):
    out = DEFAULT_OUT
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])

    channels = {}
    for name, cid in CHANNELS.items():
        rec = fetch_one(name, cid)
        channels[name] = rec
        state = f"HTTP {rec['http_status']}" if rec["http_status"] else "no response"
        tail = f"{rec['entry_count']} entries" if not rec["error"] else f"ERROR {rec['error']}"
        print(f"  {name}: {state}, {tail}", file=sys.stderr)

    ok = sum(1 for r in channels.values() if r["http_status"] == 200 and not r["error"])
    snap = {
        "snapshot_time_utc": now_utc(),
        "fetched_from": socket.gethostname(),
        "channels_total": len(channels),
        "channels_ok": ok,
        "entries_total": sum(r["entry_count"] for r in channels.values()),
        "channels": channels,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"snapshot: {ok}/{len(channels)} channels fetched, {snap['entries_total']} entries, written to {out}",
        file=sys.stderr,
    )
    if ok * 2 < len(channels):
        print(f"ERROR: fewer than half the channels fetched ({ok}/{len(channels)})", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

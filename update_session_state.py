#!/usr/bin/env python3
"""Update session_state.json from current project state.

Reads yolo_log.json, experiments.json, phase4_queue.json, and
deck_roadmap.md to reconstruct the full session state.

Usage: python3 update_session_state.py
Run after every commit or at session end.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
STATE_FILE = ROOT / "session_state.json"


def count_experiments():
    path = ROOT / "experiments.json"
    if not path.exists():
        return {"total": 0, "adopted": 0, "discarded": 0, "backlog": 0, "in_progress": 0}
    exps = json.loads(path.read_text())
    return {
        "total": len(exps),
        "adopted": sum(1 for e in exps if e.get("verdict") == "adopt"),
        "discarded": sum(1 for e in exps if e.get("verdict") == "discard"),
        "backlog": sum(1 for e in exps if e["status"] == "backlog"),
        "in_progress": sum(1 for e in exps if e["status"] == "in_progress"),
    }


def get_unprocessed_queue():
    path = ROOT / "phase4_queue.json"
    if not path.exists():
        return []
    q = json.loads(path.read_text())
    return [f"{item['channel']}: {item['title'][:60]}" for item in q if not item.get("processed")]


def get_last_session():
    path = ROOT / "markdown-deck" / "deck_roadmap.md"
    if not path.exists():
        return "unknown", "unknown", "unknown"
    text = path.read_text()
    # Find last row in session log table
    rows = re.findall(r'\| (\d{4}-\d{2}-\d{2}) \| (Tick|Tock) \| (.+?) \|', text)
    if not rows:
        return "unknown", "unknown", "unknown"
    last = rows[-1]
    return last[1], last[2].strip(), last[0]


def get_portfolio():
    path = ROOT / "yolo_log.json"
    if not path.exists():
        return {"total": 0, "culled": 0, "active": 0}
    log = json.loads(path.read_text())
    total = len(log)
    culled = sum(1 for e in log if e["status"] == "failed")
    return {"total": total, "culled": culled, "active": total - culled}


def get_pending_deck_fixes():
    path = ROOT / "markdown-deck" / "deck_roadmap.md"
    if not path.exists():
        return []
    text = path.read_text()
    pending = re.findall(r'^- \[ \] (.+)$', text, re.MULTILINE)
    return pending[:10]


def get_channels():
    path = ROOT / "phase4_fetch.py"
    if not path.exists():
        return []
    text = path.read_text()
    return re.findall(r'"(@[\w]+|\[un\]prompted)"', text)


def update():
    last_type, last_work, last_date = get_last_session()
    next_type = "tock" if last_type.lower() == "tick" else "tick"
    exp = count_experiments()
    unprocessed = get_unprocessed_queue()
    portfolio = get_portfolio()
    pending_fixes = get_pending_deck_fixes()
    channels = get_channels()

    state = {
        "version": 1,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "tick_tock": {
            "last_session_type": last_type.lower(),
            "last_session_work": last_work,
            "last_session_date": last_date,
            "next_session_type": next_type,
            "next_action": f"{'Build new YOLO project or feeder' if next_type == 'tick' else 'Work on Markdown Deck: ' + (pending_fixes[0] if pending_fixes else 'check roadmap')}",
        },
        "markdown_deck": {
            "pending_items": pending_fixes,
        },
        "phase4": {
            "channels_monitored": len(channels),
            "channels": channels,
            "experiments_total": exp["total"],
            "experiments_adopted": exp["adopted"],
            "experiments_discarded": exp["discarded"],
            "experiments_backlog": exp["backlog"],
            "experiments_in_progress": exp["in_progress"],
            "queue_unprocessed": len(unprocessed),
            "unprocessed_videos": unprocessed,
        },
        "portfolio": {
            "total_built": portfolio["total"],
            "total_culled": portfolio["culled"],
            "active_projects": portfolio["active"],
        },
        "resume_instructions": f"Last session was {last_type} ({last_work}). Next is {next_type}. "
        + (f"Pending deck fixes: {pending_fixes[0] if pending_fixes else 'none'}. " if next_type == "tock" else "")
        + f"{len(unprocessed)} unprocessed Phase 4 videos in queue."
    }

    STATE_FILE.write_text(json.dumps(state, indent=2))
    print(f"Session state updated. Next: {next_type}. {exp['backlog']} experiments in backlog. {len(unprocessed)} videos queued.")


if __name__ == "__main__":
    update()

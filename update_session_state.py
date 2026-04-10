#!/usr/bin/env python3
"""Update session_state.json from current project state.

MERGE-BASED: loads the existing state and updates only the computed
fields (phase4 counts, portfolio stats, markdown_deck pending items).
Preserves hand-maintained fields: tick_queue_approved, tick_queue_pending,
manual_queue, council_escalations, council_escalations_resolved,
resume_instructions, next_action, last_session_work, and any other
fields added by interactive sessions or cron workers.

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
        return {"total": 0, "adopted": 0, "discarded": 0, "backlog": 0,
                "in_progress": 0, "deferred": 0}
    exps = json.loads(path.read_text())
    # "adopted" = status in (done, adopted) per historical convention
    adopted = sum(1 for e in exps if e["status"] in ("done", "adopted"))
    return {
        "total": len(exps),
        "adopted": adopted,
        "discarded": sum(1 for e in exps if e["status"] == "discarded"),
        "backlog": sum(1 for e in exps if e["status"] == "backlog"),
        "in_progress": sum(1 for e in exps if e["status"] == "in_progress"),
        "deferred": sum(1 for e in exps if e["status"] == "deferred"),
    }


def get_unprocessed_queue():
    path = ROOT / "phase4_queue.json"
    if not path.exists():
        return []
    q = json.loads(path.read_text())
    return [f"{item['channel']}: {item['title'][:60]}"
            for item in q if not item.get("processed")]


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
    # Load existing state — preserve all fields not computed here
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
    else:
        state = {"version": 1, "tick_tock": {}, "markdown_deck": {},
                 "phase4": {}, "portfolio": {}}

    exp = count_experiments()
    unprocessed = get_unprocessed_queue()
    portfolio = get_portfolio()
    pending_fixes = get_pending_deck_fixes()
    channels = get_channels()

    state["last_updated"] = datetime.now(timezone.utc).isoformat()

    # --- Phase 4: overwrite computed counts only ---
    p4 = state.setdefault("phase4", {})
    p4["channels_monitored"] = len(channels)
    p4["channels"] = channels
    p4["experiments_total"] = exp["total"]
    p4["experiments_adopted"] = exp["adopted"]
    p4["experiments_discarded"] = exp["discarded"]
    p4["experiments_backlog"] = exp["backlog"]
    p4["experiments_in_progress"] = exp["in_progress"]
    p4["experiments_deferred"] = exp["deferred"]
    p4["queue_unprocessed"] = len(unprocessed)
    p4["unprocessed_videos"] = unprocessed
    # Remove stale _resync_note if present (one-time cleanup)
    p4.pop("_resync_note", None)

    # --- Portfolio: overwrite computed counts only ---
    pf = state.setdefault("portfolio", {})
    pf["total_built"] = portfolio["total"]
    pf["active_working"] = portfolio["active"]
    pf["total_culled"] = portfolio["culled"]
    pf["last_reconciled"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # --- Markdown Deck: overwrite pending items ---
    md = state.setdefault("markdown_deck", {})
    md["pending_items"] = pending_fixes

    # --- Preserved (NOT touched): ---
    # tick_tock.tick_queue_approved
    # tick_tock.tick_queue_pending
    # tick_tock.manual_queue
    # tick_tock.manual_queue_completed
    # tick_tock.next_action
    # tick_tock.last_session_work
    # council_escalations
    # council_escalations_resolved
    # resume_instructions

    STATE_FILE.write_text(json.dumps(state, indent=2))
    print(f"Session state updated (merge mode).")
    print(f"  Phase 4: {exp['total']} experiments, {exp['backlog']} backlog, "
          f"{exp['adopted']} adopted, {exp['discarded']} discarded, "
          f"{exp['deferred']} deferred.")
    print(f"  Portfolio: {portfolio['total']} built, {portfolio['active']} active.")
    print(f"  Deck: {len(pending_fixes)} pending items.")
    print(f"  Videos queued: {len(unprocessed)}.")


if __name__ == "__main__":
    update()

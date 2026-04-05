#!/usr/bin/env python3
"""Auto-generate _hot.md from current system state.

Run after every build to keep the hot cache current.
The cron agent reads _hot.md FIRST instead of scanning 3000+ lines of learnings.md.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent


def main():
    # Load state
    session = json.loads((ROOT / "session_state.json").read_text())
    log = json.loads((ROOT / "yolo_log.json").read_text())
    experiments = json.loads((ROOT / "experiments.json").read_text())

    # Portfolio stats
    active = [e for e in log if e.get("status") in ("working", "partial")]
    total = len(log)

    # Tick queue
    approved = session.get("tick_tock", {}).get("tick_queue_approved", [])
    pending = session.get("tick_tock", {}).get("tick_queue_pending", [])

    # Recent builds (last 5 working)
    recent = [e for e in reversed(log) if e.get("status") == "working"][:5]

    # Experiment stats
    backlog = [e for e in experiments if e.get("status") == "backlog"]

    # Last learnings (from build_memory if available)
    recent_learnings = []
    try:
        import sqlite3
        db = ROOT / "build_memory.db"
        if db.exists():
            conn = sqlite3.connect(str(db))
            rows = conn.execute(
                "SELECT project, type, text FROM learnings ORDER BY id DESC LIMIT 10"
            ).fetchall()
            recent_learnings = rows
            conn.close()
    except Exception:
        pass

    # Build _hot.md
    lines = [
        "# Hot Cache — Active Context",
        f"*Auto-updated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}. Read this FIRST.*",
        "",
        "## Current State",
        f"- Portfolio: {total} total, {len(active)} active",
        f"- Tick queue: {len(approved)} approved, {len(pending)} pending",
        f"- Phase 4: {len(experiments)} experiments, {len(backlog)} backlog",
        f"- Next: {session.get('tick_tock', {}).get('next_session_type', '?')}",
        "",
        "## Tick Queue",
    ]

    if approved:
        for a in approved[:5]:
            lines.append(f"- [approved] {a.get('name', '?')}: {a.get('idea', '?')[:60]}")
    else:
        lines.append("- (empty — will brainstorm)")

    if pending:
        for p in pending[:3]:
            lines.append(f"- [pending] {p.get('name', '?')}")

    lines.extend([
        "",
        "## Recent Builds (last 5)",
    ])
    for r in recent:
        lines.append(f"- {r['project']}: {r.get('idea', '?')[:60]}")

    lines.extend([
        "",
        "## Key Patterns (from recent learnings)",
    ])
    if recent_learnings:
        seen = set()
        for proj, typ, text in recent_learnings:
            if typ in ("KEEP", "INSIGHT") and text[:40] not in seen:
                lines.append(f"- [{typ}] {text[:80]}")
                seen.add(text[:40])
                if len(seen) >= 8:
                    break
    else:
        lines.extend([
            "- Always use /* */ not // in JS string literals",
            "- Split http:// as 'http:/' + '/...'",
            "- Pre-compile regexes at init, not in hot paths",
            "- Add CSP meta tag to every new project",
            "- Welcome/tutorial preset improves guide score",
        ])

    lines.append("")

    (ROOT / "_hot.md").write_text("\n".join(lines))
    print(f"_hot.md updated: {len(lines)} lines")


if __name__ == "__main__":
    main()

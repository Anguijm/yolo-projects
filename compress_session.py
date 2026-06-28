#!/usr/bin/env python3
"""compress_session.py — deterministic YOLO session-handoff generator.

Emits a compact, resumable handoff document so a fresh session can pick up
work faster than re-reading the ~287 KB raw session_state.json. Read-only:
shells out to `git log`, reads .harness/session_state.json and _hot.md, and
synthesizes a markdown (default) or JSON (--json) summary covering:

  * recent commits, grouped and de-noised (phase4/merge buckets collapsed)
  * open + deferred council escalations, each with a resolution hint
  * the top-of-queue tick spec (name / type / idea / council_focus)
  * memory-drift flags (live state vs the _hot.md headline cache)

No network, no secrets, no writes to any state file.

Usage:
    python3 compress_session.py                 # markdown to stdout
    python3 compress_session.py --json           # structured JSON
    python3 compress_session.py --out HANDOFF.md # write to a file
    python3 compress_session.py -n 30            # widen the commit window
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

STATE_PATH = os.path.join(".harness", "session_state.json")
HOT_PATH = "_hot.md"

# Commit categories that carry per-item signal vs. ones that should collapse to
# a single de-noised count (the IMPLEMENTATION council_focus).
SIGNAL_CATS = ("tick", "tock", "escalation", "resolve", "fix", "queue", "council")
COLLAPSE_CATS = ("phase4", "merge", "safety-net", "other")


# --------------------------------------------------------------------------- #
# sanitization
# --------------------------------------------------------------------------- #
def _sanitize(text: str) -> str:
    """Neutralize markdown/HTML-active sequences in untrusted strings.

    Commit subjects and escalation reasons are data, not trusted markup. If the
    handoff is ever piped into a markdown/HTML renderer, raw angle brackets or
    backticks could inject active content. We escape angle brackets, defang
    backticks, and flatten any embedded newlines so one record stays one line.
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.replace("\x00", "").replace("\r", " ").replace("\n", " ")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("`", "'")
    return text.strip()


# --------------------------------------------------------------------------- #
# git collection
# --------------------------------------------------------------------------- #
def collect_commits(n: int) -> list[dict]:
    """Return up to `n` recent commits as {hash, parents, subject} dicts.

    Uses NUL field separators. Each record line is split with maxsplit=2 so a
    subject that itself contains a NUL byte is preserved intact rather than
    corrupting the hash/parents fields (per the BUGS gate fix).
    """
    fmt = "%H%x00%P%x00%s"
    try:
        out = subprocess.run(
            ["git", "log", f"-n{int(n)}", f"--pretty=format:{fmt}"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return []
    commits = []
    for line in out.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\x00", 2)
        if len(parts) < 3:
            continue
        h, parents, subject = parts[0], parts[1], parts[2]
        commits.append(
            {
                "hash": h[:9],
                "parents": parents.split() if parents else [],
                "subject": subject,
            }
        )
    return commits


def classify_commit(subject: str, parents: list[str]) -> str:
    """Map a commit to a category label from its subject prefix + merge-ness."""
    if len(parents) >= 2:
        return "merge"
    s = subject.lstrip()
    low = s.lower()
    if low.startswith("escalation"):
        return "escalation"
    if "safety-net" in low:
        return "safety-net"
    if low.startswith("cron(phase4)") or "phase 4" in low or "phase4" in low:
        return "phase4"
    if low.startswith("cron(tock)") or low.startswith("cron(tick-tock)"):
        return "tock"
    if low.startswith("cron(tick)"):
        return "tick"
    if low.startswith("resolve"):
        return "resolve"
    if low.startswith("queue") or low.startswith("drain"):
        return "queue"
    if low.startswith("council"):
        return "council"
    if low.startswith("fix"):
        return "fix"
    return "other"


def group_commits(commits: list[dict]) -> dict:
    """Bucket commits by category; collapse low-signal buckets to a count.

    Signal buckets (tick/tock/escalation/resolve/fix/queue/council) keep their
    individual subjects. Noisy buckets (phase4 daily scans, merge commits,
    safety-net, misc) collapse to a count + newest example so they don't flood
    the handoff (the IMPLEMENTATION council_focus).
    """
    buckets: dict[str, list[dict]] = {}
    for c in commits:
        cat = classify_commit(c["subject"], c["parents"])
        buckets.setdefault(cat, []).append(c)
    signal, collapsed = [], []
    for cat, items in buckets.items():
        if cat in COLLAPSE_CATS:
            collapsed.append(
                {
                    "category": cat,
                    "count": len(items),
                    "newest": _sanitize(items[0]["subject"]),
                }
            )
        else:
            signal.append(
                {
                    "category": cat,
                    "items": [
                        {"hash": i["hash"], "subject": _sanitize(i["subject"])}
                        for i in items
                    ],
                }
            )
    return {"signal": signal, "collapsed": collapsed}


# --------------------------------------------------------------------------- #
# state extraction
# --------------------------------------------------------------------------- #
def load_state(path: str) -> dict:
    """Defensive JSON read with one 100ms retry on race (cron mid-write)."""
    for attempt in (1, 2):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            if attempt == 1:
                time.sleep(0.1)
                continue
            return {}
    return {}


def _approved_queue(state: dict) -> list:
    tt = state.get("tick_tock", {}) if isinstance(state, dict) else {}
    q = tt.get("tick_queue_approved")
    if isinstance(q, list):
        return q
    # tolerate a flattened top-level key (schema drift)
    q = state.get("tick_queue_approved")
    return q if isinstance(q, list) else []


def _pending_queue(state: dict) -> list:
    tt = state.get("tick_tock", {}) if isinstance(state, dict) else {}
    for src in (tt.get("tick_queue_pending"), state.get("tick_queue_pending")):
        if isinstance(src, list):
            return src
    return []


def top_of_queue(state: dict) -> dict | None:
    """Head approved tick spec, sanitized to the resume-relevant fields."""
    q = _approved_queue(state)
    if not q or not isinstance(q[0], dict):
        return None
    head = q[0]
    return {
        "name": _sanitize(head.get("name", "unknown")),
        "type": _sanitize(head.get("type", "yolo")),
        "idea": _sanitize(head.get("idea", "")),
        "council_focus": _sanitize(head.get("council_focus", "")),
        "remaining": len(q),
    }


def resolution_hint(esc: dict) -> str:
    """Derive a one-line 'how to resume' from an escalation record."""
    gate = esc.get("gate", "?")
    reason = (esc.get("reason") or esc.get("deferred_reason") or "").lower()
    if "deadlock" in reason or "2-attempt" in reason or "2 attempt" in reason:
        return f"{gate} gate 2-attempt deadlock — review the cited angle, then resolve via /escalation-resolve."
    if "veto" in reason or "lessons" in reason:
        return f"{gate} gate lessons veto — confirm precondition_evidence citation, then override or fix."
    if esc.get("deferred_reason"):
        return f"deferred: {_sanitize(esc.get('deferred_reason'))[:160]}"
    return f"{gate} gate objection — read the council_{gate}.json verdicts and address required_fix."


def escalations(state: dict) -> dict:
    """Open + deferred escalations, each annotated with a resolution hint."""
    def _norm(lst):
        out = []
        for e in lst if isinstance(lst, list) else []:
            if not isinstance(e, dict):
                continue
            out.append(
                {
                    "project": _sanitize(e.get("project", "unknown")),
                    "gate": _sanitize(e.get("gate", "?")),
                    "reason": _sanitize(e.get("reason") or e.get("deferred_reason") or ""),
                    "hint": resolution_hint(e),
                }
            )
        return out

    return {
        "open": _norm(state.get("council_escalations")),
        "deferred": _norm(state.get("council_escalations_deferred")),
    }


# --------------------------------------------------------------------------- #
# drift detection
# --------------------------------------------------------------------------- #
def parse_hot_counts(path: str) -> dict:
    """Extract headline numbers from _hot.md. Missing/odd lines → partial dict."""
    counts: dict[str, int] = {}
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return counts
    for line in text.splitlines():
        s = line.strip().lstrip("-").strip()
        low = s.lower()
        try:
            if low.startswith("portfolio:"):
                toks = [t for t in s.replace(",", " ").split() if t.isdigit()]
                if len(toks) >= 1:
                    counts["portfolio_total"] = int(toks[0])
                if len(toks) >= 2:
                    counts["portfolio_active"] = int(toks[1])
            elif low.startswith("tick queue:"):
                toks = [t for t in s.replace(",", " ").split() if t.isdigit()]
                if len(toks) >= 1:
                    counts["approved"] = int(toks[0])
                if len(toks) >= 2:
                    counts["pending"] = int(toks[1])
        except ValueError:
            continue
    return counts


def memory_drift_flags(state: dict, hot: dict) -> list[str]:
    """Flag mismatches between the _hot.md headline cache and live state."""
    flags = []
    if not hot:
        return ["_hot.md headline unparseable or missing — cannot verify cache freshness"]
    live_approved = len(_approved_queue(state))
    live_pending = len(_pending_queue(state))
    if "approved" in hot and hot["approved"] != live_approved:
        flags.append(
            f"approved-queue drift: _hot.md says {hot['approved']}, live state has {live_approved}"
        )
    if "pending" in hot and hot["pending"] != live_pending:
        flags.append(
            f"pending-queue drift: _hot.md says {hot['pending']}, live state has {live_pending}"
        )
    portfolio = state.get("portfolio", {}) if isinstance(state, dict) else {}
    for key, hot_key, label in (
        ("total", "portfolio_total", "portfolio-total"),
        ("active", "portfolio_active", "portfolio-active"),
    ):
        live_val = portfolio.get(key)
        if hot_key in hot and isinstance(live_val, int) and hot[hot_key] != live_val:
            flags.append(
                f"{label} drift: _hot.md says {hot[hot_key]}, live state has {live_val}"
            )
    return flags


# --------------------------------------------------------------------------- #
# orchestration + rendering
# --------------------------------------------------------------------------- #
def build_handoff(args) -> dict:
    state = load_state(args.state)
    hot = parse_hot_counts(args.hot)
    commits = collect_commits(args.commits)
    tt = state.get("tick_tock", {}) if isinstance(state, dict) else {}
    return {
        "state_available": bool(state),
        "cadence": {
            "next": _sanitize(tt.get("next_session_type", "unknown")),
            "last": _sanitize(tt.get("last_session_type", "unknown")),
            "last_tock_flagship": _sanitize(
                state.get("last_tock_flagship")
                or tt.get("last_tock_flagship", "unknown")
            ),
        },
        "commit_window": len(commits),
        "commits": group_commits(commits),
        "top_of_queue": top_of_queue(state),
        "escalations": escalations(state),
        "drift": memory_drift_flags(state, hot),
    }


def render_markdown(h: dict) -> str:
    L = ["# Session handoff", ""]
    if not h["state_available"]:
        L.append("> ⚠ session_state.json unavailable — state sections omitted.\n")

    cad = h["cadence"]
    L.append("## Cadence")
    L.append(f"- Next: **{cad['next']}** · Last: {cad['last']} · Last tock flagship: {cad['last_tock_flagship']}")
    L.append("")

    toq = h["top_of_queue"]
    L.append("## Top of queue")
    if toq:
        L.append(f"- **{toq['name']}** ({toq['type']}) — {toq['remaining']} approved remaining")
        if toq["idea"]:
            L.append(f"  - idea: {toq['idea']}")
        if toq["council_focus"]:
            L.append(f"  - council_focus: {toq['council_focus']}")
    else:
        L.append("- none — approved queue empty; next session is tock-eligible")
    L.append("")

    esc = h["escalations"]
    L.append("## Escalations")
    if not esc["open"] and not esc["deferred"]:
        L.append("- none open")
    else:
        for e in esc["open"]:
            L.append(f"- 🔴 OPEN {e['project']} ({e['gate']}) — {e['hint']}")
        for e in esc["deferred"]:
            L.append(f"- ⏸ DEFERRED {e['project']} ({e['gate']}) — {e['hint']}")
    L.append("")

    L.append("## Drift")
    if h["drift"]:
        for f in h["drift"]:
            L.append(f"- ⚠ {f}")
    else:
        L.append("- none — _hot.md cache matches live state")
    L.append("")

    L.append(f"## Recent commits ({h['commit_window']} scanned)")
    cm = h["commits"]
    if not cm["signal"] and not cm["collapsed"]:
        L.append("- (no commits / not a git repo)")
    for grp in cm["signal"]:
        L.append(f"### {grp['category']}")
        for it in grp["items"]:
            L.append(f"- `{it['hash']}` {it['subject']}")
    if cm["collapsed"]:
        L.append("### collapsed (de-noised)")
        for grp in cm["collapsed"]:
            L.append(f"- {grp['category']}: {grp['count']} commit(s); newest: {grp['newest']}")
    L.append("")
    return "\n".join(L)


def render_json(h: dict) -> str:
    return json.dumps(h, indent=2, ensure_ascii=False)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Generate a YOLO session-handoff summary.")
    p.add_argument("-n", "--commits", type=int, default=15, help="commits to scan (default 15)")
    p.add_argument("--json", action="store_true", help="emit structured JSON instead of markdown")
    p.add_argument("--out", default=None, help="write to this path instead of stdout")
    p.add_argument("--state", default=STATE_PATH, help="session_state.json path")
    p.add_argument("--hot", default=HOT_PATH, help="_hot.md path")
    args = p.parse_args(argv)

    if args.commits < 0:
        print("error: --commits must be >= 0", file=sys.stderr)
        return 2

    handoff = build_handoff(args)
    text = render_json(handoff) if args.json else render_markdown(handoff)

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        except OSError as exc:
            print(f"error: could not write {args.out}: {exc}", file=sys.stderr)
            return 1
        print(f"wrote handoff to {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

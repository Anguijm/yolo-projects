#!/usr/bin/env python3
"""Failure-mode audit of resolved council escalations.

Reads `.harness/session_state.json`, iterates `council_escalations_resolved[]`,
and classifies each entry along three orthogonal axes:

  1. Failure-mode class  (what TRIGGERED the escalation; matched on `reason`):
       parse_failure  > goalpost_move > deadlock > lessons_veto
       > two_attempt_unresolved  (priority order, first match wins; else uncategorized)
  2. Objecting angle(s)  (which lens(es) objected; ALL matches collected from `reason`):
       BUGS SECURITY UI GUIDE LESSONS COOL USEFULNESS
  3. Resolution disposition  (signal vs noise; matched on `resolution`, priority order):
       false_positive (noise) > partial (mixed) > accepted_fix (signal) > ambiguous

Signal-to-noise ratio per failure-mode class:
    SNR = accepted_fix / (accepted_fix + false_positive)
`partial` and `ambiguous` rows are EXCLUDED from the SNR denominator but are
reported as separate columns so the ratio is honest about what it omits.

The classifier is keyword/regex-based and therefore approximate. Rows that fall
through to `uncategorized` / `ambiguous` are surfaced in the report for manual
correction. Read-only: opens session_state.json for read, writes one REPORT.md.

Usage:
    python3 audit.py             # write REPORT.md next to this script
    python3 audit.py --print     # render to stdout, write nothing (for review)
    python3 audit.py --state PATH # override session_state.json location
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
DEFAULT_STATE = REPO_ROOT / ".harness" / "session_state.json"
DEFAULT_OUT = HERE / "REPORT.md"

ANGLES = ["BUGS", "SECURITY", "UI", "GUIDE", "LESSONS", "COOL", "USEFULNESS"]

# Failure-mode class: priority-ordered (rule that detects it, in order).
FAILURE_MODE_RULES = [
    ("parse_failure", re.compile(r"unparseable|parse\s+failure|phantom", re.I)),
    ("goalpost_move", re.compile(r"goalpost|same\s+argument|escalated\s+\w+\s*[→>-]+\s*\w+\s+with\s+same|re-?escalat", re.I)),
    ("deadlock", re.compile(r"attempt\s*3|deadlock|3rd\s+consecutive", re.I)),
    ("lessons_veto", re.compile(r"LESSONS\s+VETO")),
    ("two_attempt_unresolved", re.compile(r"unresolved\s+objections\s+after\s+2\s+attempts", re.I)),
]

# Resolution disposition: priority-ordered (first match wins).
# `partial` is evaluated FIRST so an explicit "ACCEPT X + OVERRIDE Y" (or
# "FIXED ..., ... OVERRIDDEN") verdict is scored as mixed before the broad
# `override` token in `false_positive` would swallow it. `false_positive` then
# catches pure overrides; `accepted_fix` catches the remaining legitimate fixes.
DISPOSITION_RULES = [
    # partial = an accept/fix AND an override appear close together in the same
    # resolution (e.g. "BUGS FIXED AT SOURCE, SECURITY OVERRIDDEN"). The {0,60}
    # window is a deliberate same-clause proximity bound, not an arbitrary
    # constant: it requires the two verdicts to co-occur within roughly one
    # clause so that an "accept" and an "override" describing the SAME issue are
    # caught, while an unrelated accept and override paragraphs apart are not.
    # Validated against real data — entries #0/#19 (true partial) match, #21
    # ("fixed at source ... rather than overridden", negated) does not. Widening
    # it reintroduces false partials.
    ("partial", re.compile(r"\bpartial\b|(?:accept|fix\w*)\b.{0,60}(?:overrid|overrul|override)|(?:overrid|overrul|override)\b.{0,60}(?:accept|fix\w*)", re.I)),
    ("false_positive", re.compile(r"false[\s._-]?positive|phantom|\boverrid|\boverrul", re.I)),
    # accepted_fix = the objection was legitimate and the code/plan was fixed.
    # "fixed at source" / "BUGS FIXED" are common phrasings in this repo's history.
    ("accepted_fix", re.compile(r"\bACCEPT|FIX\s+APPLIED|fix(?:ed)?\s+at\s+(?:the\s+)?source|\b(?:BUGS?|SECURITY|UI|GUIDE)\s+FIXED\b|legitimate\s+(?:bug|concern|critique|issue|fix|objection|defect|regression)|\b(?:real|genuine)\s+(?:bug|defect|regression)", re.I)),
]


def load_escalations(state_path=DEFAULT_STATE):
    """Defensively read council_escalations_resolved[] from session_state.json."""
    try:
        with open(state_path, encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        return []
    data = state.get("council_escalations_resolved", [])
    return data if isinstance(data, list) else []


def _classify_failure_mode(reason):
    for name, rx in FAILURE_MODE_RULES:
        if rx.search(reason):
            return name
    return "uncategorized"


def _extract_angles(reason):
    found = []
    for angle in ANGLES:
        # word-boundary, case-sensitive uppercase token (e.g. "SECURITY OBJECT")
        if re.search(r"\b" + angle + r"\b", reason):
            found.append(angle)
    return found


# Negated-override phrases describe the ABSENCE of an override
# (e.g. "fixed at source rather than overridden", "not overridden", "no override").
# Strip them before disposition matching so they don't false-trigger partial/false_positive.
_NEG_OVERRIDE_RE = re.compile(
    r"(?:rather\s+than|instead\s+of|not|no|without|never|pre-?empt\w*\s+\w+\s+)\s*(?:being\s+|getting\s+)?overrid\w*",
    re.I,
)


def _classify_disposition(resolution):
    text = _NEG_OVERRIDE_RE.sub(" ", resolution)
    for name, rx in DISPOSITION_RULES:
        if rx.search(text):
            return name
    return "ambiguous"


def classify(entry):
    reason = entry.get("reason") or ""
    resolution = entry.get("resolution") or ""
    return {
        "project": entry.get("project") or "?",
        "gate": entry.get("gate") or "?",
        "timestamp": entry.get("timestamp") or entry.get("resolved_at") or "?",
        "failure_mode": _classify_failure_mode(reason),
        "angles": _extract_angles(reason),
        "disposition": _classify_disposition(resolution),
        "reason": reason,
    }


def aggregate(rows):
    by_mode = Counter(r["failure_mode"] for r in rows)
    by_gate = Counter(r["gate"] for r in rows)
    by_disposition = Counter(r["disposition"] for r in rows)
    by_angle = Counter(a for r in rows for a in r["angles"])

    # per-class disposition breakdown + SNR
    mode_disp = defaultdict(Counter)
    for r in rows:
        mode_disp[r["failure_mode"]][r["disposition"]] += 1

    snr = {}
    for mode, disp in mode_disp.items():
        signal = disp.get("accepted_fix", 0)
        noise = disp.get("false_positive", 0)
        denom = signal + noise
        snr[mode] = (signal / denom) if denom else None

    # one representative example entry per class (first seen)
    example = {}
    for r in rows:
        example.setdefault(r["failure_mode"], r)

    return {
        "total": len(rows),
        "by_mode": by_mode,
        "by_gate": by_gate,
        "by_disposition": by_disposition,
        "by_angle": by_angle,
        "mode_disp": mode_disp,
        "snr": snr,
        "example": example,
    }


# Human-readable description of the rule that detects each failure mode.
MODE_RULE_DESC = {
    "parse_failure": "reason ~ /unparseable|parse failure|phantom/",
    "goalpost_move": "reason ~ /goalpost|same argument|escalated X→Y with same|re-escalat/",
    "deadlock": "reason ~ /attempt 3|deadlock|3rd consecutive/",
    "lessons_veto": "reason ~ /LESSONS VETO/",
    "two_attempt_unresolved": "reason ~ /unresolved objections after 2 attempts/",
    "uncategorized": "(no failure-mode rule matched — manual review)",
}


def _fmt_snr(v):
    return "n/a" if v is None else f"{v:.0%}"


def render_report(agg, rows):
    lines = []
    lines.append("# Council Escalation Failure-Mode Audit")
    lines.append("")
    lines.append(f"*Generated by `audit.py` over `council_escalations_resolved[]` "
                 f"({agg['total']} resolved escalations).*")
    lines.append("")

    if agg["total"] == 0:
        lines.append("> No resolved escalations found in session_state.json. "
                     "Nothing to classify.")
        lines.append("")
        return "\n".join(lines)

    lines.append("## Method")
    lines.append("")
    lines.append("Each resolved escalation is classified on three orthogonal axes by "
                 "priority-ordered regex (keyword-based, therefore approximate):")
    lines.append("")
    lines.append("1. **Failure-mode class** — what triggered the escalation (matched on `reason`).")
    lines.append("2. **Objecting angle(s)** — which lens(es) objected (all matches collected).")
    lines.append("3. **Resolution disposition** — `accepted_fix` (real signal), "
                 "`false_positive` (noise), `partial` (mixed), or `ambiguous`.")
    lines.append("")
    lines.append("**Signal-to-noise ratio (SNR)** per class = "
                 "`accepted_fix / (accepted_fix + false_positive)`. "
                 "`partial`/`ambiguous` rows are excluded from the SNR denominator "
                 "(shown as separate columns). Rows that fall through to "
                 "`uncategorized`/`ambiguous` are surfaced below for manual correction.")
    lines.append("")

    # --- Per-class table: count, rule, SNR, disposition breakdown, example ---
    lines.append("## Failure modes (signal-to-noise per class)")
    lines.append("")
    lines.append("| Failure mode | Count | Detecting rule | accepted_fix | false_positive | partial | ambiguous | SNR |")
    lines.append("|---|---:|---|---:|---:|---:|---:|---:|")
    for mode, count in agg["by_mode"].most_common():
        disp = agg["mode_disp"][mode]
        lines.append(
            f"| `{mode}` | {count} | {MODE_RULE_DESC.get(mode, '?')} | "
            f"{disp.get('accepted_fix', 0)} | {disp.get('false_positive', 0)} | "
            f"{disp.get('partial', 0)} | {disp.get('ambiguous', 0)} | "
            f"{_fmt_snr(agg['snr'].get(mode))} |"
        )
    lines.append("")

    # --- Per-class example ---
    lines.append("## Example per class")
    lines.append("")
    for mode, _ in agg["by_mode"].most_common():
        ex = agg["example"][mode]
        reason = ex["reason"].replace("\n", " ")
        if len(reason) > 200:
            reason = reason[:197] + "..."
        lines.append(f"- **`{mode}`** — _{ex['project']} / {ex['gate']}_: {reason}")
    lines.append("")

    # --- By gate ---
    lines.append("## By gate")
    lines.append("")
    lines.append("| Gate | Escalations |")
    lines.append("|---|---:|")
    for gate, count in agg["by_gate"].most_common():
        lines.append(f"| {gate} | {count} |")
    lines.append("")

    # --- By angle ---
    lines.append("## By objecting angle")
    lines.append("")
    lines.append("| Angle | Times it objected |")
    lines.append("|---|---:|")
    for angle, count in agg["by_angle"].most_common():
        lines.append(f"| {angle} | {count} |")
    lines.append("")

    # --- Overall disposition ---
    lines.append("## Overall disposition")
    lines.append("")
    lines.append("| Disposition | Count |")
    lines.append("|---|---:|")
    for disp, count in agg["by_disposition"].most_common():
        lines.append(f"| {disp} | {count} |")
    total_signal = agg["by_disposition"].get("accepted_fix", 0)
    total_noise = agg["by_disposition"].get("false_positive", 0)
    overall_denom = total_signal + total_noise
    overall_snr = (total_signal / overall_denom) if overall_denom else None
    lines.append("")
    lines.append(f"**Overall SNR** (accepted_fix vs false_positive) = `{_fmt_snr(overall_snr)}` "
                 f"({total_signal} signal / {total_noise} noise).")
    lines.append("")

    # --- Recommendations ---
    lines.append("## Recommendations")
    lines.append("")
    recs = []
    for mode, _ in agg["by_mode"].most_common():
        s = agg["snr"].get(mode)
        count = agg["by_mode"][mode]
        if s is not None and s < 0.4 and count >= 3:
            recs.append(f"- `{mode}` has low SNR ({_fmt_snr(s)}) over {count} cases — "
                        f"candidate for a tighter auto-downgrade rule (mostly noise).")
        elif s is not None and s >= 0.7 and count >= 3:
            recs.append(f"- `{mode}` has high SNR ({_fmt_snr(s)}) over {count} cases — "
                        f"this class reliably surfaces real defects; keep enforcing.")
    if agg["by_mode"].get("uncategorized", 0):
        recs.append(f"- {agg['by_mode']['uncategorized']} escalation(s) are `uncategorized` — "
                    f"extend the failure-mode rules or hand-label them.")
    if agg["by_disposition"].get("ambiguous", 0):
        recs.append(f"- {agg['by_disposition']['ambiguous']} resolution(s) are `ambiguous` — "
                    f"the disposition classifier could not score signal vs noise; review by hand.")
    if not recs:
        recs.append("- No class crosses the low/high-SNR thresholds at the current sample size.")
    lines.extend(recs)
    lines.append("")

    # --- Per-row appendix (audit trail) ---
    lines.append("## Appendix — per-escalation classification")
    lines.append("")
    lines.append("| # | Project | Gate | Failure mode | Angles | Disposition |")
    lines.append("|---:|---|---|---|---|---|")
    for i, r in enumerate(rows):
        angles = ", ".join(r["angles"]) or "—"
        lines.append(f"| {i} | {r['project']} | {r['gate']} | `{r['failure_mode']}` | "
                     f"{angles} | `{r['disposition']}` |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Failure-mode audit of resolved council escalations.")
    parser.add_argument("--state", default=str(DEFAULT_STATE),
                        help="path to session_state.json (default: repo .harness/session_state.json)")
    parser.add_argument("--print", dest="to_stdout", action="store_true",
                        help="render to stdout and write nothing")
    args = parser.parse_args(argv)

    entries = load_escalations(args.state)
    rows = [classify(e) for e in entries]
    agg = aggregate(rows)
    report = render_report(agg, rows)

    if args.to_stdout:
        print(report)
    else:
        # Output is fixed inside this experiment dir — not a user-supplied sink.
        DEFAULT_OUT.write_text(report, encoding="utf-8")
        print(f"{agg['total']} escalations classified -> {DEFAULT_OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

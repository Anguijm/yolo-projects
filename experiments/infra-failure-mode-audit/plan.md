# Plan — infra-failure-mode-audit

## Goal
Produce a structured failure-mode taxonomy of the resolved council escalations (`session_state.council_escalations_resolved[]`) with per-class counts, the rule that detected each class, an example, and a signal-to-noise ratio per class — giving empirical grounding for future council enforcement tuning.

## Scope
**In scope:**
- `experiments/infra-failure-mode-audit/audit.py` (~140 LOC): a read-only classifier that loads `.harness/session_state.json`, iterates `council_escalations_resolved[]`, and classifies each entry along three orthogonal axes (failure-mode class, objecting angle(s), resolution disposition), then renders `REPORT.md`.
- `experiments/infra-failure-mode-audit/REPORT.md`: generated report.

**Explicitly NOT in scope:**
- No changes to `council.py`, `session_state.json`, or any runtime pipeline file. This tick is read-only analysis; it does not alter enforcement behavior.
- No new directory at repo root (infrastructure ticks live under `experiments/`).
- No network, no DB, no external deps — pure stdlib (`json`, `re`, `collections`, `argparse`, `pathlib`).
- The rationale references "17 resolved escalations"; the data has since grown to 65. The script reads whatever count is present (no hardcoded N).

## Approach
Three orthogonal classification axes, each a priority-ordered regex applied to `reason` and/or `resolution` text (extending the priority-ordered classifier pattern from `infra-memory-feedback`):

1. **Failure-mode class** (axis = what *triggered* the escalation, matched on `reason`, priority order, first match wins):
   - `parse_failure` — `unparseable|parse failure|phantom`
   - `goalpost_move` — `goalpost|same argument|escalated\s+\w+→\w+ with same|re-?escalated`
   - `deadlock` — `attempt 3|deadlock|3rd consecutive`
   - `lessons_veto` — `LESSONS\s+VETO`
   - `two_attempt_unresolved` — `unresolved objections after 2 attempts` (the default/catch-all)
   - `uncategorized` — none matched (surfaced for manual review)

2. **Objecting angle(s)** (axis = which lens objected, matched on `reason`, ALL matches collected): scan for the 7 angle tokens `SECURITY|BUGS|UI|GUIDE|LESSONS|COOL|USEFULNESS` (word-boundary, uppercase) so multi-angle escalations are credited to each angle.

3. **Resolution disposition** (axis = signal vs noise, matched on `resolution`, priority order):
   - `false_positive` (noise) — `false[\s._-]?positive|phantom|override.*(veto|object)|overrule`
   - `partial` (mixed) — `partial|accept.*override|override.*accept` (both an accept and an override present)
   - `accepted_fix` (signal) — `\bACCEPT|FIX\s+APPLIED|legitimate\s+(bug|concern|critique|issue|fix|objection|defect|regression)|\b(real|genuine)\s+(bug|defect)`
   - `ambiguous` — none matched.

Disposition order matters: `false_positive` is checked before `accepted_fix` because override resolutions often contain the word "accept" in other clauses; `partial` catches the explicit mixed verdicts. This mirrors the "FP first, then prevented, else irrelevant" priority discipline validated in `infra-memory-feedback`.

**Signal-to-noise ratio** per failure-mode class = `accepted_fix / (accepted_fix + false_positive)` (partials and ambiguous excluded from the denominator, but reported as separate columns so the ratio is honest about what it omits). A class with high SNR means escalations of that class usually surfaced real defects; low SNR means that class is mostly noise and is a candidate for an auto-downgrade rule.

**Subtask sequencing:**
1. `load_escalations()` — read session_state.json defensively, return the list (subtask 0, no deps).
2. `classify(entry)` — apply all three axes to one entry, return a dict (depends on 1's schema).
3. `aggregate(rows)` — collections.Counter rollups by class, by angle, by disposition, plus per-class SNR (depends on 2).
4. `render_report(agg, rows)` — emit Markdown tables (depends on 3).
5. `main()` — wire 1→2→3→4, write REPORT.md, support `--print` (stdout, no write) for the tests gate (depends on all).

## File Layout
- `experiments/infra-failure-mode-audit/audit.py` — NEW, ~140 LOC.
- `experiments/infra-failure-mode-audit/REPORT.md` — NEW, generated.
- `experiments/infra-failure-mode-audit/plan.md` — this file.
- `experiments/infra-failure-mode-audit/changes.md` — written at IMPLEMENTATION gate.
- No existing files modified.

## Function Map
Grouped by `experiments/infra-failure-mode-audit/audit.py`:
- `load_escalations(state_path) -> list[dict]` — defensive JSON read; returns `council_escalations_resolved` or `[]`.
- `_classify_failure_mode(reason: str) -> str` — priority-ordered regex → one class string.
- `_extract_angles(reason: str) -> list[str]` — collect all 7-angle tokens present.
- `_classify_disposition(resolution: str) -> str` — priority-ordered regex → one disposition string.
- `classify(entry: dict) -> dict` — combine the three above + carry through project/gate/timestamp.
- `aggregate(rows: list[dict]) -> dict` — Counters + per-class SNR computation.
- `render_report(agg: dict, rows: list[dict]) -> str` — build the Markdown string.
- `main(argv=None) -> int` — argparse (`--print`, `--state`, `--out`), orchestration, file write.

## Security
- Read-only. Opens exactly one file (`.harness/session_state.json`) for read, writes exactly one file (`REPORT.md`) inside the experiment dir. No `eval`, no `exec`, no shell, no network, no user-supplied paths beyond optional CLI flags that default to repo-relative constants.
- Regex inputs come from trusted, repo-internal session state (not external/user input); no ReDoS exposure of concern, but patterns are linear (no nested quantifiers on overlapping classes).
- Output is Markdown written to a fixed path; no injection sink (not rendered as HTML by the pipeline).

## UI
N/A — CLI script. Output UX: two run modes — default writes `REPORT.md` and prints a one-line summary (`N escalations classified → REPORT.md`); `--print` streams the report to stdout without writing (used by the tests gate for inspection). Empty-data state: if zero escalations, the report still renders with a "no data" note rather than crashing.

## Guide
- Module docstring documents the three axes, the priority order of each classifier, and the SNR formula's exclusions.
- CLI `--help` lists `--print`, `--state PATH`, `--out PATH` with defaults.
- REPORT.md opens with a "Method" section stating the classifier is keyword-based and approximate, and that `uncategorized`/`ambiguous` rows are surfaced for manual correction.

## Edge Cases
- Missing/malformed session_state.json → `load_escalations` returns `[]`, report renders "no data" note, exit 0.
- Entry missing `reason` or `resolution` key → treated as empty string (`.get(k, '') or ''`), classifies as `uncategorized`/`ambiguous`.
- Multi-angle reason (e.g. "BUGS critical + SECURITY high") → each angle counted once via set.
- Resolution containing both "OVERRIDE" and "ACCEPT" (genuinely mixed) → `false_positive` regex would match first; `partial` pattern (`accept.*override|override.*accept`) is checked before `accepted_fix` and after `false_positive` — documented limitation: a mixed verdict where the override clause dominates is conservatively scored as noise. Surfaced in the per-row table so a human can spot-correct.
- SNR denominator zero (class has only partial/ambiguous rows) → render `n/a` not a ZeroDivisionError.
- Data count drift (17 → 65 → more) → no hardcoded counts anywhere.

## Test Strategy
- `python3 -c "import ast; ast.parse(open('experiments/infra-failure-mode-audit/audit.py').read())"` — syntax.
- `python3 experiments/infra-failure-mode-audit/audit.py --print` — runs end-to-end on the real 65 entries, exits 0, emits non-empty report.
- **Hand-annotated subset check** (council TESTS gate): manually classify the first ~8 escalations (e.g. entry 0 = implementation/SECURITY/accepted_fix; entry 1 = implementation/UI/false_positive; entry 3 = plan/deadlock/false_positive) and confirm the script's output matches on class + disposition for that subset.
- Verify `uncategorized` and `ambiguous` counts are low (classifier coverage sanity).
- Re-run determinism: two consecutive runs produce byte-identical REPORT.md.

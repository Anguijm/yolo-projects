# Changes — infra-failure-mode-audit

Read-only analysis tick. No runtime pipeline file was modified. Two new files
under `experiments/infra-failure-mode-audit/`.

## New files

### `audit.py` (~210 LOC)
Classifier + report generator over `session_state.council_escalations_resolved[]`.

- `load_escalations(state_path)` — defensive JSON read; returns `[]` on any
  OSError/ValueError or non-list payload (handles missing/malformed state).
- `_classify_failure_mode(reason)` (`FAILURE_MODE_RULES`, priority-ordered) —
  `parse_failure` > `goalpost_move` > `deadlock` > `lessons_veto` >
  `two_attempt_unresolved` > `uncategorized`.
- `_extract_angles(reason)` — collects all of
  `BUGS SECURITY UI GUIDE LESSONS COOL USEFULNESS` present (word-boundary,
  uppercase) so multi-angle escalations credit each angle.
- `_classify_disposition(resolution)` (`DISPOSITION_RULES`, priority-ordered) —
  `partial` > `false_positive` > `accepted_fix` > `ambiguous`.
  - `_NEG_OVERRIDE_RE` strips negated-override phrases ("fixed at source rather
    than overridden", "not overridden", "no override") BEFORE matching so they
    don't false-trigger `partial`/`false_positive`. (Caught on real entry #21.)
- `classify(entry)` — combines the three axes + carries project/gate/timestamp.
- `aggregate(rows)` — Counters by mode/gate/disposition/angle, per-class
  disposition breakdown, per-class SNR, first-seen example per class.
- `render_report(agg, rows)` — Markdown: Method, per-class SNR table, examples,
  by-gate, by-angle, overall disposition + overall SNR, Recommendations
  (low-SNR ≥3 cases → tighten; high-SNR ≥3 → keep), per-row appendix.
- `main(argv)` — argparse: `--state PATH` (default repo `.harness/session_state.json`),
  `--print` (stdout, no write). Output path is FIXED inside the experiment dir
  (`DEFAULT_OUT`); there is no arbitrary `--out` write sink.

### `REPORT.md` (generated)
Audit over the 65 resolved escalations. Headline findings:
- Overall SNR (accepted_fix vs false_positive) = 50% (23 signal / 23 noise).
- `lessons_veto` (0% SNR, n=5) and `goalpost_move` (20% SNR, n=5) are the
  lowest-signal classes — empirically validating the existing auto-downgrade
  rules that already target exactly those two classes (LESSONS-veto
  precondition_evidence enforcement + goalpost-move auto-downgrade).
- `deadlock` (100%, n=2) and `two_attempt_unresolved` (57%, n=44) carry real signal.
- By angle: BUGS objected most (26), then SECURITY (17), UI (11).

## Council-objection handling (advisory — PLAN gate)
PLAN gate (attempt 1) ran twice (Gemini non-determinism): once all-7-APPROVE,
once SECURITY OBJECT (high, arbitrary `--state`/`--out` paths) + GUIDE OBJECT
(low, no README). Council is advisory and never blocks the drain. Addressed
cheaply where real: removed the arbitrary `--out` write sink (output fixed to
the experiment dir); `--state` retained for testability, defaulting to the repo
path and only ever opened for READ. GUIDE's README objection treated as advisory
— REPORT.md's "Method" section + the module docstring document usage; a separate
README would duplicate that. Verdict JSON saved at `council_plan.json`.

## Verification
- `python3 -c "import ast; ast.parse(...)"` — passes.
- `python3 audit.py` — classifies 65, writes REPORT.md, deterministic (two runs
  byte-identical).
- Hand-annotated subset (entries 0,1,3,19,21,49) — all 6 match on
  failure-mode + disposition.

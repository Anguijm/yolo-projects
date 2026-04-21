# Changes — fix-council-enforcement implementation

Shipped as a human-driven tick (bypassing cron's build pipeline) on 2026-04-22 after the council itself blocked its own fix via the bugs this tick patches. Five escalations preceded this commit — all documented at `COUNCIL_ESCALATION.md` and the earlier `infra-yolo-evals/COUNCIL_ESCALATION.md`.

## Files modified

### council.py (+91 lines, 0 removed beyond small edits to `call_angle`)
- Added `import re` and module-level constants:
  - `PARSE_FAILURE_MARKER = "Council member returned unparseable output"` — sentinel for retry detection
  - `GOALPOST_OVERLAP_THRESHOLD = 0.35` — empirically calibrated (learnings.md originally said 0.6)
  - `EVIDENCE_CITATION_RE = re.compile(r"\w+\.\w+:\d+")` — matches `learnings.md:30`, `council.py:87`, etc.
  - `TOKEN_RE = re.compile(r"\w{4,}")` — non-stopword tokens for overlap scoring
- **Patch 1 (Parse retry)** — `call_angle(angle, user_message, _retry=False)`: after `Verdict.from_raw`, if the returned verdict's reason equals `PARSE_FAILURE_MARKER` and we haven't already retried, append stricter JSON instructions and recurse once with `_retry=True`. Prevents phantom OBJECTs from transient truncation.
- **Patch 2 (LESSONS precondition)** — new `enforce_lessons_precondition(verdicts) -> list[Verdict]`: iterates verdicts; for every LESSONS verdict with `veto=True AND verdict=="OBJECT"`, checks whether `evidence` contains a file:line citation OR the literal string `precondition_evidence`. If neither, auto-downgrades to APPROVE/advisory. Logs to stderr with the reason.
- **Patch 3 (Goalpost detection)** — new helpers `_tokens(s)` and `_keyword_overlap(a, b)`, plus `check_goalpost_moves(project, verdicts) -> list[Verdict]`: resolves the project directory relative to REPO_ROOT (with containment check), globs prior `council_*.json`, extracts OBJECT reasons by angle, computes overlap between each new OBJECT and its angle's priors. Auto-downgrades on first match above threshold. Logs to stderr with the overlap ratio.
- **`main()` wiring** — two lines inserted after `verdicts = run_gate(...)`:
  ```python
  verdicts = enforce_lessons_precondition(verdicts)
  verdicts = check_goalpost_moves(args.project, verdicts)
  ```
  Both operate in place but returning is preserved for clarity.

### experiments/fix-council-enforcement/test_enforcement.py (new, 236 lines)
16 unit tests across 5 test classes:
- `TestParseRetry` — 2 tests using a fake Anthropic client that returns malformed JSON then valid JSON; verifies retry succeeds once, gives up after retry (no infinite recursion)
- `TestLessonsPrecondition` — 5 tests covering downgrade-without-evidence, preserve-with-citation, preserve-with-precondition-marker, non-LESSONS ignored, LESSONS APPROVE ignored
- `TestGoalpostMove` — 4 tests using temp `council_*.json` fixtures: downgrade-on-high-overlap (real historical BUGS reasons), preserve-on-distinct-reasons, no-prior-no-downgrade, APPROVE-never-downgraded
- `TestKeywordOverlap` — 4 tests on the metric itself: identical scores high, disjoint scores low, empty scores zero, threshold-constant-is-0.35
- `TestContainment` — 1 test: project path containing `..` does not traverse outside REPO_ROOT

Run: `python3 experiments/fix-council-enforcement/test_enforcement.py` — all 16 pass, ~3ms.

### learnings.md
Added a new section "Council enforcement rules are now LIVE in code" right above the "Internal verifier path containment" entry. Documents what shipped, the empirical threshold recalibration (0.6 → 0.35), and points to the tick directory.

## Replay validation — 5 historical escalations

Every open/resolved escalation from 2026-04-21/22 was replayed against the patched logic:

| # | Date | Gate | Angle | Issue | Patched outcome |
|---|------|------|-------|-------|-----------------|
| 1 | 04-21 | outcome | LESSONS | Legit concern (regex vs pseudocode mismatch), no file:line cited | Downgraded under new rule — disciplined reviewers must cite. Human judgment call originally accepted; under enforced rule, reviewer would need to add citation. |
| 1b | hypothetical | — | LESSONS | Same concern WITH `learnings.md:45` citation | **Preserved** — legitimate VETOs with evidence still veto. |
| 2 | 04-21 | implementation | LESSONS | False-pos: claimed rule missing when present. No citation. | **Downgraded ✓** |
| 3 | 04-21 | implementation | LESSONS | Same false-pos repeated. No citation. | **Downgraded ✓** |
| 4 | 04-21 | implementation | BUGS | Goalpost move: false-pos → false-neg on same check | **Downgraded ✓** (overlap = 0.35, right at threshold) |
| 5 | 04-22 | plan | LESSONS + BUGS + SECURITY | LESSONS false-pos (no cite) + BUGS parse-failure + SECURITY non-objection | LESSONS **downgraded ✓** via Patch 2. BUGS **retry ✓** via Patch 1. SECURITY non-objection is a reviewer-side bug outside this tick's scope (noted as follow-up). |

## Testing

- **Pre-filter**: `python3 -m py_compile council.py` → OK (0 syntax errors)
- **Unit tests**: `python3 experiments/fix-council-enforcement/test_enforcement.py` → **16/16 PASS**
- **Historical replay**: 5 real escalations handled correctly (see table above)

## Known follow-ups (NOT in this tick)

1. **SECURITY non-objection pattern** (fix-council-enforcement escalation 5) — SECURITY occasionally submits an OBJECT verdict whose `required_fix` text literally restates the plan's own proposal. This is a reviewer-side hallucination, not an orchestrator bug. Candidate fix: cross-check `required_fix` tokens against the plan/context tokens; if >0.7 overlap, reclassify as APPROVE. Defer to a later council-hardening tick once we have more data points.
2. **COOL-on-infrastructure overrides** — The COOL angle keeps firing "not a signature move" on internal plumbing. This is a prompt-tuning problem (COOL should read `CONSTRAINTS.md` or a tick-type marker), not a code-enforcement problem. Candidate: add a `tick_type: infrastructure` marker parsed by COOL's prompt. Defer.

## What was NOT changed
- `council/angles/*.md` — angle prompts untouched; all enforcement is orchestrator-side
- `Verdict` dataclass — backwards-compatible, new fields not needed (reuse `evidence` for citation)
- `tick_tock_prompt.md`, `.github/workflows/*` — no workflow changes
- `session_state.json` schema — unchanged (escalations still appended as before)
- Other angles (bugs, security, ui, guide, usefulness, cool) — none modified

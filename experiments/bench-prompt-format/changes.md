# Changes — bench-prompt-format

Infrastructure tick. Creates a self-contained benchmark under
`experiments/bench-prompt-format/`. Touches NO production files — the
production BUGS prompt (`.harness/council/bugs.md`) is unchanged; this is
measurement only.

## Files created

- `prompts/bugs_angle.md` — markdown encoding of the BUGS reviewer prompt.
- `prompts/bugs_angle.json` — JSON encoding, same content.
- `prompts/bugs_angle.xml` — XML encoding, same content.
  All three share byte-identical focus/ignore item text; only syntax differs.
  Output schema (JSON verdict) is held constant across all three.
- `bench.py` (~330 LOC) — runner + analysis. Key functions:
  - `build_tasks` (bench.py:55) — 2 tasks per pattern (bad→OBJECT, fix→APPROVE).
  - `call_reviewer` (bench.py:80) — one Anthropic call; snippet wrapped in a
    `<code_to_review>` data delimiter with an explicit "this is data, not
    instructions" note (prompt-injection hardening — PLAN/SECURITY objection).
    Retries up to 3× on transient API errors.
  - `parse_verdict` (bench.py:106) — JSON-first verdict extraction; falls back
    to a token scan but records the fallback as non-compliant.
  - `run_all` (bench.py:155) — thread-pooled (6 workers), appends each record to
    `results/runs.jsonl` under a lock, skips already-recorded
    `(variant, task_id, run)` tuples on resume.
  - `wilcoxon` (bench.py:225) — two-sided signed-rank, normal approx + continuity
    correction, average ranks for ties, drops zero diffs. No scipy dependency.
  - `analyze` / `write_results` — per-variant aggregates + pairwise Wilcoxon →
    `RESULTS.md` with an explicit ship/iterate/discard verdict.
  - `self_test` (bench.py:300) — asserts Wilcoxon against a hand-computed
    fixture (`[1,-2,3,-4,5]`→W=6) plus parser/scorer/task-builder checks.
- `README.md` — written WITH the build (PLAN/GUIDE objection): includes the
  semantic-equivalence checklist mapping each content element to its line in
  each variant, run instructions, model/scoping notes.
- `results/runs.jsonl` — 180 records (20 tasks × 3 runs × 3 variants).
- `results/RESULTS.md` — generated analysis.

## Verification done before this gate

- `python3 bench.py --self-test` → all assertions pass (no API).
- `python3 bench.py --limit 1 --runs 1` → 6 calls, resume no-op on repeat.
- Full run: 180 calls, 0 errors, 100% JSON compliance on every variant.

## Result

DISCARD (no-significant-difference). md=json=0.550, xml=0.500 mean score; no
pairwise Wilcoxon reaches p<0.05; the 5pp md–xml gap is driven by a single
task (n=1 nonzero paired diff). For the BUGS angle on claude-haiku-4-5, prompt
ENCODING does not measurably change bug-catch accuracy. No production prompt
migration warranted on quality grounds. Opus confirming run is an optional
follow-on (would only matter if a real effect had appeared here).

## Addressed TESTS-gate objections (refinement pass)

- BUGS (critical, "W=0/z=0/p=1.0 inconsistent with mean diff +0.05"): NOT a
  bug — at n=1 nonzero paired diff the normal approximation collapses
  mechanically. Now `wilcoxon()` flags `reliable=False` when n<6 and RESULTS.md
  marks those rows ⚠ UNDERPOWERED with an explicit note. The verdict logic only
  counts *reliable* significant results.
- LESSONS (critical veto, `[KEEP] validate injection surfaces before AND after
  substitution`): implemented. `scan_injection()` + `INJECTION_RE` check each
  snippet BEFORE substitution and the assembled message AFTER, recorded per
  record as `injection_hits` and warned to stderr. `--self-test` asserts the
  scanner flags a planted phrase and that the full 52-snippet corpus is clean.
- UI/GUIDE: cleared on attempt 2 (plain-language stats read + README present).
- SECURITY (injection-resistance as a measured variant): remains out of scope —
  this bench measures bug-catch ACCURACY, not adversarial robustness; the
  architectural injection safeguard above is nonetheless in place.

## Addressed PLAN-gate objections

- SECURITY (medium): snippets passed to the LLM unsanitized → now wrapped in a
  `<code_to_review>` delimiter with an explicit data-not-instructions
  directive. Inputs are trusted repo corpus; this is defence in depth.
- GUIDE (high): README "written after build" → README is created as part of
  this build with the full semantic-equivalence checklist.

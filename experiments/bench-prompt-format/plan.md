# Plan: bench-prompt-format

## Goal
Produce empirical data on whether the same prompt content rendered in
markdown, JSON, or XML produces measurably different output quality from
Claude on the YOLO loop's most-used review prompt — the BUGS angle. Decide
whether wholesale prompt-format migration is worth pursuing based on real
numbers, not blog claims.

## Scope

**In:**
- Three variants of the BUGS angle prompt (currently lives in `council.py`)
  with identical semantic content, differing only in syntactic format.
- A 20-task eval suite reusing `eval_bugs.json` (already in repo).
- A bench runner that calls `experiments/eval-harness/eval_harness.py`.
- N=3 runs per (variant, task) to control for sampling noise.
- A `RESULTS.md` reporting: per-variant mean score, prompt token cost,
  output token cost, run-to-run variance, Wilcoxon signed-rank significance
  test, and format-compliance rate (did the model return the format we
  asked for).

**Out:**
- Migrating any production prompts. This tick is measurement only. A
  follow-on tick handles migration if results justify it.
- Other angles (LESSONS, SECURITY, etc). One angle is enough for a first
  signal; the BUGS angle gives the sharpest pass/fail.
- Multi-model comparison. Claude Opus 4.7 only.
- Bootstrapped confidence intervals or fancy stats. Wilcoxon at this N is
  enough to clear noise and matches what the council actually does today.

## Approach

### Why the BUGS angle
1. **Real, in-use prompt** — the BUGS persona (`.harness/council/bugs.md`)
   is the most-fired council angle; results have direct loop relevance.
2. **Existing planted-bug corpus:** `eval_bugs.json` holds 26 mined bug
   patterns, each with an `example_bad` (the bug) and an `example_fix`
   (the corrected, clean version). NOTE: `eval_bugs.py` is a *regex*
   scanner, not an LLM judge — it does not call the BUGS angle. So this
   bench builds its own LLM classification task on top of the corpus:
   present each snippet to the BUGS reviewer and ask for an APPROVE
   (clean) / OBJECT (bug) verdict.
3. **Sharp, judge-free signal** — score = does the reviewer's verdict
   match the snippet's ground-truth label? `example_bad` → OBJECT is a
   correct catch; `example_fix` → APPROVE is a correct clear. Including
   BOTH the buggy and the clean version of each pattern guards against a
   "always say OBJECT" reviewer scoring 100% — false positives are
   penalised symmetrically. No rubric, no LLM-as-judge.

### What "same semantic content" means
The three variants encode the same:
- Role description
- Definition of what counts as a bug
- Expected output schema (verdict + reason + cited file:line)
- Examples (if the current prompt has them)

What differs across the three is ONLY the encoding of the *instruction*:
- **Markdown variant** — current shape: headings + bullet lists + prose.
- **JSON variant** — top-level object with `role`, `focus_on`, `ignore`,
  `output_schema`, `instruction` keys; instructions are JSON strings.
- **XML variant** — `<role>`, `<focus>`, `<ignore>`, `<output_schema>`,
  `<instruction>` tags following Anthropic's documented convention.

**Controlled variable — output format held constant.** All three variants
request the SAME JSON verdict as output (the shape the production BUGS
angle already emits). We vary only the prompt encoding, not the requested
output, so answer-correctness scoring is apples-to-apples and the verdict
parser is identical for all three. Compliance rate = did the model return
parseable JSON (one shared parser). Letting each variant request a
different output format would confound prompt-encoding effect with
output-parsing fragility; we measure the former cleanly and report
compliance as a separate column.

The validation step at council PLAN review must confirm the three are
actually semantically equivalent — content drift across formats is the
single most likely way this experiment produces a misleading result.
`README.md` ships a content-element checklist mapping each semantic
element to its line in each of the three files for side-by-side diffing.

### Why N=3 with a signed-rank test
Stochasticity: same prompt + same input ≠ same output. Three runs per
variant per task gives 60 data points per variant, enough to detect a
≥5pp score difference at p<0.05 via Wilcoxon. Lower N risks claiming a
difference that's noise.

### Stopping criterion
Run all 20 tasks to completion regardless of early signals. Premature
stopping inflates effect sizes.

## File Layout
- `experiments/bench-prompt-format/plan.md` — this file.
- `experiments/bench-prompt-format/README.md` — written after build.
- `experiments/bench-prompt-format/prompts/bugs_angle.md` — markdown variant.
- `experiments/bench-prompt-format/prompts/bugs_angle.json` — JSON variant.
- `experiments/bench-prompt-format/prompts/bugs_angle.xml` — XML variant.
- `experiments/bench-prompt-format/bench.py` — runner (~120 LOC).
- `experiments/bench-prompt-format/results/runs.jsonl` — per-task per-variant per-run records (resumable).
- `experiments/bench-prompt-format/results/RESULTS.md` — final analysis.

## Function Map
`bench.py`:
- `build_tasks(limit: int|None) -> list[dict]` — from `eval_bugs.json`
  emit two tasks per pattern: `{id, snippet, expected}` for `example_bad`
  (expected=OBJECT) and `example_fix` (expected=APPROVE).
- `load_variant(name: str) -> str` — read prompt file from `prompts/`.
- `call_reviewer(system_prompt: str, snippet: str, model: str) -> str` —
  one Anthropic API call; returns raw text. Retries on transient errors.
- `parse_verdict(raw: str) -> tuple[str|None, bool]` — extract
  APPROVE/OBJECT from JSON output; returns (verdict, parsed_ok).
- `score_record(verdict: str|None, expected: str) -> float` — 1.0 if
  verdict == expected else 0.0 (None → 0.0).
- `run_all(variants, tasks, model, n, out_path) -> None` — fan out calls
  over a small thread pool, append every record to runs.jsonl, skip
  already-recorded `(variant, task_id, run)` tuples on resume.
- `wilcoxon(diffs: list[float]) -> dict` — signed-rank test on paired
  per-task mean-score differences; statistic + approximate p-value.
- `compliance_rate(records, variant) -> float` — fraction of a variant's
  outputs that parsed cleanly as JSON.
- `analyze(records) -> dict` / `write_results(stats, path)` — aggregate
  per-variant mean, variance, compliance, pairwise Wilcoxon → RESULTS.md.
- `main()` — argparse (`--model --runs --limit --variants`) → build_tasks
  → run_all → analyze → write_results.

Scoring is a direct label match (no rubric module needed — the BUGS task
is binary classification, not free-text rubric scoring, so reusing
`eval_harness.run_eval`/`rubric.score` would add indirection without
value; we record raw verdicts to runs.jsonl and score inline).

## Security
No external input parsed. Reads its own prompts; calls Claude API; writes
to its own results directory. No new trust boundaries. API key handled
via existing `ANTHROPIC_API_KEY` env var convention; never logged.

## UI
Not applicable: infrastructure.

## Guide
Not applicable: no user-facing copy.

## Edge Cases
- **API failure mid-run**: bench writes to runs.jsonl after every task;
  on restart, skip already-recorded `(variant, task_id, run_id)` tuples.
- **Variant produces unparseable output**: counts as score=0 for that
  task. Recorded separately as a format-compliance failure — itself a
  signal worth reporting (one variant being more parser-fragile is
  evidence even if the answer-correctness scores tie).
- **All three variants score within noise**: expected ~30% likely. The
  RESULTS.md template includes an explicit "no significant difference"
  conclusion path with the headline "format does not matter for this
  prompt." That's a valid result.
- **Model returns prose when asked for JSON/XML**: recorded in the
  format-compliance column, separate from answer-correctness.

## Test Strategy
- **Smoke test**: `python3 bench.py --limit 1` — one task, one run per
  variant. Verify all three outputs land in runs.jsonl with parseable
  structure and that resumption works (run twice; second run does
  nothing).
- **Full run**: 20 tasks × 3 variants × 3 runs = 180 API calls.
- **Semantic-equivalence audit**: manually inspect 5 random variant pairs
  to confirm the three prompts really are semantically equivalent. Diff
  the parsed instruction trees if possible.
- **Statistical sanity**: `scipy` is NOT installed in this environment,
  so the Wilcoxon implementation is verified against a hand-computed
  textbook fixture with a known statistic/p-value instead of against
  `scipy.stats.wilcoxon`. The fixture and expected values are asserted in
  `bench.py`'s `--self-test` mode.
- **OUTCOME gate**: `RESULTS.md` must state a clear ship / iterate /
  discard verdict with an effect-size number (not just a p-value), and
  must address what the format-compliance rate implies even if scores
  tie.

## Model & cost
- **Model:** run with `claude-haiku-4-5` for cost/latency tractability
  inside the autonomous cron turn (must finish synchronously). The plan's
  original Opus-4.7 full run is a documented follow-on if Haiku shows a
  format effect worth confirming on the production model. RESULTS.md
  states the model explicitly and scopes the verdict to it — a format
  effect (or its absence) on Haiku is real data, not a universal claim.
- **API spend:** 20 tasks × 3 runs × 3 variants = 180 Haiku calls,
  fanned out over a 6-worker pool. Resumable via runs.jsonl.

## Council focus
- **PLAN**: are the three variants truly semantically equivalent, or did
  format conversion silently change content? Reviewer should diff them
  side-by-side, not just check that all three exist.
- **IMPLEMENTATION**: does bench.py correctly resume a partial run? Does
  it correctly handle a variant that returns malformed output (skip to
  scoring, don't crash)?
- **TESTS**: smoke test passes; runs.jsonl is well-formed; statistics
  agree with scipy on a fixture input.
- **OUTCOME**: RESULTS.md gives a verdict, not a hedge. If the result is
  "no significant difference," that's the verdict — say it.

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
1. **Real, in-use prompt** — results have direct loop relevance, not
   synthetic.
2. **Existing eval set:** `eval_bugs.json` already encodes planted bugs
   with expected catches; `eval_bugs.py` already runs the angle against
   it. Score function is already implemented.
3. **Sharp pass/fail signal** — did the reviewer flag the planted bug?
   No rubric judgment required, no LLM-as-judge needed.

### What "same semantic content" means
The three variants encode the same:
- Role description
- Definition of what counts as a bug
- Expected output schema (verdict + reason + cited file:line)
- Examples (if the current prompt has them)

What differs across the three:
- **Markdown variant** — current shape: headings + bullet lists + prose.
- **JSON variant** — top-level object with `role`, `task`,
  `bug_definition`, `output_schema`, `examples` keys; instructions are
  JSON strings, not prose; output requested as JSON.
- **XML variant** — `<role>`, `<task>`, `<bug_definition>`,
  `<output_schema>`, `<examples>` tags following Anthropic's documented
  convention; output requested in XML tags.

The validation step at council PLAN review must confirm the three are
actually semantically equivalent — content drift across formats is the
single most likely way this experiment produces a misleading result.

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
- `load_variant(name: str) -> str` — read prompt file from `prompts/`.
- `make_agent(variant: str) -> Callable[[str], str]` — closure binding
  the variant prompt to a Claude API call.
- `run_variant(variant: str, tasks: list, n: int = 3) -> list[dict]` —
  run each task N times, return raw records.
- `wilcoxon(scores_a: list[float], scores_b: list[float]) -> dict` —
  signed-rank test; statistic + p-value.
- `compliance_rate(records: list[dict], format: str) -> float` —
  fraction of outputs that parsed cleanly in the expected format.
- `write_results(per_variant: dict) -> None` — render `RESULTS.md`.
- `main()` — orchestrates load → run 3 variants → analyze → write.

Reuses `eval_harness.run_eval` for scoring (do not reimplement).

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
- **Statistical sanity**: verify the Wilcoxon implementation against
  `scipy.stats.wilcoxon` on a known input.
- **OUTCOME gate**: `RESULTS.md` must state a clear ship / iterate /
  discard verdict with an effect-size number (not just a p-value), and
  must address what the format-compliance rate implies even if scores
  tie.

## Estimated effort
- Build: ~2 hours.
- API spend: ~180 Opus 4.7 calls. Modest.
- Best fit: a single tock (matches the scope of `eval-opus-47-backbone`
  and similar measurement ticks).

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

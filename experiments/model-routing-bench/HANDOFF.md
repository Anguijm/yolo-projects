# Handoff — model-routing-bench

**Verdict (after 5 cycles):** iterate

**One-line:** Task classifier + per-class router + bench harness for routing experiments.

## What this is
- `model_router.py` — keyword + length classifier mapping a prompt to one of
  {`code`, `reasoning`, `long_context`, `simple`}, with per-class model rules.
- `route_benchmark.py` — runs a labeled task suite under `single` vs `routed`
  strategies, writes `route_results.json` with per-task scores and aggregates.

## Why an agent might want to adopt this
- You want to challenge the "one model for everything" default.
- You want a classifier you can extend with more rules / training data.
- You want a benchmark harness that's already wired to your eval set.

## Production-ready bits
- **Real bug fixed in cycle 3**: the keyword regex used `\b` boundaries
  which silently skip matches between `_` and letter chars. Replaced with
  explicit non-letter boundaries; classifier accuracy went from broken to
  11/11 on the labeled subset.
- Empty prompts now raise ValueError (no silent haiku-routing).
- Long-context detection by both length (>4000) AND keyword (summarize / extract / etc with len>500).

## What still needs work
- Routing rules table (`ROUTING_RULES`) is hand-coded. The whole point of the
  benchmark is to challenge those rules with empirical data; doing so
  requires real API keys.
- Score function in `route_benchmark.py` is a synthetic stub — rewards
  class-match. Real validation: swap in eval-harness rubric scoring.

## How to run
```
python3 route_benchmark.py
```
Writes `route_results.json` with single-vs-routed comparison.

## Files
- `model_router.py` — classifier + routes (~80 LOC)
- `route_benchmark.py` — bench (~120 LOC)
- `tasks.json` — 12 starter tasks across the four classes

## Verdict: iterate. Classifier production-quality; benchmark needs real keys.

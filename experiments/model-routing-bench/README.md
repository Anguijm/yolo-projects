# model-routing-bench

Source: Phase 4 experiment `nb-2026-04-28-gpt55-vs-claude-vs-gemini-real-difference`
(NateBJones, 2026-04-28).

## Hypothesis
Routing different task classes (reasoning, code, long-context retrieval) to
the model with the strongest empirical advantage for that class improves
overall pipeline quality vs using a single model everywhere.

## What this delivers
A small router + benchmark harness:

- `model_router.py` — keyword + heuristic classifier that maps a task
  prompt to a `task_class` ∈ `{reasoning, code, long_context, simple}`,
  plus a `route(task_class)` function that returns the configured model
  identifier.
- `route_benchmark.py` — runs every task in `tasks.json` against every
  available routing strategy (`single`, `routed`) and writes
  `route_results.json` with per-task latency and a per-strategy summary.
- `tasks.json` — 12 starter tasks across the four task classes.

Model adapters degrade to deterministic stubs when API keys are absent. The
benchmark therefore runs end-to-end without any credentials, and the
relative numbers are meaningful even with stubs (latency is artificial but
consistent per class).

## Usage

```
python3 route_benchmark.py
```

Writes `route_results.json` and prints a summary table.

## Routing rules (initial guess, to be tuned with real data)
- `reasoning` → claude-opus
- `code` → gpt-5-codex
- `long_context` → gemini-1.5-pro
- `simple` → claude-haiku

These are placeholders. The whole point of the benchmark is to challenge
them with empirical results.

## Files
- `model_router.py` — router (~70 LOC).
- `route_benchmark.py` — harness (~110 LOC).
- `tasks.json` — 12 starter tasks.
- `route_results.json` — generated.

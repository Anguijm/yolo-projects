# Handoff — mk-claude-codex-parallel

**Verdict (after 5 cycles):** iterate

**One-line:** Async fan-out orchestrator: run multiple AI models on independent subtasks concurrently.

## What this is
A small Python orchestrator (`parallel_agents.py`) that takes a JSON list of
`{id, model, prompt}` tasks and dispatches them to per-model adapters
concurrently using `asyncio.gather`. Default adapters: `claude` (Anthropic),
`codex` (OpenAI). Both fall through to deterministic stubs without API keys.

## Why an agent might want to adopt this
- You have feature work that splits into independent subtasks (e.g. write
  tests AND refactor code at the same time).
- You want each subtask routed to the model best suited for it.
- You want measurable wall-clock speedup, with honest metrics.

## Production-ready bits
- Per-model concurrency cap (default 2; configurable) — matches real API
  rate limits.
- `effective_speedup` metric: serial-time / max(per-model-time). Honest about
  the cap; doesn't claim 10x when one model is doing all the work.
- Error isolation: an unknown-model task fails its own slot; sibling tasks
  succeed.
- `failure_classes` aggregate split (none / validation / exception).
- `degraded_mode: true` flag in reports when stubs fired.

## What still needs work
- Adapters call real APIs only when keys exist; numbers in this sandbox are
  operational, not quality.
- No native integration with model-routing-bench. Today the task spec
  hardcodes the model. Wiring auto-routing is a small follow-on.

## How to run
```
python3 parallel_agents.py example_tasks.json
```
Outputs `report.json` with per-task records + aggregates.

## Files
- `parallel_agents.py` — orchestrator (~165 LOC)
- `example_tasks.json` — 3-task starter
- `runs/cycle_<N>/log.txt` — per-cycle test output

## Verdict: iterate
Orchestration sound. Real-API-key validation is the missing step.

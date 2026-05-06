# mk-claude-codex-parallel

Source: Phase 4 experiment `mk-2026-04-26-run-claude-codex-together` (Mark Kashef, 2026-04-26).

## Hypothesis
Running Claude and OpenAI Codex concurrently on different subtasks of the same
codebase reduces wall-clock time per feature cycle and lets each model work in
its strongest domain.

## What this delivers
A minimal task fan-out orchestrator that:

1. Reads a list of independent subtasks from a JSON file.
2. Dispatches each task to a model adapter (`claude` / `codex`) selected per
   task.
3. Runs adapters concurrently with `asyncio.gather`.
4. Collects per-task results, wall time, and any errors into a single JSON
   report.

The Codex adapter is a stub by default (prints what it would call). Set
`OPENAI_API_KEY` and the adapter switches to a real `responses.create` call.
The Claude adapter uses the `anthropic` SDK if `ANTHROPIC_API_KEY` is set,
otherwise stubs.

This is research-spike scaffolding, not a production pipeline.

## Usage

```
python3 parallel_agents.py example_tasks.json
```

Output: `report.json` with the per-task records and aggregate timing.

## Files
- `parallel_agents.py` — orchestrator (~130 LOC).
- `example_tasks.json` — three example subtasks across two models.
- `report.json` — generated after a run.

## Why a stubbed adapter is OK for the spike
The point of this experiment is the *orchestration shape*, not the model
quality. Once the dispatcher works end-to-end with stubs, swapping in real
SDK calls is a one-function change in each adapter.

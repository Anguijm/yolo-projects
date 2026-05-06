# openai-bg-runner

Source: Phase 4 experiment `nb-2026-04-27-openai-free-employee-catch`
(NateBJones, 2026-04-27).

## Hypothesis
Wiring an OpenAI Responses API agent into the YOLO loop as a background task
executor lets us offload low-stakes async work (ticket triage, test gen, doc
updates) without blocking the foreground dev loop.

## What this delivers
A persistent task queue + worker (`bg_task_runner.py`) that:

1. Stores tasks in `bg_tasks.jsonl` (append-only, one record per state change).
2. Polls the queue for pending tasks and dispatches them to a Responses API
   adapter.
3. Records the response, status, and any conversation thread id (so
   subsequent tasks can re-enter the same persistent agent context).
4. Survives crashes — state is reconstructed by replaying the jsonl on start.

The Responses API call is stubbed unless `OPENAI_API_KEY` is set, so the
worker is runnable end-to-end without credentials.

## Usage

```
# enqueue a task
python3 bg_task_runner.py enqueue "Triage open issues in the eval-bugs project"

# run the worker once (drain the queue and exit)
python3 bg_task_runner.py drain

# inspect the queue
python3 bg_task_runner.py status
```

## Files
- `bg_task_runner.py` — CLI + queue + worker (~150 LOC).
- `bg_tasks.jsonl` — persistent state (created on first enqueue).

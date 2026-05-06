# Handoff — openai-bg-runner

**Verdict (after 5 cycles):** iterate

**One-line:** Persistent task queue + worker backed by an OpenAI Responses API agent.

## What this is
A jsonl-backed task queue with three subcommands: `enqueue`, `drain`, `status`,
plus `reset` for stuck tasks. State lives in `bg_tasks.jsonl` as an
append-only event log; the current view is reconstructed by replaying.

## Why an agent might want to adopt this
- You want low-stakes async work to grind in the background while you
  focus on something else (ticket triage, doc updates, dependency bumps).
- You want thread continuity across sessions — pass an explicit `thread_id`
  on enqueue and the same Responses API thread is resumed on drain.

## Production-ready bits
- Append-only event log → crash recovery is trivially correct.
- Stuck-task detection: any `in_progress` older than 60s gets auto-recovered
  to `pending` on the next drain, with a logged note.
- `reset <task_id>` for manual recovery if auto-recovery isn't appropriate.
- Status display flags stuck tasks with `STUCK(<seconds>)` annotation.

## What still needs work
- `_call_responses_api` falls through to a stub when `OPENAI_API_KEY` is unset.
  Real validation requires the key.
- No max-recovery-attempts counter yet (a poison-pill task could keep
  recovering forever).

## How to run
```
python3 bg_task_runner.py enqueue "Triage open issues"
python3 bg_task_runner.py drain
python3 bg_task_runner.py status
python3 bg_task_runner.py reset <task_id>
```

## Files
- `bg_task_runner.py` — queue + worker (~190 LOC after cycle 2)
- `bg_tasks.jsonl` — auto-created on first enqueue

## Verdict: iterate
Operational behavior validated; needs real OpenAI key for thread-continuity proof.

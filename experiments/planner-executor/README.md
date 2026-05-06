# planner-executor

Source: Phase 4 experiment `mk-2026-04-28-claude-codex-plan-together` (Mark
Kashef, 2026-04-28).

## Hypothesis
Separating planning and code execution into two distinct agents — Claude as
the planner (task decomposition + spec), Codex as the executor (code
generation) — produces higher-quality code with fewer revision cycles than
a single-model approach, because each model operates within its strongest
domain.

## What this delivers
A two-stage pipeline (`planner_executor.py`) that:

1. Sends the user request to Claude with a *plan-only* system prompt.
   Claude returns a structured JSON plan: `{goal, steps: [{id, description,
   files, success_criterion}]}`.
2. Validates the plan shape (rejects free-form prose, requires every step
   to name files and a success criterion).
3. Iterates over the steps, sending each one to Codex with the full plan as
   context. Codex returns the diff or full file contents for that step.
4. Collects the per-step outputs into a `pipeline_report.json`.

Both adapters degrade to deterministic stubs when the corresponding API key
is missing.

## Why the validation step matters
The planner-executor pattern is fragile if the planner produces vague
plans. The validation step is the contract: a plan that doesn't enumerate
files and success criteria gets rejected and the planner is re-asked with
a stricter system prompt before any code is generated. This is the
single-most-important difference between this pipeline and asking one
model to "plan and code".

## Usage

```
python3 planner_executor.py "Add a /healthcheck endpoint to api/server.py that returns 200 OK"
```

Outputs:
- `last_plan.json` — the plan Claude produced.
- `pipeline_report.json` — per-step results from Codex.

## Files
- `planner_executor.py` — pipeline (~160 LOC).
- `system_prompts.py` — the planner and executor system prompts.

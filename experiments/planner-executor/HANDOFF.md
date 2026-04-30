# Handoff — planner-executor

**Verdict (after 5 cycles):** iterate

**One-line:** Two-stage Claude-as-planner + Codex-as-executor pipeline with strict plan validation.

## What this is
- Stage 1: Claude reads a change request, returns a JSON plan with
  `goal` + `steps[]`. Each step must list `files` and a verifiable
  `success_criterion`. A validator rejects malformed shapes; the planner
  retries with the bad output included for diagnosis.
- Stage 2: Each step is sent to Codex with the full plan as context, plus
  any prior step's diff (accumulation). Codex returns the diff for that
  step.

## Why an agent might want to adopt this
- You have a multi-file change that benefits from explicit decomposition
  before any code is generated.
- You want every step to have a verifiable contract before it ships.
- You want a tighter audit trail: what was planned, what was executed,
  step-by-step.

## Production-ready bits
- 6 validator failure modes covered (not dict, missing goal, empty steps,
  step missing files, step empty files, step empty success_criterion).
- Retry prompt now includes the planner's prior raw output for self-
  correction (cycle 2 fix).
- Executor accumulates diffs and passes them into subsequent steps so
  step-2 sees what step-1 produced.
- `--max-retries` CLI flag for tightening / loosening the strictness.

## What still needs work
- success_criterion is a free-text string; programmatic verification
  ("does the diff actually add a /healthcheck handler?") is not
  implemented. Documented as a follow-on.
- Planner and executor both fall through to stubs without API keys, so the
  in-sandbox validation is structural only — the strictness contract
  works; the plan-quality test needs real models.

## How to run
```
python3 planner_executor.py "Add a /healthcheck endpoint to api/server.py"
python3 planner_executor.py "..." --max-retries 2
```

## Files
- `planner_executor.py` — pipeline (~190 LOC after cycle 2)
- `system_prompts.py` — planner + executor system prompts
- `last_plan.json`, `pipeline_report.json` — most recent run output

## Verdict: iterate. Orchestration sound; plan-quality test needs real models.

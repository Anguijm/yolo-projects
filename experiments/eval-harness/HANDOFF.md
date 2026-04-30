# Handoff — eval-harness

**Verdict (after 5 cycles):** adopt

**One-line:** Lightweight rubric-based scoring harness for any agent function.

## What this is
- `eval_harness.run_eval(agent_fn, tasks_path)` — runs each task in
  `tasks.json` against `agent_fn`, scores with the per-task rubric, returns
  a structured report.
- `rubric.py` — five pluggable scorers: keyword, regex, exact, length, llm.
- `feedback_inject.py` — turns a report into a markdown summary suitable for
  injecting into the next agent run's context.

## Why an agent might want to adopt this
- You want a regression test for any prompt or model change.
- You want a feedback signal for self-evolving-agent or similar loops.
- You want a pre-filter before running the full council pipeline.

## Production-ready bits
- All five rubric types validated with right/wrong inputs (cycle 1).
- Aggregate splits `score_failed` (rubric mismatch) from `agent_failed`
  (exception) — clean attribution for diagnostic.
- `degraded_mode` flag set when any LLM-judge rubric runs without a real
  Anthropic key (fallback to keyword match — clearly noted in report).
- Cross-validated in cycle 4: scored seed (0.2) and evolved (1.0) prompts
  from self-evolving-agent on the same task suite.

## What still needs work
- LLM-judge rubric falls back to keyword match without `ANTHROPIC_API_KEY`.
  Useful for tests; real validation needs the key.
- Length rubric is too lax as a *primary* rubric; should be composable
  (combine with another) rather than standalone.

## How to run
```python
from eval_harness import run_eval
def my_agent(prompt: str) -> str: ...
report = run_eval(my_agent, "tasks.json")
print(report["aggregate"])
```
CLI:
```
python3 eval_harness.py tasks.json
python3 feedback_inject.py eval_report.json
```

## Files
- `eval_harness.py` — runner (~125 LOC)
- `rubric.py` — scorers (~85 LOC)
- `tasks.json` — 8 starter tasks

## Verdict: adopt. Foundation piece for any prompt/model regression testing.

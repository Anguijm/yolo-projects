# eval-harness

Source: Phase 4 experiment `do-2026-04-28-self-evolving-agent-eval-harness`
(David Ondrej, 2026-04-28).

## Hypothesis
Attaching a structured scoring harness to each agent run and injecting the
score summary back into the next run's context makes the agent converge on
better strategies faster than an agent operating without performance
feedback.

## What this delivers
A lightweight, reusable scoring harness:

- `eval_harness.py` — runs a list of tasks against an agent function, scores
  each output via a rubric, writes `eval_report.json` with per-task scores
  and an aggregate.
- `rubric.py` — pluggable scoring functions: `keyword_match`,
  `regex_match`, `exact_match`, `llm_judge`. Each rubric returns a
  float in [0, 1].
- `tasks.json` — 8 starter tasks demonstrating each rubric type.
- `feedback_inject.py` — produces a short markdown summary of the latest
  eval run suitable for injecting into the next run's context.

## Why this is a prerequisite for self-evolving agents
The self-evolving agent (in `experiments/self-evolving-agent/`) needs
something to evolve *toward*. Without numeric feedback per task, the
reflector model has no signal. This harness produces that signal.

The harness is also useful standalone — it's the right shape for
benchmarking a model swap, validating a prompt change, or running a
regression test against the YOLO loop.

## Usage

```python
from eval_harness import run_eval

def my_agent(prompt: str) -> str:
    ...

report = run_eval(my_agent, tasks_path="tasks.json")
print(report["aggregate"])
```

CLI:
```
python3 eval_harness.py tasks.json
python3 feedback_inject.py eval_report.json
```

## Files
- `eval_harness.py` — runner (~110 LOC).
- `rubric.py` — scoring fns (~80 LOC).
- `tasks.json` — 8 starter tasks.
- `feedback_inject.py` — context summarizer (~50 LOC).

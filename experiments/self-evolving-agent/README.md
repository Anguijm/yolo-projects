# self-evolving-agent

Source: Phase 4 experiment `do-2026-04-28-self-evolving-ai-agent`
(David Ondrej, 2026-04-28).

## Hypothesis
Giving an agent the ability to inspect its own performance logs and rewrite
its system prompt or tool definitions between iterations improves task
success rate over successive runs without manual intervention.

## What this delivers
A minimal self-evolving agent loop (`self_evolve.py`) that:

1. Runs N iterations of the same task suite.
2. After each iteration, scores the agent's output (via the eval harness in
   `experiments/eval-harness/`, when available, or a built-in fallback rubric).
3. Asks a "reflector" model to read the failures and propose a *small,
   diff-style edit* to the system prompt.
4. Applies the edit, writes the new prompt to `prompts/prompt_v{N+1}.txt`,
   and runs the next iteration.

The reflector is intentionally constrained to small edits (one-line changes
or single-paragraph additions) to make the evolution legible and reversible.
The full prompt history is preserved so a regression can be traced to a
specific edit.

## Why constrained edits
Unconstrained self-modification ends in a degenerate local optimum (the
agent rewrites the prompt to game the rubric). Constraining the reflector
to a tiny edit per iteration plus a versioned history keeps a human in the
loop after-the-fact: every change can be inspected, reverted, or pinned.

## Usage

```
python3 self_evolve.py --iterations 3
```

Outputs:
- `prompts/prompt_v0.txt` ... `prompt_v{N}.txt` — full evolution history.
- `evolution_log.jsonl` — per-iteration scores + reflector edit.

## Files
- `self_evolve.py` — the loop (~140 LOC).
- `prompts/prompt_v0.txt` — seed prompt.
- `tasks.json` — small task suite reused from `eval-harness/`.

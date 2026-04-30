# Handoff — self-evolving-agent

**Verdict (after 5 cycles):** iterate

**One-line:** Self-modifying agent loop: reflector reads failures and edits the system prompt.

## What this is
An agent loop that runs N iterations on a task suite, scores each output,
asks a constrained "reflector" to propose a one-line edit to the system
prompt, and iterates. Every prompt version is saved (`prompt_v0.txt`,
`prompt_v1.txt`, ...). A regression detector reverts and stops if avg_score
drops between iterations.

## Why an agent might want to adopt this
- You want the loop to tune its own system prompts based on failure modes.
- You want a versioned, reversible record of how each prompt evolved.
- You want a hard floor: the loop won't make things worse without backing
  out the change.

## Production-ready bits
- 5 reflector heuristics (was 3 in cycle 1): verbose-output, json-format,
  numeric-answer, proper-noun, generic-fallback.
- Regression detector: if score drops >0.01 between iterations, revert and
  stop with a logged "regressed" flag.
- Per-iteration edit log: each iteration's added line is captured in
  `evolution_log.jsonl` for audit.
- Cross-validated by eval-harness in cycle 4: evolved prompt scores 1.0 vs
  seed's 0.2 when scored by an *external* harness on the same tasks. The
  evolution isn't gaming an internal metric.

## What still needs work
- Reflector is heuristic-based. Real reflection benefits from a model in
  the loop, with explicit constraints to prevent rubric gaming.
- The `--inject-bad-edit` flag for testing the regression detector wasn't
  built; current heuristics never regress so the revert path is untested
  in practice.

## How to run
```
python3 self_evolve.py --iterations 5
python3 self_evolve.py --iterations 5 --threshold 0.99
```

## Files
- `self_evolve.py` — loop + reflector (~165 LOC)
- `prompts/prompt_v*.txt` — versioned history
- `evolution_log.jsonl` — per-iteration scores + edits
- `tasks.json` — 5 starter tasks

## Verdict: iterate. Operational shape proven; reflector quality needs real model.

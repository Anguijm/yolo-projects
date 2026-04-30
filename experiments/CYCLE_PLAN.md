# Cycle Plan: 5 cycles × 10 experiments

Pause both ticks and tocks. Run all 10 Phase 4 experiment scaffolds five
times each, capturing lessons per cycle and applying them to the next.

## Schedule
- 5 cycles, 10 experiments each, ~50 runs total + a final report.
- No literal sleeps between runs — wall-clock pacing is approximate.
  The "5 min per experiment" target is a quality signal: spend real
  effort (perturbations, edge cases, measurements), don't rush past.

## Per-cycle, per-experiment recipe
1. Read `LESSONS.md` (if it exists) so prior cycles inform this one.
2. Run the baseline demo end-to-end.
3. Apply 1–2 perturbations relevant to the experiment's hypothesis:
   - Different inputs (large, malformed, empty).
   - Edge conditions (concurrent restart, mid-run kill, schema drift).
   - Changes to the lesson from the previous cycle, if any.
4. Capture a measurement specific to the experiment:
   - Latency, score, throughput, error count, format-compliance rate, etc.
5. Append one new entry to `LESSONS.md` with: cycle number, what was
   tried, what was learned, what to change next cycle.
6. Per-cycle artifacts go to `runs/cycle_<N>/`.

## What "run" means per experiment shape

| Experiment                   | Run shape |
|---|---|
| mk-claude-codex-parallel     | varied task counts + concurrency, observe speedup factor + error handling |
| openai-bg-runner             | enqueue / drain / restart-mid-run, validate persistence + thread continuity |
| cloud-sandbox-adapter        | local + dry-run with non-trivial command sequences, validate trace fidelity |
| agent-observability          | nested spans + concurrent + error spans, observe schema gaps |
| claude-code-hacks            | static-lint each command markdown for clarity / contract / failure paths |
| claude-headless              | DRY_RUN chain + simulated failure injection (bad JSON, mid-chain crash) |
| model-routing-bench          | varied tasks, perturb classifier rules, observe routing + score impact |
| self-evolving-agent          | varied seed prompts + iteration counts, observe convergence vs gaming |
| eval-harness                 | varied agents (good / bad / inconsistent), all 5 rubric types |
| planner-executor             | valid + invalid plans, validator rejection paths |

## Lesson-application rules
Between cycles:
- Read all 10 `LESSONS.md` files.
- Group lessons into: **(A) per-experiment fixes**, **(B) cross-cutting
  patterns**, **(C) defer for the final report**.
- Apply (A) directly: edit the scaffold or the run config so the next
  cycle exercises the change.
- For (B), edit shared infrastructure if any exists; otherwise just
  document in `CYCLE_LOG.md`.
- Note every applied change in `CYCLE_LOG.md` so the diff between
  cycle N and cycle N+1 is auditable.

## Output structure
- `experiments/CYCLE_PLAN.md` — this file.
- `experiments/CYCLE_LOG.md` — chronological per-cycle summary +
  cross-cutting lessons.
- `experiments/<name>/runs/cycle_<N>/log.txt` — per-cycle run output.
- `experiments/<name>/LESSONS.md` — accumulated lessons for that
  experiment (newest at bottom).

## Final reports (after cycle 5)
- `experiments/FINAL_REPORT.md` — plain-language report covering every
  experiment with one of four verdicts:
  - **adopt**: promote into production / tick queue.
  - **iterate**: needs another pass before adoption.
  - **discard**: failed; don't pursue.
  - **defer**: not enough information to verdict yet (typically because
    real API keys / production data are needed).
- `experiments/<name>/HANDOFF.md` — agent-shareable summary per
  experiment so a fresh session can read it and adopt the work.

## Constraints / caveats (recorded up front for the final report)
- No real model API keys in this sandbox → adapters stay stubbed →
  numbers are operational, not model-quality.
- No `claude` CLI → claude-headless is DRY_RUN + simulation, not real.
- The 5×10 schedule will produce diminishing returns by cycle 3–4 for
  experiments where the operational space is small (e.g. eval-harness
  rubric scoring is trivially correct after cycle 1).  When that
  happens I'll log "no new lesson — operational space exhausted" and
  move on, rather than fabricate findings.

## Progress tracking
TodoWrite list used for cycle-level progress (8 todos). Per-experiment
runs not in the top-level list — they live in the cycle logs.

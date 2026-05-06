# Final Report — 5 cycles × 10 experiments

This is the plain-language wrap-up of running all 10 Phase 4 backlog
experiments through five cycles of stress-test, perturbation, and
cross-experiment integration. Per-experiment handoff notes (for fresh
agents) live at `experiments/<name>/HANDOFF.md`. Full per-cycle history
lives in `experiments/<name>/LESSONS.md` and per-cycle run logs in
`experiments/<name>/runs/cycle_<N>/`.

## Verdicts at a glance

| # | Experiment | Verdict | One-line summary |
|---|---|---|---|
| 1 | mk-claude-codex-parallel | iterate | Async fan-out with per-model concurrency cap and honest speedup metrics. Real API keys needed to know if parallelism actually wins. |
| 2 | openai-bg-runner | iterate | Persistent task queue with stuck-task auto-recovery and reset. Real OpenAI key needed to validate Responses API thread continuity. |
| 3 | cloud-sandbox-adapter | adopt (Local+DryRun) / defer (remote) | DryRun-to-Local replay validates 0 discrepancies on a 5-op trace. Migration audit ready; remote adapter is the next step. |
| 4 | agent-observability | adopt | Nested-span tracer with cost field, in-memory summary, and tool filtering. Drops into any caller without code changes. |
| 5 | claude-code-hacks | adopt | Five live slash commands at `.claude/commands/` with consistent Usage: lines and numbered steps. Lint contract enforced. |
| 6 | claude-headless | defer | DRY_RUN + simulated failure paths all pass; needs real `claude` CLI for end-to-end validation. |
| 7 | model-routing-bench | iterate | Classifier accuracy 11/11 on labeled tasks after a real regex bug fix. Benchmark needs real API keys for quality numbers. |
| 8 | self-evolving-agent | iterate | Convergence demonstrated (0.2 → 1.0 from vague seed); validated by an external scorer. Reflector quality needs real model. |
| 9 | eval-harness | adopt | 5 pluggable rubric types with score_failed / agent_failed split and degraded-mode flag. Foundation piece for everything else. |
| 10 | planner-executor | iterate | Strict JSON plan validator + step-diff accumulation. Plan quality needs real model to verdict. |

**Verdict legend:**
- **adopt**: promote into production / tick queue. Code is sound, behavior validated under stress, no real-API-key dependency.
- **iterate**: orchestration is sound; quality verdict requires real API keys.
- **defer**: cannot be validated in this sandbox; revisit when the missing dependency (real CLI, real key, remote infra) is available.
- **discard**: would have been used if any experiment failed under stress. None did.

## What we actually shipped over 5 cycles

**Real bug fixes (not just instrumentation):**
- `mk-claude-codex-parallel`: speedup metric was misleading; added effective_speedup = serial / max(per_model_total).
- `openai-bg-runner`: drain originally skipped stuck `in_progress` tasks → infinite stuck. Added stale-detection + auto-recovery + manual reset.
- `cloud-sandbox-adapter`: DryRun.read silently returned `""` for missing files; LocalSandbox raised. Now both raise.
- `model-routing-bench`: keyword regex used `\b` boundaries which silently skip matches between underscore and letters. Real-world prompts (markdown, placeholder text) hit this. Replaced with explicit non-letter boundaries → classifier accuracy 11/11.
- `eval-harness`: aggregate didn't separate "wrong answer" from "agent crashed". Added score_failed and agent_failed.
- `planner-executor`: retry prompt didn't show the planner what it produced last time; executor didn't pass prior step diffs forward. Both fixed.

**Real features added:**
- `agent-observability`: cost_usd field with per-model rate table; in-memory tracer.summary(); --exclude tool filter on the aggregator.
- `cloud-sandbox-adapter`: replay_trace(trace, target) — the migration validation harness the README originally promised.
- `claude-headless`: retry on transient errors with exponential backoff; MAX_CONTEXT_BYTES truncation in chain.
- `self-evolving-agent`: 5 reflector heuristics (was 3); regression detector that reverts and stops if score drops; per-iteration edit log.
- `claude-code-hacks`: Usage: lines on all 5 commands.

**Cross-experiment integrations validated (cycle 4):**
- agent-observability instruments parallel_agents.py without source changes — 3 model spans nested under one batch span with correct parent_id propagation through asyncio.gather and correct cost calculation.
- eval-harness scores self-evolving-agent's seed vs evolved prompt independently. Result: seed 0.200 → evolved 1.000. Independent scorer confirms the reflector's edits are real wins, not internal-metric gaming.

## Cross-cutting patterns observed

**Pattern A — failure differentiation (applied):** Several scaffolds collapsed "wrong answer" with "the call crashed" into a single failure count, losing diagnostic information. Cycle 2 added `failure_classes` / `score_failed` / `agent_failed` fields to mk-claude-codex-parallel and eval-harness. Future experiments should adopt this convention.

**Pattern B — degraded-mode flag (applied):** When a scaffold's adapter falls back to a stub (no API key), the generated report can be misread as real numbers. Cycle 2 added a `degraded_mode: true` flag to mk-claude-codex-parallel, eval-harness, model-routing-bench, planner-executor reports. Reading any of those reports without checking the flag is a bug; the flag closes that gap.

**Pattern C — input validation gaps (partially applied):** Several scaffolds accepted edge-case inputs (empty prompts, empty step files arrays) without explicit rejection. model-routing-bench now raises on empty prompt; planner-executor's validator already covered its cases. Other scaffolds could benefit from a shared `validate_input` helper but the work isn't large enough to justify creating one yet.

## What I couldn't validate (honest caveats)

- **No model-quality numbers.** Every experiment that calls a real API (Claude / OpenAI / Gemini) falls back to a deterministic stub in this sandbox. Routing wins, parallelism speedups, and self-evolution improvements all carry the `degraded_mode: true` flag. Real validation requires keys.
- **claude-headless wasn't end-to-end tested.** No `claude` CLI in this sandbox. All testing was via simulated stub binaries. The retry, truncation, and chain-failure paths are exercised but real CLI semantics (long-running tools, multi-turn behavior, file-edit interactions) are not.
- **Cloud sandbox remote adapters not built.** LocalSandbox and DryRunSandbox are validated; E2B / Modal / Daytona adapters are an integration ticket with their respective SDKs.
- **Diminishing returns by cycle 3.** The honest plateau hit cycles 3-4 for most experiments. Cycle 5 was a final smoke pass / verdict lock-in. Doing 10 more cycles wouldn't change the verdicts; it would just generate more LESSONS.md text.

## What to do next (recommended priority order)

1. **Adopt eval-harness and agent-observability immediately.** Both are infrastructure that compounds — every other experiment runs cheaper and more legibly once they're wired into the loop.
2. **Adopt claude-code-hacks (already live).** Use the slash commands in real sessions; observe which get used; prune what doesn't.
3. **Adopt cloud-sandbox-adapter Local + DryRun.** Use DryRun in pre-flight checks for any tick that does shell-out work. Defer remote adapter to a separate ticket.
4. **Run iterate experiments under real API keys.** mk-claude-codex-parallel, model-routing-bench, planner-executor, self-evolving-agent — each of these has a real-API question that's the actual deciding factor. The bench-prompt-format tick (already approved in the queue) should run before/alongside these to settle the format question first.
5. **Defer claude-headless** until a session is run inside a real Claude Code environment.

## File index for fresh agents

```
experiments/
├── CYCLE_PLAN.md              ← the plan I executed against
├── CYCLE_LOG.md               ← chronological cross-cutting findings
├── FINAL_REPORT.md            ← this file
└── <experiment-name>/
    ├── README.md              ← what the experiment is and how to run it
    ├── LESSONS.md             ← per-cycle lessons (newest at bottom)
    ├── HANDOFF.md             ← agent-shareable summary (start here)
    └── runs/
        └── cycle_<1..5>/
            └── log.txt        ← raw run output for that cycle
```

A fresh agent investigating any experiment should start with HANDOFF.md (one page),
fall back to README.md for usage, and dig into LESSONS.md only for design history.

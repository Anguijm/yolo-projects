# Cycle Log

Chronological record of cycle-level outcomes and cross-cutting lessons.
Per-experiment lessons live in each `experiments/<name>/LESSONS.md`.

## Cycle 1 — baseline (2026-04-30)
All 10 experiments ran end-to-end. None of the scaffolds is broken.

### Per-experiment fixes queued for cycle 2
- **mk-claude-codex-parallel**: speedup metric overstates win; add per-model concurrency cap.
- **openai-bg-runner**: drain skips stuck `in_progress` tasks → infinite stuck. Add stale-detection.
- **cloud-sandbox-adapter**: DryRun.read silently returns "" for missing files; LocalSandbox raises. Diverging behavior.
- **agent-observability**: no cost_usd field; no sink rotation; no tool filter on aggregator.
- **claude-code-hacks**: `/status-deep` lacks numbered steps; lint should verify file paths exist.
- **claude-headless**: no retry on transient errors; chain has no max-context-bytes; no per-step timeout.
- **model-routing-bench**: long-context classifier broken; empty prompt classifies as `simple`; no per-task expected_class.
- **self-evolving-agent**: reflector too narrow (3 heuristics); no regression detector; no diff view.
- **eval-harness**: aggregate doesn't separate score-fail vs agent-crash; length rubric too lax as standalone.
- **planner-executor**: retry prompt doesn't include the bad output; executor doesn't pass prior step diffs forward.

### Cross-cutting patterns (apply to multiple)
- **Pattern A — error/failure differentiation**: many scaffolds collapse "failed because output was wrong" with "failed because the call crashed". Both lead to score=0 or success=False with no separate counter. Worth a shared convention: every result record gets a `failure_class` field ∈ {none, validation, exception, timeout, format}.
- **Pattern B — silent degradation**: stub adapters silently substitute for real ones when keys are absent; rubric stubs do the same. Risk: someone reads the report and thinks the numbers are real. Add a `degraded_mode: true` field to every report when any stub fired.
- **Pattern C — input validation gaps**: the routing classifier accepts empty strings, the executor accepts plans with empty arrays of dependencies, etc. Each scaffold makes its own decision. A shared `validate_input` helper would prevent the empty-input class of bug.

## Cycle 2 — apply C1 lessons
All 10 cycle-1 fixes landed. Highlights:
- **mk-claude-codex-parallel**: per-model concurrency cap added; effective_speedup metric replaces optimistic speedup_factor; degraded_mode flag added.
- **openai-bg-runner**: stuck-task auto-recovery + manual reset + status STUCK flag.
- **cloud-sandbox-adapter**: DryRun.read raises; write captures content (4KB cap) into trace.
- **agent-observability**: cost_usd column with per-model rate table; --exclude tool filter.
- **claude-code-hacks**: /status-deep gained numbered steps.
- **claude-headless**: retry-with-exp-backoff on transient errors; MAX_CONTEXT_BYTES truncation.
- **model-routing-bench**: long-context detection by keyword+length; empty prompt raises.
- **self-evolving-agent**: 5 heuristics; regression detector; per-iteration edit log. **Vague seed converges 0.2 → 0.8 → 1.0 in 2 edits.**
- **eval-harness**: score_failed / agent_failed split; degraded_mode flag.
- **planner-executor**: retry prompt includes prior raw output; executor accumulates diffs.

Cross-cutting Pattern A and Pattern B applied to relevant experiments. Pattern C deferred.

## Cycle 3 — stress + diagnosis
Stress-test runs (50-task batch, 3-step planner accumulation) and root-cause diagnoses.

### Real bug found
**model-routing-bench**: long-1 was falling through to the default reasoning fallback despite containing the keyword "Summarize". Diagnosis: the keyword regex used `\b` boundaries; underscore is a word character in regex, so `..._UVWXYZ___Summarize` has no word-boundary between `_` and `S`. The keyword silently never matched in any prompt with underscored placeholders.

### Operational space exhaustion called out
- claude-headless: no further validation possible without the real CLI.
- openai-bg-runner, cloud-sandbox-adapter, agent-observability, eval-harness, planner-executor: smoke-only, no new lessons at the orchestration layer.

## Cycle 4 — fix + cross-experiment integration
- **model-routing-bench**: replaced `\b` with explicit non-letter boundaries. **Classifier accuracy 11/11.**
- **claude-code-hacks**: normalized /test-gen's Usage: line to match the lint contract.
- **cross-integration A**: agent-observability instruments parallel_agents.py without source changes. 3 model-call spans correctly nest under a `batch` parent via ContextVar; cost computed per call.
- **cross-integration B**: eval-harness scores self-evolving-agent's seed (0.200) vs evolved (1.000) prompts on the same task suite. **Independent scorer confirms the reflector's edits are real wins, not internal-metric gaming.**

## Cycle 5 — final smoke + verdict lock-in
All 10 experiments pass smoke runs:
- mk-claude-codex-parallel: speedup=3.00x effective=1.50x (3-task baseline)
- openai-bg-runner: drain succeeds with thread continuity
- cloud-sandbox-adapter: replay returns 0 discrepancies
- agent-observability: 11 spans / $0.3240 cost
- claude-code-hacks: 5/5 commands have Usage:
- claude-headless: DRY_RUN ok (no real CLI)
- model-routing-bench: 11/11 classifier accuracy
- self-evolving-agent: convergence to 1.000
- eval-harness: 7/8 pass / score_failed=1 / agent_failed=0 / degraded=True
- planner-executor: 3 steps planned + executed

Verdicts locked in `experiments/FINAL_REPORT.md` and per-experiment `HANDOFF.md`.

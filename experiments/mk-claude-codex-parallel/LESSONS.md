# Lessons — mk-claude-codex-parallel

## Cycle 1 (baseline + perturbations)
**Tried:** 1-task, 3-task, 10-task batches; unknown-model adapter; mixed
success/failure batches.

**Learned:**
- Speedup factor as currently computed is misleading at scale. With stubs
  that all take exactly 0.2s, 10 tasks shows 9.99x speedup — but in
  reality the speedup is bounded by `min(N_tasks, N_models)` since two
  models can only run two streams. The metric overstates the win.
- Error isolation works: an unknown adapter fails its own task without
  taking down the batch.
- The orchestrator has no concept of *which model* should get a task —
  the task spec hardcodes it. That's fine for a fan-out spike but won't
  scale; integration with `model-routing-bench` is the obvious follow-on.

**Change for cycle 2:**
- Add a `model_concurrency` cap (default 2 per model: a real API has rate
  limits, a fan-out of 10 against one model isn't 10x faster).
- Improve the speedup metric to report `effective_speedup = serial / max(per_model_total)`
  rather than `serial / parallel`, which assumes infinite concurrency.

## Cycle 2 (per-model concurrency cap + new metrics)
**Tried:** Re-ran baseline; 10 same-model tasks under cap=2.
**Learned:** Effective speedup metric now correctly caps: 10 claude tasks under cap=2 give parallel=1.0s (5 batches), serial=2.0s, speedup_factor=2.0x, effective_speedup=1.0x (single model bottleneck). The honest number now matches reality. degraded_mode flag set correctly when stubs fire.
**Change for cycle 3:** Add a "model_pool" abstraction so cap defaults can be per-model (some APIs allow more concurrency than others). Today the cap is a single global. Also: report what the *theoretical* upper bound is (sum-of-per-model-totals / max-per-model-total) so we can see how close we got.

## Cycle 3 (50-task stress)
**Tried:** 50 tasks (25 claude / 25 codex), measured against the cap=2.
**Learned:** parallel=2.61s, serial=10.03s → speedup_factor=3.84x. effective_speedup=2.00x — exactly matches the cap. The honest metric is now stable at the theoretical ceiling. degraded_mode flag still works at 50-task scale.
**Change for cycle 4:** Operational space largely exhausted at this layer. Real value comes from integrating with model-routing-bench (auto-classify the task → pick the model) which is a follow-on tick, not in scope here.

## Cycle 4 (instrumented by agent-observability)
**Tried:** Wrap claude_adapter and codex_adapter with tracer.span calls.
**Learned:** Composition works cleanly: 3 task-level spans + 1 batch parent span recorded with correct parent_ids and cost. Validates that the orchestrator integrates with observability without code changes to either side.

## Cycle 5 (final smoke)
**Result:** speedup=3.00x effective=1.50x degraded=True. Stable. Verdict: **iterate** — needs real API keys to validate quality wins; orchestration sound.

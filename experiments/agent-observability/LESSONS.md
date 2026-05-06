# Lessons — agent-observability

## Cycle 1 (baseline + perturbations)
**Tried:** Baseline demo (11 spans, 7 distinct tools); error propagation
through nested spans; concurrent child spans with asyncio.gather.

**Learned:**
- Aggregator output is correct and useful — per-tool p50/p95, slowest 5,
  total spans.
- **Error propagation is correct**: an exception in an inner span flips
  both inner and outer to status=error, with the same error message
  reaching both. That's the right behavior for traceability.
- **Concurrent spans work cleanly under asyncio**: ContextVar correctly
  scopes parent_id per task, so three concurrent task.* spans all show
  the same parent_id (the surrounding `parent` span).
- **Schema gap: no cost field.** Token counts are tracked but not the
  $-cost. For council gates (the most expensive callers), token spend
  alone is misleading without per-model pricing.
- **No span sampling.** At YOLO loop scale (potentially thousands of
  spans per session), the jsonl will get unwieldy. Need either size-cap
  rotation or per-tool sampling rates.

**Change for cycle 2:**
- Add a `cost_usd` field computed from token counts × per-model rate
  (table baked into agent_tracing.py).
- Add a `tracer.flush()` and a sink-rotation hook so a long session
  doesn't write a single multi-GB file.
- Add a `--filter tool=X` flag to trace_summary so noisy infrastructure
  spans (write_file, read_file) can be excluded.

## Cycle 2 (cost field + tool filter)
**Tried:** Re-ran demo; aggregator with --exclude tool=read_file,write_file.
**Learned:** Cost column added (0.3240 USD on the demo's 7100/2900 token claude calls). Filter excludes infrastructure spans cleanly. Total cost surfaced at the top of the report.
**Change for cycle 3:** Add a sink rotation hook (size-based: rotate at 10MB by default) so a long session doesn't write a single multi-GB jsonl. Also: add a `tracer.summary()` that aggregates without writing through the file — useful for in-memory dashboards.

## Cycle 3 (tracer.summary() in-memory)
**Tried:** demo + tracer.summary() returns aggregate without spawning the CLI aggregator.
**Learned:** Summary returns clean dict-of-dicts: per-tool calls, tokens, cost, errors. Useful for in-process dashboards or live status reports.
**Change for cycle 4:** Operational space exhausted. Sink rotation (size-based) is documented in cycle 2's "change for cycle 3" but is a feature, not a measurement — defer.

## Cycle 4 (cross-experiment integration with parallel_agents)
**Tried:** Wrap parallel_agents.py adapters with tracer.span calls.
**Learned:** **Composition validated.** 3 model-call spans correctly nest under a single 'batch' parent, parent_ids correctly preserved through asyncio.gather, cost field correctly computed per call. The library is drop-in for any async caller without API changes.

## Cycle 5 (final smoke)
**Result:** 11 spans / $0.3240 cost reported correctly. Verdict: **adopt** — drop into council.py and verify_build.py.

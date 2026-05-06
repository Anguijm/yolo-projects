# agent-observability

Source: Phase 4 experiment `mlops-2026-04-27-agent-observability-cloud`
(MLOps, 2026-04-27).

## Hypothesis
Instrumenting each tool call and reasoning step with structured trace logs
(span id, parent id, tool name, token counts, input/output hash, latency)
makes failure modes diagnosable and expensive steps optimizable. Cloud-native
agent deployments lose the interactive print-debug loop, so structured traces
are required, not nice-to-have.

## What this delivers
A small tracing library (`agent_tracing.py`) that:

- Emits one JSON record per span to a file or stderr (default:
  `traces.jsonl` in the working directory).
- Supports nested spans via a context-manager `span(name)`.
- Captures: span_id, parent_id, name, tool, ts_start, ts_end, latency_ms,
  token_in, token_out, input_hash, output_hash, status.
- Hash-elides large inputs/outputs so traces stay grep-friendly.

Plus an aggregator (`trace_summary.py`) that reads a jsonl trace file and
prints:
- Per-tool latency p50/p95.
- Per-tool token totals.
- Top 5 slowest spans.
- Failure rate per tool.

## Usage

```python
from agent_tracing import tracer

with tracer.span("plan_gate") as s:
    s.tool = "claude.messages.create"
    s.token_in = 1234
    # ... do work ...
    s.token_out = 567
```

Then aggregate:

```
python3 trace_summary.py traces.jsonl
```

## Files
- `agent_tracing.py` — span recorder (~110 LOC).
- `trace_summary.py` — aggregator (~80 LOC).
- `demo.py` — runs a tiny synthetic agent through three nested spans so
  `traces.jsonl` is non-empty for the summary script.

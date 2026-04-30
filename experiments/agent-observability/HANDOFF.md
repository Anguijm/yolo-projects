# Handoff — agent-observability

**Verdict (after 5 cycles):** adopt

**One-line:** Nested-span tracer for agent steps with cost, tokens, latency, errors.

## What this is
A small tracing library: open a `tracer.span("name")` context manager around
any operation; nested spans automatically pick up parent_id via ContextVar
(works correctly under asyncio). Every span emits a JSON record with
span_id, parent_id, tool, latency_ms, token_in/out, cost_usd, status, error.

Plus an aggregator `trace_summary.py` that gives per-tool p50/p95
latencies, per-tool token totals, top-5 slowest spans, and total cost.

## Why an agent might want to adopt this
- You want to know where your agent is spending time and money.
- You want to find expensive or flaky tools without print-debugging.
- You want a baseline for any optimization work — claims like "this saved
  20% latency" need this data layer to be falsifiable.

## Production-ready bits
- ContextVar-based parent tracking → correctly nests under asyncio.gather.
- Cost field auto-computed from per-model rate table.
- `tracer.summary()` for in-process aggregation without spawning the CLI.
- `--exclude tool=X,Y` filter on the aggregator for hiding noisy
  infrastructure spans.
- Cross-experiment integration verified: instruments parallel_agents.py
  with no source changes (cycle 4 test).

## What still needs work
- No size-based sink rotation. A long session writes to a single jsonl,
  which can grow unbounded. Documented as a follow-on.

## How to run
```python
from agent_tracing import tracer
with tracer.span("plan_gate") as s:
    s.tool = "claude.messages.create"
    s.token_in, s.token_out = 1234, 567
    # ... do work ...
```
Then aggregate:
```
python3 trace_summary.py traces.jsonl
python3 trace_summary.py traces.jsonl --exclude tool=read_file,write_file
```

## Files
- `agent_tracing.py` — tracer + cost table (~145 LOC)
- `trace_summary.py` — aggregator (~95 LOC)
- `demo.py` — synthetic trace generator

## Verdict: adopt. Wire into council.py and verify_build.py.

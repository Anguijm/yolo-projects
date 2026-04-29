"""Demo: nested spans across a fake agent run so traces.jsonl is non-empty."""
from __future__ import annotations

import time
from pathlib import Path

from agent_tracing import Tracer

trace_path = Path(__file__).parent / "traces.jsonl"
trace_path.unlink(missing_ok=True)
tracer = Tracer(sink=trace_path)


def fake_tool_call(name: str, in_tokens: int, out_tokens: int, duration: float) -> None:
    with tracer.span(f"tool.{name}") as s:
        s.tool = name
        s.token_in = in_tokens
        s.token_out = out_tokens
        s.input_hash = tracer.hash({"name": name, "in": in_tokens})
        time.sleep(duration)
        s.output_hash = tracer.hash({"out": out_tokens})


with tracer.span("plan_gate") as outer:
    outer.tool = "council.plan"
    fake_tool_call("claude.messages.create", 1500, 600, 0.05)
    fake_tool_call("read_file", 0, 0, 0.005)
    fake_tool_call("claude.messages.create", 800, 300, 0.02)

with tracer.span("implementation_gate") as outer:
    outer.tool = "council.implementation"
    fake_tool_call("claude.messages.create", 4200, 1800, 0.12)
    fake_tool_call("write_file", 0, 0, 0.003)
    fake_tool_call("run_shell", 0, 0, 0.04)

with tracer.span("tests_gate") as outer:
    outer.tool = "council.tests"
    fake_tool_call("run_shell", 0, 0, 0.08)
    fake_tool_call("claude.messages.create", 600, 200, 0.025)

print(f"wrote {trace_path}")

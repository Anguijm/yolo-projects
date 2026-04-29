"""Parallel Claude + Codex task fan-out orchestrator.

Reads a JSON list of {model, task} pairs and runs each dispatch concurrently.
Writes a structured report with per-task wall time, success flag, and result.

Adapters degrade to a stub when the corresponding API key is absent, so the
script is runnable end-to-end without any credentials.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Awaitable


@dataclass
class TaskResult:
    task_id: str
    model: str
    prompt: str
    success: bool
    wall_seconds: float
    output: str
    error: str | None = None


async def claude_adapter(prompt: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        await asyncio.sleep(0.2)
        return f"[claude-stub] would call messages.create with prompt of {len(prompt)} chars"
    try:
        from anthropic import AsyncAnthropic
    except ImportError:
        return "[claude-stub] anthropic SDK not installed"
    client = AsyncAnthropic(api_key=key)
    msg = await client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


async def codex_adapter(prompt: str) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        await asyncio.sleep(0.2)
        return f"[codex-stub] would call responses.create with prompt of {len(prompt)} chars"
    try:
        from openai import AsyncOpenAI
    except ImportError:
        return "[codex-stub] openai SDK not installed"
    client = AsyncOpenAI(api_key=key)
    resp = await client.responses.create(
        model="gpt-5-codex",
        input=prompt,
    )
    return resp.output_text


ADAPTERS: dict[str, Callable[[str], Awaitable[str]]] = {
    "claude": claude_adapter,
    "codex": codex_adapter,
}


async def run_one(task: dict) -> TaskResult:
    model = task["model"]
    adapter = ADAPTERS.get(model)
    if adapter is None:
        return TaskResult(
            task_id=task["id"],
            model=model,
            prompt=task["prompt"],
            success=False,
            wall_seconds=0.0,
            output="",
            error=f"unknown model adapter: {model}",
        )
    start = time.monotonic()
    try:
        output = await adapter(task["prompt"])
        return TaskResult(
            task_id=task["id"],
            model=model,
            prompt=task["prompt"],
            success=True,
            wall_seconds=time.monotonic() - start,
            output=output,
        )
    except Exception as exc:
        return TaskResult(
            task_id=task["id"],
            model=model,
            prompt=task["prompt"],
            success=False,
            wall_seconds=time.monotonic() - start,
            output="",
            error=f"{type(exc).__name__}: {exc}",
        )


async def run_all(tasks: list[dict]) -> dict[str, Any]:
    started = time.monotonic()
    results = await asyncio.gather(*(run_one(t) for t in tasks))
    elapsed = time.monotonic() - started
    serial_total = sum(r.wall_seconds for r in results)
    return {
        "elapsed_parallel_seconds": elapsed,
        "elapsed_serial_seconds": serial_total,
        "speedup_factor": (serial_total / elapsed) if elapsed > 0 else 0.0,
        "task_count": len(results),
        "success_count": sum(1 for r in results if r.success),
        "tasks": [asdict(r) for r in results],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: parallel_agents.py <tasks.json>", file=sys.stderr)
        return 2
    tasks_path = Path(argv[1])
    tasks = json.loads(tasks_path.read_text())
    report = asyncio.run(run_all(tasks))
    out_path = tasks_path.parent / "report.json"
    out_path.write_text(json.dumps(report, indent=2))
    print(f"wrote {out_path}")
    print(
        f"  parallel={report['elapsed_parallel_seconds']:.2f}s  "
        f"serial={report['elapsed_serial_seconds']:.2f}s  "
        f"speedup={report['speedup_factor']:.2f}x  "
        f"{report['success_count']}/{report['task_count']} ok"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

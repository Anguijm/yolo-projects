"""Persistent background task runner backed by an OpenAI Responses API agent.

State lives in `bg_tasks.jsonl` next to this script: append-only event log of
{task_id, state, ts, payload}. The current view of any task is reconstructed
by replaying the log.

States: pending -> in_progress -> done | failed
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

LOG_PATH = Path(__file__).parent / "bg_tasks.jsonl"


def _append(record: dict[str, Any]) -> None:
    record = {"ts": time.time(), **record}
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")


def _read_all() -> list[dict[str, Any]]:
    if not LOG_PATH.exists():
        return []
    with LOG_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def _current_view() -> dict[str, dict[str, Any]]:
    view: dict[str, dict[str, Any]] = {}
    for rec in _read_all():
        tid = rec["task_id"]
        view.setdefault(tid, {"task_id": tid, "history": []})
        view[tid]["history"].append(rec)
        view[tid]["state"] = rec["state"]
        if "prompt" in rec:
            view[tid]["prompt"] = rec["prompt"]
        if "response" in rec:
            view[tid]["response"] = rec["response"]
        if "thread_id" in rec:
            view[tid]["thread_id"] = rec["thread_id"]
    return view


def _call_responses_api(prompt: str, prior_thread: str | None) -> tuple[str, str]:
    """Returns (response_text, thread_id)."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        time.sleep(0.1)
        return (
            f"[responses-stub] would resume thread={prior_thread} with prompt of {len(prompt)} chars",
            prior_thread or f"thread_stub_{uuid.uuid4().hex[:8]}",
        )
    try:
        from openai import OpenAI
    except ImportError:
        return ("[responses-stub] openai SDK not installed", prior_thread or "thread_noop")
    client = OpenAI(api_key=key)
    kwargs: dict[str, Any] = {"model": "gpt-5", "input": prompt, "store": True}
    if prior_thread:
        kwargs["previous_response_id"] = prior_thread
    resp = client.responses.create(**kwargs)
    return (resp.output_text, resp.id)


def cmd_enqueue(args: list[str]) -> int:
    if not args:
        print("usage: enqueue <prompt> [thread_id]", file=sys.stderr)
        return 2
    prompt = args[0]
    thread = args[1] if len(args) > 1 else None
    tid = f"task_{uuid.uuid4().hex[:8]}"
    _append({"task_id": tid, "state": "pending", "prompt": prompt, "thread_id": thread})
    print(tid)
    return 0


STALE_THRESHOLD_S = 60


def cmd_drain(_: list[str]) -> int:
    view = _current_view()
    now = time.time()
    pending = [t for t in view.values() if t["state"] == "pending"]
    stuck = [
        t for t in view.values()
        if t["state"] == "in_progress"
        and (now - max(h["ts"] for h in t["history"])) > STALE_THRESHOLD_S
    ]
    if stuck:
        print(f"recovering {len(stuck)} stuck task(s)")
        for t in stuck:
            _append({"task_id": t["task_id"], "state": "pending", "note": "auto-recovered from stuck in_progress"})
            pending.append({**t, "state": "pending"})
    if not pending:
        print("no pending tasks")
        return 0
    for task in pending:
        tid = task["task_id"]
        _append({"task_id": tid, "state": "in_progress"})
        try:
            text, thread = _call_responses_api(task["prompt"], task.get("thread_id"))
            _append({"task_id": tid, "state": "done", "response": text, "thread_id": thread})
            print(f"  {tid}: done ({len(text)} chars, thread={thread})")
        except Exception as exc:
            _append({"task_id": tid, "state": "failed", "response": f"{type(exc).__name__}: {exc}"})
            print(f"  {tid}: failed ({exc})")
    return 0


def cmd_status(_: list[str]) -> int:
    view = _current_view()
    if not view:
        print("(no tasks)")
        return 0
    now = time.time()
    counts: dict[str, int] = {}
    for t in view.values():
        counts[t["state"]] = counts.get(t["state"], 0) + 1
    print("counts:", counts)
    for tid, task in view.items():
        prompt_preview = task.get("prompt", "")[:60]
        flag = ""
        if task["state"] == "in_progress":
            age = now - max(h["ts"] for h in task["history"])
            if age > STALE_THRESHOLD_S:
                flag = f"  STUCK({int(age)}s)"
        print(f"  {tid}  {task['state']:12s}  {prompt_preview}{flag}")
    return 0


def cmd_reset(args: list[str]) -> int:
    if not args:
        print("usage: reset <task_id>", file=sys.stderr)
        return 2
    tid = args[0]
    _append({"task_id": tid, "state": "pending", "note": "manual reset"})
    print(f"reset {tid} to pending")
    return 0


COMMANDS = {"enqueue": cmd_enqueue, "drain": cmd_drain, "status": cmd_status, "reset": cmd_reset}


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in COMMANDS:
        print("usage: bg_task_runner.py {enqueue|drain|status|reset} [args]", file=sys.stderr)
        return 2
    return COMMANDS[argv[1]](argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

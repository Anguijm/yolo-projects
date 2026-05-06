"""Two-stage planner-executor pipeline.

Stage 1: Claude produces a JSON plan. Validator rejects malformed plans.
Stage 2: Codex executes each step with the full plan as context.

Both adapters fall through to deterministic stubs without API keys.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from system_prompts import EXECUTOR_PROMPT, PLANNER_PROMPT

ROOT = Path(__file__).parent
PLAN_PATH = ROOT / "last_plan.json"
REPORT_PATH = ROOT / "pipeline_report.json"


def _claude_call(system: str, user: str) -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        resp = Anthropic().messages.create(
            model="claude-opus-4-7",
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return resp.content[0].text
    # Stub: return a plausible plan shape.
    return json.dumps({
        "goal": f"Implement: {user[:60]}",
        "steps": [
            {
                "id": "step-1",
                "description": "Read existing target file to understand structure",
                "files": ["api/server.py"],
                "success_criterion": "file contents loaded into context",
            },
            {
                "id": "step-2",
                "description": "Add /healthcheck handler returning 200 OK",
                "files": ["api/server.py"],
                "success_criterion": "GET /healthcheck returns status 200 with body 'ok'",
            },
            {
                "id": "step-3",
                "description": "Add a unit test for the new endpoint",
                "files": ["tests/test_healthcheck.py"],
                "success_criterion": "pytest tests/test_healthcheck.py passes",
            },
        ],
    }, indent=2)


def _codex_call(system: str, user: str) -> str:
    if os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        resp = OpenAI().responses.create(
            model="gpt-5-codex",
            input=f"SYSTEM:\n{system}\n\nUSER:\n{user}",
        )
        return resp.output_text
    return f"[codex-stub] would produce a diff for step.\n--- a/file\n+++ b/file\n+ # added by codex\n"


def validate_plan(plan: dict) -> tuple[bool, str]:
    if not isinstance(plan, dict):
        return False, "plan is not a dict"
    if "goal" not in plan or "steps" not in plan:
        return False, "missing 'goal' or 'steps'"
    if not isinstance(plan["steps"], list) or not plan["steps"]:
        return False, "'steps' must be a non-empty list"
    for i, step in enumerate(plan["steps"]):
        for k in ("id", "description", "files", "success_criterion"):
            if k not in step:
                return False, f"step {i} missing '{k}'"
        if not isinstance(step["files"], list) or not step["files"]:
            return False, f"step {i} has no files"
        if not step["success_criterion"].strip():
            return False, f"step {i} has empty success_criterion"
    return True, "ok"


def get_plan(request: str, max_retries: int = 1) -> dict:
    user = f"Request: {request}\n\nReturn the plan JSON now."
    last_raw = ""
    for attempt in range(max_retries + 1):
        raw = _claude_call(PLANNER_PROMPT, user)
        last_raw = raw
        try:
            plan = json.loads(raw)
        except json.JSONDecodeError as exc:
            if attempt == max_retries:
                raise ValueError(f"planner returned non-JSON after {attempt+1} tries: {exc}")
            user = (
                f"Request: {request}\n\nYour previous response was:\n---\n{raw[:1000]}\n---\n"
                f"It was not valid JSON ({exc}). Return ONLY valid JSON now."
            )
            continue
        ok, reason = validate_plan(plan)
        if ok:
            return plan
        if attempt == max_retries:
            raise ValueError(f"planner returned invalid plan: {reason}")
        user = (
            f"Request: {request}\n\nYour previous plan was:\n---\n{raw[:1000]}\n---\n"
            f"It failed validation: {reason}. Return a corrected plan as JSON."
        )
    raise RuntimeError("unreachable")


def execute_plan(plan: dict) -> list[dict]:
    results = []
    accumulated = ""
    for step in plan["steps"]:
        prior = (
            f"\n\nPRIOR STEP DIFFS (use these as the current state of the files):\n{accumulated}"
            if accumulated else ""
        )
        executor_user = (
            f"PLAN:\n{json.dumps(plan, indent=2)}\n\n"
            f"EXECUTE STEP: {step['id']} — {step['description']}"
            f"{prior}"
        )
        diff = _codex_call(EXECUTOR_PROMPT, executor_user)
        results.append({
            "step_id": step["id"],
            "description": step["description"],
            "files": step["files"],
            "success_criterion": step["success_criterion"],
            "diff": diff,
        })
        accumulated += f"\n--- {step['id']} ---\n{diff}\n"
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", help="The change request to plan and execute")
    parser.add_argument("--max-retries", type=int, default=1, help="planner retry budget on JSON/validation failure")
    args = parser.parse_args()

    plan = get_plan(args.request, max_retries=args.max_retries)
    PLAN_PATH.write_text(json.dumps(plan, indent=2))
    print(f"plan ok: {len(plan['steps'])} steps -> {PLAN_PATH}")

    results = execute_plan(plan)
    REPORT_PATH.write_text(json.dumps({"goal": plan["goal"], "steps": results}, indent=2))
    print(f"executed {len(results)} steps -> {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

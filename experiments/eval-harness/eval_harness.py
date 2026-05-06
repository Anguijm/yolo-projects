"""Run a list of tasks against an agent fn, score each, write a report."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Callable

import os
from rubric import score

REPORT_PATH = Path(__file__).parent / "eval_report.json"


def _stub_agent(prompt: str) -> str:
    """Deterministic stub used when the harness is invoked from the CLI without
    a custom agent. Just echoes a canned answer per known prompt prefix."""
    canned = {
        "What is 2+2?": "4",
        "Capital of Japan?": "Tokyo",
        "Return JSON": '{"ok": true}',
        "List three primes": "2, 3, 5",
    }
    for k, v in canned.items():
        if prompt.startswith(k):
            return v
    return "(stub: no canned answer for this prompt)"


def run_eval(agent_fn: Callable[[str], str], tasks_path: str | Path = "tasks.json") -> dict:
    tasks = json.loads(Path(tasks_path).read_text())
    records = []
    for t in tasks:
        start = time.monotonic()
        try:
            output = agent_fn(t["prompt"])
            err = None
        except Exception as exc:
            output = ""
            err = f"{type(exc).__name__}: {exc}"
        latency = time.monotonic() - start
        s = 0.0 if err else score(output, t["rubric"])
        records.append({
            "task_id": t["id"],
            "prompt": t["prompt"],
            "output": output[:500],
            "rubric_type": t["rubric"]["type"],
            "score": round(s, 3),
            "latency_s": round(latency, 4),
            "error": err,
        })
    avg = sum(r["score"] for r in records) / len(records) if records else 0.0
    passed = sum(1 for r in records if r["score"] >= 0.95)
    score_failed = sum(1 for r in records if r["score"] < 0.95 and r.get("error") is None)
    agent_failed = sum(1 for r in records if r.get("error") is not None)
    degraded = bool(os.environ.get("ANTHROPIC_API_KEY")) is False and any(r["rubric_type"] == "llm" for r in records)
    aggregate = {
        "task_count": len(records),
        "avg_score": round(avg, 3),
        "passed": passed,
        "score_failed": score_failed,
        "agent_failed": agent_failed,
        "total_latency_s": round(sum(r["latency_s"] for r in records), 3),
        "degraded_mode": degraded,
    }
    report = {"aggregate": aggregate, "records": records}
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    return report


def main(argv: list[str]) -> int:
    tasks_path = argv[1] if len(argv) > 1 else "tasks.json"
    report = run_eval(_stub_agent, tasks_path)
    agg = report["aggregate"]
    print(f"avg_score={agg['avg_score']:.3f}  passed={agg['passed']}/{agg['task_count']}  latency={agg['total_latency_s']:.2f}s")
    print(f"wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

"""Render an eval_report.json into a short markdown summary suitable for
injection into the next agent run's context."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def render(report: dict) -> str:
    agg = report["aggregate"]
    lines = [
        "## Previous run summary",
        f"- avg_score: {agg['avg_score']:.3f}",
        f"- passed: {agg['passed']} / {agg['task_count']}",
        f"- total latency: {agg['total_latency_s']:.2f}s",
    ]
    failures = [r for r in report["records"] if r["score"] < 0.95]
    if failures:
        lines.append("\n### Failures (top 3)")
        for r in failures[:3]:
            lines.append(f"- `{r['task_id']}` (score={r['score']:.2f}): {r['prompt'][:60]}")
            lines.append(f"  output: {r['output'][:120]}")
    else:
        lines.append("\nAll tasks passed.")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: feedback_inject.py <eval_report.json>", file=sys.stderr)
        return 2
    report = json.loads(Path(argv[1]).read_text())
    print(render(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

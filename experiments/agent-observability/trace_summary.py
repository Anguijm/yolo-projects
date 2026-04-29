"""Aggregate a traces.jsonl file into per-tool latency / token / failure stats."""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


def _read(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = max(0, min(len(s) - 1, int(round(pct / 100 * (len(s) - 1)))))
    return s[idx]


def summarize(records: list[dict]) -> dict:
    by_tool: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_tool[r.get("tool") or "(no-tool)"].append(r)
    rows = []
    for tool, recs in sorted(by_tool.items()):
        latencies = [r["latency_ms"] for r in recs if r.get("latency_ms") is not None]
        token_in = sum(r.get("token_in") or 0 for r in recs)
        token_out = sum(r.get("token_out") or 0 for r in recs)
        errs = sum(1 for r in recs if r.get("status") == "error")
        rows.append({
            "tool": tool,
            "calls": len(recs),
            "p50_ms": _percentile(latencies, 50),
            "p95_ms": _percentile(latencies, 95),
            "token_in": token_in,
            "token_out": token_out,
            "error_rate": errs / len(recs) if recs else 0.0,
        })
    slowest = sorted(records, key=lambda r: r.get("latency_ms", 0), reverse=True)[:5]
    return {"per_tool": rows, "slowest": slowest, "total_spans": len(records)}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: trace_summary.py <traces.jsonl>", file=sys.stderr)
        return 2
    records = _read(Path(argv[1]))
    summary = summarize(records)
    print(f"total spans: {summary['total_spans']}")
    print()
    print(f"{'tool':35s} {'calls':>6} {'p50ms':>7} {'p95ms':>7} {'tok_in':>8} {'tok_out':>8} {'err%':>6}")
    print("-" * 85)
    for r in summary["per_tool"]:
        print(
            f"{r['tool']:35s} {r['calls']:>6} {r['p50_ms']:>7.0f} {r['p95_ms']:>7.0f} "
            f"{r['token_in']:>8} {r['token_out']:>8} {r['error_rate']*100:>5.1f}%"
        )
    print()
    print("slowest 5:")
    for r in summary["slowest"]:
        print(f"  {r.get('latency_ms',0):>6}ms  {r.get('name'):20s}  {r.get('tool','')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

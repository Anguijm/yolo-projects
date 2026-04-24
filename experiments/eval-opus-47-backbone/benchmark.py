#!/usr/bin/env python3
"""
Benchmark Opus 4.7 vs Haiku 4.5 as the council.py backbone.

Runs the council `implementation` gate on 3 canonical YOLO utility fixtures
using each model and records verdicts, latency, token counts, and cost.

Usage:
    python3 experiments/eval-opus-47-backbone/benchmark.py [--fixtures N] [--dry-run] [--output PATH]

See --help for full flag list. Requires ANTHROPIC_API_KEY in environment.

Cost model defaults (as of 2026-04-24):
    Haiku 4.5: $0.80 in / $4.00 out per MTok
    Opus 4.7:  $15.00 in / $75.00 out per MTok
Override via env vars: HAIKU_COST_IN, HAIKU_COST_OUT, OPUS_COST_IN, OPUS_COST_OUT
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

FIXTURES = [
    ("url-dissect",    REPO_ROOT / "url-dissect"    / "index.html"),
    ("cron-explain",   REPO_ROOT / "cron-explain"   / "index.html"),
    ("uuid-inspector", REPO_ROOT / "uuid-inspector" / "index.html"),
]

MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "opus":  "claude-opus-4-7",
}

# Cost defaults — single-line edit target when Anthropic updates pricing
_HAIKU_IN_DEFAULT  = 0.80   # $/MTok input
_HAIKU_OUT_DEFAULT = 4.00   # $/MTok output
_OPUS_IN_DEFAULT   = 15.00  # $/MTok input
_OPUS_OUT_DEFAULT  = 75.00  # $/MTok output

GOAL = (
    "Single-file HTML utility tool with clean UX, pure-JS, no external deps. "
    "Evaluate implementation quality across correctness, security, and UX dimensions."
)


def _load_cost_model() -> dict[str, dict[str, float]]:
    """Build cost table, applying env-var overrides and logging them."""
    haiku_in  = float(os.environ.get("HAIKU_COST_IN",  _HAIKU_IN_DEFAULT))
    haiku_out = float(os.environ.get("HAIKU_COST_OUT", _HAIKU_OUT_DEFAULT))
    opus_in   = float(os.environ.get("OPUS_COST_IN",   _OPUS_IN_DEFAULT))
    opus_out  = float(os.environ.get("OPUS_COST_OUT",  _OPUS_OUT_DEFAULT))

    if haiku_in  != _HAIKU_IN_DEFAULT  or haiku_out != _HAIKU_OUT_DEFAULT:
        print(f"[benchmark] cost model overridden from env: haiku in=${haiku_in}/MTok out=${haiku_out}/MTok")
    if opus_in   != _OPUS_IN_DEFAULT   or opus_out  != _OPUS_OUT_DEFAULT:
        print(f"[benchmark] cost model overridden from env: opus  in=${opus_in}/MTok out=${opus_out}/MTok")

    return {
        "haiku": {"in": haiku_in,  "out": haiku_out},
        "opus":  {"in": opus_in,   "out": opus_out},
    }


def _cost(model_key: str, input_tokens: int, output_tokens: int, costs: dict) -> float:
    c = costs[model_key]
    return (input_tokens * c["in"] + output_tokens * c["out"]) / 1_000_000


class TokenTracker:
    """Wrap client.messages.create to intercept per-call token usage."""

    def __init__(self, client: Any) -> None:
        self._client = client
        self._orig = client.messages.create
        self.records: list[dict] = []

    def __enter__(self) -> "TokenTracker":
        orig = self._orig
        tracker = self

        def _wrapped(*args, **kwargs):
            t0 = time.monotonic()
            response = orig(*args, **kwargs)
            elapsed = time.monotonic() - t0
            tracker.records.append({
                "latency_s": round(elapsed, 3),
                "input_tokens":  getattr(response.usage, "input_tokens",  0),
                "output_tokens": getattr(response.usage, "output_tokens", 0),
            })
            return response

        self._client.messages.create = _wrapped
        return self

    def __exit__(self, *_) -> None:
        self._client.messages.create = self._orig

    @property
    def total_input(self) -> int:
        return sum(r["input_tokens"] for r in self.records)

    @property
    def total_output(self) -> int:
        return sum(r["output_tokens"] for r in self.records)


def run_one(
    fixture_name: str,
    context_path: Path,
    model_key: str,
    client: Any,
    costs: dict,
) -> dict:
    """Run one (fixture, model) pair. Guarantees council module state restoration."""
    import council  # local import so REPO_ROOT sys.path manipulation happens first

    orig_backend  = council._BACKEND
    orig_client   = council._ANTHROPIC_CLIENT
    orig_model    = council.CLAUDE_MODEL

    try:
        council._BACKEND          = "claude"
        council._ANTHROPIC_CLIENT = client
        council.CLAUDE_MODEL      = MODELS[model_key]

        with TokenTracker(client) as tracker:
            t0 = time.monotonic()
            verdicts = council.run_gate(
                gate="implementation",
                project=fixture_name,
                goal=GOAL,
                context_path=str(context_path),
                inline_context="benchmark evaluation — no prior council artifacts",
            )
            gate_latency = round(time.monotonic() - t0, 2)

        approve = sum(1 for v in verdicts if v.verdict == "APPROVE")
        obj     = sum(1 for v in verdicts if v.verdict == "OBJECT")

        return {
            "fixture":       fixture_name,
            "model":         model_key,
            "model_id":      MODELS[model_key],
            "gate_latency_s": gate_latency,
            "approve":       approve,
            "object":        obj,
            "input_tokens":  tracker.total_input,
            "output_tokens": tracker.total_output,
            "cost_usd":      round(_cost(model_key, tracker.total_input, tracker.total_output, costs), 4),
            "cost_model_used": {
                "haiku_in":  costs["haiku"]["in"],
                "haiku_out": costs["haiku"]["out"],
                "opus_in":   costs["opus"]["in"],
                "opus_out":  costs["opus"]["out"],
            },
            "verdicts": [
                {
                    "angle":    v.angle,
                    "verdict":  v.verdict,
                    "severity": v.severity,
                    "reason":   v.reason,
                }
                for v in verdicts
            ],
        }
    finally:
        council._BACKEND          = orig_backend
        council._ANTHROPIC_CLIENT = orig_client
        council.CLAUDE_MODEL      = orig_model


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark Opus 4.7 vs Haiku 4.5 as the council.py backbone.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--fixtures", type=int, default=3, metavar="N",
                        help="Number of fixtures to run (1–3, default 3). Uses first N from fixture list.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print planned runs without making API calls, then exit 0.")
    parser.add_argument("--output", metavar="PATH",
                        help="Output JSON path (default: timestamped benchmark_results_<TS>.json in this directory).")
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent
    # Validate output path stays within repo
    if args.output:
        out_path = Path(args.output).resolve()
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        out_path = out_dir / f"benchmark_results_{ts}.json"

    try:
        out_path.relative_to(REPO_ROOT)
    except ValueError:
        print(f"[benchmark] ERROR: output path {out_path} is outside repo root {REPO_ROOT}", file=sys.stderr)
        sys.exit(1)

    fixtures = FIXTURES[:max(1, min(args.fixtures, len(FIXTURES)))]
    planned = [(name, path, mk) for (name, path) in fixtures for mk in ("haiku", "opus")]

    if args.dry_run:
        print(f"[benchmark] dry-run: {len(planned)} planned runs")
        for (name, path, mk) in planned:
            print(f"  {name} × {mk} ({MODELS[mk]})")
        print(f"[benchmark] output would be: {out_path}")
        sys.exit(0)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("[benchmark] ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    try:
        import anthropic as anthropic_sdk
    except ImportError:
        print("[benchmark] ERROR: anthropic SDK not installed", file=sys.stderr)
        sys.exit(1)

    if os.environ.get("GEMINI_API_KEY"):
        print("[benchmark] WARNING: GEMINI_API_KEY is set but ignored — benchmark forces Claude backend for apples-to-apples comparison")

    costs = _load_cost_model()
    client = anthropic_sdk.Anthropic(api_key=api_key)

    results: list[dict] = []
    for i, (name, path, model_key) in enumerate(planned, 1):
        print(f"[benchmark] run {i}/{len(planned)}: {name} × {model_key} ({MODELS[model_key]})")
        rec = run_one(name, path, model_key, client, costs)
        results.append(rec)
        print(f"  → latency={rec['gate_latency_s']}s  approve={rec['approve']}/7  tokens={rec['input_tokens']}in+{rec['output_tokens']}out  cost=${rec['cost_usd']}")
        # Save incrementally so partial runs are recoverable
        out_path.write_text(json.dumps(results, indent=2))

    print(f"[benchmark] DONE — {len(results)} runs saved to {out_path.name}")


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    main()

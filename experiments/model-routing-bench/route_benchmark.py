"""Benchmark a single-model strategy vs a routed strategy across N tasks."""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
from pathlib import Path

from model_router import classify, route

DEFAULT_MODEL = "claude-opus-4-7"
TASKS_PATH = Path(__file__).parent / "tasks.json"
RESULTS_PATH = Path(__file__).parent / "route_results.json"


def _stub_call(model: str, prompt: str) -> tuple[str, float]:
    """Deterministic stub: latency and quality vary by model+class. Real
    adapters replace this whole function."""
    seed = int(hashlib.sha256(f"{model}{prompt}".encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    base_latency = {
        "claude-opus-4-7": 0.04,
        "gpt-5-codex": 0.03,
        "gemini-1.5-pro": 0.05,
        "claude-haiku-4-5": 0.01,
    }.get(model, 0.04)
    latency = base_latency + rng.uniform(0, 0.02)
    time.sleep(latency)
    return (f"[{model}-stub] response to {prompt[:40]!r}", latency)


def _real_call(model: str, prompt: str) -> tuple[str, float]:
    if model.startswith("claude") and os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        start = time.monotonic()
        client = Anthropic()
        resp = client.messages.create(model=model, max_tokens=512, messages=[{"role": "user", "content": prompt}])
        return (resp.content[0].text, time.monotonic() - start)
    if (model.startswith("gpt") or model.startswith("o")) and os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        start = time.monotonic()
        resp = OpenAI().responses.create(model=model, input=prompt)
        return (resp.output_text, time.monotonic() - start)
    if model.startswith("gemini") and os.environ.get("GOOGLE_API_KEY"):
        # Google SDK varies by version; left as a hook.
        pass
    return _stub_call(model, prompt)


def _quality(prompt: str, model: str) -> float:
    """Synthetic quality score: matched-class models score higher. Replace
    with rubric scoring once eval-harness is in place."""
    cls = classify(prompt).task_class
    matched = ROUTING_AS_DICT.get(cls) == model
    base = 0.85 if matched else 0.65
    seed = int(hashlib.sha256(f"q{model}{prompt}".encode()).hexdigest(), 16) % 100
    return round(base + (seed - 50) / 1000, 3)


from model_router import ROUTING_RULES as ROUTING_AS_DICT


def run_strategy(strategy: str, tasks: list[dict]) -> dict:
    records = []
    for t in tasks:
        prompt = t["prompt"]
        if strategy == "single":
            model = DEFAULT_MODEL
            cls = "(forced)"
        else:  # routed
            cls = classify(prompt).task_class
            model = route(cls)
        _, latency = _real_call(model, prompt)
        score = _quality(prompt, model)
        records.append({
            "id": t["id"],
            "model": model,
            "task_class": cls,
            "latency_s": round(latency, 4),
            "score": score,
        })
    avg_score = sum(r["score"] for r in records) / len(records) if records else 0
    total_latency = sum(r["latency_s"] for r in records)
    return {
        "strategy": strategy,
        "avg_score": round(avg_score, 3),
        "total_latency_s": round(total_latency, 3),
        "tasks": records,
    }


def main() -> int:
    tasks = json.loads(TASKS_PATH.read_text())
    results = [run_strategy("single", tasks), run_strategy("routed", tasks)]
    RESULTS_PATH.write_text(json.dumps({"strategies": results}, indent=2))
    print(f"wrote {RESULTS_PATH}")
    print()
    print(f"{'strategy':10s} {'avg_score':>10} {'latency_s':>10}")
    print("-" * 35)
    for r in results:
        print(f"{r['strategy']:10s} {r['avg_score']:>10.3f} {r['total_latency_s']:>10.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

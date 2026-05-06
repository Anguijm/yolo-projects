"""Self-evolving agent loop with constrained reflector edits.

Each iteration:
  1. Run the agent (with current system prompt) on every task in tasks.json.
  2. Score each output against its rubric.
  3. If avg_score < threshold, ask the reflector model for a small edit.
  4. Apply the edit, write the new prompt, advance to next iteration.

Both the agent and reflector use stub adapters when no API key is set, so
the script runs end-to-end without credentials. The stub is deterministic
enough that the evolution path is repeatable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
PROMPTS_DIR = ROOT / "prompts"
EVOLUTION_LOG = ROOT / "evolution_log.jsonl"
TASKS_PATH = ROOT / "tasks.json"


def _agent_call(system_prompt: str, user_prompt: str) -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        resp = Anthropic().messages.create(
            model="claude-opus-4-7",
            max_tokens=512,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return resp.content[0].text
    # Deterministic stub: agent quality scales with prompt specificity.
    seed_input = f"{system_prompt}|{user_prompt}"
    seed = int(hashlib.sha256(seed_input.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    specificity = sum(1 for k in ("concise", "exact", "json", "only the answer", "no explanation") if k in system_prompt.lower())
    if rng.random() < 0.4 + 0.15 * specificity:
        # Agent gets it right.
        if "17 * 23" in user_prompt:
            return "391"
        if "square root of 144" in user_prompt:
            return "12"
        if "maximum of" in user_prompt:
            return "max([3, 1, 4, 1, 5, 9, 2, 6])  # 9"
        if "capital of Australia" in user_prompt:
            return "Canberra"
        if 'JSON object {"x"' in user_prompt:
            return '{"x": 1, "y": 2}'
        return "(correct)"
    # Wrong answer.
    return "I'm not sure but here's a long-winded ramble that doesn't follow the format."


def _reflector_edit(prompt: str, failures: list[dict]) -> str:
    """Return a new prompt with a single-line addition addressing the
    most common failure mode. Stub-deterministic when no key is set.

    Cycle 2: 5 heuristics instead of 3. Skips additions already present.
    """
    if not failures:
        return prompt
    sample_outputs = " ".join(f["output"][:120] for f in failures[:3]).lower()
    rubrics = [r for f in failures for r in f.get("rubric", [])]
    rubric_text = " ".join(rubrics).lower()
    additions = []
    if "ramble" in sample_outputs or len(sample_outputs) > 200:
        additions.append("Be concise. Output only the answer.")
    if "json" in sample_outputs or any('"' in r for r in rubrics):
        additions.append("When asked for JSON, return valid JSON only — no prose.")
    # New: numeric-answer heuristic
    if any(r.replace(".", "").replace("-", "").isdigit() for r in rubrics):
        additions.append("When the answer is a number, return ONLY the number.")
    # New: proper-noun heuristic
    if any(r and r[0].isupper() and r.isalpha() for r in rubrics if isinstance(r, str)):
        additions.append("Return names exactly as commonly written, with no extra words.")
    if not additions:
        additions.append("Read the question carefully and answer exactly what was asked.")
    # Pick the first heuristic whose addition isn't already in the prompt.
    for addition in additions:
        if addition not in prompt:
            return prompt.rstrip() + "\n" + addition + "\n"
    return prompt


@dataclass
class TaskScore:
    task_id: str
    output: str
    score: float
    rubric: list[str]


def score_task(output: str, rubric: list[str]) -> float:
    if not rubric:
        return 0.0
    matched = sum(1 for r in rubric if r.lower() in output.lower())
    return matched / len(rubric)


def run_iteration(prompt: str, tasks: list[dict]) -> list[TaskScore]:
    results = []
    for t in tasks:
        out = _agent_call(prompt, t["prompt"])
        results.append(TaskScore(task_id=t["id"], output=out, score=score_task(out, t["rubric"]), rubric=t["rubric"]))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=0.95)
    args = parser.parse_args()

    PROMPTS_DIR.mkdir(exist_ok=True)
    EVOLUTION_LOG.unlink(missing_ok=True)
    tasks = json.loads(TASKS_PATH.read_text())

    current_prompt = (PROMPTS_DIR / "prompt_v0.txt").read_text()

    prev_avg = -1.0
    prev_prompt = current_prompt
    for i in range(args.iterations):
        results = run_iteration(current_prompt, tasks)
        avg = sum(r.score for r in results) / len(results)
        failures = [{"task_id": r.task_id, "output": r.output, "rubric": r.rubric} for r in results if r.score < 1.0]
        regressed = i > 0 and avg < prev_avg - 0.01
        record = {
            "iteration": i,
            "prompt_version": f"prompt_v{i}.txt",
            "avg_score": round(avg, 3),
            "passed": sum(1 for r in results if r.score == 1.0),
            "total": len(results),
            "regressed": regressed,
            "failures": failures,
        }
        with EVOLUTION_LOG.open("a") as f:
            f.write(json.dumps(record) + "\n")
        print(f"iter {i}: avg={avg:.3f} passed={record['passed']}/{record['total']}{' [REGRESSED]' if regressed else ''}")

        if regressed:
            print(f"regression detected (was {prev_avg:.3f}, now {avg:.3f}); reverting to prev prompt and stopping")
            current_prompt = prev_prompt
            break

        if avg >= args.threshold:
            print("threshold reached, stopping")
            break
        new_prompt = _reflector_edit(current_prompt, failures)
        if new_prompt == current_prompt:
            print("reflector produced no change, stopping")
            break
        prev_avg = avg
        prev_prompt = current_prompt
        current_prompt = new_prompt
        diff_line = next((ln for ln in current_prompt.splitlines() if ln and ln not in prev_prompt), "")
        with EVOLUTION_LOG.open("a") as f:
            f.write(json.dumps({"iteration": i, "edit_added": diff_line}) + "\n")
        (PROMPTS_DIR / f"prompt_v{i+1}.txt").write_text(current_prompt)

    print(f"done. evolution log: {EVOLUTION_LOG}")
    print(f"final prompt: prompts/prompt_v{i}.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Scoring functions for the eval harness. Each returns float in [0, 1]."""
from __future__ import annotations

import os
import re
from typing import Any


def keyword_match(output: str, spec: dict[str, Any]) -> float:
    keywords = spec["keywords"]
    if not keywords:
        return 0.0
    out = output.lower()
    matched = sum(1 for k in keywords if k.lower() in out)
    return matched / len(keywords)


def regex_match(output: str, spec: dict[str, Any]) -> float:
    pattern = re.compile(spec["pattern"], re.IGNORECASE | re.DOTALL if spec.get("multiline") else re.IGNORECASE)
    return 1.0 if pattern.search(output) else 0.0


def exact_match(output: str, spec: dict[str, Any]) -> float:
    expected = spec["expected"]
    return 1.0 if output.strip() == expected.strip() else 0.0


def length_within(output: str, spec: dict[str, Any]) -> float:
    lo, hi = spec["min"], spec["max"]
    n = len(output)
    return 1.0 if lo <= n <= hi else 0.0


def llm_judge(output: str, spec: dict[str, Any]) -> float:
    """Send output + criteria to a judge model. Stubs to keyword fallback when no key."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        # Fall back to keyword match against the criteria as a stub.
        return keyword_match(output, {"keywords": spec.get("must_mention", [])})
    from anthropic import Anthropic
    judge_prompt = (
        "Score the following output on a scale of 0.0 to 1.0 based on the "
        "criteria. Return ONLY a JSON object: {\"score\": <float>}.\n\n"
        f"OUTPUT:\n{output}\n\nCRITERIA:\n{spec.get('criteria', '')}"
    )
    resp = Anthropic().messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    text = resp.content[0].text
    m = re.search(r'"score"\s*:\s*([0-9.]+)', text)
    return float(m.group(1)) if m else 0.0


SCORERS = {
    "keyword": keyword_match,
    "regex": regex_match,
    "exact": exact_match,
    "length": length_within,
    "llm": llm_judge,
}


def score(output: str, spec: dict[str, Any]) -> float:
    fn = SCORERS.get(spec["type"])
    if fn is None:
        raise ValueError(f"unknown rubric type: {spec['type']}")
    return fn(output, spec)

"""Task classifier + model routing rules.

The classifier is intentionally crude — keyword + length heuristics. Real
routing should learn from the benchmark output, not from hand-coded rules.
This module is the seed.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

ROUTING_RULES = {
    "reasoning": "claude-opus-4-7",
    "code": "gpt-5-codex",
    "long_context": "gemini-1.5-pro",
    "simple": "claude-haiku-4-5",
}

CODE_HINTS = re.compile(
    r"\b(def |class |function |implement|refactor|fix the bug|write code|pytest|unit test|TypeScript|Python|JavaScript|SQL|regex)\b",
    re.IGNORECASE,
)
REASONING_HINTS = re.compile(
    r"\b(why|explain|reason|trade.?off|compare|argue|infer|derive|prove)\b",
    re.IGNORECASE,
)


@dataclass
class Classification:
    task_class: str
    rationale: str


def classify(prompt: str) -> Classification:
    if len(prompt) > 8000:
        return Classification("long_context", f"prompt is {len(prompt)} chars (>8000)")
    if CODE_HINTS.search(prompt):
        return Classification("code", "matched code keywords")
    if REASONING_HINTS.search(prompt):
        return Classification("reasoning", "matched reasoning keywords")
    if len(prompt) < 120:
        return Classification("simple", f"prompt is {len(prompt)} chars (<120)")
    return Classification("reasoning", "default fallback")


def route(task_class: str) -> str:
    return ROUTING_RULES.get(task_class, ROUTING_RULES["reasoning"])

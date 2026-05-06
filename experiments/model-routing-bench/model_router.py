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

# Note: explicit non-letter boundary instead of \b. \b doesn't fire between
# `_` and a letter (underscore is a word character), so prompts with
# underscored placeholder text — common in ML/data work — silently fail
# keyword matching. Cycle 3 found this on long-1.
_BEFORE = r"(?:^|[^a-zA-Z])"
_AFTER = r"(?:[^a-zA-Z]|$)"
CODE_HINTS = re.compile(
    _BEFORE + r"(def |class |function |implement|refactor|fix the bug|write code|pytest|unit test|TypeScript|Python|JavaScript|SQL|regex)" + _AFTER,
    re.IGNORECASE,
)
REASONING_HINTS = re.compile(
    _BEFORE + r"(why|explain|reason|trade.?off|compare|argue|infer|derive|prove)" + _AFTER,
    re.IGNORECASE,
)
LONG_CONTEXT_HINTS = re.compile(
    _BEFORE + r"(summarize|extract|from this document|key entities|tldr)" + _AFTER,
    re.IGNORECASE,
)


@dataclass
class Classification:
    task_class: str
    rationale: str


def classify(prompt: str) -> Classification:
    if not prompt or not prompt.strip():
        raise ValueError("classify: prompt must be non-empty")
    # Long-context detection: either size OR keyword signals.
    if len(prompt) > 4000:
        return Classification("long_context", f"prompt is {len(prompt)} chars (>4000)")
    if LONG_CONTEXT_HINTS.search(prompt) and len(prompt) > 500:
        return Classification("long_context", "matched long-context keywords + length>500")
    if CODE_HINTS.search(prompt):
        return Classification("code", "matched code keywords")
    if REASONING_HINTS.search(prompt):
        return Classification("reasoning", "matched reasoning keywords")
    if len(prompt) < 120:
        return Classification("simple", f"prompt is {len(prompt)} chars (<120)")
    return Classification("reasoning", "default fallback")


def route(task_class: str) -> str:
    return ROUTING_RULES.get(task_class, ROUTING_RULES["reasoning"])

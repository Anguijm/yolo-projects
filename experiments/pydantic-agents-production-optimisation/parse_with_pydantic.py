#!/usr/bin/env python3
"""Pydantic-validated parser for council Verdicts.

Drop-in replacement for the ad-hoc JSON parse path currently in
.harness/scripts/council.py. Returns a typed Verdict on success or a
structured ParseError on failure — never silently degrades to a phantom
OBJECT.

Usage:
    from parse_with_pydantic import parse_verdict
    result = parse_verdict(raw_model_output)
    if isinstance(result, ParseError):
        log_and_retry(result)
    else:
        consume(result)

Demo:
    python3 parse_with_pydantic.py --demo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Union

from verdict_schema import ParseError, Verdict

try:
    from pydantic import ValidationError
except ImportError as e:
    raise SystemExit(f"pydantic not installed: {e}")


def _snippet(text: str, n: int = 200) -> str:
    text = text.strip()
    if len(text) <= 2 * n + 5:
        return text
    return f"{text[:n]} ... {text[-n:]}"


def _strip_fences(text: str) -> str:
    """Strip ```json ... ``` or ``` ... ``` wrappers if present."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


def parse_verdict(raw: str) -> Union[Verdict, ParseError]:
    """Parse a raw LLM verdict response into a Verdict or ParseError.

    The three failure modes are distinguishable:
      - empty_output: raw is empty/whitespace after fence-stripping
      - json_decode: JSON parsing itself failed
      - schema_violation: JSON parsed but doesn't match the Verdict schema
    """
    if not raw or not raw.strip():
        return ParseError(
            kind="empty_output",
            detail="raw output was empty or whitespace-only",
            raw_snippet="",
        )

    cleaned = _strip_fences(raw)
    if not cleaned:
        return ParseError(
            kind="empty_output",
            detail="raw output was only code-fence markers",
            raw_snippet=_snippet(raw),
        )

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return ParseError(
            kind="json_decode",
            detail=f"{type(e).__name__}: {e.msg} at pos {e.pos}",
            raw_snippet=_snippet(cleaned),
        )

    try:
        return Verdict.model_validate(payload)
    except ValidationError as e:
        return ParseError(
            kind="schema_violation",
            detail="; ".join(
                f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}"
                for err in e.errors()
            ),
            raw_snippet=_snippet(cleaned),
        )


DEMO_INPUTS = [
    (
        "good_approve",
        '{"verdict": "APPROVE", "severity": "low", "reason": "Diff matches '
        'the rubric; no objections."}',
    ),
    (
        "good_object_with_fence",
        '```json\n{"verdict": "OBJECT", "severity": "high", "reason": '
        '"Missing test coverage", "required_fix": "Add tests for '
        'parse_verdict edge cases", "evidence": "parse_with_pydantic.py:42"}\n```',
    ),
    (
        "good_object_min",
        '{"verdict": "OBJECT", "severity": "medium", '
        '"reason": "Schema mismatch in upstream feed"}',
    ),
    (
        "bad_truncated_json",
        '{"verdict": "APPROVE", "severity": "low", "reason": "looks fi',
    ),
    (
        "bad_wrong_verdict_value",
        '{"verdict": "MAYBE", "severity": "low", "reason": "unsure"}',
    ),
    (
        "bad_empty",
        "   \n\n  ",
    ),
]


def run_demo() -> int:
    print("Parsing 6 canned council outputs:\n")
    fail_count = 0
    pass_count = 0
    for label, raw in DEMO_INPUTS:
        result = parse_verdict(raw)
        if isinstance(result, Verdict):
            pass_count += 1
            print(f"  [VERDICT] {label}: {result.verdict} ({result.severity}) — "
                  f"{result.reason[:60]}")
        else:
            fail_count += 1
            print(f"  [ERROR ] {label}: {result.kind} — {result.detail}")
    print(f"\nSummary: {pass_count} valid verdicts, {fail_count} structured errors")
    # Demo is healthy when it produces 3 valid + 3 structured errors.
    return 0 if (pass_count == 3 and fail_count == 3) else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true",
                   help="Run 6 canned inputs through parse_verdict")
    p.add_argument("--raw", default=None,
                   help="Parse a single raw string and print the result")
    args = p.parse_args()

    if args.raw is not None:
        result = parse_verdict(args.raw)
        if isinstance(result, Verdict):
            print(result.model_dump_json(indent=2))
            return 0
        print(f"ParseError: {result.kind}", file=sys.stderr)
        print(f"  detail: {result.detail}", file=sys.stderr)
        print(f"  snippet: {result.raw_snippet}", file=sys.stderr)
        return 1

    if args.demo:
        return run_demo()

    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

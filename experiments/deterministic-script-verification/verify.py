#!/usr/bin/env python3
"""Golden-fixture shape verifier for LLM-driven scripts.

Usage:
    python3 verify.py [--script PATH] [--input PATH] [--shape PATH] [--stub PATH]

With no arguments, verifies the bundled process_experiments fixture against
fixtures/synthetic_llm_response.json (stub mode — no API spend).

The verifier checks SHAPE, not content:
  - top-level container type
  - item count within [min_items, max_items]
  - per-item required keys present with correct types
  - nested-object required keys present
  - status values restricted to an allow-list

Exit codes: 0 = PASS, 1 = FAIL, 2 = config error.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_SHAPE = ROOT / "fixtures" / "process_experiments_expected_shape.json"
DEFAULT_STUB = ROOT / "fixtures" / "synthetic_llm_response.json"


TYPE_CHECKERS = {
    "string": lambda v: isinstance(v, str),
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "null_or_string": lambda v: v is None or isinstance(v, str),
    "null": lambda v: v is None,
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
}


def check_shape(payload, shape):
    """Return a list of failure strings; empty means PASS."""
    failures = []

    top = shape.get("top_level", "array")
    if top == "array" and not isinstance(payload, list):
        failures.append(f"top_level: expected array, got {type(payload).__name__}")
        return failures
    if top == "object" and not isinstance(payload, dict):
        failures.append(f"top_level: expected object, got {type(payload).__name__}")
        return failures

    if isinstance(payload, list):
        n = len(payload)
        lo = shape.get("min_items", 0)
        hi = shape.get("max_items", float("inf"))
        if n < lo:
            failures.append(f"count: {n} < min_items {lo}")
        if n > hi:
            failures.append(f"count: {n} > max_items {hi}")

        required_keys = shape.get("required_keys", [])
        key_types = shape.get("key_types", {})
        source_required = shape.get("source_required_keys", [])
        experiment_required = shape.get("experiment_required_keys", [])
        status_allowed = shape.get("status_allowed_values", [])

        for idx, item in enumerate(payload):
            if not isinstance(item, dict):
                failures.append(f"item[{idx}]: expected object, got {type(item).__name__}")
                continue
            for k in required_keys:
                if k not in item:
                    failures.append(f"item[{idx}].{k}: missing")
                    continue
                expected_type = key_types.get(k)
                if expected_type:
                    checker = TYPE_CHECKERS.get(expected_type)
                    if checker and not checker(item[k]):
                        failures.append(
                            f"item[{idx}].{k}: expected {expected_type}, "
                            f"got {type(item[k]).__name__}"
                        )
            if "source" in item and isinstance(item["source"], dict):
                for k in source_required:
                    if k not in item["source"]:
                        failures.append(f"item[{idx}].source.{k}: missing")
            if "experiment" in item and isinstance(item["experiment"], dict):
                for k in experiment_required:
                    if k not in item["experiment"]:
                        failures.append(f"item[{idx}].experiment.{k}: missing")
            if status_allowed and item.get("status") not in status_allowed:
                failures.append(
                    f"item[{idx}].status: {item.get('status')!r} "
                    f"not in {status_allowed}"
                )

    return failures


def load_json(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", default=str(DEFAULT_SHAPE),
                        help="path to expected-shape spec JSON")
    parser.add_argument("--stub", default=str(DEFAULT_STUB),
                        help="path to canonical LLM response (stub mode)")
    parser.add_argument("--script", default=None,
                        help="path to a script that prints JSON to stdout "
                             "(real mode — not implemented in this scaffold)")
    parser.add_argument("--input", default=None,
                        help="path to fixture input passed to --script")
    args = parser.parse_args()

    if args.script:
        print("ERROR: real-script mode not implemented in this scaffold.",
              file=sys.stderr)
        print("       The blocker is that scripts/process_experiments.py has no",
              file=sys.stderr)
        print("       --stub flag yet — see README follow-on tick #1.",
              file=sys.stderr)
        sys.exit(2)

    shape = load_json(args.shape)
    payload = load_json(args.stub)

    failures = check_shape(payload, shape)

    if failures:
        print(f"FAIL: {len(failures)} shape violation(s)", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)

    print(f"PASS: shape conforms ({len(payload)} item(s) checked)")
    sys.exit(0)


if __name__ == "__main__":
    main()

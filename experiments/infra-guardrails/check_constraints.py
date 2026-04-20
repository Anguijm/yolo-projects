#!/usr/bin/env python3
"""Verify program.md Build Constraints section: heading, IDs C1-C10, and parseable row format."""
import re
import sys

REQUIRED_IDS = [f"C{i}" for i in range(1, 11)]
REQUIRED_SECTIONS = ["## Build Constraints", "## Bedrock Rules", "## Rules", "## Testing Protocol"]
# Matches markdown table data rows: | C# | non-empty | non-empty | non-empty |
ROW_RE = re.compile(r"^\|\s*(C\d+)\s*\|([^|]+)\|([^|]+)\|([^|]+)\|", re.MULTILINE)


def check_constraints(path="program.md"):
    failures = []
    try:
        text = open(path).read()
    except FileNotFoundError:
        return [f"{path} not found"]

    for section in REQUIRED_SECTIONS:
        if section not in text:
            failures.append(f"Missing section: {section!r}")

    if "## Build Constraints" not in text:
        return failures  # can't check rows without the section

    found_ids = set()
    for m in ROW_RE.finditer(text):
        cid = m.group(1)
        fields = [m.group(i).strip() for i in range(1, 5)]
        if not all(fields):
            failures.append(f"Row {cid}: one or more empty fields")
        found_ids.add(cid)

    for cid in REQUIRED_IDS:
        if cid not in found_ids:
            failures.append(f"Missing constraint: {cid}")

    return failures


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "program.md"
    failures = check_constraints(path)
    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify program.md Build Constraints section: heading, IDs C1-C10, and parseable row format.

Usage:
  python3 check_constraints.py              # reads program.md from cwd
  python3 check_constraints.py program.md   # explicit path (for testing)

Exit code 0 = PASS, exit code 1 = FAIL with listed failures.

Checks performed:
  1. Required section headings present (## Build Constraints, ## Bedrock Rules, ## Rules, ## Testing Protocol)
  2. ## Build Constraints appears exactly once
  3. Section body (from heading to next ## heading) contains exactly the IDs C1-C10, no more, no fewer
  4. Each constraint row matches r"^\\s*\\|\\s*(C\\d+)\\s*\\|([^|]+)\\|([^|]+)\\|([^|]+)\\|" with all 4 fields non-empty
"""
import re
import sys

REQUIRED_IDS = {f"C{i}" for i in range(1, 11)}
REQUIRED_SECTIONS = ["## Build Constraints", "## Bedrock Rules", "## Rules", "## Testing Protocol"]
ROW_RE = re.compile(r"^\s*\|\s*(C\d+)\s*\|([^|]+)\|([^|]+)\|([^|]+)\|", re.MULTILINE)
SECTION_RE = re.compile(r"^\s*## Build Constraints\s*$(.*?)(?=^\s*## |\Z)", re.MULTILINE | re.DOTALL)


def check_constraints(path="program.md"):
    failures = []
    try:
        text = open(path).read()
    except FileNotFoundError:
        return [f"{path} not found"]

    for section in REQUIRED_SECTIONS:
        if section not in text:
            failures.append(f"Missing section: {section!r}")

    all_matches = SECTION_RE.findall(text)
    if len(all_matches) != 1:
        failures.append(f"## Build Constraints must appear exactly once; found {len(all_matches)}")
        return failures

    section_match = SECTION_RE.search(text)
    section_body = section_match.group(1)

    found_ids = set()
    for m in ROW_RE.finditer(section_body):
        cid = m.group(1)
        fields = [m.group(i).strip() for i in range(1, 5)]
        if not all(fields):
            failures.append(f"Row {cid}: one or more empty fields")
        found_ids.add(cid)

    missing = REQUIRED_IDS - found_ids
    extras = found_ids - REQUIRED_IDS
    for cid in sorted(missing):
        failures.append(f"Missing constraint: {cid}")
    for cid in sorted(extras):
        failures.append(f"Unexpected constraint ID: {cid} (section must contain exactly C1-C10)")

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

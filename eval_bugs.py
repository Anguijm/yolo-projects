#!/usr/bin/env python3
"""
eval_bugs.py — Golden Bug Eval Suite Runner

Scans a YOLO project's index.html for known bug patterns mined from learnings.md.
Runs each detection regex from eval_bugs.json against the extracted JS code.

Usage:
    python eval_bugs.py <project-name>
    python eval_bugs.py orbital-slingshot
    python eval_bugs.py --all          # scan every project

Exit code 0 if clean, 1 if any patterns matched.
"""

import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EVAL_FILE = SCRIPT_DIR / "eval_bugs.json"
PROJECTS_DIR = SCRIPT_DIR


def load_eval_suite():
    """Load the bug pattern definitions from eval_bugs.json."""
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_js_from_html(html_path):
    """Extract all JavaScript from an HTML file.

    Pulls content from:
    - <script> tags (inline JS)
    - on* event handler attributes
    Returns the concatenated JS as a single string.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    js_parts = []

    # Extract all script tags, skip ones with src attribute
    script_tag_re = re.compile(
        r"<script([^>]*)>([\s\S]*?)</script>", re.IGNORECASE
    )
    for attrs, body in script_tag_re.findall(content):
        if "src=" in attrs.lower():
            continue
        if body.strip():
            js_parts.append(body)

    # Also include on* event handler attribute values for completeness
    onattr_re = re.compile(r'\bon\w+\s*=\s*"([^"]*)"', re.IGNORECASE)
    for match in onattr_re.findall(content):
        if match.strip():
            js_parts.append(match)

    return "\n".join(js_parts), content


def run_pattern(pattern, js_code, full_html):
    """Run a single bug pattern against extracted JS code.

    Returns a list of match descriptions, or empty list if clean.
    """
    regex_str = pattern["detection_regex"]
    matches = []

    try:
        compiled = re.compile(regex_str, re.MULTILINE | re.DOTALL)
    except re.error as e:
        return [{"error": f"Invalid regex: {e}"}]

    # Some patterns apply to full HTML (like className), most to JS
    # Run against JS first, then full HTML for CSS/HTML patterns
    targets = [("JS", js_code)]

    # Patterns that need HTML context too
    html_patterns = {
        "classname-overwrite",
        "missing-pointercancel",
        "mouseup-on-canvas-only",
        "innerhtml-xss",
    }
    if pattern["pattern_id"] in html_patterns:
        targets.append(("HTML", full_html))

    for source_label, code in targets:
        for m in compiled.finditer(code):
            # Get the line number
            line_num = code[:m.start()].count("\n") + 1
            # Get the matched text (truncated)
            matched_text = m.group(0)
            if len(matched_text) > 120:
                matched_text = matched_text[:120] + "..."
            # Clean up for display
            matched_text = matched_text.replace("\n", "\\n")
            matches.append(
                {
                    "source": source_label,
                    "line": line_num,
                    "matched": matched_text,
                }
            )

    return matches


def scan_project(project_name, patterns, verbose=True):
    """Scan a single project for all bug patterns.

    Returns (total_matches, results_list).
    """
    html_path = PROJECTS_DIR / project_name / "index.html"

    if not html_path.exists():
        if verbose:
            print(f"  SKIP: {html_path} not found")
        return 0, []

    js_code, full_html = extract_js_from_html(html_path)

    if not js_code.strip():
        if verbose:
            print(f"  SKIP: No inline JS found in {project_name}")
        return 0, []

    results = []
    total_matches = 0

    for pattern in patterns:
        matches = run_pattern(pattern, js_code, full_html)
        if matches:
            total_matches += len(matches)
            results.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "description": pattern["description"],
                    "matches": matches,
                }
            )

    return total_matches, results


def print_results(project_name, total_matches, results):
    """Print scan results for a project."""
    if total_matches == 0:
        print(f"  {project_name}: CLEAN (0 matches)")
        return

    print(f"  {project_name}: {total_matches} potential bug(s) found")
    for result in results:
        pid = result["pattern_id"]
        desc = result["description"]
        count = len(result["matches"])
        print(f"    [{pid}] ({count}x) {desc[:80]}")
        for match in result["matches"][:3]:  # Show first 3 matches
            if "error" in match:
                print(f"      ERROR: {match['error']}")
            else:
                print(
                    f"      L{match['line']} ({match['source']}): {match['matched'][:90]}"
                )
        if count > 3:
            print(f"      ... and {count - 3} more")


def main():
    if len(sys.argv) < 2:
        print("Usage: python eval_bugs.py <project-name>")
        print("       python eval_bugs.py --all")
        print("       python eval_bugs.py --all --json")
        sys.exit(2)

    json_output = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    patterns = load_eval_suite()
    print(f"Loaded {len(patterns)} bug patterns from eval_bugs.json\n")

    if args[0] == "--all":
        # Scan all projects
        if not PROJECTS_DIR.exists():
            print(f"Projects directory not found: {PROJECTS_DIR}")
            sys.exit(2)

        projects = sorted(
            d.name
            for d in PROJECTS_DIR.iterdir()
            if d.is_dir() and (d / "index.html").exists()
        )
        print(f"Scanning {len(projects)} projects...\n")

        total_all = 0
        all_results = {}
        for project in projects:
            count, results = scan_project(project, patterns, verbose=False)
            total_all += count
            if results:
                all_results[project] = results
            if not json_output:
                print_results(project, count, results)

        print(f"\n{'='*60}")
        print(
            f"TOTAL: {total_all} potential bugs across {len(all_results)} projects"
        )
        print(f"Clean: {len(projects) - len(all_results)} projects")

        if json_output and all_results:
            print("\n" + json.dumps(all_results, indent=2))

        sys.exit(1 if total_all > 0 else 0)
    else:
        project_name = args[0]
        count, results = scan_project(project_name, patterns)
        print_results(project_name, count, results)

        if json_output and results:
            print("\n" + json.dumps(results, indent=2))

        sys.exit(1 if count > 0 else 0)


if __name__ == "__main__":
    main()

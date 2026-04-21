#!/usr/bin/env python3
"""Advisory UX completeness lens for YOLO single-file HTML builds.

Checks for: error state handling, empty state handling, loading states,
focus ring preservation, and presence of a primary interactive element.

Usage:
  python3 ux_completeness.py <project>/index.html
  python3 ux_completeness.py --help

Exit 0 always (advisory mode). Prints [WARN] lines then PASS or WARNINGS: N.
Exit 1 only if the file cannot be read or is not valid HTML.
"""
import os
import re
import sys

HELP = """ux_completeness.py — Advisory UX completeness lens for YOLO HTML builds.

Usage:
  python3 ux_completeness.py <path/to/index.html>

Checks (all advisory — never blocks the build):
  error-state    Does the app surface errors to the user?
  empty-state    When there are no results, does the app say so?
  loading-state  If async operations exist, is there a loading indicator?
  focus-ring     Is outline:none used without :focus-visible compensation?
  primary-cta    Does the app have at least one interactive element?

Output:
  [WARN] <check>: <description>   — one line per issue found
  PASS                            — no issues found
  WARNINGS: N                     — N issues found

Exit codes: 0 (always, advisory mode), 1 (file not found or not valid HTML).
"""


def read_html(path):
    """Open path with utf-8 encoding; validate HTML; return text or exit 1."""
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        print(f"ERROR: {path} not found")
        sys.exit(1)
    lower = text[:500].lower()
    if "<html" not in lower and "<!doctype" not in lower:
        print(f"ERROR: {path} does not appear to be an HTML file")
        sys.exit(1)
    return text


def check_ux_completeness(path):
    """Run all UX checks on path; return list of warning strings."""
    text = read_html(path)
    warnings = []

    # 1. Error state: does the app surface errors to the user?
    has_error_ui = bool(re.search(
        r'(?i)(\.error-|#error|class=["\'][^"\']*error|'
        r'something.went.wrong|try.again|catch\s*\(|onerror\s*=|'
        r'\.catch\s*\(|errorMessage|error-msg|errMsg)',
        text
    ))
    if not has_error_ui:
        warnings.append("error-state: no error UI pattern found (class=*error, catch(), onerror=, 'try again', etc.)")

    # 2. Empty state: when there are no results, does the app say so?
    has_list_or_output = bool(re.search(r'(?i)(<ul|<ol|<table|<tbody|<tr|output-area|result-area|results)', text))
    has_empty_state = bool(re.search(
        r'(?i)(no.results|nothing.here|no.data|no.items|no.\w+.found|'
        r'empty.state|data-empty|\.empty|placeholder.*text|nothing.to.show|'
        r'no.\w+.yet|start.by|enter.a|type.a|paste.a)',
        text
    ))
    if has_list_or_output and not has_empty_state:
        warnings.append("empty-state: list/table/output area detected but no empty-state messaging found")

    # 3. Loading state: if async operations exist, is there a loading indicator?
    has_async = bool(re.search(r'(?i)(fetch\s*\(|XMLHttpRequest|async\s+function|await\s+)', text))
    has_loading = bool(re.search(
        r'(?i)(loading|spinner|\.skeleton|aria-busy|progress|fetching|'
        r'please.wait|working\.\.\.)',
        text
    ))
    if has_async and not has_loading:
        warnings.append("loading-state: async operation detected (fetch/await) but no loading indicator found")

    # 4. Focus ring: check for outline removal without :focus-visible compensation
    has_outline_none = bool(re.search(r'outline\s*:\s*(none|0)', text))
    has_focus_visible = bool(re.search(r':focus-visible|:focus\s*\{[^}]*box-shadow', text))
    if has_outline_none and not has_focus_visible:
        warnings.append(
            "focus-ring: outline:none/0 found without :focus-visible or box-shadow compensation — "
            "keyboard users lose focus indicator"
        )

    # 5. Primary CTA: does the app have any interactive element?
    has_interactive = bool(re.search(
        r'(?i)(<button|<input|<select|<textarea|role=["\']button|role=["\']textbox)',
        text
    ))
    if not has_interactive:
        warnings.append("primary-cta: no interactive element found (<button>, <input>, <select>, <textarea>)")

    return warnings


def main():
    """CLI entry point: print warnings and PASS/WARNINGS:N summary."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print(HELP)
        sys.exit(0)
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <path/to/index.html>  (--help for details)")
        sys.exit(1)
    path = os.path.abspath(sys.argv[1])
    warnings = check_ux_completeness(path)
    for w in warnings:
        print(f"[WARN] {w}")
    if warnings:
        print(f"WARNINGS: {len(warnings)}")
    else:
        print("PASS")


if __name__ == "__main__":
    main()

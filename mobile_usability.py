#!/usr/bin/env python3
"""Advisory mobile usability lens for YOLO single-file HTML builds.

Checks for: viewport meta tag, @media queries, small tap targets,
horizontal table overflow handling, and touch-only event handlers.

Usage:
  python3 mobile_usability.py <project>/index.html
  python3 mobile_usability.py --help

Exit 0 always (advisory mode). Prints [WARN] lines then PASS or WARNINGS: N.
Exit 1 only if the file cannot be read or is not valid HTML.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))

HELP = """mobile_usability.py — Advisory mobile usability lens for YOLO HTML builds.

Usage:
  python3 mobile_usability.py <path/to/index.html>

Checks (all advisory — never blocks the build):
  viewport         Is <meta name="viewport"> present?
  responsive       Are @media queries present for responsive layout?
  tap-target       Are button/input font sizes above 0.7rem?
  table-overflow   Is overflow-x:auto set on a wrapper when <table> is used?
  touch-events     Are mouseover handlers paired with touch/focus equivalents?

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


def check_mobile_usability(path):
    """Run all mobile usability checks on path; return list of warning strings."""
    text = read_html(path)
    warnings = []

    # 1. Viewport meta tag
    has_viewport = bool(re.search(
        r'<meta[^>]+name=["\']viewport["\']',
        text,
        re.IGNORECASE
    ))
    if not has_viewport:
        warnings.append("viewport: missing <meta name=\"viewport\"> — page will not scale correctly on mobile")

    # 2. Responsive CSS (@media queries)
    has_media = bool(re.search(r'@media\s*\(', text))
    if not has_media:
        warnings.append("responsive: no @media queries found — layout may break on narrow screens")

    # 3. Small tap targets — font-size below 0.7rem on buttons/interactive elements
    small_font = re.search(
        r'(?:button|input|\.btn|\.cta)[^{]*\{[^}]*font-size\s*:\s*0\.[0-6]\d*rem',
        text,
        re.IGNORECASE | re.DOTALL
    )
    if small_font:
        warnings.append(
            "tap-target: button/input font-size below 0.7rem detected — "
            "tap targets may be too small on mobile (min recommended: 0.875rem / 44px height)"
        )

    # 4. Horizontal table overflow — table without overflow-x:auto on parent
    has_table = bool(re.search(r'<table', text, re.IGNORECASE))
    has_overflow_x = bool(re.search(r'overflow-x\s*:\s*auto', text))
    if has_table and not has_overflow_x:
        warnings.append(
            "table-overflow: <table> detected without overflow-x:auto on a wrapper — "
            "wide tables will overflow on mobile screens (see ip-cidr regression)"
        )

    # 5. Mouse-only event handlers without touch/keyboard equivalents
    has_mouseover = bool(re.search(r'(?:mouseover|mouseenter|mouseleave)\s*[,\)]', text))
    has_touch_or_focus = bool(re.search(r'(?:touchstart|touchend|pointerover|focus)\s*[,\)]', text))
    if has_mouseover and not has_touch_or_focus:
        warnings.append(
            "touch-events: mouseover/mouseenter/mouseleave used without touchstart/focus equivalents — "
            "hover interactions are inaccessible on touch-only devices"
        )

    return warnings


def main():
    """CLI entry point: print warnings and PASS/WARNINGS:N summary."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print(HELP)
        sys.exit(0)
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <path/to/index.html>  (--help for details)")
        sys.exit(1)
    path = os.path.realpath(sys.argv[1])
    if not (path == REPO_ROOT or path.startswith(REPO_ROOT + os.sep)):
        print(f"ERROR: {path} is outside the repo root ({REPO_ROOT}); refusing to read")
        sys.exit(1)
    warnings = check_mobile_usability(path)
    for w in warnings:
        print(f"[WARN] {w}")
    if warnings:
        print(f"WARNINGS: {len(warnings)}")
    else:
        print("PASS")


if __name__ == "__main__":
    main()

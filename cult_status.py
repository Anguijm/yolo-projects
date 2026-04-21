#!/usr/bin/env python3
"""Advisory cult-status differentiation lens for YOLO single-file HTML builds.

Heuristic check for signature-move indicators: animations, canvas/SVG,
keyboard shortcuts, real-time interactivity, and memorable hook presence.

Usage:
  python3 cult_status.py <project>/index.html
  python3 cult_status.py --help

Exit 0 always (advisory mode). Prints [WARN] lines then PASS or WARNINGS: N.
Exit 1 only if the file cannot be read or is not valid HTML.

Note: This lens is intentionally subjective. A WARNINGS result is a prompt
for the builder to consider differentiation, not a block.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))

HELP = """cult_status.py — Advisory differentiation lens for YOLO HTML builds.

Usage:
  python3 cult_status.py <path/to/index.html>

Checks (all advisory — never blocks the build):
  animation          Is any CSS animation/transition or Web Animation present?
  canvas-svg         Is <canvas> or <svg> used for custom visualization?
  keyboard-shortcuts Are keyboard shortcuts (keydown/keyup) implemented?
  realtime           Are input/change events used for live-as-you-type feedback?
  memorable-hook     Is there a descriptive <title>, <h1>, or <p> near the top?

Output:
  [WARN] <check>: <description>   — one line per issue found
  PASS                            — no issues found (tool has signature differentiation)
  WARNINGS: N                     — N issues found

This lens is intentionally subjective. PASS = strong differentiation signals.
WARNINGS = opportunities to make the tool more memorable.

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


def check_cult_status(path):
    """Run differentiation heuristics on path; return list of warning strings."""
    text = read_html(path)
    warnings = []

    # 1. Animation or transition — "it moves"
    has_animation = bool(re.search(
        r'(?:@keyframes|transition\s*:|animation\s*:|animate\s*\()',
        text,
        re.IGNORECASE
    ))
    if not has_animation:
        warnings.append(
            "animation: no CSS animation/transition or Web Animation API found — "
            "consider a micro-interaction that makes the tool feel alive"
        )

    # 2. Canvas or SVG — "it draws something"
    has_canvas_svg = bool(re.search(r'(?:<canvas|<svg)', text, re.IGNORECASE))
    if not has_canvas_svg:
        warnings.append(
            "canvas-svg: no <canvas> or <svg> found — "
            "consider a custom data visualization or diagram to differentiate"
        )

    # 3. Keyboard shortcuts — "power-user accessibility"
    has_keyboard = bool(re.search(
        r'(?:keydown|keyup|KeyboardEvent|hotkey|shortcut)',
        text,
        re.IGNORECASE
    ))
    if not has_keyboard:
        warnings.append(
            "keyboard-shortcuts: no keyboard event handling detected — "
            "a single memorable shortcut (e.g., Ctrl+Enter to submit) elevates a tool"
        )

    # 4. Real-time / reactive update — "it responds instantly"
    has_realtime = bool(re.search(
        r'(?:addEventListener\s*\(\s*["\']input["\']|'
        r'addEventListener\s*\(\s*["\']change["\']|'
        r'oninput\s*=|onchange\s*=|debounce|throttle)',
        text,
        re.IGNORECASE
    ))
    if not has_realtime:
        warnings.append(
            "realtime: no input/change event handler for live updates detected — "
            "consider live-as-you-type feedback instead of a submit-then-show flow"
        )

    # 5. Memorable hook — tagline or descriptor in visible copy
    top_section = text[:3000]
    has_hook = bool(re.search(
        r'(?:<title>[^<]{10,}|<h1[^>]*>[^<]{10,}|<p[^>]*>[^<]{20,})',
        top_section,
        re.IGNORECASE
    ))
    if not has_hook:
        warnings.append(
            "memorable-hook: no <title>, <h1>, or introductory <p> with descriptive text in first 3KB — "
            "a one-line memorable description helps users remember and share the tool"
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
    warnings = check_cult_status(path)
    for w in warnings:
        print(f"[WARN] {w}")
    if warnings:
        print(f"WARNINGS: {len(warnings)}")
    else:
        print("PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
sync_guides.py — embed flagship formatting guides into their apps' index.html.

Each flagship has:
  - A markdown guide file (FORMATTING_GUIDE.md or DECK_GUIDE.md)
  - An index.html with a sentinel block:
    <script type="text/plain" id="ai-prompt-content"><!-- GUIDE:START -->...<!-- GUIDE:END --></script>

This script reads the .md file and writes its content between the sentinels.
Run after editing either the .md file or the app. Safe to run repeatedly.

Usage: python3 sync_guides.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (app_dir, guide_filename)
FLAGSHIPS = [
    ("naval-scribe", "FORMATTING_GUIDE.md"),
    ("markdown-deck", "DECK_GUIDE.md"),
]

SENTINEL_START = "<!-- GUIDE:START -->"
SENTINEL_END = "<!-- GUIDE:END -->"


def ensure_embed_block(html: str) -> tuple[str, bool]:
    """Ensure an embed script block exists. Returns (html, was_added)."""
    if SENTINEL_START in html and SENTINEL_END in html:
        return html, False
    # Insert an empty block just before </body>
    block = (
        '\n<script type="text/plain" id="ai-prompt-content">'
        f'{SENTINEL_START}\n{SENTINEL_END}'
        '</script>\n'
    )
    # Insert before the LAST </body>, not the first — earlier ones may be inside
    # JS string literals used by export functions (e.g., exportStandaloneHTML).
    idx = html.rfind("</body>")
    if idx != -1:
        return html[:idx] + block + html[idx:], True
    # No </body> — append
    return html + block, True


def sync_one(app_dir: str, guide_filename: str) -> bool:
    app_path = ROOT / app_dir
    guide_path = app_path / guide_filename
    html_path = app_path / "index.html"

    if not guide_path.exists():
        print(f"SKIP {app_dir}: {guide_filename} not found")
        return False
    if not html_path.exists():
        print(f"SKIP {app_dir}: index.html not found")
        return False

    guide_content = guide_path.read_text().rstrip() + "\n"
    # Safety: the content must not contain the literal '</script>' or it would break embedding
    if "</script>" in guide_content:
        print(f"ERROR {app_dir}: guide contains literal '</script>' which would break embedding")
        return False

    html = html_path.read_text()
    html, added = ensure_embed_block(html)
    if added:
        print(f"  {app_dir}: added embed block")

    pattern = re.compile(
        re.escape(SENTINEL_START) + r".*?" + re.escape(SENTINEL_END),
        re.DOTALL,
    )
    new_block = f"{SENTINEL_START}\n{guide_content}{SENTINEL_END}"
    # Use a lambda for the replacement to avoid regex-escape interpretation of \1, \p, etc.
    new_html, n = pattern.subn(lambda m: new_block, html, count=1)
    if n == 0:
        print(f"ERROR {app_dir}: sentinel pattern not found after ensure")
        return False

    if new_html != html_path.read_text():
        html_path.write_text(new_html)
        guide_bytes = len(guide_content)
        print(f"  {app_dir}: synced {guide_bytes} bytes from {guide_filename}")
        return True
    else:
        print(f"  {app_dir}: already in sync")
        return False


def main() -> int:
    any_changed = False
    for app_dir, guide in FLAGSHIPS:
        if sync_one(app_dir, guide):
            any_changed = True
    return 0


if __name__ == "__main__":
    sys.exit(main())

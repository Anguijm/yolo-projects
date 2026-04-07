#!/usr/bin/env python3
"""
sync_project_ui.py — apply cross-portfolio UI upgrades to every non-flagship project.

Two changes per project:
  1. Readability bump — injects a style override at the end of <style> that:
     - Sets html base font-size to 17px (default browser is 16px)
     - Enforces minimum 14px on inputs/buttons/selects/textareas
     - Adds line-height: 1.55 on body for easier reading
     These are additive at the end so project-specific rules still win for
     intentional decorative text.

  2. Guide button — injects a fixed-position "Guide" button before </body>
     that opens <project>/README.md in a new tab. Non-invasive: fixed bottom-right
     with high z-index, does not modify existing layout.

Both injections are wrapped in sentinel comments so the script is idempotent
and future edits to the template are picked up automatically on re-run.

Skips:
  - Flagships (naval-scribe, markdown-deck) — they have their own AI Prompt button
  - Projects with no index.html
  - Projects with no README.md (can't link a Guide)

Usage: python3 sync_project_ui.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FLAGSHIPS = {"naval-scribe", "markdown-deck"}

# Sentinel markers so re-runs replace cleanly
STYLE_START = "/* UI-UPGRADE:START */"
STYLE_END = "/* UI-UPGRADE:END */"
GUIDE_START = "<!-- GUIDE-BTN:START -->"
GUIDE_END = "<!-- GUIDE-BTN:END -->"

STYLE_BLOCK = f"""{STYLE_START}
/* Injected by sync_project_ui.py — readability bump. Additive at end so
   project-specific rules still win for intentional decorative text. */
html {{ font-size: 17px; }}
body {{ line-height: 1.55; }}
input, button, select, textarea {{
  font-size: max(14px, 0.9rem);
  min-height: 32px;
}}
{STYLE_END}"""

GUIDE_BUTTON = f"""{GUIDE_START}
<a href="README.md" target="_blank" rel="noopener" id="ui-upgrade-guide-btn"
   title="How to use this tool"
   style="position:fixed;bottom:16px;right:16px;background:#1a1a1a;color:#e0e0e0;border:1px solid #444;border-radius:6px;padding:8px 14px;font-size:13px;text-decoration:none;font-family:system-ui,-apple-system,sans-serif;font-weight:500;z-index:99999;box-shadow:0 2px 8px rgba(0,0,0,0.4);transition:all 0.15s;"
   onmouseover="this.style.background='#2a2a2a';this.style.borderColor='#58a6ff';"
   onmouseout="this.style.background='#1a1a1a';this.style.borderColor='#444';"
>📖 Guide</a>
{GUIDE_END}"""


def is_project_dir(path: Path) -> bool:
    """A project dir has index.html and isn't a flagship or infra dir."""
    name = path.name
    if not path.is_dir():
        return False
    if name.startswith(".") or name.startswith("_"):
        return False
    if name in FLAGSHIPS:
        return False
    if name in {"council", "scripts", "experiments", "tmp", "tools", "node_modules", "cost-lens"}:
        return False
    if not (path / "index.html").exists():
        return False
    return True


def inject_style(html: str) -> tuple[str, bool]:
    """Inject or replace the readability-bump style block."""
    # Remove any existing injection first
    pattern = re.compile(
        re.escape(STYLE_START) + r".*?" + re.escape(STYLE_END),
        re.DOTALL,
    )
    had_existing = bool(pattern.search(html))
    html = pattern.sub(lambda m: "", html)

    # Find the LAST </style> tag (in case there are multiple) and inject before it
    last_style_close = html.rfind("</style>")
    if last_style_close == -1:
        # No <style> block found — this is unusual for our projects. Skip.
        return html, False

    before = html[:last_style_close]
    after = html[last_style_close:]
    new_html = before + "\n" + STYLE_BLOCK + "\n" + after
    return new_html, True


def inject_guide_button(html: str) -> tuple[str, bool]:
    """Inject or replace the Guide button before the last </body>."""
    pattern = re.compile(
        re.escape(GUIDE_START) + r".*?" + re.escape(GUIDE_END),
        re.DOTALL,
    )
    html = pattern.sub(lambda m: "", html)

    # Use the LAST </body> — some projects have </body> inside JS string literals
    idx = html.rfind("</body>")
    if idx == -1:
        return html, False

    new_html = html[:idx] + GUIDE_BUTTON + "\n" + html[idx:]
    return new_html, True


def sync_one(project_dir: Path, dry_run: bool = False) -> dict:
    result = {
        "project": project_dir.name,
        "skipped": False,
        "reason": None,
        "style_injected": False,
        "guide_injected": False,
    }

    html_path = project_dir / "index.html"
    readme_path = project_dir / "README.md"

    if not readme_path.exists():
        result["skipped"] = True
        result["reason"] = "no README.md"
        return result

    try:
        html = html_path.read_text()
    except Exception as e:
        result["skipped"] = True
        result["reason"] = f"read error: {e}"
        return result

    original = html
    html, style_ok = inject_style(html)
    html, guide_ok = inject_guide_button(html)

    if not style_ok:
        result["reason"] = "no <style> block"
    if not guide_ok:
        result["reason"] = (result["reason"] + "; " if result["reason"] else "") + "no </body>"

    if html != original and not dry_run:
        html_path.write_text(html)

    result["style_injected"] = style_ok
    result["guide_injected"] = guide_ok
    result["changed"] = html != original
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="Only apply to this one project (for testing)")
    args = ap.parse_args()

    projects = []
    if args.only:
        p = ROOT / args.only
        if is_project_dir(p):
            projects = [p]
        else:
            print(f"ERROR: {args.only} is not a valid project dir")
            return 2
    else:
        for entry in sorted(ROOT.iterdir()):
            if is_project_dir(entry):
                projects.append(entry)

    print(f"Found {len(projects)} project directories (flagships excluded)")
    if args.dry_run:
        print("DRY RUN — no changes will be written")
    print()

    stats = {"changed": 0, "skipped": 0, "no_style": 0, "no_body": 0, "no_readme": 0}
    for p in projects:
        r = sync_one(p, dry_run=args.dry_run)
        tag = ""
        if r["skipped"]:
            tag = f"SKIP ({r['reason']})"
            stats["skipped"] += 1
            if r["reason"] == "no README.md":
                stats["no_readme"] += 1
        elif r["changed"]:
            parts = []
            if r["style_injected"]:
                parts.append("style")
            if r["guide_injected"]:
                parts.append("guide")
            tag = "OK " + "+".join(parts)
            stats["changed"] += 1
            if not r["style_injected"]:
                stats["no_style"] += 1
            if not r["guide_injected"]:
                stats["no_body"] += 1
        else:
            tag = "(no change)"

        print(f"  {r['project']:35s} {tag}")

    print()
    print(f"Changed: {stats['changed']} | Skipped: {stats['skipped']} "
          f"(no-readme: {stats['no_readme']}) | No <style>: {stats['no_style']} "
          f"| No </body>: {stats['no_body']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Post-build verification for YOLO projects.

Independently verifies a build succeeded WITHOUT trusting the agent's claims.

Usage:
    python3 verify_build.py <project_name>
    python3 verify_build.py --last          # verify most recent build in yolo_log.json
"""

import json
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "yolo_log.json")
DASHBOARD_FILE = os.path.join(BASE_DIR, "dashboard.html")


def load_log():
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def get_last_project(log_data):
    if not log_data:
        return None
    return log_data[-1].get("project") or log_data[-1].get("folder")


def find_log_entry(log_data, project_name):
    """Find the most recent log entry for a project."""
    for entry in reversed(log_data):
        if entry.get("project") == project_name or entry.get("folder") == project_name:
            return entry
    return None


def check_dir_exists(project_dir):
    if os.path.isdir(project_dir):
        return True, "Project directory exists"
    return False, f"Project directory not found: {project_dir}"


def check_index_html(project_dir):
    index_path = os.path.join(project_dir, "index.html")
    if not os.path.isfile(index_path):
        return False, "index.html does not exist"
    size = os.path.getsize(index_path)
    if size <= 100:
        return False, f"index.html too small ({size} bytes, need >100)"
    return True, f"index.html exists ({size} bytes)"


def check_html_structure(project_dir):
    index_path = os.path.join(project_dir, "index.html")
    if not os.path.isfile(index_path):
        return False, "index.html missing (cannot check HTML structure)"
    with open(index_path, "r", errors="replace") as f:
        content = f.read().lower()
    missing = []
    for tag in ["<html", "<head", "<body"]:
        if tag not in content:
            missing.append(tag)
    if missing:
        return False, f"index.html missing required tags: {', '.join(missing)}"
    return True, "index.html has valid HTML structure (<html>, <head>, <body>)"


def check_js_syntax(project_dir):
    index_path = os.path.join(project_dir, "index.html")
    if not os.path.isfile(index_path):
        return False, "index.html missing (cannot check JS)"
    with open(index_path, "r", errors="replace") as f:
        content = f.read()

    # Extract all inline <script> blocks (not external src references)
    pattern = re.compile(
        r"<script(?:\s[^>]*)?>(.+?)</script>",
        re.DOTALL | re.IGNORECASE,
    )
    blocks = []
    for m in pattern.finditer(content):
        tag_attrs = content[m.start(): content.index(">", m.start()) + 1]
        if "src=" in tag_attrs.lower():
            continue
        blocks.append(m.group(1))

    if not blocks:
        return True, "No inline JS found (nothing to check)"

    combined = "\n;\n".join(blocks)
    try:
        result = subprocess.run(
            ["node", "-c"],
            input=combined,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, f"JS syntax valid ({len(blocks)} inline block(s))"
        # Grab first line of error
        err = (result.stderr or result.stdout).strip().split("\n")[0]
        return False, f"JS syntax error: {err}"
    except FileNotFoundError:
        return None, "node not found — skipping JS syntax check"
    except subprocess.TimeoutExpired:
        return False, "JS syntax check timed out"


def check_log_entry(log_data, project_name):
    entry = find_log_entry(log_data, project_name)
    if entry is None:
        return False, f"Project '{project_name}' not found in yolo_log.json"
    status = entry.get("status", "unknown")
    if status == "working":
        return True, f"Log entry found with status 'working'"
    return False, f"Log entry status is '{status}' (expected 'working')"


def check_readme(project_dir):
    readme = os.path.join(project_dir, "README.md")
    if os.path.isfile(readme):
        return True, "README.md exists"
    return False, "README.md not found"


def check_dashboard_updated(log_data, project_name):
    if not os.path.isfile(DASHBOARD_FILE):
        return False, "dashboard.html does not exist"

    entry = find_log_entry(log_data, project_name)
    if entry is None:
        return False, "No log entry to compare dashboard time against"

    entry_date = entry.get("date")
    if not entry_date:
        return False, "Log entry has no date field"

    dashboard_mtime = os.path.getmtime(DASHBOARD_FILE)
    log_mtime = os.path.getmtime(LOG_FILE)

    # Dashboard should have been updated at or after the log was written
    if dashboard_mtime >= log_mtime:
        return True, "dashboard.html mtime >= yolo_log.json mtime"
    return False, (
        f"dashboard.html is stale (modified before yolo_log.json was last written)"
    )


def verify(project_name):
    log_data = load_log()
    project_dir = os.path.join(BASE_DIR, project_name)

    checks = [
        ("1. Directory exists", lambda: check_dir_exists(project_dir)),
        ("2. index.html exists (>100 bytes)", lambda: check_index_html(project_dir)),
        ("3. Valid HTML structure", lambda: check_html_structure(project_dir)),
        ("4. JS syntax valid", lambda: check_js_syntax(project_dir)),
        ("5. Log entry status 'working'", lambda: check_log_entry(log_data, project_name)),
        ("6. README.md exists", lambda: check_readme(project_dir)),
        ("7. Dashboard updated", lambda: check_dashboard_updated(log_data, project_name)),
    ]

    results = []
    for label, fn in checks:
        passed, msg = fn()
        results.append((label, passed, msg))

    # Print results
    print(f"\n{'='*60}")
    print(f"  VERIFY BUILD: {project_name}")
    print(f"{'='*60}\n")

    failures = []
    for label, passed, msg in results:
        if passed is True:
            icon = "PASS"
        elif passed is None:
            icon = "SKIP"
        else:
            icon = "FAIL"
            failures.append(label)
        print(f"  [{icon}] {label}")
        print(f"         {msg}\n")

    print(f"{'='*60}")
    if failures:
        print(f"  RESULT: FAIL  ({len(failures)} check(s) failed)")
        for f in failures:
            print(f"    - {f}")
        print(f"{'='*60}\n")
        return 1
    else:
        print(f"  RESULT: PASS  (all checks passed)")
        print(f"{'='*60}\n")
        return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_build.py <project_name>")
        print("       python3 verify_build.py --last")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--last":
        try:
            log_data = load_log()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"FAIL: Cannot read yolo_log.json: {e}")
            sys.exit(1)
        project_name = get_last_project(log_data)
        if not project_name:
            print("FAIL: No projects found in yolo_log.json")
            sys.exit(1)
        print(f"(--last resolved to: {project_name})")
    else:
        project_name = arg

    sys.exit(verify(project_name))


if __name__ == "__main__":
    main()

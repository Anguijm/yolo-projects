#!/usr/bin/env python3
"""Test suite for YOLO projects.

Runs static analysis AND headless browser tests on single-file HTML projects.
Usage:
  python3 test_project.py <project-name>     # Test one project
  python3 test_project.py --all              # Test all projects
"""

import sys
import os
import re
import json
import subprocess
import time
import http.server
import threading
from pathlib import Path

ROOT = Path(__file__).parent
VENV_PYTHON = ROOT / ".test-venv" / "bin" / "python3"

# ============ STATIC ANALYSIS ============

def extract_js(html: str) -> str:
    """Extract JS from <script> tags."""
    match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
    return match.group(1) if match else ""

def extract_html_ids(html: str) -> set:
    """Extract all id="..." from HTML."""
    return set(re.findall(r'id=["\']([^"\']+)["\']', html))

def extract_js_id_refs(js: str) -> set:
    """Extract all getElementById('...') references from JS."""
    return set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js))

def check_syntax(js: str) -> tuple[bool, str]:
    """Run node -c on JS."""
    tmp = Path("/tmp/_yolo_check.js")
    tmp.write_text(js)
    r = subprocess.run(["node", "-c", str(tmp)], capture_output=True, text=True)
    return r.returncode == 0, r.stderr.strip()

def check_id_consistency(html: str, js: str) -> list[str]:
    """Check that all JS getElementById references exist in HTML."""
    html_ids = extract_html_ids(html)
    js_refs = extract_js_id_refs(js)
    missing = js_refs - html_ids
    return sorted(missing)

def check_brace_balance(js: str) -> bool:
    """Check balanced braces/parens/brackets (rough check, ignores strings)."""
    # Strip strings and comments first (simplified)
    cleaned = re.sub(r'//.*?$', '', js, flags=re.MULTILINE)
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"'(?:[^'\\]|\\.)*'", '', cleaned)
    cleaned = re.sub(r'"(?:[^"\\]|\\.)*"', '', cleaned)
    cleaned = re.sub(r'`(?:[^`\\]|\\.)*`', '', cleaned)

    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in cleaned:
        if ch in '({[':
            stack.append(ch)
        elif ch in ')}]':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0

def check_event_listeners(html: str, js: str) -> list[str]:
    """Check that addEventListener targets exist."""
    # Find patterns like getElementById('x').addEventListener
    refs = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)\s*\.\s*addEventListener", js)
    html_ids = extract_html_ids(html)
    missing = [r for r in refs if r not in html_ids]
    return missing

def check_start_screen(html: str, js: str) -> dict:
    """Check if there's an overlay/start screen and if dismiss logic exists."""
    has_overlay = bool(re.search(r'overlay|start-screen|start_screen', html, re.I))
    if not has_overlay:
        return {"has_overlay": False, "ok": True}

    # Check for dismiss logic
    has_dismiss = bool(re.search(
        r"display\s*=\s*['\"]none|classList\.remove\(['\"]show|classList\.add\(['\"]hidden|style\.display\s*=",
        js
    ))
    return {"has_overlay": True, "has_dismiss": has_dismiss, "ok": has_dismiss}


# ============ BROWSER TESTS (Playwright) ============

def run_browser_tests(project_dir: Path, html_file: str) -> dict:
    """Run headless browser tests using Playwright."""
    results = {"console_errors": [], "page_loaded": False, "no_crash": True}

    # Start a local server
    os.chdir(project_dir)
    handler = http.server.SimpleHTTPRequestHandler
    # Suppress logs
    handler.log_message = lambda *args: None
    port = 18900 + hash(str(project_dir)) % 100
    try:
        httpd = http.server.HTTPServer(("127.0.0.1", port), handler)
    except OSError:
        port += 1
        httpd = http.server.HTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    # Run playwright test in subprocess using venv python
    test_script = f'''
import sys
from playwright.sync_api import sync_playwright

errors = []
def on_console(msg):
    if msg.type == "error":
        errors.append(msg.text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("console", on_console)
    page.on("pageerror", lambda exc: errors.append(str(exc)))

    try:
        page.goto("http://127.0.0.1:{port}/{html_file}", timeout=10000)
        page.wait_for_timeout(2000)  # Let JS initialize

        # Check if page has content
        body_text = page.inner_text("body")
        has_content = len(body_text.strip()) > 0

        # Try clicking start/play buttons if they exist
        for selector in ["#btn-start", "#btn-go", "#ov-btn", "#btn-play", "button"]:
            try:
                el = page.query_selector(selector)
                if el and el.is_visible():
                    el.click()
                    page.wait_for_timeout(500)
                    break
            except:
                pass

        # Check for overlay still visible after click
        overlay_visible = False
        for sel in ["#overlay", "#start-overlay", "#start-screen", "#help-overlay"]:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    overlay_visible = True
            except:
                pass

        import json
        print(json.dumps({{
            "page_loaded": has_content,
            "no_crash": True,
            "console_errors": errors[:5],
            "overlay_stuck": overlay_visible
        }}))
    except Exception as e:
        print(json.dumps({{
            "page_loaded": False,
            "no_crash": False,
            "console_errors": [str(e)],
            "overlay_stuck": False
        }}))
    finally:
        browser.close()
'''

    try:
        r = subprocess.run(
            [str(VENV_PYTHON), "-c", test_script],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0 and r.stdout.strip():
            results = json.loads(r.stdout.strip())
        else:
            results["console_errors"] = [r.stderr[:200] if r.stderr else "Unknown error"]
            results["no_crash"] = False
    except subprocess.TimeoutExpired:
        results["console_errors"] = ["Browser test timed out"]
        results["no_crash"] = False
    except Exception as e:
        results["console_errors"] = [str(e)]
        results["no_crash"] = False
    finally:
        httpd.shutdown()
        os.chdir(ROOT)

    return results


# ============ MAIN TEST RUNNER ============

def test_project(name: str) -> dict:
    """Run all tests on a project. Returns results dict."""
    project_dir = ROOT / name
    results = {
        "project": name,
        "passed": True,
        "checks": {}
    }

    # Find HTML file
    html_file = None
    for f in ["index.html"]:
        if (project_dir / f).exists():
            html_file = f
            break

    if not html_file:
        # Check for other HTML files
        html_files = list(project_dir.glob("*.html"))
        if html_files:
            html_file = html_files[0].name

    if not html_file:
        results["checks"]["file_exists"] = {"passed": False, "detail": "No HTML file found"}
        results["passed"] = False
        return results

    results["checks"]["file_exists"] = {"passed": True, "detail": html_file}

    html = (project_dir / html_file).read_text()
    js = extract_js(html)

    if not js:
        results["checks"]["has_js"] = {"passed": False, "detail": "No <script> block found"}
        results["passed"] = False
        return results

    # 1. Syntax check
    ok, err = check_syntax(js)
    results["checks"]["syntax"] = {"passed": ok, "detail": err if not ok else "OK"}
    if not ok:
        results["passed"] = False

    # 2. ID consistency
    missing = check_id_consistency(html, js)
    results["checks"]["id_consistency"] = {
        "passed": len(missing) == 0,
        "detail": f"Missing IDs: {missing}" if missing else "OK"
    }
    if missing:
        results["passed"] = False

    # 3. Event listener targets
    missing_listeners = check_event_listeners(html, js)
    results["checks"]["event_listeners"] = {
        "passed": len(missing_listeners) == 0,
        "detail": f"Missing: {missing_listeners}" if missing_listeners else "OK"
    }
    if missing_listeners:
        results["passed"] = False

    # 4. Brace balance
    balanced = check_brace_balance(js)
    results["checks"]["brace_balance"] = {"passed": balanced, "detail": "OK" if balanced else "Unbalanced"}
    if not balanced:
        results["passed"] = False

    # 5. Start screen check
    ss = check_start_screen(html, js)
    if ss["has_overlay"]:
        results["checks"]["start_screen"] = {
            "passed": ss["ok"],
            "detail": "OK" if ss["ok"] else "Overlay exists but no dismiss logic found"
        }
        if not ss["ok"]:
            results["passed"] = False

    # 6. Browser test (if playwright available)
    if VENV_PYTHON.exists():
        browser_results = run_browser_tests(project_dir, html_file)
        results["checks"]["browser_loads"] = {
            "passed": browser_results.get("page_loaded", False),
            "detail": "OK" if browser_results.get("page_loaded") else "Page did not load"
        }
        if browser_results.get("console_errors"):
            results["checks"]["console_errors"] = {
                "passed": False,
                "detail": browser_results["console_errors"][:3]
            }
            results["passed"] = False
        else:
            results["checks"]["console_errors"] = {"passed": True, "detail": "No errors"}

        if browser_results.get("overlay_stuck"):
            results["checks"]["overlay_dismisses"] = {
                "passed": False,
                "detail": "Overlay still visible after clicking start button"
            }
            results["passed"] = False
        elif ss.get("has_overlay"):
            results["checks"]["overlay_dismisses"] = {"passed": True, "detail": "OK"}

    return results


def print_results(results: dict):
    """Pretty print test results."""
    status = "PASS" if results["passed"] else "FAIL"
    icon = "✓" if results["passed"] else "✗"
    print(f"\n{'='*50}")
    print(f"{icon} {results['project']}: {status}")
    print(f"{'='*50}")
    for check, data in results["checks"].items():
        icon = "✓" if data["passed"] else "✗"
        print(f"  {icon} {check}: {data['detail']}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_project.py <project-name> | --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        all_results = []
        for d in sorted(os.listdir(ROOT)):
            if (ROOT / d).is_dir() and (ROOT / d / "index.html").exists():
                results = test_project(d)
                print_results(results)
                all_results.append(results)
            # Also check for other HTML files
            elif (ROOT / d).is_dir() and any((ROOT / d).glob("*.html")):
                results = test_project(d)
                print_results(results)
                all_results.append(results)

        passed = sum(1 for r in all_results if r["passed"])
        total = len(all_results)
        print(f"\n{'='*50}")
        print(f"TOTAL: {passed}/{total} passed")
        print(f"{'='*50}")
    else:
        results = test_project(sys.argv[1])
        print_results(results)
        sys.exit(0 if results["passed"] else 1)

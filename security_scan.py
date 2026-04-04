#!/usr/bin/env python3
"""
security_scan.py — Security Scanner for YOLO Build Pipeline

Scans a YOLO project's index.html for common security issues in inline JS/HTML.
Regex-based, zero external dependencies.

Usage:
    python3 security_scan.py <project-name>
    python3 security_scan.py --all
    python3 security_scan.py --all --json
    python3 security_scan.py <project-name> --json

Exit code 0 if no CRITICAL/HIGH findings, 1 if any CRITICAL/HIGH found.
"""

import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = SCRIPT_DIR

# ── Severity levels ──────────────────────────────────────────────────────────

CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

SEVERITY_ORDER = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}

# ── Security rules ───────────────────────────────────────────────────────────
# Each rule: (id, severity, description, regex, target, remediation)
#   target: "js" = inline JS only, "html" = full HTML, "both" = both

RULES = [
    # ── Secrets detection ────────────────────────────────────────────────
    {
        "id": "SEC-001",
        "severity": CRITICAL,
        "category": "Secrets",
        "description": "Hardcoded API key or token",
        "regex": r"""(?:api[_-]?key|api[_-]?secret|auth[_-]?token|access[_-]?token|secret[_-]?key|private[_-]?key)\s*[:=]\s*['"][A-Za-z0-9_\-/.]{8,}['"]""",
        "target": "js",
        "remediation": "Move secrets to a backend service or environment variable. Never ship API keys in client-side code.",
    },
    {
        "id": "SEC-002",
        "severity": CRITICAL,
        "category": "Secrets",
        "description": "AWS-style key pattern (AKIA...)",
        "regex": r"""['"]AKIA[0-9A-Z]{16}['"]""",
        "target": "js",
        "remediation": "Rotate this AWS access key immediately and remove from source.",
    },
    {
        "id": "SEC-003",
        "severity": CRITICAL,
        "category": "Secrets",
        "description": "Hardcoded password",
        "regex": r"""(?:password|passwd|pwd)\s*[:=]\s*['"][^'"]{8,}['"]""",
        "target": "js",
        "remediation": "Never hardcode passwords. Use server-side authentication flows.",
    },
    {
        "id": "SEC-004",
        "severity": HIGH,
        "category": "Secrets",
        "description": "Bearer token in source",
        "regex": r"""['"]Bearer\s+[A-Za-z0-9_\-/.+=]{10,}['"]""",
        "target": "js",
        "remediation": "Bearer tokens must be fetched at runtime, not embedded in source.",
    },
    {
        "id": "SEC-005",
        "severity": HIGH,
        "category": "Secrets",
        "description": "GitHub/GitLab token pattern",
        "regex": r"""['"](?:gh[ps]_[A-Za-z0-9_]{36,}|glpat-[A-Za-z0-9_\-]{20,})['"]""",
        "target": "js",
        "remediation": "Rotate this token immediately. Use backend proxy for API calls.",
    },

    # ── XSS vectors ──────────────────────────────────────────────────────
    {
        "id": "XSS-001",
        "severity": HIGH,
        "category": "XSS",
        "description": "innerHTML assignment with dynamic content",
        "regex": r"""\.innerHTML\s*[+]?=\s*(?:[^'"`;\n]*(?:\+|`\$\{))""",
        "target": "js",
        "remediation": "Use textContent for text, or sanitize with DOMPurify before innerHTML.",
    },
    {
        "id": "XSS-002",
        "severity": HIGH,
        "category": "XSS",
        "description": "document.write() usage",
        "regex": r"""document\.write\s*\(""",
        "target": "js",
        "remediation": "Replace document.write with DOM manipulation (createElement/appendChild).",
    },
    {
        "id": "XSS-003",
        "severity": CRITICAL,
        "category": "XSS",
        "description": "eval() with dynamic content",
        "regex": r"""(?<![.\w])eval\s*\(""",
        "strip_strings": True,
        "case_insensitive": False,
        "target": "js",
        "remediation": "Replace eval() with JSON.parse(), Function() with known input, or a proper parser.",
    },
    {
        "id": "XSS-004",
        "severity": HIGH,
        "category": "XSS",
        "description": "Function() constructor (eval equivalent)",
        "regex": r"""(?:new\s+Function|(?<![a-z])Function)\s*\(\s*(?:[a-zA-Z_$]\w*(?:\s*\+|\s*,\s*[a-zA-Z_$]))""",
        "case_insensitive": False,
        "target": "js",
        "remediation": "Avoid Function() constructor with dynamic input. Use a safe parser instead.",
    },
    {
        "id": "XSS-005",
        "severity": MEDIUM,
        "category": "XSS",
        "description": "innerHTML with template literal",
        "regex": r"""\.innerHTML\s*[+]?=\s*`[^`]*\$\{""",
        "target": "js",
        "remediation": "Template literals in innerHTML can inject HTML. Sanitize variables or use textContent.",
    },

    # ── Injection risks ──────────────────────────────────────────────────
    {
        "id": "INJ-001",
        "severity": HIGH,
        "category": "Injection",
        "description": "URL params used in DOM without sanitization",
        "regex": r"""(?:URLSearchParams|location\.search|location\.href|location\.hash)[\s\S]{0,80}(?:innerHTML|document\.write|\.src\s*=|\.href\s*=)""",
        "target": "js",
        "remediation": "Validate and sanitize all URL parameters before DOM insertion. Use textContent or allowlists.",
    },
    {
        "id": "INJ-002",
        "severity": MEDIUM,
        "category": "Injection",
        "description": "location.hash used without validation",
        "regex": r"""location\.hash(?!\.replace)""",
        "target": "js",
        "remediation": "Validate location.hash against an allowlist before using it.",
    },
    {
        "id": "INJ-003",
        "severity": MEDIUM,
        "category": "Injection",
        "description": "Unsanitized URL parameter extraction",
        "regex": r"""(?:new\s+URLSearchParams|location\.search)[\s\S]{0,40}\.get\s*\(""",
        "target": "js",
        "remediation": "Sanitize URL parameter values before use. Apply input validation.",
    },

    # ── Insecure practices ───────────────────────────────────────────────
    {
        "id": "PRC-001",
        "severity": MEDIUM,
        "category": "Insecure Practice",
        "description": "HTTP URL (not HTTPS)",
        "regex": r"""['"]http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)[^'"]+['"]""",
        "target": "both",
        "remediation": "Use https:// for all external URLs to prevent MITM attacks.",
    },
    {
        "id": "PRC-002",
        "severity": LOW,
        "category": "Insecure Practice",
        "description": "Missing Content-Security-Policy meta tag",
        "regex": r"""__CHECK_MISSING_CSP__""",
        "target": "special_csp",
        "remediation": "Add <meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; ...\">.",
    },
    {
        "id": "PRC-003",
        "severity": MEDIUM,
        "category": "Insecure Practice",
        "description": "postMessage without origin check",
        "regex": r"""addEventListener\s*\(\s*['"]message['"][\s\S]{0,200}(?!origin)""",
        "target": "js",
        "remediation": "Always verify event.origin in message event handlers.",
    },

    # ── Dependency issues ────────────────────────────────────────────────
    {
        "id": "DEP-001",
        "severity": MEDIUM,
        "category": "Dependencies",
        "description": "External script tag (CDN dependency)",
        "regex": r"""<script[^>]+src\s*=\s*['"]https?://[^'"]+['"]""",
        "target": "html",
        "remediation": "Pin CDN dependencies with integrity (SRI) hashes, or vendor them locally.",
    },
    {
        "id": "DEP-002",
        "severity": HIGH,
        "category": "Dependencies",
        "description": "External script without SRI integrity attribute",
        "regex": r"""<script[^>]+src\s*=\s*['"]https?://[^'"]+['"](?![^>]*integrity\s*=)""",
        "target": "html",
        "remediation": "Add integrity=\"sha384-...\" and crossorigin=\"anonymous\" to external script tags.",
    },
    {
        "id": "DEP-003",
        "severity": MEDIUM,
        "category": "Dependencies",
        "description": "External stylesheet (CDN dependency)",
        "regex": r"""<link[^>]+href\s*=\s*['"]https?://[^'"]+['"][^>]*rel\s*=\s*['"]stylesheet['"]""",
        "target": "html",
        "remediation": "Pin CDN stylesheets with integrity (SRI) hashes, or vendor them locally.",
    },

    # ── Data exposure ────────────────────────────────────────────────────
    {
        "id": "DAT-001",
        "severity": MEDIUM,
        "category": "Data Exposure",
        "description": "localStorage with sensitive-looking key",
        "regex": r"""localStorage\.(?:setItem|getItem)\s*\(\s*['"](?:.*(?:token|password|secret|key|auth|session|credential|api[_-]?key).*?)['"]""",
        "target": "js",
        "remediation": "Avoid storing secrets in localStorage (accessible to XSS). Use httpOnly cookies or sessionStorage.",
    },
    {
        "id": "DAT-002",
        "severity": LOW,
        "category": "Data Exposure",
        "description": "console.log with potentially sensitive data",
        "regex": r"""console\.log\s*\([^)]*(?:token|password|secret|key|auth|credential|user)[^)]*\)""",
        "target": "js",
        "remediation": "Remove console.log statements that may leak sensitive data in production.",
    },
    {
        "id": "DAT-003",
        "severity": LOW,
        "category": "Data Exposure",
        "description": "Sensitive data in data attributes",
        "regex": r"""data-(?:token|key|secret|password|auth)\s*=\s*['"][^'"]+['"]""",
        "target": "html",
        "remediation": "Do not store secrets in HTML data attributes. They are visible in the DOM.",
    },
]


# ── Scanner ──────────────────────────────────────────────────────────────────


def extract_js_from_html(html_path):
    """Extract inline JavaScript from an HTML file. Returns (js_code, full_html, line_offsets).

    line_offsets maps each JS chunk to its starting line in the original HTML.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    js_parts = []
    line_offsets = []

    script_tag_re = re.compile(
        r"<script([^>]*)>([\s\S]*?)</script>", re.IGNORECASE
    )
    for m in script_tag_re.finditer(content):
        attrs, body = m.group(1), m.group(2)
        if "src=" in attrs.lower():
            continue
        if body.strip():
            # Line number of the <script> tag in the original HTML
            start_line = content[: m.start(2)].count("\n") + 1
            js_parts.append(body)
            line_offsets.append(start_line)

    return js_parts, content, line_offsets


def get_html_line(content, char_offset):
    """Get 1-based line number for a character offset in the full HTML."""
    return content[:char_offset].count("\n") + 1


def run_rule(rule, js_parts, line_offsets, full_html):
    """Run a single security rule. Returns list of findings."""
    findings = []

    # Special check: missing CSP
    if rule["target"] == "special_csp":
        if not re.search(
            r"""<meta[^>]+http-equiv\s*=\s*['"]Content-Security-Policy['"]""",
            full_html,
            re.IGNORECASE,
        ):
            findings.append(
                {
                    "line": 1,
                    "source": "HTML",
                    "matched": "(no CSP meta tag found)",
                }
            )
        return findings

    try:
        flags = re.MULTILINE
        if rule.get("case_insensitive", True):
            flags |= re.IGNORECASE
        compiled = re.compile(rule["regex"], flags)
    except re.error as e:
        findings.append({"line": 0, "source": "ERROR", "matched": f"Bad regex: {e}"})
        return findings

    targets = []
    if rule["target"] in ("js", "both"):
        for i, js_chunk in enumerate(js_parts):
            targets.append(("JS", js_chunk, line_offsets[i] if i < len(line_offsets) else 1))
    if rule["target"] in ("html", "both"):
        targets.append(("HTML", full_html, 1))

    for source_label, code, base_line in targets:
        scan_code = code
        if rule.get("strip_strings"):
            scan_code = re.sub(r"""'(?:[^'\\]|\\.)*'""", "''", scan_code)
            scan_code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', scan_code)
            scan_code = re.sub(r'`(?:[^`\\]|\\.)*`', '``', scan_code)
        for m in compiled.finditer(scan_code):
            line_in_chunk = code[: m.start()].count("\n")
            abs_line = base_line + line_in_chunk
            matched_text = m.group(0)
            if len(matched_text) > 120:
                matched_text = matched_text[:120] + "..."
            matched_text = matched_text.replace("\n", "\\n")
            findings.append(
                {
                    "line": abs_line,
                    "source": source_label,
                    "matched": matched_text,
                }
            )

    return findings


def scan_project(project_name, verbose=True):
    """Scan a single project. Returns (findings_list, has_critical_high)."""
    html_path = PROJECTS_DIR / project_name / "index.html"

    if not html_path.exists():
        if verbose:
            print(f"  SKIP: {html_path} not found")
        return [], False

    js_parts, full_html, line_offsets = extract_js_from_html(html_path)

    all_findings = []

    for rule in RULES:
        matches = run_rule(rule, js_parts, line_offsets, full_html)
        if matches:
            for match in matches:
                all_findings.append(
                    {
                        "rule_id": rule["id"],
                        "severity": rule["severity"],
                        "category": rule["category"],
                        "description": rule["description"],
                        "remediation": rule["remediation"],
                        "line": match["line"],
                        "source": match["source"],
                        "matched": match["matched"],
                    }
                )

    # Sort by severity then line number
    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f["severity"], 99), f["line"]))

    has_critical_high = any(
        f["severity"] in (CRITICAL, HIGH) for f in all_findings
    )

    return all_findings, has_critical_high


# ── Output ───────────────────────────────────────────────────────────────────

SEVERITY_COLORS = {
    CRITICAL: "\033[91m",  # red
    HIGH: "\033[93m",      # yellow
    MEDIUM: "\033[33m",    # orange-ish
    LOW: "\033[36m",       # cyan
}
RESET = "\033[0m"


def severity_badge(sev):
    """Colored severity badge for terminal output."""
    color = SEVERITY_COLORS.get(sev, "")
    return f"{color}[{sev}]{RESET}"


def print_findings(project_name, findings):
    """Print human-readable findings for a project."""
    if not findings:
        print(f"  {project_name}: CLEAN")
        return

    crits = sum(1 for f in findings if f["severity"] == CRITICAL)
    highs = sum(1 for f in findings if f["severity"] == HIGH)
    meds = sum(1 for f in findings if f["severity"] == MEDIUM)
    lows = sum(1 for f in findings if f["severity"] == LOW)

    parts = []
    if crits:
        parts.append(f"{crits} CRITICAL")
    if highs:
        parts.append(f"{highs} HIGH")
    if meds:
        parts.append(f"{meds} MEDIUM")
    if lows:
        parts.append(f"{lows} LOW")

    print(f"\n  {project_name}: {len(findings)} finding(s) — {', '.join(parts)}")
    print(f"  {'─' * 60}")

    for f in findings:
        badge = severity_badge(f["severity"])
        print(f"    {badge} {f['rule_id']} L{f['line']} ({f['source']}): {f['description']}")
        print(f"      Match: {f['matched'][:90]}")
        print(f"      Fix:   {f['remediation']}")
        print()


def print_summary_line(project_name, findings):
    """Print one-line summary for --all mode."""
    if not findings:
        print(f"  {project_name}: CLEAN")
        return

    sev_counts = {}
    for f in findings:
        sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1

    parts = []
    for sev in (CRITICAL, HIGH, MEDIUM, LOW):
        if sev in sev_counts:
            parts.append(f"{sev_counts[sev]} {sev}")

    print(f"  {project_name}: {len(findings)} finding(s) — {', '.join(parts)}")


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 security_scan.py <project-name>")
        print("       python3 security_scan.py --all")
        print("       python3 security_scan.py --all --json")
        sys.exit(2)

    json_output = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    print(f"Security Scanner — {len(RULES)} rules loaded\n")

    if args[0] == "--all":
        projects = sorted(
            d.name
            for d in PROJECTS_DIR.iterdir()
            if d.is_dir()
            and not d.name.startswith(".")
            and not d.name.startswith("__")
            and (d / "index.html").exists()
        )
        print(f"Scanning {len(projects)} projects...\n")

        all_results = {}
        total_findings = 0
        flagged_projects = 0
        any_critical_high = False

        for project in projects:
            findings, has_ch = scan_project(project, verbose=False)
            if findings:
                total_findings += len(findings)
                flagged_projects += 1
                all_results[project] = findings
                if has_ch:
                    any_critical_high = True
            if not json_output:
                print_summary_line(project, findings)

        print(f"\n{'=' * 60}")
        print(f"TOTAL: {total_findings} findings across {flagged_projects}/{len(projects)} projects")

        # Count by severity
        sev_totals = {}
        for proj_findings in all_results.values():
            for f in proj_findings:
                sev_totals[f["severity"]] = sev_totals.get(f["severity"], 0) + 1
        for sev in (CRITICAL, HIGH, MEDIUM, LOW):
            if sev in sev_totals:
                print(f"  {sev}: {sev_totals[sev]}")

        if json_output:
            print("\n" + json.dumps(all_results, indent=2))

        sys.exit(1 if any_critical_high else 0)

    else:
        project_name = args[0]
        findings, has_critical_high = scan_project(project_name)

        if not json_output:
            print_findings(project_name, findings)
        else:
            output = {
                "project": project_name,
                "findings": findings,
                "total": len(findings),
                "has_critical_or_high": has_critical_high,
            }
            print(json.dumps(output, indent=2))

        sys.exit(1 if has_critical_high else 0)


if __name__ == "__main__":
    main()

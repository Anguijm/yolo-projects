#!/usr/bin/env python3
"""Advisory AI-code-antipattern lens for YOLO single-file HTML builds.

Scans the embedded JS/markup of a single-file HTML tool for documented
AI-generated-code failure modes: hallucinated (unbundled) imports, unused
imports, orphan TODO/FIXME markers, dead-code functions, and plan drift.

Usage:
  python3 ai_antipatterns.py <project>/index.html
  python3 ai_antipatterns.py --help

Exit 0 always (advisory mode). Prints [WARN] lines then PASS or WARNINGS: N.
Exit 1 only if the file cannot be read or is not valid HTML.

Runs advisory alongside ux_completeness.py, mobile_usability.py, and
cult_status.py — same contract, fourth lens.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))

HELP = """ai_antipatterns.py — Advisory AI-code-antipattern lens for YOLO HTML builds.

Usage:
  python3 ai_antipatterns.py <path/to/index.html>

Checks (all advisory — never blocks the build):
  hallucinated-imports  Bare-specifier import/require with no bundler or importmap
  unused-imports        Imported binding referenced only at its import site
  orphan-TODO           TODO/FIXME/XXX/HACK markers left in shipped code
  deadcode-function     Named function defined but never referenced
  mismatched-plan       Built tool's visible copy drifts from sibling plan.md

Output:
  [WARN] <check>: <description>   — one line per issue found
  PASS                            — no issues found
  WARNINGS: N                     — N issues found

Notes:
  - hallucinated-imports is suppressed when <script type="importmap"> is present.
  - Code-reference checks run against a comment/string-stripped copy of the
    source to avoid counting matches inside comments or string literals.
  - mismatched-plan is silently skipped when no sibling plan.md exists.

Exit codes: 0 (always, advisory mode), 1 (file not found or not valid HTML).
"""

# Function names that are legitimately invoked externally (entry points,
# framework hooks) and should not be flagged as dead code.
_ENTRYPOINT_NAMES = {"main", "init", "setup", "start", "run", "render", "app"}

_STOPWORDS = {
    "this", "that", "with", "from", "into", "your", "have", "will", "when",
    "what", "which", "they", "them", "then", "than", "tool", "page", "html",
    "user", "text", "data", "file", "build", "plan", "goal", "scope",
    "using", "uses", "used", "able", "also", "each", "more", "most", "some",
}


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


def _strip_comments_and_strings(text):
    """Return a copy of text with HTML/JS comments and string literals blanked.

    Replaces each comment or string with same-length whitespace so that
    identifier-reference counting in the code checks ignores matches that
    occur only inside comments or strings. Regexes are deliberately linear
    (no nested quantifiers) to avoid catastrophic backtracking / ReDoS.
    """
    def blank(m):
        # Preserve newlines so line-based context is roughly intact.
        return re.sub(r"[^\n]", " ", m.group(0))

    # Order matters: comments first, then strings.
    patterns = [
        r"<!--.*?-->",        # HTML comments
        r"/\*.*?\*/",         # JS block comments
        r"//[^\n]*",          # JS line comments
        r"'(?:\\.|[^'\\\n])*'",   # single-quoted strings
        r'"(?:\\.|[^"\\\n])*"',   # double-quoted strings
        r"`(?:\\.|[^`\\])*`",      # template literals
    ]
    out = text
    for pat in patterns:
        out = re.sub(pat, blank, out, flags=re.DOTALL)
    return out


def _comment_regions(text):
    """Return concatenated text of all HTML/JS comment regions."""
    parts = []
    for pat in (r"<!--.*?-->", r"/\*.*?\*/", r"//[^\n]*"):
        parts.extend(re.findall(pat, text, flags=re.DOTALL))
    return "\n".join(parts)


def _keywords(text):
    """Lowercase alphanumeric tokens >=4 chars, minus stopwords; as a set."""
    toks = re.findall(r"[a-zA-Z][a-zA-Z0-9]{3,}", text.lower())
    return {t for t in toks if t not in _STOPWORDS}


def check_ai_antipatterns(path):
    """Run all AI-antipattern checks on path; return list of warning strings."""
    text = read_html(path)
    # Code checks operate only on <script> contents (with comments/strings
    # blanked) so body markup/markdown — e.g. stray backticks in a sample
    # deck — can't corrupt identifier-reference counting.
    scripts = "\n".join(re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL | re.IGNORECASE))
    code = _strip_comments_and_strings(scripts)
    warnings = []

    # 1. Hallucinated imports — bare specifiers with no bundler/importmap.
    has_importmap = bool(re.search(r'<script[^>]*type\s*=\s*["\']importmap["\']', text, re.IGNORECASE))
    if not has_importmap:
        specs = re.findall(r'\bimport\s+(?:[^;\'"]*?\sfrom\s+)?["\']([^"\']+)["\']', scripts)
        specs += re.findall(r'\bimport\s*\(\s*["\']([^"\']+)["\']', scripts)
        specs += re.findall(r'\brequire\s*\(\s*["\']([^"\']+)["\']', scripts)
        bare = sorted({
            s for s in specs
            if not re.match(r'^(https?:|/|\./|\.\./|data:|blob:|node:)', s)
        })
        if bare:
            shown = ", ".join(bare[:5])
            warnings.append(
                f"hallucinated-imports: bare-specifier import(s) with no bundler or importmap "
                f"({shown}) — won't resolve in a single-file browser tool"
            )

    # 2. Unused imports — imported binding referenced only at the import site.
    import_lines = re.findall(r'\bimport\s+([^;\n]*?)\s+from\s+["\'][^"\']+["\']', scripts)
    names = set()
    for clause in import_lines:
        # default + namespace + named bindings
        for m in re.findall(r'\b([A-Za-z_$][\w$]*)\b', re.sub(r'\bas\b', ' ', clause)):
            if m not in ("import", "from"):
                names.add(m)
    # Count references against raw script text (not the stripped copy): a
    # name appearing in a comment/string then counts as "used", biasing
    # toward false negatives rather than the noisier false positives that
    # over-eager string stripping causes on large real-world JS.
    unused = sorted(n for n in names if len(re.findall(r'\b' + re.escape(n) + r'\b', scripts)) <= 1)
    if unused:
        warnings.append(
            f"unused-imports: imported binding(s) referenced only at import site "
            f"({', '.join(unused[:5])})"
        )

    # 3. Orphan TODO/FIXME/XXX/HACK markers within comments.
    comments = _comment_regions(text)
    markers = re.findall(r'\b(TODO|FIXME|XXX|HACK)\b[:\s]*([^\n*/]{0,60})', comments)
    if markers:
        kind, blurb = markers[0]
        sample = (kind + (": " + blurb.strip() if blurb.strip() else "")).strip()
        warnings.append(
            f"orphan-TODO: {len(markers)} TODO/FIXME/XXX/HACK marker(s) left in code "
            f"(first: {sample[:60]!r})"
        )

    # 4. Dead-code functions — named function defined but never referenced.
    # Only statement-position declarations (line-anchored) count: this skips
    # named function *expressions* used inline as callbacks, e.g.
    # addEventListener('x', function onX(){}), which are not dead code.
    defs = set(re.findall(r'(?m)^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(', code))
    defs |= set(re.findall(r'(?m)^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s+)?(?:function\b|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>)', code))
    # A reference exists if the name appears elsewhere in code OR in an
    # inline event-handler attribute (onclick="foo()") in the raw text.
    dead = []
    for name in sorted(defs):
        if name in _ENTRYPOINT_NAMES:
            continue
        in_code = len(re.findall(r'\b' + re.escape(name) + r'\b', scripts))
        in_handlers = len(re.findall(r'on\w+\s*=\s*["\'][^"\']*\b' + re.escape(name) + r'\b', text))
        if in_code <= 1 and in_handlers == 0:
            dead.append(name)
    if dead:
        warnings.append(
            f"deadcode-function: function(s) defined but never called "
            f"({', '.join(dead[:5])})"
        )

    # 5. Mismatched plan — visible copy drifts from sibling plan.md.
    plan_path = os.path.join(os.path.dirname(path), "plan.md")
    rp = os.path.realpath(plan_path)
    if (rp == REPO_ROOT or rp.startswith(REPO_ROOT + os.sep)) and os.path.isfile(rp):
        plan_text = open(rp, encoding="utf-8", errors="replace").read()
        plan_kw = _keywords(plan_text)
        vis_tokens = []
        for tup in re.findall(
            r'<title[^>]*>([^<]+)</title>|<h[1-6][^>]*>([^<]+)</h[1-6]>|'
            r'<button[^>]*>([^<]+)</button>|<label[^>]*>([^<]+)</label>|'
            r'placeholder\s*=\s*["\']([^"\']+)["\']',
            text, re.IGNORECASE
        ):
            vis_tokens.append(" ".join(t for t in tup if t))
        vis_kw = _keywords(" ".join(vis_tokens))
        if len(plan_kw) >= 8 and len(vis_kw) >= 5:
            overlap = len(plan_kw & vis_kw) / len(plan_kw | vis_kw)
            if overlap < 0.05:
                warnings.append(
                    f"mismatched-plan: visible copy shares little vocabulary with plan.md "
                    f"(Jaccard {overlap:.2f}) — built tool may have drifted from the plan"
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
    warnings = check_ai_antipatterns(path)
    for w in warnings:
        print(f"[WARN] {w}")
    if warnings:
        print(f"WARNINGS: {len(warnings)}")
    else:
        print("PASS")


if __name__ == "__main__":
    main()

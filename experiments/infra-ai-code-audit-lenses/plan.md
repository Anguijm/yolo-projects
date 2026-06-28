# Plan — infra-ai-code-audit-lenses

## Goal
Add a fourth advisory lens, `ai_antipatterns.py`, that scans YOLO single-file HTML builds for documented AI-generated-code failure modes, running alongside the existing three lenses (`ux_completeness.py`, `mobile_usability.py`, `cult_status.py`).

## Scope
**In scope:**
- New file `ai_antipatterns.py` at repo root (~120 LOC), identical structural/CLI contract to the existing three lenses: `read_html` validation, `REPO_ROOT` path-containment guard, `[WARN]` lines + `PASS`/`WARNINGS: N` summary, exit 0 always (advisory), exit 1 only on unreadable/non-HTML input.
- Five checks targeting AI-code antipatterns in embedded JS within a single-file HTML build.
- Experiment docs: `experiments/infra-ai-code-audit-lenses/plan.md`, `changes.md`, `README.md`.

**Explicitly NOT in scope:**
- No orchestrator wiring. The existing three lenses are invoked standalone (no shared runner exists); the fourth follows that convention. Wiring all four into a single runner is a separate future tick.
- No modification to `council.py`, `test_project.py`, or any other repo file. Deliverable paths are strictly `ai_antipatterns.py` + the two experiment docs.
- No network calls (no live npm/pypi resolution). The hallucinated-import check uses structural heuristics, not a network registry.

## Approach
Single self-contained script. Subtasks, in sequence (no inter-dependencies beyond shared helpers):

1. **Scaffold** — copy the canonical lens skeleton: shebang, module docstring, `REPO_ROOT`, `HELP`, `read_html`, `main` with `--help`/usage/path-guard, `if __name__`. (dependency for all checks)
2. **check_ai_antipatterns(path)** — runs the 5 checks below against the file text, returns `list[str]` of warnings. Each check is an independent block; order is cosmetic.
3. **Helpers** — `_strip_comments_strings` is intentionally avoided to keep parity with the other regex-only lenses; checks use targeted regexes on raw text and de-dup via sets.
4. Write `changes.md` + `README.md`.

### The 5 checks (tuned for low false-positive rate, since advisory)
1. **hallucinated-imports** — ES-module `import ... from '<spec>'`, `import('<spec>')`, or `require('<spec>')` whose specifier is a *bare* package name (not a URL, not `./`/`../`/`/`-relative, not `data:`/`blob:`). In a single-file browser tool with no bundler these never resolve — a classic "AI assumed a build step" artifact. **Suppressed** when an `<script type="importmap">` is present (bare specifiers are then legitimate).
2. **unused-imports** — for each named/default binding pulled in by an `import` statement, warn if the binding name appears only once in the whole file (i.e. only at the import site).
3. **orphan-TODO** — `TODO`/`FIXME`/`XXX`/`HACK` markers left in shipped code (in `//`, `/* */`, or `<!-- -->`). Reports count + first marker text.
4. **deadcode-function** — named function declarations (`function foo(`) and named function expressions (`const foo = function`/`const foo = (…) =>`) whose name appears exactly once in the file (defined, never called/referenced — including from inline `onclick=` handlers, which count as references). Common entry points (`main`, `init`, `setup`, `start`) are exempt.
5. **mismatched-plan** — if a sibling `plan.md` exists next to the index.html, compute Jaccard keyword overlap between the plan's Goal/Scope prose and the tool's visible copy (`<title>`, `<h1>`, headings, button labels). Warn if overlap is below a low threshold (0.05) AND both sides have enough keywords to judge — flags plan-drift where the built tool diverged from what was planned. Silently skipped when no `plan.md`.

## File Layout
- `ai_antipatterns.py` — NEW, ~120 LOC, repo root.
- `experiments/infra-ai-code-audit-lenses/plan.md` — NEW (this file).
- `experiments/infra-ai-code-audit-lenses/changes.md` — NEW (implementation gate).
- `experiments/infra-ai-code-audit-lenses/README.md` — NEW (usage + check rationale).

## Function Map
`ai_antipatterns.py`:
- `read_html(path)` — open utf-8, validate HTML header, return text or `sys.exit(1)`. (mirrors the other lenses)
- `_keywords(text)` — lowercase alphanumeric tokens ≥4 chars, minus a small stopword set; returns `set[str]`. (helper for check 5)
- `check_ai_antipatterns(path)` — run the 5 checks, return `list[str]`.
- `main()` — `--help`, usage, `REPO_ROOT` containment guard, print warnings + `PASS`/`WARNINGS: N`.

## Security
- Read-only tool; opens exactly one user-supplied path, never writes.
- `REPO_ROOT` containment guard (`os.path.realpath` + prefix check) identical to the existing lenses — refuses to read files outside the repo, blocking path-traversal/symlink escape.
- No network, no `eval`, no subprocess, no shell. `plan.md` sibling is read only if it resolves inside `REPO_ROOT` (same guard applied).
- Regex-only; inputs are bounded by file size already validated by `read_html`.

## UI
N/A — CLI lens. Output contract matches the sibling lenses exactly: `[WARN] <check>: <desc>` lines, then `PASS` or `WARNINGS: N`. `--help`/`-h` prints the HELP block and exits 0.

## Guide
- Module docstring + `HELP` text enumerate every check and the exit-code contract, matching the house style of the other three lenses.
- README.md documents when to run the lens, what each check means, and the deliberate false-positive trade-offs (e.g. importmap suppression).

## Edge Cases
- File not found / not HTML → `ERROR` + exit 1 (parity with siblings).
- No JS at all (pure markup tool) → all code checks no-op, likely `PASS`.
- `<script type="importmap">` present → hallucinated-imports suppressed.
- No sibling `plan.md` → mismatched-plan silently skipped (not a warning).
- Minified single-line JS → function/import regexes still match on tokens; dead-code may under-report (acceptable — advisory).
- Path outside repo root → `ERROR` + exit 1.
- Empty file → caught by `read_html` HTML-validation (exit 1).

## Test Strategy
- `python3 -c "import ast; ast.parse(open('ai_antipatterns.py').read())"` — syntax OK.
- `python3 ai_antipatterns.py --help` — prints HELP, exit 0.
- Run on 5 known-good portfolio projects — confirm exit 0 always and no absurd false positives on shipped code (hit-rate validation per plan_summary).
- Run on a crafted fixture containing a bare import, a TODO, and a dead function — confirm all three fire.
- Confirm exit 1 on a missing path and on a non-HTML file.

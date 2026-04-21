# Plan — infra-yolo-evals

## Goal
Add three advisory Python lenses (`ux_completeness.py`, `mobile_usability.py`, `cult_status.py`) that scan single-file HTML YOLO builds for UX, mobile, and differentiation gaps before the council review.

## Scope
**In scope:**
- Three new Python scripts at repo root: `ux_completeness.py`, `mobile_usability.py`, `cult_status.py`
- `experiments/infra-yolo-evals/` directory for plan and changes artifacts
- All three scripts are advisory-only (exit 0 always; warnings printed but do not block the build)

**Out of scope:**
- Modifying `test_project.py`, `eval_bugs.py`, `security_scan.py`, or `council.py`
- Wiring lenses into CI or making them hard-fail (planned for follow-on after 5 builds of tuning)
- Touching any project's HTML files
- Web scraping or network requests of any kind

## Approach
1. Write `experiments/infra-yolo-evals/plan.md` (this file) — PLAN gate
2. Implement the three scripts (IMPLEMENTATION)
3. Write `experiments/infra-yolo-evals/changes.md`
4. Pre-filter: `python3 -c "import ast; ast.parse(...)"` on each script
5. Run all three against ≥5 portfolio projects; collect hit counts for TESTS gate
6. TESTS gate with hit-rate evidence
7. OUTCOME gate: scripts present, no regression

Subtask sequencing:
- Steps 1→2: sequential (plan before code)
- Steps 3→4: parallel (write changes.md while confirming syntax)
- Steps 5→6→7: sequential

## File Layout
| File | Action | Notes |
|------|--------|-------|
| `ux_completeness.py` | new, ~130 lines | repo root |
| `mobile_usability.py` | new, ~120 lines | repo root |
| `cult_status.py` | new, ~110 lines | repo root |
| `experiments/infra-yolo-evals/plan.md` | new (this file) | |
| `experiments/infra-yolo-evals/changes.md` | new, post-impl | |

## Function Map
### ux_completeness.py
- `read_html(path)` — opens file with `encoding='utf-8', errors='replace'`; validates `<html` or `<!doctype` presence; returns text or raises
- `check_ux_completeness(path)` — calls `read_html`, runs all UX checks, returns `list[str]` of warning strings
- `main()` — CLI entry: reads `sys.argv[1]`, calls `check_ux_completeness`, prints results, exits 0

### mobile_usability.py
- `read_html(path)` — same as above (copied to each script — no shared module)
- `check_mobile_usability(path)` — calls `read_html`, runs all mobile checks, returns `list[str]` of warning strings
- `main()` — CLI entry: reads `sys.argv[1]`, calls `check_mobile_usability`, prints results, exits 0

### cult_status.py
- `read_html(path)` — same as above
- `check_cult_status(path)` — calls `read_html`, runs differentiation heuristics, returns `list[str]` of warning strings
- `main()` — CLI entry: reads `sys.argv[1]`, calls `check_cult_status`, prints results, exits 0

## Security
These are dev-time read-only lenses. They accept a single file path via `sys.argv[1]` and perform regex-based text scanning only — no code is executed from the HTML, no network requests, no file writes. Same trust model as `eval_bugs.py` and `security_scan.py`: internal dev-pipeline tools, no production trust boundary. Per the adopt-planning-mode 2026-04-10 precedent, SECURITY may not require producer-side sanitization absent a concrete downstream parser that executes the script argument as code.

**ReDoS safety**: All regex patterns in all three scripts are linear-time (no catastrophic backtracking). Patterns are simple literal searches or character-class alternations with no nested quantifiers and no overlapping alternation paths. Examples: `re.search(r'<meta[^>]+name=["\']viewport', text)` is O(n). No backreferences, no look-behind, no quantified groups inside quantified groups. This will be verified by inspection during IMPLEMENTATION gate review.

## UI
CLI-only. Output format matches `eval_bugs.py`:
```
[WARN] category: description of the issue found
...
WARNINGS: N  (or PASS if N=0)
```
Exit 0 always (advisory mode — warnings are informational, not build blockers).

## Guide
Usage is identical across all three scripts:
```bash
python3 ux_completeness.py <project>/index.html
python3 mobile_usability.py <project>/index.html
python3 cult_status.py <project>/index.html
```
Invocation from the tick prompt's pre-filter section, same as `eval_bugs.py <project>`.

## Edge Cases
- File not found: print `ERROR: <path> not found`, exit 1
- Not valid HTML (missing `<html` or `<!doctype html`): print `ERROR: <path> does not appear to be an HTML file`, exit 1 — prevents meaningless warnings on binary or non-HTML inputs
- Empty file (0 bytes): caught by the HTML validation check above; exit 1
- Non-ASCII content: files opened with `encoding='utf-8', errors='replace'` — mojibake is replaced with `�` rather than crashing
- Very large file (>500KB): no special handling; all patterns are O(n) linear (see Security section)

## Test Strategy
1. Syntax validation: `python3 -c "import ast; ast.parse(open(p).read())"` on each script — must pass
2. Portfolio run: execute all three against these 5 projects:
   - `cron-explain/index.html` (recent, solid)
   - `url-dissect/index.html` (recent)
   - `uuid-inspector/index.html` (recent)
   - `naval-scribe/index.html` (flagship — should score well on all three)
   - One older/simpler project to expect more warnings
3. Confirm: naval-scribe and cron-explain produce ≤2 warnings each across all three lenses
4. Confirm: at least one project has ≥1 warning from each lens (scripts are not vacuously passing)
5. Confirm: no false positives on patterns that are genuinely present (viewport meta on mobile-aware projects)

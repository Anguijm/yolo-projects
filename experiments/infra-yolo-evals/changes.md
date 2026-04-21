# Changes — infra-yolo-evals implementation

## Files created

### ux_completeness.py (new, 81 lines, repo root)
- `read_html(path)` — opens with `encoding='utf-8', errors='replace'`; validates `<html` or `<!doctype` in first 500 chars; exits 1 if not valid HTML
- `check_ux_completeness(path)` — runs 5 UX checks; returns `list[str]` of warning strings:
  1. **error-state**: looks for `class=*error`, `catch(`, `onerror=`, `try again`, `errorMessage`, `.catch(` — flags if absent
  2. **empty-state**: if `<ul`, `<table`, `output-area`, or `results` are present, checks for `no results`, `nothing here`, `empty state`, `start by`, `enter a`, etc. — flags if absent
  3. **loading-state**: if `fetch(`, `async function`, or `await` are present, checks for `loading`, `spinner`, `aria-busy`, `progress`, `please wait` — flags if absent
  4. **focus-ring**: flags `outline:none/0` without `:focus-visible` or `box-shadow` in a `:focus` rule
  5. **primary-cta**: flags if no `<button`, `<input`, `<select`, `<textarea`, or `role="button"` found
- `main()` — CLI entry; reads `sys.argv[1]`, calls `check_ux_completeness`, prints `[WARN] ...` per warning, prints `WARNINGS: N` or `PASS`; exits 0

### mobile_usability.py (new, 90 lines, repo root)
- `read_html(path)` — same as ux_completeness.py
- `check_mobile_usability(path)` — runs 5 mobile checks; returns `list[str]` of warning strings:
  1. **viewport**: flags missing `<meta name="viewport">`
  2. **responsive**: flags missing `@media (` — no responsive CSS breakpoints
  3. **tap-target**: flags `font-size: 0.[0-6]rem` on button/input/.btn selectors (below 0.7rem)
  4. **table-overflow**: flags `<table>` without `overflow-x:auto` anywhere in the file
  5. **touch-events**: flags `mouseover`/`mouseenter`/`mouseleave` without `touchstart`/`focus`/`pointerover` equivalents
- `main()` — same pattern as ux_completeness.py

### cult_status.py (new, 88 lines, repo root)
- `read_html(path)` — same as ux_completeness.py
- `check_cult_status(path)` — runs 5 differentiation heuristics; returns `list[str]` of warning strings:
  1. **animation**: flags missing `@keyframes`, `transition:`, `animation:`, or `animate(` — "it moves"
  2. **canvas-svg**: flags missing `<canvas>` or `<svg>` — "it draws something"
  3. **keyboard-shortcuts**: flags missing `keydown`/`keyup`/`KeyboardEvent`/`hotkey`/`shortcut` — "power-user accessibility"
  4. **realtime**: flags missing `input`/`change` event listeners or `oninput`/`onchange` — "it responds instantly"
  5. **memorable-hook**: flags missing `<title>` (≥10 chars), `<h1>` (≥10 chars), or `<p>` (≥20 chars) in first 3KB
- `main()` — same pattern as ux_completeness.py

## Portfolio hit rates (5 projects)

| Project | ux warnings | mobile warnings | cult warnings |
|---------|-------------|-----------------|---------------|
| cron-explain | 1 (focus-ring) | 2 (responsive, tap-target) | 2 (canvas-svg, keyboard) |
| url-dissect | 1 (focus-ring) | 2 (responsive, tap-target) | 1 (canvas-svg) |
| uuid-inspector | 1 (focus-ring) | 2 (responsive, tap-target) | 2 (canvas-svg, keyboard) |
| naval-scribe | 1 (focus-ring) | 2 (tap-target, table-overflow) | 2 (animation, canvas-svg) |
| markdown-deck | 1 (focus-ring) | 2 (responsive, tap-target) | **PASS** |

**Key findings:**
- `focus-ring` fires on all 5 — common pattern in YOLO builds (outline:none without :focus-visible)
- `responsive` fires on desktop-first tools (cron-explain, url-dissect, uuid-inspector, markdown-deck) — expected; not a defect for presentation tools
- `table-overflow` correctly caught the naval-scribe regression (SSIC table has no overflow-x:auto wrapper)
- `cult_status.py` correctly grades markdown-deck as PASS (it has transitions, canvas, keyboard shortcuts, realtime input handling, and a descriptive title)
- `tap-target` fires consistently — most YOLO tools use sub-0.7rem button fonts

## What was NOT changed
- `test_project.py`, `eval_bugs.py`, `security_scan.py`, `council.py` — all unchanged
- No project HTML files touched
- No session_state.json or roadmap files modified

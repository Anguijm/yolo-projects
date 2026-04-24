# Plan: Inline Chart Blocks

## Goal
Add `\`\`\`chart` fenced block support — bar, line, and pie charts rendered as pure inline SVGs in slides, with CSV-style data input and a theme-aware "presentation-native" aesthetic.

## Scope
**In scope:**
- Three chart types: `bar`, `line`, `pie`
- CSV-style data (label, value pairs; optional `title:` line)
- Pure SVG rendering, zero dependencies
- **Signature move:** Charts inherit active deck theme colors via `getThemeColors()` — bars/lines/pies automatically use the slide accent palette; value labels rendered directly on bars/above dots/on pie slices
- Preview/presentation parity (same `renderChart` function for both)
- PPTX export: chart SVG → canvas → PNG (same pipeline as diagrams)
- Stats panel: count chart blocks
- DECK_GUIDE.md documentation update

**Out of scope:**
- Multi-series charts
- Interactive hover/tooltips
- Axis tick customization
- Export to CSV

## Approach

### Subtask 1: CSS
Add `.slide-chart` wrapper style matching `.slide-diagram`. Add `aria-label` support note in SVG generation.

### Subtask 2: `parseChartData(csvData)` + `renderChart(type, csvData)` + helpers
**`parseChartData(csvData)`:**
1. Lines starting with `title:` → extract title
2. Remaining non-empty lines → split on first `,` → (label, parseFloat(value)) pairs
3. Invalid (NaN value, missing comma) → count as `skipped`
4. **Cap at 20 points and record `truncated` count** (per UI PLAN-escalation 2026-04-24): if `points.length > 20`, set `truncated = points.length - 20`, slice to 20, and `renderChart` displays a visible warning "20-point limit — N additional points hidden" so the truncation is never silent
5. Returns `{ title, points: [{label, value}], skipped, truncated }`

**Labels** truncated to **16 chars** (bumped from 8 per UI PLAN-escalation 2026-04-24 — 8 was aggressive for typical category names like "Q1 Revenue") with `…` appended if longer. 16 chars covers the vast majority of real labels (months, quarters, product names) while still preventing overflow.

**`renderChart(type, csvData)`:**
- Guard: 0 points → return `[chart: no data]` div
- Wraps SVG in `<div class="slide-chart" role="img" aria-label="[type] chart: [title]">`
- If `skipped > 0`, appends a `<div class="slide-chart-warn">[N line(s) skipped — invalid format]</div>` below SVG
- Dispatches to bar/line/pie renderer

**Theme integration (signature move):**
- Calls `getThemeColors()` (already defined in app) to get the current theme
- Derives a 6-color palette from theme: `[tc.accent, tc.heading, tc.primary, '#f59e0b', '#f472b6', '#a78bfa']` where `tc.accent` is the theme's main accent
- Bar fills, line strokes, pie segments all use this palette → charts look native to the current slide theme

**Bar chart SVG (viewBox 480×260):** (height bumped 220→260 per UI PLAN-escalation 2026-04-24 to accommodate the warning row + larger fonts)
- Plot area: left margin 44px (y-axis), bottom margin 44px (x-axis), top 28px (title), right 8px, **bottom-of-plot baseline at y=`plotTop + plotH * (max / (max - min))`** when negative values are present
- **Negative-value rendering** (per BUGS PLAN-escalation 2026-04-24, replaces clamping): if any point has `value < 0`, the y-axis range is `[min, max]` (not `[0, max]`) and bars below the baseline render extending downward. The baseline (zero line) is drawn as a `stroke: #444` reference line. If all values are >= 0, baseline = 0 (existing behavior). No silent data transformation.
- **Degenerate-range guard** (per BUGS PLAN-escalation #2 2026-04-25): when `max - min == 0` (all data points identical, e.g. `[-5, -5, -5]` or `[7, 7, 7]`), the formula `plotH * (max / (max - min))` would divide by zero. Guard: if `max === min`, render a single horizontal line of bars/dots at `y = plotTop + plotH / 2` (vertical center of plot area), with the baseline reference line drawn at the same y. Y-axis labels show the constant value once; no grid lines drawn for this case. Visually communicates "all values equal at N" without a NaN crash.
- Bar width: `min(36, (plotW / n) * 0.65)`, centered in each slot
- **Rounded bar caps:** `rx="3" ry="3"` on rect elements (top-rounded for positive bars, bottom-rounded for negative bars)
- **Value labels:** rendered above each positive bar / below each negative bar (right-aligned to bar center, **11px font** [bumped from 8px], theme accent color)
- Y-axis: 4 grid lines with labels (max, 75%, 50%, 25%, 0% — extended to include negatives if `min < 0`); `stroke: #1a1a1a`
- X-axis: labels **16-char max** with `…`; rotate `-35°` when >5 items; **`font-size: 11px`** [bumped from 8px]; anchored at bar center
- Title: centered, **13px** [bumped from 10px], theme heading color
- **Truncation warning row** (per UI PLAN-escalation 2026-04-24): if `parseChartData` returned `truncated > 0`, render a small text row below the chart: `"⚠ 20-point limit — {truncated} additional points hidden"`, 10px, theme warning color
- All text via `esc()` before SVG insertion; `aria-label` on wrapping div

**Line chart SVG (viewBox 480×260):** (same height bump)
- Same margins as bar
- **Negative-value rendering**: same baseline + range logic as bar chart. Line crosses below baseline naturally when values go negative.
- Filled area: polygon from points + baseline (zero line, not bottom edge), theme accent color at 15% opacity
- Polyline: stroke = theme accent, stroke-width 2, no fill
- Dots: `r=3.5`, fill = theme accent
- **Value labels:** above each dot for positive values / below for negatives, **`font-size: 11px`** [bumped from 8px], theme heading color
- X/Y axes identical to bar
- Same truncation warning row when `truncated > 0`

**Pie chart SVG (viewBox 480×260):** (height bumped 220→260 to match bar/line for layout consistency)
- Circle center: (160, 130), radius 95
- If all values 0: gray circle + centered `[no data]` text; legend shows all items with "0%"
- Segments: SVG arc paths from cumulative angles; theme palette rotation
- **Value labels:** percentage text inside/near segment center (when segment angle > 15°; else skipped)
- **Legend behavior — STANDARDIZED** (per UI PLAN-escalation #2 2026-04-25, resolves the prior contradiction with Subtask 8 item 10): show **top 5 segments by value**, then aggregate the remaining segments into a single **`Other (N more)` wedge** + legend entry. Legend total is always ≤ 6 entries — no `+N more` fly-out, no inconsistent rendering between SVG and docs.
- Legend layout: right side x=260, y starts 30; colored square 10×10 + label (**16-char max** with `…`, bumped from 8 per UI PLAN-escalation #2) + `%` value; **font-size 11px** [bumped from 8px to match bar/line label fonts]
- Title: x=160 centered, top, **13px** [bumped from 10px to match bar/line]

### Subtask 3: Wire into `md()`
Widen fenced block regex from `` `(\w*)` `` to `([\w ]*)` so `chart bar` is captured. Add `else if (lang.trim().split(' ')[0].toLowerCase() === 'chart')` branch calling `renderChart(lang.trim().split(' ')[1] || 'bar', code)`.

### Subtask 4: `parseBodyLines()` update
Add chart block detection before generic `` ``` `` branch. Capture subtype, collect lines, push `{ type: 'chart', chartType, text }`.

### Subtask 5: PPTX export
Add `item.type === 'chart'` branch in PPTX body generator parallel to diagram branch: call `renderChart`, extract SVG content, register as rasterizable image.

### Subtask 6: Stats panel
Add chart counter in extraction (mirror diagram pattern). Add "Charts" card in overview. Add `chart×N` badge in per-slide breakdown.

### Subtask 7: `complexContent()` update
Add `.slide-chart` to selector so autoFitContent fallback triggers.

### Subtask 8: DECK_GUIDE.md documentation
Add a "Chart Blocks" section after the Diagrams section. Per GUIDE PLAN-escalation 2026-04-24 the section MUST explicitly document each behavior — no "see code" hand-waving. Required coverage:

1. **Syntax** — fenced block: ` ```chart bar `, ` ```chart line `, ` ```chart pie ` followed by CSV body
2. **Optional title line** — `title: My Chart` (must be the first non-empty line) with example
3. **Data format** — `Label, Value` per line, comma split on FIRST comma only; labels must not contain commas (no escape mechanism exists)
4. **Label truncation** — labels longer than 16 chars are truncated with `…`; document the exact limit and that this is to prevent layout overflow
5. **20-point cap with warning** — if more than 20 data points, the first 20 render and a `⚠ 20-point limit — N additional points hidden` warning row appears below the chart. Not silent.
6. **Negative value rendering** — bar/line charts render negatives properly (bars extend below the baseline; line points dip below) when ANY point is negative. The baseline (zero) is drawn as a reference line. No clamping.
7. **`[chart: no data]` placeholder** — empty or all-invalid CSV body shows this placeholder div instead of an empty SVG, so authors notice and fix
8. **Skipped invalid lines** — lines with NaN values or missing comma are skipped during parse; if any lines were skipped, a visible `[N line(s) skipped — invalid format]` warning div is rendered below the chart so authors can spot and fix bad data
9. **Unknown chart type** — `chart foo` with no recognized type (bar/line/pie) falls back to `bar` with a console warning; no crash
10. **Pie chart `+N more` legend** — pie charts with > 6 slices show top 5 + an aggregate "Other (N more)" wedge so the legend stays readable
11. **Theme integration** — colors pull from current theme tokens (heading color for titles, accent for bars/lines/value-labels, warn color for the 20-point warning) so charts always match the deck's palette
12. **Inline `<details>` quick reference** (per LESSONS advisory PLAN-escalation 2026-04-24, satisfies the port-ref `<details>` pattern KEEP rule for tools accepting structured input): in the editor's chart-block help tooltip / panel, include a `<details><summary>SUPPORTED CHART FORMATS</summary>` block listing the syntax, type names, optional title, and CSV format with one example for each chart type. Mirrors the port-ref bulk-annotate help pattern.

The section should include 3 worked examples (bar / line / pie) with fenced chart blocks AND their rendered output described in prose. Total addition: ~80 lines to DECK_GUIDE.md.

## File Layout
- `markdown-deck/index.html` (only file modified)
  - CSS block (~line 94): `.slide-chart`, `.slide-chart-warn` styles
  - Before `renderMath` (~line 838): `parseChartData()` + `renderChart()` (~90 LOC)
  - `md()` code block regex (~line 929): widen regex; add chart branch
  - `complexContent()` (~line 1222): add `.slide-chart`
  - `parseBodyLines()` (~line 1947): chart fence branch
  - PPTX body generator (~line 2125): chart image branch
  - Stats extraction (~line 3709): chart counter
  - Stats display (~line 3744–3770): chart card + badge
  - DECK_GUIDE.md section (end of file, after diagrams section)

## Function Map
- `markdown-deck/index.html`
  - **New:** `parseChartData(csvData)` → `{ title, points, skipped }`
  - **New:** `renderChart(type, csvData)` → SVG HTML string in `.slide-chart` div
  - **Modified:** `md()` — regex widened; chart dispatch added
  - **Modified:** `complexContent()` — `.slide-chart` added
  - **Modified:** `parseBodyLines()` — chart fence detection added
  - **Modified:** PPTX body generator — chart → SVG → PNG branch
  - **Modified:** stats extraction — chart counter
  - **Modified:** stats display — chart card + badge

## Security
- Labels run through `esc()` before SVG text insertion
- Values parsed as `parseFloat`; NaN lines skipped
- No eval; SVG built by string concatenation with escaped values
- Theme colors from `getThemeColors()` are internal CSS values (already trusted)
- No external resources, no XHR; CSP unchanged (CONSTRAINTS.md)
- `aria-label` text uses escaped title/type strings

## UI
- Charts render inline at fenced block position (same as diagrams)
- Theme-aware: colors auto-match the active slide theme (key differentiator)
- Value labels directly on bars/points/slices — no need to read axes for simple comparisons
- Truncated labels show `…` suffix (e.g., `Category…`)
- Skipped lines → small warning note below chart: `[N line(s) skipped — invalid format]`
- `aria-label` on chart container for accessibility
- `[chart: no data]` placeholder when data is missing/all invalid
- Stats modal shows "Charts" count card

## Guide
- Syntax: ` ```chart bar `, ` ```chart line `, ` ```chart pie `
- Optional first line: `title: My Title`
- Data lines: `Label, Value` (numeric value required)
- Labels > 16 chars truncated with `…` in display
- Unknown type → bar fallback
- Invalid lines skipped; count shown below chart
- Charts automatically use the current deck theme palette

## Edge Cases
- 0 valid points → `[chart: no data]` placeholder
- 1 data point → single bar / single dot / full-circle pie
- All values 0 → bars/line at baseline; pie shows gray circle + `[no data]`; legend shows 0% for all entries
- Negative values → rendered below baseline (bars extend down, line dips; zero line drawn as reference)
- Labels > 16 chars → truncated with `…`
- Unknown chart type → bar fallback
- > 20 data points → first 20 only
- Missing comma → line skipped, count noted in warning
- Value is NaN → line skipped, count noted in warning
- Pie segment angle ≤ 15° → value label omitted (too small to fit)
- Pie legend > 8 items → first 8 shown + `+N more` text

## Test Strategy
- `test_project.py markdown-deck` — headless browser load, no JS errors
- Visual: all 3 chart types with sample data → SVG renders in preview
- Visual: presentation mode → chart visible at correct scale
- Visual: change theme → chart colors update on re-render
- Edge: empty chart block → `[chart: no data]`
- Edge: invalid lines → warning shown
- Stats panel: "Charts" card increments with chart blocks
- PPTX export: chart appears as embedded PNG

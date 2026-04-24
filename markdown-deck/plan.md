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
4. Clamp to 20 points max
5. Returns `{ title, points: [{label, value}], skipped }`

All labels truncated to 8 chars with `…` appended if longer (e.g., `Category…`).

**`renderChart(type, csvData)`:**
- Guard: 0 points → return `[chart: no data]` div
- Wraps SVG in `<div class="slide-chart" role="img" aria-label="[type] chart: [title]">`
- If `skipped > 0`, appends a `<div class="slide-chart-warn">[N line(s) skipped — invalid format]</div>` below SVG
- Dispatches to bar/line/pie renderer

**Theme integration (signature move):**
- Calls `getThemeColors()` (already defined in app) to get the current theme
- Derives a 6-color palette from theme: `[tc.accent, tc.heading, tc.primary, '#f59e0b', '#f472b6', '#a78bfa']` where `tc.accent` is the theme's main accent
- Bar fills, line strokes, pie segments all use this palette → charts look native to the current slide theme

**Bar chart SVG (viewBox 480×220):**
- Plot area: left margin 40px (y-axis), bottom margin 40px (x-axis), top 24px (title), right 8px
- Auto-scale: max value → plot height; negative values clamped to 0
- Bar width: `min(36, (plotW / n) * 0.65)`, centered in each slot
- **Rounded bar caps:** `rx="3" ry="3"` on rect elements
- **Value labels:** rendered above each bar (right-aligned to bar center, 8px font, theme accent color)
- Y-axis: 4 grid lines with labels (0%, 25%, 50%, 75%, 100% of max); `stroke: #1a1a1a`
- X-axis: labels 8-char max with `…`; rotate `-35°` when >5 items; `font-size: 8px`; anchored at bar center
- Title: centered, 10px, theme heading color
- All text via `esc()` before SVG insertion; `aria-label` on wrapping div

**Line chart SVG (viewBox 480×220):**
- Same margins as bar
- Filled area below line: polygon from points + baseline, theme accent color at 15% opacity
- Polyline: stroke = theme accent, stroke-width 2, no fill
- Dots: `r=3.5`, fill = theme accent
- **Value labels:** above each dot, `font-size: 8px`, theme heading color
- X/Y axes identical to bar

**Pie chart SVG (viewBox 480×220):**
- Circle center: (160, 110), radius 85
- If all values 0: gray circle + centered `[no data]` text; legend shows all items with "0%" 
- Segments: SVG arc paths from cumulative angles; theme palette rotation
- **Value labels:** percentage text inside/near segment center (when segment angle > 15°; else skipped)
- Legend: right side x=260, y starts 30; colored square 8×8 + label (8-char max + `…`) + `%` value; font-size 8px; up to 8 items shown, remainder indicated by `+N more`
- Title: x=160 centered, top, 10px

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
Add "Chart Blocks" section after Diagrams with syntax examples for all 3 types, theme integration note.

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
- Labels > 8 chars truncated with `…` in display
- Unknown type → bar fallback
- Invalid lines skipped; count shown below chart
- Charts automatically use the current deck theme palette

## Edge Cases
- 0 valid points → `[chart: no data]` placeholder
- 1 data point → single bar / single dot / full-circle pie
- All values 0 → bars/line at baseline; pie shows gray circle + `[no data]`; legend shows 0% for all entries
- Negative values → clamped to 0
- Labels > 8 chars → truncated with `…`
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

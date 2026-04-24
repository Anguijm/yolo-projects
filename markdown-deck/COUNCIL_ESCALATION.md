# Council Escalation — markdown-deck

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T11:55:28.101522+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The plan explicitly states that negative values will be clamped to 0 for bar and line charts, which fundamentally misrepresents the actual data and can lead to incorrect interpretations.
- **Required fix:** Implement proper rendering of negative values for bar and line charts (e.g., bars extending below the x-axis, line points below the baseline). If clamping is strictly required, a clear visual warning or indication of data transformation must be added to the chart.
- **Evidence:** `Bar chart SVG (viewBox 480×220): ... negative values clamped to 0`

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly addresses potential injection vectors by stating that all user-provided text (labels, titles, chart type in aria-label) will be run through an `esc()` function before insertion into SVG or HTML attributes, and numeric values are parsed as floats.
- **Evidence:** `Security section: 'Labels run through `esc()` before SVG text insertion'; 'Values parsed as `parseFloat`'; 'No eval; SVG built by string concatenation with escaped values'; '`aria-label` text uses escaped title/type strings'`

### UI — OBJECT (high)
- **Reason:** The plan silently truncates data to 20 points without user feedback, and uses excessively small font sizes (8-10px) and aggressive 8-character label truncation which will lead to illegibility and confusion.
- **Required fix:** Add a warning message when data points exceed the 20-point limit; increase minimum font sizes for labels and titles, and reconsider the 8-character label truncation limit or provide an option to disable it.
- **Evidence:** `Approach > Subtask 2 > parseChartData: 'Clamp to 20 points max' (no corresponding warning in renderChart); Bar/Line/Pie chart SVG sections: 'font-size: 8px', 'Title: 10px', 'All labels truncated to 8 chars with … appended if longer'`

### GUIDE — OBJECT (high)
- **Reason:** The plan for `DECK_GUIDE.md` documentation is too brief and does not explicitly guarantee coverage of all critical usage details, error messages, and UI behaviors described elsewhere in the plan.
- **Required fix:** The `DECK_GUIDE.md` update must explicitly include documentation for: the optional `title:` line, the `Label, Value` data format, label truncation behavior (`…`), the warning message for skipped invalid data lines, the `[chart: no data]` placeholder, the fallback to 'bar' for unknown chart types, the presence of value labels directly on chart elements, the 20-point data limit, and pie chart legend behavior (e.g., `+N more`).
- **Evidence:** `markdown-deck/plan.md:Subtask 8: DECK_GUIDE.md documentation`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature solves a clear problem for users who need to quickly embed simple, theme-aware charts into their markdown presentations without external tools, enhancing the core utility of markdown-deck.
- **Evidence:** `The 'signature move' of theme-aware colors and direct value labels addresses a common pain point with static image embeds, making it a practical tool for recurring presentation needs. It fills a gap not easily covered by browser features or quick web searches.`

### COOL — APPROVE (low)
- **Reason:** The theme-aware charts with inline value labels and rounded bar caps provide a clear signature move, making the tool feel native and polished, differentiating it from generic chart generators.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The plan accepts CSV-style data input but does not include a `<details>` element in the UI to list supported input formats, violating a documented `KEEP` lesson from `port-ref` that addressed a high-severity GUIDE objection.
- **Required fix:** Add a `<details>` element to the UI (e.g., near the chart input area or in a help modal) listing the supported CSV input format for chart blocks, as this was previously identified as a high-severity missing documentation issue by GUIDE.
- **Evidence:** `KEEP — `<details>` supported-formats block for bulk input features — When a tool accepts structured text input (YAML, JSON, CSV), add a `<details>` element listing supported input formats. Satisfies GUIDE at the OUTCOME gate without cluttering the primary UI; GUIDE flagged the absence of explicit fo`

## Resolution

**RESOLVED 2026-04-25 by John (interactive session). All 4 concerns accepted — plan.md updated.**

### BUGS (high) — ACCEPTED
Negative-value clamping replaced with proper rendering. Plan Subtask 2 / chart SVG sections updated: y-axis range `[min, max]` when any value is negative; bars extend below the baseline (zero line drawn as `stroke: #444`); top-rounded caps on positive bars / bottom-rounded on negative bars; no silent data transformation.

### UI (high) — ACCEPTED (all 3 sub-issues)
1. **Silent 20-point truncation** → `parseChartData` records `truncated` count; `renderChart` renders `⚠ 20-point limit — N additional points hidden` warning row below the chart
2. **8px fonts** → bumped to **11px for value/axis labels**, **13px for titles** (10px warning row). viewBox height bumped 220→260
3. **8-char label truncation** → bumped to **16 chars**

### GUIDE (high) — ACCEPTED
Subtask 8 expanded from 1-line stub to explicit 12-point coverage: syntax, title line, data format, label truncation, 20-point cap with warning, negative rendering, `[chart: no data]` placeholder, skipped invalid lines, unknown-type fallback, pie `+N more` legend, theme integration, and a `<details>` SUPPORTED CHART FORMATS reference. 3 worked examples required.

### LESSONS advisory (auto-downgraded) — ACCEPTED via Subtask 8 item 12
The port-ref `<details>` supported-formats KEEP rule applies. Folded into the documentation subtask rather than as a separate code subtask.

### Other 3 angles — APPROVE
SECURITY, USEFULNESS, COOL all clean. SECURITY praised the `esc()` wrapping pattern.

Cron may rerun PLAN; expected clean pass.

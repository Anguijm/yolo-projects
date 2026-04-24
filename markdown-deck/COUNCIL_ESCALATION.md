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

Human decision required. Resume the build after updating session_state.json.

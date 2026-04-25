# Council Escalation — markdown-deck

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T00:19:56.664966+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** Pie charts can produce incorrect or uninterpretable visual output when given negative data values, which are not explicitly supported by the stated goal for pie charts.
- **Required fix:** Modify `renderChart` to filter out negative data points for pie charts and optionally display a warning, as the stated goal only supports negative values for bar and line charts.
- **Evidence:** `file:1000-1004, function _chartPie(parsed, tc, palette) { ... var total = pts.reduce(function(a, b) { return a + b.value; }, 0); ... var angles = displayPts.map(function(p) { return p.value / total * 360; }); ... }`

### SECURITY — APPROVE (low)
- **Reason:** The new chart feature correctly escapes user-provided labels and titles, and theme-derived colors are prefixed with '#' before SVG insertion, preventing new XSS vectors.

### UI — APPROVE (low)
- **Reason:** The inline chart blocks are well-integrated, provide clear feedback for invalid data, are responsive, and include good accessibility attributes.

### GUIDE — OBJECT (medium)
- **Reason:** The inline chart block feature is not discoverable through the default application content or a dedicated UI element.
- **Required fix:** Add a basic chart block example to the initial markdown content displayed in the editor textarea.
- **Evidence:** `file:markdown-deck/index.html (textarea id='input' content is missing a chart example)`

### USEFULNESS — APPROVE (low)
- **Reason:** Inline chart blocks directly address a core need for data visualization in presentations, enhancing utility significantly.
- **Evidence:** `Common presentation tools (PowerPoint, Google Slides) all offer chart creation. This feature brings that essential capability directly into the markdown workflow, reducing friction and ensuring theme consistency. The handling of data (CSV, truncation warnings) suggests robustness for real-world use.`

### COOL — APPROVE (low)
- **Reason:** Pure SVG, zero-dependency, theme-aware inline charts with simple CSV syntax are a signature move that reinforces the project's unique ethos.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The SECURITY objection, as described in the council focus, re-litigates architectural constraints (unsafe-inline CSP, md() + innerHTML rendering) that are explicitly documented as out-of-scope for per-feature review, violating `STRUCTURAL CONSTRAINTS` and a recurring `INSIGHT` in `learnings.md`.
- **Required fix:** The SECURITY angle must retract its objection based on pre-existing architectural patterns and instead focus only on new attack surfaces introduced by the chart feature, which are already mitigated by `esc()` calls for user-provided data.
- **Evidence:** `STRUCTURAL CONSTRAINTS Constraint 1: 'SECURITY may NOT object to `unsafe-inline` as a per-feature issue.'
STRUCTURAL CONSTRAINTS Constraint 2: 'SECURITY may NOT require `DOMPurify` or any server-side sanitization for individual features that use `md() + innerHTML` when that pattern is already the ap`

## Resolution

Human decision required. Resume the build after updating session_state.json.

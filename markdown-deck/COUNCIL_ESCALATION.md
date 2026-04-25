# Council Escalation — markdown-deck

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T00:02:56.248653+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The plan robustly addresses all identified correctness risks, including degenerate data ranges, negative values, data truncation, and invalid input handling, with explicit warnings and fallback mechanisms.

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly addresses XSS by escaping all user-provided text before SVG insertion and parsing values safely, adhering to existing architectural security constraints.

### UI — OBJECT (low)
- **Reason:** When an unknown chart type is specified (e.g., `chart foo`), the system silently falls back to a bar chart, which can confuse the user who expects a different type or explicit feedback.
- **Required fix:** Display a small, visible warning message below the chart (similar to the truncation or skipped lines warnings) when an unknown chart type is encountered, informing the user of the fallback to 'bar'.
- **Evidence:** `Subtask 8, point 9: "Unknown chart type — `chart foo` with no recognized type (bar/line/pie) falls back to `bar` with a console warning; no crash"`

### GUIDE — APPROVE (low)
- **Reason:** The plan includes comprehensive documentation in DECK_GUIDE.md, explicit in-app help via a <details> block, clear examples, and visible, actionable error/warning messages, ensuring high discoverability for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature addresses a clear and recurring need for users creating data-driven presentations, integrating charts directly into the markdown workflow with theme consistency.
- **Evidence:** `The ability to define simple charts inline, with automatic theme-matching, significantly reduces friction compared to generating charts externally and embedding images, making markdown-deck a more complete and useful tool for presentations.`

### COOL — APPROVE (low)
- **Reason:** The automatic theme integration for charts is a strong signature move, making them feel native to the presentation and differentiating from generic chart tools.
- **Evidence:** `Many online CSV-to-chart tools, Chart.js demos`

### LESSONS — APPROVE (low)
- **Reason:** The plan explicitly incorporates the `<details>` pattern for structured input documentation and adheres to the `CONSTRAINTS.md` for CSP, showing proactive application of documented lessons.
- **Evidence:** `Subtask 8, item 12: 'Inline `<details>` quick reference (per LESSONS advisory PLAN-escalation 2026-04-24, satisfies the port-ref `<details>` pattern KEEP rule for tools accepting structured input)...' and Security section: 'CSP unchanged (CONSTRAINTS.md)'`

## Resolution

**RESOLVED 2026-04-25. UI low fixed at source — unknown chart type now shows a visible warning row.**

### UI low — FIXED
Updated Subtask 8 item 9 and the Edge Cases entry to specify a visible warning row when an unknown chart type is encountered, matching the existing pattern for truncation/skipped-lines warnings:

> Unknown chart type — `chart foo` with no recognized type (bar/line/pie) falls back to `bar` with a **visible warning row below the chart**: `⚠ unknown chart type "{requested}" — rendered as bar`. Same `slide-chart-warn` style as the truncation/skipped-lines warnings; never silent. Console warning still emitted for debugging.

Behavior is now uniform across the three "soft fallback" cases (truncation, skipped lines, unknown type) — every silent fallback gets a visible row.

### Other 6 angles — APPROVE
BUGS, SECURITY, GUIDE, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun PLAN; expected clean pass → IMPLEMENTATION.

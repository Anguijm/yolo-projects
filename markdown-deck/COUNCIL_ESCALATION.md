# Council Escalation — markdown-deck

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T22:06:38.656807+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The baseline calculation for bar and line charts risks a division-by-zero error if all data points have the identical value and at least one is negative.
- **Required fix:** The formula for `bottom-of-plot baseline` in bar and line charts (`plotTop + plotH * (max / (max - min))`) must include a guard for `max - min == 0` when negative values are present, and specify the fallback baseline position and rendering behavior for this edge case (e.g., all values are `[-5, -5, -5]`).
- **Evidence:** `Subtask 2, Bar chart SVG section: 'bottom-of-plot baseline at y=plotTop + plotH * (max / (max - min)) when negative values are present'`

### SECURITY — APPROVE (low)
- **Reason:** Plan explicitly details robust escaping of all user-provided text (labels, title, aria-label) via `esc()` before SVG insertion, mitigating XSS within the architectural constraints.

### UI — OBJECT (medium)
- **Reason:** The plan contains conflicting descriptions for pie chart legend behavior, and the proposed 8-character truncation for pie legend labels is too aggressive, potentially leading to ambiguity.
- **Required fix:** Standardize the pie chart legend behavior to 'top 5 + an aggregate "Other (N more)" wedge' as described in DECK_GUIDE.md, and increase the pie chart legend label truncation limit from 8 to 16 characters for improved readability.
- **Evidence:** `Approach -> Subtask 2 -> Pie chart SVG (legend truncation & item count); Approach -> Subtask 8 -> DECK_GUIDE.md documentation -> item 10 (pie chart legend behavior); Edge Cases (pie legend > 8 items)`

### GUIDE — APPROVE (low)
- **Reason:** The plan includes comprehensive documentation in DECK_GUIDE.md and an inline quick reference, ensuring high discoverability for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** Inline, theme-aware charts solve a common pain point for presentation creators by streamlining data visualization and ensuring visual consistency without external tools.
- **Evidence:** `Users frequently need to embed charts in presentations; this feature eliminates the need for external chart generation, image export, and manual theme matching, making markdown-deck a more complete and efficient tool for its target audience.`

### COOL — APPROVE (low)
- **Reason:** The automatic, theme-aware color integration for charts is a strong signature move that differentiates it from generic chart tools and enhances the presentation's aesthetic coherence.
- **Evidence:** `Generic online chart generators; presentation software often requires manual styling.`

### LESSONS — APPROVE (low)
- **Reason:** The plan explicitly incorporates lessons regarding structured input documentation and architectural constraints.
- **Evidence:** `port-ref [KEEP] <details> supported-formats block for bulk input features; markdown-deck Structural Constraints`

## Resolution

Human decision required. Resume the build after updating session_state.json.

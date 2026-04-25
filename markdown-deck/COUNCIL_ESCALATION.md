# Council Escalation — markdown-deck

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T23:58:08.131466+00:00

## Angle positions

### BUGS — OBJECT (medium)
- **Reason:** The plan contains a direct contradiction regarding the pie chart legend behavior, which could lead to inconsistent implementation or misunderstanding of the feature's specification.
- **Required fix:** Update the 'Edge Cases' section to align with the 'Subtask 2: Pie chart SVG' and 'Subtask 8: DECK_GUIDE.md documentation' sections, specifying that the pie chart legend shows 'top 5 segments + Other (N more)' for a maximum of 6 entries.
- **Evidence:** `Plan sections:
- 'Subtask 2: Pie chart SVG' states: 'Legend total is always ≤ 6 entries'
- 'Subtask 8: DECK_GUIDE.md documentation' point 10 states: 'pie charts with > 6 slices show top 5 + an aggregate "Other (N more)" wedge'
- 'Edge Cases' states: 'Pie legend > 8 items → first 8 shown + +N more te`

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly calls for `esc()` on all user-provided text before SVG insertion, mitigating XSS risks; no new external content sources or dependencies are introduced, aligning with existing architectural constraints.

### UI — APPROVE (low)
- **Reason:** The plan comprehensively addresses user experience, including clear feedback for data issues, theme integration, accessibility, and excellent documentation. All prior UI escalations have been resolved.

### GUIDE — APPROVE (low)
- **Reason:** The plan includes comprehensive documentation updates and in-app discoverability features for chart blocks.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature provides a highly useful, integrated solution for quick data visualization within markdown presentations, addressing a common need for theme-aware, easily updatable charts without external dependencies.
- **Evidence:** `The 'signature move' of theme-aware charts, combined with CSV input and robust handling of edge cases (truncation, invalid data, negative values), makes this a valuable tool for anyone creating data-driven presentations from markdown. It solves the problem of integrating simple charts without breaki`

### COOL — APPROVE ()
- **Reason:** The deep theme integration makes charts feel native to the deck, providing a clear signature move for inline markdown charts within a zero-dependency context.

### LESSONS — APPROVE (low)
- **Reason:** The plan explicitly incorporates documented lessons, including the `<details>` pattern for structured input and adherence to `CONSTRAINTS.md` for CSP, demonstrating compliance with established architectural rules and anti-patterns.
- **Evidence:** `KEEP — <details> supported-formats block for bulk input features (learnings.md); KEEP — CONSTRAINTS.md pattern for CSP override (learnings.md); Constraint 1: Zero-dep single-file HTML is irreversible (markdown-deck/CONSTRAINTS.md)`

## Resolution

**RESOLVED 2026-04-25. BUGS medium fixed at source — Edge Cases entry harmonized.**

### BUGS medium — FIXED
The Edge Cases bullet on line 175 was stale leftover text from before the round-2 standardization (`df21c3a`, 2026-04-25). It still said "Pie legend > 8 items → first 8 shown + +N more text", which contradicts the canonical "top 5 + Other (N more) wedge" approach now in Subtask 2 (line 77) and Subtask 8 (line 108).

Updated to:
> Pie segments > 6 → top 5 by value shown + aggregate `Other (N more)` wedge (matches Subtask 2 + Subtask 8 standardized behavior)

Single source of truth: top 5 + Other-wedge, ≤ 6 legend entries. No more divergence between sections.

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun PLAN; expected clean pass → IMPLEMENTATION.

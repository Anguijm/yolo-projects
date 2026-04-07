# Council Escalation — naval-scribe

**Gate:** tests
**Reason:** LESSONS VETO — The 'paste block' functionality for references violates the 'document.createDocumentFragment()' lesson by performing per-element DOM appends in a loop that can exceed 50 items.
**Timestamp:** 2026-04-07T18:45:38.620420+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The implementation of the multi-entry recipient list and distribution mode toggle appears robust and correctly handles various input scenarios and rendering logic.

### SECURITY — APPROVE (low)
- **Reason:** All user-controlled data rendered into the DOM via innerHTML is consistently escaped using the `esc()` function, mitigating XSS. The CSP is restrictive, and `connect-src 'none'` prevents external data exfiltration or script loading. Potential blind spots exist in unprovided JavaScript for features like SSIC autocomplete, drafts, import, and AI prompt generation, but based on the provided code, no direct exploitable surfaces are found.

### UI — APPROVE (low)
- **Reason:** The multi-entry list and distribution mode toggle are clearly labeled, provide good affordances, and offer helpful context for first-time users.

### GUIDE — APPROVE (low)
- **Reason:** The distribution mode toggle and multi-entry recipient list are clearly labeled and include a helpful in-app hint explaining its function for Naval Instructions.
- **Evidence:** `naval-scribe/index.html:849-851 (dist-toggle label and hint)`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly addresses a specific, recurring formatting requirement for naval correspondence, enhancing the tool's core utility.
- **Evidence:** `Naval correspondence standards require specific formatting for 'Copy to' and 'Distribution' blocks, which this feature automates and differentiates.`

### COOL — APPROVE (low)
- **Reason:** The 'Distribution mode toggle' for Naval Instructions is a highly specific, niche formatting detail that serves the target audience's unique needs, making the tool unreasonably good at its one thing.

### LESSONS — OBJECT (critical) 🚫 VETO
- **Reason:** The 'paste block' functionality for references violates the 'document.createDocumentFragment()' lesson by performing per-element DOM appends in a loop that can exceed 50 items.
- **Required fix:** Modify the `parseRefsBtn` event listener to use `document.createDocumentFragment()` for batch appending reference items to `ref-list` to avoid excessive reflows.
- **Evidence:** `KEEP (conditional): `document.createDocumentFragment()` for batch DOM appends — avoids per-element reflow when populating large lists. Precondition: applies ONLY when the loop is expected to append more than ~50 elements in a single batch (e.g., paginated tables, search results, log viewers).`

## Resolution

Human decision required. Resume the build after updating session_state.json.

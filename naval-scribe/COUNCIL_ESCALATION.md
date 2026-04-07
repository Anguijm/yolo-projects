# Council Escalation — naval-scribe

**Gate:** tests
**Reason:** LESSONS VETO — The `setValues` method for multi-field lists performs batch DOM manipulations without using `document.createDocumentFragment()`, violating a documented lesson to avoid reflows.
**Timestamp:** 2026-04-07T10:53:31.278511+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The implementation correctly handles multi-entry lists, distribution mode toggle, and includes robust parsing/migration for persistence and import, with proper HTML escaping.

### SECURITY — OBJECT (high)
- **Reason:** The `renderPreview` function is truncated, specifically for the 'moa' document type, where user-controlled data from 'Parties to Agreement' (obtained via `getParties()`) would be rendered; without the full code, it cannot be confirmed that all user input is properly HTML-escaped before being inserted into `previewPage.innerHTML`, leading to a potential Cross-Site Scripting (XSS) vulnerability, which is critical given the `script-src 'unsafe-inline'` CSP.
- **Required fix:** Ensure all user-controlled data from `d.parties` (org, serial, name, rank, title) is passed through the `esc()` function before being inserted into `previewPage.innerHTML` for MOA type documents.
- **Evidence:** `file:index.html (truncated `renderPreview` function, specifically `case 'moa'`) and `getData()` function which includes `parties: getParties()``

### UI — APPROVE (low)
- **Reason:** The multi-entry list and distribution mode toggle are clearly designed with good affordances and immediate preview feedback.

### GUIDE — APPROVE (low)
- **Reason:** The tool provides excellent in-app help, clear naming, and detailed instructions for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** The multi-entry list and distribution mode toggle directly address common formatting requirements for naval correspondence, streamlining a frequent and necessary task for the target user base.
- **Evidence:** `Naval correspondence standards (e.g., SECNAV M-5216.5) mandate specific formatting for 'Copy to' and 'Distribution' blocks, making this a core utility for anyone drafting official documents.`

### COOL — APPROVE (low)
- **Reason:** The 'Distribution mode' toggle is a niche, specific detail that reinforces the tool's deep understanding of naval correspondence, contributing to its overall unique value proposition.

### LESSONS — OBJECT (high) 🚫 VETO
- **Reason:** The `setValues` method for multi-field lists performs batch DOM manipulations without using `document.createDocumentFragment()`, violating a documented lesson to avoid reflows.
- **Required fix:** Modify the `setValues` function within `makeMultiField` (and similar batch update logic for `partyItems` if applicable) to utilize `document.createDocumentFragment()` for appending multiple elements, thereby reducing DOM reflows.
- **Evidence:** `KEEP: `document.createDocumentFragment()` for batch DOM appends in paginated tables — avoids reflow on each row. (from [unicode-char] learnings.md)`

## Resolution

Human decision required. Resume the build after updating session_state.json.

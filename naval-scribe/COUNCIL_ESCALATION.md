# Council Escalation — naval-scribe

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T06:44:55.830578+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The `applyTemplate` function calls `restoreParties([])` and accesses `byDirectionChk` and `actingChk` without these being defined, leading to `ReferenceError` and preventing template application.
- **Required fix:** 1. Define `restoreParties` function to clear and set party fields. 2. Declare and assign `byDirectionChk` and `actingChk` variables (e.g., `var byDirectionChk = document.getElementById('f-by-direction');`) at the top of the script.
- **Evidence:** `file:index.html:1900-1901,1904`

### SECURITY — APPROVE (low)
- **Reason:** The Template Letter Library feature is implemented securely, utilizing textContent for rendering static template data and adhering to existing input sanitization (esc()) for user-modifiable fields. Mutual exclusion of drawers is complete, and structural constraints regarding unsafe-inline and localStorage are acknowledged.

### UI — APPROVE (low)
- **Reason:** The Template Letter Library offers a clear, well-afforded, and frictionless experience with excellent feedback on data changes.

### GUIDE — APPROVE (low)
- **Reason:** Template Letter Library is highly discoverable with clear naming, in-app help, and comprehensive AI documentation.

### USEFULNESS — APPROVE (low)
- **Reason:** The template library directly addresses a frequent need for structured, pre-filled correspondence, significantly boosting user efficiency and ensuring correct starting formats.
- **Evidence:** `Users of document generation tools consistently prioritize templates for common document types, making this a core utility feature for a correspondence tool.`

### COOL — APPROVE (low)
- **Reason:** The template library directly reinforces the project's core identity as a reliable, specialized tool for naval correspondence, offering valuable starting points and a thoughtful confirmation flow.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The deliverable violates the 'No innerHTML with user data' lesson by using `previewPage.innerHTML` with partially escaped user content.
- **Required fix:** Refactor the `renderPreview` function to avoid setting `innerHTML` directly with user-provided data. Instead, use `DOMParser` and `textContent` or `createElement` for all user-controlled text, similar to the pattern established in `svg-fields` for safe rendering.
- **Evidence:** `KEEP: SVG templates as data-driven forms — `{{mustache}}` + `data-field="name"` markers extracted in document order become a left-column form. Live preview re-renders via DOMParser + textContent for data-field subs, direct string replace for mustache. No innerHTML with user data.`

## Resolution

Human decision required. Resume the build after updating session_state.json.

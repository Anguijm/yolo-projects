# Council Escalation — naval-scribe

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T01:20:42.741826+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The plan includes a robust confirmation gate and explicit field clearing, mitigating risks of accidental data overwrite or inconsistent state.

### SECURITY — OBJECT (high)
- **Reason:** The plan does not explicitly state that template labels and descriptions, or the new AI prompt content, will be properly escaped or rendered via `textContent` when injected into the DOM, creating a potential XSS vulnerability if `innerHTML` is used directly.
- **Required fix:** Ensure that all dynamic content, specifically `TEMPLATE_LIBRARY.label` and `TEMPLATE_LIBRARY.desc` when rendered by `renderTmplDrawer()`, and the new AI prompt content, are either inserted using `textContent` or are explicitly escaped via `esc()` before being assigned to `innerHTML`.
- **Evidence:** `Subtask 4 — JS: renderTmplDrawer()
Subtask 7 — AI prompt update`

### UI — APPROVE (low)
- **Reason:** The plan demonstrates a thorough understanding of user experience, providing clear affordances, a frictionless flow for empty states, and a well-designed inline confirmation for non-empty states.

### GUIDE — APPROVE (low)
- **Reason:** The plan explicitly details all user-facing text, button labels, hints, and an update to the AI prompt documentation, ensuring high discoverability for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly enhances the core utility of naval-scribe by providing immediate access to frequently used document structures, significantly speeding up drafting for common correspondence types.
- **Evidence:** `The 12 proposed templates cover highly common administrative and operational documents (e.g., Leave Request, Status Report, Point Paper) that users would otherwise have to type from scratch or copy-paste, aligning perfectly with the project's goal of providing a fast and reliable tool for naval offi`

### COOL — APPROVE (low)
- **Reason:** The template library directly reinforces naval-scribe's identity as a specialized, efficient, and reliable tool for naval correspondence by providing common, pre-formatted document starting points, aligning with the project's utility-flagship constraint.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The plan's confirmation gate for overwriting existing form content does not follow the documented 'WILL CHANGE / WILL CLEAR / WILL KEEP' pattern, which requires explicitly listing affected fields.
- **Required fix:** Modify the plan to include a detailed confirmation message that explicitly lists the fields that will be changed or cleared, using the 'WILL CHANGE / WILL CLEAR / WILL KEEP' structure, as required for destructive actions.
- **Evidence:** `INSIGHT — WILL CHANGE / WILL CLEAR / WILL KEEP pattern for destructive actions: When a feature overwrites or clears existing user data (body text, field sets), the preview drawer must explicitly list every affected field in three named sections. This is both a UX requirement (informed consent) and a`

## Resolution

**RESOLVED 2026-04-24. Both concerns addressed in plan.md.**

### SECURITY (high) — ACCEPTED
Plan now explicitly documents safe-rendering for TEMPLATE_LIBRARY content (Subtask 4): all author-controlled strings (`tpl.label`, `tpl.desc`, category headers) are injected via `createElement` + `.textContent` assignment, never raw innerHTML with template content. Subtask 7 notes that `#ai-prompt-content` is static HTML with no dynamic substitution — no user-controlled path.

### LESSONS advisory (auto-downgraded) — ACCEPTED
Plan's overwrite confirmation expanded into the WILL CHANGE / WILL CLEAR / WILL KEEP pattern (Subtask 5) matching the Reply Draft Auto-Fill precedent:
- **WILL CHANGE** — template-defined fields (type, subj, body-family)
- **WILL CLEAR** — fields emptied for coherence (from/to/ssic/date/via/ref/encl/copyTo/sig/etc.)
- **WILL KEEP** — classification marking + letterhead preset

Items rendered via `<ul>` + `.textContent = fieldName` — no innerHTML with field data. UI and Guide sections updated to reflect the new disclosure structure.

### Other 5 angles — APPROVE
BUGS, UI, GUIDE, USEFULNESS, COOL all clean.

Cron may rerun PLAN; expected clean pass.

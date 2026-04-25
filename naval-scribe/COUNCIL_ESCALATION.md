# Council Escalation — naval-scribe

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T05:43:15.857666+00:00

## Angle positions

### BUGS — OBJECT (medium)
- **Reason:** The plan lacks precise definitions for parsing body paragraphs and for 'non-empty' checks, which could lead to incorrect quality check results for the advisory panel.
- **Required fix:** For 'Body Para 1 Numbering', explicitly define the method for splitting paragraphs (e.g., regex for blank lines) and the exact string matching for '1.'. For 'From and To Filled' and 'Signature Block', clarify that 'non-empty' means `value.trim().length > 0`. For 'Classification Marking', explicitly state the failure condition as `classSel.value === "" || classSel.value === "No Marking"`.
- **Evidence:** `Subtask 3 — Quality checker JS: Rules 4, 5, 6, 7`

### SECURITY — OBJECT (high)
- **Reason:** The plan does not explicitly state that error messages displayed in `#draft-io-msg` will be sanitized or escaped before being written to the DOM, creating a potential XSS vulnerability if user-controlled strings (e.g., stripped key names from imported JSON) are included in error messages.
- **Required fix:** Ensure all content displayed in `#draft-io-msg` that originates from user-controlled input (e.g., stripped key names from imported JSON via `validateImportSchema`) is properly sanitized or escaped (e.g., using `esc()` or `textContent`) before being written to the DOM.
- **Evidence:** `Subtask 4 — Portable Export/Import JS: `validateImportSchema(obj)` states 'Any key not in whitelist → stripped (silent)' and 'Type mismatch → strip key, add to errors'. The `importDraftFile.change` handler then 'show success/error in `#draft-io-msg`'. The plan does not specify how these error messag`

### UI — APPROVE (low)
- **Reason:** The plan outlines clear, consistent UI elements and flows for both features, with good feedback and minimal friction.

### GUIDE — APPROVE (low)
- **Reason:** The plan thoroughly addresses discoverability through clear naming, in-app help, and actionable error messages for both features.

### USEFULNESS — APPROVE (low)
- **Reason:** Both features directly address core user needs: ensuring document compliance and providing essential data portability/backup for critical work.
- **Evidence:** `Quality checker solves the problem of manual, error-prone naval formatting checks. Export/Import solves the problem of data loss from localStorage and enables draft transfer between devices, which is a fundamental requirement for any serious productivity tool.`

### COOL — APPROVE (low)
- **Reason:** The features directly reinforce Naval Scribe's core identity as a specialized, zero-dependency utility, enhancing its reliability and conformance to naval standards.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The plan for Portable Draft Import violates the documented lesson requiring a <details> block for supported input formats, which previously led to a high-severity GUIDE objection.
- **Required fix:** Add a <details> element near the import button or within the import status area, explicitly listing the .navalscribe.json schema requirements (e.g., _navalscribe_version: "1", whitelisted top-level keys, and their expected types) as per the validateImportSchema function.
- **Evidence:** `KEEP — <details> supported-formats block for bulk input features — When a tool accepts structured text input (YAML, JSON, CSV), add a <details> element listing supported input formats. Satisfies GUIDE at the OUTCOME gate without cluttering the primary UI; GUIDE flagged the absence of explicit format`

## Resolution

Human decision required. Resume the build after updating session_state.json.

# Council Escalation — naval-scribe

**Gate:** plan
**Reason:** LESSONS VETO — The plan proposes script changes in naval-scribe/index.html but does not include a step to recompute and update the CSP script-src SHA-256 hash, which is a documented requirement after any script modification.
**Timestamp:** 2026-04-07T08:06:20.545876+00:00

## Angle positions

### BUGS — OBJECT (medium)
- **Reason:** Imported data from older formats where 'copyTo' was a single string will not be correctly parsed into multiple entries, leading to data misinterpretation.
- **Required fix:** The 'Import apply' section must include the same migration logic as 'restoreFullState' to handle 'p.copyTo' being a string or an array, ensuring old string-based imports are correctly split into multiple fields.
- **Evidence:** `Plan section 'Import apply': `copyToFields.setValues(p.copyTo)` vs. 'restoreFullState': `copyToFields.setValues(typeof s.copyTo === 'string' ? s.copyTo.split('\n').filter(Boolean) : (Array.isArray(s.copyTo) ? s.copyTo : []))``

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly addresses potential XSS and XML injection by leveraging existing, presumably robust, escaping functions (`esc()`, `makeParagraph()`) and safe DOM manipulation (`input.value`) for all user-controlled input, including imported data.

### UI — OBJECT (medium)
- **Reason:** The critical hint explaining the 'distribution mode' checkbox might not be sufficiently associated with the checkbox itself, potentially causing initial confusion for first-time users.
- **Required fix:** Ensure the hint 'For Naval Instructions — replaces Copy to: with Distribution: block' is visually and semantically tied directly to the 'distribution mode' checkbox (e.g., as part of the label, or using aria-describedby) rather than being a separate general hint.
- **Evidence:** `HTML Changes, points 1 and 2 regarding the distribution toggle layout and hint placement.`

### GUIDE — APPROVE (low)
- **Reason:** The plan includes excellent discoverability features like a clear hint for the distribution toggle and explicit data structures for AI agents.
- **Evidence:** `Plan: Distribution / Copy-To Block (v2)`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly addresses specific, recurring formatting and data entry problems for the target user base (Navy personnel drafting official instructions), improving compliance and efficiency.
- **Evidence:** `The plan explicitly mentions 'For Naval Instructions' and 'matches actual DON instruction formatting,' indicating a clear, real-world, and recurring use case for specific document types.`

### COOL — APPROVE (low)
- **Reason:** The explicit signature move of accurately rendering the 'Distribution:' block with specific, indented formatting for Naval Instructions provides strong differentiation and a 'nice' moment for the target user.

### LESSONS — OBJECT (high) 🚫 VETO
- **Reason:** The plan proposes script changes in naval-scribe/index.html but does not include a step to recompute and update the CSP script-src SHA-256 hash, which is a documented requirement after any script modification.
- **Required fix:** Add an explicit step to the plan to recompute and update the CSP script-src SHA-256 hash in naval-scribe/index.html after the proposed JavaScript changes are implemented.
- **Evidence:** `KEEP: CSP `script-src` SHA-256 hash must be recomputed after every script change (from [ip-cidr] learnings.md)`

## Resolution

Human decision required. Resume the build after updating session_state.json.

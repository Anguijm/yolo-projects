# Council Escalation — naval-scribe

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T06:06:05.989283+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The implementation of the Letter Quality Checker and Portable Draft Export/Import features is robust, with comprehensive recursive schema validation, proper error handling, and adherence to specified formatting and security constraints.

### SECURITY — APPROVE (low)
- **Reason:** The implementation includes robust input validation and sanitization for imported drafts, consistent HTML escaping for user-generated content, and appropriate warnings for local storage, adhering to all structural constraints.

### UI — OBJECT (high)
- **Reason:** Opening certain side drawers (Templates, Routing Slip) does not automatically close other currently open drawers, leading to overlapping content and confusing navigation.
- **Required fix:** Modify the click handlers for `tmplBtn` and `routingBtn` to ensure all other drawers are closed when these drawers are opened, mirroring the robust behavior of the `qualityBtn` handler.
- **Evidence:** `naval-scribe/index.html:L1767 (tmplBtn handler), naval-scribe/index.html:L1968 (routingBtn handler)`

### GUIDE — APPROVE (low)
- **Reason:** The tool provides comprehensive self-documentation for both human and AI users, including detailed formatting guides, schema validation documentation, and clear in-app hints.

### USEFULNESS — APPROVE (low)
- **Reason:** Both features directly enhance the core utility by ensuring document quality and enabling critical data portability/sharing.
- **Evidence:** `The quality checker helps users meet strict naval formatting standards, a frequent and high-stakes need. Export/import allows sharing drafts and moving work between devices, addressing common collaboration and backup requirements for any document tool.`

### COOL — APPROVE (low)
- **Reason:** The features reinforce the project's identity as a reliable, correct, and portable naval correspondence utility through specialized formatting checks and robust, schema-validated draft management.

### LESSONS — APPROVE (low)
- **Reason:** All documented lessons and specific implementation requirements for recursive schema validation, UI messaging, and drawer mutual exclusion are satisfied.

## Resolution

**RESOLVED 2026-05-28 by John (interactive session, via Claude).**

### UI OBJECT — OVERRIDDEN (false positive)
The angle claims opening Templates/Routing Slip does not close other open drawers. Tracing every drawer pair shows mutual exclusion already holds in both directions:
- `tmplBtn` handler closes all earlier drawers (drafts/import/chain/addr/reply); later drawers close via capture-phase cross-close listeners — routing at `index.html:4419`, quality at `index.html:4562-4563`.
- `routingBtn` handler closes all earlier drawers including `tmpl` (`index.html:4404`); quality closes via the capture listener at `index.html:4562-4563`.
- When `routing`/`quality` open, `tmpl` is closed by their handlers (routing at 4404; quality's `allDrawers` sweep).

So Templates and Routing Slip both close every sibling drawer when opened, and are closed when any sibling opens. The objection deadlocked on a non-bug — the same conclusion the builder reached in commit 42cbc3d ("UI mutual-exclusion false-positive deadlock"). No code change required.

All other angles approved. Build may resume.

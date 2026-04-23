# Council Escalation — naval-scribe

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T10:17:07.720412+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** Draft IDs generated using `Date.now()` are not guaranteed to be unique, which can lead to multiple drafts having the same ID, causing status updates or deletions to affect the wrong entry or fail silently for duplicates.
- **Required fix:** Replace `Date.now()` with a robust unique ID generation mechanism (e.g., UUID) when saving drafts to prevent collisions and ensure correct targeting of individual draft entries for status changes and deletions.
- **Evidence:** `saveDraftBtn.addEventListener('click', function() { ... arr.unshift({ id: Date.now(), name: name.trim(), ... }); ... });`

### SECURITY — APPROVE (low)
- **Reason:** The implementation correctly uses escaping functions (esc, escXml) for all user-controlled data before rendering to HTML or generating DOCX, mitigating injection risks. LocalStorage usage is consistent with architectural constraints, and the address book includes a user-facing warning. The CSP, while using 'unsafe-inline' as per architectural constraint, is otherwise restrictive, limiting other attack vectors.

### UI — APPROVE (low)
- **Reason:** The status tracking feature is clear, provides good visual feedback, and handles various states effectively, with addressed accessibility concerns.

### GUIDE — APPROVE (low)
- **Reason:** The new status tracking feature is highly discoverable with clear UI elements, tooltips, and comprehensive documentation for AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature provides practical, recurring utility for managing the lifecycle of official correspondence, directly addressing a common organizational need for the target user.
- **Evidence:** `Users of formal correspondence tools frequently need to track the progress of documents through various stages (drafting, review, signing, transmission, reply). This feature provides an integrated, quick-glance solution for this, eliminating the need for external tracking or opening each document to`

### COOL — APPROVE (low)
- **Reason:** The status tracker enhances the tool's core utility by providing practical workflow management for drafts, reinforcing its identity as a comprehensive and reliable naval correspondence flagship.

### LESSONS — APPROVE (low)
- **Reason:** All documented lessons, including the requirement to update the AI prompt, have been satisfied.

## Resolution

**RESOLVED 2026-04-24 by John (interactive session). BUGS fixed at source with `crypto.randomUUID()`.**

### BUGS OBJECT (high) — FIXED
Legitimate in principle. `Date.now()` collision requires two saves in the same millisecond — physically impossible via human clicks, but the correctness argument stands and the fix is one helper function.

**Fix applied** (naval-scribe/index.html, around line 2473):
```js
function uniqueDraftId() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return String(Date.now()) + '-' + Math.random().toString(36).slice(2, 10);
}
```

`saveDraftBtn` click handler now uses `uniqueDraftId()` instead of `Date.now()`. 122 bits of randomness via RFC 4122 UUID — collision-proof at any realistic draft volume. Graceful fallback for pre-`crypto.randomUUID` environments.

**Backward compatibility**: existing drafts with numeric `Date.now()` IDs continue to work. All lookups (`setDraftStatus`, delete filter) use strict `===` equality, so old numeric IDs match old entries and new string UUIDs match new entries — no cross-type confusion.

Plan.md Subtask 2 updated to document the helper and rationale.

### Other 6 angles — all APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean. LESSONS explicitly confirmed: *"All documented lessons, including the requirement to update the AI prompt, have been satisfied."* → the ai-prompt-content subtask from the prior PLAN resolution stuck.

Cron may rerun IMPLEMENTATION; expected clean pass → TESTS → OUTCOME → ship.

# Council Escalation — naval-scribe

**Gate:** tests
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T19:39:22.502443+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The implementation for generating draft IDs does not use `crypto.randomUUID()` as stated in the council focus, potentially leading to ID collisions and incorrect status tracking for drafts.
- **Required fix:** Change the draft ID generation to use `crypto.randomUUID()` to ensure collision-safe identifiers.
- **Evidence:** `file:2320 (id: Date.now() + Math.random().toString(36).substr(2, 9),) -- contradicts council focus: 'crypto.randomUUID() for collision-safe IDs'`

### SECURITY — APPROVE (low)
- **Reason:** The new Letter Status Tracker feature adheres to existing security patterns, utilizes proper escaping for user-controlled content, and introduces no new attack surfaces or data exposure beyond the established architectural constraints.

### UI — APPROVE (low)
- **Reason:** The Letter Status Tracker provides clear affordances, good visual feedback, and strong accessibility features for managing draft lifecycles.

### GUIDE — APPROVE (low)
- **Reason:** The Letter Status Tracker is well-documented in the AI prompt, and its UI elements are clearly named and visually discoverable.

### USEFULNESS — APPROVE (low)
- **Reason:** The letter status tracker provides essential workflow management for users handling multiple official documents, enhancing the tool's utility and daily use.
- **Evidence:** `Supports common document lifecycle stages (Draft, Signed, Transmitted, Replied) and enables efficient filtering for recurring tasks, directly addressing a core need for the target user managing correspondence.`

### COOL — APPROVE (low)
- **Reason:** The Letter Status Tracker provides a domain-specific workflow enhancement (Draft→Signed→Transmitted→Replied) that reinforces the tool's identity as a comprehensive utility for naval correspondence, offering a practical and intuitive way to manage document lifecycles.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or architectural constraints were violated by the current deliverable.

## Resolution

**RESOLVED 2026-04-24 — BUGS overridden as hallucinated.**

### BUGS OBJECT (high) — OVERRIDE (false positive, 2nd in a row)
The objection claims draft IDs use `Date.now() + Math.random().toString(36).substr(2, 9)` and cites `file:2320`. Both are wrong:

1. **Method mismatch**: actual code uses `.slice(2, 10)` (10 chars), not `.substr(2, 9)` (9 chars).
2. **Location wrong**: the fallback construct lives inside `uniqueDraftId()` at the top of the drafts section, not line 2320.
3. **Missed primary path**: the cited fallback only runs when `crypto.randomUUID` is unavailable. All modern browsers have it, so in practice the function always returns a UUID.

```js
function uniqueDraftId() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();  // ← primary path
  }
  return String(Date.now()) + '-' + Math.random().toString(36).slice(2, 10);
}
```

Cron is hallucinating both the evidence string and the absence of the UUID path. Overridden.

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean. LESSONS explicitly: "No documented lessons or architectural constraints were violated by the current deliverable."

Cron may rerun TESTS; expected clean pass → OUTCOME → ship.

# Council Escalation — naval-scribe

**Gate:** tests
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T19:30:47.497211+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** Status updates can fail silently due to localStorage quota limits because the error message for status changes relies on a variable that is never updated by the status update logic.
- **Required fix:** The `cycleDraftStatus` function, or a helper it calls, must explicitly catch `QuotaExceededError` during `localStorage.setItem` and set the `lastStatusError` variable, which is displayed to the user in the drafts drawer.
- **Evidence:** `file:index.html
```javascript
// In saveDraftsData() (called by cycleDraftStatus)
// This sets 'lastSaveError', not 'lastStatusError'
} catch (e) {
  if (e.name === 'QuotaExceededError' || e.name === 'NS_ERROR_DOM_QUOTA_REACHED') {
    lastSaveError = 'Storage full \u2014 could not save draft.';
  }`

### SECURITY — APPROVE (low)
- **Reason:** The new feature does not introduce new attack surfaces. Existing robust escaping mechanisms for user input, combined with a restrictive Content Security Policy (connect-src 'none', object-src 'none', form-action 'none'), mitigate potential risks. Local storage warnings are in place per architectural constraints. Crypto.randomUUID() is used appropriately.

### UI — OBJECT (medium)
- **Reason:** When a status filter is applied in the drafts drawer and no drafts match, the UI provides no specific feedback, leaving the user unsure if there are no drafts or just no matching ones.
- **Required fix:** Modify the drafts rendering logic to display a 'No drafts match this filter' message when a filter is active and the filtered list is empty, distinct from the 'No saved drafts yet' message.
- **Evidence:** `Interaction: Open drafts drawer, save a draft, then apply a status filter for which no drafts currently exist. The list area will be empty without explanation.`

### GUIDE — APPROVE (low)
- **Reason:** The Letter Status Tracker is well-documented for both human users and AI agents, with clear in-app hints and accessible controls.

### USEFULNESS — APPROVE (low)
- **Reason:** The status tracker provides practical lifecycle management for saved drafts, enhancing the utility of the drafts drawer for users handling multiple documents.
- **Evidence:** `Integrates a common organizational need (document lifecycle tracking) directly into the tool, reducing context switching and external dependencies for users managing multiple pieces of correspondence.`

### COOL — APPROVE (low)
- **Reason:** The letter status tracker provides a domain-specific workflow enhancement that reinforces naval-scribe's identity as a comprehensive, single-file utility for formal correspondence, without needing a generic 'signature move' per project constraints.

### LESSONS — APPROVE (low)
- **Reason:** All documented lessons regarding code patterns, architectural constraints, and documentation updates have been adhered to.

## Resolution

**RESOLVED 2026-04-24. BUGS overridden as false positive, UI fixed.**

### BUGS OBJECT (high) — OVERRIDE (false positive)
Objection describes a function `cycleDraftStatus` that doesn't exist in the codebase. The actual function is `setDraftStatus` at `index.html:2387`, and it DOES set `lastStatusError` on quota errors:

```js
// line 2400-2402
try {
  // ... write ...
  lastStatusError = ''; // success clears
} catch(e) {
  if (e.name === 'QuotaExceededError' || e.name === 'NS_ERROR_DOM_QUOTA_REACHED') {
    lastStatusError = 'storage';
  } else {
    lastStatusError = 'storage';
    console.warn('setDraftStatus failed:', e);
  }
  return false;
}
```

The badge click handler (line 2467+) reads `lastStatusError` and branches on `'storage' | 'not-found'` for the right message. Feature works as the objection demands — the objection is hallucinating a bug that isn't there. Overridden.

### UI OBJECT (medium) — FIXED
Real bug. The prior empty-state logic used `'No ' + statusFilter + ' drafts.'` which produced "No all drafts." when `statusFilter='all'` and the list was empty, instead of the intended "No saved drafts yet." message.

**Fix**: empty-state now branches on whether drafts exist at all AND whether a filter is active:
- `drafts.length === 0` → "No saved drafts yet."
- `statusFilter === 'all'` and empty filtered list (unreachable given the prior branch, but defensive) → "No saved drafts yet."
- `statusFilter ≠ 'all'` and empty → 'No drafts match the "[Status]" filter.'

Clear differentiation — user knows whether to clear the filter or save a new draft.

### Other 5 angles — APPROVE
SECURITY, GUIDE, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun TESTS; expected clean pass → OUTCOME → ship.

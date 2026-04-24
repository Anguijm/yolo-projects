# Council Escalation — naval-scribe

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T22:33:09.514803+00:00

## Angle positions

### BUGS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: goalpost move, 0.50 overlap vs prior bugs objection] The routing slip reviewer chain, suspense date, and drafter information are not persisted across page loads, leading to data loss.
- **Required fix:** Modify `getFullState` to serialize `routingReviewers` (name and action), `routingSuspense.value`, and `routingDrafter.value` into the application state. Modify `restoreFullState` to clear existing reviewer DOM elements, then reconstruct the reviewer chain by calling `addRoutingReviewer` for each saved entry, and restore the suspense date and drafter fields.
- **Evidence:** `The `routingReviewers` array, `routingSuspense` input, and `routingDrafter` input are not referenced in the `getFullState` or `restoreFullState` functions (which are partially elided but their structure can be inferred from `loadSaved` and other field handling), meaning their state is not saved to o`

### SECURITY — OBJECT (low)
- **Reason:** The Routing Slip data (reviewer chain, suspense date, drafter) is stored in localStorage, but the Routing Slip drawer does not display the required user-facing disclaimer about local storage, which violates the project's structural constraints.
- **Required fix:** Add a disclaimer 'Stored locally on this device. Not synced. Not encrypted.' to the Routing Slip drawer, similar to the disclaimers in the Drafts and Address Book drawers.
- **Evidence:** `naval-scribe/index.html:1052 (missing element after the intro text within #routing-drawer)`

### UI — APPROVE (low)
- **Reason:** The routing slip generator provides a clear, intuitive flow with good affordances, live preview, and attention to accessibility.

### GUIDE — APPROVE (low)
- **Reason:** The routing slip generator is highly discoverable with clear UI elements, helpful hints, a live preview, and comprehensive AI documentation.

### USEFULNESS — APPROVE (low)
- **Reason:** This feature directly addresses a frequent and critical need for the target user base, streamlining a common administrative task.
- **Evidence:** `Naval correspondence frequently requires routing slips for review and signature. This tool provides a structured way to generate these, integrating with the main document's subject and exporting to the required .docx format, making it a highly practical and recurring-use tool for any naval officer o`

### COOL — APPROVE (low)
- **Reason:** The routing slip generator directly reinforces the project's core identity as a comprehensive, accurate, zero-dependency tool for naval correspondence by adding another specialized, correctly formatted document type.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or architectural constraints were violated by the deliverable. The fix for the prior BUGS OUTCOME objection aligns with best practices for data serialization.

## Resolution

**RESOLVED 2026-04-25. SECURITY low fixed at source; BUGS goalpost-downgrade noted.**

### SECURITY low — FIXED
Added `<div id="routing-disclaimer">` with the standard `Stored locally on this device. Not synced. Not encrypted.` text inside `#routing-drawer`, right after the intro line — matching the pattern from `#drafts-disclaimer` (line 543) and `#addr-disclaimer` (line 587). Same `font-size:0.42rem;color:#555;margin-bottom:8px` styling as `#drafts-disclaimer`.

### BUGS advisory (auto-downgraded) — N/A
This round's BUGS objection was a goalpost-move from the prior round's TESTS BUGS-critical, which was already fixed at source in 5d78f04 (`getFullState` / `restoreFullState` now persist `routing: { suspense, drafter, reviewers[] }`). Auto-downgrade fired correctly (0.50 overlap).

### Other 5 angles — APPROVE
UI, GUIDE, USEFULNESS, COOL, LESSONS all clean.

7/7 naval-scribe tests pass.

Cron may rerun OUTCOME; expected clean pass → ship.

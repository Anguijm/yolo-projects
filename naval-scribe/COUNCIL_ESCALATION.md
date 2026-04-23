# Council Escalation — naval-scribe

**Gate:** tests
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T19:03:45.890984+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The `saveAddr` function throws an unhandled error on non-QuotaExceededError localStorage failures, which can crash the application instead of gracefully handling the persistence error.
- **Required fix:** Modify the `saveAddr` function to catch all localStorage errors, log them, and return `false`, consistent with `saveDraftsData` and `savePresetsData`.
- **Evidence:** `file:line 2671:       throw e;`

### SECURITY — APPROVE (low)
- **Reason:** The application adheres to its structural constraints, including 'unsafe-inline' and localStorage usage, and employs robust escaping for all user-controlled output to HTML and XML contexts, mitigating injection risks. The new feature introduces no new attack surfaces.

### UI — OBJECT (high)
- **Reason:** Interactive status badges lack proper semantic HTML or ARIA attributes, making them inaccessible for keyboard-only users.
- **Required fix:** Implement status badges as `<button>` elements or add `role="button"`, `tabindex="0"`, and descriptive `aria-label`s indicating their current status and next action. Additionally, ensure all new interactive elements, including filter buttons and status badges, have visible focus indicators.
- **Evidence:** `The `.status-badge` CSS class describes an interactive element without corresponding semantic HTML or ARIA attributes; explicit focus styles are missing for new interactive elements in the provided CSS.`

### GUIDE — APPROVE (low)
- **Reason:** The tool provides comprehensive self-documentation for both human users and AI agents, with clear in-app hints, descriptive naming, and explicit formatting guides.

### USEFULNESS — APPROVE (low)
- **Reason:** The Letter Status Tracker provides practical, recurring utility for managing the lifecycle of formal correspondence within the tool, directly addressing an organizational need for the target user.
- **Evidence:** `Users managing multiple drafts of naval correspondence will frequently need to track their progress from creation to final disposition, making this a daily-use feature for active users.`

### COOL — APPROVE (low)
- **Reason:** The status tracker reinforces naval-scribe's identity as a comprehensive, zero-dependency utility for naval correspondence, adding practical workflow management without compromising its core values.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

**RESOLVED 2026-04-24 by John (interactive session). Both concerns fixed.**

### BUGS OBJECT (high) — FIXED
Consistency fix. `saveAddr` now returns `false` on all localStorage failures (same pattern as `saveDraftsData` and `savePresetsData`) instead of rethrowing on non-quota errors. Error is logged to `console.warn` and surfaced via `addrAddErr.textContent`. Caller treats false as a soft failure.

### UI OBJECT (high) — FIXED
Status badges and filter buttons are already rendered as `<button>` elements with `aria-label` attributes (the cron objection was partially incorrect on semantics). **But the focus-styles concern was legitimate** — no `:focus` or `:focus-visible` indicator was defined, so keyboard users had no visible feedback.

Added dedicated focus styles:
```css
.status-filter-btn:focus, .status-filter-btn:focus-visible,
.status-badge:focus, .status-badge:focus-visible {
  outline: 2px solid #0ff;
  outline-offset: 2px;
  box-shadow: 0 0 0 1px #0ff inset;
}
```

Accent cyan outline + offset gives clear focus without clashing with the existing color scheme.

### Other 5 angles — APPROVE
SECURITY, GUIDE, USEFULNESS, COOL, LESSONS all clean. LESSONS approved cleanly this round (no veto attempt).

`test_project.py` passes 7/7 on naval-scribe after edits.

Cron may rerun TESTS gate; expected clean pass → OUTCOME → ship.

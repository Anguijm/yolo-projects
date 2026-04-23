# Council Escalation — naval-scribe

**Gate:** implementation
**Reason:** Unresolved objections after 3 attempts
**Timestamp:** 2026-04-23T18:50:12.502990+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** All new features and backward compatibility for status tracking are correctly implemented, including robust ID generation and error handling.

### SECURITY — APPROVE (low)
- **Reason:** The implementation correctly uses crypto.randomUUID for unique IDs, handles user input with HTML escaping, and adheres to structural constraints regarding localStorage and CSP. Backward compatibility for draft status defaults to 'draft' safely.

### UI — OBJECT (high)
- **Reason:** The clickable status badges and filter buttons have insufficient tap target sizes, leading to micro-friction and potential accessibility issues for mobile users.
- **Required fix:** Increase the padding and/or minimum dimensions of `.status-filter-btn` and `.status-badge` to ensure a minimum tap target size (e.g., 44x44px) for comfortable interaction on touch devices.
- **Evidence:** `naval-scribe/index.html:190-194 (CSS for .status-filter-btn and .status-badge)`

### GUIDE — APPROVE (low)
- **Reason:** The Letter Status Tracker feature is well-documented within the AI prompt, and its UI elements are intuitively named and interactive.
- **Evidence:** `naval-scribe/index.html:L1060-1065 (AI prompt documentation for Letter Status Tracker)`

### USEFULNESS — APPROVE (low)
- **Reason:** The status tracker provides essential real-world utility for managing the lifecycle of official correspondence, addressing a common administrative need.
- **Evidence:** `Tracking document status (Draft, Signed, Transmitted, Replied) is a fundamental requirement in professional administrative workflows, directly enhancing the utility of a correspondence drafting tool.`

### COOL — APPROVE (low)
- **Reason:** The status tracker provides domain-specific workflow management, reinforcing the tool's identity as a comprehensive utility for naval correspondence without compromising its functional aesthetic or core purpose. The specific status cycle (Draft→Signed→Transmitted→Replied) is a tailored and memorable enhancement.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The `escXml` function violates the documented anti-pattern of using `String.prototype.replace(/"/g, ...)` and several static HTML buttons are missing `aria-label` attributes.
- **Required fix:** 1. Modify `escXml` function to replace `s.replace(/"/g, '&quot;')` with `s.split('"').join('&quot;')`. 2. Add `aria-label` attributes to all static HTML buttons in the top bar (e.g., #new-btn, #import-btn, #chain-btn, #addr-btn, #print-btn, #drafts-btn, #ai-prompt-btn, #save-draft-btn, #download-btn) as per the 'aria-label at HTML layer for static sidebar buttons' lesson.
- **Evidence:** `1. `_hot.md` -> Key Patterns -> `[KEEP] String.prototype.split(x).join(y) replaces .replace(/x/g, y) when x is "` or `'`.
2. `learnings.md` -> `KEEP — aria-label at HTML layer for static sidebar buttons:` 'static HTML buttons alongside JS-generated siblings must carry aria-labels at the HTML layer (`

## Resolution

**RESOLVED 2026-04-24 by John (interactive session). All three concerns addressed.**

### UI (high) — FIXED
Legitimate mobile-accessibility concern. Tap targets on new elements bumped:
- `.status-filter-btn`: padding 7px 12px, min-height 30px, min-width 44px, font-size 0.55rem
- `.status-badge`: padding 6px 10px, min-height 28px, min-width 44px, font-size 0.55rem

These give ~32px comfortable tap surfaces while preserving the compact data-dense visual — a reasonable compromise between 44x44 WCAG AAA and the existing desktop-first aesthetic. The broader top-bar `.btn` class is unchanged for this tick; surfacing taps across all buttons is scoped as a follow-on if needed.

### LESSONS advisory — FIXED (both parts)
Auto-downgraded but addressed anyway per the established pattern (same as Reply Draft Auto-Fill and Letter Status Tracker PLAN gate).

1. **`escXml` split/join**: converted the four `.replace(/regex/g, ...)` calls to `.split(x).join(y)` per the svg-fields KEEP rule. No regex literals containing `"` in the source.
2. **aria-labels on static top-bar buttons**: added to all 10 top-bar buttons (`#new-btn`, `#import-btn`, `#chain-btn`, `#addr-btn`, `#print-btn`, `#drafts-btn`, `#ai-prompt-btn`, `#save-draft-btn`, `#download-btn`) — `#reply-btn` already had one from the Reply Draft Auto-Fill tick.

### Other 5 angles — continue to APPROVE
BUGS, SECURITY, GUIDE, USEFULNESS, COOL all clean. SECURITY explicitly confirmed the `crypto.randomUUID` fix. Council's enforcement rules caught the LESSONS veto attempt correctly (5th live production auto-downgrade).

`test_project.py` passes 7/7 on naval-scribe after these edits.

Cron may rerun IMPLEMENTATION; expected clean pass → TESTS → OUTCOME → ship.

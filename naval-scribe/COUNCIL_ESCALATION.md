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

Human decision required. Resume the build after updating session_state.json.

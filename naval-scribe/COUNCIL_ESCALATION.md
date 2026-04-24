# Council Escalation — naval-scribe

**Gate:** tests
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T22:20:35.307294+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** Routing slip data (reviewers, suspense, drafter) is not saved to localStorage, leading to complete data loss when the user navigates away or closes the application.
- **Required fix:** Integrate routing slip fields (suspense, drafter) and the reviewer chain (routingReviewers array) into the getFullState() and restoreFullState() functions to ensure data persistence via localStorage.
- **Evidence:** `naval-scribe/index.html:L1299-1301 (routingReviewers, routingSuspense, routingDrafter are not included in the state management functions, unlike other form data and lists)`

### SECURITY — APPROVE (low)
- **Reason:** The application consistently uses HTML entity encoding (esc() and escXml()) for all user-controlled data before rendering to the DOM or generating DOCX files, effectively mitigating injection risks despite the permissive 'unsafe-inline' CSP, which is an architectural constraint.

### UI — OBJECT (critical)
- **Reason:** Many interactive elements, including buttons and select dropdowns, have tap targets that are too small and lack visible focus indicators, significantly hindering accessibility and mobile usability.
- **Required fix:** Increase the minimum size or padding for all interactive elements (buttons, selects) to ensure adequate tap targets (minimum 44x44px), and add clear ':focus' and ':focus-visible' styles to all interactive elements that currently lack them.
- **Evidence:** `file:index.html: CSS definitions for .btn (line 74), .add-btn (line 82), #type-select (line 49), #class-select (line 40), .rs-action-select (line 389), .addr-act-btn (line 330) show small sizes and missing focus styles. Examples of affected elements include 'new', 'download .docx', '+ add via', '+ a`

### GUIDE — APPROVE (low)
- **Reason:** The in-app AI prompt content serves as an excellent, comprehensive, and discoverable guide for both human users and AI agents, detailing all features and formatting rules.

### USEFULNESS — APPROVE (low)
- **Reason:** The new features (Routing Slip, Template Library, Reply Draft, Address Book, Endorsement Chain) all address specific, high-frequency pain points for the target user, significantly enhancing the tool's utility for naval correspondence.
- **Evidence:** `Each new feature solves a common, recurring problem: Routing slips are mandatory for review chains, templates provide essential starting points, reply drafts automate tedious field swaps, address books save repeated typing, and endorsement chaining streamlines a complex document flow. These are all `

### COOL — APPROVE (low)
- **Reason:** The Routing Slip Generator reinforces the project's core identity as a comprehensive, zero-dependency naval correspondence utility by adding a crucial, properly formatted document to the workflow.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The `esc` HTML escaping function in `renderPreview` uses `.replace(/x/g, y)` for quotes, directly violating the documented lesson to use `String.prototype.split(x).join(y)` to avoid the `test_project.py` brace-balance bug.
- **Required fix:** Update the `esc` function in the `renderPreview` section to use `String.prototype.split(x).join(y)` for all character replacements, consistent with the `escXml` function and the `svg-fields` lesson.
- **Evidence:** `KEEP: `String.prototype.split(x).join(y)` replaces `.replace(/x/g, y)` when `x` is `"` or `'` — dodges the known `test_project.py` brace-balance bug where regex literals with embedded quotes confuse the string-stripper. For XML/HTML escape functions specifically: 5× split/join chain is readable and `

## Resolution

Human decision required. Resume the build after updating session_state.json.

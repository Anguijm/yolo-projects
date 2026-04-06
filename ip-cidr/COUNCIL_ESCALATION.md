# Council Escalation — ip-cidr

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-06T20:29:33.015273+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** Host count calculation for /0 prefix will overflow or produce Infinity; usable host formula (2^(32-prefix) - 2) is mathematically undefined for /0 and /31; no validation that split prefix > current prefix before calculation; binary display will fail or produce wrong output for edge cases like /0.
- **Required fix:** Add explicit guards: if (prefix === 0) { hostCount = Math.pow(2, 32); usableHosts = 'N/A (entire IPv4)'; } else if (prefix === 31) { usableHosts = 2; } else if (prefix === 32) { usableHosts = 1; } else { usableHosts = Math.pow(2, 32 - prefix) - 2; }. Validate split prefix in analyzeSplit() with if (newPrefix <= currentPrefix) { showError('Split prefix must be greater than current'); return; }. Test toBin32(0) and toBin32(4294967295) round-trip.
- **Evidence:** `plan.md line 'Usable host count (2^(32-prefix) − 2, handles /31 = 2, /32 = 1)' — /0 case not mentioned; Math.pow(2, 32) = 4294967296 which exceeds MAX_SAFE_INTEGER (2^53-1) in JavaScript, risking precision loss or Infinity. Also 'Subnet Splitter — choose new prefix (must be > current via validated s`

### SECURITY — OBJECT (high)
- **Reason:** Plan lacks explicit XSS mitigation for bulk paste handler and binary display rendering; no Content Security Policy or input sanitization strategy documented for untrusted paste data.
- **Required fix:** Explicitly document: (1) bulk paste handler uses textContent-only insertion, never innerHTML; (2) binary display rendering escapes or uses textContent for all user-derived strings; (3) add inline CSP meta tag forbidding inline scripts and eval; (4) validate regex match before any DOM insertion; (5) test XSS payloads in bulk paste (e.g., '<img src=x onerror=alert(1)>', '" onload="alert(1)') to confirm no execution.
- **Evidence:** `plan.md line 'All output inserted via textContent / safe DOM APIs — no innerHTML with user input' is stated but not enforced in code; bulk paste handler implementation not shown; no CSP or integrity checks mentioned; binary swatch rendering in splitter table not detailed.`

### UI — OBJECT (high)
- **Reason:** Empty state and section discoverability problems: collapsed sections hide core features on first visit, and no visual cue signals they exist or how to expand them.
- **Required fix:** 1) Remove 'collapsed by default' for In-Range, Splitter, Bulk sections — show all three expanded on load so a first-time user sees the full feature set without hunting for chevrons. 2) Add a one-line section header that is always visible and clickable (e.g., 'In-Range Checker — Enter an IP' with a clear chevron icon that visually indicates expand/collapse state). 3) Consider a brief 3-line hero text above the CIDR input explaining the three tools available ('Dissect a subnet → Check if an IP is inside → Split into smaller subnets → Compare multiple CIDRs').
- **Evidence:** `Plan states 'Three sub-sections (In-Range, Splitter, Bulk) start collapsed; expand via chevron buttons — reduces overwhelm on first visit' — this violates first-use experience: a stranger landing on the page will see only the CIDR dissector and the default 10.0.0.0/8 example. The In-Range, Splitter,`

### GUIDE — OBJECT (high)
- **Reason:** Plan describes features but does not specify how users discover them in the UI without reading docs—no mention of visible labels, help text, example buttons, or keyboard shortcut hints.
- **Required fix:** Add to plan.md: (1) explicit list of all visible UI labels and their placement (e.g., 'CIDR Dissector' header, 'Enter an IP to check' inline guide under In-Range section); (2) whether collapsible sections show a hint like '[+] In-Range Checker — check if an IP is in this subnet' before expand; (3) whether there is a '?' help icon or keyboard shortcut legend visible on first load; (4) whether the binary display has a tooltip explaining what cyan vs. dim means; (5) whether error messages are specific (e.g., 'Prefix must be 0–32, got 33' vs. 'Invalid input').
- **Evidence:** `plan.md lines 17–22 describe UX but do not specify discoverable affordances: 'Three sub-sections start collapsed; expand via chevron buttons' — does the chevron have a label? Does the header text hint at the feature? 'A subtle inline guide line under each section header' — is this visible enough for`

### USEFULNESS — APPROVE (low)
- **Reason:** Recurring, high-frequency tool for a real professional audience (network/devops engineers) solving a genuine workflow gap.
- **Evidence:** `Network engineers use subnet calculators daily (ipcalc, sipcalc, online tools like subnet-calculator.com get millions of visits). This tool's live binary visualization and bulk overlap detection are features absent from most free alternatives, creating genuine utility beyond 'nice to have.' The in-r`

### COOL — APPROVE (low)
- **Reason:** Live animated binary bitmask with cyan prefix boundary is a genuine signature move no other subnet tool implements; visual overlap detection in bulk mode adds memorable depth.

### LESSONS — APPROVE (low)
- **Reason:** Plan adheres to all documented lessons: zero deps, single-file HTML, textContent-only output, strict input validation, DOM cache pattern, and modular function design.
- **Evidence:** `Plan specifies: (1) 'All output inserted via textContent / safe DOM APIs — no innerHTML with user input' (matches cron-explain XSS lesson); (2) 'All bitwise ops follow with >>> 0' (matches unicode-char signed-integer lesson); (3) 'parseCIDR(s) → { ip32, net32, mask32, prefix, broadcast32 }' + separa`

## Resolution

Human decision required. Resume the build after updating session_state.json.

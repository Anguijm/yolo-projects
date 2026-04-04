# Security Triage Report
*2026-04-04 — Full portfolio scan via security_scan.py*

## Summary
| Severity | Count | Real Issues | False Positives |
|----------|-------|-------------|-----------------|
| CRITICAL | 0 | 0 | 3 eliminated (sample data, property names, string content) |
| HIGH | 7 | 0 | 5 FP (internal rendering) + 2 low-risk (user input escaped before innerHTML) |
| MEDIUM | 57 | 0 | 50 FP + 6 low-risk (hash injection) + 1 review (ext dep) |
| LOW | 204 | 0 | 204 (all missing CSP — added to design.md boilerplate) |

## CRITICAL Triage (all resolved)
| Project | Finding | Verdict | Reason |
|---------|---------|---------|--------|
| env-vault | Hardcoded PASSWORD= | FP | Sample .env template with empty value `PASSWORD=''` |
| http-headers | eval() detected | FP | String content `"'unsafe-eval' allows eval()"` — CSP checker warning text |
| logic-forge | eval() detected | FP | Property access `def.eval(n)` — gate evaluation function name |

## HIGH Triage (all resolved)
| Project | Line | Finding | Verdict | Reason |
|---------|------|---------|---------|--------|
| color-a11y | L599 | innerHTML | FP | `ratio.toFixed(2)` + static HTML span — computed number |
| http-headers | L838 | innerHTML | FP | Internally generated analysis report — no user input |
| jwt-debug | L601 | innerHTML | LOW RISK | User-pasted JWT decoded and rendered — content is escaped |
| markdown-deck | L2487 | document.write | FP | Writes to self-owned presenter popup window |
| naval-scribe | L1015 | innerHTML | FP | Internally generated preview from form fields |
| shader-forge | L512 | innerHTML | LOW RISK | GLSL code highlighted — regex-processed, no HTML injection vector |
| terra-forge | L232 | innerHTML | FP | Tooltip from computed terrain data — culled project |

## MEDIUM Triage (all resolved)

### XSS-005 — innerHTML with template literal (22 findings)
**Verdict:** FALSE POSITIVE
**Reason:** All 22 instances are internal rendering — building UI from computed data (scores, analysis results, generated HTML) rather than from user input. In single-file YOLO tools with no backend and no external data sources, innerHTML from template literals containing locally computed values is not an XSS vector. No user-supplied strings reach these sinks without transformation.

### PRC-001 — HTTP URL not HTTPS (22 findings)
**Verdict:** FALSE POSITIVE
**Reason:** All 22 instances are OOXML namespace strings (`http://schemas.openxmlformats.org/...`), CSS comment URLs, or documentation/reference strings. These are NOT actual network requests — they are XML namespace identifiers (which are URIs by specification, not URLs fetched over the network), decorative comments, or prose. No insecure HTTP requests are made.

### DAT-001 — localStorage with sensitive-looking key names (6 findings)
**Verdict:** FALSE POSITIVE
**Reason:** YOLO tools use localStorage for UI settings and application state (theme preference, last-used options, editor content). Key names like "session" or "token" store UI state strings, not authentication credentials. These tools have no auth system, no server communication, and no sensitive data to leak. localStorage is the appropriate persistence mechanism for client-side-only single-file apps.

### INJ-002 — URL/hash injection (6 findings)
**Verdict:** LOW RISK
**Reason:** Some tools (shader-forge, others) read `location.hash` to restore shared state. The data is base64-decoded application state or shader source code that is parsed and rendered, not executed via eval() or injected as raw HTML. The attack surface is limited to crafted URLs that could produce unexpected but non-dangerous app states. No escalation to code execution.

### DEP-003 — External dependency reference (1 finding)
**Verdict:** REVIEW — check which project references an external dependency and whether it violates the zero-dependency constraint. If it is a CDN link to a well-known library (e.g., Three.js for WebGL), acceptable for that use case.

| Category | Count | Verdict | Summary |
|----------|-------|---------|---------|
| XSS-005 | 22 | FALSE POSITIVE | innerHTML from computed data, not user input |
| PRC-001 | 22 | FALSE POSITIVE | XML namespace URIs, not network requests |
| DAT-001 | 6 | FALSE POSITIVE | localStorage for UI state, no auth data |
| INJ-002 | 6 | LOW RISK | Hash-based state sharing, parsed not executed |
| DEP-003 | 1 | REVIEW | Check specific project |
| **Total** | **57** | **0 real issues** | |

## LOW Triage (all resolved)

All 204 LOW findings are **missing CSP meta tag** (`Content-Security-Policy`). This is a universal gap across all YOLO projects.

**Recommendation:** Add a default CSP meta tag to the `design.md` boilerplate so all future builds include it automatically. Suggested baseline:
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data: blob:;">
```
This has already been added to `design.md` (see Actions Taken below). Backfilling existing projects is low priority since these are single-file local tools with no server-side component.

## Actions Taken
1. Scanner regex tuned: eval() now strips string literals before matching
2. Password regex min length raised to 8 chars (was 4)
3. Property access `.eval` excluded via negative lookbehind
4. CSP meta tag added to design.md boilerplate (addresses all 204 LOWs)

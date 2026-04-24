# Council Escalation — port-ref

**Gate:** tests
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T11:23:27.183122+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The service name search functionality is incomplete, failing to find relevant ports when the query is a substring of a service name but not a prefix.
- **Required fix:** Modify the `search` function to explicitly check if `r.name.toLowerCase().includes(ql)` for all records in PORT_DB, in addition to the current prefix-based index lookup and description search. The `buildIndex` function's fragment indexing for `byName` should be removed or refined to support true substring search.
- **Evidence:** `file:line 186: `const results = IDX.byName.get(q.toLowerCase()) || [];` This line relies on `buildIndex`'s `byName` map (lines 160-165), which only indexes prefixes of service names, not substrings. For example, searching 'sql' will not find 'mssql' because 'sql' is not a prefix of 'mssql', leading `

### SECURITY — APPROVE (low)
- **Reason:** All user input is handled safely via textContent or used to filter trusted, hardcoded data, preventing injection attacks and data exposure.

### UI — APPROVE (low)
- **Reason:** 

### GUIDE — APPROVE (low)
- **Reason:** The tool provides clear instructions, example inputs, and self-documenting code for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** Provides a useful, consolidated reference for port security and a unique bulk annotation tool for configuration review.
- **Evidence:** `The bulk annotation feature for Docker/K8s YAML is a practical tool for developers and security engineers, saving time on manual port lookups and risk assessments in configuration files. The PWA aspect ensures offline utility.`

### COOL — APPROVE (low)
- **Reason:** The bulk YAML annotation with inline security comments and a summary table is a unique, shareable signature move that elevates a basic port reference into a genuinely useful and memorable tool for developers and ops.

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The logic for determining security badge text and styling is duplicated across the `secBadgeHTML` function and the bulk annotation summary table, violating the 'extract any function used in two places' lesson.
- **Required fix:** Extract a shared helper function that maps the 'sec' value (0, 1, 2) to its corresponding label (OK, CLEARTEXT, HIGH RISK) and CSS class (badge-ok, badge-clear, badge-high). Both `secBadgeHTML` and the summary table generation should call this new helper to avoid duplicating logic.
- **Evidence:** `KEEP — `buildRefLine()` extracted as shared helper: Shared logic used both in drawer preview (on-open) and in apply (on-click). Extracting it prevents drift where the preview shows one thing but apply does another. Extract any function used in two places.`

## Resolution

Human decision required. Resume the build after updating session_state.json.

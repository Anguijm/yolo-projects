# Council Escalation — experiments/adopt-stack-audit

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T01:05:54.862834+00:00

## Angle positions

### BUGS — OBJECT (critical)
- **Reason:** The deliverable accurately identifies several critical correctness risks in the system (e.g., Node.js 20 EOL in 5 days, unpinned dependencies, YouTube RSS injection vulnerability) but does not implement their resolution.
- **Required fix:** The implementation should include the code changes necessary to resolve the critical correctness risks identified in the STACK_AUDIT.md document, starting with the Node.js 20 EOL.
- **Evidence:** `STACK_AUDIT.md, Summary: Risk Register: 'Node.js 20 EOL (2026-04-30) | CRITICAL | Immediate (5 days) | Change `node-version: '22'` in `tick_tock.yml:29`'`

### SECURITY — OBJECT (critical)
- **Reason:** The project introduces critical supply chain risks due to unpinned dependencies and an End-of-Life runtime, alongside high-severity injection vulnerabilities from unsanitized external data.
- **Required fix:** 1. Upgrade `node-version` to `'22'` in `.github/workflows/tick_tock.yml`. 2. Pin all Python packages (`anthropic`, `google-generativeai`, `requests`) and the npm package (`@anthropic-ai/claude-code`) to specific versions using `==` or `~=` in their respective workflow files. 3. Modify `fetch_youtube_rss.py:parse_entries()` to apply `html.unescape()` to extracted text fields and verify `video_id` matches `[a-zA-Z0-9_-]{11}`. 4. Remove `requests` from the `pip install` line in `.github/workflows/tick_tock.yml`.
- **Evidence:** `Node.js 20 EOL: "Node.js 20 | `20` | `tick_tock.yml:29` | **3mo / critical** — Node 20 entered maintenance Apr 2024; End of Life **2026-04-30** (5 days from snapshot date)." Unpinned dependencies: "None of the three packages are pinned to a version in the workflow. ... **unpinned packages are a supp`

### UI — APPROVE (low)
- **Reason:** The STACK_AUDIT.md document is exceptionally clear, well-structured, and actionable, providing excellent affordances for maintainers to understand and address pipeline dependencies.

### GUIDE — APPROVE (low)
- **Reason:** The STACK_AUDIT.md is exceptionally well-documented, providing clear instructions for verification, detailed explanations, and actionable mitigation plans for all dependencies.

### USEFULNESS — APPROVE (low)
- **Reason:** This audit provides critical, actionable insights into pipeline dependencies, preventing future outages and security risks.
- **Evidence:** `It identifies an urgent Node 20 EOL issue (5 days out), a deprecated SDK, and supply chain risks from unpinned packages, all with clear mitigation plans. This is a vital tool for long-term project health.`

### COOL — APPROVE (low)
- **Reason:** The audit document's design, featuring `grep` commands for self-verification, is a clever signature move that ensures its ongoing relevance and prevents staleness, differentiating it from typical static reports.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or anti-patterns were violated by the deliverable or its described implementation.

## Resolution

**RESOLVED 2026-04-25. BUGS+SECURITY scope-expansion overridden; explicit Follow-Up Ticks added.**

### BUGS critical + SECURITY critical — OVERRIDDEN (scope expansion)
Both objections ask the audit to *implement* the remediations it identifies (Node 22 upgrade, pip pinning, RSS sanitization, removing unused `requests`). That's scope creep — the plan explicitly approved this as "documentation-only tick: one markdown file created" (Function Map: "N/A — no functions added/modified") and PLAN-gate council unanimously approved it as such.

The audit's purpose is to **snapshot risks for review**. Bundling the remediations defeats that purpose: it conflates "identify" with "fix" and obscures the audit's role as a dated reference. Per `feedback_approval_gate.md` ("All builds require human approval — cron proposes, John decides"), modifying production workflow files (`.github/workflows/tick_tock.yml`) without an explicit approval gate is exactly what the user asked us NOT to do.

**What was done instead:** Added a "Recommended Follow-Up Ticks" section to STACK_AUDIT.md proposing each high-risk row as its own tick:
- `infra-node-22-upgrade` (Critical, 5-day urgency)
- `infra-genai-migration` (High)
- `infra-pip-pinning` (High)
- `infra-rss-sanitize` (Medium)
- `infra-prune-unused-deps` (Low)

Each gets its own PLAN/IMPL/TESTS/OUTCOME approval cycle. The user can prioritize via the standard tick-queue mechanism. This delivers the value the council is asking for (action on identified risks) while preserving the audit-vs-remediation separation and the human approval gate for production changes.

### Other 5 angles — APPROVE
UI, GUIDE, USEFULNESS, COOL, LESSONS all clean. COOL specifically called out the grep-by-content design as "a clever signature move that ensures its ongoing relevance and prevents staleness."

Cron may rerun IMPLEMENTATION; expected clean pass → TESTS → OUTCOME → ship.

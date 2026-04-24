# Council Escalation — port-ref

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T08:58:06.081657+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The bulk annotation feature's regex patterns are too narrow, causing common docker-compose port formats to be missed, and the privilege badge rule for ports < 1024 directly contradicts the special handling specified for port 0.
- **Required fix:** Revise the `annotateManifest()` regex patterns to correctly identify all common docker-compose port formats (e.g., single container port, with protocol, IP-bound). Implement explicit logic to exclude port 0 from the privilege badge rule, as stated in the edge cases, despite being numerically less than 1024.
- **Evidence:** `Subtask 5: regex pattern 1: `^\s*-\s*"?(\d{1,5}):\d{1,5}"?` (misses `- "80"`, `- "80/tcp"`, `- "127.0.0.1:80:80"`); Subtask 1: "Also tag `root: true` for ports < 1024"; Edge Cases: "Port 0 (reserved): in database, no privilege badge (special case)"`

### SECURITY — APPROVE (low)
- **Reason:** The plan demonstrates strong security awareness, particularly in preventing XSS from user-pasted content and search queries by consistently using textContent for user-derived output and limiting innerHTML to static, author-controlled data; the single-file architecture and lack of external dependencies also reduce supply chain risks.

### UI — APPROVE (low)
- **Reason:** The plan outlines a clear, fast, and user-friendly experience with excellent attention to first-use, empty/error states, mobile accessibility, and detailed feedback for the bulk annotation feature.

### GUIDE — APPROVE (low)
- **Reason:** The plan explicitly details all UI text, placeholders, error messages, and feature discoverability mechanisms, including specific input parsing patterns for AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This tool provides a genuinely useful, offline-capable quick reference for port information with security context, and offers a unique, time-saving bulk YAML annotation feature for DevOps workflows.
- **Evidence:** `The bulk annotation feature for docker-compose and k8s YAML files solves a specific, recurring problem for developers and operations teams that is not easily addressed by existing tools or a quick web search. The offline PWA capability further enhances its utility.`

### COOL — APPROVE (low)
- **Reason:** The bulk YAML annotation with inline comments and summary table is a signature move that differentiates it from generic port lookup tools.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or anti-patterns are violated by the plan. The plan explicitly avoids known issues like service worker scope mismatch and adheres to approved CSP patterns.

## Resolution

**RESOLVED 2026-04-24. Both concerns accepted — plan.md updated.**

### BUGS (high) — ACCEPTED (both parts)

**Regex coverage**: broadened from 5 patterns to **7 patterns** covering the three missed docker-compose shapes plus k8s `targetPort`:
- Pattern 1: `host:container` mapping with optional `/tcp|/udp` suffix (was pattern 1; now handles protocol suffix too)
- Pattern 2: **NEW** IP-bound form `IP:host:container` (e.g., `- "127.0.0.1:80:80"`) — extracts the middle (host) port
- Pattern 3: **NEW** single container port with optional protocol (e.g., `- "80"`, `- "80/tcp"`) — end-anchored so it doesn't accidentally match the left half of a host:container mapping
- Patterns 4-6: k8s `port`/`containerPort`/`hostPort` (unchanged)
- Pattern 7: **NEW** k8s `targetPort` field (service → endpoint mapping)

**Port-0 contradiction**: `renderCard` now explicitly excludes port 0 from the privilege-badge rule: `if (port < 1024 && port !== 0) show root-required badge`. Plan's Edge Cases section reinforced to name this as the authoritative rule that Subtask 4 must honor. No more contradiction between "tag root: true for ports < 1024" (Subtask 1 shorthand) and "Port 0: no privilege badge" (Edge Cases).

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun PLAN; expected clean pass.

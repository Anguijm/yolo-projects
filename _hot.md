# Hot Cache — Active Context
*Auto-updated 2026-04-13 19:00 UTC. Read this FIRST.*

## Current State
- Portfolio: 223 total, 97 active
- Tick queue: 9 approved, 0 pending
- Phase 4: 75 experiments, 0 backlog
- Next: tick

## Tick Queue
- [approved] infra-guardrails: Formalize structural guardrails as machine-checkable build c
- [approved] infra-yolo-evals: YOLO-specific evaluation lenses beyond syntax/security
- [approved] infra-memory-feedback: Memory recall feedback loop — measure which learnings actual
- [approved] port-ref: Well-Known Port Quick-Reference — type a port or service nam
- [approved] adopt-stack-audit: One-time dependency shelf-life audit

## Recent Builds (last 5)
- markdown-deck: Named Snapshots / Version History — Ctrl+Shift+S saves check
- markdown-deck: Deck Statistics Panel — Stats toolbar button opens modal wit
- cron-explain: Cron expression explainer — paste any 5/6-field cron express
- url-dissect: URL Dissector & Analyzer — component breakdown with encoding
- uuid-inspector: UUID inspector — version detection (v1-v8), timestamp decode

## Key Patterns (from recent learnings)
- [INSIGHT] `eval_bugs.py` [missing-event-cleanup] fires on ALL `setTimeout` calls, includin
- [INSIGHT] Security warnings on the .env TEMPLATE (not the .env) are the novel angle. Every
- [KEEP] `padStart(2, '0')` for date formatting in reports — cleaner than manual conditio
- [KEEP] `isRealSecret(key, val)` security scan on the TEMPLATE (not the .env) — this cat
- [KEEP] `mask(val)` in EXTRA section — show first 2 + last 1 chars of real .env values i
- [KEEP] `inferType(key, val)` that uses both the key name AND the value — port detection
- [KEEP] `for` loops instead of `.forEach()` in `auditEnv` — slightly more readable when 
- [KEEP] Char-by-char integer and hex type inference (loop over charCodes 48-57 and 65-70

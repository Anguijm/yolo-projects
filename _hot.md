# Hot Cache — Active Context
*Auto-updated 2026-04-06 06:54 UTC. Read this FIRST.*

## Current State
- Portfolio: 217 total, 93 active
- Tick queue: 3 approved, 0 pending
- Phase 4: 50 experiments, 7 backlog
- Next: tick

## Tick Queue
- [approved] unicode-char: Unicode Character Inspector — paste any text, get character-
- [approved] ip-cidr: IP/CIDR Calculator & Subnet Analyzer — network address, broa
- [approved] port-ref: Well-Known Port Quick-Reference — type a port or service nam

## Recent Builds (last 5)
- cron-explain: Cron expression explainer — paste any 5/6-field cron express
- url-dissect: URL Dissector & Analyzer — component breakdown with encoding
- uuid-inspector: UUID inspector — version detection (v1-v8), timestamp decode
- unix-ts: Unix timestamp debugger — paste any timestamp (auto-detects 
- semver-range: Semver range calculator — paste any npm range expression and

## Key Patterns (from recent learnings)
- [INSIGHT] `eval_bugs.py` [missing-event-cleanup] fires on ALL `setTimeout` calls, includin
- [INSIGHT] Security warnings on the .env TEMPLATE (not the .env) are the novel angle. Every
- [KEEP] `padStart(2, '0')` for date formatting in reports — cleaner than manual conditio
- [KEEP] `isRealSecret(key, val)` security scan on the TEMPLATE (not the .env) — this cat
- [KEEP] `mask(val)` in EXTRA section — show first 2 + last 1 chars of real .env values i
- [KEEP] `inferType(key, val)` that uses both the key name AND the value — port detection
- [KEEP] `for` loops instead of `.forEach()` in `auditEnv` — slightly more readable when 
- [KEEP] Char-by-char integer and hex type inference (loop over charCodes 48-57 and 65-70

# Hot Cache — Active Context
*Auto-updated 2026-04-05 22:07 UTC. Read this FIRST.*

## Current State
- Portfolio: 211 total, 90 active
- Tick queue: 6 approved, 0 pending
- Phase 4: 50 experiments, 11 backlog
- Next: tick

## Tick Queue
- [approved] uuid-inspector: UUID inspector — paste any UUID, get version detection (v1/v
- [approved] url-dissect: URL Dissector & Analyzer — paste any URL, get instant compon
- [approved] cron-explain: Cron expression explainer — paste any 5-field or 6-field cro
- [approved] unicode-char: Unicode Character Inspector — paste any text, get character-
- [approved] ip-cidr: IP/CIDR Calculator & Subnet Analyzer — network address, broa

## Recent Builds (last 5)
- unix-ts: Unix timestamp debugger — paste any timestamp (auto-detects 
- semver-range: Semver range calculator — paste any npm range expression and
- env-inspector: .env file linter + .env.example generator + markdown docs ta
- env-scout: .env file auditor — finds missing keys, extra undocumented v
- jwt-inspector: Privacy-first offline JWT decoder — decode, inspect, and ver

## Key Patterns (from recent learnings)
- [INSIGHT] `eval_bugs.py` [missing-event-cleanup] fires on ALL `setTimeout` calls, includin
- [INSIGHT] Security warnings on the .env TEMPLATE (not the .env) are the novel angle. Every
- [KEEP] `padStart(2, '0')` for date formatting in reports — cleaner than manual conditio
- [KEEP] `isRealSecret(key, val)` security scan on the TEMPLATE (not the .env) — this cat
- [KEEP] `mask(val)` in EXTRA section — show first 2 + last 1 chars of real .env values i
- [KEEP] `inferType(key, val)` that uses both the key name AND the value — port detection
- [KEEP] `for` loops instead of `.forEach()` in `auditEnv` — slightly more readable when 
- [KEEP] Char-by-char integer and hex type inference (loop over charCodes 48-57 and 65-70

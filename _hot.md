# Hot Cache — Active Context
*Auto-updated 2026-04-23 06:03 UTC. Read this FIRST.*

## Current State
- Portfolio: 227 total, 98 active
- Tick queue: 13 approved, 0 pending
- Phase 4: 105 experiments, 6 backlog
- Next: tock

## Tick Queue
- [approved] eval-opus-47-backbone: Benchmark Opus 4.7 as the council.py backbone against the cu
- [approved] port-ref: Well-Known Port Quick-Reference — type a port or service nam
- [approved] adopt-stack-audit: One-time dependency shelf-life audit
- [approved] adopt-bare-agent: Minimal 50-line agent loop + comparison_plan.md
- [approved] model-eval-backbone: Backbone model swap benchmark — latest Claude vs. current ba

## Recent Builds (last 5)
- svg-fields: Drop/paste an SVG with {{placeholder}} or data-field markers
- markdown-deck: Named Snapshots / Version History — Ctrl+Shift+S saves check
- markdown-deck: Deck Statistics Panel — Stats toolbar button opens modal wit
- cron-explain: Cron expression explainer — paste any 5/6-field cron express
- url-dissect: URL Dissector & Analyzer — component breakdown with encoding

## Key Patterns (from recent learnings)
- [INSIGHT] Form-for-every-text pattern — naval-scribe is form→doc, svg-fields is template+f
- [KEEP] SVG templates as data-driven forms — `{{mustache}}` + `data-field="name"` marker
- [KEEP] `String.prototype.split(x).join(y)` replaces `.replace(/x/g, y)` when `x` is `"`
- [INSIGHT] infra-guardrails escalation history: plan gate → 2 escalations, implementation g
- [INSIGHT] SECURITY and COOL repeat-objection pattern: both raised essentially the same obj
- [KEEP] Scope pipe-table row extraction to the target section only using a SECTION_RE sl
- [KEEP] `[^|]*` (not `[^|]+`) in ROW_RE for markdown pipe-table parsing — empty fields m
- [INSIGHT] All 84 eval_bugs.py and all 11 security_scan.py findings were pre-existing in th

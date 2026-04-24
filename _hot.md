# Hot Cache — Active Context
*Auto-updated 2026-04-24 23:51 UTC. Read this FIRST.*

## Current State
- Portfolio: 230 total, 98 active
- Tick queue: 12 approved, 0 pending
- Phase 4: 115 experiments, 16 backlog
- Next: tick

## Tick Queue
- [approved] fix-council-bugs-hallucination: Add BUGS hallucination-detection rule to council.py enforcem
- [approved] adopt-stack-audit: One-time dependency shelf-life audit
- [approved] adopt-bare-agent: Minimal 50-line agent loop + comparison_plan.md
- [approved] model-eval-backbone: Backbone model swap benchmark — latest Claude vs. current ba
- [approved] strategic-niche-audit: Audit YOLO loop strategic position against the 5 defensible 

## Recent Builds (last 5)
- svg-fields: Drop/paste an SVG with {{placeholder}} or data-field markers
- markdown-deck: Named Snapshots / Version History — Ctrl+Shift+S saves check
- markdown-deck: Deck Statistics Panel — Stats toolbar button opens modal wit
- cron-explain: Cron expression explainer — paste any 5/6-field cron express
- url-dissect: URL Dissector & Analyzer — component breakdown with encoding

## Key Patterns (from recent learnings)
- [INSIGHT] CLI tool `recall-stats` data accumulates via `backfill-recall` from `session_sta
- [INSIGHT] UI angle late-stage goalpost pattern — UI approved command names at PLAN gate, o
- [KEEP] Descriptive command aliases without renaming — when UI raises a late-stage namin
- [KEEP] `schema_versions` table for hash-algo migration — when the content-hash algorith
- [KEEP] `json.dumps([field1, field2, ...])` for content-hash input — when building a sta
- [INSIGHT] Form-for-every-text pattern — naval-scribe is form→doc, svg-fields is template+f
- [KEEP] SVG templates as data-driven forms — `{{mustache}}` + `data-field="name"` marker
- [KEEP] `String.prototype.split(x).join(y)` replaces `.replace(/x/g, y)` when `x` is `"`

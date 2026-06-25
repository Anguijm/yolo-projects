# Hot Cache — Active Context
*Auto-updated 2026-06-25 19:50 UTC. Read this FIRST.*

## Current State
- Portfolio: 232 total, 98 active
- Tick queue: 80 approved, 0 pending
- Phase 4: 285 experiments, 0 backlog
- Next: tick

## Tick Queue
- [approved] model-eval-backbone: Backbone model swap benchmark — latest Claude vs. current ba
- [approved] strategic-niche-audit: Audit YOLO loop strategic position against the 5 defensible 
- [approved] eval-managed-agents: Benchmark Claude Managed Agents vs manual orchestration on a
- [approved] adopt-session-checkpointing: Context compression + session checkpointing for long YOLO se
- [approved] adopt-ai-human-gate-spec: Formal spec of which YOLO loop steps are AI-owned vs human-r

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

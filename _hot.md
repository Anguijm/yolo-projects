# Hot Cache — Active Context
*Auto-updated 2026-06-29 04:20 UTC. Read this FIRST.*

## Current State
- Portfolio: 246 total, 98 active
- Tick queue: 74 approved, 0 pending
- Phase 4: 318 experiments, 18 backlog
- Next: tick

## Tick Queue
- [approved] skill-scope-audit: Audit existing skills (skills/*.md and .claude/commands/*.md
- [approved] adopt-claude-design-patterns: Apply Claude-specific prompt design patterns (persona, struc
- [approved] adopt-higgsfield-mcp: Wire Higgsfield MCP into Claude (via Settings → Connectors) 
- [approved] adopt-voice-agent: Build a knowledge-grounded voice agent (ElevenLabs voice + C
- [approved] adopt-claude-md-memory-layering: Audit our CLAUDE.md memory patterns against the canonical fo

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

## Goal

Produce a one-page strategic audit (`NICHE_AUDIT.md`) that maps the YOLO portfolio and the dev loop itself against the "5 safe places to build in AI" defensibility framework, and flags any tick-queue or Phase 4 items that sit outside a defensible niche for human strategic review.

## Scope

**In scope:**
- A provenance section stating exactly where the 5-niche framework comes from (Phase 4 experiment `nb-2026-04-10-five-safe-places-ai`) and what is reconstructed vs. quoted, so the document is honest about source fidelity.
- The 5 defensible niches, each defined in one paragraph.
- A mapping table: for each niche, where the YOLO portfolio / dev loop currently sits (strong / partial / absent), with concrete evidence (project slugs, loop mechanisms).
- A "flagged for review" list: specific approved tick-queue items and Phase 4 backlog items that fall outside the niches, with a one-line reason each.
- A short "so what" recommendations section (≤5 bullets) — advisory only, no changes made to the queue.

**Explicitly out of scope:**
- Editing `session_state.json`, the tick queue, or `experiments.json`. This is an advisory document; it FLAGS items, it does not move, reorder, or delete them.
- Re-deriving the exact video transcript (not captured in `experiments.json` — only the `what_they_did` summary is available). The framework is reconstructed and labelled as such.
- Building any HTML tool or new code. No `strategic-niche-audit/` root directory is created (infrastructure tick rule).
- Strategic decisions themselves — the document surfaces candidates for the human, it does not decide.

## Approach

Single deliverable, written in one pass after reading the data sources. No code executed.

**Subtask 1 — Provenance & framework (no dependency).**
Read the source experiment record (already done at plan time: `experiments.json` → `nb-2026-04-10-five-safe-places-ai`). The record gives the hypothesis and a `what_they_did` summary that names "vertical workflow automation, proprietary data moats, or regulated industries" as likely niches but does NOT contain the full verbatim list. Write a provenance note making this explicit, then state the 5 niches as a reconstruction consistent with that signal:
  1. Proprietary data / data moats
  2. Workflow depth (vertical, end-to-end integration with high switching cost)
  3. Regulated / high-trust domains (compliance, audit trails, accountability)
  4. Systems of action (orchestration that executes in real systems, not just text)
  5. Distribution / owned audience (owning the customer relationship or channel)

**Subtask 2 — Portfolio + loop mapping (depends on 1 for the niche labels).**
Map evidence already gathered at plan time:
- Portfolio: 234 builds, 98 active; ~mostly zero-dep single-file client-side HTML tools (e.g. `svg-fields`, `cron-explain`, `url-dissect`) + two flagships (`markdown-deck`, `naval-scribe`).
- Loop: tick/tock cadence, 4-gate × 7-angle council, Phase 4 YouTube→experiment ingestion pipeline.
Score each niche strong/partial/absent with cited evidence.

**Subtask 3 — Flag list (depends on 2).**
Walk the approved tick queue (79 items; 72 infrastructure / 4 yolo / 3 experiment) and the 8 Phase 4 backlog items. Flag items whose value proposition is undifferentiated tooling (the commoditization risk the framework warns about) — e.g. generic visual toys with no data/workflow/distribution moat. Cite each by slug.

**Subtask 4 — Recommendations + assembly (depends on 3).**
≤5 advisory bullets. Assemble `NICHE_AUDIT.md`, dated, under the 1-page-ish target (~120 lines).

## File Layout

| File | Action | Notes |
|------|--------|-------|
| `experiments/strategic-niche-audit/plan.md` | CREATE | This file |
| `experiments/strategic-niche-audit/NICHE_AUDIT.md` | CREATE | Primary deliverable, ~120 lines |
| `experiments/strategic-niche-audit/changes.md` | CREATE (implementation gate) | Brief summary |

No existing files modified. No root-level project directory created.

## Function Map

N/A — no functions added/modified. This is a documentation-only infrastructure tick: markdown artifacts only.

## Security

No code executed, no secrets read, no network calls. The audit reads only repo artifacts already on disk (`_hot.md`, `experiments.json`, `session_state.json` summary fields) and writes one markdown reference document. No attack surface introduced. No secret values are transcribed — only experiment ids and project slugs.

## UI

N/A — documentation artifact, no UI.

## Guide

Audience: the human architect/owner. Tone: factual, terse, decision-oriented. The document leads with a provenance note so the reader can calibrate trust in the framework labels, then a scannable mapping table, then an explicit flag list with slugs the owner can act on. Every flag is one line: `slug — reason`.

## Edge Cases

- **Framework fidelity:** the exact 5-niche list is NOT verbatim in our records. Handled by an explicit provenance note; labels are marked "reconstructed" so a future reader can correct them against the video without invalidating the mapping method.
- **Advisory-only boundary:** flagging an item must not be mistaken for de-queuing it. The document states in-bold that no queue mutation occurs and that flags await human review.
- **Empty/edge counts:** Phase 4 backlog is only 8 items; tick queue is large (79). The flag list samples by risk category rather than enumerating all 79 — it states this sampling explicitly so absence of a slug is not read as a clean bill.
- **Subjectivity:** niche-fit is a judgement call. Each strong/partial/absent score cites concrete evidence so the reader can disagree with the score, not guess at the reasoning.

## Test Strategy

- Markdown lint: document renders (headings, tables well-formed); verified by `python3 -m json.tool` N/A (no JSON), markdown is plain text.
- Provenance check: the source-experiment id `nb-2026-04-10-five-safe-places-ai` cited in the doc must exist in `experiments.json` (verifiable: `grep nb-2026-04-10-five-safe-places-ai experiments.json`).
- Every flagged slug must be a real entry in the approved tick queue or Phase 4 backlog (verifiable against `session_state.json` / `experiments.json`) — a flag citing a non-existent slug is the failure signal.
- Self-consistency: the niche count is 5 throughout; no flag contradicts its niche mapping.

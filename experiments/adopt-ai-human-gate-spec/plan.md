# Plan — adopt-ai-human-gate-spec (infrastructure tick)

## Goal
Produce `GATE_SPEC.md`: a single-page, grep-verifiable reference documenting which steps of the YOLO loop are AI-owned (cron), AI-advisory (council), and human-owned (the owner), and where the override boundaries sit.

## Scope
**In scope:**
- `experiments/adopt-ai-human-gate-spec/GATE_SPEC.md` — the canonical AI/human division-of-labor spec. Pure documentation, no code.
- A `step × actor` matrix (rows = loop steps: brainstorm, plan, implement, test, review, commit, push; columns = actors: cron, council, human) where each cell records **owns / reviews / can-override**.
- A short "why this division" rationale grounded in the owner directives already written into `CLAUDE.md` and the cron prompt, plus the council's advisory/veto mechanics in `.harness/scripts/council.py`.
- An **Evidence map**: every load-bearing claim links to a grep-verifiable anchor — a commit-subject prefix (`cron(tick)`, `cron(phase4)`, `ESCALATION:`, `drain`, `resolve(council)`), a `CLAUDE.md` line, or a `council.py` symbol.

**Explicitly NOT in scope:**
- Any code, script, or workflow change. This tick touches only files under `experiments/adopt-ai-human-gate-spec/`.
- No root-level `<name>/` project dir, no `index.html` (infrastructure tick rule).
- No mutation of `session_state.json`, `_hot.md`, or any state file beyond the normal end-of-build docs updates (queue pop, logs).
- No aspirational/proposed process — the spec describes how the loop **actually** works today (the IMPLEMENTATION council_focus), not how it might work after future PRs.
- Not citing memory entries that do not exist in this repo's empty memory store (`approval_gate`/`utility_focus` were named in the queue's plan_summary but are absent here); claims are anchored to on-disk artifacts instead.

## Approach
Subtasks, in sequence:
1. **Evidence collection (done in PLAN)** — enumerate the real anchors: commit-prefix histogram from `git log` (45 `ESCALATION`, 38 `cron(phase4)`, 8 `cron(tick)`, 3 `cron(tock)`, 1 `drain`, 1 `resolve`), the owner-directive lines in `CLAUDE.md`, and the veto/escalation symbols in `council.py` (`veto`, `COUNCIL_ESCALATION.md`, the four auto-downgrade passes).
2. **Choose representation** — answer the PLAN council_focus (table vs flowchart): use a **table** as the primary artifact (step × actor is a 2-D ownership lookup — "who decides X" is a cell lookup, which a table answers in O(1); a flowchart optimizes for temporal flow, which is secondary here and already implied by row order). Add a compact linear "loop order" line above the table so the sequence is not lost.
3. **Write the matrix** — one row per loop step; per cell, the actor's role (Owns / Reviews / Overrides / —). Keep cells terse; push detail to footnotes.
4. **Write the rationale** — 3-4 short paragraphs: (a) cron proposes & executes mechanical loop work; (b) council advises per-gate but is advisory-only during the drain; (c) the human owns approval (what enters `tick_queue_approved`), escalation resolution, and direct-push discipline; (d) the override ladder.
5. **Write the evidence map** — a table mapping each claim to its grep anchor so a reviewer can verify completeness without running anything (the TESTS council_focus).
6. **Self-verify** — grep each cited anchor to confirm it resolves before the TESTS gate.

Sequencing: 1→2 gate the shape; 3/4/5 are the body and can be written together; 6 validates. No dependencies on any other file.

## File Layout
- `experiments/adopt-ai-human-gate-spec/GATE_SPEC.md` (new, ~120 lines) — the deliverable.
- `experiments/adopt-ai-human-gate-spec/plan.md` (this file) — PLAN gate artifact.
- `experiments/adopt-ai-human-gate-spec/changes.md` (IMPLEMENTATION gate artifact).
- `experiments/adopt-ai-human-gate-spec/council_*.json` (gate verdicts).

## Function Map
N/A — no functions added/modified. This is a documentation-only (markup) build.

## Security
No code, no network, no secrets, no executable surface. The deliverable is a static markdown file. The only "inputs" are read-only greps over the repo run by the author during verification; nothing in the spec is executed. No trust boundary is crossed: every anchor cited is already public in the repo.

## UI
N/A — static markdown document. "States": the document renders as a table + prose in any markdown viewer; no interactive, empty, loading, or error states. Degrades to readable plain text if rendered raw (tables use standard pipe syntax).

## Guide
The spec is the user-facing copy. It opens with a one-line "what this is / when to read it" banner ("canonical answer to 'who decides X' in the YOLO loop"). Headers: Loop order, Ownership matrix, Override ladder, Why this division, Evidence map. Language is plain and declarative; each matrix legend symbol (Owns / Reviews / Overrides / —) is defined once under the table.

## Edge Cases
- **Claim with no anchor** — if a row can't be tied to a real commit/file/symbol, it is cut rather than asserted (no aspirational rows).
- **Advisory vs blocking ambiguity** — the drain currently makes council advisory (`CLAUDE.md` "COUNCIL IS ADVISORY"); the spec marks council's "veto" as *normally* blocking but *advisory during the active drain*, with both states noted so the doc stays true after the drain ends.
- **Missing memories** — `approval_gate`/`utility_focus` don't exist in this repo's memory store; the rationale cites the equivalent on-disk owner directives instead and the plan notes the substitution.
- **Phase4 cron** — `cron(phase4)` is ingestion, not a tick/tock build; the matrix scopes "cron" to the build loop and footnotes phase4 as a separate automated lane so the 38 phase4 commits aren't mis-mapped.

## Test Strategy
- Pre-filter (infrastructure): the deliverable is markdown, so the Python-AST / `bash -n` / `json.tool` checks are N/A for it; instead confirm the file is non-empty (>100 bytes) and that its markdown tables are well-formed (balanced pipes per row).
- **Grep-verifiability (the core test):** for every anchor in the Evidence map, run the corresponding grep and confirm it returns ≥1 hit — e.g. `git log --oneline | grep 'cron(tick)'`, `grep -n 'COUNCIL IS ADVISORY' CLAUDE.md`, `grep -n 'veto' .harness/scripts/council.py`. All cited anchors must resolve.
- **Accuracy (IMPLEMENTATION focus):** cross-check each matrix cell against observed behavior — cron-authored commits exist (`tick-tock-bot`), escalations were human-resolved (`resolve(council)` commit + `council_escalations_resolved` has 65 entries), council ran at gates (per-project `council_*.json` files exist).
- No browser load (infrastructure tick). `test_project.py` is not applicable to a docs-only experiment; OUTCOME re-runs the grep suite on a known-good project to confirm no repo regression.

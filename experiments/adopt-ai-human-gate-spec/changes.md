# Changes — adopt-ai-human-gate-spec

Documentation-only infrastructure tick. No code, no scripts, no workflow edits.

## Files created
- `experiments/adopt-ai-human-gate-spec/GATE_SPEC.md` (the deliverable, ~120 lines / 7.4 KB)
- `experiments/adopt-ai-human-gate-spec/plan.md` (PLAN gate artifact)
- `experiments/adopt-ai-human-gate-spec/changes.md` (this file)

## GATE_SPEC.md structure (section : line-anchor summary)
- **Banner** — what it is / when to read it.
- **Actors** — cron, council, human (with phase4 ‡ and drain ※ footnotes).
- **Loop order** — `brainstorm → plan → implement → test → review → commit → push`.
- **Ownership matrix** — 7 loop-step rows × 3 actor columns; legend Owns/Reviews/Overrides/—; 4 footnotes for the override mechanics.
- **Override ladder** — 5 rungs, human at top → cron at bottom.
- **Why this division** — 3 grounded paragraphs (cron throughput, council judgment-not-control, human intent+exceptions) + phase4/drain notes.
- **Evidence map** — 9 claims, each mapped to a runnable grep/anchor.

## Decisions made (answering council_focus)
- **Table over flowchart (PLAN focus):** the artifact answers "who decides X" — a 2-D ownership lookup. A table makes that O(1); a flowchart optimizes temporal flow, which is already captured by the one-line Loop order + row ordering. Chose table, kept the linear order line so sequence isn't lost.
- **Accuracy over aspiration (IMPLEMENTATION focus):** every row maps to observed behavior. The `approval_gate`/`utility_focus` memories named in the queue's plan_summary do **not** exist in this repo's memory store, so the rationale is anchored to the equivalent on-disk owner directives (`tick_tock_prompt.md`, `CLAUDE.md`, `council.py`, `session_state.json`) instead. Noted in plan.md Scope + Edge Cases.
- **Grep-verifiability (TESTS focus):** added a dedicated Evidence map; every cited anchor was run and confirmed to return ≥1 hit (see self-verification below).

## Self-verification run (all anchors resolve, 2026-06-28)
- `cron(tick|tock|phase4)` commits: 49 in last 200 (8 tick / 3 tock / 38 phase4)
- `ESCALATION:` / `resolve(council)` commits: 70; `council_escalations_resolved`: 65
- `veto` in `council.py`: 19 hits; auto-downgrade symbols: 15 hits
- `COUNCIL IS ADVISORY` in `tick_tock_prompt.md`: 2; `TICK-ONLY DRAIN`: 2
- `branch-guard.yml` actor carve-out: 1
- markdown tables: 20 rows, 0 malformed

## Anchor correction during build
Initial draft cited `CLAUDE.md` for the "COUNCIL IS ADVISORY" and "TICK-ONLY DRAIN" anchors; self-verification returned 0 hits there. Those phrases live in the stored cron prompt `.github/workflows/tick_tock_prompt.md` — both Evidence-map rows were corrected to point there before the IMPLEMENTATION gate.

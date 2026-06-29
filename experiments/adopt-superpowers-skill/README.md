# adopt-superpowers-skill

**Adopted:** the *Superpowers* plan-then-test discipline — as a documented
comparison + adoption decision, not a plugin install.

**Source:** Phase 4 experiment `nh-2026-05-03-superpowers-plan-first-skill`.

**Tick type:** infrastructure (no `<name>/index.html`; deliverables confined to
`deliverable_paths`).

## What shipped

- **`COMPARISON.md`** — a one-page, point-by-point comparison of Superpowers'
  enforcement model (brainstorm → written plan → test-FIRST RED/GREEN/REFACTOR →
  subagent/self review → verify-before-done, delivered as composable Markdown
  skills) against this repo's 4-gate council sequence (PLAN / IMPLEMENTATION /
  PRE-FILTER / TESTS / OUTCOME, with lessons-veto + auto-downgrade passes). Ends
  with an explicit verdict and a concrete follow-up recommendation.
- **This README** — the adoption record.

## The decision (one line)

Superpowers and the council reach the same goal — no slop ships — by opposite
routes (soft in-context discipline vs. hard out-of-process adversarial review).
They overlap on plan-first and verify-before-done; the one idea worth grafting is
**test-FIRST for Python-touching infra ticks**, filed as a follow-up, not changed
here.

## Honest scope / limitation

Upstream Superpowers is an **interactive Claude Code plugin**
(`/plugin install superpowers`). This builder runs **non-interactively** in
GitHub Actions (`claude -p`), where interactive plugin installation cannot run.
So this tick does **not** install the plugin and adds **no dependency, no
executable code, and no third-party files** — zero supply-chain surface. We
evaluate the *methodology* the plugin encodes and record an adoption decision.
Per the deliverable scope, **no pipeline file** (`council.py`, personas, gate
sequence, tick skill) is touched; any concrete pipeline change the comparison
surfaces is filed as a separate follow-up tick.

## Verification

1. `COMPARISON.md` and `README.md` both exist and are non-empty (>100 bytes).
2. `COMPARISON.md` contains all required structure: a Superpowers section, a
   council section, a mapping table, and an explicit verdict/recommendation.
3. `README.md` contains the adoption-record sections (Adopted / Source / What
   shipped / Honest scope / Verification / Council).
4. `git status` is confined to `experiments/adopt-superpowers-skill/` — no file
   outside the deliverable paths (+ process artifacts) is modified; no `<name>/`
   project directory created.
5. Infra non-regression: `python3 test_project.py <known-good-project>` still
   passes (this tick touches no pipeline code).

## Council

Per-gate verdicts saved in `council_plan.json`, `council_implementation.json`,
`council_tests.json`, `council_outcome.json`. Council is **advisory** under the
drain directive — verdicts are logged for the record and never block the ship.
PLAN gate: 7 APPROVE.

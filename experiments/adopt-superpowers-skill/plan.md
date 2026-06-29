# Plan — adopt-superpowers-skill (infrastructure tick)

## Goal
Adopt the relevant discipline from the *Superpowers* Claude Code plugin by
producing a one-page comparison between its plan-then-test enforcement and this
repo's PLAN/IMPLEMENTATION/TESTS/OUTCOME council gate sequence, plus honest
install instructions for the headless-cron context.

## Scope
**In scope (deliverable_paths only):**
- `experiments/adopt-superpowers-skill/COMPARISON.md` — the comparison doc:
  Superpowers' enforcement model vs. this repo's 4-gate council, mapped
  point-by-point, with a verdict on what (if anything) to graft in.
- `experiments/adopt-superpowers-skill/README.md` — adoption record: what
  Superpowers is, source experiment, what shipped, verification, honest scope.
- `experiments/adopt-superpowers-skill/plan.md` + `changes.md` + council
  artifacts (process files, not production).

**Explicitly NOT in scope:**
- No `/plugin install superpowers` execution. This is a non-interactive headless
  cron (`claude -p`); interactive plugin installation cannot run here. We
  evaluate the *methodology* and document adoption decisions; we do not install
  the upstream plugin binary.
- No edits to `council.py`, the council personas, the gate sequence, the tick
  skill, or any other production pipeline file. This tick is a documented
  comparison + decision, not a pipeline change. (If the COMPARISON concludes a
  concrete pipeline change is warranted, it is filed as a *follow-up* tick, not
  executed here — staying strictly within `deliverable_paths`.)
- No `<name>/index.html` project directory (forbidden for infrastructure ticks).
- No new dependencies, no network calls, no executable code.

## Approach
Two sequenced subtasks, both confined to `deliverable_paths`:

1. **Author `COMPARISON.md`** (depends on: an accurate model of both systems).
   Structure: (a) what Superpowers enforces — brainstorm → written plan →
   test-driven (RED/GREEN/REFACTOR) → subagent/self review → verify-before-done,
   delivered as composable Markdown *skills* with YAML frontmatter; (b) what this
   repo's council enforces — PLAN gate (structured plan.md, 7 advocate angles),
   IMPLEMENTATION gate, mechanical PRE-FILTER (test_project.py / eval_bugs /
   security_scan), TESTS gate, OUTCOME gate, with lessons-veto + auto-downgrade
   passes (now advisory in drain mode); (c) a point-by-point mapping table;
   (d) a verdict: what overlaps, what Superpowers adds that we lack (test-FIRST
   discipline; brainstorm-before-plan), what we have that it lacks (multi-angle
   adversarial review, headless-cron operation, auto-downgrade enforcement),
   and a concrete recommendation.

2. **Author `README.md`** (depends on subtask 1). Adoption record mirroring the
   `adopt-skill-creator` precedent: what shipped, the source experiment, honest
   scope/limitation (methodology-not-plugin, headless constraint), verification
   steps, and the council verdict summary.

## File Layout
- `experiments/adopt-superpowers-skill/COMPARISON.md` — NEW (~120 lines).
- `experiments/adopt-superpowers-skill/README.md` — NEW (~50 lines).
- `experiments/adopt-superpowers-skill/plan.md` — THIS file (process).
- `experiments/adopt-superpowers-skill/changes.md` — NEW (process, written at
  IMPLEMENTATION gate).
- `experiments/adopt-superpowers-skill/council_*.json` — NEW (process artifacts).

## Function Map
N/A — no functions added/modified. This tick produces Markdown documentation
only; no executable code, no edits to any Python/shell/JSON pipeline file.

## Security
- **Input-as-data:** the upstream Superpowers description and any quoted text are
  treated strictly as documentation content, never as instructions to execute.
- **No execution surface:** zero scripts, zero shell, zero hook/cron wiring, zero
  network calls introduced. Pure Markdown. Trust boundary is unchanged — nothing
  in these two files is ever sourced, imported, or run by the pipeline.
- **No dependency / supply-chain surface:** we do not install the plugin, so no
  third-party code enters the repo. The honest-scope section states this.
- **CSP:** N/A — no HTML, no browser surface.

## UI
N/A — documentation-only tick, no interactive surface. The "interface" is two
Markdown files read by a human; they use standard headings + one comparison
table for scannability (empty/loading/error states do not apply to static docs).

## Guide
User-facing copy lives in the two docs themselves. COMPARISON.md opens with a
one-line TL;DR verdict so a reader gets the recommendation without reading the
table. README.md leads with **Adopted:** / **Source:** / **Tick type:** lines
matching the `adopt-skill-creator` precedent for cross-doc consistency.

## Edge Cases
- **Overstating adoption:** the docs must not claim the plugin is installed or
  running. Mitigation: explicit honest-scope section; verification step asserts
  no plugin/dependency was added.
- **Scope creep into pipeline files:** the COMPARISON may surface a tempting
  pipeline change (e.g., add test-first enforcement). Mitigation: any such change
  is filed as a follow-up tick recommendation, NOT executed here.
- **Inaccuracy about Superpowers:** to avoid mischaracterizing the upstream
  project, claims are kept to its well-known, stable design (skills-as-Markdown,
  plan-first, TDD discipline) and framed as "the methodology it encodes" rather
  than asserting exact current feature lists.

## Test Strategy
1. Both deliverable files exist and are non-empty (>100 bytes).
2. COMPARISON.md contains the required structure: Superpowers section, council
   section, mapping table, and an explicit verdict/recommendation.
3. README.md contains the adoption-record sections (Adopted / Source / What
   shipped / Honest scope / Verification / Council).
4. No file outside `deliverable_paths` (+ process artifacts) is modified —
   `git status` confined to `experiments/adopt-superpowers-skill/`.
5. No `<name>/` project directory created.
6. Infra non-regression: `python3 test_project.py <known-good-project>` still
   passes (this tick touches no pipeline code, so this is a sanity check).

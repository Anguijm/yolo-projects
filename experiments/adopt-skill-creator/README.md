# adopt-skill-creator

**Adopted:** the Anthropic *Skill Creator* methodology — bootstrapping reusable
skills from plain-English descriptions instead of hand-authoring Markdown
structure each time.

**Source:** Phase 4 experiment `nh-2026-05-03-claude-code-skill-creator`.

**Tick type:** infrastructure (no `<name>/index.html`; deliverables confined to
`deliverable_paths`).

## What shipped

- **`skills/50-skill-creator.md`** — a new skill that converts a plain-English
  description (or an SOP paragraph) into a well-formed skill file under
  `skills/`, conforming to this repo's design principles (under 150 lines,
  description-first, Input/Output contract). It is the meta-skill: a skill that
  creates skills. This file *is* the proof of adoption — produced by following
  the very workflow Skill Creator encodes.
- **`skills/README.md`** (+1 roster line) — registers the new skill so it is
  discoverable; the roster stays the single source of truth for what skills exist.
- **This README** — the adoption record.

## The plain-English prompt used as the demo input

> "Make me a skill that takes a sentence describing a procedure and writes a
> new skill file in our `skills/` folder, in the same shape as the existing
> ones, so I don't have to hand-write the structure every time."

Running that description through the Skill Creator methodology (clarify trigger →
check roster for duplicates → draft the six sections → pick filename `50` →
safe-output gate → self-lint → write) produced `skills/50-skill-creator.md`.

## Honest scope / limitation

The upstream Anthropic Skill Creator is an interactive Claude Code **plugin**
(`/plugin install skill-creator`). This builder runs **non-interactively** in
GitHub Actions (`claude -p`), where interactive plugin installation cannot run.
So we adopt the **methodology** (the authoring SOP the plugin encodes) as a
native repo skill — not the plugin binary. The value Skill Creator provides
(remove the manual Markdown-authoring step for new skills) is captured directly
and works in headless cron, with zero new dependencies.

Scope note: beyond the new skill file, this tick adds exactly one roster line to
`skills/README.md` (to register the new skill — its own step 7 prescribes this,
and an unregistered skill is non-discoverable). No other production file is
touched; no `<name>/` project directory is created.

## Verification

1. `skills/50-skill-creator.md` exists, non-empty (>100 bytes), and **under the
   150-line design limit** (`wc -l` → 101 lines).
2. Contains all required skill sections: Description, Trigger, Methodology,
   Input, Output.
3. Self-consistency: the produced skill satisfies the design principles it
   references in `skills/README.md`.
4. Security hardening present: the skill's step 5 is a mandatory **safe-output
   gate** that refuses to write skill content containing script tags, run-me
   shell, hook/cron wiring, or dangerous URLs — treating the input description
   as data, not instructions (addresses the PLAN-gate SECURITY objection).
5. Only the new skill + one `skills/README.md` roster line touched; no `<name>/`
   project directory created; `test_project.py` on a known-good project still
   passes (no infra regression).

## Council

PLAN gate: 5 APPROVE, 2 OBJECT (advisory — drain mode). BUGS objected to an
ambiguous filename rule and SECURITY to the prompt-injection surface of an
agent authoring files. Both were addressed before implementation: the filename
algorithm is now deterministic (highest prefix → round up to next multiple of
10) and a hard safe-output reject gate was added. Per-gate verdicts saved in
`council_plan.json`, `council_implementation.json`, `council_tests.json`,
`council_outcome.json`.

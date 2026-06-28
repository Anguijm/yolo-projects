# Plan — adopt-skill-creator (infrastructure tick)

## Goal
Adopt the Anthropic "Skill Creator" methodology into this repo by adding one
new reusable skill (`skills/50-skill-creator.md`) that encodes the
plain-English → skill-file authoring workflow, plus a README documenting the
adoption and how it was verified.

## Scope
**In scope (deliverable_paths only):**
- `skills/50-skill-creator.md` — one new skill, in this repo's existing skill
  format (Description / Trigger / Methodology / Input / Output).
- `experiments/adopt-skill-creator/README.md` — adoption record: what Skill
  Creator is, why adopted, what shipped, verification, honest limitations.
- `experiments/adopt-skill-creator/plan.md` + `changes.md` + council artifacts
  (process files, not production).

**Explicitly NOT in scope:**
- No `/plugin install skill-creator` execution. This is a non-interactive
  headless cron (`claude -p`); interactive plugin installation cannot run here.
  We adopt the *methodology* (the SOP that Skill Creator encodes), not the
  upstream plugin binary. The README states this plainly.
- No `<name>/index.html` project directory (forbidden for infrastructure ticks).
- No edits to existing skills, council.py, session pipeline, or any other
  production file outside the two deliverable paths.
- No new dependencies, no network calls, no executable code.

## Approach
Narrative, three sequenced subtasks:

1. **Author the skill** (`skills/50-skill-creator.md`). Depends on: reading the
   existing skill format (README.md design principles + 40-refine.md shape).
   The skill must be self-consistent with the repo's documented principles:
   under 150 lines, Description-first (states WHEN to trigger), Input/Output
   contract, reasoning over bare steps, composable with bootstrap/tick. Its
   methodology: take a plain-English description (or an SOP paragraph), elicit
   the trigger, draft the methodology, define Input/Output, pick the numeric
   filename prefix, and self-check against the design principles before writing.
   This skill is itself the proof-of-adoption: it is a skill that creates skills.

2. **Write the adoption README** (`experiments/adopt-skill-creator/README.md`).
   Depends on subtask 1 (references the produced file). Sections: what the
   experiment adopted, the source experiment, the plain-English prompt used as
   the demo input, the resulting skill, verification steps, and the honest
   limitation that the upstream interactive plugin is not installable in cron.

3. **Record changes** (`changes.md`) — file:line summary for the council
   implementation gate. Depends on subtasks 1–2.

Sequencing: 1 → 2 → 3, then gates IMPLEMENTATION → PRE-FILTER → TESTS → OUTCOME.

## File Layout
- `skills/50-skill-creator.md` — NEW. ~90–120 lines. New file, no existing range.
- `experiments/adopt-skill-creator/README.md` — NEW. ~60–90 lines.
- `experiments/adopt-skill-creator/plan.md` — NEW (this file).
- `experiments/adopt-skill-creator/changes.md` — NEW. file:line summary.

## Function Map
N/A — no functions added/modified. All deliverables are Markdown documentation
(skill SOP + experiment README). No Python, shell, or JS code is created or
changed.

## Security
- Threat model: documentation-only change. No code execution, no eval, no
  network I/O, no user input parsing. Trust boundary unchanged — these files are
  read by the agent at session time, same as the other six skills.
- No secrets, tokens, or credentials referenced or embedded.
- The skill instructs authors to write Markdown only and explicitly warns
  against embedding executable hooks or shell in skill files, keeping new
  agent-authored skills inside the same documentation trust boundary.
- **Prompt-injection hardening (SECURITY objection, addressed):** the skill
  treats the plain-English description as DATA, not instructions. Its
  methodology includes a mandatory final **safe-output gate**: before writing,
  the agent must verify the generated skill contains only a safe subset of
  Markdown and REJECT (do not write) if it contains `<script>`/HTML script
  tags, executable shell/code fences presented as run-me steps, hook or cron
  wiring, or non-`https`/dangerous URLs. This is a hard reject step, not a soft
  "the agent should be careful" note — content failing the gate is refused
  regardless of what the input prompt asked for. Skill files are documentation
  read by the agent; they never auto-execute, so the blast radius is bounded,
  but the gate keeps coerced executable content out of the skills/ tree.
- CSP: not applicable (no HTML/browser surface).

## UI
Not applicable — no browser/HTML surface. The "interface" is the skill file's
structure: headings the agent reads (Description, Trigger, Methodology, Input,
Output). The skill defines its own empty/edge handling in prose (see Edge Cases).

## Guide
User-facing copy lives in the skill body and README. Key labels: the skill is
titled "Skill: Create a New Skill (Skill Creator)". Trigger line tells the agent
when to fire ("author a new skill" / "turn this SOP into a skill"). README opens
with a one-line summary of what was adopted so a human skimming `experiments/`
understands it without opening sub-files.

## Edge Cases
- Plain-English description too vague to derive a trigger → skill instructs the
  author to ask one clarifying question (what event should fire this?) before
  drafting, rather than guess.
- Filename collision with an existing numeric prefix → skill specifies an
  unambiguous algorithm: take the highest numeric prefix already present in
  `skills/`, round UP to the next multiple of 10, and use that (existing max 40
  → next 50). If that prefix is somehow taken, increment by 10 until free.
- Description that implies executable behavior (a hook, a cron) → skill says
  that belongs in settings.json/workflows, NOT a skill file; redirect.
- Over-long draft (>150 lines) → skill says split or trim to honor the repo's
  "under 150 lines per skill" principle.
- Duplicate of an existing skill → skill says check `skills/README.md` roster
  first and extend the existing skill instead of adding a near-duplicate.

## Test Strategy
- Pre-filter: no Python/shell/JSON touched, so the AST/`bash -n`/`json.tool`
  checks have no targets; instead verify both Markdown deliverables exist, are
  non-empty (>100 bytes), contain all required skill sections (Description,
  Trigger, Methodology, Input, Output), and that the skill stays under the
  150-line design limit (`wc -l`).
- Self-consistency check: the new skill must satisfy the very design principles
  it references (lint it against `skills/README.md` Design Principles).
- Council TESTS gate reviews the deliverables for safety/coherence.
- OUTCOME gate confirms both files present, no regression to existing skills
  (roster README unchanged), repo still parses (`test_project.py` on a
  known-good project to prove no infra regression).

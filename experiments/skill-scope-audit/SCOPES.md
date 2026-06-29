# Skill & Command Scope Audit

**Tick:** `skill-scope-audit` (infrastructure) · source experiment `mk-2026-05-03-global-vs-project-skill-hygiene`.

Every skill (`skills/*.md`) and slash-command (`.claude/commands/*.md`) now carries an
explicit `scope:` YAML frontmatter line. This file is the human-readable audit:
the criterion, the full classification, and the justification per file.

## What the tag means

| Tag | Meaning |
|---|---|
| `global` | A **repo-agnostic capability** — useful to any agent/session regardless of the yolo-projects harness. Loading it into an unrelated context is *not* pollution. |
| `project` | **Coupled to this repo's pipeline** (tick-tock cadence, council gates, phase4 ingestion, portfolio/yolo_log state). Useful here; would be context-window pollution for an agent not working on this harness. |

The point of the tag (per the source experiment): make the scope decision *explicit* so
that future multi-agent layering can load only the skills an agent needs, instead of
pushing the whole `skills/` tree into every context window.

> **Jargon note for non-initiated readers:** terms like *tick/tock* (build cadence),
> *council* (the 4-gate × 7-angle review), *phase4* (the YouTube→experiments pipeline),
> and *yolo_log / portfolio* (the built-project ledger) are this repo's pipeline concepts,
> all defined in `CLAUDE.md` and `program.md`. A skill is `project` precisely when it
> leans on one of these.

## Classification

**Totals: 3 global · 10 project (13 files).**

### skills/

| File | Scope | Why |
|---|---|---|
| `00-bootstrap.md` | `project` | Routes a session via `.harness/session_state.json` tick/tock — pure harness glue. |
| `10-tick.md` | `project` | The YOLO build loop (deck_roadmap, yolo_log, council gates). |
| `11-tock.md` | `project` | Markdown Deck flagship session — repo-specific product. |
| `20-review.md` | `global` | Generic "send code to Gemini, triage bugs" — works on any codebase. |
| `30-phase4.md` | `project` | YouTube ingestion: `fetch_youtube_rss.py`, `experiments.json`, `CHANNELS`. |
| `40-refine.md` | `project` | Refine a *survivor* project from `yolo_log.json` — portfolio-specific. |
| `50-skill-creator.md` | `global` | Repo-agnostic meta-capability (author a skill from a description). *Caveat:* its output follows this repo's `**Description:**/**Trigger:**` format, so a consumer elsewhere would re-skin the template. |
| `README.md` | `project` | Index/documentation for *this* repo's skill system. Not an executable skill; tagged for completeness. |

### .claude/commands/

| File | Scope | Why |
|---|---|---|
| `escalation-resolve.md` | `project` | Operates on `COUNCIL_ESCALATION.md` — council-specific. |
| `plan.md` | `project` | Emits a plan matching the council PLAN-gate section structure. |
| `review.md` | `project` | Reviews diff-vs-`main` against this repo's council rubric. |
| `status-deep.md` | `project` | Renders this repo's `status` shape (phase4, cadence, portfolio). |
| `test-gen.md` | `global` | Generic pytest generation for any Python file/function. |

## Notes & follow-ups

- **Frontmatter is inert.** For `.claude/commands/*.md`, `scope:` is a custom key the Claude
  Code harness ignores (recognized keys are `description`/`argument-hint`/`allowed-tools`/`model`),
  and frontmatter is stripped from the prompt body — command behavior is unchanged. Precedent:
  `.claude/skills/close-session.md` already used YAML frontmatter in this repo.
- **`.claude/skills/close-session.md` was NOT audited this tick** — it is outside this tick's
  `deliverable_paths`. It already carries frontmatter (`name`, `description`); it should be
  tagged `project` (session-closeout ritual for this repo) in a follow-up tick that includes
  `.claude/skills/*` in scope.
- **Consuming the tag is a future tick.** This audit only makes the data explicit. A loader that
  reads `scope:` to filter which skills enter a given agent's context window is the next step
  toward multi-agent layering.
- **Borderline call:** `50-skill-creator.md` is tagged `global` for its capability, but its
  template is repo-shaped — revisit if the skill format is ever generalized.

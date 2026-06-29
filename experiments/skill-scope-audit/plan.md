# Plan — skill-scope-audit

## Goal
Make the global-vs-project scope of every skill and slash-command explicit by adding a `scope: global|project` YAML frontmatter line to each file, and summarize the audit in `SCOPES.md`.

## Scope
**In scope (strictly within `deliverable_paths`):**
- Add a `scope:` YAML frontmatter line to all 8 `skills/*.md` files.
- Add a `scope:` YAML frontmatter line to all 5 `.claude/commands/*.md` files.
- Create `experiments/skill-scope-audit/SCOPES.md` — the audit summary table + scope criterion definition.

**Explicitly NOT in scope:**
- No change to skill *behavior*, methodology text, or command bodies — frontmatter only.
- No modification to `.claude/skills/close-session.md` (it is NOT in `deliverable_paths`). It already carries YAML frontmatter; it is flagged in SCOPES.md as a recommended follow-up, not edited here.
- No new dependency, executable code, hook, cron, or `council.py` change.
- No `skill-scope-audit/` project directory at repo root (infrastructure tick → only `experiments/skill-scope-audit/`).
- No automated loader that *reads* the new `scope:` key — this tick makes the data explicit; consuming it is a future tick.

## Approach
Single mechanical pass, no sequencing dependencies between files (each edit is independent):

1. **Classify** every target file as `global` or `project` against a single criterion (below). Done up-front so SCOPES.md and the frontmatter agree.
2. **Tag skills/** — prepend a `---\nscope: <value>\n---` block above the existing `# Skill:` / `# YOLO Skills System` heading. None of these files currently have frontmatter, so prepending is non-destructive.
3. **Tag .claude/commands/** — prepend the same block above the existing `Usage:` line. These are Claude Code slash-command files; `scope:` is a custom key that the harness ignores (known keys are `description`/`argument-hint`/`allowed-tools`/`model`), and the frontmatter is stripped from the prompt body, so command behavior is unchanged. Confirmed safe by precedent: `.claude/skills/close-session.md` already uses YAML frontmatter in this repo.
4. **Write SCOPES.md** — criterion definition + a full table (file, scope, one-line justification) + the close-session.md follow-up note.

**Classification criterion:** `project` = coupled to *this* repo's tick-tock / council / phase4 / portfolio pipeline; loading it into an unrelated agent would be context-window pollution. `global` = a repo-agnostic capability (generic code review, test generation, skill authoring) useful to any session.

**Classification (13 files):**
- `skills/00-bootstrap.md` → **project** (routes via `.harness/session_state.json` tick/tock).
- `skills/10-tick.md` → **project** (YOLO build loop, deck_roadmap, yolo_log).
- `skills/11-tock.md` → **project** (Markdown Deck flagship).
- `skills/20-review.md` → **global** (generic "send code to Gemini, triage bugs").
- `skills/30-phase4.md` → **project** (fetch_youtube_rss.py, experiments.json, CHANNELS).
- `skills/40-refine.md` → **project** (survivor projects, yolo_log, learnings).
- `skills/50-skill-creator.md` → **global** (repo-agnostic meta-capability; note: output format follows this repo's convention).
- `skills/README.md` → **project** (documents this repo's skill system; index doc).
- `.claude/commands/escalation-resolve.md` → **project** (COUNCIL_ESCALATION.md).
- `.claude/commands/plan.md` → **project** (council PLAN-gate section structure).
- `.claude/commands/review.md` → **project** (council rubric, diff-vs-main).
- `.claude/commands/status-deep.md` → **project** (this repo's `status` shape, phase4).
- `.claude/commands/test-gen.md` → **global** (generic pytest generation).

Net: 3 global, 10 project.

## File Layout
- `skills/00-bootstrap.md` (modify: +3 lines at top)
- `skills/10-tick.md` (modify: +3 lines at top)
- `skills/11-tock.md` (modify: +3 lines at top)
- `skills/20-review.md` (modify: +3 lines at top)
- `skills/30-phase4.md` (modify: +3 lines at top)
- `skills/40-refine.md` (modify: +3 lines at top)
- `skills/50-skill-creator.md` (modify: +3 lines at top)
- `skills/README.md` (modify: +3 lines at top)
- `.claude/commands/escalation-resolve.md` (modify: +3 lines at top)
- `.claude/commands/plan.md` (modify: +3 lines at top)
- `.claude/commands/review.md` (modify: +3 lines at top)
- `.claude/commands/status-deep.md` (modify: +3 lines at top)
- `.claude/commands/test-gen.md` (modify: +3 lines at top)
- `experiments/skill-scope-audit/SCOPES.md` (NEW, ~50 lines)
- `experiments/skill-scope-audit/plan.md` (this file), `changes.md`, `council_*.json` (process artifacts)

## Function Map
N/A — no functions added/modified. Markup/frontmatter-only change.

## Security
No execution surface. The added `scope:` key is inert metadata. Slash-command frontmatter is stripped from the prompt by the Claude Code harness; an unknown key cannot alter `allowed-tools` or `model`. No untrusted input parsed, no network call, no new dependency. Threat model: a malformed frontmatter block could break command parsing — mitigated by the PRE-FILTER YAML-parse check on every modified file.

## UI
No interactive UI. Readability concerns: frontmatter sits above the H1 so the rendered heading is unaffected on GitHub. SCOPES.md uses a single sortable table for at-a-glance scanning, with the criterion stated before the table (no "loading/empty/error" states — static doc).

## Guide
SCOPES.md opens with a one-paragraph definition of `global` vs `project` so a future reader (human or agent) knows what the tag *means* before acting on it. Each row carries a one-line justification so the classification is auditable without re-reading the skill.

## Edge Cases
- File already has frontmatter → only `.claude/skills/close-session.md` does, and it is out of scope; all 13 in-scope files are confirmed frontmatter-free, so prepend is safe (no double `---`).
- `skills/README.md` is an index doc, not an executable skill → still tagged (`project`) for completeness; SCOPES.md notes it is documentation.
- Borderline `global` calls (skill-creator) → flagged with a caveat in SCOPES.md rather than silently resolved.
- A consuming tool that splits on the first `---` must tolerate the block → standard YAML frontmatter, validated in pre-filter.

## Test Strategy
- PRE-FILTER: for every modified file, parse the leading `---...---` block with `yaml.safe_load` (or a regex + `json`-free check) and assert it yields a dict containing `scope` ∈ {`global`,`project`}. Assert exactly one frontmatter block per file (no duplication).
- OUTCOME: `grep`-verify all 13 files carry the line; confirm SCOPES.md table row-count == 13; confirm no `skills/*` or `.claude/commands/*` file lost body content (line count delta == +3 each). Run `python3 test_project.py markdown-deck` (a known-good project) to confirm no repo-wide regression from the edits.

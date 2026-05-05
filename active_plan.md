# Active plan — yolo-projects → V0.3.1 canonical conformance

**Status:** Plan v1, awaiting human approval before any restructure begins.
**Branch:** `claude/work-in-progress-wPNxa`.
**Base:** `main` @ `e06930a`.
**Risk level:** HIGH — touches the running hourly cron pipeline. Plan-first is mandatory.

## Why now

`harness-cli` released V0.3.1 with a clean canonical layout (`.harness/council/*.md` for personas, `.harness/learnings.md`, `.harness/scripts/council.py`, `.harness/session_state.json`, etc.) plus new dev-tooling commands (`harness lint`, `harness recall`, `harness research`, `harness synthesize`).

This repo predates that layout. Its council infrastructure lives at the **repo root and `council/angles/`** rather than under `.harness/`. As a result:

- `harness check` and `harness research` can't find this repo's personas (they hardcode `.harness/council/`).
- `drift-check.yml` would flag every weekly run because the topology genuinely is non-canonical.
- New canonical commands (`harness lint`, `harness recall`) operate on `.harness/learnings.md` etc. — paths that don't exist here yet.

Conformance brings the static layout in line with the canonical shape **without changing the runtime behavior of the cron pipeline.** The custom `council.py` (with auto-downgrade rules + lessons-veto + escalation) keeps doing exactly what it does today, just from a `.harness/scripts/council.py` path.

## Scope — three discrete changes

### Change 1 — Path moves (mechanical, high blast radius)

Move all harness-shaped artifact files to `.harness/`:

| Current path | New path | Notes |
|---|---|---|
| `council/angles/{bugs,cool,guide,lessons,security,ui,usefulness}.md` | `.harness/council/{...}.md` | Personas. 7 files. |
| `council.py` | `.harness/scripts/council.py` | The runner. Update internal path references. |
| `council_rules.md` | `.harness/scripts/council_rules.md` | Documentation alongside the runner. |
| `learnings.md` | `.harness/learnings.md` | Steering-loop artifact. ~3000 lines. |
| `session_state.json` | `.harness/session_state.json` | Auto-updated by post-commit hook (when added). |
| `yolo_log.json` | `.harness/yolo_log.json` | **Keep `.json` extension** (this repo's format is a JSON array, not the canonical `.jsonl` — format-conversion is out of scope; just move). |
| `model-upgrade-audit.md` | `.harness/model-upgrade-audit.md` | Model-bump checklist. |

After the move, `_hot.md` and `phase4_*` files stay at root — they're not harness artifacts; they're runtime / project-portfolio data that belongs with the project surface.

### Change 2 — Update every reference (mechanical, automated grep + edit)

**63 references** across **25+ files** point at the old paths. All need to be updated. Grouped by file:

**Python scripts (read/write old paths):**
- `council.py` — extensive. Reads personas via `Path(__file__).parent / "council" / "angles"`; reads `learnings.md`; writes `session_state.json`. Many internal references.
- `update_hot_cache.py` — reads `session_state.json`, `yolo_log.json`.
- `update_dashboard.py` — reads `yolo_log.json`, `learnings.md`.
- `update_session_state.py` — reads/writes `session_state.json`, reads `yolo_log.json`.
- `verify_build.py`, `eval_bugs.py`, `build_memory.py`, `phase4_*.py`, `process_experiments.py`, `security_scan.py` — varying refs.

**Workflow files:**
- `.github/workflows/tick_tock.yml` — invokes `council.py` and other scripts. Path updates.
- `.github/workflows/daily_research.yml` — phase4 cron, may reference state files.

**Documentation (human-readable):**
- `CLAUDE.md`, `RESUME.md`, `README.md`, `program.md`, `agent_architecture_audit.md`, `phase4_experiments.md`, `PHASE4_REPORT.md`.
- `skills/00-bootstrap.md`, `skills/10-tick.md`, `skills/11-tock.md`, `skills/40-refine.md`, `skills/README.md`.
- `model-upgrade-audit.md` (which itself is moving — update its references to itself first, then move).

**Strategy:** programmatic find-and-replace for the simple cases (file paths in code), manual review for the markdown narrative cases (where the references read like prose and replacing them blindly could break sentences).

### Change 3 — Add canonical surface (additive)

Run `harness init --update --stack node-ts`. Expect to add (since none exist):

- `harness.yml` — config with `council.specialized: true` (the personas are 7 angles unique to this repo, not the canonical 7).
- `.github/workflows/branch-guard.yml` — **NOT compatible with the cron tick_tock workflow** (which commits directly to main). Will be **deleted from this PR's scope** after `harness init --update` adds it. Documented as a deliberate omission.
- `.github/workflows/drift-check.yml` — weekly topology check. Pin to `V0.3.1` / `12a9f3fe...`. **Compatible** with tick_tock (read-only).
- `.github/workflows/council.yml` — PR-triggered council. **Compatible** (only fires on PRs; cron commits stay autonomous).
- `.claude/hooks/{session-start,check-branch-not-merged}.sh` — Claude Code session integration. Compatible.
- `.claude/settings.json` — hook timeouts + permissions.
- `.claude/skills/close-session.md` — 11-step session-close ritual.
- `.husky/pre-push` — **NOT applicable** here (no `lint` or `typecheck` script in `package.json`; the repo is plain HTML+JS, not Node-TS as `harness init --update` will detect). Will be **deleted from this PR's scope** after init.
- `.harness/halt_instructions.md` — circuit-breaker doctrine.
- `.gitleaks.toml` — secret-scanning config.

**Lead-architect persona:** the canonical synthesizer. Yolo's `council.py` does its own synthesis (auto-downgrade rules + lessons-veto), so the canonical lead-architect.md is **architecturally not used here**. Add it as a stub file documenting "yolo uses council.py's built-in synthesis, not a lead-architect persona" — passes drift-check, documents the difference, and matches what `harness check` expects.

**Maintainability persona:** the canonical 7th. Yolo's existing 7 angles overlap partially (`bugs`, `security`) and orthogonally (`cool`, `guide`, `lessons`, `ui`, `usefulness`) with the canonical 7. We do NOT add `architecture`, `accessibility`, `cost`, `maintainability`, `product` — that would be 12 personas and double the council cost per gate. The repo's existing 7 stay; specialized mode skips the canonical 7 in drift-check.

### Change 4 — Update CLAUDE.md doctrine (additive)

Append to existing CLAUDE.md (don't rewrite):
- Section: "Canonical conformance" — point at `.harness/` paths for human readers.
- Section: "Why this repo's council doesn't use a lead-architect synthesizer" — explain the auto-downgrade + lessons-veto pattern is yolo's equivalent.
- Section: "Hook timeouts" — same rationale block as NoDep PR #15 (since JSON config doesn't carry comments).

The existing `## Responding to "status"` section stays verbatim. Yolo's specific operational discipline is preserved.

## Risk surface

- **Cron pipeline state corruption.** The hourly tick_tock workflow reads/writes `session_state.json` and `yolo_log.json`. If a cron run starts mid-restructure (we move the files but haven't yet pushed the script updates), the cron sees missing files and crashes. **Mitigation:** all moves + reference updates land in a single commit. Cron runs against either the old layout (pre-merge) or the new layout (post-merge) — never a half-state. Open the PR with `[skip council]` is NOT applicable since this repo's council.yml will be added by this PR; the cron is the live concern, not a council review.
- **Path resolution bugs.** Easy to miss a reference. **Mitigation:** comprehensive grep before commit, dry-run of `python3 .harness/scripts/council.py --help` after the move to confirm imports work.
- **Backward-compatible imports.** Any external tool / dashboard / sidecar script that points at the old paths breaks. **Mitigation:** post-merge, grep for any remaining references and patch.
- **Drift-check pin.** V0.3.1 is the latest tag. SHA `12a9f3fe5fed4f8a7ebdfc1eb97838f8a750537d`. Pinned in this PR.

## Kill criteria

- If the cron pipeline crashes within 6 hours of the merge, **revert the entire PR** and re-plan with a smaller-slice restructure.
- If `harness check` reports drift after merge, **iterate within this PR / this branch** until clean (likely a missed file move).
- If `council.py` fails to find personas at `.harness/council/`, **iterate** to fix the path resolution.

## Test plan

- [ ] Pre-merge: `python3 .harness/scripts/council.py --help` runs cleanly on the branch.
- [ ] Pre-merge: every Python script that was modified runs without import errors (`python3 -c "import update_hot_cache"` etc.).
- [ ] Pre-merge: `harness check` reports zero missing canonical files.
- [ ] Pre-merge: grep for `council/angles\|^learnings\.md\|^session_state\.json\|^yolo_log\.json\|^council\.py\|^council_rules\.md\|^model-upgrade-audit\.md` returns ONLY references inside `.harness/` (the new home) plus markdown narrative refs that mention the old paths historically.
- [ ] Post-merge: tick_tock cron's first run succeeds (or fails for an unrelated reason; not a path issue).
- [ ] Post-merge: dashboard.html still loads correctly (reads `.harness/yolo_log.json` after path updates).

## Approval gate

Yolo's existing CLAUDE.md doesn't have a 3-gate approval rule (its discipline is `respond to status from disk`). Adopting the harness V0.3.1 canonical surface ALSO doesn't impose a 3-gate rule on this repo (the new CLAUDE.md additions don't mandate plan-first for normal work).

But this specific PR is a HIGH-RISK restructure of the running cron pipeline. The plan is tracked here; the human's `approved` / `proceed` / `ship it` is the explicit gate before execution.

**Awaiting approval before any file move.**

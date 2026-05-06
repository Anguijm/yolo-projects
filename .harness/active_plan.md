# Active plan — yolo-projects → V0.3.1 canonical conformance

**Status:** Plan v2, in flight (PR + cron-pause discipline; not direct-push).
**Branch:** `claude/work-in-progress-wPNxa`.
**Base:** `main` @ `e06930a`.
**Risk level:** HIGH — touches the running hourly cron pipeline.

## Why now

`harness-cli` released V0.3.1 with a clean canonical layout (`.harness/council/*.md` for personas, `.harness/learnings.md`, `.harness/scripts/council.py`, `.harness/session_state.json`, etc.) plus new dev-tooling commands (`harness lint`, `harness recall`, `harness research`, `harness synthesize`).

This repo predates that layout. Its council infrastructure lives at the **repo root and `council/angles/`** rather than under `.harness/`. As a result:

- `harness check` and `harness research` can't find this repo's personas (they hardcode `.harness/council/`).
- `drift-check.yml` would flag every weekly run because the topology genuinely is non-canonical.
- New canonical commands (`harness lint`, `harness recall`) operate on `.harness/learnings.md` etc. — paths that don't exist here yet.

Conformance brings the static layout in line with the canonical shape **without changing the runtime behavior of the cron pipeline.** The custom `council.py` (with auto-downgrade rules + lessons-veto + escalation) keeps doing exactly what it does today, just from a `.harness/scripts/council.py` path.

## Discipline (revised v2)

**No direct push to main.** Despite yolo's existing pattern of cron commits direct to main, this restructure is a one-shot human-decided change touching running infrastructure — exactly the case PRs are for. Direct push is rejected because (a) no diff-review surface, (b) cron commits during the change window create rebase conflicts on the same files, (c) rollback by `git revert` rather than "close PR".

**Cron pause for the merge window.** The hourly `tick_tock.yml` workflow writes `session_state.json` and `yolo_log.json`. If a cron run fires mid-restructure (files moved but cron's scripts not yet on the new layout), state can diverge between root and `.harness/` paths. Mitigations in priority order:

1. **Single-commit atomic move** (primary). All file moves + every reference update land in one commit. Cron sees either the old layout (pre-merge) or the new layout (post-merge) — never half-state.
2. **Disable tick_tock.yml via GitHub Actions UI for the merge window** (secondary belt-and-braces). Re-enable after merge + verify-by-manual-trigger. **Required before merging this PR** (not before opening it; council review can happen with the cron still running because the PR doesn't move files until merged).
3. **Time the merge** between cron runs (tertiary). Hourly cron means up to 60 minutes between runs; aim to merge within 50 minutes of the last cron completion.
4. **Recovery plan if the cron breaks anyway:** diff divergent state files (`.harness/session_state.json` vs. any stale `session_state.json` at root), merge by replaying gates, hotfix commit. Recoverable in hours, not days. Documented for future-self.

**Council review on the PR.** Yolo currently has no PR-triggered council workflow. The conformance PR itself ADDS `.github/workflows/council.yml`. GitHub runs workflows from the PR's HEAD, so council.yml fires automatically when the PR opens, using the existing `GEMINI_API_KEY` repo secret (already in use by `tick_tock.yml`).

The council reviews the FULL diff (file moves + script updates + canonical surface adds + this plan), not just the plan text. More comprehensive than `--plan` review.

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

Run `harness init --update --stack python`. Expect to add (since none exist):

- `harness.yml` — config with `council.specialized: true` (the personas are 7 angles unique to this repo, not the canonical 7).
- `.github/workflows/branch-guard.yml` — **NOT compatible** with the cron tick_tock workflow (which commits directly to main). Will be **deleted from this PR's scope** after `harness init --update` adds it. Documented as a deliberate omission.
- `.github/workflows/drift-check.yml` — weekly topology check. Pin to `V0.3.1` / `12a9f3fe5fed4f8a7ebdfc1eb97838f8a750537d`. **Compatible** with tick_tock (read-only).
- `.github/workflows/council.yml` — PR-triggered council. **Compatible** (only fires on PRs; cron commits stay autonomous).
- `.claude/hooks/{session-start,check-branch-not-merged}.sh` — Claude Code session integration. Compatible.
- `.claude/settings.json` — hook timeouts + permissions.
- `.claude/skills/close-session.md` — 11-step session-close ritual.
- `.husky/pre-push` — **NOT applicable** (no `lint` or `typecheck` script; no `package.json`). Will be **deleted from this PR's scope** after init.
- `.harness/halt_instructions.md` — circuit-breaker doctrine.
- `.gitleaks.toml` — secret-scanning config.

**Lead-architect persona:** the canonical synthesizer. Yolo's `council.py` does its own synthesis (auto-downgrade rules + lessons-veto), so the canonical lead-architect.md is **architecturally not used here**. Add it as a stub file documenting "yolo uses council.py's built-in synthesis, not a lead-architect persona" — passes drift-check, documents the difference, and matches what `harness check` expects.

**Maintainability persona:** the canonical 7th. Yolo's existing 7 angles overlap partially (`bugs`, `security`) and orthogonally (`cool`, `guide`, `lessons`, `ui`, `usefulness`) with the canonical 7. We do NOT add `architecture`, `accessibility`, `cost`, `maintainability`, `product` — that would be 12 personas and double the council cost per gate. The repo's existing 7 stay; specialized mode skips the canonical 7 in drift-check.

### Change 4 — Update CLAUDE.md doctrine (additive)

Append to existing CLAUDE.md (don't rewrite):
- Section: "Canonical conformance" — point at `.harness/` paths for human readers.
- Section: "Why this repo's council doesn't use a lead-architect synthesizer" — explain the auto-downgrade + lessons-veto pattern is yolo's equivalent.
- Section: "Hook timeouts" — same rationale block as NoDep PR #15 (since JSON config doesn't carry comments).
- Section: "Cron-pause discipline for harness restructures" — captures this PR's lesson so the next restructure (e.g. format-converting yolo_log.json → yolo_log.jsonl, or migrating to canonical session_state schema) follows the same path.

The existing `## Responding to "status"` section stays verbatim. Yolo's specific operational discipline is preserved.

## Risk surface

- **Cron pipeline state corruption.** Mitigated by single-commit atomic move + UI-pause + timing. **Recovery if breakage occurs:** diff state files, merge by replay, hotfix. Hours of toil, not days.
- **Path resolution bugs.** Easy to miss a reference. Mitigation: comprehensive grep before commit, dry-run of `python3 .harness/scripts/council.py --help` after the move to confirm imports work.
- **Backward-compatible imports.** Any external tool / dashboard / sidecar script that points at the old paths breaks. Mitigation: post-merge, grep for any remaining references and patch.
- **Drift-check pin.** V0.3.1 is the latest tag. SHA `12a9f3fe5fed4f8a7ebdfc1eb97838f8a750537d`. Pinned in this PR.
- **Council review framing.** Yolo's `council.py` reviews project gates with auto-downgrade rules; this PR adds a SEPARATE PR-triggered `council.yml` that uses the canonical multi-persona synthesis pattern. Both coexist. Document the split in CLAUDE.md.

## Kill criteria

- If the cron pipeline crashes within 6 hours of the merge, **revert the entire PR** and re-plan with a smaller-slice restructure.
- If `harness check` reports drift after merge, **iterate within this branch** until clean (likely a missed file move).
- If `council.py` fails to find personas at `.harness/council/`, **iterate** to fix the path resolution.

## Test plan

- [ ] Pre-merge: `python3 .harness/scripts/council.py --help` runs cleanly on the branch.
- [ ] Pre-merge: every Python script that was modified runs without import errors (`python3 -c "import update_hot_cache"` etc.).
- [ ] Pre-merge: `harness check` reports zero missing canonical files.
- [ ] Pre-merge: grep for old paths returns ONLY references inside `.harness/` (the new home) plus markdown narrative refs that mention the old paths historically.
- [ ] **Pre-merge: PR-triggered council.yml fires and produces a verdict.** Address remediations as required.
- [ ] **Pre-merge: tick_tock.yml disabled via GitHub Actions UI** for the merge window.
- [ ] Post-merge: tick_tock cron's first run (after re-enable) succeeds.
- [ ] Post-merge: dashboard.html still loads correctly.

## Approval gate

The plan is now in flight per your "Go A" authorization. Restructure proceeds:

1. Execute file moves + reference updates + canonical surface adds in a single commit (described above).
2. Push to `claude/work-in-progress-wPNxa`.
3. Open PR.
4. Council fires automatically; surface synthesis to human.
5. Address remediations.
6. **Human pauses tick_tock.yml via Actions UI.**
7. Merge.
8. **Human re-enables tick_tock.yml; verify next cron run.**


---
name: close-session
description: Use this skill when the user says "close the session", "wrap up", "we're done for today", "let's close out", or similar. Performs the full session-closeout ritual so the next session starts clean.
---

# Close session

When the user invokes this, do the full closeout. The goal: the next session can pick up cold without context.

## Closeout checklist (run in order)

1. **Check for uncommitted changes.**
   - `git status --short`
   - If anything is uncommitted: ask whether to commit, stash, or discard. Default to committing.
   - Show the user a one-sentence summary of what's about to commit before doing it.

2. **Check the branch is pushed.**
   - `git log @{u}..HEAD` — any local commits not in upstream?
   - If yes: push to the configured branch (per CLAUDE.md / system instructions).
   - If no upstream is set: push with `-u` to the development branch.

3. **Backport check — harness file edits.**
   - Run `git log <session-start>..HEAD --name-only --pretty=format: | sort -u` against the session's commits, OR use `git diff main --name-only`.
   - If any changed files match `.harness/**`, `.claude/**`, `.github/workflows/**`, `.husky/**`, or `.gitleaks.toml`, ask: "Looks like this session edited harness files. Should any of these flow back upstream to anguijm/harness-cli? [list the files]"
   - **Backport candidates** (would another repo benefit from this exact change?): bug fixes in hooks, council.py / council.yml fixes that aren't repo-specific, ci.yml fixes, generic gitleaks rules.
   - **Skip backport** for: persona `## Scope` edits (those are intentionally repo-specific), the security_checklist's repo-specific items, custom guard steps in council.yml (e.g., greps banning a particular anti-pattern in this repo's code).
   - If the user says yes, surface the changed files and offer to open an upstream PR. Don't auto-create.

4. **Refresh `.harness/active_plan.md`.**
   - If the plan describes work that was completed this session, mark it done or replace with the next-session pickup.
   - If the plan describes work still in progress, add a "where we left off" block at the top.

5. **Failure-mode audit — structured signal for the steering loop.**
   - Heuristically detect failure events from this session by scanning:
     - Recent commit messages for `fix`, `revert`, `rollback`, `hotfix`, `oops`.
     - PR comments / council reports for verdicts of `BLOCK`, `REVISE`, `WARN`, or `FAIL`.
     - CI runs that failed (and their fix-up commits afterwards).
     - Hook misfires you remember — anything that needed `--no-verify`, manual override, or hook disabling.
     - Tool calls that errored repeatedly before working.
   - For each detected failure, ask the user one short question to fill in the schema, then append a JSONL line to `.harness/failures.jsonl`:
     ```json
     {"ts": "<ISO-8601>", "failure_class": "<enum>", "what_happened": "<one sentence>", "sensor_involved": "<which sensor caught or missed it>", "guide_gap": "<which guide should have prevented it>", "fix_sha": "<commit>", "canonical_backport": <bool>}
     ```
   - **`failure_class` enum:** one of `sensor_miss` | `sensor_false_positive` | `hook_misfire` | `council_drift` | `plan_drift` | `other`.
   - **`sensor_involved`:** lint / typecheck / test / gitleaks / council / branch-guard / git-push-hook / drift-check / human / none.
   - **`guide_gap`:** persona-scope / claude-md-doctrine / security-checklist / hook / settings.json / workflow-yml / none.
   - **`canonical_backport`:** true if another repo would hit the same failure with today's canonical template; false if it's repo-specific.
   - Skip silently if no failures detected. Most sessions won't have any.

6. **Append narrative to `.harness/learnings.md`.**
   - Add a session entry with KEEP / IMPROVE / INSIGHT / COUNCIL blocks.
   - For each failure recorded in step 5, also write a one-line human-readable narrative under IMPROVE or COUNCIL — `failures.jsonl` is the signal layer, `learnings.md` is the prose layer.
   - One-line entries are fine — but each must be a learning, not a status update.
   - Do NOT edit prior entries; append-only.

7. **Update `README.md` if user-facing surface changed.**
   - New commands, new env vars, new setup steps → update README.
   - If nothing user-visible changed, skip.

8. **Update `SESSION_HANDOFF.md` (if the repo has one).**
   - Replace contents with: current branch, last commit, next-session pickup, any blockers.
   - This is regenerated each session, not append-only.

9. **Verify branch state.**
   - `git status --porcelain` should be empty.
   - `git log @{u}..HEAD` should be empty (everything pushed).

11. **Final summary to the user.**
   - One paragraph. What got done this session, what's next, where to resume.
   - Skip technical details unless they specifically matter for the next pickup.
   - Mention any backport PRs opened against harness-cli and their status.

## When closeout fails

If something blocks closeout (uncommitted changes the user doesn't want to commit, push fails, etc.), STOP and tell the user in plain language. Don't force-push, don't discard, don't bypass.

## Output style

Plain language. Don't show the user the git commands you're running unless they ask. Just say "committing your changes", "pushing", "updating the handoff doc", etc. Surface a diff or a file only if the user asks for it.

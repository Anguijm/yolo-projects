#!/usr/bin/env bash
# PreToolUse hook for Bash commands. Blocks `git push` on a branch whose
# contents are already merged into origin/main — the failure mode of pushing
# to a branch that had already been squash-merged, leaving orphan commits.
#
# Scope: `git push` only, NOT `git commit`. Commits are local and recoverable
# (cherry-pick to a fresh branch); pushes are the risky op. Checking at commit
# time misfires on the first commit of a new branch from main when
# HEAD..origin/main is empty until after the commit lands.
#
# Detection: if the current branch is not main/master AND the directory diff
# between origin/main and HEAD is empty, the branch's content is already in
# main — it was squash-merged or rebase-merged.
#
# Input:  JSON from stdin (Claude Code hook contract), with .tool_input.command.
# Output: on block, stdout JSON with hookSpecificOutput.permissionDecision=deny.
#         on allow, exit 0 with no output.
#
# Never blocks unrelated bash commands, never blocks pushes on main/master,
# and fail-opens on infra errors (origin unreachable, jq missing).

set -u

input=$(cat)

# Fail-open if jq is missing — don't block all bash commands on a missing dep.
if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

cmd=$(echo "$input" | jq -r '.tool_input.command // ""')

# Only intercept `git push`. Word-boundary match so `git pushd` doesn't false-
# positive. `git commit` is explicitly NOT matched — see header comment.
if ! echo "$cmd" | grep -qE '(^|[[:space:]])git[[:space:]]+push([[:space:]]|$)'; then
  exit 0
fi

# False-positive guard for chained commands: if the command also contains
# `git commit`, the commit runs before the push (shell && semantics), so
# new content will exist by the time the push executes. Allow the chain
# unconditionally. (Backported from sportsdata debt #30.)
if echo "$cmd" | grep -qE '(^|[[:space:]])git[[:space:]]+commit([[:space:]]|$|[[:space:]]-)'; then
  exit 0
fi

toplevel=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "$toplevel" ]; then
  exit 0
fi
cd "$toplevel"

branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")
if [ -z "$branch" ] || [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  exit 0
fi

# Try to fetch origin/main. Fail-open on network/auth errors.
git fetch origin main --quiet 2>/dev/null || true
if ! git rev-parse --verify origin/main >/dev/null 2>&1; then
  exit 0
fi

diff_files=$(git diff origin/main..HEAD --name-only 2>/dev/null || true)
if [ -n "$diff_files" ]; then
  exit 0
fi

reason="BLOCKED: current branch '$branch' has no content-difference from origin/main."
reason="$reason This typically means the branch was already merged (squash/rebase)."
reason="$reason Any new commits here will be orphaned. Create a fresh branch from main:"
reason="$reason   git fetch origin main && git checkout -b <new-branch> origin/main"
reason="$reason If you genuinely intend to add more commits to this merged branch,"
reason="$reason disable the hook for this invocation or override in settings.json."

jq -nc \
  --arg reason "$reason" \
  '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'

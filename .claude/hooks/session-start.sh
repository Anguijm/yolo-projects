#!/usr/bin/env bash
# SessionStart hook — runs at the start of every Claude Code session.
# Surfaces the project state Claude needs before doing any work:
#   - circuit-breaker status (.harness_halt)
#   - last commit
#   - current branch
#   - active plan (first 30 lines)
#   - last council verdict (verdict + summary only)
#
# Output is plain text written to stdout, surfaced to Claude as part of the
# session-start context. Keep it short — long output dilutes attention.

set -u

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$repo_root" ]; then
  exit 0
fi
cd "$repo_root"

echo "=== harness session start ==="

# Halt check first — most important signal.
if [ -f .harness_halt ]; then
  echo "HALT ACTIVE — see .harness_halt:"
  head -5 .harness_halt | sed 's/^/  /'
  echo "Do not run council, do not push large changes. Resolve the halt first."
  echo "============================="
  exit 0
fi

branch="$(git symbolic-ref --short HEAD 2>/dev/null || echo "<detached>")"
last_commit="$(git log -1 --pretty='%h %s (%ar)' 2>/dev/null || echo "<no commits>")"
echo "Branch: $branch"
echo "Last commit: $last_commit"

if [ -f .harness/active_plan.md ]; then
  plan_lines="$(wc -l < .harness/active_plan.md | tr -d ' ')"
  echo ""
  echo "Active plan (.harness/active_plan.md, $plan_lines lines):"
  head -20 .harness/active_plan.md | sed 's/^/  /'
  if [ "$plan_lines" -gt 20 ]; then
    echo "  ... ($((plan_lines - 20)) more lines)"
  fi
fi

if [ -f .harness/last_council.md ]; then
  echo ""
  echo "Last council verdict:"
  grep -m1 -E '^Verdict:' .harness/last_council.md 2>/dev/null | sed 's/^/  /' || echo "  (no verdict found)"
fi

echo "============================="
exit 0

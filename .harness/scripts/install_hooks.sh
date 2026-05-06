#!/usr/bin/env bash
# Install harness git hooks by pointing core.hooksPath at .harness/hooks.
# Also wires up husky pre-push if .husky/ exists.
# Run once after cloning the repo.

set -eu

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"
if [ -z "$REPO_ROOT" ]; then
  echo "[install_hooks] Not inside a git repo. Run from within the checkout." >&2
  exit 1
fi

cd "$REPO_ROOT"

if [ ! -d .harness/hooks ]; then
  echo "[install_hooks] .harness/hooks not found at $REPO_ROOT/.harness/hooks" >&2
  exit 1
fi

# Make harness hooks executable (permissions can be dropped by some git operations).
chmod +x .harness/hooks/*

# If husky is installed, set hooksPath to .husky and copy post-commit there too.
# Otherwise point hooksPath at .harness/hooks directly.
if [ -d .husky ] && [ -d node_modules/husky ]; then
  npx --no-install husky 2>/dev/null || true
  if [ ! -e .husky/post-commit ]; then
    cp .harness/hooks/post-commit .husky/post-commit
    chmod +x .husky/post-commit
  fi
  echo "[install_hooks] husky detected — post-commit copied to .husky/, hooksPath managed by husky."
else
  git config core.hooksPath .harness/hooks
  echo "[install_hooks] core.hooksPath set to .harness/hooks"
fi

# Make .claude hooks executable too if they exist (they're invoked by Claude Code,
# not git, but executable bit gets dropped on some clones).
if [ -d .claude/hooks ]; then
  chmod +x .claude/hooks/* 2>/dev/null || true
fi

echo "[install_hooks] Installed: $(ls .harness/hooks | tr '\n' ' ')"
echo "[install_hooks] To uninstall: git config --unset core.hooksPath"

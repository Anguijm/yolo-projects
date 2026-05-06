#!/usr/bin/env bash
# One-time per-machine setup: load API keys for the harness from a file in
# your home directory and sync them to this repo as GitHub Actions secrets.
#
# Why: the user doesn't want to manage GEMINI_API_KEY (and friends) per repo.
# Set them once at ~/.config/harness/secrets.env, run this script in any new
# repo, and the relevant secrets are uploaded.
#
# The secrets file format is plain shell:
#   GEMINI_API_KEY=...
#   ANTHROPIC_API_KEY=...
#
# Never commit ~/.config/harness/secrets.env. It lives outside any repo.

set -eu

SECRETS_FILE="${HARNESS_SECRETS_FILE:-$HOME/.config/harness/secrets.env}"

if [ ! -f "$SECRETS_FILE" ]; then
  echo "[setup-secrets] No secrets file at $SECRETS_FILE."
  echo "[setup-secrets] Create it with one KEY=value per line:"
  echo "[setup-secrets]   mkdir -p ~/.config/harness"
  echo "[setup-secrets]   cat > ~/.config/harness/secrets.env <<EOF"
  echo "[setup-secrets]   GEMINI_API_KEY=your-key-here"
  echo "[setup-secrets]   ANTHROPIC_API_KEY=your-key-here"
  echo "[setup-secrets]   EOF"
  echo "[setup-secrets]   chmod 600 ~/.config/harness/secrets.env"
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "[setup-secrets] gh CLI not installed. Install from https://cli.github.com/" >&2
  exit 1
fi

# Verify we're in a git repo with a GitHub remote.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[setup-secrets] Not in a git repo." >&2
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || true)"
if [ -z "$REPO" ]; then
  echo "[setup-secrets] No GitHub remote detected. Run 'gh repo create' first." >&2
  exit 1
fi

echo "[setup-secrets] Syncing to $REPO"

# Read keys from the secrets file and upload each. Lines starting with # are
# comments; blank lines are skipped. Values can be quoted or unquoted.
while IFS='=' read -r KEY VALUE || [ -n "$KEY" ]; do
  case "$KEY" in
    ''|\#*) continue ;;
  esac
  # Strip surrounding quotes from value.
  VALUE="${VALUE#\"}"; VALUE="${VALUE%\"}"
  VALUE="${VALUE#\'}"; VALUE="${VALUE%\'}"
  if [ -z "$VALUE" ]; then
    echo "[setup-secrets]   skip $KEY (empty value)"
    continue
  fi
  printf '%s' "$VALUE" | gh secret set "$KEY" --repo "$REPO" --body -
  echo "[setup-secrets]   set $KEY"
done < "$SECRETS_FILE"

echo "[setup-secrets] Done. Verify at https://github.com/$REPO/settings/secrets/actions"

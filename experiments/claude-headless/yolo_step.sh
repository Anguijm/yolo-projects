#!/usr/bin/env bash
# Single-step headless Claude Code invocation.
# Usage: ./yolo_step.sh "<prompt>" [extra-claude-flags...]
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: yolo_step.sh \"<prompt>\" [extra-claude-flags...]" >&2
  exit 2
fi

prompt="$1"
shift
extra_flags=("$@")

cmd=(claude -p "$prompt" --output-format json --max-turns 6 "${extra_flags[@]}")

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  printf '[dry-run] would run:'
  printf ' %q' "${cmd[@]}"
  printf '\n'
  exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "error: claude CLI not on PATH" >&2
  exit 127
fi

max_attempts="${YOLO_MAX_ATTEMPTS:-3}"
attempt=1
resp=""
while [[ $attempt -le $max_attempts ]]; do
  resp=$("${cmd[@]}" 2>&1) && break || true
  if echo "$resp" | grep -qiE "rate.?limit|429|temporar|retry"; then
    sleep_for=$((2 ** (attempt - 1)))
    echo "[retry] transient error, sleeping ${sleep_for}s (attempt $attempt/$max_attempts)" >&2
    sleep $sleep_for
    ((attempt++))
  else
    break
  fi
done

if ! echo "$resp" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1; then
  echo "error: claude returned non-JSON" >&2
  echo "$resp" >&2
  exit 1
fi

is_error=$(echo "$resp" | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('is_error', False))")
result=$(echo "$resp" | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('result', ''))")
turns=$(echo "$resp" | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('num_turns', 0))")

if [[ "$is_error" == "True" ]]; then
  echo "[FAIL] turns=$turns" >&2
  echo "$result" >&2
  exit 1
fi

printf '[OK] turns=%s chars=%s\n' "$turns" "${#result}"
echo "$result"

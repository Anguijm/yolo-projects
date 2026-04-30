#!/usr/bin/env bash
# Chained plan -> implement -> test -> commit pipeline using headless Claude Code.
# Usage: ./chain_steps.sh <task-name> "<initial-prompt>"
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: chain_steps.sh <task-name> \"<initial-prompt>\"" >&2
  exit 2
fi

task="$1"
prompt="$2"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
step_runner="$script_dir/yolo_step.sh"

max_context_bytes="${MAX_CONTEXT_BYTES:-32768}"

run_step() {
  local label="$1"
  local input_file="$2"
  local output_file="$3"
  local context=""
  if [[ -f "$input_file" ]]; then
    context=$(head -c "$max_context_bytes" "$input_file")
    local full_size
    full_size=$(wc -c < "$input_file")
    if [[ $full_size -gt $max_context_bytes ]]; then
      context="$context

[truncated: prior output was $full_size bytes, kept first $max_context_bytes]"
    fi
  fi
  local full_prompt
  if [[ -n "$context" ]]; then
    full_prompt="$prompt

PRIOR STEP OUTPUT:
$context

CURRENT STEP: $label"
  else
    full_prompt="$prompt

CURRENT STEP: $label"
  fi
  echo "==> $label"
  if "$step_runner" "$full_prompt" > "$output_file"; then
    echo "    ok ($(wc -c < "$output_file") bytes captured)"
  else
    echo "    FAILED at step: $label" >&2
    return 1
  fi
}

tmp_plan="/tmp/yolo_chain_${task}_plan.txt"
tmp_impl="/tmp/yolo_chain_${task}_impl.txt"
tmp_test="/tmp/yolo_chain_${task}_test.txt"
tmp_commit="/tmp/yolo_chain_${task}_commit.txt"

trap 'rm -f "$tmp_plan" "$tmp_impl" "$tmp_test" "$tmp_commit"' EXIT

run_step "plan"     ""          "$tmp_plan"
run_step "implement" "$tmp_plan" "$tmp_impl"
run_step "test"      "$tmp_impl" "$tmp_test"
run_step "commit"    "$tmp_test" "$tmp_commit"

echo "chain complete for task: $task"

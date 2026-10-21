#!/usr/bin/env bash
# Local engine benchmark (plan.md). Start ONLY after ops sends GO.
#   run.sh            preflight, then the whole run inside one scope with memguard watching it
#   run.sh --inner    what runs inside the scope (do not call by hand)
# Terms from ops (2026-10-22): scope MemoryMax=32G MemorySwapMax=0, memguard floor 20 GB, port 1254,
# no ptt services touched, swap checked first, no downloads.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
PORT=1254
OUT=${OUT:-$HERE/results-$(date +%F)}
ENG_PTT=$HOME/ptt/src/llama.cpp/build/bin           # what ptt runs, 2026-10-09
ENG_MF=$HOME/mini-forge/llama.cpp/build/bin         # serve_llm.sh, 2026-08-22 (server only, no llama-bench)
ENG_NEW=$HOME/llm-bench/llama.cpp-master/build/bin  # master 1d88cb0, 2026-10-20
M_MOE=$HOME/ptt/models/qwen3-30b-a3b-instruct-2507-q4_k_m.gguf
M_DENSE=$HOME/llm-models/Qwen3.8-27B-UD-Q6_K.gguf

if [[ ${1:-} != --inner ]]; then
  for m in "$M_MOE" "$M_DENSE"; do [[ -s $m ]] || { echo "missing model $m (no downloads: tell ops)"; exit 1; }; done
  for e in "$ENG_PTT/llama-bench" "$ENG_NEW/llama-bench" "$ENG_PTT/llama-server" "$ENG_MF/llama-server" "$ENG_NEW/llama-server"; do
    [[ -x $e ]] || { echo "missing engine $e"; exit 1; }
  done
  swap_used=$(awk '/SwapTotal/{t=$2}/SwapFree/{f=$2}END{print int((t-f)/1024)}' /proc/meminfo)
  avail=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
  echo "preflight: swap used ${swap_used} MiB, MemAvailable ${avail} GB"
  (( swap_used < 512 )) || { echo "swap in use, stopping (ops term)"; exit 1; }
  (( avail >= 60 )) || { echo "MemAvailable under 60 GB, stopping"; exit 1; }
  ss -tln | grep -q ":$PORT " && { echo "port $PORT busy"; exit 1; }
  mkdir -p "$OUT"
  "$HOME/ops/bin/memguard" engine-bench.scope 20 &
  timeout 7200 systemd-run --user --scope --unit=engine-bench -p MemoryMax=32G -p MemorySwapMax=0 \
    env OUT="$OUT" bash "$0" --inner 2>&1 | tee "$OUT/run.log"
  wait
  grep 'engine-bench' "$HOME/.local/state/memguard.log" | tail -2 | tee -a "$OUT/run.log"
  exit 0
fi

# ---- inside the scope ----
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
log() { echo "$(date '+%F %T') $*"; }
server_pid=
stop_server() { [[ -n $server_pid ]] && kill "$server_pid" 2>/dev/null && wait "$server_pid" 2>/dev/null; server_pid=; }
trap stop_server EXIT

for model in "$M_MOE" "$M_DENSE"; do
  mname=$(basename "$model" .gguf)
  for eng in PTT NEW; do
    dir=ENG_$eng
    log "llama-bench $eng $mname"
    timeout 1800 "${!dir}/llama-bench" -m "$model" -ngl 99 -p 512 -n 128 -d 4096,16384 -r 2 -o json \
      > "$OUT/bench-$eng-$mname.json" 2> "$OUT/bench-$eng-$mname.err" || log "llama-bench $eng $mname failed ($?)"
  done
  for eng in PTT MF NEW; do
    dir=ENG_$eng
    log "chat $eng $mname"
    "${!dir}/llama-server" -m "$model" -ngl 99 -c 16384 --host 127.0.0.1 --port $PORT \
      > "$OUT/server-$eng-$mname.log" 2>&1 &
    server_pid=$!
    timeout 1200 python3 "$HERE/chat_bench.py" $PORT "$eng $mname" "$OUT/chat.jsonl" \
      > /dev/null || log "chat $eng $mname failed ($?)"
    stop_server
  done
done
log "scope memory.peak $(( $(cat "$cg/memory.peak" 2>/dev/null || echo 0) / 1048576 )) MiB"
log "done"

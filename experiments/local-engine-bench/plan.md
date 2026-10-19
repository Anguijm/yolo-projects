# Plan: local inference engine benchmark on the MS-S1 (cards dc-2026-10-18-dwarfstar-deepseek-strix-halo,
# dc-2026-10-16-specialized-inference-engine-per-gpu-model, dc-2026-10-18-terminal-bench-mini-token-efficiency)

Written 2026-10-20 (JST). Status: PARKED by John 2026-10-20 ("skip the benchmark for now, keep it in todo"). Ops had approved the schedule (fresh build any time, CPU only; GPU runs in the 22:00-03:45 window, port 1254, MemoryMax=32G, memguard 20). Re-check in with ops before running.

## Finding: the cards as written do not fit this machine
- FACT (antirez/deepseek-v4.1-flash-gguf on Hugging Face): DeepSeek V4.1 Flash for DwarfStar is 340.60 GiB to
  download at Q2, with 151.77 GiB of main weights; the page says a 128 GB machine can only run it by streaming
  from SSD. The MS-S1 has 128 GB unified, of which dictation holds 27 GB all the time. Ops' download cap is 60 GB.
- FACT (dwarfstar.sh): DwarfStar's Strix Halo backend is ROCm (built with `make strix-halo`); there is no Vulkan
  backend listed and no pipx package. Checked here: no ROCm toolchain is installed (no hipcc, no /opt/rocm);
  llama.cpp on this box is Vulkan only.
- Assessment: the second card's engines (DFlash-2 builds, vLLM forks) also need ROCm (or CUDA). Installing the ROCm
  SDK system-wide is a separate decision with risk to the working ROCm venvs (mini-forge CLAUDE.md: "Do not
  casually reinstall the ROCm venvs"), so it is not part of this plan.

## What can be measured within the limits (proposal)
Question it answers: is the dictation stack's llama.cpp as fast as it can be on this GPU, and does a newer
build help? (The card's own stated payoff: push-to-talk latency.)
- Engines: (a) ~/ptt/src/llama.cpp, Vulkan, 2026-10-09 (what ptt runs); (b) ~/mini-forge/llama.cpp, Vulkan,
  2026-08-22 (serve_llm.sh); (c) a fresh llama.cpp master, Vulkan, built in a new directory (source ~0.1 GB,
  build ~10 min CPU).
- Models: already on disk, no download: qwen3-30b-a3b-instruct-2507 Q4_K_M (17.3 GB, the ptt-large model) and
  Qwen3.8-27B-UD Q6_K (20.5 GB, the writer model).
- Measures: llama-bench prompt processing (512 tokens) and generation (128 tokens), at context 4k and 16k; then
  the same fixed 10-turn growing conversation through llama-server's OpenAI-compatible endpoint, recording
  time to first token and tokens/s per turn. Same prompts, same flags as ptt (-ngl 99, -c 16384).
- Memory: one model at a time, about 18-24 GB resident plus KV cache. Run under
  `systemd-run --user --scope -p MemoryMax=32G`, memguard floor: stop if MemAvailable < 20 GB.
- Download: 0 GB of weights; about 0.1 GB of source.
- Window: a daytime slot when no training or writer job is due and dictation is idle; ops to pick. About 45 min.
- Output: a table of tokens/s per engine x model x context, and a one-line verdict: switch ptt's build or not.
  Nothing is switched without John's go.

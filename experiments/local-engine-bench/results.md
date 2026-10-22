# Results: local engine benchmark, 2026-10-22

Verdict: **do not switch dictation's llama.cpp build for speed.** The fresh build (master 1d88cb0) reads long
prompts faster, 38% faster for the dictation model at 16k context, but it writes text at the same speed as
the build dictation already runs. In a dictation-sized chat it answered in the same 0.13 s.
A newer build is worth taking only if dictation starts sending long contexts, or for a fix of its own.

Run: 08:56:56 to 09:11:57 JST (15 min), on ops' GO after writer v2 training. `run.sh`, exit 0, no errors.
Scope MemoryMax=32G, MemorySwapMax=0, nice 5, memguard floor 20 GB. memory.peak 32768 MiB (the cap,
nothing killed: most likely mmapped model pages counted as page cache); lowest MemAvailable 91 GB.
Raw data: `results-2026-10-22/`.

## llama-bench (tokens per second, mean of 2 runs, Vulkan, -ngl 99)

| model | test | ptt build 79e2e74 (2026-10-09) | master 1d88cb0 (2026-10-20) | change |
|---|---|---|---|---|
| qwen3-30b-a3b Q4_K_M | prompt 512 at 4k | 904.4 | 972.0 | +7% |
| qwen3-30b-a3b Q4_K_M | prompt 512 at 16k | 369.3 | 510.9 | +38% |
| qwen3-30b-a3b Q4_K_M | generate 128 at 4k | 80.2 | 80.1 | 0 |
| qwen3-30b-a3b Q4_K_M | generate 128 at 16k | 55.3 | 55.5 | 0 |
| Qwen3.8-27B Q6_K | prompt 512 at 4k | 303.3 | 312.9 | +3% |
| Qwen3.8-27B Q6_K | prompt 512 at 16k | 224.2 | 268.5 | +20% |
| Qwen3.8-27B Q6_K | generate 128 at 4k | 9.9 | 9.9 | 0 |
| Qwen3.8-27B Q6_K | generate 128 at 16k | 9.6 | 9.6 | 0 |

The mini-forge build (2026-08-22) has no llama-bench, so it appears only in the chat test.

## 10-turn chat through llama-server (128 tokens per reply, temperature 0, -c 16384)

| model | engine | time to first token, mean | generation t/s, mean |
|---|---|---|---|
| qwen3-30b-a3b | ptt | 0.13 s | 91.1 |
| qwen3-30b-a3b | mini-forge | 0.16 s | 91.1 |
| qwen3-30b-a3b | master | 0.13 s | 91.5 |
| Qwen3.8-27B | ptt | not measured | 10.0 |
| Qwen3.8-27B | mini-forge | not measured | 10.0 |
| Qwen3.8-27B | master | not measured | 10.0 |

The server reuses the cached conversation, so each turn processes only the new message (about 20 to 75
tokens). That is why the chat shows no prompt-speed difference between builds.

Qwen3.8-27B is a reasoning model: in 8 of 10 turns it spent all 128 tokens thinking before any visible text,
so time to first visible token could not be measured. Its generation speed comes from the server's own timings.

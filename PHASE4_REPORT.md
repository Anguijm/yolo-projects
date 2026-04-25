# Phase 4 Pipeline — Comprehensive Report

**Snapshot date:** 2026-04-25
**Source-of-truth files** (read live, never recall): `phase4_run.json`, `experiments.json`, `session_state.json`, `_hot.md`, `fetch_youtube_rss.py` (CHANNELS dict).

---

## 1. Executive Summary

Phase 4 is the **YouTube Research Pipeline** — the daily cron that ingests new videos from a curated channel roster, extracts experiment proposals, runs them through a council-graded cull, promotes winners into the YOLO tick queue, and reflects outcomes back into project memory. It is the upstream feeder for everything the tick-tock builder builds.

**Current state at a glance:**
- Last cron run: **2026-04-24 22:24 UTC** — 7.9 hours ago — **success** (within the 12h freshness window).
- 11 channels scanned, 0 feeds failed, 12 new videos found, 4 new experiments added.
- Lifetime experiment total: **115**.
- Currently waiting at the cull: **16 backlog items**.
- **41 experiments adopted; 33 have shipped with concrete outcomes** that are now load-bearing in the loop.
- Approved tick queue: **10 infrastructure items** ready to build.
- Open council escalations: **0**. Deferred: **1** (`adopt-bare-agent` PLAN, awaiting `CONSTRAINTS.md`).
- 63 escalations resolved across the project's lifetime.

The pipeline is healthy. The discard/defer logic is doing real work — only ~41/87 evaluated experiments (47%) are adopted; the rest are filtered out for scope, redundancy, or low signal.

---

## 2. Pipeline Architecture

Phase 4 is one of two GitHub Actions cron workflows in this repo:

| Workflow | Purpose | Schedule |
|---|---|---|
| **`Daily YouTube Research (Phase 4)`** | Ingests new videos, generates experiment proposals, culls them with council, promotes winners to tick queue | Daily at ~22:24 UTC (06:24 JST) |
| **`Tick-Tock Builder (Hourly)`** | Pops from tick queue, runs 4-gate council build (PLAN→IMPL→TESTS→OUTCOME), commits, pushes | Hourly + on workflow_dispatch |

The two workflows are decoupled. Phase 4 is the *feeder*; Tick-Tock is the *consumer*.

### End-to-end flow

```
[ YouTube RSS feeds (11 channels) ]
            |
            v
[ fetch_youtube_rss.py ]
            |
            +-- video_id, title, published_date written to disk
            v
[ Phase 4 cron — Daily YouTube Research ]
            |
            +-- Phase 1: Ingest new videos since last run
            +-- Phase 2: Generate experiment proposals via Gemini
            +-- Phase 3: Cull each via council (boring-but-high-ROI filter)
            +-- Phase 4: Reflect (write outcomes back to learnings.md)
            v
[ experiments.json ]  status flows: backlog -> done -> adopted | discarded | deferred
            |
            v
[ tick_queue_approved (in session_state.json) ]
            |
            v
[ Tick-Tock Builder cron, hourly ]
            |
            v
[ experiments/<name>/ deliverables, council artifacts, _hot.md update ]
```

### Channel roster (authoritative — `fetch_youtube_rss.py:CHANNELS`)

11 channels, council-evaluated for signal quality (8-10/10 retained):

| Channel | YouTube ID | Notes |
|---|---|---|
| @NateBJones | UC0C-17n9iuUQPylguM1d-lQ | Original roster |
| @MLOps | UCG6qpjVnBTTT8wLGBygANOQ | Original roster |
| @DavidOndrej | UCPGrgwfbkjTIgPoOh2q1BAg | Original roster |
| [un]prompted | UC5GCrYGsm7EHQzQZj65A-5w | Original roster |
| @NateHerk | UC2ojq-nuP8ceeHqiroeKhBA | Original roster |
| @swyx | UC50YKpKY_2Y86Qo4DZY3mMQ | Council-added (signal 8-10/10) |
| @GregKamradt | UC7mHKIdjuKTJVamHqR5JTRg | Council-added |
| @AIJasonZ | UCrXSVX9a1mj8l0CMLwKgMVw | Council-added |
| @echohive | UCL7przoMtZTmiQMhc9ifIww | Council-added |
| @ShawTalebi | UCa9gErQ9AE5jT2DZLjXBIdA | Council-added |
| @Mark_Kashef | UCHkzp52CldSPZqU5T49mOnA | Council-added |

`fetch_youtube_rss.py` uses unauthenticated YouTube RSS feeds — no API key, no rate-limit risk, no credential rotation. The current `parse_entries()` function is title-only ingestion (no transcript fetch); experiment generation runs against the title + Gemini knowledge.

---

## 3. Cron Health (Live)

Read from `phase4_run.json` at this report's snapshot time:

| Field | Value |
|---|---|
| `last_run_utc` | 2026-04-24T22:24:34Z (06:24 JST) |
| Age | **7.9 hours** |
| Freshness status | **success** (< 12h window) |
| `channels_scanned` | 11 |
| `feeds_successful` | 11 |
| `feeds_failed` | 0 |
| `new_videos_found` | 12 |
| `new_experiments_added` | 4 |
| `total_experiments` | 115 |
| `backlog_count` | 16 |

**Freshness rules** (per `CLAUDE.md`):
- `<12h` → success
- `12-24h` → stale
- `>24h` → failed (surface prominently)

The cron has been running consistently. No feeds failing means YouTube RSS is healthy and our channel IDs are still valid.

---

## 4. Lifecycle State Machine

Every experiment moves through this state machine:

```
[ ingested from RSS ]
        |
        v
   [ backlog ]      <-- 16 currently here, waiting for next cull
        |
        v
   [ done ]         <-- 44, evaluated and verdict assigned
        |
        +--> [ adopted ]   <-- 17, fully promoted into the portfolio
        +--> [ deferred ]  <-- 20, parked for later (with rationale)
        +--> [ discarded ] <-- 16, rejected (with rationale)
        +--> [ skipped ]   <--  2, rare — not evaluated at all
```

**Status counts (115 total):** 44 done, 17 adopted, 20 deferred, 16 discarded, 2 skipped, 16 backlog.

**Verdict counts (when set):** 41 adopt, 15 discard, 20 deferred, 11 discarded, 10 adopted (the `verdict` and `status` fields use slightly different labels — counts overlap by lifecycle).

**Conversion math:**
- 99 experiments have been evaluated (115 total minus 16 backlog).
- Of those, 41 carry `verdict=adopt` (~41% adoption rate).
- 16 discarded + 20 deferred = 36 rejected/parked (~36% filter-out rate).
- The rest are in transitional states.

This is the system working: it accepts ideas readily but actively filters about 1 in 3 for scope/redundancy/low-value reasons.

---

## 5. What the Pipeline Has Delivered (33 Adopted with Outcomes)

These are the experiments that have not just been approved but have produced concrete artifacts that are now part of the YOLO loop. Grouped by category for readability.

### 5.1 Build pipeline foundations

| ID | What it shipped |
|---|---|
| `up-2026-03-31-personal-ai-infrastructure` | **The Council itself** — 7-angle review skill that gates every build. Originally 2 angles (ssl-check pilot), expanded to 6, now the standard for all builds including cron. |
| `nh-2026-03-30-codex-plan-claude-execute` | **3-phase build pipeline in cron**: Phase 1 PLAN (idea filter + vertical outline + Gemini critique), Phase 2 BUILD, Phase 3 REVIEW (6-angle council). Gemini validates plans before any code is written. |
| `mlops-2026-03-25-qrspi-vertical-planning` | **Vertical planning protocol** — write structure outline (types, signatures, DOM IDs) before coding. env-diff: 7/7 tests on first try, 52s build vs 3 fix rounds without outline. |
| `nb-2026-03-25-dark-factory-pattern` | **Dark Factory Retry Loop** codified into program.md: test→fix→retest with max 3 retries, mandatory retest after Gemini fixes, gate requiring both test suite AND audit to pass. |

### 5.2 Quality gates (run before council)

| ID | What it shipped |
|---|---|
| `nb-2026-04-05-evaluative-agents-review-bottleneck` | **PRE-FILTER gate**: `test_project.py + eval_bugs.py + security_scan.py` must ALL pass before council runs. Saves Gemini calls on broken builds. |
| `mlops-2026-04-01-coding-agent-evals` | **eval_bugs.json (26 patterns)** + `eval_bugs.py` runner. Mined from 2700+ lines of learnings.md. Patterns: URL double-slash, clipboard fallback, hot-path perf, GPU leaks, prototype pollution, etc. |
| `mlops-2026-04-03-ai-code-security` | **security_scan.py — 22 regex patterns** for secrets, XSS, injection, insecure transport, missing CSP, external deps, sensitive localStorage. |
| `nb-2026-04-05-independent-observability` | **verify_build.py** — 7 independent checks (dir exists, HTML valid, JS syntax, log entry, README, dashboard fresh). Never trusts agent self-reporting. |
| `mlops-2026-04-01-continuous-model-eval` | **model-eval/** with 8 golden prompts + runner with `--compare` for regression detection. Pairs with model-upgrade-audit.md. |

### 5.3 Memory and context

| ID | What it shipped |
|---|---|
| `nh-2026-04-05-karpathy-llm-wiki-hot-cache` | **`_hot.md` hot cache** (33 lines) + `update_hot_cache.py` auto-generator. Cron reads `_hot.md` FIRST instead of the 3000+ line `learnings.md`. ~95% token reduction for context recovery. |
| `nb-2026-04-04-compounding-agent-memory` | **build_memory.py** — SQLite + FTS5 store. Imported 1916 learnings from 263 projects. Query by text, project, patterns, context. Replaces flat learnings.md scanning with instant queryable database. |
| `mlops-2026-03-17-durable-execution-agents` | **session_state.json + update_session_state.py** — file-based state persistence. Tracks tick-tock position, pending fixes, Phase 4 queue, portfolio counts, resume instructions. |
| `nh-2026-04-02-compact-at-milestones` | **3 compaction milestones** in cron prompt: after reading learnings, after build complete, after council fixes. Each summarizes and discards verbose output. |
| `mlops-2026-03-31-agent-debug-logging` | **build_log.py** — structured JSON logging per project. Events: idea_selected, plan_created, gemini_critique, build_complete, test_result, eval_bugs, council_review, fixes, shipped. |

### 5.4 Idea-quality filtering

| ID | What it shipped |
|---|---|
| `nh-2026-03-29-boring-automation-products` | **Boring-but-high-ROI filter** in cron prompt. 4 questions: would a business pay? would a dev bookmark? is it repeatable automation? is it just pretty? Plus explicit GOOD list (file converters, config generators, cost calculators). |
| `nb-2026-04-01-model-upgrade-stack-audit` | **model-upgrade-audit.md** — 4-layer checklist (prompts, retrieval, verification, orchestration) with files to audit and post-audit validation protocol. Run before any model swap. |
| `nb-2026-04-03-agent-architecture-12-pieces` | **262-line audit report** mapping our PAI agent stack against 12 critical agent pieces. Result: 5 STRONG, 5 ADEQUATE, 2 WEAK (escalation path, cost management). |

### 5.5 Reflection and self-learning

| ID | What it shipped |
|---|---|
| `mlops-2026-04-03-self-learning-feedback-loop` | **Mandatory Phase 4: REFLECT step** in cron. Every tick build appends structured reflection to learnings.md (KEEP/IMPROVE/INSIGHT/COUNCIL scores). |
| `do-2026-03-31-autoresearch-loop` | **Autoresearch loop** with metric=Gemini bug count, target=0. color-mix: iter 1 = 4 bugs, iter 2 = 0 bugs, converged in 216 seconds. |
| `do-2026-03-29-self-improving-eval-loop` | **Self-critique** subsumed into Phase 1C Gemini plan validation (catches data model issues and missing edge cases) plus 6-angle council. |

### 5.6 Skills, recipes, and meta-tooling

| ID | What it shipped |
|---|---|
| `nb-2026-03-31-agent-readable-skills` | **skills/ directory** — 6 skill files: 00-bootstrap, 10-tick, 11-tock, 20-review, 30-phase4, 40-refine. Each <150 lines with Description, Methodology, Input/Output contracts. |
| `nb-2026-03-31-skill-composability` | **Composable handoffs** — each skill defines explicit Input/Output. Bootstrap routes to Tick or Tock. All skills output to same state files (session_state.json, learnings.md, yolo_log.json). |
| `st-2026-04-05-skill-creator-meta-agent` | **harness `learn` command (490 lines)** — scans completed plans, extracts patterns (type, council weights, architecture, edge cases), generates reusable recipe .md files. |
| `nb-2026-04-04-agent-recipe-presets` | **5 recipe presets** in harness-cli: devtool, bugfix, feature, refactor, api. Each pre-loads custom council angles + plan template. |
| `nb-2026-03-28-design-md-agent-readable` | **design.md** — full color palette, typography scale, component patterns, spacing/layout rules extracted from 6 best projects. Required read before building. |

### 5.7 Multi-agent and orchestration

| ID | What it shipped |
|---|---|
| `nb-2026-03-28-mcp-tool-integration` | **MCP backbone** — gemini-analyze-code (review), gemini-brainstorm (idea evaluation), gemini-youtube-summary (Phase 4 ingestion). Already fully adopted. |
| `mlops-2026-04-01-agent-orchestration-cloud` | **Parallel agent sessions** — 3 projects built in parallel (git-resolve, cron-viz, dns-lookup) in 151s wall clock vs ~5-6min sequential. ~2x throughput gain. |
| `mlops-2026-04-02-mcp-spec-roadmap` | **Layer 5 of model-upgrade-audit.md**: MCP Spec Changes — checked at every model upgrade alongside the other 4 layers. |
| `fs-2026-04-02-junie-cli-multi-model` | **Per-angle `model_overrides`** in harness.yml — each council angle can use a different LLM (backward compatible). |

### 5.8 Partial / passive adoption

These were adopted but the loop already practiced them implicitly:

| ID | What it shipped |
|---|---|
| `nb-2026-03-24-context-compression` | Already implemented organically: learnings.md accumulates per-project, conversation compaction preserves key decisions, memory files store cross-session context. |
| `nb-2026-03-24-strict-linting-agents` | `.eslintrc.json` with 14 rules. 68/70 survivors pass clean. Gemini reviews already caught most lint-level issues. Config committed for future test pipeline use. |
| `nb-2026-03-29-close-the-loops` | Phase 2 refinement and Phase 3 cull already embodied close-the-loops; principle adopted implicitly. No new tooling. |
| `fs-2026-04-02-pretext-text-measurement` | Validated 30KB Pretext IIFE bundle passes YOLO inline constraint. layout() at 0.0002ms. Integration target: autoFitContent() in markdown-deck. Ready for implementation. |

---

## 6. Adopted but Pending Implementation (18 Items)

These have `verdict=adopted` (or `verdict=adopt`/`status=adopted`) but no `outcome` field yet — meaning they're approved but the deliverable hasn't shipped. Most are queued in `tick_queue_approved` (see §10).

| ID | Title (truncated) |
|---|---|
| `nb-2026-04-03-agent-guardrails-leak` | Add explicit guardrail and fallback layers to autonomous build agents |
| `mlops-2026-04-03-beyond-swebench-evals` | Build custom evals beyond synthetic benchmarks |
| `mlops-2026-04-03-self-learning-agent-memory` | Structured memory retrieval so the build agent learns from past builds |
| `nb-2026-04-07-ephemeral-layers-stack-audit` | Classify each YOLO loop dependency by shelf-life (→ shipped 2026-04-25 as `adopt-stack-audit`) |
| `do-2026-04-07-minimal-agent-pattern` | Bare-metal minimal agent loop — queue position 0 (deferred) |
| `nh-2026-04-07-claude-code-planning-mode` | Spec-decomposition pre-pass via Claude Code planning mode |
| `do-2026-04-08-claude-mythos-agentic-eval` | Backbone benchmark — queue position 1 |
| `nh-2026-04-09-claude-managed-agents` | Benchmark managed agents vs manual — queue position 3 |
| `nb-2026-04-10-five-safe-places-ai` | Strategic niche audit — queue position 2 |
| `nh-2026-04-10-claude-stop-using-best-model` | Benchmark Haiku/Sonnet vs Opus on YOLO tasks |
| `st-2026-04-12-claude-style-guide-prompt` | Encode YOLO Loop Style Guide as reusable Claude system prompt |
| `nb-2026-04-13-amazon-ai-code-quality-audit` | AI antipattern lens — queue position 8 |
| `nb-2026-04-16-fix-bottleneck-not-ai-speed` | Loop timing audit — queue position 7 |
| `nb-2026-04-16-agent-failure-mode-audit` | Failure-mode audit — queue position 6 |
| `do-2026-04-16-claude-code-opus-47-agent` | Opus 4.7 vs Sonnet on YOLO tasks |
| `nb-2026-04-19-karpathy-700-experiments` | Sweep mode — queue position 9 |
| `mlops-2026-04-20-modern-software-engineer` | AI/human gate spec — queue position 5 |
| `nh-2026-04-20-claude-session-limit` | Session checkpointing — queue position 4 |

10 of these 18 are already in the explicit tick queue (positions 0-9 below). The other 8 are adopted but not yet queued — they live as approved-but-waiting items, ready to be promoted when slot opens.

---

## 7. Discard Logic in Action (16 Discarded)

The boring-but-high-ROI filter and feedback memory rules are doing real work. Recent discards with rationale:

| ID | Why discarded |
|---|---|
| `nh-2026-04-21-claude-3d-website-design` | "UTILITY is king — no visual toys, build things people bookmark." 3D UI generation is a visual-novelty rabbit hole. |
| `nh-2026-04-19-claude-24-7-trader` | Financial trading is outside YOLO scope (dev tools, utilities, agent infrastructure — not financial systems). |
| `nb-2026-04-19-ai-replaced-managers` | Too abstract for tick-sized work — no concrete deliverable, no API surface, no benchmark. |
| `mlops-2026-04-20-new-kind-of-marketplace` | "YOLO loop as composable marketplace primitives" — same abstract category, no concrete deliverable. |
| `mk-2026-04-16-replace-openclaw-hermes-claude-code` | Misframes our stack — we are already Claude Code + GitHub Actions + minimal tooling. Nothing to consolidate. |
| `mlops-2026-03-27-specialized-agent-team` | 3-agent test complete. Works but 40% slower than single-agent 3-phase. Single-agent better. |
| `nb-2026-03-29-scheduled-tasks-monitoring` | Cron already serves this role. Scheduled Tasks would be redundant. |
| `nb-2026-03-29-close-the-loops` | Already implemented organically — no new tooling needed. |
| `nb-2026-03-25-auto-research-metric-optimization` | Phase 2 already tracked bug counts as implicit metric. |
| `nb-2026-03-24-agent-readiness-checklist` | Phase 2 refinement + Phase 3 cull already accomplished this. |
| `mlops-2026-03-27-trust-ladder-adoption` | Already at max autonomy. |
| `nb-2026-04-02-session-isolation-per-task` | Already solved by cron architecture. |
| `nh-2026-04-01-claude-md-optimization` | Cron performing well without it. |
| `do-2026-03-27-private-local-agent` | Park until hardware upgrade; start hybrid for low-complexity. |
| `nh-2026-03-31-paperclip-agent-org` | Depends on specialist experiment. |
| `tmp-2026-04-01-quantized-local-inference` | Parked — shifting to different hardware. |

**Patterns:**
- ~6 discarded for *redundancy* (already solved by cron/Phase 2/Phase 3).
- ~4 discarded for *scope* (financial systems, video editing, marketplaces — outside dev-tool/utility focus).
- ~3 discarded for *abstraction* (no concrete deliverable path).
- ~3 discarded for *hardware/infra dependency* (parked).

---

## 8. Defer Logic (20 Deferred)

Deferred ≠ discarded. These are kept alive but not actionable yet, with explicit rationale.

| ID | Why deferred |
|---|---|
| `nh-2026-04-21-claude-design-prompt-structure` | Better as a learnings.md entry later — not a distinct tick deliverable. |
| `nh-2026-04-19-claude-video-editing` | Video editing outside current portfolio scope. |
| `nh-2026-04-19-claude-design-unstoppable` | Generic "Claude iterates UI" prompting — vague deliverable. |
| `nh-2026-04-16-claude-heygen-content-pipeline` | Requires HeyGen API key + video trust model not established. |
| `nh-2026-04-16-claude-code-routines-scheduler` | Duplicates GitHub Actions scheduling. Low differentiation. |
| `nh-2026-04-13-claude-code-vs-antigravity-benchmark` | 100-task head-to-head too big for a tick. Defer until model-eval-backbone (queued #1) ships. |
| `nh-2026-04-12-claude-code-plugin-10x` | Title-only RSS extraction; needs deeper review. |
| `nh-2026-04-11-seedance-claude-code-websites` | Title-only RSS extraction; needs deeper review. |
| `nb-2026-04-17-memory-control-layer` | Overlaps with build_memory.py + infra-memory-feedback. Revisit after memory-feedback ships. |
| `nb-2026-04-14-track-model-drops-against-product-viability` | Needs a long-running service. Could reframe as a quarterly audit. |
| `nb-2026-04-11-google-quantization-inference` | Title-only RSS extraction; needs deeper review. |
| `nb-2026-04-08-analyze-leaked-code-patterns` | Title-only RSS extraction; needs deeper review. |
| `nb-2026-04-07-polymarket-bot-disruption-audit` | Title-only RSS extraction; needs deeper review. |
| `mlops-2026-04-20-tensorrt-llm-latency` | Hardware-blocked. TensorRT-LLM requires GPU infrastructure we don't have. |
| `mlops-2026-04-10-ship-agents-track2` | Title-only RSS extraction; needs deeper review. |
| `mlops-2026-04-03-mcp-day2-integrations` | Title-only RSS extraction; needs deeper review. |
| `mlops-2026-04-03-coding-agent-multiverse` | Title-only RSS extraction; needs deeper review. |
| `mk-2026-04-19-claude-design-industry` | Overlaps with two other "design brief via Claude" deferred items. Defer all three pending a focused design-prompting session. |
| `do-2026-04-20-hermes-agent` | Replacing existing orchestration is high-risk low-value now. Revisit if current stack hits limits. |
| `do-2026-04-13-claude-swift-rork-mobile` | Mobile not in current portfolio scope; Rork is external service. |

**Patterns:**
- ~9 deferred for *title-only ingestion* (needs deeper review than the cron's first-pass scan can do).
- ~4 deferred because *another in-flight tick covers them*.
- ~3 deferred for *out-of-scope* (mobile, video, financial).
- ~2 deferred for *hardware-blocked*.
- ~2 deferred for *abstraction* (better as prompt patterns than ticks).

The defer pile has natural recall mechanisms: when `model-eval-backbone` ships, the deferred Antigravity benchmark gets revisited. When memory-feedback ships, the memory-control-layer gets revisited. When hardware lands, TensorRT-LLM and quantization come back.

---

## 9. Backlog (16 Items Awaiting Cull)

These were ingested in the most recent cron run but have not yet been evaluated. Listed newest-first:

| ID | Title |
|---|---|
| `up-2026-04-23-llm-safety-mechanisms` | Audit YOLO loop outputs for safety mechanism degradation after fine-tuning or prompt chaining |
| `up-2026-04-23-confidential-ai-tee` | Evaluate Trusted Execution Environment (TEE) deployment for sensitive-data inference |
| `up-2026-04-23-beyond-chatbot-agents` | Architect a persistent-state agent layer above the YOLO loop's stateless inference |
| `nh-2026-04-23-gpt55-vs-opus47` | Benchmark GPT-5.5 vs Claude Opus 4.7 on YOLO loop coding tasks |
| `nh-2026-04-23-claude-video-editing` | Use Claude as agentic video editing orchestrator via tool calls |
| `nh-2026-04-22-openai-image2-use-cases` | Integrate OpenAI Image 2 as a UI Mockup Generator in the Dev Loop |
| `nb-2026-04-24-claude-design-sprint` | Replace UI/UX Sprint Cycles with Claude-Driven Design Sessions |
| `nb-2026-04-23-codex-no-api` | Replace REST API layer with Codex-driven direct task execution |
| `nb-2026-04-22-wiki-vs-openbrain-reliability` | Stress-Test Knowledge Retrieval Under Load Conditions |
| `nb-2026-04-22-opus-47-prompt-behavior-shift` | Audit Existing Prompts Against Opus 4.7 Behavioral Changes |
| `nb-2026-04-22-claude-code-memory-patterns` | Implement Structured CLAUDE.md Memory Layering for the YOLO Loop |
| `mlops-2026-04-24-openxdata-conference` | Audit Dev Loop for Open Data Pipeline Integration Points |
| `mlops-2026-04-22-evals-still-matter-2026` | Implement a Minimal Persistent Eval Harness for the YOLO Loop |
| `do-2026-04-24-gpt-images-native-gen` | Integrate GPT Native Image Generation into Asset Pipeline |
| `do-2026-04-24-deepseek-v4-benchmark` | Benchmark DeepSeek V4 Against Current Loop Models on Code Gen Tasks |
| `aij-2026-04-22-self-evolving-agent` | Add a Self-Reflection Step That Rewrites the Agent's Own System Prompt |

**Likely outcomes when culled** (predicting against discard/defer patterns):
- Several model-benchmark items (`gpt55-vs-opus47`, `deepseek-v4`, `opus-47-prompt-shift`) likely **defer** until `model-eval-backbone` (queue #1) ships and provides the methodology.
- `claude-video-editing` likely **discard** — out-of-scope, same category as already-deferred video items.
- `claude-design-sprint`, `gpt-images-native-gen`, `openai-image2-use-cases` — UI/visual generation items likely **defer** pending design-prompting consolidation.
- `evals-still-matter-2026`, `claude-code-memory-patterns`, `self-evolving-agent` — these have real overlap with shipped infrastructure (build_memory, REFLECT, council enforcement); likely **discard** for redundancy.
- `confidential-ai-tee`, `beyond-chatbot-agents`, `llm-safety-mechanisms` — substantive infra ideas; likely **adopt** if scoped tightly, otherwise **defer**.
- `wiki-vs-openbrain-reliability`, `codex-no-api`, `openxdata-conference` — research-flavored; likely **defer** as title-only.

The next Phase 4 cron run (~24h from snapshot) will resolve all 16. Expect ~5-7 adopts, ~5-7 defers, ~2-4 discards based on historical 41/20/16 ratios.

---

## 10. Approved Tick Queue (10 Items, Ready to Build)

These are adopted experiments with full rationale, plan summaries, and council focus already specified. The Tick-Tock Builder pops from position [0] each tick session.

### [0] adopt-bare-agent (DEFERRED — see §11)
- **Source:** `do-2026-04-07-minimal-agent-pattern`
- **Idea:** Minimal 50-line agent loop + comparison_plan.md
- **Rationale:** Research-spike counter-argument to harness-cli's complexity. If a 50-line loop can do the same job, every harness-cli feature needs justification.
- **Deliverables:** `bare_agent.py` (50-80 LOC raw Anthropic SDK + dict tool registry), `comparison_plan.md` (study protocol vs harness-cli), `README.md` (when to use which).
- **Council focus:** PLAN: 50-80 lines feasible? IMPLEMENTATION: end-to-end on trivial task? OUTCOME: three files exist, runs, comparison protocol complete.

### [1] model-eval-backbone
- **Source:** `do-2026-04-08-claude-mythos-agentic-eval` (reframed from unverifiable "Claude Mythos" marketing name)
- **Idea:** Backbone model swap benchmark — latest Claude vs current backbone on historical YOLO builds.
- **Rationale:** Low-effort, high-signal: pick N historical build specs, replay through current backbone vs latest Claude, measure clarification requests, retry counts, completion rate.
- **Deliverables:** `benchmark.py` (100-150 LOC), N historical build replay results, comparison report.
- **Council focus:** PLAN: 5 builds enough or need 10+? IMPLEMENTATION: clarification-request count robustly measurable?

### [2] strategic-niche-audit
- **Source:** `nb-2026-04-10-five-safe-places-ai`
- **Idea:** Audit YOLO loop strategic position against the 5 defensible AI niches framework.
- **Rationale:** Low-effort one-page document mapping the YOLO portfolio + dev loop to the 5 niches. Flags experiments or queue items outside defensible niches for strategic review.
- **Plan/council focus:** Not yet detailed.

### [3] eval-managed-agents
- **Source:** `nh-2026-04-09-claude-managed-agents`
- **Idea:** Benchmark Claude `/v1/agents` + `/v1/sessions` (managed orchestration) vs our manual cron approach.
- **Rationale:** If managed agents reduce coordination overhead, we can simplify tick-tock dispatch. Run one historical build through both; compare.

### [4] adopt-session-checkpointing
- **Source:** `nh-2026-04-20-claude-session-limit`
- **Idea:** Context compression + session checkpointing for long YOLO sessions.
- **Rationale:** Yesterday's 22-commit session is evidence the pain is real. Hit escalation loops that would have benefited from deterministic context resets.
- **Deliverables:** `compress_session.py` (~80 LOC) emitting markdown handoff: last N commits grouped by ticker prefix, open escalations, top-of-queue spec, memory-drift flags. Runs in ~2s.

### [5] adopt-ai-human-gate-spec
- **Source:** `mlops-2026-04-20-modern-software-engineer`
- **Idea:** Formal spec of which YOLO loop steps are AI-owned vs human-reviewed.
- **Rationale:** Your `feedback_approval_gate.md` already encodes "cron proposes, John decides" but the specific division of labor isn't documented anywhere readable.
- **Deliverables:** One-page `GATE_SPEC.md` with table (loop step × actor) showing who owns / reviews / can override. Grep-verifiable claims.

### [6] infra-failure-mode-audit
- **Source:** `nb-2026-04-16-agent-failure-mode-audit`
- **Idea:** Structured failure-mode categorization of resolved escalations.
- **Rationale:** We have exceptional raw data — 17+ resolved escalations in `session_state.council_escalations_resolved[]` with project/gate/reason/resolution. Tick produces a taxonomy (false-positive LESSONS VETO, goalpost move, parse failure, substantive BUGS, etc.).
- **Deliverables:** `audit.py` (~100 LOC) classifying by reason+resolution keyword patterns; `REPORT.md` with per-class count, example, rule-that-caught-it, signal/noise ratio, recommendations.
- **High signal-to-effort** — empirical grounding for future council enforcement ticks.

### [7] infra-loop-timing
- **Source:** `nb-2026-04-16-fix-bottleneck-not-ai-speed`
- **Idea:** Measure wall-clock time per YOLO loop stage to find non-AI bottlenecks.
- **Rationale:** Yesterday's infra-yolo-evals took 5 escalation rounds over ~6 hours; we don't know where time went.
- **Deliverables:** `timing_extract.py` (~120 LOC) pulls recent tick-tock GitHub Actions runs via `gh run view --log`, extracts `[council]` timing marks + workflow YAML stage timings, emits `timing_log.json` and `REPORT.md`.

### [8] infra-ai-code-audit-lenses
- **Source:** `nb-2026-04-13-amazon-ai-code-quality-audit`
- **Idea:** Extend infra-yolo-evals lens scripts with AI-code systemic failure patterns.
- **Rationale:** Existing `ux_completeness.py` / `mobile_usability.py` / `cult_status.py` lenses catch UX gaps. New `ai_antipatterns.py` catches: hallucinated imports/dependencies, unused imports, orphan TODOs, deadcode functions, mismatched-plan content.
- **Deliverables:** `ai_antipatterns.py` (~100 LOC), 5 checks, same pattern as existing lenses.

### [9] infra-sweep-mode
- **Source:** `nb-2026-04-19-karpathy-700-experiments`
- **Idea:** Parameterized experiment sweeps mode for the tick queue.
- **Rationale:** Loop currently does one-experiment-per-tick. Sweep mode parameterizes a single tick across N variants (same build, different model; same lens, different threshold) and runs all N in one cron slot.
- **Deliverables:** `sweep_runner.py` (~150 LOC) reading `sweep_spec.yaml`, enumerating cartesian product, writing N tick_queue_approved entries. Safety: max 10 runs/sweep, $5 budget cap.

**Realistic timeline if run sequentially:** 8 of these 10 are infrastructure (no UI), each ~10-20min for the cron when uncomplicated. Doing all 10 takes roughly **4-8 cron hours**.

**Highest signal-to-effort:**
- **#6** (`infra-failure-mode-audit`) — mines the very escalation history we keep generating.
- **#7** (`infra-loop-timing`) — quantifies the bottleneck we keep guessing at.
- **#1** (`model-eval-backbone`) — informs every future model decision.

**Robustness:** #0 (research spike), #4 (session checkpointing), #5 (gate spec).

**Strategic:** #2 (niche audit) — could change what categories we build next.

---

## 11. Deferred Escalations

One escalation is in `council_escalations_deferred[]`:

### `experiments/adopt-bare-agent` PLAN
- **Reason:** Unresolved objections after 2 attempts.
- **Deferred at:** 2026-04-25T05:35:45Z.
- **Deferred reason:** User chose to prioritize naval-scribe Letter Quality Checker tock first.
- **Underlying objections:**
  - **SECURITY critical:** `run_shell` uses `subprocess.run(shell=True)` (command injection); `write_file` allows arbitrary path traversal. Both are intentional for a "minimal reference agent" but the plan didn't acknowledge them as architectural choices.
  - **BUGS high:** No retry logic on `client.messages.create()`; `run_shell` truncates output to 2000 chars silently.
- **Resume path:** Author `experiments/adopt-bare-agent/CONSTRAINTS.md` (matching the naval-scribe CSP unsafe-inline pattern) declaring "local-developer-use only" trust boundary. Optionally tighten the BUGS items if shipping for non-research use.

The escalation file `experiments/adopt-bare-agent/COUNCIL_ESCALATION.md` remains in place; the entry is preserved with deferred_at + deferred_reason metadata so it can be resumed cleanly.

---

## 12. Resolved Escalations (Historical Reference)

`session_state.council_escalations_resolved[]` contains **63 resolved escalations** as of this snapshot. This is the dataset that `infra-failure-mode-audit` (queue #6) will mine.

Recent resolution patterns observed in the past 24h:
- Multiple naval-scribe tock escalations resolved through plan-tightening (predicate definitions, .textContent safety, recursive schema validation).
- Multiple `fix-council-bugs-hallucination` OUTCOME re-attempts with shifting goalposts; ultimately shipped via retroactive 4-gate stamps.
- One adopt-stack-audit IMPL escalation resolved by overriding scope-expansion (audit ≠ remediation) and adding Recommended Follow-Up Ticks section.
- Goalpost-move auto-downgrade fired correctly in production multiple times.

**Pending data-mining hypotheses** (to be tested by queue #6):
1. ~30-40% of escalations are LESSONS VETO false positives caught by precondition_evidence enforcement.
2. ~15-20% are goalpost moves caught by keyword-overlap auto-downgrade.
3. ~30% are substantive BUGS that need real fixes.
4. ~10% are SECURITY architecture re-litigation overruled per CONSTRAINTS.md pattern.
5. The remainder are GUIDE/UI/COOL improvements that ship after one round of fix.

---

## 13. Risks and Gaps

### Pipeline-level risks (from `STACK_AUDIT.md`)
- **Node.js 20 EOL on 2026-04-30** — 5 days after this snapshot. The cron runner installs `@anthropic-ai/claude-code` via `npm install -g` on Node 20. Fix is one line in `tick_tock.yml`; queued as a follow-up tick `infra-node-22-upgrade`.
- **`google-generativeai` SDK actively deprecated** — FutureWarning fires on every import. ~3-month risk window. Migration target: `google-genai`. Queued as `infra-genai-migration`.
- **Unpinned pip packages** — `anthropic`, `google-generativeai`, `requests` install latest-at-cron-run. Supply-chain risk. Queued as `infra-pip-pinning`.
- **YouTube RSS field handling** — `parse_entries()` writes title/video_id directly into experiments.json without HTML-unescape or video_id format validation. Queued as `infra-rss-sanitize`.
- **`requests` package installed but never imported** — `grep -rn "^import requests\|^from requests" --include="*.py" .` returns empty. Trivial cleanup queued as `infra-prune-unused-deps`.

### Phase 4 gaps
- **Title-only ingestion** — `parse_entries()` extracts only title + video_id; no transcript, no description body. Many "Extracted from YouTube RSS" rationale items are deferred precisely because we can't tell from the title alone. A transcript-fetch step would dramatically improve cull accuracy at the cost of one more API per video.
- **No cull cadence guarantee** — backlog of 16 has been growing because the cron only adds 4 new experiments per run on average but doesn't always cull immediately. The cull step is opportunistic; some items can sit for days before being evaluated.
- **No cost tracking** — every Phase 4 cycle invokes Gemini for proposal generation and council, but we have no per-cycle cost metric. The 12-piece audit flagged this as one of two WEAK areas.
- **No human escalation path** — if Phase 4 itself fails (e.g., all feeds error, or cull produces empty results for 3 days), there's no automatic alert. Also flagged as WEAK.

### Memory and operational risk
- The memory layer (`build_memory.db` + `learnings.md` + `_hot.md` + memory feedback) is increasingly load-bearing. A schema migration bug or accidental file deletion would compound across the loop. `infra-memory-feedback` ticks have been adding redundancy here.

---

## 14. How To Use This Report

This report is a **dated snapshot** like `STACK_AUDIT.md` — useful for:
- Quickly catching up on what Phase 4 has produced and what's queued.
- Understanding which experiments are real vs which are still proposals.
- Justifying queue reorderings against the actual backlog.
- Mining the discard/defer patterns when designing new ingestion filters.

**To re-derive any number in this report**, read the file cited in §1 directly. The numbers are not memoized — every value here was a live read at snapshot time.

**To extend this report:** add a new dated snapshot rather than editing this one in place. The diff between snapshots is the most valuable signal (which items moved categories, which discards were reversed, which ideas the channel roster surfaces over time).

**Recommended cadence:** regenerate when the backlog count crosses a threshold (e.g., >20), or after a major model swap, or before any strategic queue reordering decision.

---

## 15. Cross-References

- Adoption pipeline: `experiments.json`, `phase4_run.json`
- Tick queue + escalation log: `session_state.json`
- Channel roster: `fetch_youtube_rss.py:CHANNELS`
- Council mechanics: `council_rules.md`, `council.py` module docstring, `learnings.md` "Council enforcement rules are now LIVE in code"
- Status protocol contract: `CLAUDE.md`
- Live portfolio summary: `_hot.md`
- Workflow definitions: `.github/workflows/daily_research.yml`, `.github/workflows/tick_tock.yml`
- Stack dependency snapshot: `experiments/adopt-stack-audit/STACK_AUDIT.md`

---

*End of report.*

# Phase 4 backlog triage — 2026-06-24

One-shot triage that cleared the Phase 4 experiment backlog (111 → 0) by
applying an owner-preference model inferred from the existing adopt/discard
history. **No deliverables were built** — these verdicts record intent so
adopted items can be promoted to `tick_queue_approved` at the next triage.

- **111 items triaged**: **65 adopt**, **46 discard**
- Source: `experiments.json` `status_history` entries timestamped 2026-06-24
- Each record kept its original ingestion note; verdict + `status_history`
  `from→to` rationale were appended.

## Decision rubric

**Adopt** — agent-harness work on the Claude stack: context/memory discipline,
skills & reusable recipes, planning + verification/guardrails, multi-perspective
review, on-Claude-family model-tier/eval/benchmark, harness ownership/health, and
directly YOLO-buildable artifacts (generative art, dashboards).

**Discard** — consistent prior NOs: local/open-source/cheaper-model cost-cutting
(cost is not a constraint), GPU/fine-tuning infra, enterprise/SOC/org-scale
pipelines, heavyweight multi-agent OSes, vendor harness swaps, media/voice/brand
pipelines, off-domain career/policy items, plus expired and duplicate cards.

## Adopted (65)

| ID | Title | Effort | Why |
|---|---|---|---|
| `nb-2026-04-22-claude-code-memory-patterns` | Implement Structured CLAUDE.md Memory Layering for the YOLO Loop | medium | Context/memory discipline on the Claude stack — extends the hot-cache + build_memory patterns already adopted. |
| `nh-2026-05-03-claude-design-course` | Apply structured Claude prompt design patterns to YOLO loop system prompts | medium | Prompt-design discipline for loop system prompts; same family as the adopted style-guide/system-prompt work. |
| `nh-2026-05-03-claude-code-skill-creator` | Install Skill Creator globally to bootstrap all Claude Code skills via plain-English prompts | low | Skill tooling — mirrors the adopted skill-creator meta-agent (harness learn); Anthropic-native, low effort. |
| `nh-2026-05-03-superpowers-plan-first-skill` | Add Superpowers skill to enforce plan-then-test coding discipline in Claude Code | low | Plan-then-test discipline — directly reinforces the adopted vertical-planning / self-critique gates. |
| `mk-2026-05-03-global-vs-project-skill-hygiene` | Audit and promote skills to global vs. project scope as a prerequisite to multi-agent reliability | low | Skill scope hygiene; cheap, supports the skills-as-recipes architecture. |
| `nb-2026-06-11-claude-cockpit-vs-codex-ops-desk` | Map tasks to Claude (steering) vs Codex (dispatching) based on fuzziness | medium | Claude-vs-Codex task routing — extends the adopted Codex-as-planner + Claude-as-executor pattern. |
| `nb-2026-06-11-claude-md-context-file` | Maintain a claude.md standing-context file to prevent context drift across sessions | low | Standing-context file — already core practice (CLAUDE.md); confirm + tighten. |
| `nb-2026-06-11-token-burn-dashboard` | Build a personal token-burn dashboard to surface AI usage habits and expand imagination | medium | Closes the cost-management gap flagged WEAK in the PAI audit; also a YOLO-buildable dashboard. |
| `nb-2026-06-11-slash-workflows-multi-agent-personal-productivity` | Use /workflows (slash-workflows) to spawn multi-agent sub-task decomposition for complex research | low | Workflow-based sub-task decomposition; on-stack, matches parallel-agent + council adoption. |
| `mlops-2026-06-11-planning-doc-to-prevent-spaghetti-code` | Front-load a full planning document to Claude before coding to prevent spaghetti code across sessions | low | Front-loaded planning doc — same lesson as adopted vertical-planning (env-diff zero-rework evidence). |
| `mlops-2026-06-11-ifood-latency-goldilocks-recommender` | Use LLM-as-judge on conversation logs to understand true user satisfaction beyond explicit ratings | medium | LLM-as-judge on logs — applicable to judging build/council logs; fits eval discipline. |
| `do-2026-06-11-codex-context-skills-magipath` | Inject structured design context and skills into Codex to improve frontend output quality | medium | Inject design.md + skills into Codex — extends the adopted agent-readable design system. |
| `up-2026-06-11-salesforce-agentic-soc-ai-constitution` | Write an AI constitution document to codify agent behavior rules, primitives, and trust-earning criteria | low | AI constitution (rules, irreversible-action gates, audit logging) — matches adopted guardrails + security work. |
| `nh-2026-06-11-four-cs-ai-os-second-brain` | Structure a Claude Code second brain using the four-Cs framework: Context, Connections, Capabilities, Cadence | medium | Context/Connections/Capabilities/Cadence framing aligns with the existing memory+MCP+skills+cron stack. |
| `nh-2026-06-11-scoped-api-keys-permission-layer` | Implement scoped API keys per integration to enforce a read-only permission layer for Claude Code connections | low | Least-privilege scoped keys — security/guardrail match; low effort. |
| `nh-2026-06-11-subagent-persona-parallel-review` | Spin up parallel persona sub-agents to stress-test outputs from multiple stakeholder viewpoints | medium | Parallel persona reviewers — the council multi-angle pattern, already adopted. |
| `nh-2026-06-11-custom-subagent-markdown-files` | Build reusable custom sub-agent files with YAML front-matter for repeatable specialist tasks | low | Reusable sub-agent files w/ YAML front-matter — the skills/recipes pattern; on-stack. |
| `nh-2026-06-11-grill-me-context-extraction` | Use a 'Grill Me' interrogation skill to extract tacit knowledge into reusable context docs before building | low | Context-extraction interview skill; cheap, feeds planning/brainstorm. |
| `nh-2026-06-11-skills-as-reusable-recipes` | Build a personal skill library as markdown recipes to replace repetitive prompts with slash commands | medium | Direct match to adopted pre-wired recipes + skill files. |
| `nh-2026-06-11-dynamic-workflows-parallel-jobs` | Run a dynamic workflow to audit all skills in parallel with cheap scoring agents feeding one synthesis agent | medium | Fan-out scorers -> synthesis — council/parallel-agent + golden-eval family. |
| `nh-2026-06-11-opus48-effort-levels-token-efficiency` | Map personal pain points from Opus 4.7 to Opus 4.8 effort levels to find the cheapest effective setting | low | Find cheapest effective effort level — efficiency without leaving Claude; matches Haiku/Sonnet-vs-Opus benchmarking. |
| `nh-2026-06-11-claudecode-vs-codex-task-routing` | Route tasks between Claude Code and Codex based on creative vs execution phase to improve output quality | medium | Creative-vs-execution routing — reinforces the adopted Codex/Claude split. |
| `nh-2026-06-11-prompt-caching-session-preservation` | Preserve prompt cache by avoiding model switches and idle gaps over 1 hour to cut token costs 10x | low | Prompt-cache preservation — on-stack token efficiency, same discipline as the harness cache window. |
| `aij-2026-06-11-closed-loop-self-improving-agent` | Implement a closed-loop agent with cron jobs, a temporal memory log, and auto-skill-proposal to create self-improving workflows | high | Cron + temporal memory + auto-skill-proposal — this IS the YOLO loop; reinforces reflect/memory/skill-gen. |
| `mk-2026-06-11-six-dynamic-workflow-patterns` | Apply the six Claude Code dynamic workflow patterns to match task structure to agent topology | medium | Task-shape -> agent-topology patterns; reference for council/workflow orchestration. |
| `mk-2026-06-11-dynamic-workflow-personal-model-migration` | Mine local JSONL conversation history with a fan-out workflow to generate personalized model-upgrade guidance | high | Mine JSONL for upgrade guidance — model-upgrade audit + memory-mining family. |
| `mk-2026-06-11-polyskill-cross-provider-adapter` | Build a PolySkill universal adapter to convert skills bidirectionally between Claude Code and Codex | medium | Skill portability across Claude/Codex — supports the dual-tool routing already adopted. |
| `mk-2026-06-11-slash-goal-agentic-os-maintenance` | Use /goal with a rubric file to continuously self-optimize the agentic OS skill and rule set | medium | Self-optimizing skill/rule maintenance — matches the self-improving loop + skill audits. |
| `mk-2026-06-11-skill-quality-eight-tips` | Audit skill library with eight quality heuristics and the Claude Code guide agent to eliminate dead weight | low | Skill-quality heuristics audit; cheap skill-hygiene. |
| `aie-2026-06-11-agentic-retrieval-over-simple-rag` | Replace single-shot vector search with iterative agentic retrieval (search→read→assess→repeat) for agent context gathering | medium | Iterative search/grep/regex retrieval — matches adopted structured memory retrieval (build_memory FTS). |
| `aie-2026-06-11-context-optimization-strategies` | Replace full-codebase context dumps with ranked hierarchical summaries and knowledge graphs for agentic code review | medium | Ranked hierarchical summaries for code review — context-compression family (hot-cache/build_memory). |
| `aie-2026-06-11-otel-agent-observability-flywheel` | Instrument agent traces with OpenTelemetry auto-instrumentation then drive prompt/model experiments from the resulting dataset | low | OTel traces -> eval dataset — observability + eval flywheel; extends build_log/verify. |
| `aie-2026-06-11-evals-hill-climbing-zones` | Implement a three-zone hill-climbing eval loop: fix obvious harness bugs, apply model-family-specific prompt tuning, then stop before overfitting | medium | Eval hill-climbing w/ stop-before-overfit — sound eval methodology; matches golden-eval discipline. |
| `mk-2026-06-11-fable5-tiered-effort-workflow` | Route tasks across model tiers by complexity to minimize token burn | medium | Tier routing across Fable/Opus/Sonnet — on-Claude-family cost/quality balance, not local-model cost-cutting. |
| `aie-2026-06-11-async-agent-verification-loop` | Give agents MCP access to the target environment so they can self-verify before surfacing results | medium | Agent self-verifies against the real env before surfacing — the never-trust-self-report / verify_build principle. |
| `nb-2026-06-12-codex-chief-of-staff-loop` | Structure Codex Tasks With Goal-Source-Standard-Permission-Proof Loops | medium | Goal-Source-Standard-Permission-Proof loop — planning + proof-of-completion discipline. |
| `nb-2026-06-12-codex-permission-boundary-safety` | Enforce Least-Privilege Boundaries on Codex Agent Sessions | low | Least-privilege agent sessions — guardrail/security match. |
| `eh-2026-06-13-interactive-geometry-watercolor-visualizer` | Build an AI-generated interactive geometry visualizer with watercolor-style rendering | medium | YOLO-buildable single-file generative-art piece; fits the portfolio (WebGL art). |
| `mk-2026-06-14-mine-jsonl-fable-playbook` | Mine Claude Code JSONL sessions to generate a model behavior playbook | medium | Mine JSONL -> behavior playbook — memory-mining + model-upgrade family. |
| `mk-2026-06-14-behavioral-diff-cross-model` | Automate cross-model behavioral diff to quantify agent capability gaps | low | Quantified cross-model behavioral diff — model-regression/eval discipline; cheap. |
| `nb-2026-06-14-harness-ownership-audit` | Audit your AI workflows to identify harness ownership vs vendor dependency | medium | Harness-ownership mapping — a stated core value; matches dependency shelf-life classification. |
| `nb-2026-06-14-model-dependency-resilience` | Build and warm-test a fallback model routing layer for critical workflows | medium | Warm-tested fallback routing for resilience (not cost) — prudent, matches dependency-replaceability work. |
| `nh-2026-06-15-ai-person-workflow-automation` | Automate one recurring weekly workflow end-to-end with Claude to establish measurable ROI baseline | low | Fully automate one recurring workflow + measure ROI — Scheduled-Tasks + boring-but-high-ROI family. |
| `mlops-2026-06-15-context-engineering-coding-agents` | Run a timed coding agent challenge on a real domain dataset to benchmark context engineering strategies | high | Head-to-head context-engineering benchmark — eval/benchmark discipline. |
| `eh-2026-06-16-webgl-morphing-sculpture` | Build a Continuously Morphing WebGL Generative Sculpture | medium | YOLO-buildable generative-art piece; portfolio fit. |
| `eh-2026-06-16-threejs-living-symmetry` | Implement a Procedural Symmetry Engine in Three.js | medium | YOLO-buildable generative-art piece; portfolio fit. |
| `nb-2026-06-17-prune-agent-tools-harness` | Audit and prune agent tool sets to improve reliability | low | Prune tools for reliability — harness discipline (mirrors tool-deferral); cheap. |
| `nb-2026-06-17-harness-health-checklist` | Implement a five-point harness health check for every production agent | low | Five-point harness health check — matches verify_build + status + audit habit. |
| `nh-2026-06-17-five-level-second-brain` | Map each knowledge folder to its minimum viable second-brain level | medium | Right-size retrieval per knowledge folder — memory/retrieval discipline. |
| `do-2026-06-18-strategic-vs-tactical-programming-ai` | Redesign Codebase Architecture Explicitly for Agent Readability (AX) | high | Agent-experience (AX) codebase design — extends agent-readable design.md / skill-file philosophy. |
| `do-2026-06-18-blank-slate-agent-audit` | Strip Agent Config to Zero and Rebuild Only What Is Missed | low | Strip-to-zero config audit — context-bloat hygiene; cheap experiment. |
| `nh-2026-06-18-claude-code-director-mindset` | Add 'Intent + Why' Preamble to Every Claude Code Task Spec | low | Intent+Why preamble per task — already a harness convention; reinforce. |
| `nh-2026-06-18-context-window-dumb-zone-mitigation` | Instrument Claude Code Sessions to Detect and Interrupt the 'Dumb Zone' | medium | Detect/interrupt context degradation — compaction/checkpoint discipline, already adopted. |
| `aij-2026-06-18-loop-engineering-harness` | Implement a Loop-Engineer Harness with Domain Contracts and Artifact Logging | high | Domain contracts + typed artifact logging — matches the harness's contracts/logging/compounding loops. |
| `aij-2026-06-18-agent-skill-context-management` | Use Skills as Context-Efficient Capability Extensions Instead of Inline Prompts | medium | Skills by pointer vs inline — context-efficient capability extension; skills + compression family. |
| `aie-2026-06-18-eval-first-production-ai` | Define Business-Metric Evals and Growing Test Case Library Before Writing Agent Code | medium | Define evals + growing test library before code — eval-first discipline (golden eval). |
| `aie-2026-06-18-structured-prompt-versioning` | Enforce Structured Commit Messages for Prompt Changes with Failure-Reason Traceability | low | Structured commit messages w/ failure-reason traceability — matches build_log + learnings traceability. |
| `nb-2026-06-19-open-skills-portable-procedures` | Structure agent procedures as scoped markdown skills with verification contracts | medium | Scoped skills w/ verification contracts — skills + verification double match. |
| `mlops-2026-06-19-autonomy-spectrum-enterprise-agents` | Gate agent autonomy by reversibility and blast radius using a three-tier classification | medium | Gate autonomy by reversibility/blast-radius — mirrors the harness's hard-to-reverse-confirm doctrine + escalation. |
| `nh-2026-06-19-agent-loop-reason-act-observe` | Build agent loops with explicit checkable goal, hard stop condition, and separate checker agent | medium | Checkable goal + hard stop + separate verifier agent — council/verify + loop discipline. |
| `nb-2026-06-21-agent-owner-card` | Create an Agent Owner Card for Every Production Agent | low | Owner card per agent (job/sources/permissions/failure-modes) — accountability; harness-health match. |
| `nb-2026-06-21-agent-diet-review-loop` | Implement a Scheduled Diet Audit for Agent Context Sources | medium | Scheduled staleness review of context sources — context hygiene + cadence; mirrors learnings-staleness concern. |
| `mlops-2026-06-22-logs-only-observability` | Replace metrics/traces with logs-only observability for agent pipelines | medium | Logs-only, LLM-queryable observability — matches the existing structured build_log approach. |
| `nb-2026-06-23-big-task-delegation` | Hand Off a Whole Consulting-Scale Task to a Frontier Model | medium | Probe the frontier-model capacity ceiling with larger task scope — useful for sizing bigger ticks; benchmark family. |
| `nh-2026-06-23-fugu-multi-model-orchestration` | Benchmark Single-Model vs. Orchestrated Multi-Model API on Identical Task Suite | high | Benchmark single vs orchestrated multi-model — benchmark discipline; tests (and likely confirms) single-model sufficiency. |

## Discarded (46)

| ID | Title | Effort | Why |
|---|---|---|---|
| `mk-2026-05-03-hive-mind-multi-agent-os` | Build a multi-agent hive-mind with shared memory database and Telegram interface over Claude Code | high | Heavyweight multi-agent business OS — over-engineered; prior discards favor a single 3-phase agent over specialist swarms. |
| `nh-2026-05-04-voice-agent-claude-code-elevenlabs` | Build a Knowledge-Grounded Voice Agent via Claude Code and ElevenLabs in a Single Session | medium | Voice-agent/media build — off the dev-tool/sim/art YOLO focus. |
| `nh-2026-05-05-higgsfield-claude-mcp-creative-agency` | Connect Higgsfield MCP to Claude and Drive Full Brand Asset Generation from a Single Prompt | medium | Brand-asset creative-agency pipeline — off-domain. |
| `mlops-2026-06-11-rocket-ride-gpu-aggregation` | Use shared-inference model server to cut LLM inference costs via GPU aggregation | high | Shared-GPU inference cost-cutting — enterprise infra; cost is not a constraint. |
| `mlops-2026-06-11-agentic-soc-multi-agent-hunt` | Build a human-in-the-loop multi-agent pipeline using existing SOAR integrations rather than replacing them | high | Enterprise SOC/SOAR security-ops pipeline — off-domain. |
| `mlops-2026-06-11-meta-multiagent-short-video-perceiver` | Decompose content-understanding pipelines into specialized perceiver + attribution + decision agents with caching between stages | high | Enterprise multimodal content pipeline — off-domain, high effort. |
| `mlops-2026-06-11-despegar-sofia-orchestration-layer` | Keep an explicit orchestration layer (Chappie) above domain agents to prevent tool-routing failures as agent count grows | high | Enterprise multi-agent orchestration scaling — single-agent preference; off-scale. |
| `mlops-2026-06-11-despegar-federated-agent-development` | Let domain teams own and iterate their own agent flows on top of a central scaffold | medium | Domain-team org structure — irrelevant to a solo loop. |
| `do-2026-06-11-fable-cursor-agent-view-workflow` | Run Claude Fable (Mythos 5) exclusively through Cursor agent view to avoid safeguard false-positives and leverage auto-fallback | low | Cursor-specific tooling swap — not the owned harness. |
| `do-2026-06-11-minimax-m3-hermes-agent-cost-reduction` | Power Hermes Agent with Minimax M3 to enable 24/7 always-on agentic loops at 10-20x lower cost than Opus | low | Cheaper non-Claude model for cost — consistent local/cheap-model NO. |
| `do-2026-06-11-cmax-terminal-parallel-agents` | Use CMAX terminal for managing parallel CLI agents with per-pane zoom, workspaces, and jump-to-unread notifications | low | Specific terminal product for ergonomics — low value vendor tooling. |
| `nh-2026-06-11-fable5-model-tier-awareness` | Audit workflows for Fable 5 upgrade window before June 22 paywall | low | Time-boxed 'before June 22 paywall' — window has passed; stale. |
| `nh-2026-06-11-aios-four-cs-framework` | Structure an AI operating system around the Four Cs: Context, Connections, Capabilities, Cadence | high | Duplicate of the adopted four-Cs second-brain card; this is the high-effort over-scoped 'AI OS' variant. |
| `st-2026-06-11-ai-foundations-business-mental-model` | Frame agent delegation as intern-coaching to improve prompt quality | low | Vague business mindset framing, no concrete deliverable. |
| `st-2026-06-11-reusable-skills-business-automation` | Build reusable Claude skill files for recurring business workflows | medium | Business workflows (email/CRM/proposals) — off the YOLO domain. |
| `st-2026-06-11-four-step-skill-building-framework` | Use a four-step calendar-audit-to-skill pipeline to systematically delegate recurring tasks | low | Calendar/personal-productivity delegation — off-domain. |
| `mk-2026-06-11-dynamic-workflows-due-diligence` | Use the 'build a workflow' keyword trigger to auto-generate multi-agent harnesses for large document analysis | medium | Large-document due-diligence use case — off-domain; the workflow-pattern insight is already captured by the six-patterns card. |
| `aie-2026-06-11-small-model-tool-use-rl-training` | Fine-tune a small model on tool-use discipline with RL to match large-model performance on structured tasks | high | RL fine-tuning of a small model — GPU-heavy, off-focus, wrong hardware. |
| `aie-2026-06-11-gemma4-open-model-local-agentic` | Replace a cloud-API agent step with a locally-hosted Gemma 4 31B model for data-sensitive sub-tasks | medium | Local Gemma 4 for sub-tasks — consistent local-model NO (cf. prior Gemma/Ollama discards). |
| `aie-2026-06-11-posthog-signal-to-pr-pipeline` | Build a signal-ingestion-to-PR pipeline that converts product observability events into auto-generated code fixes | high | Product-telemetry -> auto-PR pipeline — needs product signals the loop doesn't have; high effort. |
| `aie-2026-06-11-runpod-flash-sdk-local-gpu-iteration` | Use RunPod Flash SDK decorator to deploy GPU inference functions from local dev environment without Docker build cycles | medium | GPU inference dev tooling — off-focus. |
| `aie-2026-06-11-gemini-audio-rich-transcription` | Use Gemini Flash audio API to extract structured metadata (speakers, timestamps, language, emotion) from meeting recordings in a single API call | low | Alternate audio transcription — current Phase 4 transcript pipeline already works. |
| `aie-2026-06-11-long-context-ulysses-upipe` | Stack DeepSpeed Ulysses + gradient checkpointing + U-Pipe chunked-head recompute for long-context fine-tuning | high | 8xH100 long-context fine-tuning — far off-focus. |
| `aie-2026-06-11-eval-as-compute-primitive` | Use Cloudflare Durable Objects as stateful, addressable compute units for long-running AI agents | medium | Cloudflare Durable Objects for stateful agents — file-based session_state suffices; off-stack infra. |
| `aie-2026-06-11-runpod-serverless-llm-endpoint` | Deploy a HuggingFace open-source LLM as a RunPod serverless endpoint from a preconfigured Hub listing in under 5 minutes | low | Deploy an open LLM endpoint — infra off-focus. |
| `aie-2026-06-11-self-healing-scraper-pipeline-mcp` | Use Bright Data MCP + LLM agent to auto-generate, execute, and self-heal web scrapers instead of calling LLM per page | medium | Web-scraper pipeline — not needed; Phase 4 uses RSS + transcript APIs. |
| `aie-2026-06-11-mcp-apps-rich-ui-in-chat` | Return sandboxed interactive HTML iframes from MCP tool calls to replace text-only agent responses with rich UI | medium | MCP-host iframe rendering — niche VS Code feature, not core to the build loop. |
| `aie-2026-06-11-studio-nl-business-queries` | Build an internal NL-to-SQL agent with persistent widget output for business queries | high | Enterprise NL-to-SQL business tool — off-domain, high effort. |
| `aie-2026-06-11-webmcp-structured-site-tools` | Expose site capabilities as Web MCP tools to replace brittle DOM-scraping agent flows | medium | Web-automation MCP infra — off-focus. |
| `do-2026-06-12-pi-agent-minimal-harness` | Swap Opinionated Agent Framework for Pi Agent's Minimal Harness | low | Swap to a third-party minimal harness — against harness-ownership; build-our-own minimal loop was the adopted version. |
| `do-2026-06-12-pi-agent-skills-reuse` | Build Pi Agent Skills as Reusable Prompt Modules for Repeated Workflows | medium | Pi Agent-specific skills — vendor tie; skills already native. |
| `nh-2026-06-12-claude-fable-one-prompt-video` | Drive a Multi-Tool Media Pipeline From a Single /goal Prompt Using Claude Code | high | Media-generation pipeline — off-domain, high effort. |
| `nh-2026-06-12-head-of-ai-non-technical-path` | Validate a Non-Technical AI Adoption Lead Role With Hands-On Claude Code Builds | low | Career/role validation — not a technical experiment. |
| `do-2026-06-15-hermes-apify-mcp-scraping` | Connect Hermes Agent to Apify MCP for unrestricted web scraping | medium | Gray-area social scraping via Hermes/Apify — off-focus. |
| `do-2026-06-15-fable-ban-local-model-fallback` | Build a model-fallback routing layer to hedge against frontier model access bans | medium | Open-source/local fallback hedging — overlaps the adopted resilience card and leans into the local-model NO. |
| `mlops-2026-06-15-multiplayer-ai-flocking` | Design multi-agent workflows using flocking algorithm principles (local separation, distant attraction, alignment) | medium | Flocking-metaphor multi-agent coordination — abstract, no concrete deliverable; single-agent preference. |
| `aie-2026-06-15-double-iframe-csp-mcp-apps` | Integrate a CSP inspector into MCP app development workflow to catch missing domain declarations before store submission | low | CSP inspector for MCP app-store submission — workflow the loop doesn't run. |
| `aie-2026-06-16-diffusion-speedup-stack` | Stack Quantization + Caching + Distillation to Approach Real-Time Diffusion | high | GPU diffusion-model optimization — off-focus. |
| `aie-2026-06-17-mcp-real-web-access` | Replace default LLM web fetch with a proxy-backed MCP scraping tool and compare hallucination rate | medium | Proxy-backed scraping vs hallucination — web-infra off-focus. |
| `mlops-2026-06-19-voice-agent-cascaded-hybrid-architecture` | Use a foreground/background dual-model pattern for voice agents to balance latency and quality | high | Voice-agent architecture — off-domain. |
| `nh-2026-06-19-glm52-claude-code-model-routing` | Route Claude Code to open-source models via base URL override and per-directory settings.local.json | low | Route Claude Code to GLM 5.2 for cheapness — consistent local/open-model NO. |
| `nb-2026-06-20-creator-trust-stack-disclosure` | Implement a Creator Trust Stack metadata layer for AI-assisted outputs | medium | AI-media provenance disclosure — the loop ships code, not published media; off-domain. |
| `nb-2026-06-20-voice-clone-consent-policy` | Draft and enforce a pre-incident AI likeness and voice policy for team outputs | low | Voice/likeness cloning policy — off-domain. |
| `do-2026-06-21-obsidian-living-files-agent-context` | Store Agent Context as Obsidian Markdown Vault for Living File Access | medium | Obsidian+VPS vault — redundant with the in-repo markdown context (learnings/_hot/skills) already used. |
| `mlops-2026-06-22-genetic-pareto-agent-trajectories` | Apply genetic Pareto sampling across parallel agent trajectories | high | 100 parallel runs + genetic selection — over-scale compute for a solo loop. |
| `nh-2026-06-22-internal-ai-consultant-roadmap` | Run a 4-step internal AI consultant playbook tied to measurable KPIs | medium | Org AI-consultant/career playbook — off-domain. |

## Notes

- `phase4_run.json.backlog_count` set to 0 to match.
- Adoption here ≠ shipped. Promotion to builds still goes through the normal
  triage → `tick_queue_approved` → scaffold → council flow.
- Downstream: `llm-wiki-hub`'s nightly sync reads this `experiments.json` and
  will reflect the new statuses on its next run (its own automation).

## Promotion to build queue (2026-06-24)

All **65 adopted** experiments were promoted into `tick_queue_approved`
in `.harness/session_state.json` — the repo's canonical "approved to build"
queue that the Tick-Tock cron dispatches from. This is how yolo turns an
adopted experiment into an actual build.

Each queue entry carries: `id`, `title`, `idea` (hypothesis + steps),
`type`, `rationale`, `effort`, `council_focus`, `source_experiment_id`,
`status: approved`. Ordered **buildable-first, then low-effort-first**.

| Type | Count | Meaning |
|---|---|---|
| `yolo` | 4 | Standalone single-file builds (3 generative-art pieces + token-burn dashboard) |
| `infra` | 61 | Harness/process ticks — eval suites, observability, retrieval, guardrails, skills, context/memory, routing, audits |

Effort mix: 23 low · 36 medium · 6 high.

### How these become builds (and why this PR does not hand-build them)

The yolo build pipeline (`skills/10-tick.md`, `program.md`) builds **one
project per tick** under hard gates — C1 ≤50 files, C2 ≤2000 lines added
per build, and a **mandatory Gemini council review** (`gemini-analyze-code`)
before any push (bedrock rule + gate C10). Building 65 items in one PR would
violate the per-build gates, and the Gemini review MCP only runs in the cron
environment, not this session.

So the correct incorporation is **promotion, not hand-coding**: the cron now
draws from `tick_queue_approved` and builds each item one tick at a time with
the full test → council → gate pipeline. On merge, the autonomous builder
will work through all 65 over subsequent ticks. Pause/throttle via the
`tick_tock.yml` Actions schedule if a slower cadence is wanted (and note the
Gemini API cost of 65 gated builds).

Gates at promotion time: `council_escalations` empty (C8 ✓), no `.harness_halt`
(C9 ✓). One unrelated deferred escalation remains (`adopt-bare-agent` PLAN).

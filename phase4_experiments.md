# Phase 4: YouTube Experiment Catalog

Complete catalog of all experiments extracted from the Phase 4 YouTube intelligence pipeline.
Generated 2026-04-13. Covers 75 experiments from 60 videos across 8 channels.

## Overview

| Metric | Value |
|---|---|
| Total experiments | 75 |
| Videos processed | 60 |
| Channels monitored | 8 |
| Date range (published) | 2026-03-17 to 2026-04-12 |
| Date range (ingested) | 2026-03-29 to 2026-04-12 |
| Adopted | 43 (57%) |
| Discarded | 20 (26%) |
| Deferred | 7 (9%) |
| Backlog | 3 |
| Skipped (no experiment) | 2 |

## Channel Signal Quality

| Rank | Channel | Experiments | Adopted | Adopt Rate | Discarded | Deferred | Backlog | Signal |
|---|---|---|---|---|---|---|---|---|
| 1 | Fireship | 2 | 2 | 100% | 0 | 0 | 0 | Excellent |
| 2 | [un]prompted | 1 | 1 | 100% | 0 | 0 | 0 | Excellent |
| 3 | NateBJones | 26 | 17 | 70% | 4 | 3 | 0 | Strong |
| 4 | DavidOndrej | 7 | 4 | 57% | 3 | 0 | 0 | Mixed |
| 5 | MLOps | 20 | 11 | 55% | 6 | 3 | 0 | Mixed |
| 6 | NateHerk | 15 | 7 | 46% | 6 | 1 | 1 | Mixed |
| 7 | ShawTalebi | 3 | 1 | 33% | 0 | 0 | 2 | Weak |
| 8 | TwoMinutePapers | 1 | 0 | 0% | 1 | 0 | 0 | Weak |

---

## Experiments by Channel

### NateBJones

**Nvidia Just Open-Sourced What OpenAI Wants You to Pay Consultants For** (2026-03-24)

- **Apply strict linting to all agent-generated code** [medium] — `adopt`
  - If we add automated static analysis (ESLint, HTMLHint) to the test pipeline, then bug rates drop because agents are 'lazy developers' who take shortcuts unless forced to comply with standards.
- **Build an Agent Readiness checklist for the YOLO codebase** [high] — `discard`
  - If we evaluate the YOLO codebase against an 'Agent Readiness Framework' (code quality, documentation, test coverage, clear file structure), then agent productivity improves because failures are usuall
- **Use incremental summarization for context compression in long sessions** [low] — `adopt`
  - If we implement incremental summarization (summarize segments, merge into structured persistent summary) for long YOLO build sessions, then context window usage drops and agent coherence improves beca

**Tobi Lutke Made a 20-Year-Old Codebase 53% Faster Overnight** (2026-03-25)

- **Adopt the Dark Factory pattern for autonomous builds** [medium] — `adopt`
  - If we restructure the YOLO build loop as a Dark Factory (spec in → autonomous processing → eval out with retry loops), then build quality increases because the agent iterates against automated tests u
- **Apply Auto Research pattern to optimize Gemini review scores** [medium] — `discard`
  - If we treat Gemini code review scores as a metric and use hill-climbing (iterating on code until the score improves), then average code quality increases because we're optimizing against a measurable 

**A Markdown File Just Replaced Your Most Expensive Design Meeting (Google Stitch)** (2026-03-28)

- **Create a design.md as an agent-readable design system** [medium] — `adopt`
  - If we capture our UI design conventions in a structured markdown file (design.md), then AI agents will produce more visually consistent projects because they can reference explicit design tokens, colo
- **Use MCP to connect build agents to professional tools** [medium] — `adopt`
  - If we connect the builder agent to external tools via MCP (e.g., image generation, 3D rendering, browser testing), then project ambition increases because the agent can leverage capabilities beyond ju

**Anthropic Just Gave You 3 Tools That Work While You're Gone** (2026-03-29)

- **Use Claude Scheduled Tasks for automated recurring work** [low] — `discard`
  - If we set up Claude Scheduled Tasks for recurring monitoring (e.g., daily test runs, dependency checks, competitor analysis), then we reduce manual overhead and catch issues earlier because the agent 
- **Adopt the 'close the loops' delegation framework** [low] — `adopt`
  - If we identify open commitments (pending tasks causing mental load) and delegate them to background agents, then we free up cognitive bandwidth for high-level decisions because agents handle the execu

**Anthropic, OpenAI, and Microsoft Just Agreed on One File Format. It Changes Everything.** (2026-03-31)

- **Restructure program.md as agent-readable skill files** [medium] — `adopt`
  - If we decompose program.md into discrete, focused skill files (build-skill.md, review-skill.md, test-skill.md) with specific descriptions and methodology sections, then the builder agent produces high
- **Design skill outputs as composable handoffs** [medium] — `adopt`
  - If we design each YOLO loop phase to produce output formatted as input for the next phase (brainstorm outputs a spec, spec feeds the builder, builder outputs code, code feeds the reviewer), then the p

**Anthropic Just Built a Model That Breaks Everything (Claude Mythos Is Nigh)** (2026-04-01)

- **Run a 4-layer stack audit before every major Claude model upgrade** [low] — `adopt`
  - If we audit each layer of the YOLO build loop (system prompts, retrieval, verification, orchestration) before upgrading to a new Claude model, then we remove brittle workarounds before they break beca

**Your Claude Limit Burns In 90 Minutes Because Of One ChatGPT Habit.** (2026-04-02)

- **Use task-isolated fresh Claude sessions to prevent context bloat** [low] — `discard`
  - If we start a fresh Claude session for each discrete YOLO task (build, review, logging) instead of continuing a single long session, then we stay within token limits and reduce costs because each sess
  - *Reason: Parked, architecture already provides this.*

**I Broke Down Anthropic's $2.5 Billion Leak. Your Agent Is Missing 12 Critical Pieces.** (2026-04-02)

- **Audit PAI agent stack against the 12 critical agent architecture pieces** [medium] — `adopt`
  - If we audit our agent infrastructure against Anthropic's leaked 12-piece agent architecture checklist, then we identify structural gaps (missing guardrails, evaluation layers, memory systems, etc.) be
- **Add explicit guardrail and fallback layers to autonomous build agents** [medium] — `adopted`
  - If we add explicit guardrail layers (cost caps, output validation, rollback triggers) to YOLO build agents, then autonomous builds become safer for higher-stakes projects because failures are caught a

**Wall Street Just Bet $285 Billion on AI Agents. The Best One Barely Works.** (2026-04-04)

- **Implement compounding agent memory that improves with each build** [medium] — `adopt`
  - If the build agent accumulates structured context about past builds (what patterns worked, which codebases have which quirks, user preferences) in a queryable store rather than a flat text file, then 
- **Create pre-wired agent recipes instead of blank-canvas prompting** [low] — `adopt`
  - If we create named recipe presets for common tasks ("new devtool", "flagship feature", "bug fix", "code review", "refactor") with pre-loaded context and tool configurations, then agent success rate in

**Your Agent Produces at 100x. Your Org Reviews at 3x.** (2026-04-05)

- **Deploy evaluative agents alongside generative agents to eliminate review bottleneck** [low] — `adopt`
  - If we build Agent B to review/filter Agent A output before human review (pre-filtered council), then the human only sees pre-audited work and the 100x/3x bottleneck disappears.
- **Build independent observability that never trusts agent self-reporting** [medium] — `adopt`
  - If we add an independent verification layer that checks actual outcomes (file exists, tests pass, git committed) instead of trusting the agent's claim that it did the work, then we catch silent failur

**A Polymarket Bot Made $438,000 In 30 Days. Your Industry Is Next. Here's What To Do About It.** (2026-04-07)

- **Map Your Dev Loop Steps Against Automation Displacement Risk** [low] — `deferred`
  - If we systematically audit each step in the YOLO loop for autonomous-agent replaceability, then we can prioritize which components to harden or own before commodity AI bots commoditize them, because t
  - *Reason: Deferred 2026-04-08: interesting but not currently actionable.*

**You're Building AI Agents on Layers That Won't Exist in 18 Months. (What this Means for You)** (2026-04-07)

- **Classify Each YOLO Loop Dependency by Shelf-Life and Replaceability** [medium] — `adopted`
  - If we tag every external library, orchestration framework, and model API in our stack with an estimated deprecation horizon, then we can isolate business logic from ephemeral scaffolding and reduce fu

**I Analyzed 512,000 Lines of Leaked Code. It Shows What's Coming for Your AI Tools.** (2026-04-08)

- **Mine AI Tool Source Code for Architectural Patterns to Adopt Early** [medium] — `deferred`
  - If we systematically analyze leaked or open-sourced AI tool codebases for recurring architectural patterns, then we can anticipate and implement emerging best practices before they become mainstream, 
  - *Reason: Deferred 2026-04-09: leaked source code is ethically/legally problematic as a corpus — do not adopt as-is.*

**There Are Only 5 Safe Places to Build in AI Right Now. Are You in One?** (2026-04-10)

- **Audit current build position against the 5 safe AI niches framework** [low] — `adopted`
  - If we map our AI development focus to one of the 5 identified defensible niches, then we can reduce strategic risk and prioritize features that align with durable value creation because undifferentiat

**Google's New Quantization is a Game Changer** (2026-04-11)

- **Benchmark Google's new quantization scheme against existing INT4/INT8 baselines on local model inference** [medium] — `deferred`
  - If we apply Google's new quantization method to a mid-size model in our dev loop, then we will see improved inference speed or reduced memory footprint with minimal quality degradation because Google'
  - *Reason: Deferred 2026-04-12: local-model adjacent.*

**The $3 Trillion IPO Trap Nobody's Talking About** (2026-04-12)

- *Skipped — no actionable experiment*

**I Watched 3 Companies Lay Off Their Managers. All 3 Hit the Same Wall.** (2026-04-12)

- *Skipped — no actionable experiment*

### MLOps

**Durable Execution and Modern Distributed Systems** (2026-03-17)

- **Evaluate durable execution for long-running agent workflows** [high] — `adopt`
  - If we structure long-running YOLO workflows (multi-project refinement, Phase 3 cull) as durable workflows with automatic state persistence, then we eliminate lost progress from crashes/disconnects bec

**Everything We Got Wrong About Research-Plan-Implement - Dexter Horthy** (2026-03-25)

- **Adopt vertical planning with structure outlines before coding** [low] — `adopt`
  - If we add a structure outline phase (define signatures, types, interfaces before implementation) and plan vertically (small testable slices from data to UI), then we reduce rework because mistakes are

**Lessons from 25 Trillion Tokens — Scaling AI-Assisted Development at Kilo** (2026-03-27)

- **Use specialized agent roles instead of one monolithic agent** [medium] — `discard`
  - If we split the YOLO builder into specialized agent roles (Architect for research/design, Code Agent for implementation, Debug Agent for troubleshooting), then build quality improves because each agen
  - *Reason: The 3-phase pipeline within a single agent captures most of the value.*
- **Apply the trust ladder to increase agent autonomy incrementally** [low] — `discard`
  - If we gradually increase agent autonomy (autocomplete → chat → single agent → orchestration) based on measured trust metrics (bug rate, rework rate), then we avoid the pitfall of over-trusting agents 
  - *Reason: Parked, not discarded permanently.*

**2026 The Year of Agent Orchestration** (2026-03-31)

- **Run parallel agent sessions for independent YOLO tasks** [low] — `adopt`
  - If we run multiple agent sessions in parallel (e.g., 3 Tick builds simultaneously using subagents), then throughput increases because independent builds do not need sequential execution — each gets it

**Stop Shipping on Vibes — How to Build Real Evals for Coding Agents** (2026-03-31)

- **Build a golden dataset of past bugs as an eval suite** [medium] — `adopt`
  - If we extract 20-30 past Gemini-caught bugs from learnings.md as test cases (input: buggy code, expected: the fix), then we can measure whether future agent builds avoid those same bug patterns — turn

**Decomposing the Agent Orchestration System: Lessons Learned** (2026-03-31)

- **Add structured debug logging at agent decision points to speed up failure diagnosis** [low] — `adopt`
  - If we emit structured log events at each major agent decision (tool call initiated, response evaluated, branch taken, test outcome), then diagnosing build failures takes minutes instead of hours becau

**Choosing the Right Model is Hard. Maintaining Accuracy is Harder.** (2026-04-01)

- **Build a golden-prompt eval suite to detect model regression after upgrades** [medium] — `adopt`
  - If we maintain a set of 5-10 representative YOLO build prompts as a regression suite and run it after any model upgrade, then we catch model behavioral changes before they affect production builds bec

**MCP Dev Summit [Day 1] ft. Anthropic, Hugging Face, Open AI & Microsoft** (2026-04-02)

- **Track the Anthropic MCP technical roadmap and adopt spec updates proactively** [low] — `adopt`
  - If we monitor Anthropic's MCP spec roadmap (as presented by David Soria Parra) and update our tool integrations to align with emerging MCP standards, then our agent tool usage remains forward-compatib

**MCP Dev Summit [Day 2] ft AWS, Docker, & Datadog** (2026-04-02)

- **Evaluate Docker and Datadog MCP servers for agent-driven DevOps** [high] — `deferred`
  - If we integrate Docker MCP (container management) and Datadog MCP (observability) into the agent toolkit, then build agents can deploy, monitor, and debug containerized projects autonomously because t
  - *Reason: Deferred 2026-04-07: high effort, requires Docker + Datadog credentials, current YOLO does not deploy containers.*

**The Coding Agent Multiverse of Madness** (2026-04-02)

- **Benchmark multiple coding agents on the same YOLO build spec** [high] — `deferred`
  - If we run the same build specification through multiple coding agents (Claude Code, Codex, Gemini CLI, Cursor, etc.) and compare outputs, then we identify which agent is best suited for which project 
  - *Reason: Deferred 2026-04-07: cross-agent benchmark is high cost (API keys for Codex, Gemini, Cursor, multi-day runs).*

**Practical Security for AI-generated Code** (2026-04-02)

- **Add security scanning to the YOLO build pipeline for AI-generated code** [medium] — `adopt`
  - If we add automated security scanning (SAST, dependency audit, secrets detection) to the YOLO build pipeline, then we catch vulnerabilities introduced by AI-generated code before they ship because AI 

**Beyond SWE-Bench Pro - Where do Agents go from Here?** (2026-04-02)

- **Build custom evals that measure real YOLO build quality beyond synthetic benchmarks** [medium] — `adopted`
  - If we design custom evaluation metrics tailored to YOLO project requirements (user experience quality, feature completeness, maintainability) rather than relying on generic benchmarks, then we get a m

**How to Fix Your Agent's Amnesia: Lessons from Building a Self-learning Agent** (2026-04-02)

- **Implement structured memory retrieval so the build agent learns from past builds** [medium] — `adopted`
  - If we give the build agent structured access to past build outcomes (what worked, what failed, which patterns caused bugs), then build quality compounds over time because the agent doesn't repeat mist
- **Add automatic post-build reflection that writes back to agent memory** [low] — `adopt`
  - If the build agent automatically reflects after each build (what went well, what went wrong, what to do differently) and writes structured entries to its memory, then the memory grows organically with

**AI Agents Summit Seattle** (2026-04-07)

- **Implement a Lightweight Agent Eval Harness Drawn from Summit Patterns** [high] — `discarded`
  - If we implement an eval harness that tests agent task-completion, tool-call correctness, and loop termination conditions on a small benchmark suite, then we can catch regressions in the YOLO loop's ag
  - *Reason: Discarded 2026-04-08 as duplicate of mlops-2026-04-03-beyond-swebench-evals (already adopted as infra-yolo-evals tick).*

**Ship Agents  A Virtual Conference Track 2** (2026-04-10)

- **Extract and benchmark agent deployment patterns from Ship Agents conference talks** [medium] — `deferred`
  - If we implement the agent shipping patterns demonstrated by practitioners in this conference track, then we will reduce time-to-production for new agents because the talks aggregate hard-won lessons a
  - *Reason: Deferred 2026-04-12: potentially useful agent deployment patterns but too broad without someone watching the actual talks.*

**Fixing GPU Starvation in Large-Scale Distributed Training** (2026-04-10)

- **Implement GPU starvation detection and mitigation in distributed training pipeline** [high] — `discarded`
  - If we add monitoring and scheduling fixes for GPU starvation conditions in our distributed training runs, then we will reduce idle GPU time and improve training throughput because starvation is a comm
  - *Reason: Discarded 2026-04-12: YOLO loop does not do distributed GPU training.*

**Production Sub-agents for LLM Post Training** (2026-04-10)

- **Wire sub-agents into the LLM post-training pipeline for automated data curation and eval** [high] — `discarded`
  - If we deploy specialized sub-agents to handle discrete steps in the post-training pipeline such as data filtering, reward labeling, or evaluation, then we will reduce manual intervention and accelerat
  - *Reason: Discarded 2026-04-12: YOLO loop does not do LLM fine-tuning or post-training.*
- **Use a judge sub-agent to automate reward signal generation during RLHF or DPO runs** [medium] — `discarded`
  - If we replace or augment human preference labeling with a calibrated LLM judge sub-agent during post-training, then we can scale preference data collection by 10x at lower cost because LLM judges have
  - *Reason: Discarded 2026-04-12: RLHF/DPO reward signal generation is out of scope.*

### NateHerk

**5 ‘Boring’ AI Workflows that Businesses Actually Want (And Pay For)** (2026-03-29)

- **Filter YOLO Tick ideas through the 'boring-but-high-ROI' automation criteria** [low] — `adopt`
  - If we bias YOLO Tick session ideas toward the 'boring automation' patterns (repeatable, unglamorous, businesses actually pay for), then the portfolio generates more commercial value because automation

**Codex Just 10x’d Claude Code Projects** (2026-03-30)

- **Adopt Codex-as-planner + Claude Code-as-executor 3-phase build cycle** [low] — `adopt`
  - If we use Codex to generate a structured plan (iterating clarifying questions until 95% confidence) before handing to Claude Code for execution, then we reduce mid-build architectural rework because a

**Claude Code + Paperclip Just Destroyed OpenClaw** (2026-03-31)

- **Use Paperclip's company-layer to orchestrate multi-agent Claude Code builds** [medium] — `discard`
  - If we use Paperclip (open-source company-layer OS) to coordinate multiple Claude Code agents with org charts, budgets, heartbeats, and job checkout, then complex multi-file YOLO projects and Phase 2 r
  - *Reason: Parked pending specialist experiment outcome.*

**All of Claude Code Just Leaked — How to Become a Top 1% User** (2026-04-01)

- **Optimize CLAUDE.md as short opinionated onboarding doc + configure wildcard permissions** [low] — `discard`
  - If we restructure CLAUDE.md to be a short, opinionated onboarding document (high-level rules, not detailed docs) and configure wildcard permissions for common operations, then agent autonomy increases
  - *Reason: Parked, not permanently discarded.*

**18 Claude Code Token Hacks in 18 Minutes** (2026-04-02)

- **Apply /compact at defined YOLO session milestones to preserve context within token limits** [low] — `adopt`
  - If we run /compact at defined YOLO session checkpoints (after reading learnings.md, after build completes, before logging), then we reduce mid-session token exhaustion while retaining all decision con

**Ollama + Claude Code = 99% CHEAPER** (2026-04-02)

- **Use Ollama local models for Claude Code's routine sub-tasks to cut costs** [medium] — `discarded`
  - If we route Claude Code's routine sub-tasks (file reading, simple edits, boilerplate generation) through a local Ollama model while keeping complex reasoning on Claude, then we reduce API costs by up 
  - *Reason: Discarded 2026-04-07: same local-model policy decision as #42.*
- **Route Low-Stakes Claude Code Subtasks to Local Ollama Models to Cut Loop Cost** [medium] — `discarded`
  - If we configure Claude Code to route boilerplate-heavy or low-complexity subtasks (file scaffolding, docstring generation, simple refactors) to a local Ollama model while reserving Claude API calls fo
  - *Reason: Discarded 2026-04-08 as REPEAT of nh-2026-04-03-ollama-claude-code-cost (discarded 2026-04-07).*

**Andrej Karpathy Just 10x'd Everyone's Claude Code** (2026-04-05)

- **Implement Karpathy hot-cache pattern for instant agent context recovery** [low] — `adopt`
  - If we maintain a _hot.md file (~500 tokens) that the agent reads at session start containing active threads, key metrics, and recent decisions, then context recovery drops from reading 3000+ lines to 

**Planning In Claude Code Just Got a Huge Upgrade** (2026-04-07)

- **Use Claude Code's New Planning Mode as a Spec-Decomposition Pre-Pass** [low] — `adopted`
  - If we invoke Claude Code's upgraded planning mode before any implementation task in the YOLO loop, then the resulting step-by-step plan will surface ambiguities and scope issues earlier, reducing mid-

**Claude's New AI Just Changed the Internet Forever** (2026-04-08)

- **Integrate Claude's New Web-Native Capabilities as a Live-Data Tool in the YOLO Loop** [medium] — `discarded`
  - If we add Claude's new internet-connected or web-native capabilities as a tool call within the YOLO loop, then agents will produce more accurate and up-to-date outputs on tasks requiring current infor
  - *Reason: Discarded 2026-04-09: redundant with existing capabilities.*

**I Gave OpenClaw $10,000 to Trade Stocks** (2026-04-09)

- **Deploy a Live-Capital Agentic Trading Loop and Instrument Its Decision Trail** [high] — `discarded`
  - If we connect an AI agent to a real brokerage account with a defined risk budget, then we can observe how agentic reasoning degrades or holds under real financial pressure, because live stakes surface
  - *Reason: Discarded 2026-04-12: live-capital agentic trading is completely out of scope for the YOLO dev loop.*

**I Tested Claude's New Managed Agents... What You Need To Know** (2026-04-09)

- **Benchmark Claude Managed Agents Against Manual Orchestration on a Multi-Step Dev Task** [medium] — `adopted`
  - If we replace our hand-rolled agent orchestration with Claude's native managed agents API, then task completion reliability will improve and boilerplate coordination code will decrease, because Anthro

**Claude Just Told Us to Stop Using Their Best Model** (2026-04-10)

- **Benchmark Claude Haiku or Sonnet against Opus on YOLO Loop tasks and measure cost-quality tradeoff** [low] — `adopted`
  - If we route routine YOLO Loop tasks to a smaller Claude model instead of defaulting to the flagship model, then we will achieve comparable output quality at significantly lower cost and latency becaus

**Seedance 2.0 + Claude Code Creates $10k Websites in Minutes** (2026-04-11)

- **Pipe Seedance 2.0 video output into Claude Code to auto-generate animated website assets** [medium] — `deferred`
  - If we use Seedance 2.0 to generate short video or motion assets and feed them directly into a Claude Code agentic workflow, then we can produce production-quality animated web components in minutes be
  - *Reason: Deferred 2026-04-12: creative but tangential.*

**This One Plugin Just 10x'd Claude Code** (2026-04-12)

- **Integrate the Featured Plugin into Claude Code Workflow** [low] — `backlog`
  - If we install and configure the highlighted plugin for Claude Code, then our agentic coding loop will complete tasks faster and with fewer manual corrections because the plugin extends Claude Code's t

### DavidOndrej

**RIP OpenClaw… this 100% private AI Agent is insane** (2026-03-27)

- **Run YOLO builds via a 100% local AI agent stack** [high] — `discard`
  - If we run YOLO builds using a self-hosted AI agent (OpenClaw or n8n + local LLM) instead of interactive cloud sessions, then we gain persistent autonomous execution (no session timeouts, no API key ex
  - *Reason: Park until 48GB+ VRAM hardware.*

**This 100% self-improving AI Agent is insane… just watch** (2026-03-29)

- **Wire a self-critique step into the YOLO build loop before running external tests** [medium] — `adopt`
  - If we add a self-evaluation step where the builder agent critiques its own code against the acceptance criteria before running test_project.py, then the test pass rate on first attempt improves becaus

**The only AutoResearch tutorial you will ever need** (2026-03-31)

- **Implement autoresearch loop for YOLO project optimization** [medium] — `adopt`
  - If we structure the YOLO build loop as a Karpathy-style autoresearch loop (single file to edit, single metric to optimize, automated eval, git commit on success / reset on failure), then project quali

**Gemma 4 is insane… best open-source model ever?!** (2026-04-02)

- **Evaluate Gemma 4 as a local code review model to reduce API costs** [medium] — `discarded`
  - If Gemma 4 is capable enough for code review tasks, then we can run it locally via Ollama for routine reviews (linting-level checks, pattern enforcement) and reserve Gemini API calls for deep architec
  - *Reason: Discarded 2026-04-07: local-model policy decision = NO.*

**This 100% minimal AI Agent can do anything… just watch** (2026-04-07)

- **Build a Bare-Metal Minimal Agent Loop with No Framework Dependencies** [low] — `adopted`
  - If we implement the smallest possible agent loop (LLM call → tool dispatch → result injection → repeat) using only raw API calls and a dictionary-based tool registry, then we will have a maximally und

**Claude Mythos might actually be AGI… wtf** (2026-04-08)

- **Benchmark Claude Mythos on Open-Ended Agentic Tasks in the YOLO Loop** [low] — `adopted`
  - If we run Claude Mythos on our existing suite of multi-step agentic tasks inside the YOLO loop, then we will observe measurably fewer clarification requests and higher task completion rates compared t

**CODEX FULL COURSE: From Zero to Deployed App (2026)** (2026-04-12)

- **Build and Deploy a Full App Using OpenAI Codex End-to-End** [medium] — `discarded`
  - If we follow a structured Codex-driven workflow from blank repo to deployed app, then we can establish a repeatable agentic scaffolding pattern for the YOLO loop because Codex can handle code generati
  - *Reason: Discarded 2026-04-12: OpenAI Codex end-to-end deployment is a competitor tool demo, not an adoptable pattern.*

### ShawTalebi

**How to Automate Anything with Claude (4-Step Framework)** (2026-04-05)

- **Build a skill-creator meta-agent that writes SKILL.md files from successful interactions** [medium] — `adopt`
  - If we have an agent whose only job is to observe successful build sessions and extract reusable skill documents (trigger, steps, output format, edge cases), then our methodology self-documents and new

**How I Taught Claude To Edit My YouTube Videos** (2026-04-12)

- **Build a Claude-Driven Video Edit Instruction Pipeline** [medium] — `backlog`
  - If we provide Claude with a transcript plus a structured editing style guide, then Claude can output a precise cut list or edit instructions because it can reason over temporal text data and apply con
- **Encode a YOLO Loop Style Guide as a Reusable Claude System Prompt** [low] — `backlog`
  - If we distill our dev loop's coding conventions and output format rules into a compact system prompt style guide fed to Claude on every task, then output consistency will improve and post-generation e

### Fireship

**He just crawled through hell to fix the browser...** (2026-04-02)

- **Use Pretext library for instant text measurement without DOM reflows** [medium] — `adopt`
  - If we integrate Pretext (pure TypeScript text measurement library by Cheng Lou) into text-heavy YOLO projects, then virtualized lists and dynamic layouts become trivially fast because text dimensions 
- **Evaluate Junie CLI multi-model routing for harness-cli council** [low] — `adopt`
  - If we route different council angles to different models (e.g. Claude for architecture, Gemini for security, GPT-4 for product) like Junie auto-switches models per task, then council quality improves 

### [un]prompted

**Anatomy of an Agentic Personal AI Infrastructure** (2026-03-31)

- **Build a Council skill for multi-perspective task review** [low] — `adopt`
  - If we spin up multiple specialized agents to debate a task from different perspectives (security, performance, UX, architecture) before committing code, then build quality improves because blind spots

### TwoMinutePapers

**Google's New AI Just Broke My Brain (TurboQuant)** (2026-04-01)

- **Prototype a YOLO project using local quantized LLM inference via Ollama** [medium] — `discard`
  - If we build one YOLO project that runs LLM inference locally using a quantized model (4-bit via Ollama), then we validate whether quantized local inference is production-viable for YOLO builds, becaus
  - *Reason: Parked.*

---

## Adopted Experiments — Detail

Every experiment with verdict `adopt` or `adopted`, with full context.

### Adopt the 'close the loops' delegation framework

- **ID:** `nb-2026-03-29-close-the-loops`
- **Channel:** NateBJones
- **Video:** Anthropic Just Gave You 3 Tools That Work While You're Gone
- **Published:** 2026-03-29 | **Ingested:** 2026-03-29
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we identify open commitments (pending tasks causing mental load) and delegate them to background agents, then we free up cognitive bandwidth for high-level decisions because agents handle the execution while we focus on direction.

**What they did:** Nate described 'open commitments' as tasks that cause mental buzzing. He recommends using agents to close them — meeting minutes, revised scopes, follow-up emails — so humans focus on decision-making.

**Relevance:** The YOLO loop accumulates open commitments during Phase 2/3 (unfinished refinements, dashboard updates, learnings not yet written).

### Create a design.md as an agent-readable design system

- **ID:** `nb-2026-03-28-design-md-agent-readable`
- **Channel:** NateBJones
- **Video:** A Markdown File Just Replaced Your Most Expensive Design Meeting (Google Stitch)
- **Published:** 2026-03-28 | **Ingested:** 2026-03-29
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we capture our UI design conventions in a structured markdown file (design.md), then AI agents will produce more visually consistent projects because they can reference explicit design tokens, color palettes, and layout patterns instead of improvising.

**What they did:** Google Stitch introduced Design.md — a markdown file that captures design systems so AI agents can read, understand, and build against consistent design patterns. This replaces the need for Figma handoffs.

**Relevance:** Every YOLO project reinvents its CSS from scratch. A shared design.md would compound visual quality across all builds.

### Use MCP to connect build agents to professional tools

- **ID:** `nb-2026-03-28-mcp-tool-integration`
- **Channel:** NateBJones
- **Video:** A Markdown File Just Replaced Your Most Expensive Design Meeting (Google Stitch)
- **Published:** 2026-03-28 | **Ingested:** 2026-03-29
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we connect the builder agent to external tools via MCP (e.g., image generation, 3D rendering, browser testing), then project ambition increases because the agent can leverage capabilities beyond just writing code.

**What they did:** Nate described MCP as 'USB for AI' — a universal connector letting AI agents interact with Blender, Remotion, and other professional tools. This removes the need for manual tool operation.

**Relevance:** The YOLO builder currently only writes code. MCP integration would expand what it can build (e.g., generate assets, test in real browsers).

### Adopt the Dark Factory pattern for autonomous builds

- **ID:** `nb-2026-03-25-dark-factory-pattern`
- **Channel:** NateBJones
- **Video:** Tobi Lutke Made a 20-Year-Old Codebase 53% Faster Overnight
- **Published:** 2026-03-25 | **Ingested:** 2026-03-29
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we restructure the YOLO build loop as a Dark Factory (spec in → autonomous processing → eval out with retry loops), then build quality increases because the agent iterates against automated tests until passing, removing the human bottleneck from the middle.

**What they did:** Nate described 'Dark Factories' as fully autonomous build pipelines: specification goes in, agent builds and tests iteratively, evaluation comes out. If tests fail, the agent loops back and tries again.

**Relevance:** The YOLO loop already has spec → build → test → fix. Formalizing it as a Dark Factory with explicit retry loops would reduce human intervention.

### Apply strict linting to all agent-generated code

- **ID:** `nb-2026-03-24-strict-linting-agents`
- **Channel:** NateBJones
- **Video:** Nvidia Just Open-Sourced What OpenAI Wants You to Pay Consultants For
- **Published:** 2026-03-24 | **Ingested:** 2026-03-29
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we add automated static analysis (ESLint, HTMLHint) to the test pipeline, then bug rates drop because agents are 'lazy developers' who take shortcuts unless forced to comply with standards.

**What they did:** Nate cited Factory.ai's finding that strict automated linting is required to force agents to adhere to clean code standards. Agents produce working-but-sloppy code without enforcement.

**Relevance:** Current test_project.py checks syntax and ID consistency but not code quality. Linting would catch style issues, unused vars, and potential bugs the current tests miss.

### Use incremental summarization for context compression in long sessions

- **ID:** `nb-2026-03-24-context-compression`
- **Channel:** NateBJones
- **Video:** Nvidia Just Open-Sourced What OpenAI Wants You to Pay Consultants For
- **Published:** 2026-03-24 | **Ingested:** 2026-03-29
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we implement incremental summarization (summarize segments, merge into structured persistent summary) for long YOLO build sessions, then context window usage drops and agent coherence improves because the agent retains key decisions without drowning in raw history.

**What they did:** Factory.ai found that incremental summarization — summarizing segments and merging them into a structured persistent summary — was the most effective approach to context compression for long agent sessions.

**Relevance:** Phase 2 refinement runs through many projects sequentially and already hits context limits. Structured summarization would help.

### Evaluate durable execution for long-running agent workflows

- **ID:** `mlops-2026-03-17-durable-execution-agents`
- **Channel:** MLOps
- **Video:** Durable Execution and Modern Distributed Systems
- **Published:** 2026-03-17 | **Ingested:** 2026-03-29
- **Effort:** high
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we structure long-running YOLO workflows (multi-project refinement, Phase 3 cull) as durable workflows with automatic state persistence, then we eliminate lost progress from crashes/disconnects because the system automatically resumes from the last checkpoint.

**What they did:** Johann Schleier-Smith from Temporal described durable execution: Workflows (deterministic control flow) + Activities (side effects with retries). State saved automatically. If failure occurs, replay from last known state. Especially valuable for AI agents running over days/weeks.

**Relevance:** The YOLO loop runs long sessions via cron that can fail mid-refinement. Durable execution would make the pipeline crash-proof.

### Adopt vertical planning with structure outlines before coding

- **ID:** `mlops-2026-03-25-qrspi-vertical-planning`
- **Channel:** MLOps
- **Video:** Everything We Got Wrong About Research-Plan-Implement - Dexter Horthy
- **Published:** 2026-03-25 | **Ingested:** 2026-03-30
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we add a structure outline phase (define signatures, types, interfaces before implementation) and plan vertically (small testable slices from data to UI), then we reduce rework because mistakes are caught at the design level before code is written.

**What they did:** Dexter Horthy found RPI (Research-Plan-Implement) fails at scale due to horizontal planning and mega-prompts exceeding instruction budgets (~150-200 max). QRSPI adds objective research (hide the task from researcher), design docs (~200 lines for alignment), structure outlines (signatures/types first), and vertical slicing.

**Relevance:** The YOLO builder currently goes from idea straight to code. Adding a lightweight structure outline could prevent the architectural bugs that Gemini catches in review.

### Restructure program.md as agent-readable skill files

- **ID:** `nb-2026-03-31-agent-readable-skills`
- **Channel:** NateBJones
- **Video:** Anthropic, OpenAI, and Microsoft Just Agreed on One File Format. It Changes Everything.
- **Published:** 2026-03-31 | **Ingested:** 2026-03-31
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we decompose program.md into discrete, focused skill files (build-skill.md, review-skill.md, test-skill.md) with specific descriptions and methodology sections, then the builder agent produces higher quality output because each skill provides focused context instead of one monolithic prompt.

**What they did:** Nate described skills as markdown files with a Description (tells agent when to trigger) and Methodology (instructions + reasoning). Best practices: specific descriptions with trigger phrases, under 150 lines per skill, reasoning over steps, lean design with 80% effort on description. Agent-first design means hundreds of skill calls per run.

**Relevance:** program.md is already ~200 lines and growing. Decomposing into skills would make each phase more focused and allow the Tick-Tock system to load only the relevant skill.

### Design skill outputs as composable handoffs

- **ID:** `nb-2026-03-31-skill-composability`
- **Channel:** NateBJones
- **Video:** Anthropic, OpenAI, and Microsoft Just Agreed on One File Format. It Changes Everything.
- **Published:** 2026-03-31 | **Ingested:** 2026-03-31
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we design each YOLO loop phase to produce output formatted as input for the next phase (brainstorm outputs a spec, spec feeds the builder, builder outputs code, code feeds the reviewer), then the pipeline becomes more reliable because each handoff has a clear contract.

**What they did:** Nate emphasized composability: the output of one skill should be perfectly formatted as input for the next agent in the chain. Design skills with clear SLAs defining exactly what the agent will and will not get.

**Relevance:** The YOLO loop already chains phases but the handoffs are implicit. Making them explicit contracts would improve autonomous execution.

### Implement autoresearch loop for YOLO project optimization

- **ID:** `do-2026-03-31-autoresearch-loop`
- **Channel:** DavidOndrej
- **Video:** The only AutoResearch tutorial you will ever need
- **Published:** 2026-03-31 | **Ingested:** 2026-03-31
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we structure the YOLO build loop as a Karpathy-style autoresearch loop (single file to edit, single metric to optimize, automated eval, git commit on success / reset on failure), then project quality improves autonomously because the agent iterates hundreds of times without human intervention.

**What they did:** Karpathy's AutoResearch uses a 3-file architecture: program.md (goals/constraints), train.py (editable file), prepare.py (read-only metric). The loop: hypothesize → modify → train → evaluate → keep/discard → repeat. Applied to ML training, website optimization (50ms→25ms load time), trading strategies, prompt engineering.

**Relevance:** The YOLO loop already has program.md and test_project.py. Adding a metric-driven feedback loop would be a natural evolution — especially for the refinement phase.

### Build a Council skill for multi-perspective task review

- **ID:** `up-2026-03-31-personal-ai-infrastructure`
- **Channel:** [un]prompted
- **Video:** Anatomy of an Agentic Personal AI Infrastructure
- **Published:** 2026-03-31 | **Ingested:** 2026-03-31
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we spin up multiple specialized agents to debate a task from different perspectives (security, performance, UX, architecture) before committing code, then build quality improves because blind spots from any single perspective are caught before shipping.

**What they did:** Daniel Miessler's PAI system includes a Council feature that spins up a group of specialized agents to debate a task from multiple perspectives before providing a final recommendation. Also includes IterativeDepth (same question from multiple angles) and TheAlgorithm (reverse-engineer ambiguous goals into testable criteria).

**Relevance:** Currently the YOLO loop uses one Gemini review pass focused on bugs. Adding perspective-specific passes (security, perf, UX) could catch more issues.

### Run parallel agent sessions for independent YOLO tasks

- **ID:** `mlops-2026-04-01-agent-orchestration-cloud`
- **Channel:** MLOps
- **Video:** 2026 The Year of Agent Orchestration
- **Published:** 2026-03-31 | **Ingested:** 2026-04-01
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we run multiple agent sessions in parallel (e.g., 3 Tick builds simultaneously using subagents), then throughput increases because independent builds do not need sequential execution — each gets its own context and tools.

**What they did:** Zach Lloyd (Warp/Oz) argued local agents hit capacity limits. Cloud orchestration enables multiple parallel agents, persistent background execution, and team visibility. Demo showed launching multiple agent sessions simultaneously to implement independent features.

**Relevance:** We already use subagents for Tick builds. Formalizing parallel execution for independent builds would increase throughput significantly.

### Build a golden dataset of past bugs as an eval suite

- **ID:** `mlops-2026-04-01-coding-agent-evals`
- **Channel:** MLOps
- **Video:** Stop Shipping on Vibes — How to Build Real Evals for Coding Agents
- **Published:** 2026-03-31 | **Ingested:** 2026-04-01
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we extract 20-30 past Gemini-caught bugs from learnings.md as test cases (input: buggy code, expected: the fix), then we can measure whether future agent builds avoid those same bug patterns — turning learnings into a regression test.

**What they did:** Conference talk on building evals for coding agents. Key insight: mine your own past bugs as a proprietary eval suite. Also: execution-based evals (run the code, not string comparison), trajectory evaluation (track tool calls), and tiered eval systems (unit → tool → end-to-end).

**Relevance:** learnings.md has 350+ bug fixes documented. Mining them into an automated regression check would compound the value of all that accumulated knowledge.

### Filter YOLO Tick ideas through the 'boring-but-high-ROI' automation criteria

- **ID:** `nh-2026-03-29-boring-automation-products`
- **Channel:** NateHerk
- **Video:** 5 ‘Boring’ AI Workflows that Businesses Actually Want (And Pay For)
- **Published:** 2026-03-29 | **Ingested:** 2026-04-01
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we bias YOLO Tick session ideas toward the 'boring automation' patterns (repeatable, unglamorous, businesses actually pay for), then the portfolio generates more commercial value because automations addressing real business pain points (lead gen, data extraction, CRM, email nurturing, reporting) have proven paying customers vs. flashy demos that nobody wants.

**What they did:** NateHerk distilled 500 AI workflows into 5 boring patterns that businesses consistently pay for in 2026. The core insight: the most commercially valuable automations are not impressive demos — they are repeatable solutions to mundane tasks. The 5 categories include lead generation, email nurturing sequences, document data extraction, CRM integration, and automated business reporting. All implemented via n8n.

**Relevance:** YOLO builds 1 project per Tick. Applying the 'boring automation' filter during Gemini brainstorm would bias the portfolio toward commercially useful tools without changing the build protocol. Could double as a product discovery exercise.

### Adopt Codex-as-planner + Claude Code-as-executor 3-phase build cycle

- **ID:** `nh-2026-03-30-codex-plan-claude-execute`
- **Channel:** NateHerk
- **Video:** Codex Just 10x’d Claude Code Projects
- **Published:** 2026-03-30 | **Ingested:** 2026-04-01
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we use Codex to generate a structured plan (iterating clarifying questions until 95% confidence) before handing to Claude Code for execution, then we reduce mid-build architectural rework because ambiguity is resolved upfront rather than surfaced in Gemini review after code is written.

**What they did:** NateHerk demonstrated a 3-phase workflow with the official Codex plugin for Claude Code: (1) Planning — use Codex to ask clarifying questions iteratively until 95% confidence in a complete plan before any implementation begins. (2) Execution — copy the plan into Claude Code which implements systematically with full context. (3) Review — take the git diff back to Codex to verify implementation matches plan and catch missed edge cases. Benchmarks showed Opus 4.6 for deep implementation and GPT models for structured analysis.

**Relevance:** The YOLO loop goes from Gemini brainstorm directly to Claude build. Inserting a Codex planning step before execution could catch architectural issues before they become Gemini review bugs, directly reducing the Dark Factory retry loop count.

**Notes:** Partially overlaps with mlops-2026-03-27-specialized-agent-team (abstract specialized roles). This card is the concrete tool-specific implementation: Codex plan → Claude Code execute → Codex diff review.

### Run a 4-layer stack audit before every major Claude model upgrade

- **ID:** `nb-2026-04-01-model-upgrade-stack-audit`
- **Channel:** NateBJones
- **Video:** Anthropic Just Built a Model That Breaks Everything (Claude Mythos Is Nigh)
- **Published:** 2026-04-01 | **Ingested:** 2026-04-02
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we audit each layer of the YOLO build loop (system prompts, retrieval, verification, orchestration) before upgrading to a new Claude model, then we remove brittle workarounds before they break because stronger models expose — not hide — architectural debt built around weaker predecessors.

**What they did:** Nate analyzed Claude Mythos (Anthropic's new capability tier above Opus) and described how production AI stacks built around model weaknesses become brittle when the model improves. He proposed a 4-question diagnostic audit (one per stack layer) and a 'simplification pattern': strip workarounds proactively because complex prompt engineering that patched around gaps in weaker models becomes noise for stronger ones. The Klarna case study showed the cost of ignoring this principle.

**Relevance:** skills/ and program.md contain rules written to patch around old model behaviors. As Claude 4.x capabilities improve, some of these become dead weight that confuses rather than guides. A pre-upgrade audit keeps the loop lean and avoids the Klarna anti-pattern.

### Track the Anthropic MCP technical roadmap and adopt spec updates proactively

- **ID:** `mlops-2026-04-02-mcp-spec-roadmap`
- **Channel:** MLOps
- **Video:** MCP Dev Summit [Day 1] ft. Anthropic, Hugging Face, Open AI & Microsoft
- **Published:** 2026-04-02 | **Ingested:** 2026-04-02
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we monitor Anthropic's MCP spec roadmap (as presented by David Soria Parra) and update our tool integrations to align with emerging MCP standards, then our agent tool usage remains forward-compatible and gains new capabilities as the spec matures.

**What they did:** The MCP Dev Summit brought together Anthropic, Hugging Face, OpenAI, and Microsoft to standardize MCP as the universal intelligence layer for agents. David Soria Parra (Anthropic) presented the technical roadmap. The summit signals MCP is becoming a true industry standard — not just an Anthropic protocol.

**Relevance:** MCP is already adopted in the YOLO loop (Gemini code review, brainstorm, Phase 4 ingestion). Staying aligned with the evolving spec ensures tools don't break on updates and new capabilities (e.g., streaming, multi-modal tool calls) can be leveraged.

**Notes:** Summit also covered: Hugging Face MCP integrations, OpenAI and Microsoft MCP adoption signals.

### Build a golden-prompt eval suite to detect model regression after upgrades

- **ID:** `mlops-2026-04-01-continuous-model-eval`
- **Channel:** MLOps
- **Video:** Choosing the Right Model is Hard. Maintaining Accuracy is Harder.
- **Published:** 2026-04-01 | **Ingested:** 2026-04-02
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we maintain a set of 5-10 representative YOLO build prompts as a regression suite and run it after any model upgrade, then we catch model behavioral changes before they affect production builds because we have a measurable baseline to compare against.

**What they did:** Ash Lewis (Fastino) argued at the Coding Agents Conference that model selection is not one-time — models update, drift, or get replaced, and production accuracy degrades silently. Her team uses agents to continuously test, swap, and tune model choices in production rather than hardcoding a single model.

**Relevance:** The YOLO loop uses claude-sonnet-4-6 throughout. When Claude updates (new versions, behavioral changes), there is currently no mechanism to detect regression. A golden prompt suite would catch these before they silently break build quality.

**Notes:** Complements mlops-2026-04-01-coding-agent-evals which focuses on past bugs as evals; this card focuses on model regression detection.

### Add structured debug logging at agent decision points to speed up failure diagnosis

- **ID:** `mlops-2026-03-31-agent-debug-logging`
- **Channel:** MLOps
- **Video:** Decomposing the Agent Orchestration System: Lessons Learned
- **Published:** 2026-03-31 | **Ingested:** 2026-04-02
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we emit structured log events at each major agent decision (tool call initiated, response evaluated, branch taken, test outcome), then diagnosing build failures takes minutes instead of hours because we have a complete audit trail of what the agent decided and why.

**What they did:** Niels Bantilan (Union.ai) at the Coding Agents Conference argued that production agent failures are almost always infrastructure and debuggability failures — not model failures. Durable, self-healing, debuggable systems beat flashy model features. Key lesson: invest in observability before capability.

**Relevance:** YOLO build sessions currently fail silently — if a test fails or Gemini review reveals issues, there's no structured log of what decisions led there. Adding event logging (even to a simple JSONL file) would make post-mortems faster and identify patterns across failures.

**Notes:** Concept reinforced by mlops-2026-03-17-durable-execution-agents (done/adopt). This card focuses on the observability/logging angle specifically.

### Wire a self-critique step into the YOLO build loop before running external tests

- **ID:** `do-2026-03-29-self-improving-eval-loop`
- **Channel:** DavidOndrej
- **Video:** This 100% self-improving AI Agent is insane… just watch
- **Published:** 2026-03-29 | **Ingested:** 2026-04-02
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we add a self-evaluation step where the builder agent critiques its own code against the acceptance criteria before running test_project.py, then the test pass rate on first attempt improves because obvious issues are self-corrected earlier, reducing total retry cycles.

**What they did:** David demonstrates an agent (Agent Zero + Hermes) that generates a solution, then enters a closed self-improvement loop: evaluate output against success criteria, identify gaps, regenerate, repeat. The loop runs autonomously until the evaluation passes — no human in the middle.

**Relevance:** The YOLO Dark Factory loop already retries on test failure, but the retry is triggered by external tests. Adding a pre-test self-critique (agent asks 'does this code actually satisfy the acceptance criteria I defined?') could catch issues before the test suite runs, reducing the outer retry loop.

**Notes:** Agent Zero is open-source; Hermes is the evaluation model used for self-scoring. See: https://github.com/agent0ai/agent-zero

### Apply /compact at defined YOLO session milestones to preserve context within token limits

- **ID:** `nh-2026-04-02-compact-at-milestones`
- **Channel:** NateHerk
- **Video:** 18 Claude Code Token Hacks in 18 Minutes
- **Published:** 2026-04-02 | **Ingested:** 2026-04-02
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we run /compact at defined YOLO session checkpoints (after reading learnings.md, after build completes, before logging), then we reduce mid-session token exhaustion while retaining all decision context because /compact preserves key information in a fraction of the tokens.

**What they did:** Nate Herk shares 18 practical Claude Code token optimization techniques. Key relevant ones: use /compact aggressively at natural break points, write minimal CLAUDE.md files (every line costs tokens on every session), use sub-agents for isolated tasks to prevent context cross-contamination.

**Relevance:** Long YOLO sessions (Phase 2 refinement, multi-project builds) are most vulnerable to token runaway. Defining 3-4 explicit /compact checkpoints (post-context-load, post-build, pre-logging) would systematize what currently happens ad-hoc.

**Notes:** Extends nb-2026-03-24-context-compression (adopted) with specific /compact workflow. Also relates to nb-2026-04-02-session-isolation-per-task — use both together.

### Use Pretext library for instant text measurement without DOM reflows

- **ID:** `fs-2026-04-02-pretext-text-measurement`
- **Channel:** Fireship
- **Video:** He just crawled through hell to fix the browser...
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we integrate Pretext (pure TypeScript text measurement library by Cheng Lou) into text-heavy YOLO projects, then virtualized lists and dynamic layouts become trivially fast because text dimensions are computed via Canvas API without triggering browser reflows.

**What they did:** Cheng Lou built Pretext — uses canvas.measureText() for width and an automated recursive browser-testing loop for line-break height calculation. Two-step API: prepare() caches segment widths, layout() returns exact pixel height instantly. Zero DOM touching.

**Relevance:** Several YOLO projects render dynamic text (markdown-deck slide content, prose-xray text analysis, log-lens log viewer). Pretext could eliminate layout jank in text-heavy tools. Also relevant for harness-cli if it ever renders terminal UIs.

### Evaluate Junie CLI multi-model routing for harness-cli council

- **ID:** `fs-2026-04-02-junie-cli-multi-model`
- **Channel:** Fireship
- **Video:** He just crawled through hell to fix the browser...
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we route different council angles to different models (e.g. Claude for architecture, Gemini for security, GPT-4 for product) like Junie auto-switches models per task, then council quality improves because each model has different strengths.

**What they did:** JetBrains Junie CLI automatically switches between GPT-4, Claude Haiku, and Gemini Flash depending on the task — optimizing for speed, cost, and capability per call.

**Relevance:** Directly applicable to harness-cli council. Currently all 3 council angles use the same model. Multi-model routing could improve quality and reduce cost by using cheaper models for simpler angles.

### Audit PAI agent stack against the 12 critical agent architecture pieces

- **ID:** `nb-2026-04-03-agent-architecture-12-pieces`
- **Channel:** NateBJones
- **Video:** I Broke Down Anthropic's $2.5 Billion Leak. Your Agent Is Missing 12 Critical Pieces.
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we audit our agent infrastructure against Anthropic's leaked 12-piece agent architecture checklist, then we identify structural gaps (missing guardrails, evaluation layers, memory systems, etc.) because Anthropic's internal architecture reflects what they've learned building production agents at scale.

**What they did:** Nate broke down Anthropic's leaked $2.5B internal agent architecture into 12 critical components that production agents need. The implication is most DIY agents are missing key structural pieces.

**Relevance:** PAI is a production agent system. Validating its architecture against Anthropic's internal best practices ensures we aren't missing critical infrastructure layers.

**Notes:** Title-only inference. Need to watch video or find summary for the actual 12 pieces.

### Add explicit guardrail and fallback layers to autonomous build agents

- **ID:** `nb-2026-04-03-agent-guardrails-leak`
- **Channel:** NateBJones
- **Video:** I Broke Down Anthropic's $2.5 Billion Leak. Your Agent Is Missing 12 Critical Pieces.
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** medium
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we add explicit guardrail layers (cost caps, output validation, rollback triggers) to YOLO build agents, then autonomous builds become safer for higher-stakes projects because failures are caught and contained before they propagate.

**What they did:** The leaked Anthropic architecture implies production agents need guardrails as a distinct layer — not just prompting, but structural boundaries on agent behavior, cost, and output scope.

**Relevance:** As YOLO builds become more autonomous (Dark Factory pattern), explicit guardrails prevent costly failures and give confidence to increase autonomy further.

**Notes:** Adopted 2026-04-07: formalize structural guardrails (cost caps, output validation, rollback triggers) on top of existing approval gate + pre-filter. Maps to current "3 attempts then escalate" pattern. Low net-new work — mostly capturing what we already do as explicit constraints in program.md.

### Add security scanning to the YOLO build pipeline for AI-generated code

- **ID:** `mlops-2026-04-03-ai-code-security`
- **Channel:** MLOps
- **Video:** Practical Security for AI-generated Code
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we add automated security scanning (SAST, dependency audit, secrets detection) to the YOLO build pipeline, then we catch vulnerabilities introduced by AI-generated code before they ship because AI models can introduce insecure patterns (hardcoded secrets, SQL injection, XSS) that pass functional tests.

**What they did:** MLOps presented practical security measures specifically for AI-generated code — addressing the unique vulnerability patterns that LLMs introduce compared to human-written code.

**Relevance:** YOLO builds ship fast with AI-generated code. Security scanning is the missing layer between Gemini code review (which focuses on quality) and deployment.

**Notes:** Title-only inference. Complements existing Gemini code review with security-specific scanning.

### Build custom evals that measure real YOLO build quality beyond synthetic benchmarks

- **ID:** `mlops-2026-04-03-beyond-swebench-evals`
- **Channel:** MLOps
- **Video:** Beyond SWE-Bench Pro - Where do Agents go from Here?
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** medium
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we design custom evaluation metrics tailored to YOLO project requirements (user experience quality, feature completeness, maintainability) rather than relying on generic benchmarks, then we get a more accurate picture of agent capability because SWE-Bench style metrics don't capture what matters for our use case.

**What they did:** MLOps discussed the limitations of SWE-Bench Pro as a coding agent benchmark and explored what comes next — real-world evals that measure agent performance on actual engineering tasks beyond isolated bug fixes.

**Relevance:** Related to mlops-2026-04-01-coding-agent-evals but focuses on going beyond generic benchmarks to YOLO-specific quality metrics.

**Notes:** Adopted 2026-04-07: extends current test_project.py + eval_bugs.py + security_scan.py with YOLO-specific lenses. Low effort, real value. Next step: write 2-3 new lens scripts (e.g., ux-completeness.py, mobile-usability.py, cult-status.py).

### Implement structured memory retrieval so the build agent learns from past builds

- **ID:** `mlops-2026-04-03-self-learning-agent-memory`
- **Channel:** MLOps
- **Video:** How to Fix Your Agent's Amnesia: Lessons from Building a Self-learning Agent
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** medium
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we give the build agent structured access to past build outcomes (what worked, what failed, which patterns caused bugs), then build quality compounds over time because the agent doesn't repeat mistakes and reinforces successful patterns.

**What they did:** MLOps presented lessons from building a self-learning agent — specifically how to fix the 'amnesia' problem where agents forget context between sessions and keep making the same mistakes.

**Relevance:** The YOLO loop already has learnings.md but it's read passively. Making it an active memory retrieval system would close the learning loop.

**Notes:** Adopted 2026-04-07: validates and extends current build_memory.py (1916 learnings, 263 projects, FTS5). Adoption work: add a feedback loop logging "did the recalled learning prevent a bug?" so we can measure the angle's value over time.

### Add automatic post-build reflection that writes back to agent memory

- **ID:** `mlops-2026-04-03-self-learning-feedback-loop`
- **Channel:** MLOps
- **Video:** How to Fix Your Agent's Amnesia: Lessons from Building a Self-learning Agent
- **Published:** 2026-04-02 | **Ingested:** 2026-04-03
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If the build agent automatically reflects after each build (what went well, what went wrong, what to do differently) and writes structured entries to its memory, then the memory grows organically without human curation because the agent maintains its own knowledge base.

**What they did:** The self-learning agent approach implies a write-back loop: agent acts, evaluates outcome, writes learnings to persistent memory, retrieves them in future sessions.

**Relevance:** Currently learnings.md is human-curated. Automating the write-back loop would make the system truly self-learning.

**Notes:** Title-only inference. Companion to self-learning-agent-memory — this is the write side, that is the read side.

### Implement compounding agent memory that improves with each build

- **ID:** `nb-2026-04-04-compounding-agent-memory`
- **Channel:** NateBJones
- **Video:** Wall Street Just Bet $285 Billion on AI Agents. The Best One Barely Works.
- **Published:** 2026-04-04 | **Ingested:** 2026-04-05
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If the build agent accumulates structured context about past builds (what patterns worked, which codebases have which quirks, user preferences) in a queryable store rather than a flat text file, then build 100 is dramatically better than build 1 because the agent compounds knowledge instead of starting fresh.

**What they did:** NateBJones analyzed successful vs failing agent startups. Winners have persistent memory as a database layer (Postgres + MCP), not afterthought text files. Agents that compound context over time outperform those that start fresh. Likened memory to a substrate, not a feature.

**Relevance:** learnings.md is 3000+ lines of flat text. The build agent reads it but cannot query it. A structured memory store (SQLite or indexed JSON) with per-project, per-pattern, per-bug entries would let the agent ask "what went wrong last time I built a JWT tool?" instead of skimming 3000 lines.

### Create pre-wired agent recipes instead of blank-canvas prompting

- **ID:** `nb-2026-04-04-agent-recipe-presets`
- **Channel:** NateBJones
- **Video:** Wall Street Just Bet $285 Billion on AI Agents. The Best One Barely Works.
- **Published:** 2026-04-04 | **Ingested:** 2026-04-05
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we create named recipe presets for common tasks ("new devtool", "flagship feature", "bug fix", "code review", "refactor") with pre-loaded context and tool configurations, then agent success rate increases because each recipe eliminates the prompt engineering step and provides the right context automatically.

**What they did:** Successful agents use "punch card" recipes — pre-wired workflows like Code Review Recipe, Unit Test Generator, Boilerplate Setup. Users pick a recipe instead of writing prompts from scratch. Abstracts complexity while keeping output editable.

**Relevance:** Directly applicable to harness-cli. Instead of , offer , ,  with pre-loaded council configurations, context gathering, and plan templates per recipe type.

### Deploy evaluative agents alongside generative agents to eliminate review bottleneck

- **ID:** `nb-2026-04-05-evaluative-agents-review-bottleneck`
- **Channel:** NateBJones
- **Video:** Your Agent Produces at 100x. Your Org Reviews at 3x.
- **Published:** 2026-04-05 | **Ingested:** 2026-04-06
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we build Agent B to review/filter Agent A output before human review (pre-filtered council), then the human only sees pre-audited work and the 100x/3x bottleneck disappears.

**What they did:** NateBJones argues scaling agent output breaks human review capacity. Solution: secondary LLM agents as critical thinkers that auto-filter and auto-fix before human sees anything. Also: independent observability (never trust agent self-reporting).

**Relevance:** We already do this — the 6-angle council IS the evaluative agent layer. But we could add an automated pre-filter that rejects builds with test failures or security issues BEFORE council runs, saving Gemini calls.

### Build independent observability that never trusts agent self-reporting

- **ID:** `nb-2026-04-05-independent-observability`
- **Channel:** NateBJones
- **Video:** Your Agent Produces at 100x. Your Org Reviews at 3x.
- **Published:** 2026-04-05 | **Ingested:** 2026-04-06
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we add an independent verification layer that checks actual outcomes (file exists, tests pass, git committed) instead of trusting the agent's claim that it did the work, then we catch silent failures that currently slip through.

**What they did:** NateBJones: never ask the agent "did you do it?" — build automated auditing that independently verifies. Stack traces, logs, health monitors that validate without asking.

**Relevance:** Our Phase 4 cron failed silently for days because we trusted the agent to commit. The status protocol partially addresses this but we could add a post-build verification script that independently checks: does the project folder exist? Does index.html exist? Did test_project.py actually run?

### Implement Karpathy hot-cache pattern for instant agent context recovery

- **ID:** `nh-2026-04-05-karpathy-llm-wiki-hot-cache`
- **Channel:** NateHerk
- **Video:** Andrej Karpathy Just 10x'd Everyone's Claude Code
- **Published:** 2026-04-05 | **Ingested:** 2026-04-06
- **Effort:** low
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we maintain a _hot.md file (~500 tokens) that the agent reads at session start containing active threads, key metrics, and recent decisions, then context recovery drops from reading 3000+ lines to reading 500 tokens — 95% reduction.

**What they did:** Karpathy uses flat Markdown wiki with CLAUDE.md rules, index.md catalog, log.md history, and a _hot.md "hot cache" that auto-updates at end of each session with the most relevant current context. Agent reads _hot.md first, skips full wiki unless needed.

**Relevance:** Directly applicable. Our cron reads learnings.md (3000+ lines) every session. A _hot.md with the last 5 builds, current queue state, and active issues would give the agent instant context without the full scan. build_memory.py could auto-generate _hot.md.

### Build a skill-creator meta-agent that writes SKILL.md files from successful interactions

- **ID:** `st-2026-04-05-skill-creator-meta-agent`
- **Channel:** ShawTalebi
- **Video:** How to Automate Anything with Claude (4-Step Framework)
- **Published:** 2026-04-05 | **Ingested:** 2026-04-06
- **Effort:** medium
- **Status:** done | **Verdict:** adopt

**Hypothesis:** If we have an agent whose only job is to observe successful build sessions and extract reusable skill documents (trigger, steps, output format, edge cases), then our methodology self-documents and new skills emerge automatically from practice.

**What they did:** Shaw Talebi 4-step framework: (1) do task once with AI manually, (2) distill into a SKILL.md with trigger/steps/format/rules, (3) test in fresh session, (4) iterate and update skill on errors. Progressive disclosure: load skill names only, pull full SKILL.md on demand.

**Relevance:** Directly applicable to harness-cli recipes. Instead of manually writing recipe presets, a meta-agent could watch successful harness plan sessions and auto-generate new recipes. Also: the progressive disclosure pattern maps to how we could load council personas on-demand instead of all at once.

### Classify Each YOLO Loop Dependency by Shelf-Life and Replaceability

- **ID:** `nb-2026-04-07-ephemeral-layers-stack-audit`
- **Channel:** NateBJones
- **Video:** You're Building AI Agents on Layers That Won't Exist in 18 Months. (What this Means for You)
- **Published:** 2026-04-07 | **Ingested:** 2026-04-07
- **Effort:** medium
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we tag every external library, orchestration framework, and model API in our stack with an estimated deprecation horizon, then we can isolate business logic from ephemeral scaffolding and reduce future rework, because agent frameworks (LangChain, AutoGPT-style wrappers) are historically replaced by native model capabilities within 12-18 months.

**What they did:** Speaker argued that current AI agent frameworks and middleware layers (orchestration libs, memory stores, tool-calling wrappers) will be absorbed directly into foundation models or superseded by new paradigms, making code tightly coupled to them a liability. Recommended building on thin abstractions or owning the logic layer independently of any specific framework.

**Relevance:** Directly applies to how the YOLO loop chains tools: if orchestration glue (e.g., specific agent frameworks) is ephemeral, the loop should be architected so the core spec-execute-eval cycle is framework-agnostic and the integration points are swappable.

**Notes:** Adopted 2026-04-08 as a ONE-TIME deliverable, not ongoing infrastructure. Produce STACK_AUDIT.md for harness-cli listing each dependency (Next.js, Anthropic SDK, Gemini SDK, commander, chalk, etc.) with: estimated deprecation horizon, what would replace it, how tightly coupled our code is, and migration cost. Snapshot only — do not maintain ongoing horizon tags. YOLO single-file HTML tools pass this trivially (zero deps) so they need no audit.

### Build a Bare-Metal Minimal Agent Loop with No Framework Dependencies

- **ID:** `do-2026-04-07-minimal-agent-pattern`
- **Channel:** DavidOndrej
- **Video:** This 100% minimal AI Agent can do anything… just watch
- **Published:** 2026-04-07 | **Ingested:** 2026-04-07
- **Effort:** low
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we implement the smallest possible agent loop (LLM call → tool dispatch → result injection → repeat) using only raw API calls and a dictionary-based tool registry, then we will have a maximally understandable and portable core that can be extended without framework lock-in, because the video demonstrates that a dozen lines of Python are sufficient for a fully functional general agent.

**What they did:** Speaker live-coded a minimal AI agent from scratch: a while-loop that sends a prompt to an LLM, parses a structured tool-call response, executes the matched Python function, appends the result to the conversation, and loops until the model signals completion. No LangChain, no AutoGPT. Showed it browsing the web, writing files, and calling APIs.

**Relevance:** This is a candidate replacement or reference implementation for the orchestration layer of the YOLO loop. Testing whether our current loop can be simplified to this pattern would reduce complexity and improve debuggability.

**Notes:** Adopted 2026-04-08: run as a bifurcation comparison study. Build the bare-metal 50-line agent loop and run it on one harness-cli project (roadtripper or sportsdata). Measure where harness-cli's overhead is real vs. ceremonial. Result feeds the YOLO/Harness bifurcation memory. ~1 day of work, high signal value about whether harness-cli is actually justified vs. could be replaced by a thin core.

### Use Claude Code's New Planning Mode as a Spec-Decomposition Pre-Pass

- **ID:** `nh-2026-04-07-claude-code-planning-mode`
- **Channel:** NateHerk
- **Video:** Planning In Claude Code Just Got a Huge Upgrade
- **Published:** 2026-04-07 | **Ingested:** 2026-04-07
- **Effort:** low
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we invoke Claude Code's upgraded planning mode before any implementation task in the YOLO loop, then the resulting step-by-step plan will surface ambiguities and scope issues earlier, reducing mid-task derailments, because the new planning pass forces explicit sub-task enumeration and dependency identification before any code is written.

**What they did:** Speaker demonstrated a newly upgraded planning feature in Claude Code that, when triggered, produces a detailed hierarchical task plan (with subtasks, file targets, and sequencing) before writing any code. Showed side-by-side comparison of runs with and without planning mode, with planning-mode runs completing complex multi-file refactors more reliably.

**Relevance:** The YOLO loop's spec stage could be augmented with this planning pre-pass: feed the spec to Claude Code in planning mode, review the decomposition, then execute. This adds a lightweight human-in-the-loop checkpoint at minimal cost.

**Notes:** Adopted 2026-04-08: most directly applicable of the 6. Wire into PLAN gate as "use Claude Code planning mode for the experiments/<name>/plan.md deliverable rather than free-form prose." One-line tick prompt change. Tiny work, direct fit with current 4-gate council.

### Benchmark Claude Mythos on Open-Ended Agentic Tasks in the YOLO Loop

- **ID:** `do-2026-04-08-claude-mythos-agentic-eval`
- **Channel:** DavidOndrej
- **Video:** Claude Mythos might actually be AGI… wtf
- **Published:** 2026-04-08 | **Ingested:** 2026-04-08
- **Effort:** low
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we run Claude Mythos on our existing suite of multi-step agentic tasks inside the YOLO loop, then we will observe measurably fewer clarification requests and higher task completion rates compared to prior Claude versions, because the model reportedly demonstrates stronger autonomous reasoning and self-correction.

**What they did:** Speaker demoed Claude Mythos performing complex, multi-step reasoning and agentic tasks with minimal human intervention, arguing its behavior qualitatively resembles AGI-level generalization across novel problems.

**Relevance:** If Mythos reduces mid-loop failures and clarification interrupts, it could replace or augment our current backbone model in the YOLO loop with minimal prompt changes, improving end-to-end task throughput.

**Notes:** Adopted 2026-04-09: low-effort model-swap benchmark. Reframed from 'Claude Mythos' (unverifiable marketing name) to 'latest-Claude-vs-current-backbone on N historical YOLO build specs, measuring clarification requests, council retry count, and completion rate'. Promoted to tick_queue_approved as 'model-eval-backbone'.

### Benchmark Claude Managed Agents Against Manual Orchestration on a Multi-Step Dev Task

- **ID:** `nh-2026-04-09-claude-managed-agents`
- **Channel:** NateHerk
- **Video:** I Tested Claude's New Managed Agents... What You Need To Know
- **Published:** 2026-04-09 | **Ingested:** 2026-04-09
- **Effort:** medium
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we replace our hand-rolled agent orchestration with Claude's native managed agents API, then task completion reliability will improve and boilerplate coordination code will decrease, because Anthropic's managed layer handles context passing, subagent lifecycle, and error recovery natively.

**What they did:** Nate walked through Claude's new managed agents feature, demonstrating how Anthropic now provides a first-party orchestration layer for spawning and coordinating subagents, and evaluated what developers need to know to adopt it.

**Relevance:** Directly relevant to the orchestration layer of the YOLO loop. If managed agents reduce coordination overhead, we can simplify the loop's dispatch logic and focus effort on task design and eval rather than plumbing.

**Notes:** Adopted 2026-04-12: medium-effort orchestration benchmark. Claude Managed Agents (/v1/agents, /v1/sessions) are a first-party orchestration layer that could simplify the tick-tock dispatch logic. Promoted to tick_queue_approved as 'eval-managed-agents'.

### Audit current build position against the 5 safe AI niches framework

- **ID:** `nb-2026-04-10-five-safe-places-ai`
- **Channel:** NateBJones
- **Video:** There Are Only 5 Safe Places to Build in AI Right Now. Are You in One?
- **Published:** 2026-04-10 | **Ingested:** 2026-04-10
- **Effort:** low
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we map our AI development focus to one of the 5 identified defensible niches, then we can reduce strategic risk and prioritize features that align with durable value creation because undifferentiated AI tooling is being rapidly commoditized.

**What they did:** Nate laid out a framework of 5 specific categories where builders are insulated from commoditization pressure, likely covering areas like vertical workflow automation, proprietary data moats, or regulated industries.

**Relevance:** Informs which experiment categories to prioritize in the backlog; any experiment outside the 5 niches should be flagged for strategic review before investment.

**Notes:** Adopted 2026-04-12: low-effort strategic positioning audit. Maps YOLO loop focus to the 5 defensible AI niches framework. Complements existing experiment triage — any future experiment outside the 5 niches gets flagged for strategic review. Promoted to tick_queue_approved as 'strategic-niche-audit'.

### Benchmark Claude Haiku or Sonnet against Opus on YOLO Loop tasks and measure cost-quality tradeoff

- **ID:** `nh-2026-04-10-claude-stop-using-best-model`
- **Channel:** NateHerk
- **Video:** Claude Just Told Us to Stop Using Their Best Model
- **Published:** 2026-04-10 | **Ingested:** 2026-04-10
- **Effort:** low
- **Status:** adopted | **Verdict:** adopted

**Hypothesis:** If we route routine YOLO Loop tasks to a smaller Claude model instead of defaulting to the flagship model, then we will achieve comparable output quality at significantly lower cost and latency because Anthropic's own guidance suggests flagship models are over-specified for many production tasks.

**What they did:** Nate reported that Anthropic recommended against using their most capable model for typical use cases, implying that smaller models in the Claude family handle the majority of production tasks with better cost-efficiency and that the largest model should be reserved for specific high-complexity needs.

**Relevance:** Directly impacts model selection defaults in the loop; a simple routing experiment could reduce API costs significantly without degrading loop output quality.

**Notes:** Adopted 2026-04-12: low-effort cost-quality benchmark. Directly complements model-eval-backbone already in tick queue. Merged scope: model-eval-backbone will now also test Haiku/Sonnet vs Opus, not just 'latest vs current'. No separate tick needed — folded into existing model-eval-backbone deliverables.

---

## Discarded Experiments

| ID | Video | Channel | Effort | Reason |
|---|---|---|---|---|
| `nb-2026-03-29-scheduled-tasks-monitoring` | Anthropic Just Gave You 3 Tools That Work While Yo | NateBJones | low | No reason recorded |
| `nb-2026-03-25-auto-research-metric-optimization` | Tobi Lutke Made a 20-Year-Old Codebase 53% Faster  | NateBJones | medium | No reason recorded |
| `nb-2026-03-24-agent-readiness-checklist` | Nvidia Just Open-Sourced What OpenAI Wants You to  | NateBJones | high | No reason recorded |
| `mlops-2026-03-27-specialized-agent-team` | Lessons from 25 Trillion Tokens — Scaling AI-Assis | MLOps | medium | The 3-phase pipeline within a single agent captures most of the value. |
| `mlops-2026-03-27-trust-ladder-adoption` | Lessons from 25 Trillion Tokens — Scaling AI-Assis | MLOps | low | Parked, not discarded permanently. |
| `nh-2026-04-01-claude-md-optimization` | All of Claude Code Just Leaked — How to Become a T | NateHerk | low | Parked, not permanently discarded. |
| `do-2026-03-27-private-local-agent` | RIP OpenClaw… this 100% private AI Agent is insane | DavidOndrej | high | Park until 48GB+ VRAM hardware. |
| `nh-2026-03-31-paperclip-agent-org` | Claude Code + Paperclip Just Destroyed OpenClaw | NateHerk | medium | Parked pending specialist experiment outcome. |
| `tmp-2026-04-01-quantized-local-inference` | Google's New AI Just Broke My Brain (TurboQuant) | TwoMinutePapers | medium | Parked. |
| `nb-2026-04-02-session-isolation-per-task` | Your Claude Limit Burns In 90 Minutes Because Of O | NateBJones | low | Parked, architecture already provides this. |
| `do-2026-04-03-gemma4-local-review` | Gemma 4 is insane… best open-source model ever?! | DavidOndrej | medium | Discarded 2026-04-07: local-model policy decision = NO. |
| `nh-2026-04-03-ollama-claude-code-cost` | Ollama + Claude Code = 99% CHEAPER | NateHerk | medium | Discarded 2026-04-07: same local-model policy decision as #42. |
| `mlops-2026-04-07-agents-summit-evals-patterns` | AI Agents Summit Seattle | MLOps | high | Discarded 2026-04-08 as duplicate of mlops-2026-04-03-beyond-swebench-evals (already adopted as infra-yolo-evals tick). |
| `nh-2026-04-07-ollama-claude-code-cost-reduction` | Ollama + Claude Code = 99% CHEAPER | NateHerk | medium | Discarded 2026-04-08 as REPEAT of nh-2026-04-03-ollama-claude-code-cost (discarded 2026-04-07). |
| `nh-2026-04-08-claude-internet-tool-integration` | Claude's New AI Just Changed the Internet Forever | NateHerk | medium | Discarded 2026-04-09: redundant with existing capabilities. |
| `nh-2026-04-09-openclaw-trading-agent` | I Gave OpenClaw $10,000 to Trade Stocks | NateHerk | high | Discarded 2026-04-12: live-capital agentic trading is completely out of scope for the YOLO dev loop. |
| `mlops-2026-04-10-gpu-starvation-distributed-training` | Fixing GPU Starvation in Large-Scale Distributed T | MLOps | high | Discarded 2026-04-12: YOLO loop does not do distributed GPU training. |
| `mlops-2026-04-10-production-subagents-llm-posttraining` | Production Sub-agents for LLM Post Training | MLOps | high | Discarded 2026-04-12: YOLO loop does not do LLM fine-tuning or post-training. |
| `mlops-2026-04-10-production-subagents-reward-modeling` | Production Sub-agents for LLM Post Training | MLOps | medium | Discarded 2026-04-12: RLHF/DPO reward signal generation is out of scope. |
| `do-2026-04-12-codex-zero-to-deployed` | CODEX FULL COURSE: From Zero to Deployed App (2026 | DavidOndrej | medium | Discarded 2026-04-12: OpenAI Codex end-to-end deployment is a competitor tool demo, not an adoptable pattern. |

---

## Deferred Experiments

| ID | Video | Channel | Effort | Reason | Reopen When |
|---|---|---|---|---|---|
| `mlops-2026-04-03-mcp-day2-integrations` | MCP Dev Summit [Day 2] ft AWS, Docker, & Datadog | MLOps | high | Deferred 2026-04-07: high effort, requires Docker + Datadog credentials, current YOLO does not deploy containers. | until harness-cli has a project that needs container deployment + observability |
| `mlops-2026-04-03-coding-agent-multiverse` | The Coding Agent Multiverse of Madness | MLOps | high | Deferred 2026-04-07: cross-agent benchmark is high cost (API keys for Codex, Gemini, Cursor, multi-day runs). |  |
| `nb-2026-04-07-polymarket-bot-disruption-audit` | A Polymarket Bot Made $438,000 In 30 Days. Your In | NateBJones | low | Deferred 2026-04-08: interesting but not currently actionable. | when considering the next major architectural change |
| `nb-2026-04-08-analyze-leaked-code-patterns` | I Analyzed 512,000 Lines of Leaked Code. It Shows  | NateBJones | medium | Deferred 2026-04-09: leaked source code is ethically/legally problematic as a corpus — do not adopt as-is. | Reopen as a new experiment when that reframe is prioritized; this entry stays deferred to preserve t |
| `mlops-2026-04-10-ship-agents-track2` | Ship Agents  A Virtual Conference Track 2 | MLOps | medium | Deferred 2026-04-12: potentially useful agent deployment patterns but too broad without someone watching the actual talks. | Reopen when specific patterns are identified |
| `nb-2026-04-11-google-quantization-inference` | Google's New Quantization is a Game Changer | NateBJones | medium | Deferred 2026-04-12: local-model adjacent. | until policy review |
| `nh-2026-04-11-seedance-claude-code-websites` | Seedance 2.0 + Claude Code Creates $10k Websites i | NateHerk | medium | Deferred 2026-04-12: creative but tangential. | Reopen as a Tick idea candidate if video-generation tools mature |

---

## Backlog (Awaiting Triage)

- **Integrate the Featured Plugin into Claude Code Workflow** [low] — `nh-2026-04-12-claude-code-plugin-10x`
  - Video: This One Plugin Just 10x'd Claude Code (NateHerk)
  - If we install and configure the highlighted plugin for Claude Code, then our agentic coding loop will complete tasks faster and with fewer manual corr
- **Build a Claude-Driven Video Edit Instruction Pipeline** [medium] — `st-2026-04-12-claude-video-editing`
  - Video: How I Taught Claude To Edit My YouTube Videos (ShawTalebi)
  - If we provide Claude with a transcript plus a structured editing style guide, then Claude can output a precise cut list or edit instructions because i
- **Encode a YOLO Loop Style Guide as a Reusable Claude System Prompt** [low] — `st-2026-04-12-claude-style-guide-prompt`
  - Video: How I Taught Claude To Edit My YouTube Videos (ShawTalebi)
  - If we distill our dev loop's coding conventions and output format rules into a compact system prompt style guide fed to Claude on every task, then out

---

## Cross-Channel Topic Clusters

Experiments from different channels addressing the same underlying topic.

### Local Models / Ollama Cost Reduction
*6 experiments from 4 channels (DavidOndrej, NateBJones, NateHerk, TwoMinutePapers)*

Verdicts: deferred: 1, discard: 2, discarded: 3

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `do-2026-03-27-private-local-agent` | DavidOndrej | Run YOLO builds via a 100% local AI agent stack | discard |
| `tmp-2026-04-01-quantized-local-inference` | TwoMinutePapers | Prototype a YOLO project using local quantized LLM inference | discard |
| `do-2026-04-03-gemma4-local-review` | DavidOndrej | Evaluate Gemma 4 as a local code review model to reduce API  | discarded |
| `nh-2026-04-03-ollama-claude-code-cost` | NateHerk | Use Ollama local models for Claude Code's routine sub-tasks  | discarded |
| `nh-2026-04-07-ollama-claude-code-cost-reduction` | NateHerk | Route Low-Stakes Claude Code Subtasks to Local Ollama Models | discarded |
| `nb-2026-04-11-google-quantization-inference` | NateBJones | Benchmark Google's new quantization scheme against existing  | deferred |

### Agent Orchestration / Multi-Agent
*4 experiments from 3 channels (DavidOndrej, MLOps, NateHerk)*

Verdicts: adopt: 1, adopted: 2, discard: 1

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `mlops-2026-04-01-agent-orchestration-cloud` | MLOps | Run parallel agent sessions for independent YOLO tasks | adopt |
| `nh-2026-03-31-paperclip-agent-org` | NateHerk | Use Paperclip's company-layer to orchestrate multi-agent Cla | discard |
| `do-2026-04-07-minimal-agent-pattern` | DavidOndrej | Build a Bare-Metal Minimal Agent Loop with No Framework Depe | adopted |
| `nh-2026-04-09-claude-managed-agents` | NateHerk | Benchmark Claude Managed Agents Against Manual Orchestration | adopted |

### Agent Evals / Quality Gates
*19 experiments from 5 channels (DavidOndrej, Fireship, MLOps, NateBJones, NateHerk)*

Verdicts: adopt: 7, adopted: 5, deferred: 4, discarded: 3

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `nb-2026-03-24-strict-linting-agents` | NateBJones | Apply strict linting to all agent-generated code | adopt |
| `mlops-2026-03-17-durable-execution-agents` | MLOps | Evaluate durable execution for long-running agent workflows | adopt |
| `mlops-2026-04-01-coding-agent-evals` | MLOps | Build a golden dataset of past bugs as an eval suite | adopt |
| `mlops-2026-04-01-continuous-model-eval` | MLOps | Build a golden-prompt eval suite to detect model regression  | adopt |
| `fs-2026-04-02-junie-cli-multi-model` | Fireship | Evaluate Junie CLI multi-model routing for harness-cli counc | adopt |
| `mlops-2026-04-03-mcp-day2-integrations` | MLOps | Evaluate Docker and Datadog MCP servers for agent-driven Dev | deferred |
| `mlops-2026-04-03-coding-agent-multiverse` | MLOps | Benchmark multiple coding agents on the same YOLO build spec | deferred |
| `mlops-2026-04-03-beyond-swebench-evals` | MLOps | Build custom evals that measure real YOLO build quality beyo | adopted |
| `mlops-2026-04-03-self-learning-agent-memory` | MLOps | Implement structured memory retrieval so the build agent lea | adopted |
| `do-2026-04-03-gemma4-local-review` | DavidOndrej | Evaluate Gemma 4 as a local code review model to reduce API  | discarded |
| `nb-2026-04-05-evaluative-agents-review-bottleneck` | NateBJones | Deploy evaluative agents alongside generative agents to elim | adopt |
| `nb-2026-04-05-independent-observability` | NateBJones | Build independent observability that never trusts agent self | adopt |
| `mlops-2026-04-07-agents-summit-evals-patterns` | MLOps | Implement a Lightweight Agent Eval Harness Drawn from Summit | discarded |
| `do-2026-04-08-claude-mythos-agentic-eval` | DavidOndrej | Benchmark Claude Mythos on Open-Ended Agentic Tasks in the Y | adopted |
| `nh-2026-04-09-claude-managed-agents` | NateHerk | Benchmark Claude Managed Agents Against Manual Orchestration | adopted |
| `mlops-2026-04-10-ship-agents-track2` | MLOps | Extract and benchmark agent deployment patterns from Ship Ag | deferred |
| `mlops-2026-04-10-production-subagents-llm-posttraining` | MLOps | Wire sub-agents into the LLM post-training pipeline for auto | discarded |
| `nh-2026-04-10-claude-stop-using-best-model` | NateHerk | Benchmark Claude Haiku or Sonnet against Opus on YOLO Loop t | adopted |
| `nb-2026-04-11-google-quantization-inference` | NateBJones | Benchmark Google's new quantization scheme against existing  | deferred |

### Memory / Context / Learning
*8 experiments from 3 channels (MLOps, NateBJones, NateHerk)*

Verdicts: adopt: 6, adopted: 1, discard: 1

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `nb-2026-03-24-context-compression` | NateBJones | Use incremental summarization for context compression in lon | adopt |
| `mlops-2026-03-17-durable-execution-agents` | MLOps | Evaluate durable execution for long-running agent workflows | adopt |
| `nb-2026-04-02-session-isolation-per-task` | NateBJones | Use task-isolated fresh Claude sessions to prevent context b | discard |
| `nh-2026-04-02-compact-at-milestones` | NateHerk | Apply /compact at defined YOLO session milestones to preserv | adopt |
| `mlops-2026-04-03-self-learning-agent-memory` | MLOps | Implement structured memory retrieval so the build agent lea | adopted |
| `mlops-2026-04-03-self-learning-feedback-loop` | MLOps | Add automatic post-build reflection that writes back to agen | adopt |
| `nb-2026-04-04-compounding-agent-memory` | NateBJones | Implement compounding agent memory that improves with each b | adopt |
| `nh-2026-04-05-karpathy-llm-wiki-hot-cache` | NateHerk | Implement Karpathy hot-cache pattern for instant agent conte | adopt |

### Planning / Pre-Build
*10 experiments from 4 channels (MLOps, NateBJones, NateHerk, [un]prompted)*

Verdicts: adopt: 6, adopted: 2, deferred: 1, discard: 1

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `mlops-2026-03-27-specialized-agent-team` | MLOps | Use specialized agent roles instead of one monolithic agent | discard |
| `mlops-2026-03-25-qrspi-vertical-planning` | MLOps | Adopt vertical planning with structure outlines before codin | adopt |
| `nb-2026-03-31-agent-readable-skills` | NateBJones | Restructure program.md as agent-readable skill files | adopt |
| `up-2026-03-31-personal-ai-infrastructure` | [un]prompted | Build a Council skill for multi-perspective task review | adopt |
| `nh-2026-03-30-codex-plan-claude-execute` | NateHerk | Adopt Codex-as-planner + Claude Code-as-executor 3-phase bui | adopt |
| `mlops-2026-04-02-mcp-spec-roadmap` | MLOps | Track the Anthropic MCP technical roadmap and adopt spec upd | adopt |
| `mlops-2026-03-31-agent-debug-logging` | MLOps | Add structured debug logging at agent decision points to spe | adopt |
| `mlops-2026-04-03-coding-agent-multiverse` | MLOps | Benchmark multiple coding agents on the same YOLO build spec | deferred |
| `mlops-2026-04-03-self-learning-agent-memory` | MLOps | Implement structured memory retrieval so the build agent lea | adopted |
| `nh-2026-04-07-claude-code-planning-mode` | NateHerk | Use Claude Code's New Planning Mode as a Spec-Decomposition  | adopted |

### Model Selection / Upgrades
*12 experiments from 5 channels (DavidOndrej, Fireship, MLOps, NateBJones, NateHerk)*

Verdicts: adopt: 4, adopted: 4, deferred: 1, discarded: 3

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `nb-2026-04-01-model-upgrade-stack-audit` | NateBJones | Run a 4-layer stack audit before every major Claude model up | adopt |
| `mlops-2026-04-01-continuous-model-eval` | MLOps | Build a golden-prompt eval suite to detect model regression  | adopt |
| `fs-2026-04-02-junie-cli-multi-model` | Fireship | Evaluate Junie CLI multi-model routing for harness-cli counc | adopt |
| `nb-2026-04-03-agent-architecture-12-pieces` | NateBJones | Audit PAI agent stack against the 12 critical agent architec | adopt |
| `do-2026-04-03-gemma4-local-review` | DavidOndrej | Evaluate Gemma 4 as a local code review model to reduce API  | discarded |
| `nh-2026-04-03-ollama-claude-code-cost` | NateHerk | Use Ollama local models for Claude Code's routine sub-tasks  | discarded |
| `nb-2026-04-07-ephemeral-layers-stack-audit` | NateBJones | Classify Each YOLO Loop Dependency by Shelf-Life and Replace | adopted |
| `nh-2026-04-07-ollama-claude-code-cost-reduction` | NateHerk | Route Low-Stakes Claude Code Subtasks to Local Ollama Models | discarded |
| `do-2026-04-08-claude-mythos-agentic-eval` | DavidOndrej | Benchmark Claude Mythos on Open-Ended Agentic Tasks in the Y | adopted |
| `nb-2026-04-10-five-safe-places-ai` | NateBJones | Audit current build position against the 5 safe AI niches fr | adopted |
| `nh-2026-04-10-claude-stop-using-best-model` | NateHerk | Benchmark Claude Haiku or Sonnet against Opus on YOLO Loop t | adopted |
| `nb-2026-04-11-google-quantization-inference` | NateBJones | Benchmark Google's new quantization scheme against existing  | deferred |

### MCP / Tool Integration
*3 experiments from 2 channels (MLOps, NateBJones)*

Verdicts: adopt: 2, deferred: 1

| ID | Channel | Title | Verdict |
|---|---|---|---|
| `nb-2026-03-28-mcp-tool-integration` | NateBJones | Use MCP to connect build agents to professional tools | adopt |
| `mlops-2026-04-02-mcp-spec-roadmap` | MLOps | Track the Anthropic MCP technical roadmap and adopt spec upd | adopt |
| `mlops-2026-04-03-mcp-day2-integrations` | MLOps | Evaluate Docker and Datadog MCP servers for agent-driven Dev | deferred |

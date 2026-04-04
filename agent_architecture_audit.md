# Agent Architecture Audit: YOLO/PAI Autonomous Build System

**Date:** 2026-04-02
**Auditor:** Claude Opus 4.6 (automated)
**System under audit:** YOLO Projects autonomous build pipeline + PAI infrastructure
**Framework:** 12 critical agent architecture components (standard best practices)

---

## Summary

| # | Component | Rating | Key Evidence |
|---|-----------|--------|--------------|
| 1 | Task Decomposition / Planning | STRONG | 3-phase pipeline, skill routing, ISC criteria system |
| 2 | Memory (short + long term) | STRONG | session_state.json + learnings.md + MEMORY.md index |
| 3 | Tool Use / Function Calling | STRONG | Gemini MCP, yt-dlp, Playwright, node, Python scripts |
| 4 | Self-Reflection / Self-Critique | STRONG | Post-build reflection, learnings.md, Algorithm LEARN phase |
| 5 | Error Recovery / Retry Logic | ADEQUATE | Dark Factory 3-retry loop, but no circuit breaker or escalation |
| 6 | Guardrails / Safety Constraints | ADEQUATE | Bedrock rules + design system, but no token/cost hard limits |
| 7 | Human-in-the-Loop Escalation | WEAK | No explicit escalation path when autonomous builds fail |
| 8 | Observability / Logging | ADEQUATE | build_log.py exists but build-logs/ is empty; session_state works |
| 9 | Cost Management / Budget Controls | WEAK | No token tracking, no per-run cost caps, no spend alerts |
| 10 | Evaluation / Quality Metrics | STRONG | test_project.py + eval_bugs.py + 6-angle council + golden prompts |
| 11 | Context Management / Compression | ADEQUATE | session_state.json recovery, but no explicit context window management in cron |
| 12 | Multi-Agent Coordination | STRONG | Gemini-as-reviewer, Phase 4 pipeline, tick-tock scheduling, PAI Agent system |

**Overall: 5 STRONG, 5 ADEQUATE, 2 WEAK, 0 MISSING**

---

## Detailed Analysis

### 1. Task Decomposition / Planning — STRONG

**What exists:**
- `skills/00-bootstrap.md` routes sessions to the correct skill chain (Tick/Tock/Phase4/Refine)
- `skills/10-tick.md` decomposes a build into 6 explicit phases: Ideate, Build, Test, Review, Ship, Commit
- PAI Algorithm v3.7.0 has a 7-phase decomposition (Observe, Think, Plan, Build, Execute, Verify, Learn) with ISC criteria that enforce atomic task breakdown
- Gemini brainstorm step before building forces idea validation
- `program.md` defines a 13-step loop with clear sequencing

**Why STRONG:** The system has multiple layers of decomposition — strategic (tick-tock cadence), tactical (skill routing), and operational (phase steps within each skill). The ISC splitting test in PAI Algorithm is particularly sophisticated, enforcing that no criterion can hide compound requirements.

---

### 2. Memory (Short-Term + Long-Term) — STRONG

**What exists:**
- **Short-term:** `session_state.json` captures tick-tock state, Phase 4 stats, portfolio counts, and resume instructions. Read at session start, written at session end.
- **Long-term:** `learnings.md` (3,069 lines) accumulates KEEP/IMPROVE/DISCARD/INSIGHT entries across all builds. `yolo_log.json` is append-only build history.
- **Structured long-term:** `experiments.json` (44 experiments) with full lifecycle tracking.
- **PAI-level:** `~/.claude/projects/*/memory/MEMORY.md` index pointing to topic-specific memory files (user profile, feedback, project state).
- **Algorithm-level:** PRD files in `MEMORY/WORK/{slug}/` serve as per-task memory with YAML frontmatter and criteria checkboxes.

**Why STRONG:** Memory spans multiple timescales (within-session, across-sessions, permanent knowledge) with both unstructured (learnings.md) and structured (JSON) stores. The resume_instructions field in session_state.json is a clever "compressed context" pattern.

---

### 3. Tool Use / Function Calling — STRONG

**What exists:**
- **Gemini MCP tools:** `gemini-analyze-code` (code review), `gemini-youtube-summary` (video processing), `gemini-query` (brainstorming)
- **CLI tools:** `yt-dlp` (YouTube fetching), `node -c` (syntax checking), Playwright (browser testing)
- **Python scripts as tools:** `test_project.py`, `eval_bugs.py`, `build_log.py`, `phase4_fetch.py`, `update_dashboard.py`, `update_session_state.py`
- **PAI skill system:** Skills invokable via `Skill` tool with defined input/output contracts

**Why STRONG:** The tool ecosystem covers the full build lifecycle from ideation (Gemini brainstorm) through testing (Playwright headless browser) to deployment (git push). Tools are composable — the skill system chains them into pipelines.

---

### 4. Self-Reflection / Self-Critique — STRONG

**What exists:**
- **Per-build reflection:** `learnings.md` entries with KEEP/IMPROVE/DISCARD/INSIGHT/TEST CAUGHT categories
- **Every-5-builds review:** `program.md` mandates reviewing the last 5 builds for recurring problems
- **PAI Algorithm LEARN phase:** 4 reflection questions ("What should I have done differently?", "What would a smarter algorithm have done?", etc.) with mandatory JSONL logging to `algorithm-reflections.jsonl`
- **Model upgrade audit:** `model-upgrade-audit.md` is a 5-layer self-audit checklist for when the underlying model changes
- **Experiment lifecycle:** `experiments.json` verdict field (adopt/discard/iterate) forces explicit evaluation of whether experiments worked

**Why STRONG:** Reflection is baked in at every level — per-build, per-cycle, per-model-upgrade. The JSONL reflections log creates a queryable history of what the system learned over time. The experiment tracker with explicit verdicts prevents "trying things but never evaluating them."

---

### 5. Error Recovery / Retry Logic — ADEQUATE

**What exists:**
- **Dark Factory retry loop:** Build -> test -> fix -> retest, max 3 cycles. Defined in `program.md` and referenced in every skill.
- **Phase 4 fetch:** `subprocess.TimeoutExpired` and `FileNotFoundError` caught in `phase4_fetch.py`
- **Test runner:** Playwright tests have 30-second timeout, browser error collection, graceful HTTP server shutdown
- **15-minute stuck rule:** "If you're stuck on one approach for more than 15 minutes, try a completely different approach."

**What's missing:**
- No circuit breaker pattern — if 3 consecutive builds fail, the system keeps trying the same approach
- No exponential backoff on external API failures (Gemini, yt-dlp)
- No "quarantine" for projects that fail repeatedly
- No alerting when retry budget is exhausted

**Fix:** Add a `consecutive_failures` counter to `session_state.json`. If it hits 3, switch to a "safe mode" that builds from a simpler template or refines existing projects instead of attempting novel builds. Add exponential backoff to `phase4_fetch.py` for network failures.

---

### 6. Guardrails / Safety Constraints — ADEQUATE

**What exists:**
- **Bedrock rules:** 4 non-negotiable rules in `program.md` (test everything, Gemini audits all, learn from every build, honest status reporting)
- **Design system enforcement:** `design.md` read before every build
- **Code review gate:** Gemini must review actual code, not summaries, before shipping
- **PAI behavioral rules:** Referenced via `PAI/AISTEERINGRULES.md`
- **Scope constraint:** "Keep the scope small", single-file HTML, zero dependencies

**What's missing:**
- No hard limit on file size (a runaway build could generate massive files)
- No content safety filter on generated projects (the system builds whatever Gemini brainstorm suggests)
- No rate limit on git pushes (a malfunctioning cron could spam commits)
- No resource consumption limits (CPU, memory, disk) for the build process
- Eval_bugs.py catches 26 patterns but has no mechanism to prevent the patterns from being generated in the first place (it's detection, not prevention)

**Fix:** Add a pre-commit hook that rejects files over 500KB. Add a `max_commits_per_hour: 3` guard to the cron prompt. Add a project name blocklist to prevent rebuilding known-problematic names.

---

### 7. Human-in-the-Loop Escalation — WEAK → RESOLVED

**What exists:**
- The tick-tock model allows the human to intervene ("build" for tick, "deck" for tock)
- `session_state.json` resume_instructions let the human see what happened
- PAI Algorithm has an `AskUserQuestion` tool for interactive sessions
- The model-upgrade audit explicitly requires human judgment for layer decisions

**What's missing:**
- **No automated notification on failure.** If the hourly cron builds a broken project, the human only discovers it by manually checking.
- **No "needs human review" queue.** When the system is uncertain (e.g., council scores are borderline, Gemini critique is ambiguous), there's no mechanism to flag items for human review.
- **No approval gate for risky operations.** The system auto-pushes to GitHub without any human approval step for builds that score below a threshold.
- **No escalation from Phase 4.** When experiments are marked "high effort" or involve architectural changes, there's no alert to the human.

**Fix applied (2026-04-02):** Added halt-file escalation to both `program.md` (Dark Factory section) and `skills/10-tick.md` (Test phase). Rule: if `test_project.py` fails 3 times in a row on the same project, the agent writes a `.harness_halt` file in the project directory containing the error and timestamp, then STOPS. No further builds are attempted until a human removes the halt file. This is a simple, file-based circuit breaker that requires zero infrastructure — the human sees the halt file on next check and can investigate.

---

### 8. Observability / Logging — ADEQUATE

**What exists:**
- **Build logging:** `build_log.py` provides structured JSON event logging per project with timestamps, event types, and data payloads
- **Session state:** `session_state.json` tracks portfolio stats, phase 4 metrics, tick-tock history
- **Phase 4 run log:** `phase4_run.json` records last run stats (channels scanned, experiments found, status)
- **YOLO log:** `yolo_log.json` is the append-only project registry
- **PAI-level:** PRD files with phase tracking, progress counters, and verification evidence
- **Algorithm reflections:** JSONL log of per-session learning

**What's missing:**
- **build-logs/ directory is empty** — `BuildLog` class exists but is never called in the actual skill chain. The infrastructure is built but not wired in.
- **No centralized dashboard for cron health.** The HTML dashboard shows projects, not system health.
- **No latency tracking.** How long each phase takes is not recorded, so you can't identify bottlenecks.
- **No Gemini API call logging.** If Gemini is slow or returning poor reviews, there's no record.

**Fix:** Wire `build_log.py` into `skills/10-tick.md` by adding explicit `BuildLog` calls at each phase transition. This is low-hanging fruit — the code exists, it just needs to be called. Add a `timing` field to session_state.json that records phase durations. Create a `system_health.json` that tracks: cron success rate, average build time, Gemini response times.

---

### 9. Cost Management / Budget Controls — WEAK

**What exists:**
- **Implicit scope control:** "Keep the scope small", single-file HTML, zero dependencies
- **Max retry cap:** Dark Factory loop caps at 3 retries
- **PAI Algorithm effort tiers:** Time budgets per tier (Standard < 2min, Extended < 8min, etc.)
- **Cron frequency:** Hourly tick, daily Phase 4 — implicit cost ceiling via scheduling

**What's missing:**
- **No token/cost tracking.** The system doesn't record how many tokens each build consumes (Claude input/output, Gemini calls).
- **No per-run budget cap.** A complex build could consume unlimited tokens with no stopping mechanism.
- **No cost alerting.** No way to know if this month's spend is abnormal.
- **No model cost awareness.** The system doesn't distinguish between expensive (Opus) and cheap (Haiku) model calls.
- **No Gemini API quota tracking.** If the Gemini free tier runs out, the system fails without graceful degradation.

**Fix:** Add a `cost_tracking` section to `session_state.json`:
```json
{
  "cost_tracking": {
    "today_builds": 3,
    "today_gemini_calls": 12,
    "max_daily_builds": 10,
    "max_daily_gemini_calls": 50
  }
}
```
Check these counters at session start. If over budget, skip to a "zero-cost" activity (reviewing learnings, reorganizing experiments). For deeper tracking, log API call counts in `build_log.py` events.

---

### 10. Evaluation / Quality Metrics — STRONG

**What exists:**
- **Automated testing:** `test_project.py` with 7 checks (syntax, ID consistency, event listeners, brace balance, start screen, browser load, console errors)
- **Bug pattern scanning:** `eval_bugs.py` with 26+ regex patterns mined from real learnings
- **6-angle council review:** Bugs, security, UI, guide-compliance, usefulness, coolness — each scored
- **Golden-prompt eval:** 8 regression prompts for testing model behavior
- **Model upgrade audit:** 5-layer checklist comparing eval results before/after upgrade
- **Experiment success metrics:** Each experiment card has an explicit `success_metric` field

**Why STRONG:** The evaluation stack is multi-layered: static analysis (syntax, patterns), dynamic testing (Playwright browser), external review (Gemini council), and meta-evaluation (golden prompts, model upgrade audit). The eval_bugs.json pattern suite is a living document mined from real failure modes — this is genuinely unusual for an autonomous system and represents real learning.

---

### 11. Context Management / Compression — ADEQUATE

**What exists:**
- **Session state compression:** `resume_instructions` in `session_state.json` is a compressed natural-language summary for context recovery
- **Skill routing:** `00-bootstrap.md` reads only the state needed, then routes to the relevant skill — avoiding loading everything at once
- **PAI Algorithm compaction:** At phase boundaries (Extended+ effort), accumulated context is self-summarized. "Preserve: ISC status, key results, next actions. Discard: verbose tool output, intermediate reasoning."
- **Context recovery protocol:** If lost, read the most recent PRD for full state recovery

**What's missing:**
- **Cron sessions have no explicit context budget.** The hourly cron loads `program.md` (327 lines), `learnings.md` (3,069 lines), `design.md`, `session_state.json`, and potentially `yolo_log.json` — all at session start. No evidence of selective loading.
- **learnings.md is growing unbounded.** At 3,069 lines, it may already exceed useful context. No summarization or archival strategy.
- **No context priority ranking.** When approaching context limits, there's no defined order of what to drop first.

**Fix:** Add a `learnings_archive.md` and cap `learnings.md` at the most recent 500 lines. Older entries get moved to the archive (still searchable, not loaded by default). In `skills/10-tick.md`, change "Read learnings.md (first 50 lines)" to explicitly use the Read tool with `limit: 50` so the full file is never loaded. Add a `context_budget` section to skill files defining what to load and in what order.

---

### 12. Multi-Agent Coordination — STRONG

**What exists:**
- **Gemini as external reviewer:** Every build goes through Gemini for code review — a genuine multi-model architecture
- **Phase 4 YouTube pipeline:** A separate cron agent that feeds the experiment backlog, decoupled from the build agent
- **Tick-Tock scheduling:** Two agent "modes" (builder vs. flagship developer) with state-machine coordination via `session_state.json`
- **PAI Agent system:** Full agent composition framework with traits, voices, specializations, and team creation
- **Council pattern:** 6-angle review simulates multiple expert perspectives
- **Skill chaining:** Skills call sub-skills (Tick calls Review, Refine calls Review) — a basic agent delegation pattern
- **harness-cli:** Separate repo packaging the methodology as a reusable CLI

**Why STRONG:** The system uses multi-agent patterns at multiple levels: model-level (Claude + Gemini), process-level (build agent + Phase 4 agent), and conceptual-level (council of virtual reviewers). The PAI framework provides formalized agent composition and delegation primitives.

---

## Priority Fixes (Ranked by Impact)

### P0 — Wire build_log.py into the skill chain
**Impact:** Fixes observability gap. **Effort:** Low (< 1 session).
The `BuildLog` class exists and is well-designed. Add import and event calls to `skills/10-tick.md` methodology. Every phase transition should log an event. This gives you timing data, failure tracking, and an audit trail for free.

### P1 — Add failure notification and human escalation
**Impact:** Fixes the WEAK human-in-the-loop rating. **Effort:** Low-Medium.
Add `needs_review` array to `session_state.json`. When council scores average below 7, or Dark Factory exhausts retries, append an entry. Use PAI's notification curl to alert immediately on critical failures. Display the queue at session start.

### P2 — Add basic cost tracking counters
**Impact:** Fixes the WEAK cost management rating. **Effort:** Low.
Add `daily_build_count` and `daily_gemini_calls` to `session_state.json`. Check at session start. If over threshold, switch to low-cost activities. This prevents runaway spend without complex token counting.

### P3 — Cap and archive learnings.md
**Impact:** Improves context management. **Effort:** Low.
Create `learnings_archive.md`. Move entries older than 30 days. Keep `learnings.md` under 500 lines. The "read first 50 lines" instruction in tick.md already acknowledges this file is too large — archiving makes the implicit explicit.

### P4 — Add circuit breaker for consecutive failures
**Impact:** Improves error recovery. **Effort:** Low.
Add `consecutive_build_failures` to `session_state.json`. If >= 3, next session auto-routes to refine (skill 40) instead of new build (skill 10). Resets on success.

---

## Conclusion

The YOLO/PAI system is architecturally mature for an autonomous build pipeline. It covers 12/12 standard agent architecture components with no outright MISSING pieces. The strongest areas are evaluation (multi-layered testing), memory (multi-timescale stores), and self-reflection (JSONL learning logs). The two WEAK areas — human escalation and cost management — are both fixable with lightweight additions to `session_state.json` and the existing notification infrastructure. The most impactful single fix is wiring the existing `BuildLog` class into the skill chain, which would immediately close the observability gap.

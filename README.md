# YOLO Projects

A portfolio of single-file browser tools and three flagships, kept by a Claude Code session on John's MS-S1. Nothing ships without his say.

## How It Works

Since 2026-10-19 (John's ruling: "We're not doing ticks and tocks any longer") there is no hourly builder. The
work is two things:

1. **Keep up with the flagships**: Markdown Deck, Naval Scribe and PDF to CSV. PDF to CSV is developed by hand in
   its own repo and published here as a built file.
2. **Review new cards**: every morning at 05:50 JST, `scripts/daily_cards.sh` turns new rows from John's video
   watch log into cards in `experiments.json`, opens a pull request and merges it when secret-scan and validate
   pass. The session judges each card against all of John's projects, logs one line per card in
   `.harness/card_reviews.md`, and raises only the useful ones with him. Nothing is built until he says go.

Changes reach `main` through pull requests. The older tick/tock build pipeline (plan, build, test, 7-angle
council, reflect) and its workflow files are kept for history; the cron stays off.

## Portfolio

Counts change every hour, so they are not copied here: the live numbers (total built, active, culled) are in
[`_hot.md`](_hot.md), and the dashboard shows the active tools: https://anguijm.github.io/yolo-projects/dashboard.html

### Categories
- **Dev Tools** — jwt-decode, json-explorer, regex-playground, ssl-check, dns-lookup, diff-painter, shader-forge, yaml-fmt, etc.
- **Creative Tools** — beat-haus, note-lab, sonic-sight, palette-pull, sprite-forge, haiku-gen, etc.
- **Productivity** — markdown-deck, naval-scribe, pdf-to-csv, prompt-built-tools, kanban-board, pomodoro-flow, flash-cards, etc.
- **Games** — picross, sudoku, neon-tetra, dungeon-descent, regex-quest, etc.
- **Generators & Utilities** — entropy-forge, qr-forge, prose-xray, curl-converter, etc.
- **Education** — neural-playground, circuit-sim, automata-lab, etc.

## Flagships

### Markdown Deck
Markdown-to-slide-deck editor with live preview, fullscreen presentation, PPTX export, 6 themes, templates, speaker notes, presenter view, slide search, find/replace, kiosk mode, standalone HTML export, Pretext canvas measurement, and clipboard image paste. Single HTML file, zero dependencies.

### Naval Scribe
Naval correspondence formatter per SECNAV M-5216.5. 7 document types (standard letter, memo, endorsement, business letter, point paper, action memo, MOA with multiple signers). Classification markings, SSIC autocomplete, signature block builder, letterhead presets, saved drafts library, print-to-PDF. Exports .docx via hand-rolled OOXML ZIP.

### PDF to CSV
Offline converter from a folder of PDF records (scanned with an OCR text layer, or born digital) to one CSV: one row per record, one column per named field, plus a list of the files it could not read and why. Reads boxed forms by their drawn lines, follows long text across pages and "(cont.)" boxes, ignores running headers and footers, scopes repeated labels by block ("Approved By > Date"), can compare several records to tell labels from values, splits packets of several forms by their page counters (telling the main form type from page 1), reads tables, and says in problems.csv each place it had to guess. One HTML file with pdf.js embedded; the page cannot make network requests. Current version v0.8.11 (2026-10-20). [Open it](https://anguijm.github.io/yolo-projects/pdf-to-csv/index.html) · [Usage guide](pdf-to-csv/GUIDE.md) · [Prompts for studying packets](pdf-to-csv/GENAI-PROMPTS.md) · The prompt series for GenAI.mil moved to [prompt-built-tools](prompt-built-tools/README.md).

### Prompt-built tools
Planning tools for a ship repair yard, built inside GenAI.mil from prompt series: a chat model writes one self-contained offline HTML file per tool. A JCN analog estimator (similar past jobs with reasons and a match strength, the estimate and its CSV, a weight test that fits the matching weights on the yard's own history, batch mode, planned jobs and material), a Resource Map (shop load by week with drill-down) and its leveler (drag jobs and projects, the contractor line, automatic level and farm-out), a dictionary page (harvests the shorthand in the JCN free text with counts and examples, a planner decides each term, and it writes the estimator's dictionary.json), a workbook converter page (Excel workbooks in, one CSV per sheet out), a direct Excel reader and a shared look. Made-up data only. [Build guide](prompt-built-tools/GENAI-BUILD-GUIDE.md) · [Folder](prompt-built-tools/README.md) · [Process flow](https://anguijm.github.io/yolo-projects/prompt-built-tools/GENAI-PROCESS-FLOW.html) · [Loops and graphs](https://anguijm.github.io/yolo-projects/prompt-built-tools/GENAI-LOOPS-AND-GRAPHS.html)

## Quality Pipeline

### Phase 1: Duplicate Resolution
Council reviews competing projects head-to-head. Higher score survives.

### Phase 2: Usefulness Refinement
Full 7-angle council on every survivor. Score 5+ on usefulness or get culled.

### Phase 3: Usefulness Cull
Final pass — anything still not genuinely useful gets cut.

### Phase 4: YouTube Research
Off since 2026-10-17; the daily cards from John's watch log replaced it. When it ran, a daily cron (~07:00 JST) auto-discovered new videos from 22 monitored YouTube channels via RSS (the feeds are read on the MS-S1 at home twice a day by `scripts/snapshot_feeds.sh` and pushed to the branch `feeds/snapshot`; the runner fetches live only when that snapshot is missing or over 8 hours old, because YouTube refuses GitHub's runners), pulls auto-captions through supadata.ai, generates experiment proposals (since 2026-10-15 each card carries `relevance_to_yolo_loop` and `relevance_to_operator_projects`, both scored high, medium or none; a card is in scope when either is high), runs them through council cull, and promotes adopted items into the tick queue. Live lifetime counts: see `phase4_run.json`. Per-experiment narrative: `experiments.json` is the source of truth; `experiments/FINAL_REPORT.md` has the most recent comprehensive write-up.

### Security Scanning
22-rule regex scanner (`security_scan.py`) runs on every build. Full portfolio triaged: 0 real vulnerabilities. CSP meta tag in design.md boilerplate.

### Architecture Audit
12-piece agent architecture audit: 5 STRONG, 5 ADEQUATE, 0 WEAK (2 resolved). Halt mechanism and cost cap implemented.

## Adopted Experiments (live count in `phase4_run.json`; per-experiment outcomes in `experiments.json`)

Key process improvements from Phase 4 research:

- **Approval-gated builds** — cron proposes, human approves, then it builds
- **7-angle council review** — bugs, security, ui, guide, usefulness, cool, lessons (lessons has veto power)
- **Council enforcement rules (live in `.harness/scripts/council.py`)** — auto-downgrade for: parse-failure retry, LESSONS precondition_evidence, goalpost-move (keyword-overlap > 0.35 vs prior reasons), BUGS hallucination (claimed-undefined symbols that grep finds defined). See `.harness/scripts/council_rules.md` for the canonical reference.
- **Vertical planning** — structure outline before code eliminates rework
- **Boring-but-high-ROI filter** — "would a business pay for this?" idea selection
- **3-phase pipeline** — Plan (Gemini critique) → Build → Review (council)
- **Auto post-build reflection** — structured KEEP/IMPROVE/INSIGHT after every build
- **Golden bug eval** — 26 patterns from learnings.md, run on every build
- **Security scanning** — 22 rules for secrets, XSS, injection, CSP
- **Model upgrade audit** — 5-layer checklist + MCP spec review
- **Golden-prompt eval** — 8 regression prompts for model quality verification
- **Structured build logging** — JSON audit trail per project
- **Multi-model council routing** — per-angle model overrides in harness-cli
- **Pretext text measurement** — canvas-based layout without DOM reflows

## Automation

| Trigger | Schedule | What |
|---------|----------|------|
| Daily cards | Daily 05:50 JST (MS-S1 cron) | `scripts/daily_cards.sh`: new cards from the watch log, opened and merged as a pull request on secret-scan and validate |
| Tick-Tock Builder | Off since 2026-06-28 | Retired 2026-10-19; workflow kept for history |
| Phase 4 Research | Off since 2026-10-17 (no API key; the daily cards replaced it) | YouTube RSS scan across 22 channels (feed snapshot from the MS-S1, live fallback), experiment extraction, always commits run report, fails red when zero feeds were read |

## Monitored YouTube Channels (22; authoritative roster in `fetch_youtube_rss.py:CHANNELS`; read by Phase 4, off since 2026-10-17)
@NateBJones, @MLOps, @DavidOndrej, [un]prompted, @NateHerk, @AIJasonZ, @echohive, @ShawTalebi, @Mark_Kashef, @aiDotEngineer, @mattpocockuk, @indydevdan, @ColeMedin, @AILABS-393, @LatentSpacePod, @anthropic-ai, @LangChain, @donatocapitella, @AZisk, @AliElZoheiry, @PhilippLackner, @PixelArtistry_

Added 2026-10-15: the seven from @mattpocockuk to @LangChain, scouted from the approval evidence (which channels' cards the triage already approves; record in the brain vault, `10_staging/yolo-channels/synthesis.md`); then the five from @donatocapitella on, which cover the operator's other projects (local inference on Strix Halo, Unreal Engine 5, Android, text-to-3D printing) and only make sense with the widened card prompt.

Dropped 2026-10-15: @swyx, @GregKamradt, @AndrejKarpathy (zero cards across 171 runs; their existing cards and wiki pages stay).

## Key Files

| File | Purpose |
|------|---------|
| `program.md` | Full builder methodology |
| `design.md` | Visual design system (dark industrial aesthetic) |
| `.harness/learnings.md` | Accumulated build knowledge (3000+ lines) |
| `.harness/yolo_log.json` | Append-only log of all builds |
| `experiments.json` | Phase 4 experiment tracker (live count) |
| `experiments/FINAL_REPORT.md` | Most recent comprehensive Phase 4 write-up |
| `STACK_AUDIT.md` (in `experiments/adopt-stack-audit/`) | Dated dependency shelf-life audit with grep-by-content citations |
| `.harness/scripts/council_rules.md` | Canonical reference for council mechanics + 4 enforcement rules |
| `.harness/session_state.json` | Tick-tock state, approval queues, phase 4 queue |
| `dashboard.html` | Portfolio dashboard (generated from log) |
| `test_project.py` | Automated test suite (7 checks) |
| `eval_bugs.py` | 26-pattern bug scanner |
| `security_scan.py` | 22-rule security scanner |
| `fetch_youtube_rss.py` | Phase 4 RSS feed fetcher (11 channels) |
| `build_log.py` | Structured JSON audit trail per build |
| `.harness/model-upgrade-audit.md` | 5-layer checklist for model swaps |
| `model-eval/` | Golden-prompt regression suite (8 prompts) |
| `security_triage.md` | Full portfolio security triage report |
| `agent_architecture_audit.md` | 12-piece architecture audit |
| `phase4_run.json` | Daily Phase 4 run report (always committed) |
| `update_dashboard.py` | Dashboard regenerator |
| `update_session_state.py` | Session state persistence |

## Related Repos

- **[harness-cli](https://github.com/Anguijm/harness-cli)** — AI development methodology as a standalone CLI. Council, planning, memory, handoff to any coding tool.
- **[ai-dev-team-template](https://github.com/Anguijm/ai-dev-team-template)** — ARCHIVED. Governance concepts ported to harness-cli.

## Stack

- **Builder**: Claude Code (remote triggers); current model Claude Opus 4.7 with Sonnet/Haiku fallbacks per workflow definition
- **Council**: Gemini 2.5 Flash (primary), Claude Haiku 4.5 (fallback) — 7-angle reviews invoked from `.harness/scripts/council.py`
- **Testing**: Python + Node.js + Playwright
- **Frontend**: Single-file HTML, zero external dependencies
- **Design**: Dark industrial aesthetic, monospace, ghost buttons

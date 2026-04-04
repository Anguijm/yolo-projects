# YOLO Projects

AI-assisted build system with human-gated approval. Claude proposes project ideas hourly, a 6-angle Gemini council reviews everything, and nothing ships without human sign-off.

## How It Works

An hourly cron trigger fires a Claude Code remote agent that alternates between two modes:

### Tick (New Projects — Approval-Gated)
1. **If approved ideas exist** — builds the next one: Plan (Gemini critique) → Build → Test → 6-angle Council → Reflect
2. **If queue is empty** — brainstorms 1 idea, adds to pending queue, does NOT build. Human approves or denies at next check-in.

### Tock (Flagship Features)
Alternates between two flagship projects, implementing approved features or brainstorming 2 new proposals for approval.

### Build Pipeline (when approved)
1. **Plan** — boring-but-high-ROI filter, vertical outline, Gemini critique
2. **Build** — code from validated plan
3. **Test** — `test_project.py` (7 checks) + `eval_bugs.py` (26 patterns) + `security_scan.py` (22 rules)
4. **Review** — 6-angle Gemini council (bugs, security, UI, guide, usefulness, cool)
5. **Reflect** — structured KEEP/IMPROVE/INSIGHT/COUNCIL appended to learnings.md

### Safety
- `.harness_halt` circuit breaker — 3 test failures = full stop until human intervenes
- 15-call Gemini cost cap per session
- No visual-only simulations (enforced in prompt)

## Portfolio

| Metric | Count |
|--------|-------|
| Total built | 210+ |
| Active (passed council) | 87+ |
| Culled (duplicates, visual toys, low utility) | 121+ |

### Categories
- **Dev Tools** — jwt-decode, json-explorer, regex-playground, ssl-check, dns-lookup, diff-painter, shader-forge, yaml-fmt, etc.
- **Creative Tools** — beat-haus, note-lab, sonic-sight, palette-pull, sprite-forge, haiku-gen, etc.
- **Productivity** — markdown-deck, naval-scribe, kanban-board, pomodoro-flow, flash-cards, etc.
- **Games** — picross, sudoku, neon-tetra, dungeon-descent, regex-quest, etc.
- **Generators & Utilities** — entropy-forge, qr-forge, prose-xray, curl-converter, etc.
- **Education** — neural-playground, circuit-sim, automata-lab, etc.

## Flagships

### Markdown Deck
Markdown-to-slide-deck editor with live preview, fullscreen presentation, PPTX export, 6 themes, templates, speaker notes, presenter view, slide search, find/replace, kiosk mode, standalone HTML export, Pretext canvas measurement, and clipboard image paste. Single HTML file, zero dependencies.

### Naval Scribe
Naval correspondence formatter per SECNAV M-5216.5. 7 document types (standard letter, memo, endorsement, business letter, point paper, action memo, MOA with multiple signers). Classification markings, SSIC autocomplete, signature block builder, letterhead presets, saved drafts library, print-to-PDF. Exports .docx via hand-rolled OOXML ZIP.

## Quality Pipeline

### Phase 1: Duplicate Resolution
Council reviews competing projects head-to-head. Higher score survives.

### Phase 2: Usefulness Refinement
Full 6-angle council on every survivor. Score 5+ on usefulness or get culled.

### Phase 3: Usefulness Cull
Final pass — anything still not genuinely useful gets cut.

### Phase 4: YouTube Research
Daily cron (06:15 JST) auto-discovers new videos from 7 monitored YouTube channels via RSS, extracts experiment cards, maintains a backlog. 44 experiments processed: 27 adopted, 10 parked, 7 in backlog.

### Security Scanning
22-rule regex scanner (`security_scan.py`) runs on every build. Full portfolio triaged: 0 real vulnerabilities. CSP meta tag in design.md boilerplate.

### Architecture Audit
12-piece agent architecture audit: 5 STRONG, 5 ADEQUATE, 0 WEAK (2 resolved). Halt mechanism and cost cap implemented.

## Adopted Experiments (27)

Key process improvements from Phase 4 research:

- **Approval-gated builds** — cron proposes, human approves, then it builds
- **6-angle council review** — bugs, security, UI, guide, usefulness, cool
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
| Tick-Tock Builder | Hourly | Proposes ideas (tick) or implements flagship features (tock). Builds only approved items. |
| Phase 4 Research | Daily 06:15 JST | YouTube RSS scan across 7 channels, experiment extraction, always commits run report |

## Monitored YouTube Channels (7)
@NateBJones, @MLOps, @DavidOndrej, [un]prompted, @NateHerk, @TwoMinutePapers, @Fireship

## Key Files

| File | Purpose |
|------|---------|
| `program.md` | Full builder methodology |
| `design.md` | Visual design system (dark industrial aesthetic) |
| `learnings.md` | Accumulated build knowledge (3000+ lines) |
| `yolo_log.json` | Append-only log of all builds |
| `experiments.json` | Phase 4 experiment tracker (44 experiments) |
| `session_state.json` | Tick-tock state, approval queues, phase 4 queue |
| `dashboard.html` | Portfolio dashboard (generated from log) |
| `test_project.py` | Automated test suite (7 checks) |
| `eval_bugs.py` | 26-pattern bug scanner |
| `security_scan.py` | 22-rule security scanner |
| `fetch_youtube_rss.py` | Phase 4 RSS feed fetcher (7 channels) |
| `build_log.py` | Structured JSON audit trail per build |
| `model-upgrade-audit.md` | 5-layer checklist for model swaps |
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

- **Builder**: Claude Sonnet 4.6 (remote triggers)
- **Council**: Gemini Pro (6-angle reviews via MCP)
- **Testing**: Python + Node.js + Playwright
- **Frontend**: Single-file HTML, zero external dependencies
- **Design**: Dark industrial aesthetic, monospace, ghost buttons

# YOLO Projects

Autonomous AI build system. Claude builds a new browser-based tool every hour, reviews it with a 6-angle council, and ships it — all unattended.

## How It Works

An hourly cron trigger fires a Claude Code remote agent that:

1. **Plans** — picks a high-ROI idea, writes a structure outline, sends it to Gemini for critique
2. **Builds** — implements a single-HTML-file, zero-dependency browser tool from the validated plan
3. **Tests** — runs automated test suite + 26-pattern bug eval scanner
4. **Reviews** — 6-angle Gemini council (bugs, security, UI, user guide, usefulness, cool factor)
5. **Ships** — fixes issues, writes README, logs to dashboard, commits, pushes

Every other hour is a **Tock** session that alternates between two flagship projects (Markdown Deck and Naval Scribe), implementing approved features or brainstorming new ones for approval.

## Portfolio

| Metric | Count |
|--------|-------|
| Total built | 198 |
| Active (passed council) | 77 |
| Culled (duplicates, visual toys, low utility) | 121 |

### Categories

- **Dev Tools** (22) — jwt-decode, json-explorer, regex-playground, ssl-check, dns-lookup, diff-painter, shader-forge, etc.
- **Creative Tools** (12) — beat-haus, note-lab, sonic-sight, palette-pull, sprite-forge, etc.
- **Productivity** (11) — markdown-deck, naval-scribe, kanban-board, pomodoro-flow, flash-cards, etc.
- **Games** (12) — picross, sudoku, neon-tetra, dungeon-descent, regex-quest, etc.
- **Generators & Utilities** (10) — entropy-forge, qr-forge, prose-xray, yaml-fmt, etc.
- **Education** (5) — neural-playground, circuit-sim, automata-lab, etc.

## Flagships

### Markdown Deck
Markdown-to-slide-deck editor with live preview, fullscreen presentation, PPTX export, 6 themes, templates, speaker notes, and presenter view. Single HTML file, zero dependencies.

### Naval Scribe
Naval correspondence formatter per SECNAV M-5216.5. 7 document types (standard letter, memo, endorsement, business letter, point paper, action memo, MOA with multiple signers). Exports properly formatted .docx files via hand-rolled OOXML ZIP generation.

## Quality Pipeline

### Phase 1: Duplicate Resolution
Council reviews competing projects head-to-head. Higher score survives. Lower score culled but preserved in log for learning.

### Phase 2: Usefulness Refinement
Full 6-angle council on every survivor. Projects must score 5+ on usefulness ("would someone bookmark this?"). Visual-only toys are culled.

### Phase 3: Usefulness Cull
Final pass. Anything that survived Phase 2 but still isn't genuinely useful gets cut.

### Phase 4: YouTube Research
Daily cron (06:15 JST) auto-discovers new videos from 6 monitored YouTube channels via RSS, extracts experiment cards, maintains a backlog. 32 experiments processed: 22 adopted, 10 parked.

## Adopted Experiments

Key process improvements from Phase 4 research:

- **6-angle council review** — every build reviewed for bugs, security, UI, guide, usefulness, cool
- **Vertical planning** — structure outline before code eliminates rework
- **Parallel builds** — 3 projects simultaneously via worktree isolation (2x throughput)
- **Autoresearch loop** — Gemini bug count as convergence metric
- **Boring-but-high-ROI filter** — "would a business pay for this?" idea selection
- **3-phase pipeline** — Plan (Gemini critique) → Build → Review (council)
- **Golden bug eval** — 26 patterns mined from learnings.md, run on every build
- **Model upgrade audit** — 5-layer checklist before any model swap
- **Golden-prompt eval** — 8 regression prompts to verify model quality after upgrades
- **Structured build logging** — JSON audit trail per project

## Automation

| Trigger | Schedule | What |
|---------|----------|------|
| Tick-Tock Builder | Hourly | Alternates new YOLO builds (tick) and flagship work (tock) |
| Phase 4 Research | Daily 06:15 JST | YouTube RSS scan, experiment extraction, backlog review |

## Key Files

| File | Purpose |
|------|---------|
| `program.md` | Full builder methodology |
| `design.md` | Visual design system (dark industrial aesthetic) |
| `learnings.md` | Accumulated build knowledge (2700+ lines) |
| `yolo_log.json` | Append-only log of all 198 builds |
| `experiments.json` | Phase 4 experiment tracker |
| `session_state.json` | Tick-tock state, phase 4 queue, portfolio counts |
| `dashboard.html` | Portfolio dashboard (generated from log) |
| `test_project.py` | Automated test suite (syntax, IDs, braces, browser) |
| `eval_bugs.py` | 26-pattern bug scanner |
| `build_log.py` | Structured JSON audit trail per build |
| `model-upgrade-audit.md` | 5-layer checklist for model swaps |
| `model-eval/` | Golden-prompt regression suite |
| `update_dashboard.py` | Dashboard regenerator |
| `update_session_state.py` | Session state persistence |

## Stack

- **Builder**: Claude Sonnet 4.6 (remote triggers)
- **Council**: Gemini Pro (6-angle reviews via MCP)
- **Testing**: Python + Node.js + Playwright
- **Frontend**: Single-file HTML, zero external dependencies
- **Design**: Dark industrial aesthetic, monospace, ghost buttons

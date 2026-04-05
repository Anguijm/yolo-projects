# Markdown Deck — Flagship Roadmap

Markdown Deck is a graduated YOLO project operating under Flagship rules: multi-session development, regression testing, iterative refinement.

## Architecture Constraints

- Single HTML file, zero external dependencies
- All CSS/JS inline — no CDNs, no build tools, no frameworks
- System font stacks only (no web fonts)
- Must work offline after first load
- Mobile-responsive (375px minimum)
- PPTX export must stay in sync with all visual features

## Current State (v1.0 — 2026-03-30)

### Core Features
- [x] Markdown → slide parser (h1-h4, bold, italic, code, lists, blockquotes, tables, images)
- [x] Live preview with thumbnail strip
- [x] Fullscreen presentation mode with keyboard nav
- [x] PPTX export (inline ZIP writer + OOXML generation)
- [x] design.md token system (structured design tokens → CSS)
- [x] 6 preset themes (Dark, Midnight, Light, Warm, Neon, Corporate)
- [x] Two-column layout (`|||` separator)
- [x] Element positioning (`[@ x:... y:... w:...]`)
- [x] Rich formatting (strikethrough, highlights, superscript, subscript)
- [x] Nested lists with indentation
- [x] Task lists (checkboxes)
- [x] Code blocks with language labels
- [x] Multi-line blockquotes
- [x] Table header row distinction
- [x] Speaker notes (`???`)
- [x] localStorage persistence for design tokens
- [x] DECK_GUIDE.md for model-driven authoring

### Known Limitations
- No slide transitions/animations
- No image embedding in PPTX (text only)
- No drag-and-drop element positioning (code only)
- No collaborative editing
- No PDF export
- Brace balance test false-positive (OOXML strings confuse regex counter)
- No undo/redo for editor
- No syntax highlighting in code blocks (monochrome only)

## Roadmap

### P0 — Authoring & Export (primary focus)
- [x] Syntax highlighting for code blocks — integrated from syntax-glow feeder
- [x] Save/load deck to localStorage + file open/save (.md files)
- [x] Per-slide theme overrides (<!-- bg: #color, text: #color --> directives)
- [x] Diagram support (```diagram fenced blocks via flow-ascii feeder)
- [x] PDF export (via browser print dialog)
- [x] Progressive reveal (-- fragment syntax, PPTX slide duplication)
- [x] Drag-and-drop visual positioning mode (Layout button)
- [x] Slide reordering via drag in thumbnail strip
- [x] PPTX structure fix (slideMaster/layout/theme/notes)
- [x] Speaker notes in PPTX
- [x] Tables in PPTX
- [x] Diagrams in PPTX (SVG→Canvas→PNG)
- [x] IL2+ security (CSP, zero external URLs)
- [x] Auto-close unclosed code fences
- [x] DECK_GUIDE.md stricter Gemini prompting instructions + validation checklist
- [x] Math/LaTeX rendering ($inline$, $$block$$, fractions, Greek, symbols — zero-dep)
- [x] Custom slide aspect ratios (16:9, 4:3, 1:1, 9:16 — dropdown + PPTX dims)
- [x] Template library (6 pre-built decks: pitch, tech review, sprint, lecture, status, blank)

### P1 — Presentation Features (lowest priority per user)
- [x] Presenter view (current slide + next slide + speaker notes + timer)
- [x] Slide transitions (fade, slide-left, zoom) — fade/slide/zoom with direction-aware animation, localStorage persistence
- [x] Standalone HTML Export — self-contained .html with embedded slides, nav, speaker notes toggle, slide counter
- [x] Slide Outline Panel — collapsible side panel with clickable H1 titles, O shortcut, current slide highlighted
- [x] Find & Replace (Ctrl+H) — overlay in markdown editor, find/replace single or all occurrences
- [x] Kiosk / Auto-Advance Mode — auto-advance every N seconds, configurable, loop option, Esc to dismiss
- [ ] Markdown editor improvements: line numbers, tab indentation — deprioritized
- [ ] Animation within slides — deprioritized

### P2 — Parking Lot
- [ ] Collaborative editing (WebRTC or shared localStorage)
- [ ] Import from .pptx (parse OOXML back to markdown) — rejected (violates zero-dep)
- [x] Image references in PPTX export (relationship infrastructure)

## Proposed Features (Pending Approval)

- **Laser pointer & annotation mode** — During fullscreen presentation: L = glowing laser dot (cursor/touch), A = freehand annotation drawing on slide canvas, S = spotlight (radial dim + lit circle around cursor), C = clear, Esc = exit. Pure overlay, no markdown/PPTX impact. Highest-value presenter feature missing from current build.
- **Per-slide talk time budget** — Presenter sets total duration (e.g. 20 min); budget = total ÷ slides. Supports `<!-- time: 2m -->` per-slide overrides. Presenter view shows slide time-used / budget with color ring (green→amber→red) and an overall progress bar. Optional opt-in chime at budget exhaustion via AudioContext.
- **Deck Statistics Panel** — Toolbar button opens a modal showing: total slides, words per slide (bar chart), total word count, estimated talk time at 120/150/200 WPM (selectable), slide breakdown by H1 section, and counts of code blocks/diagrams/math blocks/images. Pure string analysis of existing markdown, zero deps, all offline. Useful for speaker prep and deck health checks.
- **Named Snapshots (Version History)** — Ctrl+Shift+S saves a named checkpoint of the deck text to localStorage (up to 20 snapshots, auto-pruned). A "History" panel (toolbar button) lists snapshots with timestamp + name label; click any to preview (word count delta shown) and restore. Protects against accidental deletion, enables experiment-and-rollback authoring. localStorage-only, zero deps.

## Approved (Next Tock)


## Parking Lot

- Per-slide talk time budget — total duration ÷ slides, amber/red warnings when over
- Laser pointer & annotation mode — L for laser, S for spotlight, A for freehand annotation during present
- Slide transitions (fade, slide-left, zoom) — deprioritized
- Markdown editor improvements: line numbers, tab indentation — deprioritized
- Animation within slides — deprioritized
- Collaborative editing (WebRTC or shared localStorage)

## YOLO Feeder Projects

These are features complex enough to prototype as standalone YOLO single-session builds before integrating into Markdown Deck:

1. **syntax-glow** — Standalone code syntax highlighter (tokenizer for JS/Python/HTML/CSS → colored spans). If it works, extract the tokenizer into Markdown Deck's code block renderer.
2. **flow-ascii** — ASCII/text-based diagram renderer (boxes, arrows, flowcharts from simple text syntax). If it works, integrate as a new block type in slides.
3. **print-snap** — Browser-based HTML-to-PDF renderer using canvas + jsPDF-style approach. If it works, add PDF export to Markdown Deck.
4. **drag-layout** — Visual drag-and-drop positioning tool on a 16:9 canvas that outputs `[@ x:... y:... w:...]` directives. If it works, embed as an optional GUI mode.

## Session Log

| Date | Type | Work Done |
|------|------|-----------|
| 2026-03-30 | Tock | design.md token system, PPTX export |
| 2026-03-30 | Tock | Rich formatting, nested lists, images, tables |
| 2026-03-30 | Tock | Two-column layout, element positioning |
| 2026-03-30 | Tock | DECK_GUIDE.md authoring guide |
| 2026-03-30 | Tock | Syntax highlighting via syntax-glow feeder integration |
| 2026-03-30 | Tick | flow-ascii feeder: text diagram renderer |
| 2026-03-30 | Tock | Save/load: localStorage auto-save, Ctrl+S, file open/save |
| 2026-03-30 | Tick | cron-calc: multi-cron visual timeline |
| 2026-03-30 | Tock | Per-slide theme overrides (<!-- bg/text/font/align --> directives) |
| 2026-03-31 | Tick | api-bench: browser-based API latency benchmarker |
| 2026-03-31 | Tock | Progressive reveal (-- fragments) + PPTX slide duplication |
| 2026-03-31 | Tick | dep-graph: package manifest dependency visualizer |
| 2026-03-31 | Tock | Presenter view: dual-window with notes, next slide, timer |
| 2026-03-31 | Tick | commit-log: git history pattern analyzer |
| 2026-03-31 | Tock | Diagram support via flow-ascii feeder integration |
| 2026-03-31 | Tick | env-vault: .env file manager with diff and encrypt |
| 2026-03-31 | Tock | Slide reordering via drag-and-drop thumbnails |
| 2026-03-31 | Tick | snap-mock: device frame mockup generator |
| 2026-03-31 | Tock | PDF export via print dialog with per-slide themes |
| 2026-03-31 | Tick | log-lens: log file viewer with filtering and timeline |
| 2026-03-31 | Tock | PPTX image infrastructure + PDF export + image parsing |
| 2026-03-31 | Tick | drag-layout feeder: visual positioning GUI for [@ directives] |
| 2026-03-31 | Tock | Visual Layout mode: drag-and-drop positioning integrated from feeder |
| 2026-03-31 | Tock | P0 CRITICAL: Fix PPTX (slideMaster/layout/theme/notes), IL2 CSP, auto-close fences |
| 2026-03-31 | Tick | token-count: LLM token counter and cost estimator |
| 2026-03-31 | Tock | PPTX tables: parse markdown tables + render as formatted text in export |
| 2026-03-31 | Tick | jwt-decode: JWT token inspector with expiry timeline |
| 2026-03-31 | Tock | PPTX diagrams: SVG→Canvas→PNG pipeline for embedded diagram images |
| 2026-03-31 | Tick | schema-viz: JSON Schema / OpenAPI spec visualizer |
| 2026-04-01 | Tock | DECK_GUIDE.md: strict AI prompting rules, failure table, example prompt, validation checklist |
| 2026-04-01 | Tick | http-status: interactive HTTP status code reference |
| 2026-04-01 | Tock | Math/LaTeX rendering: $inline$, $$block$$, fractions, Greek, symbols |
| 2026-04-01 | Tick | color-a11y: WCAG contrast checker with CVD simulation |
| 2026-04-01 | Tock | Custom aspect ratios: 16:9, 4:3, 1:1, 9:16 with PPTX dimension sync |
| 2026-04-02 | Tick | readme-forge: README.md generator with badges and templates |
| 2026-04-02 | Tock | Template library: 6 pre-built decks (pitch, tech review, sprint, lecture, status, blank) |
| 2026-04-02 | Tick | ssl-check: SSL cert inspector (COUNCIL PILOT: bugs + security reviews) |
| 2026-04-02 | Tock | Preview/present parity: both use 960px virtual slide + scale-to-fit, identical fonts |
| 2026-04-02 | Tick | shader-forge (#168): live GLSL editor + naval-scribe (#169): naval correspondence .docx |
| 2026-04-02 | Tock | 6-bug fix: PPTX dims scoping, content auto-fit, Save reliability, Layout UX, bold regex, theme docs |
| 2026-04-02 | Tock | Slide transitions: fade/slide/zoom for presentation mode, direction-aware, localStorage persistence |
| 2026-04-02 | Tock | Brainstormed 2 features (pending approval): Standalone HTML export, Laser pointer & annotation mode |
| 2026-04-02 | Tock | Brainstormed 2 features (pending approval): Clipboard image paste, Per-slide talk time budget |
| 2026-04-03 | Tock | Clipboard image paste: Ctrl+V inserts base64 data URL at cursor, with KB size feedback toast |
| 2026-04-03 | Tock | Brainstormed 2 features (pending approval): Slide search, Notes export |
| 2026-04-03 | Tock | Pretext canvas measurement: IIFE replaces DOM reflow in autoFitContent for simple slides; fallback to scrollHeight for complex content |
| 2026-04-03 | Tock | Slide search: Ctrl+F overlay, searches slide bodies, highlights matches, keyboard nav (Enter/Esc/Arrows), jump-to-slide |
| 2026-04-03 | Tock | Notes export: "Notes" toolbar button exports all speaker notes as speaker-notes.md with heading per slide |
| 2026-04-03 | Tock | Brainstormed 2 features (pending approval): Standalone HTML export, Slide Outline Panel |
| 2026-04-03 | Tock | Brainstormed 2 features (pending approval): Find & Replace (Ctrl+H), Kiosk/Auto-Advance Mode |
| 2026-04-03 | Tock | All 4 approved features: Standalone HTML Export, Slide Outline Panel, Find & Replace (Ctrl+H), Kiosk Auto-Advance |
| 2026-04-04 | Tock | Brainstormed 2 features (pending approval): Laser pointer & annotation mode, Per-slide talk time budget |
| 2026-04-05 | Tock | Brainstormed 2 features (pending approval): Deck Statistics Panel, Named Snapshots (Version History) |

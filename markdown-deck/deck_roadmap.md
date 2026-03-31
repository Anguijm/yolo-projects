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

### P0 — Critical (next 2-3 sessions)
- [ ] Slide transitions (fade, slide-left, zoom) for presentation mode
- [x] Syntax highlighting for code blocks (keyword coloring by language) — integrated from syntax-glow feeder
- [ ] Markdown editor improvements: line numbers, tab indentation, auto-closing pairs
- [x] Save/load deck to localStorage + file open/save (.md files)

### P1 — High Value (next 5-10 sessions)
- [x] Per-slide theme overrides (<!-- bg: #color, text: #color --> directives)
- [x] Diagram support (```diagram fenced blocks via flow-ascii feeder integration)
- [x] Image references in PPTX export (relationship infrastructure + placeholder text; full base64 embedding deferred)
- [x] PDF export (via browser print dialog with print-specific stylesheet)
- [x] Progressive reveal (-- fragment syntax with fade-in, PPTX slide duplication)
- [x] Drag-and-drop visual positioning mode (Layout button, drag/resize overlay)
- [x] Presenter view (current slide + next slide + speaker notes + timer)
- [x] Slide reordering via drag in thumbnail strip

### P2 — Nice to Have
- [ ] Collaborative editing (WebRTC or shared localStorage)
- [ ] Custom slide aspect ratios (4:3, 1:1, vertical)
- [ ] Animation within slides (fade-in bullets, progressive reveal)
- [ ] Template library (pre-built slide layouts)
- [ ] Import from .pptx (parse OOXML back to markdown)
- [ ] Math/LaTeX rendering (KaTeX inline)

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

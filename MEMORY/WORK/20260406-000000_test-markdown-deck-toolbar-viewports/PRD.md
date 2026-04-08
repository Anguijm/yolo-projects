---
task: Test markdown-deck toolbar at three viewport widths
slug: 20260406-000000_test-markdown-deck-toolbar-viewports
effort: standard
phase: complete
progress: 12/12
mode: interactive
started: 2026-04-06T00:00:00+09:00
updated: 2026-04-06T00:00:00+09:00
---

## Context

Test the right-pane preview toolbar of markdown-deck at three viewport widths (1920×1080, 1280×800, 900×800). Serve via HTTP (file:// blocked). Capture screenshots and report toolbar row count, button visibility, cutoff, wrapping, and slide preview correctness at each width.

### Risks
- HTTP server may not be running or port conflicts
- Playwright session viewport resize may not reflow correctly without reload
- Toolbar may use overflow:hidden making cut-off invisible in snapshot but visible visually

## Criteria

- [x] ISC-1: HTTP server started and index.html returns HTTP 200
- [x] ISC-2: Screenshot captured at 1920x1080 viewport width
- [x] ISC-3: Toolbar row count at 1920x1080 reported
- [x] ISC-4: Button visibility (cut-off/hidden) at 1920x1080 reported
- [x] ISC-5: Slide preview render status at 1920x1080 reported
- [x] ISC-6: Screenshot captured at 1280x800 viewport width
- [x] ISC-7: Toolbar row count at 1280x800 reported
- [x] ISC-8: Button visibility (cut-off/hidden) at 1280x800 reported
- [x] ISC-9: Slide preview render status at 1280x800 reported
- [x] ISC-10: Screenshot captured at 900x800 viewport width
- [x] ISC-11: Toolbar row count at 900x800 reported
- [x] ISC-12: Button visibility and wrapping at 900x800 reported

## Decisions

## Verification

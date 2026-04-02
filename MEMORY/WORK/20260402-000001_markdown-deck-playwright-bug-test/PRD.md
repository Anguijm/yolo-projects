---
task: Test Markdown Deck browser bugs via Playwright
slug: 20260402-000001_markdown-deck-playwright-bug-test
effort: standard
phase: complete
progress: 15/15
mode: interactive
started: 2026-04-02T00:00:01Z
updated: 2026-04-02T00:00:15Z
---

## Context

Test the Markdown Deck app at http://localhost:8000/markdown-deck/index.html for four specific bugs using Playwright CLI browser automation. The app already has sample slide content loaded by default. The task is pure observation — no code changes. Report exactly what happens for each interaction.

### Risks

- Server may not be running; need to start it first
- PPTX download may silently fail without console error
- Layout button may have no visible change but toggle internal state
- Console errors may only appear after interactions, not on load

## Criteria

- [x] ISC-1: HTTP server starts successfully on port 8000
- [x] ISC-2: Page loads at localhost:8000/markdown-deck/index.html
- [x] ISC-3: Sample slide content is visible on page load
- [x] ISC-4: Console errors on page load are captured and reported
- [x] ISC-5: PPTX button is located and clicked
- [x] ISC-6: PPTX click result (download or no download) is reported
- [x] ISC-7: Console errors after PPTX click are captured and reported
- [x] ISC-8: Save button is located and clicked
- [x] ISC-9: Save click result (download or file picker) is reported
- [x] ISC-10: Console errors after Save click are captured and reported
- [x] ISC-11: Screenshot taken before Layout button click
- [x] ISC-12: Layout button is located and clicked
- [x] ISC-13: Screenshot taken after Layout button click
- [x] ISC-14: Visual difference (or lack thereof) after Layout click reported
- [x] ISC-15: Console errors after Layout click are captured and reported

## Decisions

## Verification

### Page Load
- URL: http://localhost:8000/markdown-deck/index.html — 200 OK
- Title: "Markdown Deck"
- Console error on load: `[ERROR] Failed to load resource: 404 @ http://localhost:8000/favicon.ico` (favicon only — not a JS bug)
- 11 slides loaded in markdown editor
- All buttons visible: Prev, Next, Present, Presenter, Layout, Templates, Theme, PPTX, PDF, Save, Open

### PPTX Button
- Result: DOWNLOAD triggered — `presentation.pptx` downloaded to `.playwright-cli/presentation.pptx`
- No new console errors after click

### Save Button
- Result: DOWNLOAD triggered — `presentation.md` downloaded to `.playwright-cli/presentation.md`
- No new console errors after click

### Layout Button
- Before: Standard editor+preview split layout, Layout button not active
- After: Layout button shows `[active]` state; new overlay "LAYOUT MODE" panel appears on slide with "Click + Block to add positioned elements" and a `+ Block` button
- Visual change: CONFIRMED — layout mode overlay appears on current slide
- No new console errors after click

### Summary
- All three buttons function correctly with no JS errors
- Only error across entire session: favicon.ico 404 (cosmetic, not a bug)

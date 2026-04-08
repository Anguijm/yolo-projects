---
task: Thorough browser test of markdown-deck index.html
slug: 20260406-000001_markdown-deck-browser-test
effort: standard
phase: complete
progress: 14/16
mode: interactive
started: 2026-04-06T00:00:01+09:00
updated: 2026-04-06T00:00:30+09:00
---

## Context

Markdown-deck is a local HTML tool (single file, file:// URL). User reports it "still does not work" after a prior fix. Prior verification was likely too shallow. We need a thorough multi-step browser automation test using Playwright to verify each aspect of the tool's functionality: initial render, live typing response, Present mode, toolbar buttons, console errors, and JS state values.

### Risks
- file:// URL may trigger CSP or CORS issues in Chromium
- Preview may render but show wrong content (old cached state)
- Present button may exist but fail silently
- JS functions may be undefined due to scope issues or load order

## Criteria

- [x] ISC-1: Page loads without HTTP or resource errors at file:// URL
- [x] ISC-2: Left textarea is visible and contains default markdown content
- [x] ISC-3: Right preview pane is visible after initial page load
- [x] ISC-4: Preview pane shows rendered slide content (not blank)
- [x] ISC-5: Textarea can be cleared and new content typed via Playwright
- [x] ISC-6: Preview updates after typing new markdown (debounce wait)
- [x] ISC-7: Preview shows slide title from newly typed content
- [x] ISC-8: Present button exists in the toolbar
- [x] ISC-9: Clicking Present button triggers presentation mode
- [x] ISC-10: Presentation mode is visually active (fullscreen overlay)
- [x] ISC-11: All toolbar button labels are enumerated and reported
- [ ] ISC-12: Zero console errors reported throughout the test
- [x] ISC-13: `typeof inputEl` evaluates to 'object'
- [x] ISC-14: `typeof parseSlides` evaluates to 'function'
- [x] ISC-15: `typeof renderPreview` evaluates to 'function'
- [ ] ISC-16: `document.getElementById('preview').children.length` is greater than 0

## Decisions

## Verification

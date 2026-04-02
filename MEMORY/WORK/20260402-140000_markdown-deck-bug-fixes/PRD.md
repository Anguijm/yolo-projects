---
task: Fix six Markdown Deck bugs — Tock session
slug: 20260402-140000_markdown-deck-bug-fixes
effort: advanced
phase: complete
progress: 12/12
mode: interactive
started: 2026-04-02T14:00:00+09:00
updated: 2026-04-02T14:15:00+09:00
---

## Context

Six bugs reported by John in Markdown Deck. This is a Tock session — flagship work with higher quality bar.

### Risks
- The codebase is 2317 lines in a single HTML file — surgical fixes needed to avoid regressions
- PPTX export uses async/await with miniZip — need to verify the zip function still exists after cron changes

## Criteria

- [ ] ISC-1: PPTX export button triggers download of presentation.pptx
- [ ] ISC-2: PPTX export generates valid file openable in PowerPoint/LibreOffice
- [ ] ISC-3: Slide content auto-scales to fit within slide dimensions
- [ ] ISC-4: Default aspect ratio is 16:9 (960x540 virtual)
- [ ] ISC-5: Layout button shows visible overlay with + Block button
- [ ] ISC-6: Layout button visual feedback when active (highlight/border change)
- [ ] ISC-7: Save button downloads .md file (or uses File System Access API)
- [ ] ISC-8: Theme panel changes apply to ALL slides, not just current
- [ ] ISC-9: Theme panel has clear label explaining "global vs per-slide"
- [ ] ISC-10: Bold (**text**) does not create spurious line breaks
- [ ] ISC-11: DECK_GUIDE.md updated with theme clarification
- [ ] ISC-12: All changes tested — no regressions in existing functionality
- [ ] ISC-A-1: Anti: No console errors after fixes

## Decisions

- 2026-04-02 14:00: PPTX bug likely caused by cron overwriting with different version — need to check miniZip function exists
- 2026-04-02 14:00: Content fitting fix via CSS overflow + auto font scaling approach
- 2026-04-02 14:00: Theme panel confusion is UX — add explanatory text to panel

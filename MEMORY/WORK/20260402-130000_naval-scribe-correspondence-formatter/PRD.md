---
task: Build naval-scribe Naval Correspondence formatter to DOCX
slug: 20260402-130000_naval-scribe-correspondence-formatter
effort: advanced
phase: complete
progress: 28/28
mode: interactive
started: 2026-04-02T13:00:00+09:00
updated: 2026-04-02T13:00:30+09:00
---

## Context

Build **naval-scribe** — a browser-based tool that takes pasted text or markdown and formats it as proper naval correspondence per SECNAV M-5216.5, then exports a correctly formatted .docx file. Single HTML file, zero external dependencies.

User pastes content into a structured form (From, To, Via, Subj, Ref, Encl, body text) or raw markdown, the tool applies naval formatting rules (Times New Roman 12pt, 1" margins, proper spacing, paragraph numbering), shows a live preview, and generates a downloadable .docx.

The .docx is generated in-browser using raw Office Open XML (OOXML) — a .docx is just a ZIP of XML files. We build the ZIP using a minimal inline implementation (STORE method, no compression needed).

**Not requested:** Full SSIC code database, every correspondence type, Marine Corps-specific variants.

### Risks
- Building a ZIP file from scratch in browser JS is non-trivial
- OOXML formatting (margins, fonts, spacing) requires exact XML namespace handling
- Paragraph numbering hierarchy (1. a. (1) (a)) needs correct indentation in OOXML
- Preview parity with actual .docx output is hard to guarantee

## Criteria

- [ ] ISC-1: Form has From field with text input
- [ ] ISC-2: Form has To field with text input
- [ ] ISC-3: Form has Via field supporting multiple numbered entries
- [ ] ISC-4: Form has Subj field (auto-uppercases input)
- [ ] ISC-5: Form has Ref field supporting multiple lettered entries
- [ ] ISC-6: Form has Encl field supporting multiple numbered entries
- [ ] ISC-7: Form has body textarea for correspondence text
- [ ] ISC-8: Form has signature block fields (name, rank, title)
- [ ] ISC-9: Form has date field defaulting to today in DD Mon YYYY format
- [ ] ISC-10: Form has Copy To field for distribution list
- [ ] ISC-11: Live preview panel shows formatted naval letter
- [ ] ISC-12: Preview uses Times New Roman 12pt font
- [ ] ISC-13: Preview shows proper double-spacing between header sections
- [ ] ISC-14: Body paragraphs use hierarchical numbering (1. a. (1) (a))
- [ ] ISC-15: Download button generates a valid .docx file
- [ ] ISC-16: Generated .docx has 1-inch margins on all sides
- [ ] ISC-17: Generated .docx uses Times New Roman 12pt
- [ ] ISC-18: Generated .docx has correct From/To/Via/Subj/Ref/Encl layout
- [ ] ISC-19: Generated .docx has signature block 4 lines below body text
- [ ] ISC-20: Correspondence type selector (Standard Letter, Memorandum)
- [ ] ISC-21: Layout uses split-pane: form left, preview right
- [ ] ISC-22: Design follows YOLO design system (dark bg, industrial aesthetic)
- [ ] ISC-23: Page is responsive — stacks vertically below 768px
- [ ] ISC-24: All code wrapped in IIFE
- [ ] ISC-25: test_project.py passes all automated checks
- [ ] ISC-26: Single index.html file with zero external dependencies
- [ ] ISC-A-1: Anti: No CDN imports or external references
- [ ] ISC-A-2: Anti: No console errors on initial page load

## Decisions

- 2026-04-02 13:00: Named naval-scribe — descriptive, fits portfolio naming
- 2026-04-02 13:00: .docx via inline OOXML ZIP — STORE method (no deflate needed), builds valid Office Open XML
- 2026-04-02 13:00: Form-based input over raw markdown parsing — naval correspondence has strict structure, form ensures correct fields

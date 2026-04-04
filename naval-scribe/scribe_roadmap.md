# Naval Scribe — Flagship Roadmap

Naval Scribe is a graduated YOLO project operating under Flagship rules alongside Markdown Deck. Tock sessions alternate between the two flagships.

## Current State (v1.0 — 2026-04-02)

### Correspondence Types (7)
- [x] Standard Naval Letter
- [x] Memorandum
- [x] Endorsement
- [x] Business Letter
- [x] Point Paper
- [x] Action Memo
- [x] Memorandum of Agreement (multiple signers)

### Core Features
- [x] Form-based input with conditional field visibility per type
- [x] Live preview with proper naval formatting
- [x] .docx export via hand-rolled OOXML ZIP
- [x] Auto paragraph numbering (1. a. (1) (a))
- [x] SSIC field, DD Mon YYYY date format
- [x] Multi-entry Via/Ref/Encl fields
- [x] localStorage auto-save
- [x] Times New Roman 12pt, 1-inch margins

## Approved (Next Tock)

- [ ] Second-Page Header Continuation — auto-insert recipient/SSIC/date header on page 2+, preview indicator + DOCX support
- [ ] Boilerplate Paragraph Library — 12-15 standard naval paragraph templates, one-click insert at cursor

## Recently Completed

- [x] Classification Marking Toggle — UNCLASSIFIED/CUI/FOUO/SECRET/TOP SECRET dropdown, colored banner in preview, proper DOCX header+footer XML with color-coded text
- [x] Letterhead Presets per Command — save up to 5 named presets (label + From value) in localStorage, one-click load to pre-fill From field, delete support
- [x] Saved Drafts Library — multiple named drafts in localStorage, save/load/delete drawer (up to 25 drafts, full state including via/refs/encls/parties)
- [x] Print-to-PDF mode — window.print() with @media print CSS hiding UI, one-click PDF
- [x] SSIC Code Lookup & Autocomplete — searchable dropdown, 46 bundled codes, keyboard nav, auto-fill on select
- [x] Signature Block Builder — paygrade select (E-1 through O-10 + W-1 to W-5), abbreviation lookup, by-direction checkbox, acting checkbox

## Completed

- [x] Inline tables in body text — parse markdown-style tables and render in preview + .docx
- [x] Paste-to-parse references — paste a block of references, auto-split into lettered (a), (b), (c) entries

## Parking Lot

- SSIC code search/lookup database
- Letterhead presets per command
- Second-page header continuation
- Classification marking toggle (UNCLASSIFIED/CUI)
- Endorsement chaining (append to existing letter)

## Session Log

| Date | Type | Work Done |
|------|------|-----------|
| 2026-04-02 | Tick | Initial build: 6 correspondence types, .docx export, council review |
| 2026-04-02 | Tock | Added Memorandum of Agreement with multiple signers |
| 2026-04-03 | Tock | Inline markdown tables in body (preview + .docx); paste-to-parse references block |
| 2026-04-03 | Tock | No approved items; brainstormed 2 PENDING features: Saved Drafts Library, Print-to-PDF mode |
| 2026-04-03 | Tock | No approved items; brainstormed 2 PENDING features: SSIC Code Lookup & Autocomplete, Signature Block Builder |
| 2026-04-03 | Tock | Implemented all 4 approved features: Saved Drafts Library, Print-to-PDF, SSIC Autocomplete (46 codes), Signature Block Builder. Also fixed: autoSave now saves full state, DOCX w:spacing merged, single-para no-number naval standard, New/Clear button added |
| 2026-04-03 | Tock | No approved items; brainstormed 2 PENDING features: Classification Marking Toggle, Letterhead Presets per Command |
| 2026-04-03 | Tock | Implemented Classification Marking Toggle (UNCLASSIFIED/CUI/FOUO/SECRET/TOP SECRET, preview banner + DOCX header/footer) and Letterhead Presets (up to 5 named presets, fill From field) |
| 2026-04-04 | Tock | No approved items; brainstormed 2 PENDING features: Second-Page Header Continuation, Boilerplate Paragraph Library |

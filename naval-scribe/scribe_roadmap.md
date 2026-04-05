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

_(queue empty — pending human approval)_

## Pending Approval

- [ ] **Endorsement Chaining** — Load any saved draft, then layer 1st/2nd/Nth endorsements on top of it. The UI shows the chain: Original + each endorsement in order. Export as a single .docx with proper OOXML endorsement headers ("FIRST ENDORSEMENT ON [ORIGINATOR] [SSIC] OF [DATE]"). Rationale: the most common naval routing workflow; existing Endorsement type only creates standalone endorsements, not a chained document.
- [ ] **Distribution / Copy-To Block** — Add a multi-entry "Copy to:" section (same pattern as Via/Ref/Encl) that renders at the bottom of the letter body in preview and .docx. Include a "Distribution" checkbox for wide distribution per SECNAVINST 5216.5D. Rationale: every real naval letter has a distribution list; currently missing from the form and export.
- [ ] **Auto-Format Import (Paste Existing Letter)** — Paste raw text of any naval letter into an import field; a regex-based parser extracts From/To/Via/Subj/SSIC/Date/References/Body paragraphs and pre-fills the entire form. Naval letter format is rigid enough (labeled fields, numbered paragraphs) to parse reliably. Rationale: staff officers receive letters and need to draft replies — currently they must retype every field from scratch; this closes that workflow gap entirely.
- [ ] **Command Address Book** — Persistent localStorage directory of frequently-used commands/units with formal names (e.g., "COMMANDING OFFICER, USS ENTERPRISE (CVN 65)"). Pre-seeded with ~20 common addressees (SECNAV, CNO, BUPERS, regional commands). One click populates any To/From/Via field; full CRUD (add/edit/delete custom entries). Rationale: typing formal command names correctly every time is error-prone and tedious; staff write to the same commands repeatedly.
- [ ] **Reply Draft Auto-Fill** — From any loaded saved draft, one click generates a pre-populated reply: From/To swapped, subject prefixed with "REPLY TO", date cleared, SSIC preserved, opening boilerplate inserted ("1. Reference (a) is acknowledged..."), original letter auto-added to references list. Closes the "receive a letter → draft a response" workflow gap with zero backend risk — pure state manipulation in JS. Rationale: staff officers spend significant time manually constructing reply templates; this collapses a multi-step process to one click.
- [ ] **Letter Status Tracker** — Add a `status` field to each saved draft: Draft → Signed → Transmitted → Replied. Draft library shows color-coded status badge and date milestone per letter. Filter/sort library by status. Rationale: staff officers track multiple concurrent correspondence actions; no tool currently connects the draft with its routing lifecycle. Pure localStorage — zero implementation risk.

## Recently Completed

- [x] Second-Page Header Continuation — visual indicator in preview (dashed break + SSIC/Date/To/Page# section), DOCX uses `<w:titlePg/>` with first-page (class only) and default (continuation) headers/footers
- [x] Boilerplate Paragraph Library — 13 templates across 4 categories (Opening, Standard, Action, Admin), collapsible panel in form, one-click insert at cursor

## Previously Completed

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
| 2026-04-04 | Tock | Implemented both approved features: Second-Page Header (preview indicator + DOCX titlePg/dual-header) and Boilerplate Library (13 templates, 4 categories, cursor-insert) |
| 2026-04-05 | Tock | No approved items; brainstormed 2 PENDING features: Endorsement Chaining, Distribution/Copy-To Block |
| 2026-04-05 | Tock | No approved items; brainstormed 2 PENDING features: Auto-Format Import, Command Address Book |
| 2026-04-05 | Tock | No approved items; brainstormed 2 PENDING features: Reply Draft Auto-Fill, Letter Status Tracker |

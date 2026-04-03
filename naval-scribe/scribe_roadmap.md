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

- [x] Inline tables in body text — parse markdown-style tables and render in preview + .docx
- [x] Paste-to-parse references — paste a block of references, auto-split into lettered (a), (b), (c) entries

## Pending (Brainstormed — Not Yet Approved)

- **Saved Drafts Library** — Multiple named drafts persisted in localStorage. User can name a draft, save it to a list, browse saved drafts, load or delete them. Solves the overwrite problem with the current single-slot auto-save. Implementation: `drafts` key in localStorage holds an array of `{name, type, fields, savedAt}`; a collapsible drawer in the form panel lists them.

- **Print-to-PDF mode** — "Print" button that triggers `window.print()` with `@media print` CSS hiding the form panel, top bar, and all UI chrome so only the formatted letter page is sent to the print dialog. Users get a properly margined PDF in one click, no .docx conversion needed. Implementation: add `@media print { #form-panel, #top-bar { display: none; } #preview-panel { padding: 0; } }` and a print button.

- **SSIC Code Lookup & Autocomplete** — Inline searchable dropdown for Standard Subject Identification Codes. As the user types in the SSIC field, it filters a bundled list of SSIC numbers and official subject titles, auto-filling on selection. Eliminates context-switch to SECNAV Manual 5210.11 and reduces miscoded correspondence. Implementation: static JS object of SSIC ranges/titles bundled in the HTML (<100KB), `keyup` event filters and renders a custom dropdown, no external requests.

- **Signature Block Builder** — Structured sub-form for name, paygrade (E-1 through O-10, WO/CWO), designator, billet title, and by-direction checkbox that outputs a correctly formatted signature block per naval correspondence standards. Enforces correct rank abbreviations, name capitalization, and element order — common error sources for junior personnel. Implementation: paygrade→abbreviation lookup table (~3KB), formatter assembles block in real time and injects into preview at correct position.

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

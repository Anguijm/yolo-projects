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

## Approved (Next Tock — priority order)

- [x] **Naval Instruction format** — selectable type with instruction number, cancellation date, structured sections
- [x] **Standard Operating Procedure format** — selectable type with SOP number, effective date, review cycle
- [x] **Enclosure footers** — each enclosure page shows "Enclosure (N) to [originator] ltr [SSIC] of [date]"
- [x] **Auto-Format Import (Paste Existing Letter)** — Paste raw text of any naval letter; regex parser fills form

## Approved (Remaining — one per tock)

- [x] Endorsement Chaining — layer endorsements on saved drafts, export as single .docx
- [x] Distribution / Copy-To Block — multi-entry copy-to section with Distribution checkbox
- [x] Command Address Book — localStorage directory of commands, one-click fill To/From/Via
- [ ] Reply Draft Auto-Fill — one click generates reply with swapped From/To, boilerplate
- [ ] Letter Status Tracker — Draft→Signed→Transmitted→Replied per saved draft
- [ ] Template Letter Library — 12 pre-built templates for common letter situations
- [ ] Routing Slip Generator — DON routing slip with reviewer chain, .docx export

## Recently Completed

- [x] **Distribution / Copy-To Block** (2026-04-08) — multi-entry recipient list with "distribution mode" checkbox; Naval Instructions get a `Distribution:` label + indented entries, all other types get standard `Copy to:` label per recipient. Wired in form (`copyto-list`), preview (`renderCopyTo`), DOCX export (`dCopyTo`), and draft restore. Council unanimous approve; lessons veto on adjacent `parseRefsBtn` paste loop resolved by adding `addItems()` batch method using `document.createDocumentFragment()`.
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
| 2026-04-05 | Tock | No approved items; brainstormed 2 PENDING features: Template Letter Library, Routing Slip Generator |
| 2026-04-06 | Tock | Auto-Format Import: "import" button opens drawer with paste area; state-machine parser detects type, SSIC, date, From/To/Via, Subj, Ref/Encl, body (with numbering-strip), all-caps signature + rank-line lookahead, Copy-to; all tests pass |
| 2026-04-06 | Tock | Endorsement Chaining: "chain" button opens drawer; set base from current form or saved draft; add N endorsements (FIRST/SECOND/...) each with date/from/to/body/sig; preview chain inline in preview panel; export full chain as endorsement_chain.docx with page breaks between docs |
| 2026-04-08 | Tock | Command Address Book: "addr book" button opens drawer; add up to 50 entries (label + full name); one-click → From / → To / + Via / × delete per entry; QuotaExceededError handling inline; createDocumentFragment batch render; aria-labels on all 5 action buttons; mutual exclusion with drafts/import/chain drawers. 4 council gates passed (plan attempt 2 after escalation; implementation attempt 2 after John fixed font-size 0.48rem→0.55rem + aria-labels; tests attempt 2; outcome attempt 2). |

# Naval Scribe — Routing Slip Generator Plan

## Goal
Add a DON routing slip generator: a new drawer that builds a reviewer chain (name/office + action code), previews a formatted routing slip table, and exports a standalone routing_slip.docx.

## Scope

**In scope:**
- New "routing slip" button in top-bar (opens `#routing-drawer`)
- Drawer: suspense date, drafter/return-to field, document subject (auto-populated from current form subject), editable reviewer chain (up to 15 rows)
- Each reviewer row: Name/Office text input + Action select (Review / Concur / Sign / Info)
- Live HTML table preview inside the drawer (static placeholder cells for Date Received, Date Returned, Initials — filled by hand on paper)
- Export standalone `routing_slip.docx` via existing `createZip` + `makeParagraph` infrastructure
- Mutual exclusion: routing-drawer closes all other drawers; all other drawer-open clicks close routing-drawer

**Not in scope:**
- Modifying the main letter's preview or download
- Saving routing slips to localStorage
- Printing the routing slip directly (docx export covers this)
- Any changes to the existing correspondence type system

## Approach

1. **CSS** — add `#routing-drawer` styles (same pattern as `#tmpl-drawer`: fixed left overlay, `.open` toggle). Add `.rs-*` class names for the routing slip table preview.
2. **HTML (drawer)** — add `#routing-drawer` div before the form panel (same location as other drawers). Include: close button, suspense date input, drafter/return-to input, subject display (read-only, mirroring form subject), reviewer chain container, "+ add reviewer" button, live preview div, export button.
3. **HTML (button)** — add `<button class="btn" id="routing-btn" aria-label="Generate routing slip for this correspondence">routing slip</button>` in the top-bar `.top-controls`, after reply-btn and before print-btn.
4. **JS** — all new code within the existing IIFE, after the Template Library block and before the `/* ── Init ── */` comment:
   - DOM refs: `routingBtn`, `routingDrawer`, `routingClose`, `routingSuspense`, `routingDrafter`, `routingSubjDisplay`, `routingChainContainer`, `routingPreviewDiv`
   - `addRoutingReviewer(name, action)` — appends a reviewer row to chain container; each row has text input (name/office), action select, and a remove button; all changes call `renderRoutingPreview()`
   - `renderRoutingPreview()` — rebuilds the HTML preview table: header row (Reviewer/Office | Action | Date Recv'd | Date Ret'd | Initials/Sig), body rows from current reviewer inputs, footer row showing suspense + drafter
   - `generateRoutingDocx()` — assembles OOXML using existing `makeParagraph`, `createZip`, `escXml` helpers; table rendered using `<w:tbl>` OOXML; downloads as `routing_slip.docx`
   - `routingBtn.addEventListener('click', …)` — mutual exclusion (close all other drawers), open routing-drawer, call `renderRoutingPreview()`
   - `F.subj.addEventListener('input', updateRoutingSubj)` — always-on listener that updates `#routing-subj-display` and calls `renderRoutingPreview()` whenever the form subject changes, whether drawer is open or not
   - `routingClose.addEventListener('click', …)` — close routing-drawer
   - Add `routingDrawer.classList.remove('open')` listeners on all existing drawer buttons (draftsBtn, importBtn, chainBtn, addrBtn, replyBtn, tmplBtn)
   - Add `routingBtn.addEventListener('click', ...)` close listener on each existing drawer's open button

**Sequencing:** CSS → HTML drawer → HTML button → JS (in above order). No inter-subtask dependencies except JS requires DOM elements to exist.

## File Layout

- `naval-scribe/index.html` — single file, all changes inline
  - CSS block (~line 424, end of `<style>`): append ~60 lines of routing drawer + preview table CSS
  - HTML: insert `#routing-drawer` div (~line 540, after `#reply-drawer` div), ~65 lines
  - HTML top-bar: insert `routing-btn` button (~line 455, after reply-btn), 1 line
  - JS: insert new routing slip block (~line 3916, before `/* ── Init ── */`), ~120 lines

## Function Map

`naval-scribe/index.html`:
- `addRoutingReviewer(name, action)` — **added** — appends one reviewer row (input + select + remove btn) to `#routing-chain`, wires input/change → `renderRoutingPreview`
- `renderRoutingPreview()` — **added** — reads all reviewer row inputs + suspense/drafter inputs; rebuilds `#routing-preview` innerHTML with an HTML table
- `generateRoutingDocx()` — **added** — reads routing slip data, calls `makeParagraph` + new inline `makeWTbl` helper for OOXML table; calls `createZip`; triggers download of `routing_slip.docx`
- `routingBtn.addEventListener` — **added** — mutual exclusion open/close toggle for routing-drawer
- `routingClose.addEventListener` — **added** — closes routing-drawer
- Cross-close listeners on all 6 existing drawer buttons — **added** (6 × 1-liner)

## Security

- All user input rendered in preview via `textContent` assignment (no `innerHTML` of user data). The drawer's live preview table uses DOM construction, not innerHTML concatenation of user strings.
- DOCX export: all user strings pass through existing `escXml()` before insertion into OOXML.
- No new external loads; no fetch; no form action. CSP unchanged (`connect-src 'none'`).
- Routing slip data is never written to localStorage. No new storage surface.
- Trust boundary: user controls name/office, action, suspense, drafter fields. All are text; no eval; no URL parsing.

## UI

- Button: `routing slip` in top-bar, same `.btn` class, mutual exclusion with all 6 existing drawers.
- Drawer opens over form panel (same overlay pattern as all other drawers). 420px wide on desktop; 100% on mobile.
- Drawer header: "Routing Slip" title + close × button.
- Fields: Suspense date (text input, placeholder "DD Mon YYYY or NLT [date]"), Drafter / Return To (text input), Document Subject (read-only text display wired via live `input` listener on `F.subj`; shows "(none)" when subject is empty; auto-updates in real time as user edits the form subject).
- Reviewer chain: vertical stack of rows, each row = [Name/Office text input (flex:1)] [Action select] [× remove button]. Rows added with "+ add reviewer" button; minimum 0 rows; max 15 enforced with a warning at 15.
- Live preview: rendered HTML table below the chain, updating on every keystroke. Table has a header row and one row per reviewer, plus a footer row for suspense/drafter. Static placeholder text "________" for date/initials columns — these are filled by hand.
- Empty state (0 reviewers): preview shows the table with only header + footer rows and a note "Add reviewers above."
- Export button: `export routing_slip.docx` — full-width, `.btn-primary` style; always enabled (can export even with 0 reviewers for a blank form).
- Drawer close: × button at top, and clicking any other drawer button closes routing-drawer.

## Guide

- Button label: `routing slip`
- Drawer title: `Routing Slip`
- Suspense field label: `Suspense Date`
- Drafter field label: `Drafter / Return To`
- Subject field label: `Document Subject` (with hint: "sourced from current form; edit above")
- Add button text: `+ add reviewer`
- Action options: `Review`, `Concur`, `Sign`, `Info`
- Export button text: `export routing_slip.docx`
- Max-15 warning: `Maximum 15 reviewers. Remove one to add another.`
- Preview table headers: `Reviewer / Office` | `Action` | `Date Recv'd` | `Date Ret'd` | `Initials / Sig`
- Preview footer row label: `Drafter / Return To:`
- Preview suspense row label: `Suspense:`

## Edge Cases

- **0 reviewers:** export produces a docx with only the header and footer rows — valid blank routing slip.
- **Empty name/office field:** row still appears in preview and docx; blank cell is fine (user fills on paper).
- **Subject empty in form:** display "(none)" in subject area; export uses "(none)" as document subject line.
- **Very long name/office text:** Preview table cells use `word-break: break-word` with no truncation — full text is always visible; the preview div has `overflow-x: auto` so very wide content scrolls. Docx wraps naturally via OOXML `<w:tblLayout w:type="autofit"/>`.
- **Suspense/drafter empty:** footer row shows blank cells in both preview and docx — acceptable.
- **15-reviewer max:** `+` button shows warning text and refuses to add; existing rows unaffected.
- **Drawer already open:** clicking routing-slip button again closes it (toggle, matching all other drawers).
- **Form subject changes after drawer opens:** subject display auto-updates in real time via an `input` listener on `F.subj`. No stale display — if the user edits the subject while the drawer is open, the field refreshes immediately.

## Test Strategy

1. `python3 test_project.py naval-scribe` — page loads, no JS errors (existing test).
2. Manual checks:
   - Click "routing slip" → drawer opens; all other drawers close.
   - Click another drawer btn while routing-drawer open → routing-drawer closes.
   - Add 3 reviewers, set suspense + drafter → preview table updates with each keystroke.
   - Export: downloads `routing_slip.docx`; opening in Word shows "DON ROUTING SLIP" heading, header row, reviewer rows, suspense + drafter footer.
   - At 15 reviewers, `+` button shows max warning.
   - Empty form (no subject): subject shows "(none)" in preview and docx.
   - Close × button closes drawer.

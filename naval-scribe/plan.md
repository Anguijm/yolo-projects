# Plan — Command Address Book (Naval Scribe Tock, 2026-04-08)

## Goal
Add a localStorage-backed directory of naval commands/organizations. Each entry stores a short label and a full official name. One-click buttons fill To, From, or append to Via in the form. Eliminates re-typing frequently-used command names.

## Scope
- `naval-scribe/index.html` — only file modified
- No new files

## Approach

### HTML Changes
1. Add `<button class="btn" id="addr-btn">addr book</button>` in `#top-bar` after `chain-btn`
2. Add `<div id="addr-drawer">` block (after `#chain-drawer`, before `#form-panel`)
   - Header row: "Command Address Book" title + close button
   - `<div id="addr-list"></div>` — rendered entries
   - Empty-state `<div id="addr-empty">` — "No entries yet — add a command below."
   - Add-entry form at bottom: two text inputs (label + name) + save button + inline error span

### CSS Changes
1. `#addr-drawer` — same pattern as `#chain-drawer`: fixed left panel, z-index 200, 420px wide, mobile 100%
2. `.addr-entry` — flex row: label (accent color) + name (secondary text) + three mini buttons [→ From] [→ To] [+ Via]
3. `#addr-add-form` — flex row, label input (80px), name input (flex:1), save btn
4. `#addr-add-err` — inline error text, small, amber

### JS Changes (new block `/* ── Command Address Book ── */`)
1. `ADDR_KEY = 'naval-scribe-addr-book'`
2. `getAddr()` / `saveAddr(arr)` — localStorage get/set with try/catch
3. `renderAddr()` — rebuilds `#addr-list` from stored data; shows/hides empty state
   - Each entry: label span (accent), name span, three buttons: fill-from, fill-to, add-via
   - Delete button per entry (×)
4. Mutual exclusion: `addrBtn` listener closes drafts/import/chain before opening
5. Close button `#addr-close` removes `.open` class
6. Fill buttons:
   - fill-from: `F.from.value = entry.name; updatePreview()`
   - fill-to: `F.to.value = entry.name; updatePreview()`
   - add-via: `viaFields.addItem(entry.name)` (already triggers `updatePreview`)
7. Add-entry save button:
   - Reads label + name inputs; trims both
   - Validates: both non-empty; max 50 entries; shows `#addr-add-err` inline (no alert)
   - On success: push to array, saveAddr, renderAddr, clear inputs
8. Delete: filter array, saveAddr, renderAddr
9. Existing mutual-exclusion listeners (`draftsBtn`, `importBtn`, `chainBtn`): add `addrDrawer.classList.remove('open')` to each

## File: `naval-scribe/index.html`
- Functions added: `getAddr`, `saveAddr`, `renderAddr`
- HTML added: `#addr-drawer`, `#addr-btn`
- CSS added: `#addr-drawer`, `.addr-entry`, `#addr-add-form`, `#addr-add-err`
- No changes to: `getFullState`, `restoreFullState`, DOCX generation, draft state

## Security
- All user-entered label/name values rendered through `esc()` before innerHTML
- Fill targets are direct `.value` assignments — no eval, no innerHTML injection

## UI
- Drawer pattern identical to existing drawers (fixed left, z-index 200, scrollable)
- Entry: `[LABEL]  full official name  [→ From] [→ To] [+ Via] [×]`
- Add form: `[label____] [Full Name_____________] [save]`
- Inline error above inputs (no browser alert)
- Limit: 50 entries; error shown if over limit

## Edge Cases
- Empty label or empty name → inline error, no save
- Over 50 entries → inline error, no save
- Via fill with no drawer open: works fine (viaFields.addItem is standalone)
- Addr drawer close when drafts/import/chain is open and vice versa

## Test Strategy
- `python3 test_project.py naval-scribe` — HTML loads, key IDs present, JS syntax clean
- `eval_bugs.py` — check for setTimeout / missing cleanup patterns (addr drawer has none)
- `security_scan.py` — verify no new external URLs or eval usage
- Manual: add 3 entries, fill To/From/Via each, verify form fields update
- Manual: delete an entry, verify list updates
- Manual: attempt to add >50 entries, verify inline error shown
- Manual: open addr with drafts open — drafts should close; vice versa

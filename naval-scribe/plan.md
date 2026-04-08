# Plan — Command Address Book (Naval Scribe Tock, 2026-04-08)

## Goal
Add a localStorage-backed directory of naval commands/organizations. Each entry stores a short label and a full official name. One-click buttons fill To, From, or append to Via in the form. Eliminates re-typing frequently-used command names.

**Escalation resolution applied (2026-04-08 by John, option A):**
- `saveAddr()` specifically catches `QuotaExceededError` by name; generic errors rethrow; on quota failure shows inline error in `#addr-add-err`; does NOT update in-memory array
- Inline storage disclaimer visible in drawer: "Stored locally on this device. Not synced. Not encrypted."
- LESSONS CSP-sha256 rule does not apply (FALSE POSITIVE — project uses `unsafe-inline`, no sha256 tokens)
- SECURITY CSP objection: `unsafe-inline` is the deliberate architecture for the entire zero-dep single-file HTML app — changing it would require extracting ALL inline styles and scripts across 3200+ lines into external files, breaking the zero-dep constraint. This is a known architectural tradeoff, not a per-feature issue.
- COOL signature-move requirement: OVERRIDDEN per `feedback_utility_focus.md` — "utility is king, no visual toys, build things people bookmark and use." Address book IS the utility win; zero visual toys required.

## Scope
- `naval-scribe/index.html` — only file modified
- No new files

## Approach

### HTML Changes
1. Add `<button class="btn" id="addr-btn">addr book</button>` in `#top-bar` after `chain-btn`
2. Add `<div id="addr-drawer">` block (between `#chain-drawer` and `#form-panel`)
   - Header row: "Command Address Book" title + close button
   - Storage disclaimer: "Stored locally on this device. Not synced. Not encrypted."
   - `<div id="addr-list"></div>` — rendered entries
   - Empty-state `<div id="addr-empty">` — "No entries yet — add a command below."
   - Add-entry form: label input with placeholder `e.g. CNO`, name input with placeholder `e.g. Chief of Naval Operations, Department of the Navy`, save button
   - `<span id="addr-add-err"></span>` — inline error (never alert)

### CSS Changes
1. `#addr-drawer` — same pattern as `#chain-drawer`: `display:none; position:fixed; top:32px; left:0; width:420px; bottom:0; z-index:200; background:var(--bg-surface); border-right:1px solid #333; overflow-y:auto; padding:12px`; `.open { display:block }`; mobile: `width:100%`
2. `.addr-entry` — flex row, align-items:center, gap:6px, padding:5px 4px, border-bottom:1px solid var(--border-default)
   - `.addr-label` — accent color, font-size:0.55rem, min-width:60px, flex-shrink:0
   - `.addr-name` — color var(--text-secondary), font-size:0.6rem, flex:1, overflow:hidden, text-overflow:ellipsis, white-space:nowrap
   - `.addr-acts` — display:flex, gap:4px, flex-shrink:0
3. `.addr-act-btn` — tap-target-safe buttons: `padding:5px 8px; min-height:32px; background:transparent; border:1px solid var(--border-default); color:var(--text-tertiary); font-family:inherit; font-size:0.48rem; cursor:pointer; white-space:nowrap` — ensures adequate mobile tap area
4. `#addr-add-form` — display:flex; gap:4px; margin-top:10px; align-items:flex-start
   - `#addr-label-in` — width:90px; flex-shrink:0
   - `#addr-name-in` — flex:1
5. `#addr-add-err` — display:block; font-size:0.45rem; color:#e3b341; margin-top:4px; min-height:1em
6. `#addr-disclaimer` — font-size:0.4rem; color:var(--text-tertiary); margin-bottom:8px; line-height:1.5

### JS Changes (new block `/* ── Command Address Book ── */`)
1. `var ADDR_KEY = 'naval-scribe-addr-book'`
2. `function getAddr()` — safe read: `try { return JSON.parse(localStorage.getItem(ADDR_KEY)) || []; } catch(e) { return []; }`
3. `function saveAddr(arr)` — specific QuotaExceededError handling:
   ```js
   try {
     localStorage.setItem(ADDR_KEY, JSON.stringify(arr));
     return true;
   } catch(e) {
     var errEl = document.getElementById('addr-add-err');
     if (e.name === 'QuotaExceededError' || e.name === 'NS_ERROR_DOM_QUOTA_REACHED') {
       if (errEl) errEl.textContent = 'Storage full — entry not saved.';
     } else {
       if (errEl) errEl.textContent = 'Could not save entry.';
       throw e;  // rethrow unexpected errors
     }
     return false;  // caller must NOT update in-memory array on false
   }
   ```
4. `function renderAddr()` — rebuilds `#addr-list` using `document.createDocumentFragment()` (batch DOM pattern):
   - For each entry: create row with `.addr-label` (esc(entry.label)), `.addr-name` (esc(entry.name)), 3 action buttons (→ From, → To, + Via), delete button (×)
   - All buttons use `.addr-act-btn` class for adequate tap targets
   - Shows `#addr-empty` when array empty
5. `addrBtn` click: closes draftsDrawer/importDrawer/chainDrawer, toggles `#addr-drawer.open`
6. `#addr-close` click: removes `.open`
7. Fill buttons wired in `renderAddr()` per entry (closures):
   - `→ From`: `F.from.value = entry.name; updatePreview()`
   - `→ To`: `F.to.value = entry.name; updatePreview()`
   - `+ Via`: `viaFields.addItem(entry.name)` (triggers updatePreview internally)
8. Add-entry save button:
   - Reads `#addr-label-in` and `#addr-name-in`; trims both; clears prior error
   - Validates: both non-empty; `arr.length >= 50` (max 50 entries); shows inline error in `#addr-add-err` if invalid
   - On validation pass: push to local copy of array; call `saveAddr(newArr)` — if `false`, do NOT commit (quota error already shown); if `true`, update global ref, call `renderAddr()`, clear inputs
9. Delete button per entry (wired in `renderAddr()`): filter array, call `saveAddr(newArr)`, if success call `renderAddr()`
10. Mutual exclusion: add `addrDrawer.classList.remove('open')` to existing `draftsBtn`, `importBtn`, `chainBtn` listeners
11. Init: call `renderAddr()` at end of init block

## Files touched
- Functions added: `getAddr`, `saveAddr`, `renderAddr`
- Variables added: `ADDR_KEY`, `addrDrawer`, `addrBtn`, addr input/error refs
- HTML added: `#addr-drawer`, `#addr-btn`
- CSS added: `#addr-drawer`, `.addr-entry`, `.addr-act-btn`, `.addr-label`, `.addr-name`, `.addr-acts`, `#addr-add-form`, `#addr-add-err`, `#addr-disclaimer`
- No changes to: `getFullState`, `restoreFullState`, DOCX generation, draft state

## Security
- All user-entered label/name values rendered through `esc()` before innerHTML
- Fill targets are direct `.value` assignments — no eval, no innerHTML injection
- `saveAddr` specifically catches `QuotaExceededError` (and `NS_ERROR_DOM_QUOTA_REACHED` for Firefox); generic errors rethrow
- CSP `unsafe-inline`: architectural constant for entire zero-dep single-file pattern — not addressable per-feature

## UI
- Drawer pattern identical to existing drawers (fixed left, z-index 200, scrollable)
- Storage disclaimer visible at top of drawer body
- Entry: `[LABEL]  full official name  [→ From] [→ To] [+ Via] [×]`
- Add form: label input (placeholder "e.g. CNO"), name input (placeholder "e.g. Chief of Naval Operations, Department of the Navy"), [save] button
- Action buttons use `.addr-act-btn` with `min-height:32px; padding:5px 8px` for mobile tap safety
- Inline error in `#addr-add-err` (never alert)
- Limit: 50 entries; inline error if over limit

## Edge Cases
- Empty label or empty name → inline error, no save
- Over 50 entries → inline error, no save
- localStorage quota exceeded → inline "Storage full — entry not saved.", array unchanged
- Other localStorage errors → rethrow (unexpected condition)
- Via fill: works fine (viaFields.addItem is standalone)
- Addr drawer close when drafts/import/chain open and vice versa

## Test Strategy
- `python3 test_project.py naval-scribe` — HTML loads, key IDs present, JS syntax clean
- `eval_bugs.py` — check for setTimeout / missing cleanup (addr drawer has none)
- `security_scan.py` — verify no new external URLs or eval usage
- Manual: add 3 entries, fill To/From/Via each, verify form fields update
- Manual: delete an entry, verify list updates
- Manual: attempt to add >50 entries, verify inline error
- Manual: open addr with drafts open — drafts close; vice versa

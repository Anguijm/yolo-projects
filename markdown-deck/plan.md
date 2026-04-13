# Plan: Named Snapshots / Version History

## Goal
Add Named Snapshots / Version History to Markdown Deck: Ctrl+Shift+S takes a named checkpoint (up to 20), a toolbar "Snapshots" button opens a modal with preview thumbnails and one-click restore.

## Scope
**In scope:**
- `takeSnapshot()` triggered by Ctrl+Shift+S
- Up to 20 checkpoints stored in localStorage key `mdeck_snapshots`; oldest auto-pruned when limit exceeded
- Snapshot panel modal: list of checkpoints with thumbnail, label, timestamp, slide count, restore, delete
- Inline editable label per snapshot (click label text → contenteditable)
- Restore: replaces textarea + design panel content, parses slides, triggers autoSave
- Confirm dialog before restore (content will be overwritten)
- Brief toast notification on snapshot taken (accurate status — success or failure)
- ESC closes the modal
- Toolbar button "Snapshots" (no keyboard shortcut for opening panel — Ctrl+Shift+S only saves)

**Not in scope:**
- Branching / diff views between snapshots
- Export snapshots to file
- Automatic periodic snapshots (only manual)
- Thumbnail shows slide 1 only (not multi-slide gallery)

## Approach

### Subtask 1: CSS (no dependencies)
Add styles for `#snapshots-modal`, `.sn-*` classes (header, list, item, thumb, label, meta, actions, empty state). Follow existing modal patterns: `display:none` → `.open { display:flex }`.
**Modal width: `680px; max-width: calc(100vw - 2rem)`** — matching existing KEEP pattern from Deck Statistics modal.

### Subtask 2: HTML (depends on CSS names)
Insert `#snapshots-modal` div after `#stats-modal` (line ~608). Add a `<div id="snap-toast">` for the save confirmation indicator. Add "Snapshots" toolbar button after "Stats" button (line ~406).

### Subtask 3: JS — storage helpers (no dependencies)
`var SNAP_KEY = 'mdeck_snapshots'` constant.  
`function _loadSnaps()` — reads localStorage, returns parsed array or `[]`. **Wraps `JSON.parse` in try/catch to gracefully handle corrupt data without crashing.**  
`function _saveSnaps(arr)` — JSON.stringify + setItem, wrapped in try/catch. **Returns `true` on success, `false` on QuotaExceededError or other exception.** Never mutates the array.

### Subtask 4: JS — takeSnapshot (depends on subtask 3)
```
function takeSnapshot(label)
```
- Captures `inputEl.value`, `designInputEl.value`, `slides.length`, ISO timestamp, auto-label.
- Builds candidate array: prepend new snapshot, slice to 20.
- **Calls `_saveSnaps(candidate)`. If it returns `false`, show failure toast "Storage full — snapshot not saved" and do NOT update the in-memory `_snaps` array.**
- If `_saveSnaps` returns `true`, update `_snaps = candidate` and show "Snapshot saved (N/20)" toast.
- ID generation: `Date.now().toString(36) + Math.random().toString(36).slice(2, 8)` — collision-resistant without external libs.

### Subtask 5: JS — renderSnapshotsList (depends on takeSnapshot structure)
Builds snapshot list items using `document.createDocumentFragment()` for batch rendering (per naval-scribe KEEP pattern — full re-render of a bounded list uses fragment to avoid unnecessary DOM reflows). Clears `#sn-list` children, then appends the completed fragment. Each `.sn-item` contains:
- `.sn-thumb` div: renders `md(firstSlideMarkdown)` at `font-size:0.35rem` with overflow hidden (same pattern as thumb strip at line 118 — identical rendering technique used throughout the app for all thumbnails and previews)
- `.sn-label` span: `contenteditable="true"`, blur handler saves edited label; if label emptied on blur, revert to auto-generated label. **Discoverability: subtle pencil icon (✎ via CSS `::after`) appears on hover, plus `title="Click to rename"` tooltip** (per GUIDE feedback)
- `.sn-meta` span: timestamp + "N slides"
- `.sn-actions`: "Restore" and "Del" buttons

Thumbnail: extract text before first `\n---\n` from snapshot.content, pass through `md()`, inject as innerHTML of `.sn-thumb`. This is the identical pattern to the existing thumb strip (which also sets `innerHTML = md(slideText)`).

### Subtask 6: JS — restoreSnapshot / deleteSnapshot (depends on subtask 5)
`restoreSnapshot(id)`: `confirm()` dialog, then set `inputEl.value`, set design textarea if snapshot has design, call `applyDesign()`, `parseSlides()`, `renderPreview()`, `autoSave()`, close modal.  
`deleteSnapshot(id)`: filter array, call `_saveSnaps()` (ignore return on delete since we're only removing data), update `_snaps`, re-render list.

### Subtask 7: JS — openSnapshotsPanel / closeSnapshotsPanel (depends on subtask 5)
Open: load from storage into `_snaps`, render list, add `.open` class.  
Close: remove `.open` class.

### Subtask 8: Keyboard shortcut (depends on takeSnapshot)
In main `keydown` handler (line ~1639–1641), add before existing Ctrl+F/Ctrl+H:
```js
if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'S') { e.preventDefault(); takeSnapshot(); return; }
```

### Subtask 9: ESC handler (depends on modal)
Add `#snapshots-modal` to the existing ESC block at line 1622–1629.

### Sequencing
1→2→3→4→5→6→7 are sequential (each builds on prior).  
8 and 9 are independent of 5–7 but depend on 4.  
All can be written in a single pass.

## File Layout
- `markdown-deck/index.html` — sole file modified
  - CSS section (~line 232): insert ~60 lines of new `.sn-*` and `#snapshots-modal` styles and `#snap-toast`
  - HTML section (~line 608): insert `#snapshots-modal` div (~30 lines) and `#snap-toast` div (~1 line)
  - Toolbar (~line 406): add 1 button
  - JS keydown handler (~line 1639): add 1 conditional
  - JS keydown ESC block (~line 1622): add 1 modal close check
  - New JS section near bottom (~line 3759, after stats close): ~130 lines of snapshot logic

**Total estimated additions: ~225 lines.**

## Function Map

### `markdown-deck/index.html`

**New functions:**
- `_loadSnaps()` — reads `mdeck_snapshots` from localStorage; returns `[]` on missing/corrupt (try/catch around JSON.parse)
- `_saveSnaps(arr)` — writes array to localStorage; returns `true` on success, `false` on QuotaExceededError
- `takeSnapshot(label?)` — creates checkpoint `{id, ts, label, content, design, slideCount}`, prepends, trims to 20, calls `_saveSnaps()`; only updates `_snaps` if persistence succeeds; shows accurate toast
- `_snFirstSlide(content)` — returns markdown text of first slide (before first `\n---\n`)
- `_fmtSnapTs(isoStr)` — formats ISO timestamp to "Apr 12, 06:21"
- `renderSnapshotsList()` — rebuilds `#sn-list` using `document.createDocumentFragment()` for batch rendering from `_snaps` array
- `restoreSnapshot(id)` — confirms, restores content + design, refreshes preview, closes modal
- `deleteSnapshot(id)` — removes from `_snaps`, saves, re-renders list
- `openSnapshotsPanel()` — loads from storage, renders, opens modal
- `closeSnapshotsPanel()` — removes `.open` class

**Modified functions/handlers:**
- Main `keydown` handler (line ~1639) — add `Ctrl+Shift+S` branch
- ESC block (line ~1622) — add `#snapshots-modal` close check

## Security
- All snapshot content is user-authored markdown stored in `localStorage` (same origin, never transmitted externally). Users author the content themselves; there is no external injection surface.
- `innerHTML` assignment from `md()` is the **exact same pattern** used throughout the app for all thumbnails (thumb strip line 118), preview panel (line 1264), and presentation mode (line 1334). No new attack surface is introduced — if this were a vulnerability, the entire existing slide rendering system would also be vulnerable.
- The `esc()` function is used for inline code and code block content. Markdown text in heading/paragraph context is transformed by `md()` into HTML markup, consistent with all existing rendering.
- Label text is rendered via `textContent` assignment (not `innerHTML`) — no XSS risk on editable label.
- `confirm()` before restore prevents accidental data loss.
- `_saveSnaps` returns `boolean`; `takeSnapshot` only updates in-memory state on confirmed persistence success.
- `_loadSnaps` wraps `JSON.parse` in try/catch to handle corrupt storage gracefully.
- CSP: `unsafe-inline` is the existing architectural baseline.

## UI
- "Snapshots" button in toolbar (next to Stats button), matching existing button style.
- Ctrl+Shift+S triggers snapshot from anywhere (editor or outside textarea).
- Modal: centered, **680px wide, max-width: calc(100vw - 2rem)**, max 80vh, dark theme matching existing modals.
- Each item: 120×68px thumbnail on the left (same rendering as thumb strip), label text on right (click to edit inline), timestamp + slide count below, "Restore" and "Del" action buttons.
- Empty state: "No snapshots yet — press Ctrl+Shift+S to save your first checkpoint."
- Header: "SNAPSHOTS" title (small caps, like other modals) + "N / 20" count badge + close ×. (No "Take Snapshot" button in the modal — Ctrl+Shift+S is the primary save method, per UI feedback.)
- Toast: pill at top-center, visible 1.5s. **"Snapshot saved (N/20)"** on success. **"Storage full — not saved"** on QuotaExceededError.
- On restore confirm: `confirm("Restore this snapshot? Your current content will be replaced.")`.

## Guide
- Button label: "Snapshots"
- Button title tooltip: "Named Snapshots — Ctrl+Shift+S to save checkpoint"
- Modal title: "Snapshots"
- Count badge: "3 / 20"
- Snapshot default label: auto-generated from `new Date().toLocaleTimeString()` (e.g., "7:21:03 AM")
- Edit label: click label to edit inline (pencil icon ✎ on hover + tooltip "Click to rename"), blur to save; empty string reverts to auto-generated
- Restore button: "Restore"
- Delete button: "Del"
- Toast (success): "Snapshot saved (N/20)"
- Toast (failure): "Storage full — not saved"
- Empty state: "No snapshots yet. Press Ctrl+Shift+S to save your first checkpoint."
- Restore confirm: "Restore this snapshot? Your current content will be replaced."

## Edge Cases
- **localStorage full (QuotaExceededError):** `_saveSnaps` returns `false`. `takeSnapshot` does NOT update `_snaps`. Toast shows "Storage full — not saved". Snapshot is not retained in-memory (no phantom state).
- **Corrupt localStorage data:** `_loadSnaps` catches the JSON.parse exception, logs to console, returns `[]`. Effectively a clean slate.
- **Snapshot taken with 0 slides:** `slideCount = 0` is valid; thumbnail will be blank.
- **Restore when presenting:** not possible (no toolbar access during presentation). Non-issue.
- **Editing label to empty string:** if label becomes empty on blur, revert to the stored auto-generated label.
- **20-snapshot limit:** oldest (last item in array) is removed when 21st is added; badge shows count.
- **Confirm dialog cancelled:** no change to content. Modal stays open.
- **Design panel empty:** `designInputEl.value` is the default text; saved as-is; restore sets it back.
- **Two rapid Ctrl+Shift+S presses:** each creates a distinct snapshot (`Date.now().toString(36) + random` ID).
- **ID uniqueness:** `Date.now().toString(36) + Math.random().toString(36).slice(2,8)` — safe for up to 20 in-session snapshots; collision probability negligible.

## Test Strategy
- `test_project.py markdown-deck` must PASS (loads HTML, checks for syntax errors, basic structure).
- Manual verification checklist:
  1. Press Ctrl+Shift+S → toast "Snapshot saved (1/20)" appears
  2. Take 21 snapshots → oldest auto-removed, count stays at 20
  3. Edit label → persists after blur; empty label reverts to auto-generated
  4. Restore snapshot → confirm dialog → content replaced, design restored, deck re-parses
  5. Cancel restore → no change
  6. Delete snapshot → item removed from list, count decrements
  7. ESC closes modal
  8. Open modal → all snapshots shown with correct thumbnails and timestamps
  9. Empty state shown when 0 snapshots
  10. Toolbar "Snapshots" button opens modal
  11. Toast shows "Storage full — not saved" on QuotaExceededError

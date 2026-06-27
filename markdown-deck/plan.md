# Markdown Deck — Slide Sorter View (Tock plan)

## Goal
Add a Slide Sorter View: a full-screen overlay grid of slide thumbnails (Shift+V) where the user can click a slide to jump to it and drag a slide to reorder the deck.

## Scope
**In scope:**
- New `Shift+V` keyboard shortcut to toggle a full-screen Slide Sorter overlay (and a toolbar button).
- A responsive grid (target 4 columns on desktop, fewer when narrow) of numbered slide cards, each rendering a live `md()` thumbnail of the slide body.
- Click a card → jump to that slide (sets `currentSlide`, re-renders preview) and close the sorter.
- Drag a card onto another → reorder the deck, reusing the EXACT same reorder logic as the existing thumbnail-strip drag (extracted into one shared function so both paths stay identical).
- Highlight the current slide; live re-render of the grid after a reorder.
- Esc closes the overlay (wired into the existing Escape handler chain).

**Explicitly NOT in scope:**
- No change to the markdown parser, PPTX/PDF/HTML export, or rendering pipeline.
- No multi-select / bulk move, no slide deletion or duplication from the sorter.
- No new persistence keys (reorder already persists via existing `autoSave`).
- No touch-specific drag gestures beyond what native HTML5 DnD provides (matches existing thumbnail strip behavior).

## Approach
Subtask 1 — **Refactor shared reorder (dependency for everything else):** Extract the body of the existing `thumbsEl` `drop` handler (lines ~3015-3046) into a reusable `reorderSlideByIndex(srcIdx, dropIdx)` that mutates the textarea, fixes `currentSlide`, re-parses, re-renders, and auto-saves. Point the existing thumbnail drop handler at it (no behavior change). This guarantees the sorter and the strip reorder identically.

Subtask 2 — **Markup + CSS:** Add a `#sorter-modal` full-screen overlay (modeled on `#snapshots-modal` / outline panel conventions: header with title + count + close, scrollable body). Add a `.sorter-grid` (CSS grid, `repeat(auto-fill, minmax(...))` → ~4 cols at desktop width) and `.sorter-card` styles reusing the dark theme tokens. Reuse the `.sn-thumb` look for the per-card preview.

Subtask 3 — **Render + open/close (depends on 1, 2):** `renderSorter()` builds cards from `slides[]`, each `draggable`, with `data-idx`, a number badge, an `md()` preview, active-state highlight, and an `onclick="goSlide(i); closeSorter()"`. `openSorter()/closeSorter()/toggleSorter()` mirror the outline panel pattern. Drag handlers on the grid container call `reorderSlideByIndex` then `renderSorter()` to refresh in place.

Subtask 4 — **Wire shortcuts (depends on 3):** Add `Shift+V` to the main keydown handler (guarded by `!presenting` and not typing in the textarea) and an Esc branch to close the sorter. Add a toolbar button.

Subtask 5 — **Docs:** Update `deck_roadmap.md` (check the item, add session-log row) and the in-file help/guide text.

## File Layout
- `markdown-deck/index.html` (single file, all changes):
  - CSS block (~line 260, before `</style>`): add `#sorter-modal`, `.sorter-grid`, `.sorter-card`, `.sorter-thumb`, badge/active styles.
  - Body markup (~line 668, after `#snapshots-modal`): add `#sorter-modal` overlay element.
  - Toolbar (~line 451): add `<button onclick="toggleSorter()">Sorter</button>`.
  - Main keydown handler (~line 1849-1879): add `Shift+V` toggle + Esc-close branch (~line 1856).
  - Reorder section (~line 2990-3053): extract `reorderSlideByIndex`; repoint existing drop handler.
  - New JS section after reorder (~line 3053): `renderSorter`, `openSorter`, `closeSorter`, `toggleSorter`, sorter drag handlers.
- `markdown-deck/deck_roadmap.md`: check Slide Sorter item; append session-log row.
- `markdown-deck/plan.md`: this file.

## Function Map
- `markdown-deck/index.html`:
  - **`reorderSlideByIndex(srcIdx, dropIdx)`** — NEW. Extracted shared reorder: splits `inputEl.value` on `/\n---\n/`, moves the segment, fixes `currentSlide`, `currentFragment=0`, `parseSlides()`, `renderPreview()`, `autoSave()`. Returns early on invalid/no-op indices.
  - **`thumbsEl 'drop'` handler** — MODIFIED. Now computes `dropIdx`/`dragSrcIdx` and delegates to `reorderSlideByIndex`.
  - **`renderSorter()`** — NEW. Rebuilds `#sorter-grid` innerHTML from `slides[]`.
  - **`openSorter()`** — NEW. `renderSorter()` + add `.open`.
  - **`closeSorter()`** — NEW. Remove `.open`.
  - **`window.toggleSorter`** — NEW. Open/close based on current state.
  - **Sorter `dragstart`/`dragover`/`dragleave`/`drop`/`dragend` handlers** — NEW, on the grid container; `drop` calls `reorderSlideByIndex(...)` then `renderSorter()`.
  - **main keydown handler** — MODIFIED. Adds `Shift+V` and Esc-for-sorter branches.

## Security
- Threat model unchanged: local-only, single-file, user authors their own markdown (see `CONSTRAINTS.md`). The sorter introduces NO new external content source or injection vector.
- Per-card previews use the same `md() + innerHTML` rendering pattern already used by the thumbnail strip, preview, presentation mode, and snapshots modal (CONSTRAINTS Constraint 2 — app-wide baseline, not a new surface). The number badge and any titles are escaped via the existing `esc()` where text is interpolated.
- No new storage keys; reorder persists through the existing `autoSave` localStorage path (CONSTRAINTS Constraint 3). CSP/`unsafe-inline` unchanged (CONSTRAINTS Constraint 1).

## UI
- Toolbar "Sorter" button + `Shift+V` toggle. Full-screen dark overlay above the editor.
- Header: title "Slide Sorter", live "N slides" count, × close button.
- Grid of cards (~4 cols desktop, collapses on narrow widths via `auto-fill minmax`). Each card: number badge (top-left), live slide preview, green border on the current slide, `cursor: pointer`.
- Drag affordance reuses the strip's `dragging`/`drag-over` visual language (dashed accent border on the drop target, reduced opacity on the dragged card).
- **Empty state:** if `slides.length === 0`, show a centered muted "No slides yet" message instead of an empty grid.
- **Loading state:** N/A — synchronous, no async fetch.
- **Error state:** invalid drag (drop on self / out of range) is a silent no-op via `reorderSlideByIndex` guards.

## Guide
- Toolbar button label: `Sorter`, title `Slide Sorter — grid overview, click to jump, drag to reorder (Shift+V)`.
- Header copy: `Slide Sorter`. Empty copy: `No slides yet — add content in the editor.`
- Append a "Slide Sorter View" section to the in-file DECK help text describing Shift+V, click-to-jump, drag-to-reorder, Esc-to-close.

## Edge Cases
- Empty deck (0 slides) → empty-state message, no grid, no crash.
- Single slide → grid of 1; drag is a no-op (guarded).
- Drop on self or out-of-range index → no-op (existing reorder guards preserved).
- Reorder when the moved slide is the current slide → `currentSlide` follows the move (existing index-fix logic reused).
- Opening the sorter while presenting → guarded: `Shift+V` ignored when `presenting`.
- Typing `V` in the textarea → guarded by `document.activeElement !== inputEl`.
- Very long decks → grid body scrolls (`overflow-y: auto`), thumbnails are size-capped.

## Test Strategy
- `python3 test_project.py markdown-deck` — structural/HTML validity must PASS.
- `python3 eval_bugs.py markdown-deck` — no new matches.
- `python3 security_scan.py markdown-deck` — no new CRITICAL/HIGH.
- Manual code-trace verification: confirm `reorderSlideByIndex` is called by both paths with identical args; confirm Shift+V toggles the overlay; confirm grid card click routes through `goSlide`.
- Regression: existing thumbnail-strip drag reorder still works (same shared function).

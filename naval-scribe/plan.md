# Plan: Letter Status Tracker

## Goal
Add Draft→Signed→Transmitted→Replied status tracking to saved drafts, visible and editable directly in the Drafts drawer.

## Scope
**In scope:**
- Status field on each saved draft (4 values: Draft, Signed, Transmitted, Replied)
- Colored status badge in draft-item rows (click to advance through states)
- Backward-compatible: drafts without a `status` field default to "Draft"
- Filter row in Drafts drawer (All / Draft / Signed / Transmitted / Replied) to narrow the list

**Not in scope:**
- No new top-bar button
- No new drawer
- No date/timestamp per status transition
- No push notifications or reminder logic
- No status visible on the main preview page or in .docx export

## Approach

### Subtask 1 — CSS: add status badge and filter row styles
Four status colors embedded in the `<style>` block:
- Draft: `#555` (grey)
- Signed: `#d29922` (amber)
- Transmitted: `#0ff` (cyan, matching accent)
- Replied: `#3fb950` (green, matching `--color-success`)

Add `.status-badge` (small pill button) and `.status-filter-row` (flex row of filter buttons) styles.

### Subtask 2 — Data layer: `setDraftStatus()` helper, draft save update, and unique ID

**Unique ID generation (per BUGS IMPL-escalation 2026-04-23):** `Date.now()` as draft ID could theoretically collide if two saves land in the same millisecond. New `uniqueDraftId()` helper uses `crypto.randomUUID()` when available (all modern browsers), falls back to `Date.now() + '-' + Math.random().toString(36).slice(2,10)` for older environments. UUIDs carry 122 bits of randomness — collision probability negligible even with millions of drafts. Existing numeric IDs from legacy drafts continue to work via the strict-equality lookup path.

The `saveDraftBtn` click handler always creates a **new draft** (via `uniqueDraftId()` + `arr.unshift`). There is no "update existing draft" path. Therefore `status: 'draft'` is always correct for a newly created draft — the first save of any document is always in Draft state, regardless of the current form's contents.

New helper `setDraftStatus(id, newStatus)`: reads drafts array, finds entry by `id` via `.find()`.

**Per BUGS PLAN-escalation (2026-04-23): explicit id-not-found guard.** If `.find()` returns `undefined`, set module-scoped `lastStatusError = 'not-found'` and return `false` immediately — do NOT proceed to mutate (which would throw `TypeError: Cannot set property 'status' of undefined`) and do NOT surface the misleading "storage full" message.

If the id IS found, sets `.status`, writes back via `saveDraftsData`. If the write fails (localStorage full), `saveDraftsData` catches the error silently; `setDraftStatus` sets `lastStatusError = 'storage'` and returns `false`. On success returns `true` and clears `lastStatusError`.

Return value semantics:
- `true` — draft found, status updated, write succeeded
- `false` + `lastStatusError = 'not-found'` — id didn't match any saved draft (rare — usually means the draft was deleted in another tab)
- `false` + `lastStatusError = 'storage'` — draft found, write failed (localStorage quota)

### Subtask 3 — Error display for status change failures
In the drafts drawer HTML: add `<div id="drafts-status-err"></div>`. In the badge click handler: if `setDraftStatus` returns `false`, branch on `lastStatusError`:
- `'storage'` → "Could not save status — storage full."
- `'not-found'` → "Draft no longer exists — refresh the drawer."
- fallback → "Could not save status."

Clear the message after 2.5s. If success, render immediately.

### Subtask 4 — Render: extend `renderDraftsList()` with filter and badges
- Module-scoped `var statusFilter = 'all'` variable.
- Render filter row inside `#status-filter-row` at top of drawer.
- For each draft: append a `.status-badge` button after the meta line. Badge shows status label + `▶` suffix to signal clickability. `title="Click to advance status"`. `aria-label="Status: [Status] — click to advance"`. Clicking cycles states (draft→signed→transmitted→replied→draft) via `setDraftStatus`, then re-renders only if successful.
- Apply filter: skip items where `(draft.status || 'draft') !== statusFilter` when filter ≠ 'all'.
- Empty-after-filter message: "No [status] drafts."

### Subtask 5 — HTML: add placeholders in drafts-drawer
Add `<div id="status-filter-row" class="status-filter-row"></div>` and `<div id="drafts-status-err"></div>` inside `#drafts-drawer`, above `#drafts-list`.

### Subtask 6 — Update `#ai-prompt-content` discoverability block
Per the naval-scribe KEEP rule "AI prompt updated on every feature tock" (auto-downgraded LESSONS advisory on this PLAN gate, acknowledged and addressed): add a section to the `#ai-prompt-content` block in `index.html` documenting the Letter Status Tracker feature. Include:
- The 4 status values (Draft, Signed, Transmitted, Replied) and their colors
- How to interact: click the status badge on any saved draft to advance through states
- Filter row usage: click a filter button (All / Draft / Signed / Transmitted / Replied) to narrow the list
- Persistence: status saves to localStorage alongside the draft data; backward-compatible (drafts without `status` default to Draft)

This is a single-paragraph addition to the existing prompt block. Independent of other subtasks.

### Sequencing
Subtasks 1+2+5+6 are independent; Subtask 3 depends on 2; Subtask 4 depends on 1+2+3+5.

## File Layout
- `naval-scribe/index.html` — only file modified
  - CSS block (~line 12–350): +~30 lines for badge and filter styles
  - HTML `#drafts-drawer` (~line 388–395): +2 lines for `#status-filter-row` and `#drafts-status-err`
  - HTML `#ai-prompt-content` block: +~6 lines documenting the Letter Status Tracker feature (per LESSONS advisory fix)
  - JS draft save handler (~line 2384–2394): +1 line for `status: 'draft'`
  - JS draft section (~line 2252–2394): +`statusFilter` + `lastStatusError` module vars, +`setDraftStatus()` with id-not-found guard, modified `renderDraftsList()` (~40 net lines)

## Function Map
| File | Function | Change |
|---|---|---|
| `naval-scribe/index.html` | `setDraftStatus(id, newStatus)` | **Added** — reads drafts, updates status by id, writes back; returns bool success |
| `naval-scribe/index.html` | `renderDraftsList()` | **Modified** — adds filter row render + per-draft status badge with error feedback |
| `naval-scribe/index.html` | `saveDraftBtn` click handler | **Modified** — adds `status: 'draft'` to new draft object |

## Security
- Status values come from a hardcoded 4-element array; no user input enters the status field. No injection surface.
- Badge label derived from hardcoded array, not user data.
- localStorage is same-origin only; no new trust boundary introduced.
- All existing user-visible strings still routed through `esc()`.

## UI
- **Status badge**: small pill button on each draft row. Color matches status. Shows status label + `▶` to indicate clickability. `title="Click to advance status"`. `aria-label="Status: [Status] — click to advance"`. Click advances one step in the 4-state cycle.
- **Filter row**: five compact buttons (All, Draft, Signed, Transmitted, Replied) above the draft list. Active filter has accent border.
- **Empty after filter**: "No [status] drafts." replaces the generic empty message.
- **Error state**: inline "Could not save status — storage full." message in drawer, auto-clears after 2.5s.

## Guide
- Badge labels (title-case): Draft, Signed, Transmitted, Replied
- Badge suffix: `▶` (Unicode U+25B6)
- Filter button labels: All, Draft, Signed, Transmitted, Replied
- Badge aria-label pattern: `"Status: Signed — click to advance"`
- Error message: "Could not save status — storage full."

## Edge Cases
- Draft with no `status` field (legacy save): treated as 'draft' via `|| 'draft'` default everywhere.
- `setDraftStatus` localStorage failure: returns `false`; drawer shows inline error; badge does NOT advance visually (re-render reads real state from storage).
- Filter = 'signed', all signed drafts deleted: shows "No signed drafts."; filter stays on 'signed'.
- Max 25 drafts enforced by existing save handler — unchanged.
- `saveDraftBtn` always creates a new draft (new `Date.now()` id) — `status: 'draft'` is always the correct initial state.

## Test Strategy
1. Save a new draft → verify `status: 'draft'` in localStorage JSON.
2. Open drafts drawer → filter row renders; "All" button active by default.
3. Click badge on a Draft draft → shows Signed ▶; again → Transmitted ▶; again → Replied ▶; again → Draft ▶.
4. Set filter to Signed → only signed drafts visible.
5. Filter set to Transmitted with zero matches → "No transmitted drafts." message shown.
6. Legacy draft (no `status` field in localStorage) → displays as "Draft ▶" badge.
7. `test_project.py` passes.

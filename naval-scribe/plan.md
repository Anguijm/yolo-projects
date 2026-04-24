# Plan: Template Letter Library

## Goal
Add a "templates" button to the naval-scribe top bar that opens a drawer listing 12 pre-built letter templates in 4 categories; clicking a template fills the entire form with pre-populated type, subject, and body content.

## Scope
**In scope:**
- A `templates` button in the top bar (after `import`, before `chain`)
- A `#tmpl-drawer` sliding panel listing 12 templates in 4 categories (Personnel, Administrative, Operations, Policy & Instructions)
- Each template pre-populates: type, subject, body (and bodyBullets/bodyAction/bluf/recommendation for relevant types)
- Confirmation gate when the form has existing content (inline confirm/cancel row in the drawer, not a browser confirm() dialog)
- Mutual exclusion: opening templates closes other drawers (drafts, import, chain, addr, reply)
- AI prompt section updated with Template Library documentation

**NOT in scope:**
- Saving custom templates to localStorage
- Editing template content before applying
- Per-template SSIC or From/To pre-fill (too command-specific; users fill those themselves)
- Mobile-only redesign (drawer follows existing responsive pattern: full width under 768px)

## Approach

### Subtask 1 — CSS
Add `#tmpl-drawer` CSS block (copy structure from `#reply-drawer`). Add `.tmpl-cat` (category header) and `.tmpl-item` (template button) styles. Position follows the same fixed-left-panel drawer pattern.

### Subtask 2 — HTML
Add `<button class="btn" id="tmpl-btn" aria-label="Open template letter library">templates</button>` in the top bar between `import-btn` and `chain-btn`.

Add `<div id="tmpl-drawer">` before `#form-panel`, with:
- Header row: "Template Library" label + close button
- Description hint
- Confirmation row `#tmpl-confirm-row` (hidden by default): "This will overwrite the current form." + [apply template] + [cancel] buttons
- Template list area `#tmpl-list` (rendered by JS)

### Subtask 3 — JS data: TEMPLATE_LIBRARY
Define a `TEMPLATE_LIBRARY` array of 12 template objects. Each object:
```
{ cat, label, desc, state: { type, fields: {subj, body?, bodyBullets?, bodyAction?, bluf?, recommendation?} } }
```
Categories and templates:
- **Personnel** (3): Leave Request, Commendation Recommendation, Personnel Action Request
- **Administrative** (3): Appointment Memorandum, Meeting Minutes Forwarding, After-Action Report
- **Operations** (3): Status Report, Request for Information, Non-Concurrence
- **Policy & Instructions** (3): Point Paper, Action Memo, Instruction Template

### Subtask 4 — JS: renderTmplDrawer()
Render the 12 template buttons grouped by category into `#tmpl-list`. Each `.tmpl-item` button shows label (large) + desc (small). Event listener calls `selectTemplate(tpl)`.

### Subtask 5 — JS: selectTemplate(tpl) and applyTemplate(tpl)
`selectTemplate(tpl)` checks if any key form field has content (from, to, subj, body, bodyAction, bodyBullets, bodyMoa). If yes, store `pendingTemplate = tpl` and show `#tmpl-confirm-row`. If no, call `applyTemplate(tpl)` directly.

`applyTemplate(tpl)` clears all form fields (sets each input to empty, clears multi-fields, resets type to 'letter') then calls `restoreFullState(tpl.state)`, then sets `pendingTemplate = null`, hides `#tmpl-confirm-row`, and closes the drawer.

### Subtask 6 — JS: drawer toggle and mutual exclusion
`tmplBtn` click handler: toggle drawer. If opening, close draftsDrawer, importDrawer, chainDrawer, addrDrawer, replyDrawer. Call `renderTmplDrawer()` once on first open (memoized with `tmplRendered` flag).

Close button and cancel button both hide `#tmpl-confirm-row`, set `pendingTemplate = null`, and close/cancel appropriately. `applyTemplate()` also sets `pendingTemplate = null` after applying.

### Subtask 7 — AI prompt update
Add a `### Template Letter Library` section to the `#ai-prompt-content` element describing the 12 templates and how to use them.

### Subtask 8 — Sequencing
CSS → HTML (drawer + button) → TEMPLATE_LIBRARY data → renderTmplDrawer → selectTemplate + applyTemplate → toggle/mutual exclusion → AI prompt

## File Layout
- `naval-scribe/index.html` — sole file modified
  - `<style>` block: add ~30 lines (drawer CSS + `.tmpl-cat` + `.tmpl-item`)
  - `<body>`: add `#tmpl-btn` button (1 line) and `#tmpl-drawer` HTML (~25 lines)
  - `<script>`: add `TEMPLATE_LIBRARY` data (~80 lines), `renderTmplDrawer()` (~25 lines), `selectTemplate()`/`applyTemplate()` (~25 lines), drawer toggle (~20 lines)
  - `#ai-prompt-content`: add Template Library section (~15 lines)
  - Net addition: ~220 lines to a 4116-line file

## Function Map
**naval-scribe/index.html (new functions):**
- `renderTmplDrawer()` — builds and injects HTML for all 12 template buttons into `#tmpl-list`; called once on first open
- `selectTemplate(tpl)` — checks form emptiness; if content present, shows confirm row with pending template; if empty, calls applyTemplate directly
- `applyTemplate(tpl)` — clears all form fields then calls `restoreFullState(tpl.state)`, closes drawer

**Modified behavior (not new functions):**
- `tmplBtn` click handler (inline event listener) — drawer toggle + mutual exclusion

## Security
- All template strings are author-controlled literal JavaScript strings — no external data, no user input in the template definitions
- Template content is passed to `restoreFullState()` which populates form inputs via `.value =` assignment, not `innerHTML` — no XSS surface
- The confirm row uses `textContent` assignment not `innerHTML`
- No new localStorage keys, no new network calls, no new trust boundaries
- CSP unchanged: `unsafe-inline` already allows inline scripts per Constraint 1; `connect-src 'none'` ensures no external requests
- Template field values flow through `esc()` in `updatePreview()` before any `innerHTML` rendering — same path as all other form fields

## UI
- `templates` button in top bar: same `.btn` class, between `import` and `chain`
- Drawer: fixed left panel (420px, full-width on mobile), same style as `#reply-drawer`
- Templates grouped by category. Category header as small-caps label (`.tmpl-cat`). Template buttons as full-width `.tmpl-item` rows showing label + desc in smaller text
- Confirmation row: hidden until user clicks a template while form has content. Amber warning text + "apply template" (primary) and "cancel" (secondary) buttons
- Empty form state: template applies immediately, no confirmation
- Loading a template closes the drawer after apply
- Tap targets: `.tmpl-item` min-height 44px for mobile touch

## Guide
- Button label: "templates"
- Button aria-label: "Open template letter library"
- Drawer header: "Template Library"
- Drawer hint: "Select a template to pre-fill the form. Edit fields after loading."
- Confirmation text: "This will overwrite the current form."
- Confirm button label: "apply template"
- Cancel button label: "cancel"
- Category labels: "Personnel", "Administrative", "Operations", "Policy & Instructions"
- Template labels (12): Leave Request, Commendation Rec, Personnel Action, Appt Memorandum, Meeting Minutes, After-Action Report, Status Report, Request for Info, Non-Concurrence, Point Paper, Action Memo, Instruction Template

## Edge Cases
- Form has content → confirm row shown before applying (no destructive overwrite without confirmation)
- Form is empty → template applies immediately
- User opens templates, then opens another drawer → templates drawer closes (mutual exclusion handled symmetrically)
- Template type is `pointpaper` or `actionmemo` — `applyTemplate` calls `restoreFullState` which sets the correct type; `updateFieldVisibility()` called inside `restoreFullState` ensures the right body field is shown
- User clicks template, sees confirm row, then clicks close or cancel → `pendingTemplate = null`, confirm row hidden, form unchanged
- After `applyTemplate` runs successfully → `pendingTemplate = null`, confirm row hidden, drawer closed
- `applyTemplate` clears all fields first (like new-btn) so partial template state leaves other fields empty rather than keeping stale content

## Test Strategy
1. `python3 test_project.py naval-scribe` must PASS after implementation
2. "templates" button appears in top bar between `import` and `chain`
3. Click templates → drawer opens; other open drawers close
4. Drawer renders 12 template buttons in 4 categories with labels and descriptions
5. Empty form: click "Leave Request" → type=letter, subject filled, body filled; drawer closes
6. Non-empty form: fill any field, open templates, click a template → confirm row appears; click "apply template" → form fills and drawer closes; click "cancel" → form unchanged
7. All 12 templates apply without JS error
8. Mobile viewport (375px): drawer spans full width
9. Close button closes drawer, clears pending template
10. AI prompt updated: "Template Library" section visible in the prompt text

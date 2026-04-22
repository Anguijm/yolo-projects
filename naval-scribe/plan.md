# Reply Draft Auto-Fill — Tock Plan

## Goal
One-click generation of a reply draft with From/To swapped, today's date, original letter as reference (a), and a boilerplate body opener — all within a lightweight preview drawer.

## Scope

**In scope:**
- "reply" button added to top-bar controls
- `#reply-drawer` (same fixed-left panel pattern as import/chain/addr drawers)
- Drawer shows from→to swap preview and generated reference line before user commits
- "Fill Reply Draft" button applies changes: swap From/To, today's date, original as Ref (a), boilerplate body, clear Via/Encl/CopyTo/Sig
- Drawer mutual exclusion (closes all other drawers when reply opens; reply closes when other drawers open)
- Type is reset to "letter" (replies are standard naval letters)
- SSIC and Subject preserved from original

**Not in scope:**
- Via chain reversal (too situational — same chain may not apply; user adjusts manually)
- Reference line formatting beyond "From ltr SSIC of Date" pattern
- Saving the prefill state to localStorage
- Any DOCX changes
- Support for non-letter types as reply target (reply is always a letter)

## Approach

### Subtask 1: HTML additions
Add `#reply-drawer` div after `#addr-drawer`. Structure mirrors import-drawer: close button, preview section (from/to swap display + ref line), warning div (if From/To are empty), and "Fill Reply Draft" button.

Add `<button class="btn" id="reply-btn" aria-label="Generate reply draft with From/To swapped">reply</button>` in top-bar controls between `addr-btn` and `print-btn`. The `aria-label` is included at the HTML layer per the naval-scribe learning: static HTML buttons alongside JS-generated siblings must carry aria-labels at the HTML layer (not just via JS). This addresses the auto-downgraded LESSONS advisory on PLAN escalation.

**No sequencing dependency** — HTML can be written in one pass.

### Subtask 2: CSS additions
Add `#reply-drawer` style block (identical geometry to `#addr-drawer`). Add `.reply-preview-row` for the swap display rows (label + value, two-column grid). Add `.reply-warn` for the empty-field warning.

**Depends on:** Subtask 1 HTML structure being defined.

### Subtask 3: JS — generateReplyDraft()
New function `generateReplyDraft()`:
1. Capture `origFrom`, `origTo`, `origSsic`, `origDate` from current form fields
2. Build `refLine`: `origFrom + ' ltr ' + origSsic + ' of ' + origDate` (fallback to shorter forms if SSIC or date missing)
3. Apply to form: `F.from.value = origTo`, `F.to.value = origFrom`, `F.date.value = todayNaval()`, keep SSIC + subject
4. `viaFields.setValues([])`, `enclFields.setValues([])`, `copyToFields.setValues([])`
5. `distCheck.checked = false`
6. `refFields.setValues(refLine ? [refLine] : [])` 
7. `F.body.value = refLine ? 'Per reference (a), ' : ''`
8. Clear sig: `F.sigName.value = F.sigRank.value = F.sigTitle.value = ''`
9. `typeSelect.value = 'letter'`; `updateFieldVisibility()`; `updatePreview()`

### Subtask 4: JS — drawer UI wiring
- `replyBtn.addEventListener('click', ...)` — closes other 4 drawers, populates preview rows in drawer, opens reply drawer
- `replyCloseBtn.addEventListener('click', ...)` — closes reply drawer
- `replyFillBtn.addEventListener('click', ...)` — calls `generateReplyDraft()`, closes drawer, flash feedback
- 4× existing drawer btn listeners: each gets `replyDrawer.classList.remove('open')` appended (same pattern as addrDrawer mutual exclusion)
- `addrBtn.addEventListener(...) { replyDrawer.classList.remove('open'); }` — add reply to addr's list

**Depends on:** Subtask 3 function defined first.

### Subtask 5: Populate drawer preview on open
When `replyBtn` is clicked, before opening the drawer:
- Read current From/To/SSIC/Date, and `viaFields.getValues()`
- Inject into `#reply-from-preview`, `#reply-to-preview`, `#reply-ref-preview` spans using `.textContent` (not innerHTML)
- If From or To is empty, show `#reply-warn` with warning text; hide "Fill" button
- Otherwise hide `#reply-warn`; show "Fill" button
- If the original letter has Via entries (`viaFields.getValues().length > 0`), show `#reply-via-warn`: "Via chain cleared — reverse the chain manually if required for correct routing." This warning is always visible in the drawer when Via is non-empty, so the user is informed before they commit.

## File Layout

| File | Change | Lines |
|------|--------|-------|
| `naval-scribe/index.html` | Add CSS (~20 lines), HTML (~30 lines), JS (~80 lines) | ~130 net new lines; touches ~3809→~3939 |

## Function Map

**File: naval-scribe/index.html**

| Function | Action | Notes |
|----------|--------|-------|
| `generateReplyDraft()` | NEW | Core reply logic: swap fields, build ref, set boilerplate |
| `replyBtn` click handler | NEW | Opens drawer, populates preview (incl. via-warn if Via non-empty) |
| `replyCloseBtn` click handler | NEW | Closes drawer |
| `replyFillBtn` click handler | NEW | Calls `generateReplyDraft()`, closes drawer |
| Existing drawer open handlers (draftsBtn, importBtn, chainBtn, addrBtn) | MODIFIED | Each gets +1 line: `replyDrawer.classList.remove('open')` |

## Security

- `generateReplyDraft()` reads only existing form field values (`F.from.value`, `F.to.value`, `F.ssic.value`, `F.date.value`) — all previously user-entered, already in the DOM, no new attack surface
- **Preview rows use `.textContent` (not `innerHTML`)** when populating `#reply-from-preview`, `#reply-to-preview`, `#reply-ref-preview`, `#reply-via-warn` — no XSS vector in preview rendering
- **`refFields.setValues()` XSS analysis**: `makeMultiField.setValues()` calls `addItems()` internally (see line ~734). `addItems()` creates `<input>` elements and sets their value via `input.value = val` (DOM property assignment, not `innerHTML`). `input.value` is a safe plain-text setter — there is no HTML parsing, so `refLine` does NOT need to be passed through `esc()`. The value is only rendered in the input's value attribute by the browser, not as markup.
- **Via warning text** uses `.textContent` (static string literal, not user data)
- No new localStorage writes; no new network calls; no new `innerHTML` with user data
- CSP unchanged: `unsafe-inline` is the existing architectural decision per CONSTRAINTS.md (SECURITY should not re-litigate this)
- Trust boundary: all values flow through existing form fields before the reply function reads them

## UI

**Interaction flow:**
1. User has a letter form filled (From, To, SSIC, Date, Subj at minimum)
2. Clicks "reply" button in top bar
3. Reply drawer opens from left panel, other drawers close
4. Drawer shows (per UI+GUIDE critique on PLAN escalation — full disclosure of what changes):
   - **Will change** section:
     - "From: [current To]" — clearly labeled swap preview
     - "To: [current From]" — clearly labeled swap preview
     - "Date: [today in DD Mon YYYY]" — auto-set
     - "Ref (a): [From] ltr [SSIC] of [Date]" — generated reference string
     - "Body (will REPLACE existing): Per reference (a), " — explicit overwrite warning
     - "Type: letter (auto-set)" — explicit even if current type is already letter
   - **Will clear** section — always visible, lists every field that gets emptied:
     - "Enclosures: cleared"
     - "Copy To: cleared"
     - "Distribution checkbox: unchecked"
     - "Signature: cleared (name, rank, title)"
     - "Via chain: cleared — reverse manually if routing requires it" (only shown when Via has content; bolded)
   - **Will keep** section (reassurance):
     - "SSIC, Subject"
5. "Fill Reply Draft" button at bottom
6. User clicks → form is filled, drawer closes, preview updates

**Empty/loading/error states:**
- If From or To is empty when reply drawer opens: show warning "Fill in From and To fields first."; hide "Fill Reply Draft" button
- If original letter had a Via chain: show `#reply-via-warn` advisory "Via chain cleared — reverse the chain manually if required for correct routing." This is always visible when Via is non-empty, ensuring the user is informed before committing.
- If SSIC or Date is missing: ref line degrades gracefully (omits missing parts), still functional
- No loading state (all synchronous)
- Drawer mutual exclusion: reply drawer closes all others on open

**Flash feedback:** "Fill Reply Draft" button text changes to "draft filled ✓" for 1.5s after apply (same pattern as "save draft" button).

## Guide

**Button label:** "reply" (matches existing btn labels: "import", "chain", "addr book" — all lowercase, terse)

**Drawer title:** "Reply Draft"

**Preview sections** (reply drawer, from top to bottom):
- **"WILL CHANGE"** header — items that get new values:
  - "FROM →" and "TO →" (uppercase, with arrow indicating direction)
  - "DATE →" (today's date)
  - "REF (a):" for the reference line
  - "BODY (replaces existing):" — explicit overwrite warning in bold
  - "TYPE → letter" (auto-set)
- **"WILL CLEAR"** header — items that get emptied:
  - "Enclosures, Copy To, Distribution checkbox, Signature" (always)
  - "Via chain — reverse manually if needed" (only if Via has content, in warning color)
- **"WILL KEEP"** header — items preserved:
  - "SSIC, Subject"

**Warning text (if From/To empty):** "Fill in From and To fields first."

**Fill button:** "fill reply draft"

**Success feedback:** "draft filled ✓"

## Edge Cases

| Case | Handling |
|------|----------|
| From is empty | Show warning, hide Fill button |
| To is empty | Show warning, hide Fill button |
| Both empty | Same warning |
| SSIC missing | Ref line: "From ltr of Date" (omit SSIC) |
| Date missing | Ref line: "From ltr SSIC" (omit date) |
| Both missing | Ref line: "From letter" |
| From and To are the same value | Swap still happens (degenerate case, user adjusts) |
| Long From/To values | Preview rows use `overflow: hidden; text-overflow: ellipsis` |
| Body has existing content | **Replaced, but drawer preview explicitly shows "BODY (will REPLACE existing):" before user clicks Fill — per UI+GUIDE critique on PLAN escalation.** No silent overwrite; user consent is informed. |
| Original letter has Via chain | `#reply-via-warn` shown in drawer: "Via chain cleared — reverse the chain manually if required for correct routing." User informed before Fill. |
| User clicks reply then close (no fill) | No change to form — drawer is preview-only until Fill is clicked |
| Instruction / SOP type | Reply is set to "letter" regardless; user can change type after |

## Test Strategy

1. **Unit: generateReplyDraft() field swap** — Fill From="A", To="B", SSIC="5216", Date="22 Apr 2026"; click reply → Fill; verify `F.from.value === "B"`, `F.to.value === "A"`
2. **Unit: ref line generation** — From="CO, USS EXAMPLE", SSIC="5216", Date="22 Apr 2026" → ref = "CO, USS EXAMPLE ltr 5216 of 22 Apr 2026"
3. **Unit: ref line degradation** — SSIC empty → "CO, USS EXAMPLE ltr of 22 Apr 2026"; Date empty → "CO, USS EXAMPLE ltr 5216"; both empty → "CO, USS EXAMPLE letter"
4. **Unit: body boilerplate** — After fill, body textarea starts with "Per reference (a), "
5. **Unit: fields cleared** — After fill: Via=[], Encl=[], CopyTo=[], distCheck=false, sigName/Rank/Title=""
6. **Unit: type reset** — After fill, `typeSelect.value === "letter"`
7. **Unit: SSIC + Subject preserved** — SSIC and Subj values unchanged after fill
8. **UI: empty From warning** — Clear From, click reply → drawer shows warning, Fill button hidden
9. **UI: drawer mutual exclusion** — Open drafts drawer, click reply → drafts closes, reply opens
10. **test_project.py** — Must pass (file loads, no JS errors in static analysis)

# Plan: Distribution / Copy-To Block (v2)

## Goal
Convert the single-line "Copy To" textarea into a multi-entry list with a "Distribution" mode toggle. When Distribution is checked, the label becomes "Distribution:" (standard for Naval Instructions); otherwise "Copy to:". Also auto-detects "Distribution:" during import.

## Scope
- naval-scribe/index.html only
- No new files

## Approach

### HTML Changes
1. Replace `<textarea id="f-copyto" rows="3">` with:
   - Header row: Distribution checkbox FIRST (above the list), with hint "For Naval Instructions — replaces Copy to: with Distribution: block"
   - `<div id="copyto-list"></div>` — multi-field container
   - `<button class="add-btn" id="add-copyto">+ add recipient</button>`
2. Distribution toggle layout: `<label class="dist-toggle"><input type="checkbox" id="f-dist-check"> distribution mode</label>` placed as the first element in the field, above the list — so user sees the context before adding entries.
3. Remove `copyTo` from the `F` object (no longer a DOM element reference).

### JS Changes

1. **New multi-field**: `var copyToFields = makeMultiField('copyto-list', 'add-copyto', 'copyto')` after enclFields
2. **Dist checkbox**: `var distCheck = document.getElementById('f-dist-check')` + `distCheck.addEventListener('change', updatePreview)`
3. **getFormData()**: replace textarea read with `copyTo: copyToFields.getValues(), distribution: distCheck.checked`
4. **renderCopyTo()** (preview): label = `d.distribution ? 'Distribution:' : 'Copy to:'`. All values go through existing `esc()` — no new XSS surface.
5. **dCopyTo()** (main DOCX builder): same label logic; existing XML escaping via `makeParagraph()` handles injection.
6. **dxCopyTo()** (chain DOCX builder): same label logic.
7. **newBtn handler**: remove 'copyTo' from the F-keys array; add `copyToFields.setValues([]); distCheck.checked = false;`
8. **autoSave()**: change `copyTo: F.copyTo.value` → `copyTo: copyToFields.getValues(), distribution: distCheck.checked`
9. **restoreFullState()**: remove copyTo from the FM map; add explicit calls:
   - `copyToFields.setValues(typeof s.copyTo === 'string' ? s.copyTo.split('\n').filter(Boolean) : (Array.isArray(s.copyTo) ? s.copyTo : []))`
   - `distCheck.checked = !!(s.distribution)`
10. **Shortcut restore** (line ~1274): same migration logic as above for `state.copyTo`
11. **Import apply**: `copyToFields.setValues(p.copyTo)` replaces `F.copyTo.value = p.copyTo.join('\n')`
12. **Import parser**: also detect "Distribution:" heading (in addition to "Copy to:") as a trigger for `inCopy = true; distCheck.checked = true`
13. **Chain DOCX getFormDataForChain()**: `copyTo: f.copyTo || [], distribution: !!(f.distribution)`

### Security note
All copyTo values rendered to DOM pass through the existing `esc()` function. Values written to DOCX XML pass through `makeParagraph()` which uses text node construction. `makeMultiField` inserts values via `input.value` (safe). No new XSS or XML injection surface is introduced.

### Migration compatibility
Old localStorage saves store `copyTo` as a raw string. New restore logic detects `typeof === 'string'` and splits on '\n', preserving all existing data without loss.

### Signature move (COOL fix)
When switching to Distribution mode, the preview renders the recipients as an indented block under a bold "Distribution:" heading — visually distinct from "Copy to:". This matches actual DON instruction formatting where Distribution is a standalone section, not inline with the rest of the letter.

## File Layout
- naval-scribe/index.html (all changes in one file)

## Test Strategy
- `python3 test_project.py naval-scribe` — syntax, ID, event listener checks
- Verify label switches between "Copy to:" and "Distribution:" in preview
- Verify multi-entry add/remove works, preview updates live
- Verify old draft strings migrate without data loss
- Verify import detects both "Copy to:" and "Distribution:" headings
- Verify Distribution state saves/restores from localStorage

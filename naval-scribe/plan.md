# Naval Scribe — Letter Quality Checker + Portable Draft Export/Import

## Goal
Add a "check" button that opens a drawer running 7 naval formatting rules against the current form (advisory only), plus "export draft" / "import draft" buttons for portable `.navalscribe.json` backup/transfer with strict schema validation on import.

## Scope

**In scope:**
- Letter Quality Checker: new `#quality-drawer` with 7 checks, `check` button in top bar
- Portable Draft Export: `export draft` button triggers immediate `.navalscribe.json` download
- Portable Draft Import: `import draft` button triggers hidden file picker; JSON validated (whitelist + type-check) before `restoreFullState`

**Explicitly out of scope:**
- Blocking export when checks fail (advisory only — zero friction)
- Server-side storage or sync (CONSTRAINTS.md Constraint 3: localStorage only)
- Any change to the `.docx` export path
- Modifying existing `getFullState` or `restoreFullState` signatures
- Auto-run of quality check on every keystroke (on-open only, with a re-check button)

## Approach

**Subtask 1 — CSS (no dependencies)**
Add styles for:
- `#quality-drawer` — same fixed-left-420px pattern as all existing drawers
- `.qc-item` — row layout: status icon + rule name + note
- `.qc-pass` / `.qc-fail` — green ✓ / red ✗ styling
- `#draft-io-msg` — small inline feedback span in top-bar area for import/export status

**Subtask 2 — HTML (depends on Subtask 1)**
Add to `<div id="top-bar">`:
- `<button id="quality-btn">check</button>` (before `print-btn`)
- `<button id="export-draft-btn">export draft</button>` (after `routing-btn`)
- `<button id="import-draft-btn">import draft</button>` (after `export-draft-btn`)
- `<input type="file" id="import-draft-file" accept=".json" style="display:none">`

Add `#quality-drawer` HTML block (before `#autosave-err`):
- Close button, intro text, `<div id="quality-results">` container
- "re-check" button to re-run without closing

**Subtask 3 — Quality checker JS (depends on Subtask 2)**
`function runQualityChecks()` — reads current form state, returns `[{label, pass, note}, …]`. Throughout, "non-empty" means **`String(value || '').trim().length > 0`** (consistent across all checks; trims whitespace before length check):

1. **Date Format** — `F.date.value` matches `/^\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}$/i` (skip check for pointpaper/actionmemo/moa which don't show date field)
2. **SSIC Pattern** — `F.ssic.value` matches `/^\d{4,5}$/` (skip for types without SSIC: pointpaper/actionmemo/moa)
3. **Subject Non-Empty and Length** — `F.subj.value.trim().length > 0` AND ≤ 80 chars; if > 80 fail with "Subject exceeds 80 characters — consider abbreviating"
4. **From and To Filled** — `F.from.value.trim().length > 0` AND `F.to.value.trim().length > 0` (skip for pointpaper/actionmemo/moa which use different header)
5. **Body Para 1 Numbering** — for letter/memo/endorsement/business/instruction/sop: paragraphs split by **`F.body.value.split(/\n\s*\n+/)`** (one or more blank lines, allowing trailing whitespace). If `paragraphs.filter(p => p.trim().length > 0).length >= 2`, the first non-empty paragraph's `.trimStart()` MUST begin with the literal 4-character prefix `"1.  "` (digit `1`, period, two spaces — naval letter convention) to pass; the looser `/^1\.\s/` regex is also accepted (single space) for users who haven't typed the canonical double-space yet. Single-paragraph or empty bodies pass always.
6. **Signature Block** — for types with a sig block (letter/memo/endorsement/business/actionmemo/instruction/sop): `F.sigName.value.trim().length > 0` AND `F.sigRank.value.trim().length > 0`
7. **Classification Marking** — failure condition is exactly **`!classSel.value || classSel.value === '' || classSel.value === 'No Marking'`**; if any of those, advisory note "Consider setting classification marking" (advisory does not flip overall pass count for this rule — it always counts as informational, never blocks).

`function renderQualityPanel()` — clears `#quality-results` and injects one `.qc-item` per check; drawer shows summary line "N/7 checks passed" at top.

Quality drawer open/close + mutual exclusion with all existing drawers (same pattern as routing-drawer).

**Subtask 4 — Portable Export/Import JS (no dependency on Subtask 3)**
`function exportDraft()`:
- Calls `getFullState()`
- Adds `_navalscribe_version: "1"` and `_navalscribe_exported_at: new Date().toISOString()`
- `JSON.stringify(state)` → Blob → download link → click → revoke
- Filename: `naval_draft_<YYYYMMDD>.navalscribe.json`

`function validateImportSchema(obj)`:
- Returns `{valid: bool, sanitized: obj, errors: []}`
- Checks `obj` is a plain object (not null, not array)
- Checks for `_navalscribe_version` key (rejects file without it: "Not a Naval Scribe draft file")
- Checks that `_navalscribe_version === "1"` (the current schema version); rejects files with a different version value with "Unsupported draft version — cannot import"
- Whitelisted top-level keys: `type, classification, fields, copyTo, distribution, via, refs, encls, parties, routing, _navalscribe_version, _navalscribe_exported_at`
- Any key not in whitelist → stripped (silent)
- Type checks: `type` string, `classification` string, `fields` object, `copyTo` array-or-undefined, `distribution` boolean-or-undefined, `via` array, `refs` array, `encls` array, `parties` array, `routing` object-or-undefined
- Type mismatch → strip key, add to errors

`importDraftBtn.click` → triggers `importDraftFile.click()`
`importDraftFile.change` → FileReader → JSON.parse → `validateImportSchema` → if valid call `restoreFullState(sanitized)` → show success/error in `#draft-io-msg` (auto-clears after 4s)

**Status-message safety (XSS prevention):** All writes to `#draft-io-msg` MUST use `.textContent` assignment, never `.innerHTML`. Error strings may contain user-controlled content (e.g., schema-validator messages naming a stripped key like `"Stripped unknown key: foo<script>"`); `.textContent` ensures any such content renders as inert text rather than executing as DOM. The success path also uses `.textContent` for consistency. No `esc()` call needed because `.textContent` is the strongest guarantee — the browser will not interpret HTML in the assigned string at all. This is documented as a planning constraint so the implementation reviewer can grep for `draft-io-msg.innerHTML` and reject the patch if it appears.

**Schema discoverability:** Add a `<details><summary>SUPPORTED FORMAT</summary>` block adjacent to the import button (or inside `#draft-io-msg`'s container) listing the `.navalscribe.json` schema requirements: required `_navalscribe_version: "1"` envelope, the whitelisted top-level keys (`type, classification, fields, copyTo, distribution, via, refs, encls, parties, routing, _navalscribe_version, _navalscribe_exported_at`), and each key's expected type. This satisfies the `<details>` supported-formats KEEP rule from learnings.md and pre-empts the recurring GUIDE objection that bulk-input features lack discoverable format docs.

## File Layout

**`naval-scribe/index.html`** (sole file modified)
- CSS section (~line 498 end of `</style>`): insert `#quality-drawer` + `.qc-*` styles + `#draft-io-msg` style (~40 lines)
- HTML `#top-bar` buttons (~line 530 area): insert `quality-btn`, `export-draft-btn`, `import-draft-btn`, hidden file input (~5 lines)
- HTML drawers section (~line 663, before `#autosave-err`): insert `#quality-drawer` block (~20 lines)
- JS section (~line 4367, before `loadSaved()`): insert ~170 lines of new JS (quality checks, export, import, drawer wiring)

## Function Map

**`naval-scribe/index.html`**

New functions added:
- `runQualityChecks()` — reads form, returns array of 7 check results `[{label, pass, note}]`
- `renderQualityPanel()` — clears and repopulates `#quality-results` div
- `exportDraft()` — builds JSON payload, triggers download as `.navalscribe.json`
- `validateImportSchema(obj)` — returns `{valid, sanitized, errors}` with whitelisted/type-checked copy
- *(anonymous)* `importDraftFile.addEventListener('change', …)` — FileReader → validate → restoreFullState

No existing functions are modified.

## Security

- Import path: all JSON is validated via `validateImportSchema` before any DOM writes; extra keys stripped, type mismatches stripped — no XSS vector via import payload
- `restoreFullState` already escapes via `esc()` before any `innerHTML` write — the existing escape chain covers imported data
- **Status messages**: all writes to `#draft-io-msg` use `.textContent` (never `.innerHTML`), so error messages naming user-controlled content (e.g., stripped key names from imported JSON) render as inert text. Implementation reviewers must reject any patch that writes `.innerHTML` to that element.
- Export: `JSON.stringify` of in-memory state only; no shell, no eval, no innerHTML
- File input: `accept=".json"` is a hint not enforcement; actual validation is JSON.parse + schema check in JS
- CSP: `connect-src 'none'` already blocks outbound — export/import is purely local blob/file, within existing constraints
- No new injection surface introduced; import validation + `.textContent` for status messages = defense in depth per roadmap requirement

## UI

- **Quality checker button**: "check" — compact, consistent with other top-bar buttons
- **Quality drawer**: left-side overlay (same as all drawers); close button top-right; intro "Advisory only — does not block export."; summary line "N/7 passed" in accent color; 7 rows each: icon (✓ or ✗) + rule name + note text; "re-check" button at bottom
- **Pass state**: icon `✓` in `var(--color-success)` (#3fb950 green); rule name in `var(--text-secondary)`; note in `var(--text-tertiary)`
- **Fail state**: icon `✗` in `#e05252` red; rule name in `var(--text-primary)`; note in `#e3b341` amber (highlights the issue)
- **Export draft button**: "export draft" — triggers immediate download, no modal
- **Import draft button**: "import draft" — triggers file picker, then shows 1-line status message `#draft-io-msg` that auto-clears
- **Import success**: "Draft imported." in green
- **Import error**: "Import failed: <reason>" in amber/red
- **Empty state**: quality drawer opened with no body content shows all checks that need content with their "not filled" notes

## Guide

- Quality drawer intro: "Advisory checks — does not block export."
- Re-check button label: "re-check"
- Check item labels (7): "Date Format", "SSIC Pattern", "Subject", "From / To", "Body Numbering", "Signature Block", "Classification"
- Export button: "export draft"
- Import button: "import draft"
- Import file filter: `.json` (user-visible)
- Import success message: "Draft imported."
- Import error prefix: "Import failed: "
- Draft-io status auto-clears after 4000ms

## Edge Cases

- **Quality checker opened on blank form**: all checks that require content will fail — expected, shows what needs to be filled
- **Single-paragraph body**: Body Numbering check passes (no "1." required by naval convention)
- **Type without SSIC/date field** (pointpaper, actionmemo, moa): corresponding checks are skipped (marked pass with "N/A for this type")
- **Import of non-JSON file**: JSON.parse throws → catch → show "Import failed: Not a valid JSON file"
- **Import of JSON without `_navalscribe_version`**: rejected with "Not a Naval Scribe draft file"
- **Import with extra keys**: extra keys stripped silently; import proceeds with valid keys only
- **Export filename collision**: browser handles via download dialog / auto-rename — no action needed
- **Subject > 80 chars**: quality check fails with note "Subject exceeds 80 characters"
- **Classification = "No Marking"**: quality check fails advisory with "Consider setting classification marking"
- **Mutual exclusion**: quality-drawer opens → all other drawers close; any other drawer opens → quality-drawer closes

## Test Strategy

1. `python3 test_project.py naval-scribe` — must pass (HTML/JS syntax, file existence)
2. Manual feature verification plan:
   - Open quality drawer on blank form → all 7 fail with appropriate notes
   - Fill all fields correctly → all 7 pass; "7/7 checks passed" shown
   - Fill date as "2 Apr 2026" → Date Format passes; fill as "April 2" → fails
   - Set SSIC to "5216" → passes; "abc" → fails
   - Fill 60-char subject → passes; 90-char subject → fails
   - Fill From/To → passes; clear From → fails
   - Two-paragraph body starting with "1." → passes; two-paragraph without "1." → fails
   - Fill sig name+rank → passes; clear one → fails
   - Set classification to UNCLASSIFIED → passes; set to No Marking → advisory fail
3. Export draft → file downloads as `.navalscribe.json`; contents are valid JSON with `_navalscribe_version` key
4. Import downloaded file → form restores correctly
5. Import arbitrary JSON without `_navalscribe_version` → "Not a Naval Scribe draft file" error
6. Import JSON with extra keys → extra keys stripped, rest restores correctly
7. Mutual exclusion: open quality drawer → other drawers closed; open drafts → quality drawer closes

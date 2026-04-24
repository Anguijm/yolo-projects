# Changes — fix-council-bugs-hallucination

## council.py

**Added constants** (after TOKEN_RE, ~line 43):
- `_HALLUCINATION_CLAIM_RE` — matches undefined/undeclared/not defined/does not exist/missing language
- `_SYMBOL_FROM_FIX_RE` — extracts backtick-quoted identifiers of 3+ chars
- `_FILE_REF_RE` — extracts file:line references from evidence field

**Added functions** (after check_goalpost_moves):
- `_symbol_defined_in_content(symbol, content, ext) -> bool` — language-specific definition-pattern check. `.html`/`.js`/`.ts` uses three patterns: (1) `function NAME`, (2) `(?:const|let|var) NAME =` (covers all three JS variable-declaration keywords), (3) line-anchored method shorthand `NAME(args) {`. `.py` uses `def NAME` / `class NAME` and line-anchored `NAME =` (module/class-level assignment). Unknown extensions return `False` (skip whole-file check).
- `detect_bugs_hallucination(verdict, project) -> bool` — two-layer check: (1) cited-line window ±5 lines around each file:NNN reference, (2) definition-pattern scan across whole file; returns True iff any cited file disproves the "undefined symbol" claim. Symbols are extracted only from the window BEFORE each claim keyword in the reason field (proximity filter) to avoid false positives from scope identifiers ("in `getFullState`") and fix alternatives ("replace with `setDraftStatus`").

**Modified main()** (after check_goalpost_moves call):
- Added Patch 4 loop that calls detect_bugs_hallucination on each verdict and auto-downgrades matching ones to APPROVE/advisory with `[AUTO-DOWNGRADED: hallucinated symbol claim, ...]` prefix

## experiments/fix-council-enforcement/test_enforcement.py

**Added imports**: `_symbol_defined_in_content`, `detect_bugs_hallucination`

**Added test classes**:
- `TestBugsHallucination` — 6 unit tests (downgrades when defined, preserves when absent, angle filter, verdict filter, phrasing filter, symbol-length filter)
- `TestBugsHallucinationFixtures` — 4 historical fixture replays:
  1. LST round 9 (F.id/F.status — dot-notation symbols too short, no downgrade)
  2. Template Lib round 1 (byDirectionChk/actingChk/restoreParties defined — downgrade)
  3. LST round 7 (cycleDraftStatus genuinely absent — no downgrade)
  4. infra-memory-feedback round 3 (no undefined phrasing — no downgrade)
- `TestSymbolDefinedInContent` — 7 layer-2 helper tests (JS function, const, method shorthand, call site, Python def, Python call site, unknown ext)

## Behavior changes

- BUGS OBJECTs using "undefined/missing" language AND citing 3+-char backtick symbols are now cross-checked against the cited files before blocking the build
- If any cited file disproves the claim (symbol found at cited line or via definition pattern), the OBJECT is auto-downgraded to APPROVE/advisory and logged to stderr
- Real BUGS objections (symbol genuinely absent, or no "undefined" phrasing, or no symbol citations) are unaffected

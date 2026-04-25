# Council Escalation — naval-scribe

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T05:55:12.981935+00:00

## Angle positions

### BUGS — OBJECT (medium)
- **Reason:** The import draft schema validation is shallow, only checking top-level container types for 'fields', 'parties', and 'routing' but not their nested contents, which contradicts 'strict schema validation' and could lead to runtime errors or malformed output if inner data is malformed.
- **Required fix:** Implement recursive schema validation within `validateImportSchema` for nested objects and arrays (e.g., `fields`, `parties` elements, `routing` properties) to ensure their internal structure and types conform to expectations.
- **Evidence:** `file:2250:5-2273:7`

### SECURITY — APPROVE (low)
- **Reason:** The application adheres to structural constraints, uses robust input escaping for rendering, and implements strict schema validation for draft imports. User-facing warnings for local storage are present as required.

### UI — APPROVE (low)
- **Reason:** The Letter Quality Checker and Portable Draft Export/Import features are well-implemented with clear feedback, consistent UI patterns, and good affordances.

### GUIDE — APPROVE (low)
- **Reason:** The tool provides comprehensive in-app documentation and hints for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** Both the quality checker and portable draft features provide essential utility for the target user, addressing real pain points in naval correspondence drafting and data management.
- **Evidence:** `The Letter Quality Checker automates adherence to complex naval formatting standards, a frequent and critical task for the target audience. The Portable Draft Export/Import feature provides crucial backup, sharing, and cross-device functionality, directly mitigating the limitations of local-only sto`

### COOL — APPROVE (low)
- **Reason:** The Letter Quality Checker provides a deeply domain-specific validation that reinforces the tool's core promise of 'proper formatting' and 'correctness,' making it unreasonably good at a niche task. The Portable Draft Export/Import enhances the utility's single-file portability, aligning perfectly with its unique architectural constraints.

### LESSONS — APPROVE (low)
- **Reason:** All documented lessons regarding escaping, error handling, disclaimers, and format documentation are correctly implemented or not applicable.

## Resolution

**RESOLVED 2026-04-25. BUGS medium fixed at source — recursive schema validation added.**

### BUGS medium — FIXED
The original `validateImportSchema` only checked top-level container types. Added three recursive helpers + a `QC_FIELD_KEYS` whitelist for `fields`:

- `_sanitizeFieldsObj(v, errors)` — keeps only known field names from `QC_FIELD_KEYS` (the 17 form fields actually used by `getFullState`); type-checks each as string; strips unknown or non-string entries.
- `_sanitizeStringArray(v, label, errors)` — used for `via`, `refs`, `encls`, `copyTo`; drops non-string entries with a positional error note.
- `_sanitizeParties(v, errors)` — drops non-object entries; keeps only the four recognized party-string fields (`name`, `title`, `organization`, `signature`); skips empty entries.
- `_sanitizeRouting(v, errors)` — type-checks `suspense` / `drafter` strings; for `reviewers` array, drops non-object entries and coerces `name`/`action` to safe defaults.

Each helper drops malformed entries silently and pushes a one-line `errors[]` note for the user-facing import status (which already uses `.textContent`, so the note renders as inert text). The envelope keys (`_navalscribe_version`, `_navalscribe_exported_at`) are also now string-type-checked. 7/7 naval-scribe tests pass.

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun IMPLEMENTATION; expected clean pass → TESTS → OUTCOME → ship.

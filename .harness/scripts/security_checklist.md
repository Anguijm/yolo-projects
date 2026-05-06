# Security checklist

Loaded by `council.py` and injected into the Security reviewer's prompt as authoritative non-negotiables.

**Specialize this file for the repo.** The generic items below apply broadly; the most valuable additions are repo-specific (your auth model, your trust boundaries, your destructive operations).

## Generic non-negotiables

- **No real secrets in committed files.** `.env.example` placeholders only (empty values or `KEY=`); real secrets live in `.env.local`, env vars, or platform secret stores.
- **All third-party GitHub Actions pinned to commit SHAs**, not floating tags.
- **Untrusted input sanitized at the boundary** before reaching LLMs, eval-like surfaces, shell commands, or DB writes that bypass schema validation.
- **Destructive operations gated.** Bulk delete / wipe / drop must require explicit `--confirm` or `DRY_RUN=false` env opt-in; never silent.
- **Dependencies pinned** (exact versions, not ranges) in lockfiles committed to git.

## Repo-specific (fill in)

<!-- Replace with the actual security surface of this repo. Examples:
- Auth model: <e.g., "Supabase RLS on every table; service-role key server-only">
- External keys: <list each, where it lives, what bypasses what>
- Trust boundaries: <where untrusted input enters; what sanitization is applied>
- Forbidden operations: <e.g., "Pipeline must never write saved_hunts/*">
- Audit trail: <what gets logged, where, retention>
-->

(Add repo-specific items here. The Security reviewer reads this file via `load_security_checklist()` in `council.py`.)

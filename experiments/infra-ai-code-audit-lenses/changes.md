# Changes — infra-ai-code-audit-lenses

## Files

- **`ai_antipatterns.py`** (NEW, repo root, ~190 LOC) — fourth advisory lens.
  - `read_html(path)` (`ai_antipatterns.py:62`) — utf-8 read + HTML validation, mirrors the sibling lenses.
  - `_strip_comments_and_strings(text)` (`ai_antipatterns.py:75`) — blanks HTML/JS comments and string/template literals to same-length whitespace; linear regexes (no nested quantifiers) to avoid ReDoS. Used for *definition* detection only.
  - `_comment_regions(text)` (`ai_antipatterns.py:108`) — concatenates comment regions for the orphan-TODO scan.
  - `_keywords(text)` (`ai_antipatterns.py:116`) — token set (≥4 chars, minus stopwords) for the plan-drift Jaccard.
  - `check_ai_antipatterns(path)` (`ai_antipatterns.py:121`) — the five checks; returns `list[str]`.
  - `main()` (`ai_antipatterns.py:~210`) — `--help`, usage, `REPO_ROOT` containment guard, `[WARN]`/`PASS`/`WARNINGS: N` output, exit 0 always.
- **`experiments/infra-ai-code-audit-lenses/plan.md`** (NEW) — plan-gate artifact.
- **`experiments/infra-ai-code-audit-lenses/README.md`** (NEW) — usage + check rationale + trade-offs.
- **`experiments/infra-ai-code-audit-lenses/changes.md`** (NEW) — this file.

No other repo files touched (stayed strictly within `deliverable_paths`). No orchestrator wiring — the existing three lenses are standalone; the fourth follows that convention.

## How the PLAN-gate objections were addressed

- **BUGS (OBJECT, high)** — "avoidance of stripping comments/strings will cause false positives/negatives." Addressed: added `_strip_comments_and_strings` and scoped all code checks to `<script>` block contents. Definition detection runs on the stripped copy; reference counting runs on raw script text (bias toward false negatives over the noisier false positives). Validated: zero false positives across five known-good projects after the fix (two real false positives — `onPointerCancel` named callback in `url-dissect`, and `_playChime`/`parseSlideTimeSecs` in `markdown-deck` — were found and eliminated during validation).
- **SECURITY (OBJECT, low)** — ReDoS on regex-only processing. Addressed: all stripping/scan regexes are linear with no nested quantifiers `(a+)+`; inputs are local repo files behind the `REPO_ROOT` containment guard, not network-fetched hostile content. The sibling `plan.md` read is also behind the same containment guard.
- LESSONS approved (no veto). UI / GUIDE / USEFULNESS / COOL approved.

## Verification performed

- `ast.parse` clean.
- `--help` exits 0; missing-file and out-of-repo paths exit 1 with `ERROR`.
- Fixture with a bare import / unused import / TODO / dead function → all four checks fire; relative import, used binding, `onclick` ref, and named callback expression correctly *not* flagged.
- Five known-good portfolio projects (`svg-fields`, `cron-explain`, `url-dissect`, `markdown-deck`, `naval-scribe`) → all `PASS`, exit 0.

# ai_antipatterns.py — AI-code-antipattern lens

A fourth advisory lens for YOLO single-file HTML builds, joining
`ux_completeness.py`, `mobile_usability.py`, and `cult_status.py`. It scans the
embedded JS/markup of a built tool for documented AI-generated-code failure
modes and prints advisory `[WARN]` lines. It **never blocks the build**
(exit 0 always; exit 1 only when the input file is missing or not HTML).

Adopted from Phase 4 experiment `nb-2026-04-13-amazon-ai-code-quality-audit`.

## Usage

```bash
python3 ai_antipatterns.py <project>/index.html
python3 ai_antipatterns.py --help
```

Like the other three lenses it is invoked standalone (there is no shared lens
runner today). Run it alongside the others during a build's review pass.

## The five checks

| Check | What it flags | Why it matters |
|---|---|---|
| `hallucinated-imports` | Bare-specifier `import`/`import()`/`require()` (e.g. `import _ from 'lodash'`) when there's no `<script type="importmap">` | A single-file browser tool has no bundler; bare specifiers never resolve. Classic "AI assumed a build step" artifact. |
| `unused-imports` | An imported binding whose name appears only at its import site | Dead import left after the code that used it was removed/rewritten. |
| `orphan-TODO` | `TODO`/`FIXME`/`XXX`/`HACK` markers inside comments | Placeholder intentions the model never completed. |
| `deadcode-function` | A named function *declaration* never referenced (incl. from inline `onclick=` handlers) | Orphan functions from plan drift. Entry points (`main`, `init`, `setup`, `start`, `run`, `render`, `app`) are exempt. |
| `mismatched-plan` | The tool's visible copy shares almost no vocabulary with a sibling `plan.md` (Jaccard < 0.05) | The shipped tool drifted from what was planned. Silently skipped when no `plan.md`. |

## Deliberate trade-offs (low false-positive bias)

This lens is advisory, so noise erodes trust faster than a missed warning. Two
design choices bias it toward **false negatives over false positives**:

1. **Code analysis is scoped to `<script>` blocks**, not the whole document.
   A sample markdown deck in the page body can contain stray backticks/quotes
   that would otherwise corrupt identifier scanning.
2. **Reference counting runs against raw script text.** Comments and string
   literals are blanked only for *definition* detection (so a function name
   inside a string isn't mistaken for a definition). For deciding whether a
   binding/function is *used*, a mention in a comment or string counts as a
   use — under-reporting some dead code rather than wrongly flagging live code.
   This was validated against five known-good portfolio projects, all of which
   the lens passes cleanly.
3. **`hallucinated-imports` is suppressed when an importmap is present**, since
   bare specifiers are then legitimate.

## Validation

- Passes cleanly (no warnings) on five shipped, known-good projects:
  `svg-fields`, `cron-explain`, `url-dissect`, `markdown-deck`, `naval-scribe`.
- Fires correctly on a fixture containing a bare import, an unused import, a
  TODO marker, and a dead function — while correctly *not* flagging a relative
  import, a used binding, an `onclick`-referenced function, or a named callback
  function expression.

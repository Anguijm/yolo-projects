## Goal

Produce a dated snapshot document cataloguing every external dependency in the yolo-projects pipeline with deprecation horizon, coupling depth, and replacement plan.

## Scope

**In scope:**
- All external pip packages installed in `.github/workflows/*.yml`
- All GitHub Actions marketplace actions referenced in `.github/workflows/*.yml`
- The Claude Code CLI npm package (`@anthropic-ai/claude-code`)
- Runtime versions pinned in workflows (Node.js, Python)
- External API services the pipeline calls at runtime (Anthropic API, Google Gemini API)
- GitHub Actions platform itself as a hosting dependency
- YouTube RSS (no auth, but a live network dependency)
- Hardcoded model names in `council.py`
- The zero-dep single-file HTML YOLO tool pattern (celebrating what we DON'T depend on)

**Explicitly out of scope:**
- Python stdlib modules (json, re, pathlib, etc.) — stable, zero risk
- The 231 single-file HTML portfolio tools — they are the deliverables, not pipeline deps
- Harness-cli in a separate repo (cron cannot access it)
- Local dev machine dependencies

## Approach

Single file: `experiments/adopt-stack-audit/STACK_AUDIT.md`.

**Step 1 — Installable packages and runtime versions (from workflow YAML):**
Locate by **grep-by-content**, not by line number — line numbers rot when files shift. Each commands below should be cited verbatim in `STACK_AUDIT.md` so a future reader can re-derive the data with one command:
- `grep -nE "pip install" .github/workflows/*.yml` — pip packages
- `grep -nE "npm install" .github/workflows/*.yml` — npm packages
- `grep -nE "uses: [^@]+@" .github/workflows/*.yml` — every `owner/action@version` reference
- `grep -nE "(node|python)-version:" .github/workflows/*.yml` — pinned runtime versions

Each row in the dependency table records the grep match itself (file + content) rather than a static line number. If the workflow file is reorganized, the grep still finds the dep.

**Security note:** GitHub Actions secrets are never stored in workflow files — they appear only as `${{ secrets.KEY_NAME }}` references. The grep output for `ANTHROPIC_API_KEY` or `GEMINI_API_KEY` will contain the variable reference, not any actual secret value. If a grep match unexpectedly contains what appears to be an actual secret value, redact it with `[REDACTED]` before recording it in STACK_AUDIT.md and flag the source file for immediate remediation.

**Step 2 — Hardcoded model names (from council.py):**
- `grep -nE "^(MODEL_NAME|CLAUDE_MODEL)\s*=" council.py`

These are pipeline dependencies even though they aren't installable packages — a model deprecation forces a code edit. Recording the grep pattern means the audit stays valid even if the constants move within the file.

**Step 3 — External API services (documented from code inspection):**
These are not installable packages but are live runtime dependencies. Each citation is a grep pattern, not a line number:
- **Anthropic API** — `grep -n "anthropic_sdk.Anthropic\|anthropic\.Anthropic" council.py` for SDK construction; `grep -n "ANTHROPIC_API_KEY" .github/workflows/*.yml` for secret usage.
- **Google Gemini API** — `grep -n "genai\.configure\|genai\.GenerativeModel" council.py` for SDK construction; `grep -n "GEMINI_API_KEY" .github/workflows/*.yml` for secret usage.
- **GitHub Actions platform** — the entire cron scheduling, runner provisioning, and `git push` integration depends on GitHub-hosted runners. Citation: existence of `.github/workflows/tick_tock.yml` (entire file is the dependency surface).
- **YouTube RSS** — `grep -n "youtube\.com/feeds\|urllib\.request" fetch_youtube_rss.py` for the network call site; `grep -n "fetch_youtube_rss" .github/workflows/daily_research.yml` for the workflow invocation.

**Step 4 — Zero-dep celebration section:** Document the single-file HTML YOLO tool pattern as the lowest-coupling surface.

**Step 5 — Assembly:** Write `STACK_AUDIT.md` with all tables and sections.

No subtask dependencies — the entire document can be written in one pass after the reads.

## Assessment Methodology

How each column in the dependency table is populated:

**Current version:** Exact string from the `@version` tag in workflow YAML, or from `pip install pkg` (no pin = latest-at-install-time), or the constant string in source code.

**Deprecation horizon:** Expert estimate based on known support lifecycle signals:
- `stable` — no known EOL, actively maintained by a major org (e.g., `actions/checkout`, Python 3.12, Node 20 LTS)
- `24mo` — major version, EOL announced but ≥2 years out
- `12mo` — upstream has a successor; migration path exists but no urgency
- `6mo` — EOL announced or successor is default in new projects
- `3mo` — actively deprecated (e.g., `google-generativeai` — the FutureWarning fires on every import)

**Coupling depth:**
- `shallow` — one import statement, replaced by swapping a package name
- `medium` — several call sites; migration requires touching multiple files but no architectural change
- `deep` — architectural coupling; replacing it requires rethinking the surrounding system (e.g., hardcoded model names in council.py affect retry logic, fallback paths, cost model)

**Replacement plan:** Concrete successor package, action, or runtime version that resolves the risk. "N/A — stable" for items with no foreseeable risk.

## File Layout

| File | Action | Notes |
|------|--------|-------|
| `experiments/adopt-stack-audit/STACK_AUDIT.md` | CREATE | Primary deliverable, ~120 lines |
| `experiments/adopt-stack-audit/plan.md` | CREATE | This file |
| `experiments/adopt-stack-audit/changes.md` | CREATE (implementation gate) | Brief summary |

No existing files modified.

## Function Map

N/A — no functions added/modified. This is a documentation-only tick: one markdown file created.

## Security

No code executed. No secrets stored. The STACK_AUDIT.md is a read-only reference document — no attack surface introduced.

## UI

N/A — documentation artifact, no UI.

## Guide

Document is authored for the human architect/owner. Tone: factual, terse. Each row is grep-verifiable against the cited file:line.

## Edge Cases

- `requests` pip package: installed via `tick_tock.yml` (locate by `grep -n "pip install.*requests" .github/workflows/*.yml`) but no `import requests` found in repo Python files (`grep -rn "^import requests\|^from requests" --include="*.py" .`). Document as installed-but-unused with a note.
- `stefanzweifel/git-auto-commit-action@v5` only appears in `daily_research.yml`, not `tick_tock.yml` (which uses `git` directly). Document per workflow.
- Model names are hardcoded strings in `council.py`, not versioned packages — coupling is deep despite the simple syntax.

## Test Strategy

- Each dependency row cites the **grep pattern** that locates it (not a line number) — verifiable by re-running the command. This is the central anti-rot mechanism: if a file is reorganized, the grep still finds the dep.
- Model names verified by `grep -nE "^(MODEL_NAME|CLAUDE_MODEL)\s*=" council.py`.
- Runtime versions verified by `grep -nE "(node|python)-version:" .github/workflows/*.yml`.
- `requests` installed-but-unused status verified by `grep -rn "^import requests\|^from requests" --include="*.py" .` returning empty.
- The audit document is invalid if any cited grep returns zero matches — that is the test signal.

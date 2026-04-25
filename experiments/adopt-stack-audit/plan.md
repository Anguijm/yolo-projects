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
Read `.github/workflows/tick_tock.yml` and `.github/workflows/daily_research.yml`. Extract:
- All `pip install` packages (line 37 of tick_tock.yml, line 59 of daily_research.yml)
- All `npm install` packages (tick_tock.yml line 40)
- All `uses: owner/action@version` references
- `node-version` and `python-version` pinned values

**Step 2 — Hardcoded model names (from council.py):**
Read `council.py:90-91` to extract `MODEL_NAME` and `CLAUDE_MODEL` constants. These are pipeline dependencies even though they aren't installable packages — a model deprecation forces a code edit.

**Step 3 — External API services (documented from code inspection):**
These are not installable packages but are live runtime dependencies:
- **Anthropic API** — `council.py` calls `anthropic_sdk.Anthropic(api_key=...)` (line ~553); `scripts/process_experiments.py` calls the Anthropic messages API. Citation: `council.py:553`, `tick_tock.yml:99` (ANTHROPIC_API_KEY secret).
- **Google Gemini API** — `council.py` calls `genai.configure(api_key=...)` (line ~542) and `genai.GenerativeModel(...)` (line ~232). Citation: `council.py:542`, `tick_tock.yml:100` (GEMINI_API_KEY secret).
- **GitHub Actions platform** — the entire cron scheduling, runner provisioning, and `git push` integration depends on GitHub-hosted runners. Citation: `.github/workflows/tick_tock.yml` (entire file).
- **YouTube RSS** — `fetch_youtube_rss.py` uses `urllib.request.urlopen` on YouTube RSS endpoints. No API key — pure HTTP. Citation: `fetch_youtube_rss.py` (imports `urllib`), `.github/workflows/daily_research.yml:63`.

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

- `requests` pip package: installed in `tick_tock.yml` line 37 but no `import requests` found in repo Python files. Document as installed-but-unused with a note.
- `stefanzweifel/git-auto-commit-action@v5` only appears in `daily_research.yml`, not `tick_tock.yml` (which uses `git` directly). Document per workflow.
- Model names are hardcoded strings in `council.py`, not versioned packages — coupling is deep despite the simple syntax.

## Test Strategy

- Each dependency row cites the exact file and line where it appears — verifiable by `grep`.
- Model names verified against `council.py:90-91`.
- Runtime versions verified against workflow YAML step definitions.
- `requests` installed-but-unused status verified by absence of `import requests` in `*.py`.

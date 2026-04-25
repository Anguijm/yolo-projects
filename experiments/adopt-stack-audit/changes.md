# changes.md — adopt-stack-audit IMPLEMENTATION

## File created
- `experiments/adopt-stack-audit/STACK_AUDIT.md` (~140 lines) — primary deliverable

## Content summary
7 sections covering every dependency surface in the pipeline:
1. Python packages: `anthropic`, `google-generativeai` (3mo deprecated), `requests` (unused)
2. npm: `@anthropic-ai/claude-code` (global install, no pin)
3. GitHub Actions: `checkout@v4`, `setup-node@v4`, `setup-python@v5`, `git-auto-commit-action@v5`
4. Runtimes: Python 3.12 (stable), Node 20 (**EOL 2026-04-30 — 5 days**)
5. Hardcoded model names: `gemini-2.5-flash` (council primary), `claude-haiku-4-5-20251001` (fallback)
6. Runtime API services: Anthropic, Google Gemini, GitHub Actions, YouTube RSS
7. Zero-dep celebration: the 231 single-file HTML YOLO tools

## Key findings
- **Node 20 EOL in 5 days** — most urgent finding, one-line fix in tick_tock.yml
- `google-generativeai` SDK deprecated — 3mo horizon, migrate to `google-genai`
- `requests` installed but never imported — can be removed

All rows use grep-by-content patterns rather than static line numbers.

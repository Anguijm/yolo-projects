# env-inspector

A browser-based `.env` file linter, `.env.example` generator, and markdown docs table generator. **All processing is local — no data ever leaves your browser.**

## What it does

Paste any `.env` file and instantly get:

- **Lint tab** — errors (parse failures, duplicate keys, keys with spaces), warnings (non-UPPER_SNAKE_CASE, unquoted spaces), and info (quoted values, secret key advisories)
- **Example tab** — a `.env.example` file with values masked (secrets replaced with `your_secret_here`, URLs with passwords masked, booleans/numbers kept)
- **Docs tab** — a markdown table of all keys with detected types (boolean, number, url, secret, string) and notes

## How to run

Open `index.html` directly in any browser. No server required.

## Features

- Live re-parse as you type (180ms debounce)
- Drag-and-drop a `.env` file onto the left pane
- Download `.env.example` or `env-docs.md` directly
- Copy any tab's output to clipboard
- Clear button to start fresh
- Stats bar: key count, comment count, duplicate count, issue count
- Lint severity legend (error / warning / info)
- Mobile-responsive layout

## Design decisions

- Single HTML file, zero dependencies
- All state is computed on the fly from `elInput.value` — no sync bugs
- Case-insensitive duplicate detection (`API_KEY` and `api_key` are flagged)
- Inline comment stripping: `KEY=value # comment` correctly strips the comment
- URL masking preserves structure but replaces credentials

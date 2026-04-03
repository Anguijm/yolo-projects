# cURL to Code

Paste a cURL command, get equivalent code in Python, JavaScript, Go, or PHP.

## What it does

- Parses any cURL command (including flags from browser DevTools "Copy as cURL")
- Shows a visual breakdown of the request (method, URL, headers, auth, flags)
- Generates equivalent code in 4 languages with one click:
  - **Python** — `requests` library with proper `json=` / `data=` / `auth=` handling
  - **JavaScript** — `fetch` API with async/await
  - **Go** — `net/http` package with full error handling
  - **PHP** — `curl_*` functions

## How to run

Open `index.html` in any browser. No server needed.

## Features

- Auto-parses on paste (no button click required)
- `Ctrl+Enter` / `Cmd+Enter` to convert
- 5 sample commands covering GET, POST JSON, POST form, basic auth, complex requests
- Handles: `-X`, `-H`, `-d`, `--data-raw`, `--data-urlencode`, `-F`, `-u`, `-L`, `-k`, `--compressed`, `-b`, `-A`
- Backslash line continuations (`\` + newline) and Windows `^` continuations
- Copy to clipboard button

## Languages

- Zero external dependencies — single HTML file
- All processing is client-side — no data leaves your browser

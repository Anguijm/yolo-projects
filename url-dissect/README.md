# URL Dissect

URL anatomy breakdown, relative URL resolver, and bulk URL extractor — all in one offline tool.

## What it does

**Dissect tab**: Paste any URL and instantly see every component:
- Scheme, userinfo (user + masked password), host with TLD badge
- Port with default-port awareness (shows "443 — default for https")
- Non-standard port flagged with a warning badge
- Path segments decoded individually
- Query params as key/value table: raw vs decoded, encoding issues flagged (double-encoded, `+` as space, malformed %-sequences)
- Fragment

Below the breakdown: a **Live Rebuild widget** — edit any field (scheme, host, port, path, query, fragment) and the full URL updates in real time. Click the output to copy.

**Resolve tab**: Type a base URL and a relative URL; see the resolved absolute URL instantly.

**Bulk tab**: Paste any block of text (logs, HTML, markdown, config files). All URLs are extracted, deduplicated, and listed. Click a row to copy the URL; click **Dissect** to switch tabs and analyze it.

## How to run

Open `index.html` in any modern browser. No server required, no dependencies.

For PWA offline support, serve from a local server:
```bash
python3 -m http.server 8080
# then visit http://localhost:8080/url-dissect/
```

## Tech

- Pure browser `URL()` API + `URLSearchParams` — zero external deps
- Raw query param parsing from `u.search` string to detect raw vs decoded values
- `new RegExp(...)` used for patterns with `{n}` quantifiers (test suite compatibility)
- Single HTML file + manifest.json + sw.js for PWA

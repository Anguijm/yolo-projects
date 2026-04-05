# Unix TS — Timestamp Debugger

Paste any Unix timestamp and instantly see it in every useful format. Auto-detects seconds vs milliseconds (threshold: 1e12).

## What it does

**Forward (timestamp → formats):**
- ISO 8601
- UTC
- Local (with IANA timezone name)
- RFC 2822
- SQL DATETIME
- Relative ("3 months ago" / "in 2 hrs") — live-updating
- Epoch seconds + Epoch milliseconds
- Copy button on every row

**Reverse (date → epoch):**
- Pick a date/time with a native datetime-local picker
- Choose UTC or Local interpretation
- Get epoch seconds and milliseconds

**Presets:** Now, Now (ms), Y2K, Epoch 0, Y2038

Accepts comma-formatted timestamps like `1,712,345,678`.

## How to run

Open `index.html` directly in a browser — no server needed.

For full PWA offline support, serve from a local HTTP server:
```
python3 -m http.server 8080
```
Then open `http://localhost:8080/unix-ts/`.

## PWA

Includes `manifest.json` and `sw.js` for offline use and home screen installation.

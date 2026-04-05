# UUID Inspector

Paste any UUID and get instant deep inspection. Zero external dependencies, works offline.

## What it does

- **Version detection** — v1 through v8, plus Nil and Max UUIDs
- **v1 decode** — 60-bit Gregorian timestamp → ISO date + relative time, MAC/node extraction (with random/assigned flag), clock sequence
- **v7 decode** — 48-bit Unix ms timestamp → ISO date + relative time, rand_a field
- **v3/v5** — identifies hash-based UUIDs and notes that namespace+name are unrecoverable
- **Namespace recognition** — identifies the 4 RFC 4122 predefined namespace constants (DNS, URL, OID, X.500 DN)
- **Structure bar** — color-coded field breakdown showing which bits carry which data (v1 and v7)
- **Format validator** — valid/invalid badge, RFC 9562 Nil and Max special-case detection
- **Share** — sets URL hash so the UUID is bookmarkable/shareable
- **Bulk mode** — paste up to 500 UUIDs (one per line), get a version/timestamp summary table
- **Generator** — Gen v1 (current timestamp + synthetic random node), Gen v4 (random), Gen v7 (Unix ms + random)

## How to run

Open `index.html` in any modern browser. No server needed.

```
open uuid-inspector/index.html
```

For PWA/offline: serve over HTTP (e.g. `python3 -m http.server 8080`) and visit `http://localhost:8080/uuid-inspector/`.

## Tech notes

- Pure JS, zero deps — all math is BigInt arithmetic in the browser
- v1 Gregorian offset: `122192928000000000n` (100-ns ticks between 1582-10-15 and 1970-01-01)
- v7 timestamp extracted from first 48 bits as `parseInt(hex.slice(0,12), 16)` — safe within `Number.MAX_SAFE_INTEGER` until year 10889
- Generated v1 UUIDs use the multicast bit (I/G bit) to signal a synthetic/random node

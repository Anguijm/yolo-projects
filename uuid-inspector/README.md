# UUID Inspector

Paste any UUID, get instant version detection, field decode, and a generator — all offline, zero deps.

## What it does

- **Version detection** — v1/v2/v3/v4/v5/v6/v7/v8 + Nil + Max UUID
- **Color-coded anatomy** — each UUID field highlighted by role (timestamp, version, variant, random bits, MAC node)
- **Per-version decode:**
  - v1: Gregorian 60-bit timestamp → Unix ms + ISO datetime + relative time + MAC node + clock seq
  - v7: 48-bit Unix ms timestamp → datetime + relative time + rand_a/rand_b fields
  - v3/v4/v5: algorithm info, sortability, notes
  - v2/v6/v8: informational notes
- **Generator** — produce v1, v4, or v7 UUIDs; click output to load into inspector
- **Bulk mode** — paste one UUID per line, get a table with version + timestamp info for each

## How to run

Open `index.html` in any modern browser. No server needed.

## Tech notes

- Pure JS, zero dependencies, single HTML file
- BigInt for 60-bit Gregorian timestamp math (v1)
- `crypto.getRandomValues` for all generators
- v7 generator produces correctly spec-compliant time-ordered UUIDs

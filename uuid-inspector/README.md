# UUID Inspector

Offline UUID decoder, analyzer, and generator. Zero dependencies — single HTML file.

## What it does

**Inspect tab** — paste any UUID to instantly decode:
- Version detection (v1–v8, Nil, Max)
- v1: 60-bit Gregorian timestamp → date/time, MAC address extraction, clock sequence, multicast/locally-administered MAC flags
- v6: reordered Gregorian timestamp decode (RFC 9562)
- v7: 48-bit Unix ms timestamp decode → date/time + relative time
- Variant detection (RFC 4122, Microsoft, NCS, Future)
- Color-coded segment breakdown (time fields, version nibble, variant bits, node)
- Accepts plain, braced `{...}`, and URN `urn:uuid:...` forms

**Bulk tab** — paste N UUIDs (one per line):
- Valid/invalid count, version distribution summary
- Per-row: version, decoded timestamp, notes

**Generate tab** — generate UUIDs:
- v4 (cryptographic random, 122 bits)
- v7 (time-ordered, 48-bit Unix ms prefix — default in Rails 7.1+, Laravel 11+)
- v1 mock (current timestamp, random node with multicast bit)
- Click any generated UUID to copy; "INSPECT →" jumps it to the Inspect tab

## How to run

Open `index.html` in any browser. No server required.

```
open uuid-inspector/index.html
```

## What to change

- Add SHA-1/MD5 computation to generate real v3/v5 UUIDs from namespace+name input
- Add OUI database lookup for v1 MAC vendor identification
- Add v6 generator

# Char Map — Unicode Character Inspector

Paste any text and see every Unicode code point as an interactive grid. Click any character cell for full encoding details.

## What it does

- **Character grid**: Every code point from your text shown as a clickable cell with U+XXXX label
- **Full encoding details** on click: UTF-8 bytes, UTF-16 units, JS escape, HTML entity, block, category
- **Stats bar**: total code points, UTF-8 byte count, non-ASCII count, unique count
- **Show invisible**: reveals control chars (LF, TAB, ZWJ, BOM, etc.) with their names
- **Deduplicate**: collapse repeated code points, show count badge
- **Copy tools**: Copy as JS escape sequences (`\u0048\u0065...`), or as Base64 (UTF-8)
- **Preset text**: ships with a sample covering ASCII, accented Latin, math symbols, CJK, and emoji

## How to run

Open `index.html` in any modern browser. No server required.

## What to change

- Increase `MAX_DISPLAY = 2000` if you want to render more cells (may slow down on huge pastes)
- Add more entries to the `block-data` JSON for finer block identification
- Add more named HTML entities to `common-entities` JSON

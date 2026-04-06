# Unicode Character Inspector

Paste any text, get a full character-by-character breakdown.

## What it does

- **Per-character table**: Glyph · Index · Codepoint (U+XXXX) · Name · Unicode category · UTF-8 bytes (hex) · UTF-16 representation · HTML entity · JSON escape
- **Suspicious character panel**: Automatically flags and explains zero-width spaces, BOM, invisible format chars, BIDI direction overrides (Trojan Source attacks), and Cyrillic/Greek homoglyphs that visually impersonate Latin letters
- **6 demo presets**: ASCII, Latin/diacritics, Invisible chars, Homoglyphs, Emoji, Math symbols
- **Copy buttons**: Copy U+XXXX codepoint or raw character per row
- **Paginated**: First 500 code points rendered, load-more for longer text

## How to run

Open `index.html` in any browser. No server or dependencies needed.

## Security angles covered

- Zero-width space (U+200B), BOM (U+FEFF), invisible joiners/marks
- BIDI overrides: U+202E (RTL Override) — the Trojan Source attack vector, flagged as **critical**
- Cyrillic homoglyphs: а е о р с у х А В Е К М Н О Р С Т Х (and more)
- Greek homoglyphs: Α Β Ε Ζ Η Ι Κ Μ Ν Ο Ρ Τ Υ Χ
- Fullwidth ASCII lookalikes (U+FF01–U+FF5E)
- Tag characters (U+E0000–U+E007F) — covert data channels

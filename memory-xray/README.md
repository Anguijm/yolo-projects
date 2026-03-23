# Memory X-Ray

Brutalist 64-bit binary explorer. Toggle individual bits and see real-time readouts as Float64 (IEEE 754), Int64, Uint64, Float32x2, Hex, and ASCII. Inject text or numbers directly into the buffer.

## Features

- 64 clickable bit toggles grouped into 8 bytes
- IEEE 754 color-coding: sign (yellow), exponent (magenta), mantissa (cyan)
- Real-time readouts: Float64, signed/unsigned Int64 (BigInt), Float32x2, Hex dump, ASCII
- Text injection: type up to 8 characters, see their byte representation
- Number injection: type any float (including Infinity, NaN, -0) and press Enter
- Big/Little Endian toggle with correct DataView interpretation and IEEE 754 re-highlighting
- Utility buttons: Clear, Invert, Randomize, Shift Left, Shift Right
- Brutalist terminal aesthetic (monospace, harsh neon, zero border-radius)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Float formatter regex stripped trailing zeros from integers (100 displayed as "1") — switched to Number(toPrecision()).toString()
- Endian toggle physically reversed bytes instead of changing DataView interpretation — now uses !bigEndian flag in all DataView calls
- IEEE 754 highlighting was static (didn't update on endian toggle) — now rebuilds grid with correct mathBit mapping
- Number input used parseFloat (accepts "123abc" as 123) — switched to strict Number() parsing

## How to Run

Open `index.html`. Click bits to toggle them. Type in the text or number fields to inject values. Try typing `0.1` in the number field and see why `0.1 + 0.2 !== 0.3`.

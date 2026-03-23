# Base Sync

Developer-grade number base converter. Decimal, hexadecimal, binary, and octal with live bidirectional sync. BigInt for arbitrary precision.

## Features

- 4 synced inputs: decimal, hex, binary, octal
- Type in any field, others update instantly
- BigInt for arbitrary precision (beyond 2^53)
- Binary auto-formatted in nibbles (4-bit groups with spaces)
- Decimal auto-formatted with commas
- Input validation per base (rejects invalid characters)
- Cursor-aware formatting (cursor doesn't jump on mid-edit)
- One-click copy per field (strips formatting)
- Copy button visual feedback (checkmark flash)
- Clipboard API with textarea fallback
- Bit length display
- Error state on invalid input
- Dark monospace UI, OLED black, mobile-first

## Bugs Fixed by Gemini Audit

- Cursor jumped to end on mid-string edit (formatting reassignment killed cursor position) — implemented data-character-relative cursor tracking
- Dead variable (toastTimer) and unused function (filterInput) removed
- Input handling consolidated into single handleInput function

## How to Run

Open `index.html`. Type a number in any field (decimal, hex, binary, octal). The other fields update in real-time. Click the copy button next to any field to copy the raw value.

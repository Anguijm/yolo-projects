# Tip Calculator

Enter your bill, pick a tip percentage, split between people. The most useful restaurant app.

## Features

- Bill input with decimal keyboard (inputmode="decimal")
- 5 preset tip buttons (10/15/18/20/25%) + custom percentage input
- Split bill between 1-20 people
- Live calculation on every input change
- Per-person amount shown only when split > 1
- Custom tip cleared resets to 0% (no ghost percentage)
- parseFloat for tip buttons (supports decimal percentages)
- Auto-focus bill input on load
- OLED black, mobile-first, all PWA metas, click events only

## Bugs Fixed by Gemini Audit

- Custom tip cleared left ghost percentage (reset to 0 on invalid/empty)
- parseInt truncated decimal tips (switched to parseFloat)

## How to Run

Open `index.html` on your phone. Enter your bill amount.

# Entropy Forge

Cryptographically secure password and passphrase generator with entropy visualization. Dual mode: random strings or word-based passphrases.

## Features

- String mode: configurable length (8-64), toggleable character sets (upper/lower/numbers/symbols)
- Passphrase mode: 3-8 random words from embedded 1000+ word dictionary
- crypto.getRandomValues with rejection sampling (no modulo bias)
- Shannon entropy calculation and display (bits)
- Color-coded entropy bar (red/yellow/green/blue)
- Scramble reveal animation (progressive character settling)
- One-click copy with visual flash feedback
- Clipboard API with textarea fallback for non-HTTPS
- Settings changes auto-regenerate password (no stale display)
- Animation race condition protection (cancelAnimationFrame)
- Brutalist terminal aesthetic, OLED black, mobile-first

## Bugs Fixed by Gemini Audit

- Scramble animation race condition: rapid clicks caused multiple concurrent animations fighting for output (added cancelAnimationFrame)
- Settings changes (sliders, checkboxes) only updated entropy bar without regenerating password — stale password displayed with wrong entropy (now auto-generates on any change)
- cryptoRandInt could receive 0 max causing NaN/infinite loop (added guard clause)

## How to Run

Open `index.html`. Click Generate or press Enter. Toggle between String and Passphrase modes. Adjust length and character sets. Tap the output to copy.

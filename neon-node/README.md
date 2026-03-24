# Neon Node

Memory card matching game. Flip cards to find matching pairs. CSS 3D flip animations, move counter, timer, and multiple grid sizes.

## Features

- 3 difficulty levels: 4x3 (6 pairs), 4x4 (8 pairs), 5x4 (10 pairs)
- CSS 3D card flip animation (rotateY + backface-visibility)
- 16 Unicode symbol cards with unique neon colors per pair
- Fisher-Yates shuffle for random card placement
- Board locked during mismatch display (prevents click spam)
- Miss animation (shake) on mismatched pairs
- Glow animation on successful match
- Timer starts on first card flip
- Move counter and pairs found tracker
- Win message with final time and move count
- Haptic feedback on game completion
- Reset-safe: clears pending mismatch timeouts on new game (prevents stale state)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Timer/state leak: mismatch setTimeout fired on stale cards array after reset during animation window — tracked timeouts with clearTimeout on newGame, added null guards

## How to Run

Open `index.html`. Click cards to flip them. Find all matching pairs. Select difficulty with the buttons at the bottom. Click Reset to start over.

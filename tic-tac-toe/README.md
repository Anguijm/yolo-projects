# Tic Tac Toe

Play against an unbeatable minimax AI, or an easy random opponent. Win/loss/draw tracking.

## Features

- Minimax AI with alpha-beta depth scoring (unbeatable on Hard)
- Easy mode: 40% random moves
- Click spam prevention (aiThinking flag locks input during AI delay)
- Win line highlighting
- Synthesized audio on place and win
- Haptic on win
- W/L/D score tracked in localStorage
- Arrow key navigation, keyboard number input
- OLED black, mobile-first, click events only

## Bug Fixed by Gemini Audit

- Click spam: player could place multiple X's during 200ms AI delay (added aiThinking lock)

## How to Run

Open `index.html`. Tap cells to play X. AI responds as O.

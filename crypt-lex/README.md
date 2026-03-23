# Crypt-Lex

5-letter word deduction game. Guess the word in 6 attempts with color-coded feedback. Split dictionary with 500+ target words and 3000+ valid guesses.

## Features

- 5-letter word guessing with 6 attempts
- Two-pass evaluation for correct duplicate letter handling
- Color feedback: correct (green), present (amber), absent (gray)
- Virtual QWERTY keyboard with cumulative state tracking (keys never downgrade)
- Physical keyboard support (A-Z, Enter, Backspace)
- Split dictionary: curated targets + large validation list
- Invalid word shake animation with reflow-based restart
- Only active row updated on keystroke (not full grid re-evaluation)
- Win messages based on attempt count (Genius → Phew)
- Loss reveals target word
- New Game button on completion
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- updateGrid re-evaluated all past guesses on every keystroke (now only updates active row)
- Shake animation race condition on rapid Enter (used void offsetWidth reflow trick to restart animation)
- Submitted row rendering moved to submitGuess (direct render instead of full grid re-evaluation)

## How to Run

Open `index.html`. Type a 5-letter word and press Enter. Green = correct position, amber = wrong position, gray = not in word. 6 attempts to find the target.

# Cyber Breach

Hangman-style word guessing game with hacker/terminal theme. Guess tech words letter by letter before the system trace completes.

## Features

- 30 curated tech words with category hints (Security, Programming, API, etc.)
- On-screen QWERTY keyboard + physical keyboard support
- Correct guesses reveal letters in green
- Wrong guesses advance trace bar (6 max), key turns red
- Wrong letters displayed below word
- Shake animation on wrong guess (reflow trick for restart)
- Win (ACCESS GRANTED) / Lose (SYSTEM LOCKED) with word reveal
- Haptic feedback on win
- classList used for state (not className overwrite)
- Object.keys for safe property iteration (no for...in prototype risk)
- Modifier key guard (Ctrl/Cmd/Alt ignored)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- className = 'win' wiped all classes — switched to classList.remove/add
- for...in loop on guessed object vulnerable to prototype pollution — switched to Object.keys().filter()

## How to Run

Open `index.html`. Read the category hint. Type letters or tap the on-screen keyboard. Guess the word before 6 wrong guesses. Click REBOOT to play again.

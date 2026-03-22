# Name Picker

Enter names, pick one randomly with slot-machine animation, or split into teams. Perfect for teachers and groups.

## Features

- Pick One: slot-machine animation with decelerating speed, lands on random winner
- Split Teams: Fisher-Yates shuffle, auto-sizes 2-4 teams based on count
- Shuffle: randomize the list order
- Synthesized tick sounds during animation, arpeggio on result
- Haptic feedback on ticks and results
- Single-name handling (shows immediately without animation)
- Picking state lock prevents teams/shuffle during animation
- Names auto-saved to localStorage on every keystroke
- Color-coded team cards
- OLED black, mobile-first, click events only, all PWA metas

## Bugs Fixed by Gemini Audit

- State leak: teams/shuffle could run during pick animation (added picking guard)
- Single name: clicking Pick with 1 name did nothing (now shows it immediately)

## How to Run

Open `index.html`. Enter names (one per line). Pick, split, or shuffle.

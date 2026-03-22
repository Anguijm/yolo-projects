# KEY/STRIKE

A brutalist typing speed test. Start typing instantly — no buttons, no setup. Live WPM, accuracy, combo streaks, micro-shake on errors, synthesized key sounds. Single HTML file, zero dependencies.

## Features

- Instant start: text ready on page load, begin typing immediately
- Live WPM counter (5 chars = 1 word standard)
- Live accuracy percentage
- Combo counter: consecutive correct characters, glow at 10+
- Synthesized key sounds (Web Audio square wave, randomized pitch)
- Noise burst on errors
- Micro screen shake on typos (50ms, 1-2px CSS transform)
- Wrong characters shown in red (advance and backspace to fix)
- 8 curated passages (developer quotes, prose)
- Results: WPM, accuracy, time, errors, best combo, grade tier
- Grade tiers: LEGENDARY, BLAZING, FAST, SOLID, WARMING UP, HUNT & PECK
- Share button: copies ego-baiting score to clipboard
- localStorage personal best tracking
- Tab+Enter instant restart
- AudioContext.resume() for browser autoplay compliance
- performance.now() for sub-ms timing accuracy

## Bugs Fixed by Gemini Code Audit

- Wrong characters never rendered as red (chars array wasn't updated on error)
- AudioContext not resumed from suspended state
- Error typing didn't advance cursor (user couldn't see mistakes)

## How to Run

Open `index.html` in a browser. Start typing immediately.

## What You'd Change

- Leaderboard API
- Custom passage input
- Difficulty modes (time limit, no backspace)
- Mobile virtual keyboard support

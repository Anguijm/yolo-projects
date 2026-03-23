# Neon Reflex

Visual reaction time test. 5 rounds — wait for the screen to flash green, then tap as fast as possible. False start penalties. Grade ranking and all-time best tracking.

## Features

- 5-round visual reaction test
- Random delay (2-5 seconds) before trigger
- performance.now() for sub-millisecond precision
- False start detection with shake animation and penalty
- Round progress dots (green = success, red = false start)
- Final stats: average time, best time, S/A/B/C/D grade
- History bar chart showing per-round times
- All-time best persisted in localStorage
- Double-tap cooldown (100ms) prevents input skip
- Key auto-repeat guard prevents speedrun exploit
- Play again starts directly from results (no extra tap)
- Shake animation uses reflow trick for restart
- pointerdown + keyboard (Space/Enter) support
- Haptic feedback on false start
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Key auto-repeat: holding Space cycled through all rounds instantly (added e.repeat guard)
- Double-fire: simultaneous pointer+keyboard skipped result screen (added 100ms cooldown)
- Play again required two taps (done→idle→start — simplified to done→start directly)
- Shake animation didn't restart on rapid false starts (added reflow trick)

## How to Run

Open `index.html`. Tap or press Space to start. Wait for the screen to turn green, then tap as fast as you can. Don't tap too early!

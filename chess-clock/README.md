# Chess Clock

Brutalist dual-timer chess clock. 50/50 split screen with 180° rotation for the opponent. Tap your half to end your turn. Fischer increment support.

## Features

- 50/50 viewport split, top half rotated 180° for opponent
- Tap your zone to end turn and start opponent's clock (chess convention)
- Fischer increment: configurable seconds added per move
- 6 presets: 1|0, 3|2, 5|0, 5|5, 10|0, 15|10
- performance.now() + requestAnimationFrame for drift-free timing
- Panic mode: sub-60s switches from MM:SS to SS.ms (centiseconds)
- Active/inactive visual inversion (white vs black)
- Timeout state with red styling and haptic alert
- Screen Wake Lock API prevents screen dimming during play
- Auto-pause on background tab (prevents invisible time loss)
- WakeLock orphan prevention (check before re-acquiring)
- Move counter per player
- Pause via center divider tap
- pointerdown for zero-latency input
- Haptic feedback (15ms pulse) on turn switch
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- First tap started YOUR clock instead of opponent's (chess convention: tap starts opponent's time)
- Initial display showed 0.00 (timeLeft not initialized until startGame called)
- Background tab caused massive time jump on return (auto-pause + lastTick reset on visibility change)
- WakeLock orphaned on rapid acquire (added !wakeLock guard)
- No feedback on timeout (added vibration pattern)

## How to Run

Open `index.html`. Select a time preset, tap START. Place device between two players. Tap your half to end your turn. Tap the center line to pause.

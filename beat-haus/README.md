# Beat Haus

Brutalist 4-track, 16-step drum sequencer with synthesized audio. Kick, snare, hat, and acid synth — all mathematically generated via Web Audio API. No samples.

## Features

- 4 tracks: Kick (sine pitch drop), Snare (noise + triangle), Hat (HP noise), Acid (sawtooth + resonant filter)
- 16-step grid with click-to-toggle (acid track cycles: off → lo → hi)
- Lookahead audio scheduler (25ms interval, 100ms lookahead) for sample-accurate timing
- Visual playhead synced to audio time via event queue (not frame-based)
- WaveShaperNode distortion with adjustable drive curve
- DynamicsCompressorNode master limiter prevents clipping
- Symmetric swing (even steps lengthen, odd shorten by equal amount)
- BPM slider (60-200), drive slider, swing slider
- Beat grouping visual markers (every 4 steps)
- NaN-safe input parsing with fallback values
- Brutalist aesthetic: #0a0a0a black, #ff003c accent, zero border-radius
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Swing math asymmetric (added 0.5x to odd, subtracted 0.1x from even — tempo slowed with swing). Fixed to symmetric ±0.66x.
- Visual playhead and flash fired immediately on schedule, not when audio played (100ms ahead). Fixed with visual event queue checked against audioCtx.currentTime.
- parseInt('') on slider input returned NaN, permanently breaking scheduler. Added || fallback values.

## How to Run

Open `index.html`. Click PLAY. Click grid cells to toggle beats. Acid track cycles: off → low pitch → high pitch. Adjust BPM, drive, and swing.

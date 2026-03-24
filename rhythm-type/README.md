# Rhythm Type

Type words to the beat. A rhythm-action typing game with procedural drums, falling word notes, timing-based scoring, and progressive difficulty. Type each word as it reaches the hit line.

## Features

### Rhythm Engine
- Procedural 120 BPM drum beat (kick/snare/hat via Web Audio API)
- Lookahead scheduler (25ms interval, 100ms ahead) for sample-accurate beat timing
- Melodic synth stab on each correct keystroke
- Audio node cleanup via onended

### Typing Gameplay
- Words fall toward hit line, synced to audio clock (not frame-based)
- Type each word character by character — typed letters highlight cyan
- Timing scored on word completion: PERFECT (±50ms), GOOD (±120ms), OK (beyond)
- Combo multiplier: score increases with consecutive successful words
- Miss if word passes hit line by 400ms without completion
- Progressive difficulty: longer words and faster fall speed as you advance

### Audio-Visual Sync
- Note Y position anchored to audioCtx.currentTime (frame-rate independent)
- Fall speed locked per-note at spawn (mid-flight speed changes don't desync)
- Beat pulse on hit line synced to drum pattern
- Missed notes fall off-screen (distinct from completed notes that float up)

### Visual Feedback
- Particle burst on word completion
- Grade popup (PERFECT/GOOD/OK/MISS) with color coding
- Screen shake on miss or wrong key
- Proximity glow when note approaches hit line
- HUD: score, combo, WPM, best score

### Architecture
- Web Audio lookahead scheduler for beat timing
- Canvas rendering with dt-based particles but time-based note positions
- Audio context initialized on user interaction (browser policy compliant)
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Note positions were dt-based (desynced from audio on frame drops) — anchored to audioCtx.currentTime
- FALL_SPEED changes invalidated in-flight note timing — locked speed per-note at spawn
- Missed notes flew upward like completed notes — added distinct missed state (falls off screen)
- Targeting included missed notes — added missed filter

## How to Run

Open `index.html`. Click START. Type the falling words as they reach the blue hit line. Each correct keystroke plays a melodic note. Score based on timing accuracy. Combo multiplier rewards consistency.

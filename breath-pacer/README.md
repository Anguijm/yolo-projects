# Breath Pacer

A minimalist breathing exercise for your phone. OLED-black, synthesized tones, haptic feedback. The first mobile-first PWA in the collection.

## Features

- 4 breathing patterns: Box (4-4-4-4), 4-7-8 Relaxation, Calm (5-5), Energize (2-2)
- Expanding/contracting circle with CSS transform (hardware accelerated, 60fps)
- Phase-colored labels: blue=inhale, purple=hold, green=exhale
- Synthesized sine wave tones on phase transitions (396/432/528 Hz)
- Haptic vibration on phase changes (navigator.vibrate)
- Screen Wake Lock API keeps screen on during sessions
- WakeLock release event handling, re-acquisition on visibility change
- Session timer and cycle counter
- OLED black background (#000) for battery saving
- Delta-time cap (dt > 2s = 0) prevents rapid-fire catch-up after tab switch
- Tap circle OR button to start/stop
- Dual event handling (pointerdown + click) for iOS audio compatibility
- Mobile-first: viewport meta, apple-mobile-web-app-capable, touch-only controls
- No console errors, no keyboard required

## Bugs Fixed by Gemini Code Audit

- Tab inactive dt bug: returning after 30s caused rapid-fire phase transitions (capped dt)
- WakeLock leaked: repeated start/stop overwrote lock reference without releasing (added guard + release listener)
- iOS audio: pointerdown alone may not satisfy WebKit audio autoplay policy (added click fallback)

## How to Run

Open `index.html` on your phone. Tap the circle to begin breathing.

## What You'd Change

- Background ambient drone during breathing
- Custom pattern builder
- Session history with localStorage
- Dark/light theme toggle

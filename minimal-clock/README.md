# Minimal Clock

A fullscreen analog clock with 4 visual faces. Tap to cycle. Designed for nightstands.

## Features

- 4 clock faces, tap to cycle:
  - Classic: Swiss-design thin hands, red second hand, hour markers
  - Bauhaus: Three concentric arcs (blue hours, yellow minutes, red seconds)
  - Radar: Air traffic control green sweep with conic gradient trail, hour/minute blips
  - Binary: 6-column BCD display with glowing blue dots, decimal labels
- Smooth sweeping second hand (millisecond precision, no ticking)
- High-DPI canvas scaling (devicePixelRatio)
- All drawing relative to Math.min(W,H) — responsive on any screen
- Screen Wake Lock (with visibilitychange re-acquisition + user-gesture trigger)
- Preferred face saved in localStorage
- Label shows face name on switch, fades after 2 seconds
- createConicGradient fallback for older browsers
- Skip render when window minimized (W/H = 0)
- OLED black (#000), mobile-first, all PWA metas

## Improvements from Gemini Code Audit

- createConicGradient crashes on older browsers (added feature detection + fallback)
- Wake lock on load may fail without user gesture (added request on click)
- Rendering continues when minimized (added W/H = 0 skip)

## How to Run

Open `index.html` on your phone. Tap anywhere to cycle faces. Leave on nightstand.

## What You'd Change

- Date display option
- World time zones
- OLED burn-in protection (pixel shift)
- Alarm feature

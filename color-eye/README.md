# Color Eye

Point your phone camera at anything. Tap to capture its color. Get hex, RGB, HSL. Build palettes from the real world.

## Features

- Rear camera (environment mode) fills full screen
- Tap anywhere to sample the color at that point
- Accurate coordinate mapping for object-fit: cover video scaling
- 3x3 pixel averaging (single getImageData call) for noise reduction
- Hex, RGB, HSL conversion displayed simultaneously
- Dynamic text contrast (white on dark, black on light via BT.601 luminance)
- One-tap copy for each format (Clipboard API + iOS fallback)
- Save colors to palette (localStorage, max 20, deduped)
- Palette dots at top — tap to copy hex
- Haptic vibration on color sample
- Camera permission error handled (falls back to message)
- MediaDevices existence check (graceful on HTTP)
- Toast notifications with clearTimeout race fix
- Array.isArray guard on localStorage palette
- OLED black UI, mobile-first, all PWA metas
- Click events only, no pointerdown
- willReadFrequently canvas optimization

## Improvements from Gemini Code Audit

- 9x getImageData calls replaced with single call for 3x3 area (major perf win)
- Added navigator.mediaDevices existence check (prevents crash on HTTP)
- iOS clipboard fallback uses setSelectionRange(0, 99999)

## How to Run

Open `index.html` on your phone (HTTPS required). Allow camera. Point and tap.

## What You'd Change

- Complementary/analogous palette generation from sampled color
- Camera freeze frame on tap (currently stays live)
- Color name lookup (nearest named CSS color)
- Export palette as PNG swatch card

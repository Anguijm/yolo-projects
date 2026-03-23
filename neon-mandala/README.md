# Neon Mandala

Radial symmetry drawing tool with neon glow and fading trails. Draw anywhere and watch your strokes reflected across 2-24 symmetry segments, creating mesmerizing mandala patterns that slowly fade to black.

## Features

- Radial symmetry with adjustable segments (2-24)
- Neon glow effect via Canvas shadowBlur
- Auto-cycling HSL color based on time + distance from center
- Ephemeral fade-out creates ghost trails
- Adjustable glow intensity, stroke width, and fade speed
- High-DPI canvas rendering (sharp on Retina)
- setPointerCapture for smooth drawing beyond canvas edges
- Glassmorphic floating controls (fade in on hover)
- OLED black, mobile-first, touch-friendly

## Bugs Fixed by Gemini Audit

- High-DPI canvas overflow: canvas.width scaled by DPR but CSS dimensions not set, causing page overflow on Retina screens
- Mouse coordinate offset: used raw clientX instead of accounting for canvas bounding rect position
- Missing parseInt radix parameter

## How to Run

Open `index.html`. Draw anywhere on the screen. Adjust segments, glow, width, and fade with the controls at the bottom (hover to reveal).

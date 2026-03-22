# Gradient Studio

A fullscreen gradient designer. The preview IS the UI. Pick colors, choose type, copy CSS. Mobile-first PWA.

## Features

- Fullscreen gradient preview (the entire screen IS the gradient)
- 4 color pickers with live update
- 3 gradient types: linear, radial, conic
- Angle slider for linear/conic gradients
- 2/3/4 color stop selector
- Randomize button generates pleasing random gradients (HSL with constrained S/L)
- Copy CSS to clipboard with fallback for non-HTTPS
- Save up to 50 favorites to localStorage (with Array.isArray corruption guard)
- Load saved gradients (resets all 4 color slots to prevent stale leftovers)
- Delete saved gradients individually
- Toast notifications with race condition fix (clearTimeout)
- Glassmorphic floating control panel (backdrop-filter blur)
- HSL-to-hex conversion for randomization
- OLED-safe, mobile-first, all PWA metas
- Click events only (no pointerdown — new process rule)
- No console errors

## Bugs Fixed by Gemini Code Audit

- Toast race condition: rapid clicks queued multiple timeouts (added clearTimeout)
- Stale colors on load: unused color slots kept previous values (reset to random)
- Corrupted localStorage: non-array data caused crashes (added Array.isArray guard)

## How to Run

Open `index.html` on your phone. Pick colors, tap Randomize, copy the CSS.

## What You'd Change

- Drag color stops on a gradient bar (position control)
- Preset palette library (popular gradient collections)
- Export as PNG/SVG image
- Undo/redo history

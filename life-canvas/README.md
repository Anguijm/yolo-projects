# Life Canvas

Conway's Game of Life with age-based gradient coloring. Newborn cells spark cyan, aging cells fade to deep purple. Ghost trails linger where cells die.

## Features

- Conway's Game of Life with standard rules (B3/S23)
- Cell age tracking (Int16Array) — survived cells age up each generation
- HSL gradient coloring: hue shifts cyan→purple with age, lightness dims
- Ghost trails: dead cells leave fading purple afterglow (Float32Array)
- Ghost decay pauses when simulation is paused
- Toroidal wrapping (modulo edges — cells wrap around)
- Tap to toggle cells, drag to paint
- 6 pattern presets: Glider, Spaceship (LWSS), Pulsar, Gosper Glider Gun, R-Pentomino, Random Fill
- Stamp mode: select pattern, click to place
- Play/Pause, single Step, Clear, speed slider
- Generation counter
- Debounced resize (200ms)
- touchmove prevention scoped to canvas only (not whole document)
- pointercancel handling prevents stuck paint state
- OLED black, mobile-first, all PWA metas

## Improvements from Gemini Code Audit

- Ghost decay only runs when playing (was tied to render = faded during pause)
- touchmove scoped to canvas (was on document — blocked all page scrolling)
- Added pointercancel handler (prevents stuck painting on system interrupts)

## How to Run

Open `index.html` in a browser. Tap cells or select a pattern, then Play.

## What You'd Change

- Resize preserves board state (currently resets)
- Rule customization (different B/S rulesets)
- Speed presets (slow/normal/fast/turbo)
- Cell population chart over time

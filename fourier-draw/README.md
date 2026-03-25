# Fourier Draw

Draw any shape freehand, watch it decomposed into spinning epicycles that reconstruct your drawing. The Discrete Fourier Transform extracts frequencies from your path, and rotating circles of decreasing size trace it back.

## Features

- Freehand drawing on full-screen canvas
- DFT computation extracts frequencies, amplitudes, and phases
- Epicycle animation reconstructs the drawing with spinning circles
- Adjustable number of circles (1 to N) — watch accuracy increase
- Speed control for animation
- 4 preset shapes: Star, Heart, Note, Infinity
- Path resampling for even point distribution
- Circles sorted by amplitude (largest first) for clean visual
- Neon trace line with glow effect
- OLED dark theme, mobile-first with pointer events

## How to Run

Open `index.html`. Draw a shape on the screen. Release to see the DFT epicycles reconstruct your drawing. Adjust the circle count slider to see how adding frequencies improves accuracy. Try the preset shapes for instant demos.

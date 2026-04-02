# Epicycles — Fourier Drawing Machine

Draw any closed shape. Watch spinning circles reconstruct it.

## What it does

Uses the Discrete Fourier Transform to decompose any 2D path into a set of rotating circles (epicycles). Each circle spins at an integer frequency; stacked together they trace out the original shape with mathematical precision.

- **Draw mode**: draw any closed shape with your finger or mouse
- **Animate mode**: 128 DFT coefficients sorted by amplitude drive the epicycle chain
- **Controls**: toggle circles, trace, ghost overlay; adjust speed (0.1x–5x) and active epicycle count (1–100%)
- **8 presets**: Circle, 5-pointed Star, Heart, Figure-8, Square, Trefoil, Lissajous (3:2), Spiral

## How to run

Open `index.html` in any browser. No server needed, no dependencies.

## Technical details

- Pure Canvas 2D, zero dependencies
- O(N²) DFT computed on 128 resampled points (fast enough to run instantly)
- `chain()` computed once per frame and shared between physics and render passes
- `setPointerCapture` for correct touch tracking across the drawing surface
- DPR-aware canvas for crisp Retina rendering

## What to change

- **N_SAMPLES** (line ~480): increase to 256 for finer detail (slower DFT, more epicycles)
- **speed range**: edit `min`/`max` on `#speed` input
- Add more presets in the `PRESETS` object — any function returning `[{x,y}]` array works

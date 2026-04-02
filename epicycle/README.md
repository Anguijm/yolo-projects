# Epicycle — Fourier Drawing Visualizer

Draw anything, watch rotating circles redraw it.

Computes the Discrete Fourier Transform of your drawing and plays it back as a cascade of concentric rotating circles (epicycles). Each circle rotates at a different frequency; their combined tip traces your original shape. Fewer circles = rough approximation; all circles = mathematically exact reconstruction.

## How to run

Open `index.html` in any browser. No server needed.

## How to use

1. **Draw** — click/touch and drag on the canvas to draw any shape
2. **Analyze** — press the Analyze button (or `A`) to compute the DFT
3. Watch the epicycles spin and redraw your shape
4. **Circles slider** — drag left for coarse approximation, right for exact reconstruction
5. **Presets** — click Heart, Star, ∞, Rose, or Fish to see built-in parametric curves
6. **Save PNG** — export the current frame
7. **Space** — pause/resume

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| D | Start drawing (clears canvas) |
| A | Analyze drawing |
| C | Clear |
| Space | Pause / Resume |
| + / = | More circles (+5) |
| - | Fewer circles (-5) |

## Math

Each drawn point is treated as a complex number z_n = x_n + i·y_n. The DFT gives N complex coefficients, each with an amplitude and phase. Sorting by amplitude (largest first) and plotting as nested rotating arms produces the epicycle visualization. The tip of the innermost arm traces the original path — exactly when all N terms are used, approximately when fewer.

## What to change

- **MAX_SAMPLES**: controls DFT resolution (currently 512). Higher = slower compute, smoother paths.
- **MIN_MOVE_SQ**: minimum pixel distance between recorded points (currently 9px²). Lower = more detail captured.
- **Presets**: add more parametric curves in the `PRESETS` object.

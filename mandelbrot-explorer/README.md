# Mandelbrot Explorer

Interactive Mandelbrot/Julia set explorer in a single HTML file. Zero dependencies.

## Features

- Smooth coloring with normalized iteration count
- 6 color palettes (classic, fire, ocean, neon, grayscale, rainbow)
- Mouse wheel zoom toward cursor
- Click-drag to pan
- Double-click to zoom in
- Progressive rendering (4x4 blocks during drag, debounced full render)
- Julia mode toggle with interactive C picking (hold Shift over Mandelbrot)
- Iteration depth slider (50-2000)
- PNG export
- Keyboard shortcuts: +/- to zoom, R to reset
- Uint32Array pixel writes for performance
- Reusable ImageData buffer (no GC pressure)

## How to Run

Open `index.html` in any modern browser.

## What You'd Change

- Web Worker for background rendering (prevents UI freeze at 4K)
- WebGL fragment shader for GPU-accelerated rendering
- Bookmark/share specific coordinates via URL hash

# Voronoi Forge

Interactive Voronoi diagram generator. Click to add seed points, drag to reshape cells in real-time. Brute-force nearest-seed pixel rendering with edge detection and multiple color modes.

## Features

### Voronoi Rendering
- Brute-force nearest-seed calculation per pixel
- Edge detection via distance differential (nearest vs second-nearest)
- 4 color modes: Vivid, Pastel, Monochrome, Distance Shade
- Distance shade darkens cells further from their seed
- 2x downscale rendering with pixelated upscale for performance
- Toggle edges and seed dots independently

### Interaction
- Click empty space to add new seed points
- Drag existing seeds to reshape cells in real-time
- Right-click to delete nearest seed
- Random 20 button generates instant showcase
- Clear button resets

### Architecture
- ImageData pixel buffer for brute-force Voronoi (no Fortune's algorithm, no external libs)
- Debounced rendering (16ms) for smooth drag interaction
- Off-screen canvas for scaled rendering + imageSmoothingEnabled=false upscale
- Color parsing via ctx.fillStyle normalization trick
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Click to add points. Drag them around to watch cells reshape. Right-click to delete. Try different color modes. Hit Random for instant beautiful tessellations.

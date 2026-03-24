# Dither Forge

Image dithering tool. Upload a photo, apply classic dithering algorithms, choose retro color palettes, and download the result as pixel art.

## Features

### Dithering Algorithms
- **Threshold** — simple luminance cutoff
- **Floyd-Steinberg** — error diffusion (classic smooth dithering)
- **Atkinson** — error diffusion with 6/8 spread (sharper, classic Mac look)
- **Bayer 4x4** — ordered dithering (crosshatch pattern)
- **Bayer 8x8** — ordered dithering (finer pattern)

### Color Palettes
- 1-Bit B&W (black and white)
- GameBoy (4 olive greens)
- CGA (black, cyan, magenta, white)
- Amber CRT (black to amber gradient)
- Cyberpunk (deep purple to neon)

### Image Processing
- Float32Array buffer for error diffusion (prevents Uint8ClampedArray truncation)
- Nearest-color matching via Euclidean RGB distance
- Brightness and contrast pre-processing sliders
- Pixel scale slider (downscale → dither → pixelated upscale)
- Procedural sample image for instant demo

### Interaction
- Drag-and-drop or click-to-upload image input
- Real-time re-dither on any parameter change (debounced 50ms)
- Download result as PNG via toBlob
- dragenter/dragover/drop handlers for reliable file drop

### Architecture
- Canvas-based pixel manipulation via getImageData/putImageData
- imageSmoothingEnabled=false for crisp pixelated upscale
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Error diffusion directly modified Uint8ClampedArray (truncated accumulated error → banding in dark/bright areas) — switched to Float32Array intermediate buffer
- Diffusion now reads from float buffer, writes final color to Uint8 output

## How to Run

Open `index.html`. Click "Sample Image" or upload your own photo. Select an algorithm and palette. Adjust pixel scale, brightness, and contrast. Download the result.

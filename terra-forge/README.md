# Terra Forge

Procedural terrain generator with Simplex noise, biome mapping, and hillshading. Generate infinite unique landscapes with real-time parameter control.

## Features

### Terrain Generation
- Custom Simplex noise implementation (no external libraries)
- Fractional Brownian Motion (fBm) with configurable octaves for natural detail
- Dual noise layers: elevation map + moisture map
- 13 biomes determined by elevation × moisture lookup (Deep Ocean → Snow)
- Island mode with radial falloff mask
- Continent mode without edge masking
- Seeded PRNG for reproducible worlds

### Visual Polish
- Hillshading from neighbor elevation gradients — faux-3D topographic depth
- Coastline shadow fix: water elevation clamped to sea level in shade calculation
- ImageData pixel buffer for high-performance rendering
- Half-resolution rendering with CSS pixelated upscale for smooth slider interaction

### Interactivity
- Real-time sliders: sea level, frequency, octaves, moisture bias, hillshade intensity
- Hover tooltip showing biome name, elevation %, and moisture %
- New Seed button for infinite variety
- Island / Continent mode toggle
- Debounced regeneration (80ms) for smooth slider dragging

### Architecture
- Custom Simplex noise + seeded PRNG (Lehmer/Park-Miller)
- Float32Array elevation and moisture maps
- Zero external dependencies
- Single-file HTML
- Glassmorphism auto-hiding control panel
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Zero seed broke PRNG (multiplicative PRNG produces constant 0 from seed 0) — clamped to Math.max(1, ...)
- Harsh coastline shadows (hillshade used deep water elevation for slope) — clamped water neighbors to seaLevel

## How to Run

Open `index.html`. Adjust sliders to reshape the world. Click "New Seed" for a completely different landscape. Hover to explore biome details. Toggle Island/Continent modes.

# Chladni Sim

Interactive Chladni figure simulator. Sand particles settle onto the nodal lines of a vibrating plate, forming the geometric patterns discovered by Ernst Chladni in 1787.

## What it does

- 2,500 sand particles animate on a square virtual plate
- Physics: each particle is pushed toward nodal lines where plate displacement = 0
- The force is `-Z * ∇Z` — a gradient flow toward Z=0 (nodal lines of the mode shape)
- Mode shapes use cosine standing waves: `cos(m·π·x) · cos(n·π·y)` (free-plate boundary)
- **M/N sliders** — control the number of half-waves on each axis
- **MIX** — blend in the rotated mode shape for richer patterns
- **NOISE** — how energetically the sand moves (lower = tighter patterns)
- **TAP CANVAS** — scatter all particles, watch them resettle
- 8 preset modes for classic Chladni figures

## How to run

Open `index.html` directly in a browser — no server needed.

## Technical notes

- Float32Array SoA for particles (zero GC in update loop)
- Pre-allocated density map, ImageData, and OffscreenCanvas (no per-frame allocation)
- Density map → soft-glow rendering via additive pixel accumulation
- High-DPI canvas with devicePixelRatio scaling
- Analytic gradient of the mode field (no finite differences)

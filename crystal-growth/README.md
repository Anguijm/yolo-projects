# Crystal Growth

DLA (Diffusion Limited Aggregation) crystal simulator. Random walkers wander until they touch the aggregate and stick — growing fractal crystals that look like snowflakes, coral, lightning, and ice.

## How to run

Open `index.html` in any modern browser. No server required.

## What it does

- Particles do Brownian random walks from the outer edge inward
- When a walker touches the growing crystal it sticks, adding to the aggregate
- Rotational symmetry (2×–8×) mirrors each added pixel, creating snowflakes and star fractals
- **Tap the canvas** to plant additional seed points — creates branching chaos
- **H** to hide the UI for clean screenshots, **Space** to pause, **R** to reset

## Controls

| Control | Effect |
|---|---|
| SYMM buttons | Set rotational symmetry order (6× = snowflake, 4× = crystal cross) |
| RADIAL / AGE / ICE / FIRE | Color mode: angle, growth cycle, blue-to-white ice, red-to-yellow lava |
| SPEED | Steps per animation frame (higher = faster growth) |
| WALKERS | Number of simultaneous random walkers |
| STICKY | Sticking probability on contact (lower = denser, rounder crystal) |
| GLOW | Glow halo intensity around crystal branches |
| SAVE PNG | Export current crystal as PNG (no UI overlay) |

## What I'd change

- Add a "burst" button to fast-forward 10,000 steps for large crystals
- WebGL offscreen rendering for massive crystal size (>500k pixels slows down)
- Edge seeds (grow inward from the frame edges) for different topologies
- Animated color cycling on the live aggregate (requires per-pixel re-render)

# Particle Life

Emergent artificial life simulation. Thousands of colored particles follow simple attraction/repulsion rules, spontaneously forming cells, worms, swarms, and ecosystems. Mesmerizing, interactive, endlessly replayable.

## Features

- 1500+ particles across 6 color groups at 60fps
- Configurable 6x6 attraction/repulsion matrix (click cells to adjust)
- Emergent behavior: cells, chains, predator-prey, swarms from simple rules
- 4 presets: Cells, Worms, Swarm, Ecosystem
- Randomize button for unpredictable new lifeforms
- Mouse interaction: left-click attracts, right-click repels
- Toroidal wrap (particles wrap around edges for infinite-feeling space)
- Close-range repulsion prevents particle collapse
- Float32Array particle data (SoA layout for cache performance)
- Batch rendering by color with fillRect (minimized state changes)
- Pre-calculated constants (friction multiplier, repulse radius, inverse distance)
- Trail effect via semi-transparent canvas clear
- Glassmorphism control panel (auto-hides, hover to reveal)
- Adjustable: particle count (200-3000), friction, interaction radius, force multiplier
- FPS counter
- OLED black, mobile-first, all PWA metas

## How It Works

Each color group has attraction/repulsion values toward every other color (the 6x6 matrix). Positive = attract, negative = repel. Particles within the interaction radius experience forces based on these rules. At very close range, all particles repel to prevent collapse. Friction dampens velocity. The result: complex, organic, life-like behavior emerges from incredibly simple rules.

## Performance

- O(N²) particle interactions with optimized inner loop
- Typed arrays (Float32Array/Uint8Array) for contiguous memory access
- Batch color rendering eliminates per-particle fillStyle changes
- fillRect instead of arc for 3x rendering speedup
- Pre-calculated divisions and constants outside inner loop

## How to Run

Open `index.html`. Watch the particles self-organize. Click "Randomize" for new rules. Try the presets. Click the matrix cells to fine-tune interactions. Left-click the canvas to attract particles, right-click to repel.

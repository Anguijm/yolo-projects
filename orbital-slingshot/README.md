# Orbital Slingshot

A gravity physics puzzle game. Guide your probe to the target by harnessing gravitational slingshots around planets.

## How to Play

Open `index.html` in a browser.

**Drag from the probe to aim** — the dotted cyan line shows your predicted trajectory. **Release to launch.** Use gravity to curve your path around planets and reach the glowing green target.

- Low shots = better score
- R = reset probe, ◀▶ = change level
- Arrow keys also navigate levels

## 6 Levels

1. **First Contact** — one planet, simple curve
2. **Swing By** — complete loop-around required
3. **Binary** — two planets, sequential slingshots
4. **The Crossing** — heavy planet + small steering body
5. **Figure Eight** — thread between two equal masses
6. **The Gauntlet** — four planets, find the gap

## Physics

- Velocity Verlet integration (stable, energy-conserving)
- Softened gravity (`r² + ε` denominator prevents singularities)
- 3 physics substeps per frame for accuracy
- 480-step trajectory preview runs ahead in real time

## Stack

Single HTML file. Zero dependencies. Canvas 2D rendering.

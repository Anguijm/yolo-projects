# fluid-sim

Real-time 2D fluid dynamics simulation using the Stable Fluids (Stam 1999) method — fully GPU-accelerated via WebGL2.

## What it does

Drag your mouse (or finger) across the screen to inject velocity and dye into the fluid. Watch incompressible Navier-Stokes dynamics: swirling vortices, pressure waves, diffusion, dissipation.

**Physics pipeline per frame:**
1. Splat — Gaussian injection of velocity + dye at pointer
2. Advect — Semi-Lagrangian advection (velocity self-advects; dye follows velocity)
3. Curl — Compute vorticity of velocity field
4. Vorticity confinement — Amplify spinning regions to prevent numerical diffusion from killing swirls
5. Divergence — Compute div(v) for the pressure solve
6. Pressure (Jacobi, 20 iterations) — Solve Poisson equation for pressure
7. Gradient subtract — Project velocity to divergence-free (incompressible)
8. Render — Display dye with selected colormap

## Color modes

- **Reactive** — Color = velocity direction (angle → hue), brightness = dye amount. Swirls become rainbows.
- **Fire** — Orange→yellow tone map. Turbulent red flames.
- **Ocean** — Deep blue to cyan to white foam.
- **Neon** — Cyan/magenta/green additive blending.

## Presets

- **Vortex** — 24-point circular velocity injection → tight spinning ring
- **Storm** — 8 random radial splats → chaotic turbulence
- **Streams** — 5 opposing horizontal flows → collision vortex streets
- **Fountain** — Upward spray from base → cascading dye

## Controls

- **Drag** — paint velocity + dye
- **Color buttons** — switch colormap
- **Preset buttons** — inject demo patterns
- **Clear** — reset all fluid state
- **Save PNG** — download current frame

## How to run

Open `index.html` directly in any modern browser (Chrome, Firefox, Safari, Edge). No server required.

WebGL2 is required. Tested on Chrome 120+, Firefox 120+, Safari 17+.

## What to change

- `SIM_RES` (128) — higher = more detailed physics, slower
- `DYE_RES` (256) — higher = sharper dye, more VRAM
- `ITERATIONS` (20) — more Jacobi iterations = more accurate pressure solve
- `CURL` (25) — higher = more aggressive vorticity confinement (more swirls)
- `VEL_DISS` / `DYE_DISS` — closer to 1.0 = longer persistence

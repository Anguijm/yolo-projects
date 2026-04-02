# FIELD LINES — Magnetic Field Visualizer

Interactive electromagnetic field simulator. Place magnetic poles and current-carrying wires on a canvas and watch the field visualize in real time.

## How to run

Open `index.html` directly in any browser. No server required.

## What you built

- **Tap canvas** to place the currently selected source type (N pole, S pole, Wire+, Wire−)
- **Drag** any source to move it — the field updates live
- **Tap a source** to select it, then adjust its strength via the slider or delete it

### Visualization modes
- **FIELD LINES** — streamlines traced with RK4 integration, with direction arrows
- **IRON FILINGS** — grid of oriented dashes aligned to the local field direction
- **FLUX DENSITY** — spectral heat map (dark → blue → cyan → white) showing |B|

### Presets
- **DIPOLE** — north-south pair (classic bar magnet field)
- **QUADRUPOLE** — 4 alternating poles showing saddle topology
- **2 WIRES** — parallel wires with opposing currents
- **SOLENOID** — row of wires approximating solenoid cross-section

### Particles
Toggle animated test charges that flow along field lines with glowing trails.

## Physics

- **Magnetic monopole** (N/S pole): B ∝ q·r̂/r²
- **Wire (current out/in)**: B ∝ I/r in tangential direction (right-hand rule)
- **Superposition**: fields from all sources added linearly
- Streamlines traced with 4th-order Runge-Kutta on the unit field vector

## What to change

- Increase line count (currently 16/12 per source) for denser field line displays
- Add dipole source type (two close monopoles) for true bar magnet behavior
- Add field magnitude colorization to the field lines themselves
- Add a configurable grid for equipotential lines

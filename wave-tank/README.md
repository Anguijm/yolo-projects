# wave-tank

2D wave equation simulator using the FTCS finite-difference scheme.
Place sources, draw barriers, and watch interference and diffraction patterns emerge in real time.

## What it is

Solves ∂²Z/∂t² = c²∇²Z on a 250×250 grid with:
- **Sponge boundary** — absorbs outgoing waves so the simulation feels infinite
- **Triple-buffer FTCS** — stable wave propagation (Courant number r=0.45)
- **EMA intensity mode** — time-averaged energy reveals the static interference pattern

## Presets

| Preset | What it shows |
|--------|--------------|
| POINT | Single source, circular wavefronts — the baseline |
| TWO SRC | Two coherent sources — Young's double-source interference pattern |
| DBL SLIT | Two-gap barrier — classic double-slit diffraction and interference |
| GRATING | 5-slit diffraction grating — sharper, narrower fringes |

## How to run

Open `index.html` in any modern browser. No server needed.

## Controls

- **DRAW modes**: SOURCE (place/remove), WALL (draw barriers), ERASE (clear barriers)
- **FREQ slider**: changes wavelength (λ readout shown next to slider)
- **VIEW modes**: WAVE (live peaks/troughs) vs INTENSITY (time-averaged energy — use this to see fringes clearly)
- **PAUSE**: freeze the simulation to study a pattern
- **SAVE PNG**: export the current view as a PNG

## Tips

- Switch to **INTENSITY mode** after loading a preset for the clearest interference fringes
- Adjust the **FREQ slider** to change wavelength — watch fringes compress/expand
- In **WALL mode**, drag to draw curved reflectors and cavities
- Add multiple sources manually to create custom interference setups

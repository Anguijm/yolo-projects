# LENIA — Continuous Life

A WebGL2-accelerated simulation of Lenia, a mathematical framework for continuous cellular automata developed by Bert Wang-Chak Chan. Unlike discrete Game of Life, Lenia uses a continuous state space [0,1], smooth ring-shaped convolution kernels, and Gaussian growth functions — producing emergent creatures that move, multiply, and interact.

## What You Built

- **6 species presets**: Orbium (canonical glider), Hydrogeminium, Geminium, Scutium, Random Soup, Clear field
- **Ping-pong FBO simulation**: WebGL2 shader runs the full Lenia convolution kernel every frame at 256×256 resolution
- **4 colormaps**: Cyan, Plasma, Green, Fire
- **Live parameter control**: Adjust growth mu/sigma, kernel mu/sigma, radius R, dt, and simulation speed in real time
- **Paint/Erase tools**: Draw activation directly onto the field
- **Screenshot export**: Save any frame as PNG
- **Hide UI mode**: Press H for fullscreen cinema view

## How to Run

Open `index.html` in any modern browser (Chrome 80+, Firefox 75+, Safari 15+). No server required.

Requires WebGL2 with `EXT_color_buffer_float` support (all modern desktop browsers).

## Controls

| Key | Action |
|-----|--------|
| Space | Pause/resume |
| P | Toggle paint mode |
| E | Toggle erase mode |
| R | Reset to initial state |
| H | Hide/show controls |
| S | Save PNG screenshot |

## The Math

Lenia update rule per timestep:
```
Z(x) = Σ K(‖x−y‖) · A(y) dy   (kernel convolution)
A'(x) = clip(A(x) + dt · G(Z(x)), 0, 1)
G(z)  = 2·exp(−4.5·((z−μ)/σ)²) − 1  (bell growth function)
K(r)  = exp(−4.5·((r/R−μₖ)/σₖ)²)    (ring kernel)
```

## What to Change

- Increase `W` and `H` from 256 to 512 for higher resolution (4× slower)
- Extend `MAX_R` in the GLSL step shader to support larger kernels (also increase slider max)
- Add more species from the Lenia paper: Hydrogeminium, Scutium gravidus, Gyrorbium, etc.
- Add URL hash serialization to share parameter configurations

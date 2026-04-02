# L-System Garden

Interactive Lindenmayer system explorer with turtle graphics. Write production rules, watch fractal plants and geometric curves grow with an animated drawing effect.

## What it is

L-Systems are a formal grammar invented by biologist Aristid Lindenmayer to model plant growth. A short set of recursive rules expands into sequences that, when interpreted as turtle graphics instructions, produce beautiful fractals — branching plants, space-filling curves, snowflakes.

## How to run

Open `index.html` directly in a browser. No server needed.

## Features

- **6 presets**: Dragon Curve, Fractal Plant, Koch Snowflake, Hilbert Curve, Sierpinski Triangle, Binary Tree
- **Live rule editor**: Add/remove/edit production rules, axiom, and angle — redraws instantly
- **Animated growth**: Each grow animates from root to tip with an ease-out curve
- **4 color modes**: Mono (cyan), Spectrum (rainbow), Depth (branch nesting), Age (brightness over time)
- **ITER / STEP sliders**: Control complexity (1–12 iterations) and scale
- **EXPORT**: Saves current canvas as PNG
- **SHARE**: Encodes full config in URL hash — copy/paste to share any L-system

## Syntax reference

| Symbol | Meaning |
|--------|---------|
| `F`, `G` | Draw forward one step |
| `+` | Turn right by angle |
| `-` | Turn left by angle |
| `[` | Push turtle state (start branch) |
| `]` | Pop turtle state (end branch) |
| `X`, `Y`, `A`, `B` | Variables (no draw, expand via rules) |

## What to change

- Add stochastic rules (randomly pick from multiple productions per symbol) for organic variation
- Add depth-dependent stroke width (thick trunk → thin twigs) for 3D-like realism
- Add 3D turtle graphics (pitch/yaw/roll) for true 3D fractals

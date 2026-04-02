# Slime Mold — Physarum polycephalum

A simulation of the slime mold organism using 30,000 autonomous agents. Each agent senses chemical trails ahead and to each side, turns toward the strongest signal, moves forward, and deposits trail. The trail diffuses and decays. Complex branching networks emerge spontaneously from these simple rules — mimicking actual Physarum polycephalum behavior.

## How to Run

Open `index.html` in a browser. The simulation begins immediately on the intro screen tap.

## Controls

| Action | Effect |
|--------|--------|
| Hold canvas | Paint food (attracts agents) |
| BLOOM | Agents start in a circle, pointing outward |
| SCATTER | Agents randomly distributed, random heading |
| RING | Agents on a ring, pointing inward |
| CLEAR | Clear all trails + scatter |
| SLIME/CYAN/FIRE/MONO | Switch colormap |
| PAINT ON/OFF | Toggle canvas paint interaction |
| SAVE | Export current frame as PNG |

**Keyboard:** `R` = bloom reset, `S` = scatter, `C` = cycle colormap, `P` = toggle paint, `Space` = scatter, `1/2/3` = presets

## How It Works

- **Agents (30,000)**: Each has a position and heading angle. Per tick: sense 3 points ahead (forward, left-front, right-front at 30° separation, 9 pixels away), rotate toward the strongest trail, move 1.3 pixels, deposit trail.
- **Trail grid (800×500)**: Float32Array. Deposit: `trail[i] = min(255, trail[i] + 5)`. Diffuse: 3×3 box filter. Decay: multiply by 0.96.
- **Double-buffer**: Two float arrays swapped each frame so diffusion reads clean input.
- **Rendering**: LUT lookup per pixel → `Uint32Array` over ImageData → `putImageData`. 400K pixels at 60fps.

## Performance

- Agent update: ~30K agents × 6 trig calls = ~180K trig ops/frame (~1ms)
- Diffusion: 400K cells × 9 reads = ~3.6M ops/frame (~3ms)
- Render: 400K LUT lookups + putImageData (~2ms)
- Total: ~6ms → runs at 60fps on mid-range hardware

## Colormaps

- **SLIME**: Black → dark green → lime yellow → white (looks like actual slime mold)
- **CYAN**: Black → deep teal → cyan → white (bioluminescence aesthetic)
- **FIRE**: Black → red → orange → yellow → white (volcanic networks)
- **MONO**: Pure grayscale

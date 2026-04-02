# Penrose — Aperiodic Tiling Explorer

Interactive Penrose tiling (P3 rhombus) explorer built with a Robinson triangle subdivision algorithm. The tiling has perfect 5-fold rotational symmetry but never repeats — it's a quasi-crystal.

## What it is

A Penrose P3 tiling using Robinson triangles:
- **Acute triangles** (36° apex) and **Obtuse triangles** (108° apex)
- Subdivision rule: acute → 1 acute + 1 obtuse; obtuse → 1 acute + 2 obtuse
- The ratio of fat to thin rhombuses converges to the golden ratio φ ≈ 1.618
- Starts with a 10-triangle "sun" pattern, auto-inflated to generation 5 (890 tiles)

## How to run

Open `index.html` in any browser. No server needed.

## Controls

- **INFLATE** — subdivide all tiles into smaller tiles (or double-tap canvas)
- **DEFLATE** — undo last subdivision
- **COLOR** — cycle through 4 color modes: Dual / Radial / Phase / Void
- **SAVE** — export as PNG
- **RESET** — return to gen 0 and auto-inflate to gen 5
- **Scroll / Pinch** — zoom in/out
- **Drag** — pan

## Generation counts

| Gen | Tiles   |
|-----|---------|
| 0   | 10      |
| 5   | 890     |
| 6   | 2,330   |
| 7   | 6,100   |
| 8   | 15,970  |

## Technical notes

- Uses Robinson triangle deflation in world-space (pan/zoom doesn't re-derive)
- Canvas 2D with batched fill paths for performance
- Color modes batch fills by color to minimize state changes
- Single HTML file, zero dependencies

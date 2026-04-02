# Powder World

A falling sand / powder simulator with 11 interacting materials. Cellular automaton physics running at 60fps.

## How to run

Open `index.html` in any browser. No server required.

## Materials

| Key | Material | Behaviour |
|-----|----------|-----------|
| 1   | SAND     | Falls, piles, sinks through liquids |
| 2   | WATER    | Flows sideways, turns to steam near fire |
| 3   | FIRE     | Spreads to wood/oil/plant, extinguished by water/ice |
| 4   | WOOD     | Immovable, ignites near fire |
| 5   | OIL      | Flows like water, floats on water, burns easily |
| 6   | STONE    | Completely immovable, acid-resistant |
| 7   | ACID     | Flows, dissolves anything except stone (acid also consumed) |
| 8   | ICE      | Melts near fire → water; slowly freezes adjacent water |
| 9   | PLANT    | Spreads to adjacent sand cells slowly |
| 0   | ERASE    | Removes material |

Smoke and steam are produced by interactions (not paintable directly).

## Controls

- **Draw** on canvas to place selected material
- **Toolbar buttons** to switch material
- **SIZE** — cycles brush radius 1→2→3→5→8
- **CLEAR** — wipe the canvas
- **PAUSE / RESUME** — freeze simulation
- **SAVE** — download canvas as PNG
- Keys **1-9, 0** — select material by number
- **C** — clear
- **Space** — pause/resume
- **+/-** — increase/decrease brush size

## What to try

- Pour WATER then add ICE nearby — watch it freeze
- Build a WOOD tower and ignite with FIRE — watch smoke billow
- Pour OIL on water — oil floats on top
- Drop ACID on anything — watch it eat through
- Draw PLANT seeds in SAND — they slowly colonise
- Fire + Water = Steam rising up

## Technical

- Single HTML file, zero dependencies
- Internal simulation grid scales to viewport (SCALE factor)
- Bottom-to-top scan, alternating L→R / R→L each frame to prevent drift
- `Uint8Array` grid + meta; `Uint32Array` pixel buffer via `ImageData`
- `image-rendering: pixelated` for sharp chunky pixels

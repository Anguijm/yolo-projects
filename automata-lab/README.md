# Automata Lab

Generalized cellular automata sandbox. Multiple rulesets, custom B/S rules, cell aging heatmap, pattern library, draw while running. The project we dodged for 20+ builds.

## Features

### Multi-Rule Engine
- **Conway's Life** (B3/S23) — classic emergence
- **HighLife** (B36/S23) — replicators
- **Seeds** (B2/S) — explosive growth
- **Day & Night** (B3678/S34678) — symmetrical patterns
- **Diamoeba** (B35678/S5678) — amoeba-like blobs
- **Brian's Brain** (3-state: on → dying → off) — expanding wavefronts
- **Custom** — type any B/S rule string (e.g. B368/S245)

### Cell Aging Heatmap
- New cells glow bright cyan
- Old cells shift through warm hues to deep purple
- Uint16Array age tracking (up to 65535 generations)
- Creates stunning visual maps of stable vs chaotic regions

### Pattern Library
- Glider — the classic spaceship
- Gosper Glider Gun — infinite stream generator
- Pulsar — period-3 oscillator
- R-pentomino — chaotic methuselah

### Interaction
- Draw/erase cells while simulation runs
- Adjustable brush size (1-5)
- Click toggles cell state
- Play/pause/step controls
- Speed slider (1-60 tps)
- Randomize and clear buttons

### Architecture
- Double-buffered Uint8Array grid (read current, write next, swap)
- Toroidal edge wrapping (patterns wrap around edges)
- Canvas-rendered with per-cell HSL coloring
- B/S rule string parser for custom rulesets
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Watch the Glider Gun fire. Select different rules to see fundamentally different behaviors. Draw patterns with your mouse. Try Brian's Brain for mesmerizing wavefronts. Type custom B/S rules.

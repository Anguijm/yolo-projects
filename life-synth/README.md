# LIFE-SYNTH

Conway's Game of Life as a generative music sequencer. A scanline sweeps across a 32×16 grid of cells — alive cells trigger musical notes. Enable EVOL and watch the CA evolve the pattern over time, turning stable oscillators into rhythms and gliders into traveling melodies.

## How to run

Open `index.html` in any modern browser. No server needed.

## How it works

- **Grid**: 32 columns (time steps) × 16 rows (pitches). Lowest row = lowest note.
- **Scanline**: Sweeps left-to-right one column per 16th note. Alive cells in the active column play their note.
- **EVOL**: When enabled, the CA rule runs once per full sweep (32 steps). The music evolves as the pattern does.
- **Draw**: Click/drag on the grid to toggle cells. First click on an alive cell erases; on a dead cell draws.

## Controls

| Control | Action |
|---------|--------|
| PAUSE / PLAY | Start/stop the scanline |
| EVOL | Toggle CA evolution per sweep |
| BPM | Tempo (40–240) |
| SCALE | Pitch set: Pentatonic / Major / Minor / Blues / Chromatic |
| WAVE | Oscillator: Sine / Triangle / Square / Sawtooth |
| RULE | CA rule: Life / HighLife / Seeds / Maze |
| CLR | Clear all cells |
| RND | Random 28% fill |
| Presets | Glider / Pulsar / Acorn / R-pentomino |

**Keyboard**: SPACE=play, E=evol, R=random, C=clear

## What's interesting to try

1. Load **PULSAR** preset → enable **EVOL** → the oscillator eventually destabilizes into chaos
2. Load **GLIDER** with **SEEDS** rule → explosive growth patterns drive unpredictable rhythms
3. **MAZE** rule creates long stable corridors — try with Minor scale for a cinematic drone
4. Draw a single row of cells → steady rhythm on one note → add cells in other rows for harmony

## Audio

Web Audio API synthesis with dynamics compression to prevent clipping on dense patterns. Higher octave rows have slightly lower gain for natural instrument voicing. Waveforms: sine (smooth), triangle (mellow), square (harsh), sawtooth (buzzy).

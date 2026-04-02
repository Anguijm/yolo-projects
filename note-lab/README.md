# Note Lab — Music Theory Explorer

Interactive music theory tool: play a 3-octave piano keyboard, highlight any scale, visualise the circle of fifths, and preview diatonic chords.

## What it does

- **3-octave playable piano** (C3–B5) with WebAudio synthesis (multi-partial piano-like tone)
- **10 scale types**: Major, Minor, Harmonic Minor, Dorian, Phrygian, Lydian, Mixolydian, Pentatonic Major/Minor, Blues
- **12 root notes** — change root with one click; piano highlights update instantly
- **Scale degree badges** — highlighted keys show their degree number (1–7)
- **Circle of fifths** — dual-ring canvas showing major (outer) and relative minor (inner) keys; current scale highlighted
- **Diatonic chord cards** — 7 chords for any 7-note scale, click to hear the triad
- **QWERTY keyboard** — `A S D F G H J K` = white keys (C4–C5), `W E T Y U` = black keys; SPACE = sustain pedal
- **Info bar** — shows current scale name, note names, and interval pattern (W/H/m3)

## How to run

Open `index.html` in any modern browser. No server needed.

```
open note-lab/index.html
```

## Tech

- Single HTML file, zero dependencies
- WebAudio API for synthesis (triangle wave harmonics, ADSR envelope)
- Canvas 2D for circle of fifths
- Pointer events with `setPointerCapture` for correct touch behaviour

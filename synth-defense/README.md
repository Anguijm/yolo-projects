# Synth Defense

Musical tower defense game. Towers play pentatonic synth notes quantized to 120 BPM. Your defense becomes a procedural composition. Single HTML file, zero dependencies.

## Features

- 3 tower types:
  - **Bass** (magenta square) — Square wave, low octave, fires on quarter notes, high damage
  - **Melody** (cyan circle) — Sine wave, mid octave, fires on 8th notes, medium damage
  - **Arp** (yellow triangle) — Triangle wave, high octave, fires on 16th notes, fast low damage
- Towers play pentatonic scale notes via Web Audio API oscillators
- Tower Y position maps to note pitch — place towers musically!
- All firing quantized to 120 BPM global clock
- DynamicsCompressor prevents audio clipping with many towers
- Fixed serpentine path, wave-based enemy spawning
- Gold economy: earn per kill, spend on towers
- Object-pooled projectiles (200) and particles (500)
- Neon glow via `globalCompositeOperation = 'lighter'`
- Motion trails, beat pulse indicator bar
- Keyboard shortcuts: 1/2/3 for tower types

## How to Run

Open `index.html` in a browser. Click "Initiate Vibe Check" to start.

## What You'd Change

- Drag-to-preview tower placement with range indicator
- More tower types (reverb delay, filter sweep)
- Enemy types with resistances
- Track export (record the generated audio)

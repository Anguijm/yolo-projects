# Drum Lab

A drum synthesizer + step sequencer. 4 tracks, 16 steps. Every sound built from scratch using Web Audio — no samples. Shape each drum live with parameter knobs. Single HTML file, zero dependencies.

## Features

- 4 synth drum tracks: Kick (sine sweep), Snare (tone + filtered noise), Hi-Hat (bandpass noise), Clap (burst noise)
- Per-track parameter knobs: pitch, decay, noise mix, filter frequency, burst spread
- Per-track volume slider
- 16-step grid with click-to-toggle and sound preview
- BPM slider (60-200)
- Swing control (lengthens downbeats, shortens offbeats)
- Lookahead scheduler (100ms window, 25ms check interval)
- DynamicsCompressor on master bus
- Cached noise buffer (created once, reused for all percussion — zero GC per hit)
- Safe volume clamping (prevents exponentialRamp crash at zero)
- Randomize button with per-track density distributions
- Pattern save/load via localStorage
- Step highlight synced to audio timing
- Space bar toggles play/stop
- AudioContext.resume() for browser autoplay compliance

## Bugs Fixed by Gemini Code Audit

- Swing math reversed AND caused tempo drift (even/odd swapped, asymmetric add/subtract)
- Zero volume crashed exponentialRampToValueAtTime (clamped to 0.001 minimum)
- Noise buffer recreated every drum hit (now cached once in initAudio)
- DOM highlight queried all steps every tick (now tracks previousStep)

## How to Run

Open `index.html` in a browser. Click steps, press Play.

## What You'd Change

- Per-track oscilloscope waveform preview (AnalyserNode)
- More drum types (toms, rimshot, cowbell)
- Pattern chain (play A then B)
- Export as WAV

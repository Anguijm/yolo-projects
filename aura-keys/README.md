# Aura Keys

Polyphonic synthesizer keyboard playable via QWERTY keyboard and touch. 2 octaves, 4 waveforms, octave shifting, delay effect. All audio synthesized via Web Audio API.

## Features

- 2-octave keyboard with white and black keys
- QWERTY mapping: A-S-D-F-G-H-J (white), W-E-T-Y-U (black), K-L-;-' (upper octave)
- Multi-touch/mouse support with glissando (slide across keys)
- Polyphonic — play full chords simultaneously
- ADSR envelope with setTargetAtTime release (no audio clicks/pops)
- 4 waveform types: sine, triangle, sawtooth, square
- Octave shift (C1-C7)
- Toggleable delay effect (feedback delay network)
- Audio node disconnect on note stop (prevents memory leaks)
- Modifier key passthrough (Ctrl/Cmd/Alt don't trigger notes)
- Stop all notes on window blur (prevents stuck notes on tab switch)
- Touch glissando with preventDefault (prevents page scroll)
- Equal temperament tuning (A4 = 440Hz)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- exponentialRampToValueAtTime crashed when gain was 0 (fast click/release) — switched to setTargetAtTime which safely approaches zero
- Notes stuck when switching tabs (keyup never fires) — added window blur → stopAll
- Modifier keys (Ctrl+A) played notes and blocked browser shortcuts — added ctrlKey/metaKey/altKey guard
- Audio nodes not disconnected on stop — added disconnect() to prevent memory leaks
- Touch glissando scrolled page — added preventDefault on pointermove

## How to Run

Open `index.html`. Play with QWERTY keys (A=C, W=C#, S=D...) or tap/click the on-screen keyboard. Select waveform, shift octave, toggle delay.

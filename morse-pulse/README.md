# Morse Pulse

Brutalist Morse code trainer using the Koch method with Farnsworth timing. Listen to synthesized Morse, type the letter. Pool expands silently as accuracy improves.

## Features

- Koch method: starts with K and M, adds characters at 90% accuracy (rolling 20)
- Farnsworth timing: characters play at 20 WPM, spacing stretched to 10 WPM effective
- Web Audio synthesized tones (550Hz sine, click-free 5ms envelope)
- Error feedback: low 150Hz square wave thud, replays correct answer with visual aid
- History resets on level-up to prevent cascading progression
- Minimal HUD: WPM, accuracy %, pool size
- Replay button for re-hearing current character
- Brutalist aesthetic: pure black, white monospace, zero decoration
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Cascading level-up: history not cleared on progression caused instant multi-level jumps (now resets)
- Farnsworth timing function was defined but never called (now used for inter-round delay)
- Visual aid (letter = morse) reverted before replay audio finished (moved revert into playMorse callback)
- Audio envelope could crash at high WPM (dynamic ramp = min(5ms, duration/4))

## How to Run

Open `index.html`. Press space or tap to start. Listen to the Morse beeps, type the correct letter. Get 90% accuracy to unlock new characters.

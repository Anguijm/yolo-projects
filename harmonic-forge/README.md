# Harmonic Forge

Interactive music theory explorer and chord progression builder. Circle of Fifths with clickable key segments, diatonic chord display, 8-slot progression sequencer, and looping playback. Learn theory by hearing it.

## Features

### Circle of Fifths
- 12 major keys (outer ring) + 12 relative minor keys (inner ring)
- Click any key to hear its root chord and switch the active key
- Diatonic chords highlighted on the circle
- Visual feedback: active key (blue), diatonic neighbors (dim blue)

### Diatonic Chords
- Shows all 7 diatonic chords (I, ii, iii, IV, V, vi, vii°) for the selected key
- Click any chord to hear it and add it to the progression
- Roman numeral + chord name display
- Visual pulse on the currently playing chord

### Progression Sequencer
- 8-slot timeline for building chord progressions
- Click diatonic chords to add them
- Click × to remove individual chords
- Click slots to preview individual chords
- Play/stop/clear controls
- Adjustable BPM (80/100/120/140)

### Preset Progressions
- Pop (I-V-vi-IV) — the universal pop hook
- Jazz (ii-V-I) — the jazz turnaround
- Sad (i-iv-VII-III) — melancholic progression
- Rock (I-IV-V-V) — classic rock
- Pachelbel Canon (I-V-vi-iii-IV-I-IV-V) — the famous 8-chord progression

### Audio
- Soft triangle+sine synth with slight detune for warmth
- Strum delay (40ms between chord tones) for musical feel
- ADSR envelope via setTargetAtTime release (no clicks)
- Audio node cleanup via onended

### Architecture
- DOM-based UI (no Canvas) — pure CSS/HTML for circle and controls
- Web Audio API for all synthesis
- Chord theory computed from intervals (no hardcoded frequency tables)
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Click keys on the circle to explore. Click the diatonic chord buttons to hear them and add to the timeline. Hit Play to loop your progression. Try the presets to hear famous chord patterns.

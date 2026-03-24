# Neon Runner

**Project #100 — The Grand Finale.** A complete platformer game engine built from scratch in a single HTML file. Three levels, full physics, particles, synthesized audio, and the game type we dodged for 99 builds.

## Features

### Physics Engine
- AABB tile collision with separate X/Y axis resolution
- Gravity with terminal velocity
- Acceleration/deceleration-based horizontal movement
- Collision resolution based on actual movement direction (not velocity sign — prevents zero-velocity wall clipping)

### Modern Platforming Feel
- **Coyote time** (5 frames) — jump briefly after leaving a ledge
- **Jump buffering** (5 frames) — queue a jump before landing
- **Variable jump height** — release early for short hops (velocity capped, not dampened)
- **Squash and stretch** — player compresses on land, stretches on jump

### Visual Polish
- Procedural parallax background (stars + buildings at different scroll rates)
- Particle system: dust on jump/land, sparks on coin collect
- Neon glow via Canvas shadowBlur
- Smooth lerp camera following player
- Only renders visible tiles (culled to viewport)

### Audio
- Synthesized Web Audio: jump (sine pitch up), coin (dual-tone arpeggio), death (square pitch down)
- Audio node cleanup via onended disconnect

### Game Design
- 3 hand-crafted levels with progressive difficulty
- Spikes (triangles), coins (collectibles), goal (green portal)
- Death counter and completion time
- Level 3 layout references "100"
- Touch controls for mobile (3-zone: left, jump, right)
- Arrow keys / WASD / Space for desktop

### Architecture
- Zero external assets — all graphics are Canvas draw calls
- Single-file HTML with embedded CSS and JS
- Fixed game resolution (320×200) scaled to fit any screen
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Variable jump height used continuous 0.5× damping (jerky mid-air halt) — capped velocity once to -3
- X collision resolved based on vx sign (fails at vx=0) — now uses previous position comparison
- inputJump() polled twice per frame — cached to single variable

## How to Run

Open `index.html`. Press any key or tap to start. Arrow keys/WASD to move, Up/Space to jump. Reach the green goal on each level. 3 levels, death counter, completion timer.

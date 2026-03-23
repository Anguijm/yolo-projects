# Neon Shatter

Brick breaker arcade game with neon glow aesthetic. Bounce the ball off your paddle to destroy bricks. Paddle position affects ball angle. Progressive levels with increasing difficulty.

## Features

- Canvas-rendered breakout with fixed aspect ratio scaling
- Paddle-relative bounce angles (hit edge = sharper angle)
- Circle-to-AABB collision detection for bricks
- Direction-aware collision response (prevents ball trapping in bricks)
- Ball trailing effect (newest = brightest)
- Particle explosions on brick destruction
- Neon glow via Canvas shadowBlur on ball, paddle, and bricks
- 6 brick color tiers per level
- Progressive difficulty (more rows + faster ball per level)
- Smooth keyboard input via held-key tracking (not key repeat)
- Mouse, touch, and arrow key paddle control
- Synthesized audio (sine bounce, square pitch-drop break)
- Score (10 × level per brick), lives (3), level counter
- Delta-time capped game loop (prevents physics explosions on tab return)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Trail rendering inverted: oldest points were brightest (fixed ratio calculation so newest = brightest)
- Keyboard stuttery: relied on OS key repeat (switched to held-key map with continuous dt-based movement)
- Brick collision could trap ball: velocity inversion didn't check direction (now forces velocity AWAY from brick center)
- Unused trail.age computation removed

## How to Run

Open `index.html`. Click/tap to start. Move mouse/finger or use arrow keys to control paddle. Click/tap to launch ball. Break all bricks to advance levels.

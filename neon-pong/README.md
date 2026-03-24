# Neon Pong

Classic Pong vs AI with neon glow aesthetic. Ball trail, screen shake, increasing speed, and synthesized audio. First to 7 wins.

## Features

- Player (cyan, left) vs AI (magenta, right)
- Paddle-relative bounce angles (hit edge = sharper angle)
- Ball speeds up with each volley (capped at 10)
- Neon glow via Canvas shadowBlur on ball and paddles
- Ball trailing effect (fading position history)
- Screen shake on paddle impact (intensity scales with speed)
- Collision snap prevents ball tunneling and sticky paddle
- Ball radius included in collision detection
- Held-key keyboard controls (smooth movement, not mushy)
- Mouse/touch pointer tracking for paddle control
- Synthesized square wave audio blips on hits
- Audio node cleanup via onended disconnect
- Score display, first to 7 wins
- Delta-time capped game loop
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Ball tunneling/sticky paddle: narrow collision window missed fast balls — snap ball to paddle edge on hit
- Keyboard controls mushy: used targetY offset per keydown — switched to held-key tracking with continuous movement

## How to Run

Open `index.html`. Click START. Move mouse/finger or use arrow keys/WASD to control left paddle. First to 7 points wins.

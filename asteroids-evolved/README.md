# Asteroids Evolved

Classic Asteroids but destroying rocks spawns AI drones. Green allies orbit you and auto-fire. Red enemies hunt you. The battlefield becomes a chaotic ecosystem. Single HTML file, zero dependencies.

## Features

- Classic thrust/rotate/shoot physics with screen wrapping
- Procedurally generated rock shapes (random vertex offsets)
- Asteroids split into smaller pieces, then spawn AI drones
- Green allies: orbit player, auto-target nearest enemy/asteroid, fire green bullets
- Red enemies: seek player with steering behavior, fire red bullets
- Drone separation forces prevent clumping
- Screen shake proportional to asteroid size
- Particle explosions on all deaths
- Invincibility blink on spawn
- Thrust flame animation
- Wave system with escalating asteroid count
- Start screen with color legend
- Score, wave, ally/enemy count HUD

## How to Run

Open `index.html` in a browser. Press Enter to start. Arrow keys to move, Space to shoot.

## What You'd Change

- Object pooling for bullets/particles (eliminate GC)
- Power-ups from special asteroids
- Boss asteroids at wave milestones
- Mobile touch controls

# Tower Siege

Tower defense game. Place towers along a winding path, enemies march through in waves, defend your base. 3 tower types, wave economy, splash damage.

## Features

### Gameplay
- Fixed winding path that enemies follow (44-segment route)
- 3 tower types: Arrow (fast/cheap), Cannon (slow/powerful), Splash (area damage)
- Place towers by clicking empty non-path cells
- Towers auto-target nearest enemy in range
- Bump-to-attack: enemies that reach the end cost lives
- Wave system: click "Next Wave" to start, waves scale in HP and count
- Gold economy: earn from kills + wave completion bonus, spend on towers

### Combat System
- Projectiles fired toward enemies with dt-based movement (frame-rate independent)
- Splash towers damage all enemies within blast radius
- Towers skip dead enemies (no wasted shots)
- HP bars on enemies
- Death particles on kill

### Balance
- Arrow: 25g, range 3, fast fire, 1 damage
- Cannon: 50g, range 2.5, slow fire, 4 damage
- Splash: 75g, range 2, AoE, 2 damage per target
- Enemies: HP 3+wave*2, speed increases with waves
- Wave bonus: 10+wave*5 gold on clear

### Architecture
- Canvas-rendered grid with path visualization
- Delta-time physics (projectiles, enemies, spawns all dt-based)
- Path-following via linear interpolation between waypoints
- Shop UI with cost gating (disabled when insufficient gold)
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Projectiles were frame-rate dependent (vx/vy and life not multiplied by dt) — fixed to dt-based
- Towers targeted dead enemies (hp<=0 not checked) — added hp check in targeting loop
- Zero-distance targeting caused NaN projectile velocity — clamped distance to Math.max(0.001, d)

## How to Run

Open `index.html`. Select a tower type from the shop. Click the grid to place towers (not on the path). Click "Next Wave" to start enemies. Earn gold from kills, buy more towers. Survive as long as you can.

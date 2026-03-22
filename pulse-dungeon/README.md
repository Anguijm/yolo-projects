# Pulse Dungeon

A roguelike that sounds as good as it plays. Every step makes music, every fight is percussion, and low health compresses the audio into claustrophobic tension. Single HTML file, zero dependencies.

## Features

- Procedurally generated dungeons (BSP room carving + corridor connection)
- Turn-based bump combat (move into enemies to attack)
- 3 enemy types: Slime, Bat, Orc (scaling with floor depth)
- Movement triggers pentatonic notes mapped to grid position
- Combat triggers synthesized percussion (kick on kill, noise burst on hit)
- Descending stairs plays ascending arpeggio
- Gold pickup plays bright triangle chime
- Death plays descending sawtooth dirge
- DynamicsCompressor reacts to health (low HP = aggressive compression = tense audio)
- Permadeath with game over stats
- Gold and stairs placement, HP recovery on floor descent
- Enemy AI chases player within 8-tile range
- Enemy overlap prevention on spawn
- Multiple game-over timeout prevention
- HUD: HP bar, floor, kills, gold
- Arrow keys + WASD movement
- Start screen with clickable button

## Bugs Fixed by Gemini Code Audit

- Double attack: enemy counter-attacked immediately AND in moveEnemies() (removed instant counter)
- Enemy stacking: enemies could spawn on same tile (added overlap check)
- Multiple game over: dying to 3 enemies queued 3 showGameOver() calls (added gameActive guard)

## How to Run

Open `index.html` in a browser. Click "ENTER THE DUNGEON" or press Enter.

## What You'd Change

- Visibility/fog of war (only show tiles near player)
- Items and potions
- Boss enemies every 5 floors
- localStorage high score persistence

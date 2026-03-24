# Dungeon Descent

ASCII roguelike dungeon crawler. Procedurally generated rooms, turn-based combat, fog of war, enemy AI, health potions, and infinite descent. Every run is different.

## Features

### Dungeon Generation
- Random room placement with overlap rejection
- L-shaped corridors connecting room centers
- Stairs down to next floor (deeper = harder)

### Gameplay
- Turn-based: game only advances when you act
- Bump-to-attack combat (walk into enemies to fight)
- 3 enemy types: Rat (weak), Goblin (medium), Ogre (strong)
- Enemies scale with floor depth (more HP and ATK)
- Health potions auto-consumed on walk-over
- Wait action (period key or center touch button)
- R to restart after death

### Field of View
- Raycasting FOV with configurable radius
- Visible tiles shown in full color
- Explored but out-of-sight tiles shown dimmed
- Unexplored tiles completely hidden
- Enemies only act when visible to player

### Rendering
- Canvas-rendered ASCII characters (monospace)
- Camera centered on player with scroll
- Neon color coding: @ cyan player, green goblins, orange ogres, red potions, blue stairs
- HUD: HP (color-coded), ATK, floor, kills
- Scrolling message log with color-coded events

### Controls
- Arrow keys / WASD for movement
- Period (.) to wait a turn
- R to restart after death
- Touch D-pad for mobile

### Architecture
- Procedural dungeon every floor
- Simple chase AI (move toward player when visible)
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Use arrow keys or WASD to explore the dungeon. Walk into enemies to attack. Find the blue `>` stairs to descend deeper. Collect red `+` potions to heal. Survive as long as you can.

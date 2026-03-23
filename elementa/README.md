# Elementa

Falling sand physics sandbox with cellular automata. Paint elements and watch them interact — sand piles, water flows, fire spreads, acid corrodes, oil floats, plants grow.

## Features

- 7 interactive elements: Sand, Water, Wall, Fire, Acid, Oil, Plant (+ emergent Steam)
- Cellular automata physics with density-based displacement (sand sinks through water, oil floats)
- Emergent chemistry: fire + oil = inferno, fire + water = steam, acid corrodes everything, water grows plants
- Uint32Array pixel rendering via ImageData for 60fps performance
- Bresenham line algorithm for gap-free brush strokes
- Alternating scan direction prevents directional fluid bias
- Processed-flag bitmask prevents fire/steam teleportation
- Adjustable brush size
- Resize preserves simulation state
- OLED black, mobile-first, touch-friendly

## Bugs Fixed by Gemini Audit

- Fire/steam teleported to top of screen instantly (upward-moving cells processed multiple times per frame — fixed with bit-flag marking)
- Window resize destroyed entire simulation (now copies old grid data into new grid)
- Brush couldn't paint over existing elements (removed restriction so brush overwrites)

## How to Run

Open `index.html`. Select an element from the toolbar, paint on the canvas. Try: build a wall cup, fill with water, drop sand in, add fire and oil.

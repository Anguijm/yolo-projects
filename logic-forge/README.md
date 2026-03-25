# Logic Forge

Interactive digital logic gate simulator. Place switches, AND/OR/NOT/XOR/NAND gates, and LEDs on a canvas. Wire them together by tapping pins. Toggle switches to see signals propagate through glowing wires in real-time.

## Features

- 6 gate types: AND, OR, NOT, XOR, NAND, plus Switch (input) and LED (output)
- Tap-to-place: select component, tap canvas to position it
- Tap-to-wire: tap output pin, then tap input pin to connect
- Real-time signal propagation with convergence-based simulation
- Glowing green wires for HIGH signals, dim for LOW
- Bezier curve wires between pins
- Delete tool for removing components (auto-cleans wires)
- Anti-stacking: can't place gates on top of existing ones
- Dot grid background, dark neon aesthetic
- Mobile-first with pointer events

## How to Run

Open `index.html`. Select a component from the toolbar, tap the canvas to place it. Select Wire mode, tap an output pin (right side), then an input pin (left side) to connect. Place switches and LEDs, toggle switches to test your circuit.

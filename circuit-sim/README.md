# Circuit Simulator

Interactive logic gate circuit simulator. Single HTML file, zero dependencies.

## Features

- 6 gate types: AND, OR, NOT, XOR, NAND, NOR
- INPUT/OUTPUT nodes with click-to-toggle
- Drag-and-drop gate placement from toolbar
- Wire gates by dragging between ports (bezier curves)
- Color-coded ports: green (high), gray (low), orange (unknown)
- Automatic signal propagation
- Truth table generation
- Example circuit (half adder)
- Delete gates with Delete/Backspace key
- Keyboard shortcuts: I/O/A/R/N/X for gate types

## How to Run

Open `index.html` in a browser. Click a gate type in the toolbar, then click the canvas to place it. Drag between output and input ports to wire.

## What You'd Change

- Sequential logic (flip-flops, clocks with tick system)
- Undo/redo history
- Save/load circuits as JSON
- Custom gate creation from sub-circuits

# Graph Forge

Interactive force-directed graph visualizer. Build mind maps and network diagrams with self-organizing physics. Nodes repel, edges attract, the graph finds its own balance.

## Features

### Graph Building
- Double-click to add nodes with auto-labels
- Drag from node to node to create edges (spring connections)
- Click node to edit its label (inline input)
- Right-click node to delete (removes connected edges too)
- Colored nodes cycling through 8-color palette

### Force-Directed Physics
- Coulomb repulsion between all node pairs
- Hooke's law spring attraction on edges
- Centering gravity pulls graph toward viewport center
- Velocity friction for smooth settling
- Terminal velocity cap prevents explosion
- Random jitter for overlapping nodes (prevents zero-force deadlock)
- Dragged nodes are pinned (graph reacts organically around them)

### Controls
- Repulsion strength slider (500-5000)
- Spring constant slider (0.005-0.1)
- Friction slider (0.8-0.99)
- Link length slider (60-250)
- Sample Graph button (8-node demo with cross-links)
- Clear button
- Node/edge count display

### Persistence
- Auto-saves to localStorage on every change
- Restores full graph on reload

### Architecture
- Canvas-rendered with neon glow on nodes
- Edge preview line while drawing connections
- Zero external dependencies, single-file HTML
- Glassmorphism auto-hiding panel
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Overlapping nodes had zero repulsion force (dx=dy=0 → force=0) — added random jitter
- No terminal velocity — high repulsion exploded nodes off-screen — capped at 15 px/frame

## How to Run

Open `index.html`. Double-click to add nodes. Drag between nodes to connect them. Click a node to rename it. Right-click to delete. Adjust physics with the sliders. Your graph auto-saves.

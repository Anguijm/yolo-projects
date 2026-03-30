# dep-graph

Browser-based dependency graph visualizer. Paste a package.json (npm), requirements.txt (Python), or Cargo.toml (Rust) and it renders an interactive force-directed graph.

## Features

- Auto-detects npm / pip / cargo format
- Force-directed layout with interactive drag
- Zoom and pan (mouse wheel, pinch-to-zoom on touch)
- Color-coded nodes: root (cyan), deps (green), dev deps (amber), peer/optional (blue)
- Click any node to see version, type, connection count, registry
- Presets: React App, Express API, Python ML, Python Web, Rust Web, Rust CLI
- Zero dependencies — single HTML file

## Usage

1. Open `index.html` in a browser
2. Paste a manifest file into the text area, or click a preset
3. Click **Parse** to render the graph
4. Drag nodes to rearrange; pan canvas by dragging empty space
5. Scroll/pinch to zoom; click a node for details

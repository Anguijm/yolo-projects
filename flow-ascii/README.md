# flow-ascii

Zero-dependency browser-based flowchart/diagram renderer. Type a simple text syntax, get an auto-laid-out SVG diagram. Feeder project for [Markdown Deck](../markdown-deck/).

## Usage

Open `index.html` in any modern browser. No server required.

## Syntax

```
[Node Name]                      — define a standalone node
[A] --> [B]                      — directed edge from A to B
[A] --label--> [B]               — edge with a label
[A] --> [B] --> [C]              — chain (3 or more nodes on one line)
// comment                       — ignored
```

Nodes are auto-registered from any `[...]` token. You don't need to declare them separately.

## Example

```
[Input] --> [Validate]
[Validate] --valid--> [Transform]
[Validate] --invalid--> [Error Handler]
[Transform] --> [Save]
[Error Handler] --> [Input]
[Save] --> [Done]
```

## Features

- Live render as you type
- Auto-layout: TB (top-to-bottom) or LR (left-to-right)
- Fit to view / center buttons, keyboard shortcuts (F, C)
- Pan (drag) and zoom (scroll / pinch)
- SVG export
- 5 built-in presets

## Extractable API

The `FlowASCII` module is a self-contained IIFE with a pure function API:

```js
const { nodes, edges, errors } = FlowASCII.parse(source)
const positions = FlowASCII.layout(nodes, edges, 'TB') // or 'LR'
FlowASCII.render(svgGroupElement, positions, edges)
const bounds = FlowASCII.getBounds(positions)
```

`render()` injects its own `<defs>` (arrowhead marker) into the target `<g>`, so it has no external SVG dependencies.

## Layout Algorithm

Uses Bellman-Ford longest-path layering — handles DAGs, cycles, and disconnected graphs correctly. Each layer is centered relative to the widest layer.

## Design

Follows the YOLO design system: `#0a0a0a` dark page, neon cyan accent (`#0ff`), monospace font stack, zero external dependencies.

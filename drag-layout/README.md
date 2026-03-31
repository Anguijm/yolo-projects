# drag-layout

**FEEDER** — Visual drag-and-drop positioning GUI for [Markdown Deck](../markdown-deck/) `[@ x:... y:... w:...]` directives.

## What it does

Shows a 16:9 slide canvas. Add text blocks, drag them around, resize them with corner/edge handles. The output panel shows ready-to-paste Markdown Deck directive syntax in real time.

## Output format

Each positioned block generates:

```
[@ x:10% y:30% w:80% h:20%]
# Slide Title
```

Paste directly into a Markdown Deck slide to position content at exact percentages.

## Controls

| Action | How |
|--------|-----|
| Add block | `+ Add Block` button or `A` key |
| Move block | Drag the block body |
| Resize block | Drag corner/edge handles |
| Edit content | Double-click block or `Enter` key |
| Delete block | Click `×` handle or `Delete` key |
| Nudge (1 step) | Arrow keys when block selected |
| Nudge (fine) | Shift + Arrow keys |
| Copy output | `Copy` button or `C` key |
| Toggle grid | `Grid` button or `G` key |
| Toggle snap | `Snap` button or `S` key |
| Deselect | `Escape` |
| Confirm dialog | `Ctrl+Enter` |

## Presets

Click `Presets` to load a layout template:
- **Title Slide** — headline + subtitle
- **Two Column** — side-by-side panels
- **Hero + Caption** — big statement + detail
- **Code Slide** — heading + code block
- **Three Points** — three-column grid

## Notes

- Snap grid: 32×18 (matches 16:9 aspect ratio in grid units)
- All positions output as percentages — device-independent
- The `h:` directive is always included for precise vertical sizing
- FEEDER: intended for integration into Markdown Deck as an optional GUI mode

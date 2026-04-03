# yaml-fmt

A zero-dependency YAML formatter and converter that runs entirely in the browser. Single HTML file, no build tools, no tracking, works offline.

## Features

- **YAML/JSON conversion** -- paste YAML or JSON, get formatted output in either format
- **Auto-detection** -- automatically identifies whether input is YAML or JSON
- **Indent control** -- toggle between 2-space and 4-space indentation
- **Sort keys** -- alphabetically sort all keys recursively
- **Clipboard integration** -- copy output / paste input with one click
- **Sample data** -- loads a realistic YAML config on startup so the tool is immediately explorable
- **Error reporting** -- parse errors shown with line numbers and cursor positioning
- **Live stats** -- line count, key count, nesting depth, byte size updated in real time
- **Mobile responsive** -- panels stack vertically on small screens, 44px touch targets

## YAML Support

The built-in parser handles:

- Mappings and sequences (block and flow style)
- Block scalars (`|`, `>`, `|-`, `>-`, `|+`, `>+`) with inline comments
- Quoted strings (single and double)
- YAML boolean variants (`true`/`yes`/`on`, `false`/`no`/`off`)
- Null values (`null`, `~`, empty)
- Integers, floats, `.inf`, `.nan`
- Comments (with quote-awareness and escape handling)
- Document markers (`---`, `...`)

**Not supported:** anchors/aliases (`&`/`*`), tags (`!!`), complex mapping keys (`?`), merge keys (`<<`).

## Usage

Open `index.html` in any modern browser. No server required.

1. Paste or type YAML/JSON in the left panel
2. Formatted output appears in the right panel
3. Use the toolbar to switch output format, adjust indentation, or sort keys
4. Click **Copy** to copy the result to your clipboard

## Security

- All processing happens client-side; data never leaves the browser
- Parsed objects use `Object.create(null)` to prevent prototype pollution
- Input size is capped at 2 MB
- No `eval`, no `innerHTML`, no external requests

## License

MIT

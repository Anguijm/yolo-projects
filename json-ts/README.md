# json-ts — JSON → TypeScript Interface Generator

Paste any JSON and get typed TypeScript interfaces instantly. Zero dependencies, works offline, single HTML file.

## How to run

Open `index.html` in a browser. No server needed.

## What it does

- Paste JSON in the left pane → TypeScript appears in the right pane (live, 180ms debounce)
- Handles: nested objects (generates referenced child interfaces), arrays of objects (merged schema from first 5 items), null fields, mixed-type arrays (union types), numeric/special-char keys (auto-quoted)
- **SAMPLE** — loads a representative user+address+posts example
- **FORMAT** — pretty-prints the JSON input (also Ctrl+Shift+F)
- **COPY** — copies generated TypeScript to clipboard (also Ctrl+Shift+C)
- **CLEAR** — clears the input

## Options

| Option | Default | Effect |
|---|---|---|
| Root | Root | Name of the root interface |
| INTERFACE / TYPE | INTERFACE | `interface Foo` vs `type Foo =` |
| EXPORT | on | Adds `export` keyword |
| READONLY | off | Adds `readonly` to all fields |
| OPT NULLS | on | `null` fields become optional (`field?: unknown`) |
| CAMELCASE | off | Converts `snake_case` keys to `camelCase` |
| SEMIS | on | Adds semicolons to field definitions |

## What to change

- **More array items sampled**: change `objItems.slice(0, 5)` in `inferArrayType` to a higher number
- **Date detection**: check `typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v)` and return `'Date'` instead of `'string'`
- **Enum detection**: if all string values in an array are the same few strings, generate a union literal type

# yaml-fmt — Architecture Plan

Single-file browser tool. YAML formatter, validator, and JSON converter.
Monospace font stack. Accent: `--accent-cyan: #0ff`. Scrollable layout (`overflow-y: auto`).

---

## 1. DATA TYPES

```
AppState {
  inputText:    string          // raw user input (YAML or JSON)
  outputText:   string          // formatted result
  mode:         "yaml" | "json" // current output format
  parseError:   ParseError | null
  inputFormat:  "yaml" | "json" | "unknown"  // auto-detected from input
  stats:        DocStats
}

ParseError {
  message:  string       // human-readable error description
  line:     number | null  // 1-based line number, null if unknown
  column:   number | null  // 1-based column, null if unknown
}

DocStats {
  lines:      number   // line count of input
  keys:       number   // total key count (recursive)
  depth:      number   // max nesting depth
  bytes:      number   // byte size of input
}

FormatOptions {
  indent:     number   // 2 or 4 spaces (default 2)
  sortKeys:   boolean  // alphabetical key sort (default false)
}
```

---

## 2. FUNCTION SIGNATURES

### Core

```
parseInput(raw: string): { data: any, format: "yaml"|"json" } | { error: ParseError }
```
Tries YAML parse first, falls back to JSON parse. Returns parsed data + detected format, or a ParseError.

```
formatYaml(data: any, opts: FormatOptions): string
```
Serializes parsed data back to YAML string with given indent/sort options.

```
formatJson(data: any, opts: FormatOptions): string
```
Serializes parsed data to JSON string with given indent/sort options.

```
computeStats(raw: string, data: any): DocStats
```
Counts lines, recursive keys, max depth, byte size.

```
countKeys(obj: any): number
```
Recursively counts all object keys (skips array indices).

```
maxDepth(obj: any): number
```
Recursively measures deepest nesting level.

### UI Handlers

```
handleInput(): void
```
Reads `#input` value. Calls `parseInput`. On success: calls format function matching current `mode`, writes to `#output`, updates stats bar, clears error. On failure: shows error in `#error-bar`, highlights error line, clears output.

```
handleModeToggle(newMode: "yaml" | "json"): void
```
Sets `mode`. Re-runs formatting on last successful parse. Updates button active states.

```
handleCopy(): void
```
Copies `#output` text to clipboard. Shows brief "copied" flash on `#copy-btn`.

```
handleClear(): void
```
Clears `#input`, `#output`, error bar, stats bar.

```
handleIndentChange(n: number): void
```
Updates `FormatOptions.indent`. Re-runs formatting.

```
handleSortToggle(): void
```
Toggles `FormatOptions.sortKeys`. Re-runs formatting.

```
handlePaste(): void
```
Reads clipboard into `#input`, triggers `handleInput`.

```
handleSample(): void
```
Loads a hardcoded sample YAML string into `#input`, triggers `handleInput`.

```
highlightErrorLine(line: number): void
```
Visually marks the error line in the input textarea (via an overlay or line-number gutter highlight).

```
clearErrorHighlight(): void
```
Removes any error line highlight.

```
debounce(fn: Function, ms: number): Function
```
Standard debounce wrapper. Used on input handler (250ms).

### Init

```
init(): void
```
Attaches all event listeners. Sets default state. Loads sample if input is empty.

---

## 3. DOM ELEMENT IDS

### Layout

| ID | Element | Purpose |
|----|---------|---------|
| `#app` | div | Root container, max-width 960px centered |
| `#header` | div | Title + subtitle row |
| `#toolbar` | div | Control buttons row |
| `#editor-area` | div | Flex row: input panel + output panel |
| `#input-panel` | div | Left panel container |
| `#output-panel` | div | Right panel container |
| `#stats-bar` | div | Bottom stats strip |
| `#error-bar` | div | Error message bar (hidden when no error) |

### Controls (in `#toolbar`)

| ID | Element | Purpose |
|----|---------|---------|
| `#btn-yaml` | button | Output as YAML (toggle, default active) |
| `#btn-json` | button | Output as JSON (toggle) |
| `#btn-indent-2` | button | 2-space indent (toggle, default active) |
| `#btn-indent-4` | button | 4-space indent (toggle) |
| `#btn-sort` | button | Sort keys toggle |
| `#btn-copy` | button | Copy output to clipboard |
| `#btn-paste` | button | Paste from clipboard into input |
| `#btn-clear` | button | Clear all |
| `#btn-sample` | button | Load sample YAML |

### Editor

| ID | Element | Purpose |
|----|---------|---------|
| `#input` | textarea | User pastes/types YAML or JSON here |
| `#input-label` | span | Label above input ("INPUT — YAML detected") |
| `#output` | textarea (readonly) | Formatted output displayed here |
| `#output-label` | span | Label above output ("OUTPUT — YAML") |
| `#line-count` | span | Inside stats bar — line count |
| `#key-count` | span | Inside stats bar — key count |
| `#depth-count` | span | Inside stats bar — nesting depth |
| `#byte-count` | span | Inside stats bar — byte size |
| `#error-msg` | span | Error text inside error bar |
| `#error-line` | span | Error line number inside error bar |

---

## 4. UI FLOW

### On Load

1. Page renders: dark background, two equal-width textarea panels side by side (stacked on mobile < 640px).
2. Toolbar row above editors: mode toggles (YAML active), indent toggles (2 active), sort off, copy/paste/clear/sample buttons.
3. Input textarea shows placeholder: "Paste YAML or JSON here..."
4. Output textarea is empty, readonly.
5. Stats bar at bottom shows "0 lines / 0 keys / depth 0 / 0 B".
6. Error bar is hidden.
7. `init()` runs, attaches listeners.

### Core Interaction: Typing/Pasting

1. User types or pastes into `#input`.
2. Debounced `handleInput` fires after 250ms idle.
3. `parseInput` auto-detects format. `#input-label` updates to show detected format.
4. On success:
   - Output formatted per current mode + options into `#output`.
   - `#output-label` shows output format.
   - Stats bar updates.
   - Error bar hides. Error highlight clears.
5. On failure:
   - `#error-bar` appears with red border-left accent.
   - `#error-msg` shows error description.
   - `#error-line` shows line:col if available.
   - Error line highlighted in input (red left-border overlay or background tint).
   - Output clears or retains last valid output (retain last valid).

### Mode Toggle (YAML / JSON)

1. User clicks `#btn-json`.
2. `#btn-json` gets `.active` class, `#btn-yaml` loses it.
3. Output re-renders as JSON from last successful parse.
4. `#output-label` updates.
5. If no valid parse exists, no change.

### Indent / Sort

1. Clicking indent button updates option, re-renders output.
2. Clicking sort toggles the flag, re-renders output with sorted/unsorted keys.

### Copy

1. User clicks `#btn-copy`.
2. Output text copied to clipboard.
3. Button text briefly flashes "COPIED" (1s), reverts to "COPY".

### Paste

1. User clicks `#btn-paste`.
2. Clipboard contents written into `#input`.
3. `handleInput` triggered.

### Clear

1. Both textareas emptied.
2. Error bar hidden. Stats reset.

### Sample

1. Hardcoded multi-level YAML loaded into `#input`.
2. `handleInput` triggered. User sees formatted output immediately.

---

## 5. EDGE CASES

### Malformed YAML

- Tabs mixed with spaces: parse error caught, line reported.
- Unclosed quotes: parse error with line number.
- Duplicate keys: last-value-wins (standard YAML behavior), no error.
- YAML with document markers (`---`, `...`): handled normally.
- Multi-document YAML (`---` separator): parse first document only, show info note in stats bar.

### Empty Input

- Empty string or whitespace-only: output clears, stats show "0 lines / 0 keys / depth 0 / 0 B", no error.

### Huge Files

- Input > 500KB: show warning in error bar "Large input — formatting may be slow", proceed anyway.
- Input > 2MB: refuse to parse, show error "Input exceeds 2MB limit".
- Debounce prevents re-parse on every keystroke.

### Special Characters

- Unicode (emoji, CJK, RTL): pass through unchanged; byte count uses `new Blob([text]).size`.
- YAML special strings (`yes`, `no`, `true`, `null`, `1.0`): quoted in YAML output to preserve type fidelity.
- Multiline strings (literal `|` and folded `>`): preserved in YAML output.
- Anchors and aliases (`&`, `*`): resolved on parse, expanded in output (no alias preservation).

### JSON Input

- Valid JSON auto-detected and parsed.
- JSON with trailing commas: parse error (strict JSON).
- JSON with comments: parse error (strict JSON).
- Converting JSON to YAML: works via the normal pipeline (parse JSON, serialize YAML).

### Clipboard

- Clipboard API unavailable (HTTP, older browser): paste/copy buttons hidden, fallback to manual Ctrl+V / Ctrl+C.
- Empty clipboard on paste: no-op.

### Responsive

- Below 640px: panels stack vertically (input on top, output below).
- Textareas get `min-height: 200px` on mobile.
- Toolbar wraps to two rows if needed.

---

## 6. YAML LIBRARY

Embed a minimal YAML parser/serializer inline (no CDN). Use the public-domain `js-yaml` library source (~30KB minified) vendored directly into the HTML file's `<script>` block. This is the only viable approach for single-file YAML parsing without writing a parser from scratch.

Alternatively: write a subset parser handling the most common YAML features (mappings, sequences, scalars, multiline strings, comments). This limits compatibility but keeps the file smaller. Recommended approach: vendor js-yaml.

---

## 7. FILE STRUCTURE

```
yaml-fmt/
  PLAN.md        # this file
  index.html     # single-file tool (HTML + CSS + JS, all inline)
```

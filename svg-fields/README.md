# svg-fields

Parse any existing SVG, edit every text element through a left-column form, export the result. No template markers required.

## Run

```
open svg-fields/index.html
```

Single-file HTML, no build step. Works offline.

## How it works

1. Drop, paste, or open any SVG file.
2. The tool walks the SVG DOM and finds every text-bearing element:
   - SVG native: `<text>`, `<tspan>`, `<title>`, `<desc>`, `<textPath>`
   - Inside `<foreignObject>`: any HTML element with direct text content (`<div>`, `<span>`, `<p>`, `<h1>`–`<h6>`, `<li>`, `<td>`, `<th>`, `<label>`, etc.)
   - This means **Mermaid-generated SVGs work** — Mermaid embeds labels in `<foreignObject>` + HTML `<span>`, not SVG `<text>`.
3. Each text node becomes a form field in the left column, **in document order**, pre-filled with the current value.
4. As you type, the right-pane preview re-renders with your changes live.
5. Click **download** (or Ctrl+S) to save the edited SVG. Layout, styles, filters, gradients, and other attributes are preserved untouched — only text changes.

## Hover to find

Hovering a field input highlights the matching text in the preview (bold accent color + glow). Useful when the SVG has many similar-looking labels and you want to know which one you're editing.

## Label precedence

Each field gets a label derived from (highest first):

1. `data-field="name"` attribute on the element
2. `id` attribute on the element
3. If the text is exactly `{{name}}`, uses `name` (template-friendly)
4. Otherwise the current text content, truncated to 40 chars

So arbitrary diagrams "just work" — the current text acts as the label. Templates with explicit markers get nicer labels automatically.

## Shortcuts

- `Ctrl+O` — open file
- `Ctrl+S` — download edited SVG
- Drag and drop an SVG onto the preview
- **paste** button for clipboard SVG

## Example

Click **sample** to load a Release Pipeline diagram with 16 editable text elements. Rename "Build" → "Compile", change the owner line, update the date. Download to see the modified SVG.

## Mermaid output works

Render any Mermaid diagram to SVG (e.g., via `mermaid-cli` or a Mermaid live editor), drop the output into svg-fields, and every node/edge label appears as an editable field. Duplicate labels (e.g., multiple `Yes`/`No` edge labels) are auto-disambiguated with a `(2)` suffix so each input targets a specific element.

## What gets preserved

- All non-text attributes (styles, classes, transforms, filters, gradients)
- All non-text elements (rects, paths, circles, groups, defs, clipPaths)
- All comments, namespaces, and processing instructions
- Document order of every element

## What changes

- Only the `.textContent` of text node children of editable elements.
- A temporary `data-svgfields-id` attribute is added during editing for hover-highlight tracking. It's stripped from the downloaded SVG so the export stays clean.

## Why

Any SVG that has more than three labels is a candidate for this tool. Common cases: flow diagrams, org charts, architecture diagrams, badge mockups, exam answer keys, labeled screenshots, calendar templates. Anywhere you'd otherwise hand-edit XML.

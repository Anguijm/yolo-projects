# schema-viz

Browser-based JSON Schema / OpenAPI spec visualizer. Paste a schema, get an interactive collapsible tree.

## Features

- **Auto-detects** JSON Schema (draft-07) vs OpenAPI 3.x spec
- **Collapsible tree** — click any node to expand/collapse
- **Type badges** — color-coded: string, number, boolean, array, object, enum, $ref, allOf/oneOf/anyOf
- **Required fields** highlighted; optional fields dimmed
- **Field metadata** — format, description, enum values, default, min/max, minLength/maxLength, pattern
- **OpenAPI mode** — renders paths, HTTP methods (GET/POST/PUT/PATCH/DELETE), parameters, request bodies, responses
- **Path-level parameters** merged into operations automatically
- **Search** — live field search with ancestor expansion
- **Collapse all** — one-click to fold entire tree
- **Presets** — four built-in examples: User schema, Product schema, PetStore API, Auth API

## Usage

1. Paste a JSON Schema or OpenAPI 3.x YAML (JSON format) into the left panel
2. Click **Parse** or use the keyboard shortcut
3. Explore the rendered tree — click rows to expand/collapse
4. Use the search box to find fields by name or type
5. Load a preset via the dropdown to see example schemas

## Supported Schema Features

- `type`, `format`, `description`, `default`, `enum`
- `properties`, `required`, `additionalProperties`
- `items` (single schema or tuple)
- `allOf`, `oneOf`, `anyOf`
- `$defs`, `definitions`
- `$ref` (display only, no resolution)
- `minimum`, `maximum`, `minLength`, `maxLength`, `minItems`, `maxItems`, `pattern`

## Tech

Single HTML file, zero dependencies.

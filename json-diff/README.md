# JSON Diff

Structural JSON comparison tool. Paste two JSON objects and instantly see what changed — added keys, removed keys, and changed values — with color-coded output and nested object support.

## What it does

- **Recursive diff**: compares nested objects and arrays at every level
- **Color-coded output**: green = added, red = removed, amber = changed
- **Stats bar**: counts of added/removed/changed fields at a glance
- **Show/Hide Unchanged**: toggle to focus on changes only or see full structure
- **Swap**: instantly flip left ↔ right to reverse the diff
- **Sample**: loads example API response data to explore the tool
- **Auto-diff**: debounced live diff as you type (also Ctrl+Enter)
- **Copy values**: hover any value to reveal a COPY button

## How to run

Open `index.html` in a browser. No server needed, no dependencies.

## What to change

- To add support for "set-based" array diffing (order-independent): replace `diffArrays` with an LCS or Myers diff implementation
- To add JSON path display (e.g. `address.city`): thread the path string through recursive calls and display it alongside each key
- To add text export: collect all changed nodes into a plain-text report on demand

# Prompt S: the look (the demo's style on any of the built pages, light and dark, color squares, summary cards)

Version 0.3, 2026-10-23 (v0.1 and v0.2 kept in the private source). v0.3: item 4 wires the map table's hover listeners once per
table (a mark in dataset) instead of on every draw (optional point in the review of PR 60); MODULE S regenerated from
the v0.3 text and retested. v0.2: item 3 of the Resource Map's MODULE S calls styleBar() from the
renderMap hook; v0.1 defined styleBar and never called it (review of PR 60), so a model that followed the text to the
letter would never create the stats cards or the tip line. The tested answer had called it there on its own, so the
text now says what the tested code does. One prompt, run LAST in a series: after B2-4 (and X2, if used) for the Resource Map, after
Prompts D (and X2) for the estimator. It answers hole 10 of the process flow page: the pages built by the series are
plain because no prompt ever asked for a look. The owner's demo leveler (the demo page) has the look he wants; its
stylesheet is about sixty lines, plus a different map cell (a color square, the number on hover). Both are written
into this prompt, so the model inside the enclave pastes a look rather than inventing one. Fonts are the system
stack only: no web fonts can load at IL5, and the demo rendered with the network blocked still looks right.

Tested here on the leveler build and on the estimator build (the private test record): no console errors,
the map cells become 14 by 22 px squares, the band colors come from the tokens, dark mode follows the system and
the toggle, and the whole leveler test still passes on the styled page (the look changes nothing underneath).

## What it does

1. Replaces the page's stylesheet with the demo's: tokens for every color (light values on :root, dark values under
   prefers-color-scheme and under a data-theme attribute so a toggle wins both ways), the type scale, cards,
   tables, buttons, pills, a legend. The earlier modules keep working because their variable names are mapped to
   the new tokens at the end of the stylesheet.
2. A hook on renderMap: the map table gets the class heat; its cells become color squares (the number stays in the
   title and in a tip line under the map, and a "Numbers" button brings the text back); a strip above the map
   carries the legend and five summary cards (shops, weeks, shop-weeks over the band, under it, unplaced hours).
3. A theme toggle (Auto, Light, Dark) remembered in the browser.

## Prompt S

```
Continue the same file. Two changes, which I will paste myself:

(1) The whole <style> element in the head is replaced by the stylesheet below. Keep it unchanged, and APPEND one
block that maps every CSS variable name the page's own scripts and styles already use (the ones the earlier
modules declared, such as --bg, --text, --border, --accent, and whatever the map module named its band colors,
for example --c-under, --c-band, --c-over, --c-red, --c-darkred, --c-na, or --band-under and so on; find the
actual names in the file) onto the new tokens, like `:root { --bg: var(--s-bg); --text: var(--s-fg); --border:
var(--s-line); --accent: var(--s-accent); --c-under: var(--s-under); --c-band: var(--s-band); --c-over:
var(--s-over1); --c-red: var(--s-over2); --c-darkred: var(--s-over3); --c-na: var(--s-line); }`, so that nothing
else in the file has to change. Any <style> element an earlier module appends from JavaScript stays as it is.

(2) MODULE S, two <script> blocks to paste as the LAST scripts in the file: a one-line block `var renderMapS =
renderMap;` and then a block of plain global function declarations (no IIFE, no class, no window assignment, no
typeof guards, no libraries, no em dashes; events through arrow functions; the capture and the new declaration
never share a block).

The stylesheet:

<style>
/* Look: the owner's shop-load demo. Tokens first, light on :root, dark twice (system and toggle). System fonts only. */
:root {
  --s-bg: #f3f5f4; --s-surface: #ffffff; --s-fg: #17201d; --s-muted: #5b6763; --s-line: #d5dcd9;
  --s-accent: #1f5f8b;
  --s-under: #c9d6e3; --s-band: #6f9f7f; --s-over1: #e3a85a; --s-over2: #c9562f; --s-over3: #8e2417;
  --s-display: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
  --s-body: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
  --s-mono: ui-monospace, "Cascadia Mono", Consolas, "SFMono-Regular", Menlo, monospace;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --s-bg: #121816; --s-surface: #1a2220; --s-fg: #e4ebe8; --s-muted: #9aa8a3; --s-line: #2c3834;
  --s-accent: #7db4dc; --s-under: #2b3c4d; --s-band: #4f8a64; --s-over1: #c98f3f; --s-over2: #d0603a; --s-over3: #f08a6c;
  color-scheme: dark; } }
:root[data-theme="dark"] {
  --s-bg: #121816; --s-surface: #1a2220; --s-fg: #e4ebe8; --s-muted: #9aa8a3; --s-line: #2c3834;
  --s-accent: #7db4dc; --s-under: #2b3c4d; --s-band: #4f8a64; --s-over1: #c98f3f; --s-over2: #d0603a; --s-over3: #f08a6c;
  color-scheme: dark; }
html { background: var(--s-bg); }
body { margin: 0 auto; max-width: 1180px; padding: 20px max(16px, env(safe-area-inset-right, 0px)) 48px max(16px, env(safe-area-inset-left, 0px));
  background: var(--s-bg); color: var(--s-fg); font-family: var(--s-body); font-size: 15px; line-height: 1.5; }
h1 { font-family: var(--s-display); font-weight: 800; font-size: clamp(1.5rem, 4vw, 2.1rem); margin: 0 0 6px; letter-spacing: -0.01em; }
h2 { font-family: var(--s-display); font-weight: 700; font-size: 1.1rem; margin: 26px 0 10px; }
h3, h4 { font-family: var(--s-display); font-weight: 700; font-size: 1rem; margin: 16px 0 8px; }
p { margin: 0 0 10px; max-width: 72ch; }
label { display: inline-block; margin: 2px 12px 6px 0; color: var(--s-muted); font-size: 0.9rem; }
input, select, textarea, button { font: inherit; color: var(--s-fg); background: var(--s-surface); border: 1px solid var(--s-line); border-radius: 6px; padding: 5px 8px; }
button { font-weight: 600; cursor: pointer; }
button:hover { border-color: var(--s-accent); }
button:focus-visible, a:focus-visible, td:focus-visible { outline: 2px solid var(--s-accent); outline-offset: 2px; }
a { color: var(--s-accent); }
textarea { width: 100%; min-height: 120px; font-family: var(--s-mono); font-size: 0.8rem; box-sizing: border-box; }
.scroll-container, .table-container { overflow-x: auto; background: var(--s-surface); border: 1px solid var(--s-line); border-radius: 8px; padding: 10px; margin: 8px 0; }
table { border-collapse: collapse; font-size: 0.88rem; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--s-line); vertical-align: top; }
th { font-weight: 600; color: var(--s-muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
table.heat { border-collapse: separate; border-spacing: 2px; font-family: var(--s-mono); font-size: 0.72rem; }
table.heat th { color: var(--s-muted); font-weight: 400; text-transform: none; letter-spacing: 0; border: 0; padding: 0 4px 4px; white-space: nowrap; }
table.heat th.wk { writing-mode: vertical-rl; transform: rotate(180deg); font-size: 0.65rem; line-height: 1; padding: 2px 0 0; height: 44px; vertical-align: bottom; }
table.heat td { border: 0; padding: 2px 4px; border-radius: 2px; font-variant-numeric: tabular-nums; }
table.heat td.sq { width: 14px; min-width: 14px; height: 22px; padding: 0; font-size: 0; color: transparent; }
body.present #map td.sq, body.present table.heat td.sq { width: 30px; min-width: 30px; height: 38px; padding: 0; font-size: 0; }
body.present #map th.wk, body.present table.heat th.wk { padding: 2px 0 0; font-size: 0.7rem; }
#stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin: 10px 0; }
.stat { background: var(--s-surface); border: 1px solid var(--s-line); border-radius: 8px; padding: 10px 14px; display: grid; gap: 2px; }
.stat b { font-family: var(--s-mono); font-size: 1.4rem; font-variant-numeric: tabular-nums; }
.stat span { color: var(--s-muted); font-size: 0.82rem; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; margin: 8px 0; font-size: 0.82rem; color: var(--s-muted); align-items: center; }
.legend i { display: inline-block; width: 12px; height: 12px; border-radius: 2px; vertical-align: -1px; margin-right: 5px; }
.flag { font-family: var(--s-mono); font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--s-accent); }
.pill { display: inline-block; font-size: 0.78rem; padding: 2px 8px; border-radius: 999px; border: 1px solid currentColor; white-space: nowrap; }
#tip { font-family: var(--s-mono); font-size: 0.8rem; min-height: 1.4em; margin: 6px 0; }
#drillbox, #leveler-panel, #verdicts { font-size: 0.9rem; }
.chip { border-color: var(--s-accent); color: var(--s-accent); }
.dropcell { border-color: var(--s-muted); }
@media (max-width: 600px) { body { font-size: 14px; } h2 { margin-top: 18px; } }
/* mapping block: APPEND HERE the page's own variable names onto the tokens above */
</style>

MODULE S, in the second block:
1. themeInit(): read localStorage "s-theme" inside try; when it is "light" or "dark", set that as data-theme on
   document.documentElement; otherwise remove the attribute. setTheme(mode): "auto" removes the attribute and the
   stored value, "light" or "dark" sets both; everything inside try, a failure only means the choice is not
   remembered.
2. styleBar(): inserts once (if $("stylebar") exists, return), before the container that holds the map table
   ($("map").parentNode), a div id stylebar holding: a div id stats (empty); a div class legend with five swatches
   (an <i> colored by var(--s-under), var(--s-band), var(--s-over1), var(--s-over2), var(--s-over3)) labeled
   "under", "in band", "over", "well over", "far over", then the band values read from band-lo and band-hi (for
   example "band 80 to 100%"); a button id btn-squares ("Numbers" when squares are on, "Squares" when off); a
   select id theme-mode with options auto, light, dark (label "Theme"); and a div id tip with the hint "hover or
   focus a cell for its numbers". Wire: btn-squares toggles the class "squares" on document.body, remembers it in
   localStorage "s-squares" inside try, and calls run(); theme-mode change calls setTheme(value). On first build,
   body gets the class squares unless localStorage "s-squares" is "off".
3. renderMap(): the hook. renderMapS(); then styleBar() (it inserts once, so calling it on every draw is safe, and
   the map's container exists by then); then heatify(); then renderStats().
4. heatify(): find the table: $("map") itself if it has rows, else the first <table> inside $("map"); add the class
   heat to it and clear any inline width and border-collapse the map module wrote on it (table.style.width = "auto";
   table.style.borderCollapse = ""), or the cells cannot shrink to squares. In the header row, every <th> except the first (the shop column) and the
   last (the unplaced column) gets the class wk, which draws its label vertically, so a column can be 14 px wide.
   For every <tr> of its body (and of the table, when there is no tbody): the first cell is the shop
   label and the last cell is the unplaced column, both left alone; every other <td> gets the class sq when
   document.body has the class squares (and loses it otherwise), keeps its title attribute (the map module wrote
   "shop, week, load and capacity" there) and gets data-text = its own text when sq is set (so the number is not
   lost; the class makes the text invisible). Wire the table once, through arrow functions: when table.dataset.sWired
   is not set, set it to "1" and add the listeners (mouseover and focusin on the table write the hovered or focused
   cell's title into $("tip"); mouseout clears it); a table the map module rebuilt has no such mark and is wired
   again, a table that persists is never wired twice.
5. renderStats(): reads the global GRID (keyed "shop|week", cells {assigned, proposed, capacity}), the view mode
   (the select id view-mode, whose values are the option texts "Assigned only", "Assigned + proposed", "Proposed
   only") and band-lo, band-hi; counts shops (DB.shops.length), weeks (DB.weeks.length), shop-weeks over the band
   (percent above band-hi, capacity > 0), shop-weeks under (below band-lo), and the unplaced hours (the sum of the
   global UNPLACED's values); writes five .stat cards into $("stats"): a <b> with the number and a <span> with the
   label ("shops", "weeks", "over the band", "under the band", "unplaced hours").
6. At the end of the block: themeInit(); if DB.weeks is non-empty call run() so the page redraws with the look.
7. No em dashes.

Answer with three blocks and nothing after them: first a <style> element holding only the mapping block of change
(1) (I paste it into the head right after the new stylesheet), then the one-line <script> block, then the MODULE S
<script> block.
```

## For the estimator page

The same prompt applies with one change: the estimator has no shop-by-week map, so items 3, 4 and 5 are dropped.
Replace the text from "MODULE S, in the second block" to the end with this, and ask for the mapping block and ONE
script block:

```
MODULE S, one <script> block (this page has no map, so there is no renderMap hook and no one-line capture):
1. themeInit() and setTheme(mode) exactly as above (localStorage "s-theme", data-theme on the html element).
2. styleBar(): inserts once, before the first <h2> of the page, a div id stylebar holding a select id theme-mode
   with options auto, light, dark (label "Theme"), wired through an arrow function to setTheme(value), and
   showing the stored choice.
3. At the end of the block: themeInit(); styleBar().
Answer with two blocks and nothing after them: the <style> element holding only the mapping block, then the
MODULE S <script> block.
```

The estimator built from the series here names its variables --bg-color, --text-color, --border-color, --btn-bg
and --btn-hover; the mapping block then reads `:root { --bg-color: var(--s-bg); --text-color: var(--s-fg);
--border-color: var(--s-line); --btn-bg: var(--s-surface); --btn-hover: var(--s-line); }`. The model finds the
names in the chat; this is what to expect.

## Debug

The Debug prompts of series B apply. A page that looks wrong after this prompt almost always has a variable name
missing from the mapping block: open the console, look for a color that stayed at its default, and ask the model to
add that name to the mapping block.

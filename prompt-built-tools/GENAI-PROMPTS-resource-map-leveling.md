# Prompts B2: the leveler (move work, farm out, zoom, snapshot, automatic leveling) for the Resource Map, inside GenAI.mil

Version 0.5, 2026-10-25 (v0.1 to v0.4 kept in the private source). v0.5 changes one import rule in B2-1 (item 9): the estimator's
consumption file has one line per job, phase AND shop (estimator series v0.7, from the task records of the owner's
pulls), so a re-import replaces each job's lines whole, by proposed_id, instead of by proposed_id and phase_no, which
kept one shop per phase and silently dropped the rest (found 2026-10-25 on a several-shops file: 182 lines in, 104
kept, the status line still saying 182). Consumption rows also keep the file's tasks column; the consumption_moved
export keeps its 24 columns (tasks is not exported). MODULE 5 regenerated from this text on the Resource Map v0.6
base and the whole leveler test rerun with a several-shops import check (the private test record, round 5).
v0.4 (2026-10-23) took two optional points from the review of PR 60: a
capacity file loaded twice no longer doubles the contractor line (B2-1 item 10 replaces rows by shop and week), and
a dropped job chip whose id is written in lower case still moves (B2-2 item 4 compares uppercased ids). MODULES 5 and
6 were regenerated from the v0.4 text and the whole leveler test rerun (the private test record, round 4).
v0.3 renames the lookup column to map_name (the old name carried a workplace report's name, which the public copy
must not; review of PR 60) and nothing else; the tested build was renamed the same way and retested. v0.2 (2026-10-23; v0.1 of 2026-10-22 was never
tested: it needed a schedule export with float per phase that does not exist yet) is built around what the owner asked for on 2026-10-22: click an overloaded shop-week
and see its jobs (series B already does that), drag a job week to week, drag a whole project, keep the dates of record
as the baseline so every move is a what-if on top of it, read the contractor as its own line, zoom to a time frame,
take a snapshot for the TVs, and level and farm out automatically then compare. The windows the automatic leveler
moves work inside come from the project list (project start and end), not from a schedule export: an unplanned job may
run anywhere inside its availability, in its phase order. Tested against Gemini the way the other series were (made-up
data only, headless browser, an independent computation of the same rules); the record is in
the private test record.

Series B2 adds to the Resource Map built by series B (`GENAI-PROMPTS-resource-map.md`, B1 to B4). Run order
inside GenAI.mil: after B4 and before Prompts X (the workbook hook must wrap B2's importer, so B2 comes first; if
Prompts X are already in the file, run X2 again after B2), then the style prompt (`GENAI-PROMPTS-style.md`) last.
B2-1, B2-2, B2-3, B2-4, then B2-5 (the check). The Debug prompts of series B apply unchanged. Each answer is pasted
as the LAST scripts in the file, in order.

What it does, in the owner's terms:

1. **The baseline stays.** The loaded files are the dates of record. A move never changes a stored row; it is kept in a
   moves list and applied when the map is drawn. Reset puts everything back. The moves list exports as a CSV for
   whoever keys the schedule of record, because nothing on the work computer writes back to it.
2. **Drag a job.** In the drill-down of a shop-week, every proposed job has "1 week earlier" and "1 week later"
   buttons (they work on a touch screen) and a chip that can be dragged onto a week in the drop strip above the map,
   which moves the job's first week there. All phases of the job move together.
3. **Drag a project.** A projects strip lists every project with its span; each has the same buttons, a "slip by n
   weeks" box and a draggable chip. A project move shifts the workforce map's assigned hours for that project and
   every proposed job of that project.
4. **The contractor is its own line.** Proposed work marked farm-out (by screening, by planning, by the analogs as a
   guess, or by hand here) loads the contractor's line on the map instead of the organic shop, when the box is
   ticked. The farm-out list shows what is on that line and why.
5. **Project names.** The workforce map names a project its own way; the estimator uses the project id from the JCN
   history. A lookup file (map_name, project) joins them; without it, names are used as they are.
6. **Zoom and snapshot.** A time frame (from week, to week, or a preset) cuts the map to the weeks that matter; the
   snapshot button draws the visible map as a PNG image to download or copy for the TVs; present mode hides the
   controls and enlarges the map.
7. **Level and farm out automatically.** The leveler slides every unplanned proposed job inside its project's window
   to cut peaks, then sends whole jobs to the contractor where a shop is still over the band, and shows a before,
   leveled and farmed comparison per shop. Its moves are suggestions until "Apply" writes them into the moves list,
   marked auto, where they can be discarded as a group.

All data in the tests is made up. The prompts never need a real value.

## Contract additions (repeated in every B2 prompt)

Stored with the rest of DB by the existing saveStore (DB is stored whole):

- `DB.lookup`: array of {map_name, project, hull}. lookupProject(name) returns the project of the row whose
  map_name equals name (trimmed, case-insensitive), else name unchanged.
- `DB.projects` (already in the contract): {project, hull, start, end}, start and end as Monday strings.
- `DB.settings`: {contractor_shop: "CTR", contractor_line: true, zoom_from: "", zoom_to: "", moved_by: ""}.
- `DB.moves`: array of {id (number, 1 upward), kind ("job", "project" or "performing"), key (the proposed_id, uppercased
  and trimmed, or the project name as shown on the map), weeks (whole number; 0 for performing), performing
  ("farm-out", "in-house" or ""), by, at (ISO text), auto (true or false)}.
- Consumption rows keep every column of the file: the 19 contract fields plus source, performing and
  performing_basis (blank when the file has no such column). Rows are stored under exactly these names.
- Globals declared by B2: `var MOVED = null` (the effective rows after the moves, refreshed by renderMap) and
  `var LEVELED = null` (the automatic leveler's result).

Week arithmetic: addWeeks(monday, n) returns the Monday string n weeks later (n may be negative), built with
Date.UTC and read with UTC getters; weeksBetween(a, b) returns the whole number of weeks from Monday a to Monday b
(negative when b is earlier). A consumption row's span is every Monday from week_start to week_end inclusive (one
week when week_end is blank or equal); its load_hours are spread evenly over the span, which is exactly how the map
already draws it.

Hooks: B2 never rewrites a series B function. It captures the earlier one in a one-line script block (`var
renderMapB1 = renderMap;`) and declares the name again in the NEXT block, calling the captured one for everything
that is not B2's. The capture and the redeclaration never share a block (a function declaration is hoisted to the
top of its block, so a capture in the same block would take the new one and recurse).

Element ids added by B2 (created by buildLevelerPanel(), inserted after the container of table verdicts):
leveler-panel, moved-by, zoom-from, zoom-to, zoom-preset, btn-zoom, btn-zoom-clear, contractor-shop,
contractor-line, dropstrip, projects-strip, moves, btn-reset-moves, btn-reset-auto, farmout-list, farmout-summary,
btn-snapshot, btn-copy-image, snapshot-link, snapshot-img, snapshot-status, btn-present, present-bar,
btn-present-exit, auto-panel, btn-level, btn-apply-auto, btn-discard-auto, auto-status, compare, auto-moves.
csvkind gains the options moves, consumption_moved, assigned_moved, farmout_list.

---

## Prompt B2-1: the overlay (lookup, settings, moves), the importer hook and the map hook

```
Continue the same file (the Resource Map built in steps B1 to B4). Write MODULE 5 in two parts, to paste after
MODULE 4: first a one-line <script> block containing exactly `var importFilesB1 = importFiles; var renderMapB1 =
renderMap;`, then one <script> block that declares plain global functions (no IIFE, no class, no window assignment,
no typeof guards, no declarations inside if blocks, no libraries, no network, no em dashes). The capture block and
the block that declares importFiles and renderMap again must stay separate: a function declaration is hoisted to
the top of its own block, so a capture in the same block would take the new function and recurse forever.

Existing contract: DB = {assigned (project, shop, week_start, assigned_hours, src), capacity (shop, week_start,
capacity_hours, src), projects (project, hull, start, end), consumption (the 19 contract fields), weeks, shops};
helpers $(id), esc, toDate, fmtDate, mondayOf, num, csvCell, parseCSV (returns an array of arrays); normalizeShop(s)
and normalizeProject(s) exist (MODULE 2 wrote them); importFiles(fileList) reads files and ends in rebuildIndex(),
which recomputes DB.weeks and DB.shops from the stored rows, fills filter-project and filter-shop, calls
saveStore() then run(); run() calls renderMap(), renderVerdicts() and exportCSV(); renderMap() reads DB.assigned,
DB.consumption, DB.capacity, DB.weeks, DB.shops and the controls, and fills the global GRID keyed "shop|week".
Every Date is built with Date.UTC from parsed parts and read with UTC getters only. The select id filter-project
holds the project filter ("" = all).

Contract additions (keep every name exactly):
- DB.lookup: array of {map_name, project, hull}. DB.settings: {contractor_shop: "CTR", contractor_line: true,
  zoom_from: "", zoom_to: "", moved_by: ""}. DB.moves: array of {id, kind, key, weeks, performing, by, at, auto}
  (kind "job", "project" or "performing"; key = proposed_id uppercased and trimmed, or the project name as shown on
  the map; weeks a whole number, 0 for performing; performing "farm-out", "in-house" or ""; auto true or false).
- Consumption rows keep every column of the file: the 19 fields plus source, performing, performing_basis, tasks
  (blank when the file has no such column). A job has one row per phase AND shop.
- Global `var MOVED = null;` declared at the top of the second block.

Write, in the second block:
1. ensureB2(): gives DB.lookup, DB.projects, DB.settings, DB.moves their default values when missing (a stored DB
   from before this module has none), filling missing settings keys one by one, without touching anything that
   exists. Every function in this and the later B2 modules calls ensureB2() first.
2. addWeeks(monday, n): the Monday string n weeks later, built with Date.UTC from the parts of monday and
   setUTCDate(getUTCDate() + 7 * n), returned through fmtDate; "" when monday is blank. weeksBetween(a, b): the
   whole number of weeks from Monday a to Monday b, Math.round((Date.UTC of b minus Date.UTC of a) / 604800000);
   negative when b is earlier.
3. lookupProject(name): the project of the DB.lookup row whose map_name equals name after trimming, ignoring
   case; else name unchanged (trimmed).
4. spanWeeks(row): the array of Monday strings from row.week_start to row.week_end inclusive (one week when
   week_end is blank, equal, or earlier); [] when week_start is blank.
5. applyMoves(): returns {assigned, consumption, projectShift, jobShift, performing}. First the nets: projectShift[p]
   = the sum of weeks of the project moves with key p; jobShift[id] = the sum of weeks of the job moves with key id;
   performing[id] = the performing of the LAST performing move with key id (in DB.moves order). Then copies, never
   the stored rows:
   a. For each DB.assigned row: a copy with project = lookupProject(row.project), shift = projectShift[project] or
      0, week_start = addWeeks(row.week_start, shift) when shift is not 0, moved_weeks = shift.
   b. For each DB.consumption row: a copy with id = (proposed_id or "").trim().toUpperCase(), project =
      lookupProject(row.project), shift = (projectShift[project] or 0) + (jobShift[id] or 0), week_start and
      week_end each through addWeeks by shift when non-blank and shift is not 0, moved_weeks = shift, performing =
      performing[id] when a performing move exists for id (then performing_basis = "manual"), else row.performing
      or "" with the row's own performing_basis, shop_organic =
      row.shop, shop = DB.settings.contractor_shop when DB.settings.contractor_line is true and performing is
      "farm-out", else row.shop.
6. allWeeks(moved): the sorted unique Mondays of DB.capacity week_start, moved.assigned week_start, and every week
   of spanWeeks(row) for moved.consumption rows (blanks dropped). effectiveWeeks(moved): allWeeks(moved) with weeks
   before DB.settings.zoom_from dropped when zoom_from is non-blank, and weeks after zoom_to dropped when zoom_to is
   non-blank. effectiveShops(moved): the sorted unique non-blank shops of DB.capacity, moved.assigned and
   moved.consumption.
7. renderMap(): the hook. ensureB2(); MOVED = applyMoves(); keep base = {assigned: DB.assigned, consumption:
   DB.consumption}; set DB.assigned = MOVED.assigned, DB.consumption = MOVED.consumption, DB.weeks =
   effectiveWeeks(MOVED), DB.shops = effectiveShops(MOVED); refill the select filter-project with "" (All projects)
   plus the sorted unique projects of MOVED.assigned and MOVED.consumption, keeping the selected value when it is
   still there; then call renderMapB1() inside try, and in finally put base.assigned and base.consumption back into
   DB (DB.weeks and DB.shops stay as set, so the verdicts and the export see the same weeks as the map). After that
   call afterMap(), declared here as an empty stub (`function afterMap() {}`); MODULE 6 declares it again.
8. addMove(kind, key, weeks, performing): ensureB2(); key trimmed, uppercased when kind is "job"; id = 1 + the
   largest id in DB.moves (or 1); push {id, kind, key, weeks: Math.round(num(weeks)) or 0, performing: performing or
   "", by: DB.settings.moved_by, at: new Date().toISOString(), auto: false}; a job or project move of 0 weeks is
   ignored; then saveStore() and run(). removeMove(id): drop that move; saveStore(); run(). resetMoves(which):
   "all" empties DB.moves, "auto" drops the moves with auto true, "manual" the others; saveStore(); run().
   setSetting(name, value): DB.settings[name] = value; saveStore(); run().
9. importConsumption(rows, fileName): rows is parseCSV's output; the header is the first row with at least two
   non-blank cells; match headers to these fields by squashed name (case, spaces, underscores and punctuation
   removed): proposed_id, hull, project, phase_no, phase_title, shop, est_hours_low, est_hours_high,
   charged_hours_low, charged_hours_high, load_hours, week_start, week_end, placement, summaries_used, same_class,
   top_score, analog_jcns, notes, source, performing, performing_basis, tasks. Store every row under the contract names:
   hours through num(), week_start and week_end through mondayOf(toDate()) ("" when blank), shop through
   normalizeShop, project through normalizeProject, everything else trimmed text ("" when the column is absent).
   Before appending, drop every earlier DB.consumption row whose proposed_id (trimmed, uppercased) appears in this
   file, then append all of the file's rows, so a re-import replaces each job whole; never replace by proposed_id and
   phase_no, because a phase has one row per shop and that rule keeps one shop and drops the others. Return the count.
10. importB2(kind, rows, fileName): "lookup": header with map_name (aliases mapname, resourcemapname,
    workforcename, workforcemapname) and project; rows {map_name, project, hull} replace earlier rows with the same
    map_name. "projects": header with project, start and end and NO shop and NO week_start; rows {project
    (normalizeProject), hull, start: mondayOf(toDate()), end: mondayOf(toDate())} replace earlier rows with the
    same project. "capacity": header with shop, week_start and capacity_hours; rows {shop (normalizeShop),
    week_start (mondayOf(toDate())), capacity_hours (num), src "<file>:<row>"} replace an earlier DB.capacity row with
    the same shop and week_start (so loading the same file twice does not double the line), else append. Return a
    one-line summary.
11. importFiles(fileList): the hook. ensureB2(); for each file (a for-of loop, no IIFE), read the whole text (these
    files are small), parse
    with parseCSV, find the header (the first row with at least two non-blank cells), squash its names, and decide:
    proposedid together with loadhours is a consumption file, handled here by importConsumption and NOT passed on
    (so performing survives); mapname (or an alias above) with project is "lookup"; project with start and end and
    without shop or weekstart is "projects"; shop with weekstart and capacityhours is "capacity"; anything else is
    kept, as the File, for the earlier importer. Append one line per file to the element with id datastatus (that
    exact id, no hyphen) saying what it was taken for and how many rows. When every file is looked at: if any File was kept, call importFilesB1(the array of kept
    Files) (it ends in rebuildIndex); else call rebuildIndex() yourself.
12. No DOM is built in this module beyond the status lines and the filter-project refill.

Answer with the two <script> blocks only, the one-line block first, and nothing after them.
```

## Prompt B2-2: the panel, the drill controls, drag and drop, the moves table

```
Continue the same file. Write MODULE 6 in two parts: first a one-line <script> block containing exactly `var drillB1
= drill;`, then one <script> block of plain global function declarations (no IIFE, no class, no window assignment,
no typeof guards, no declarations inside if blocks, no libraries, no em dashes). It builds the what-if panel, adds
move controls to the drill-down, and makes the chips draggable.

Contract reminder: DB.settings {contractor_shop, contractor_line, zoom_from, zoom_to, moved_by}; DB.moves rows {id,
kind, key, weeks, performing, by, at, auto}; MOVED = {assigned, consumption, projectShift, jobShift, performing}
(the effective rows: consumption rows carry id-ready proposed_id, project, shop, shop_organic, performing,
performing_basis, moved_weeks, week_start, week_end, load_hours, phase_title); helpers $(id), esc, addWeeks,
weeksBetween, spanWeeks, allWeeks, effectiveWeeks, ensureB2, addMove(kind, key, weeks, performing),
removeMove(id), resetMoves(which), setSetting(name, value), saveStore, run; GRID keyed "shop|week" with
proposedRows and assignedRows, where a proposedRows entry is either the consumption row itself or an object with
the row under .row (read it as `var r = e.row || e;`) and an assignedRows entry is the assigned row (or under .row
likewise). renderMap() ends by calling afterMap(), a stub to declare again here. drill(shop, week) is captured as
drillB1. Events are wired through arrow functions. The map table has id map; the verdicts table id verdicts.

Write:
1. buildLevelerPanel(): inserts the panel once (if $("leveler-panel") exists, return). Find table id verdicts; if
   its parent is not document.body, insert after the parent (insertAdjacentHTML "afterend"), else after the table.
   The panel, a div id leveler-panel, in this order, with these ids:
   a heading "5. What-if: move work, farm out, zoom, snapshot" and one sentence: "The loaded files are the dates of
   record. Every move here is a what-if on top of them; nothing writes back. Export the moves list for whoever keys
   the schedule."; a text input id moved-by (label "Moved by"); a zoom row: selects id zoom-from and zoom-to
   (first option "" labeled "open"), a select id zoom-preset with options all, next8, next13, next26 (labels "all
   weeks", "next 8 weeks", "next 13 weeks", "next 26 weeks"), buttons id btn-zoom "Apply zoom" and id
   btn-zoom-clear "Clear zoom"; a contractor row: text input id contractor-shop (label "contractor's line (shop
   code on the workforce map)"), checkbox id contractor-line (label "count farm-out work on the contractor's line
   instead of the shop"); a div id dropstrip with the hint "Drag a job or project chip onto a week to move its
   first week there (or use the 1-week buttons)"; a table id projects-strip; a table id moves with buttons id
   btn-reset-moves "Reset all moves" and id btn-reset-auto "Discard leveler moves"; a div id farmout-summary and a
   table id farmout-list; a snapshot row: buttons id btn-snapshot "Snapshot the map", id btn-copy-image "Copy
   image", a link id snapshot-link (download="resource-map-snapshot.png", text "Download PNG"), a span id
   snapshot-status, an img id snapshot-img (max-width 100%); a button id btn-present "Present (TV mode)"; a div id
   auto-panel (empty; MODULE 8 fills it). Also add the options moves, consumption_moved, assigned_moved and
   farmout_list to the select id csvkind if they are not there.
   Wire through arrow functions: moved-by change calls setSetting("moved_by", value); btn-zoom calls
   setSetting("zoom_from", zoom-from value) and sets zoom_to likewise (one saveStore and run: set both in
   DB.settings then saveStore() and run()); btn-zoom-clear clears both; zoom-preset change sets zoom_from to the
   first week of allWeeks(MOVED) and zoom_to to the week 7, 12 or 25 weeks later (or clears both for "all"), then
   saveStore() and run(); contractor-shop change calls setSetting("contractor_shop", trimmed value or "CTR");
   contractor-line change calls setSetting("contractor_line", checked); btn-reset-moves calls resetMoves("all");
   btn-reset-auto calls resetMoves("auto").
2. controlsFromSettings(): fills moved-by, contractor-shop, contractor-line from DB.settings; fills zoom-from and
   zoom-to with "" plus every week of allWeeks(MOVED) and selects the stored values; never fires events.
3. renderDropStrip(): fills dropstrip with one span per week of effectiveWeeks(MOVED), class dropcell, data-week =
   the Monday, text M/D (from the Monday string, no leading zeros), each wired: dragover prevents default (so a
   drop is allowed), drop reads dataTransfer "text/plain" and calls dropOn(data, week).
4. dropOn(data, week): data is "job:<id>" or "project:<name>". For a job: key = the id trimmed and uppercased
   (addMove uppercases a job key the same way), and first = the earliest non-blank week_start among
   MOVED.consumption rows whose id (already trimmed and uppercased by applyMoves) equals key, so an id written in
   lower case still moves; for a project: first = the earliest week_start among
   MOVED.assigned rows of that project and MOVED.consumption rows of that project; weeks = weeksBetween(first,
   week); addMove(kind, key, weeks, "") when first is non-blank and weeks is not 0.
5. chip(kind, key): returns the HTML of a draggable chip (a span, draggable="true", class chip, text key, with
   ondragstart="event.dataTransfer.setData('text/plain', '<kind>:<key>')" written inline because a dragstart needs
   the event; escape the key).
6. renderProjectsStrip(): table projects-strip, one row per project among MOVED.assigned and MOVED.consumption
   (sorted): project, hull (from DB.projects or the consumption rows, "" if unknown), first week, last week (over
   its assigned rows and consumption spans), assigned hours, proposed hours, net shift (MOVED.projectShift or 0),
   then controls: a button "1 wk earlier" (addMove("project", p, -1, "")), a button "1 wk later" (addMove("project",
   p, 1, "")), a number input (default 2) and a button "Slip" (addMove("project", p, that number, "")), and the chip.
   A header row names the columns.
7. renderMoves(): table moves, one row per DB.moves entry in order: id, kind, key, weeks, performing, by, at, auto
   (yes or no), and an "undo" link calling removeMove(id). A line above the table: "<n> moves (<m> by the leveler)".
8. drillControls(shop, week): appends to drillbox a div id drill-moves: for each distinct proposed_id among
   GRID["shop|week"].proposedRows (rows read as `var r = e.row || e`), one line: the id, its project, its phase
   titles in that cell joined with ", ", its performing (and basis in parentheses), then buttons "1 wk earlier"
   (addMove("job", id, -1, "")), "1 wk later" (addMove("job", id, 1, "")), and either "Farm out"
   (addMove("performing", id, 0, "farm-out")) when performing is not "farm-out" or "Bring in"
   (addMove("performing", id, 0, "in-house")) when it is, and the chip("job", id). Then for each distinct project
   among assignedRows: the project name, buttons "1 wk earlier" and "1 wk later" for the project, and the
   chip("project", name). When the cell has neither, write "nothing to move here".
9. drill(shop, week): the hook: drillB1(shop, week); drillControls(shop, week).
10. afterMap(): ensureB2(); buildLevelerPanel(); controlsFromSettings(); renderDropStrip(); renderProjectsStrip();
    renderMoves(); then renderFarmout() and renderAuto(), both declared here as empty stubs (MODULE 7 and 8 declare
    them again).
11. A <style> element appended once by buildLevelerPanel: .chip (inline-block, border 1px solid currentColor,
    border-radius 999px, padding 1px 8px, cursor grab, margin-left 6px), .dropcell (inline-block, min-width 34px,
    text-align center, border 1px dashed currentColor, margin 2px, padding 2px 4px, cursor copy), #leveler-panel
    table (border-collapse collapse) and td, th (padding 3px 6px). Colors only through the page's existing CSS
    variables or currentColor.
12. At the end of the block: if MOVED is not null, call afterMap() (the page may already be drawn), else nothing.

Answer with the two <script> blocks only, the one-line block first, and nothing after them.
```

## Prompt B2-3: the farm-out list, the snapshot, present mode and the exports

```
Continue the same file. Write MODULE 7 in two parts: first a one-line <script> block containing exactly `var
exportCSVB1 = exportCSV;`, then one <script> block of plain global function declarations (no IIFE, no class, no
window assignment, no typeof guards, no declarations inside if blocks, no libraries, no em dashes). It declares
renderFarmout() again (replacing MODULE 6's stub), the snapshot, present mode, and exportCSV again as a hook.

Contract reminder: MOVED = {assigned, consumption, ...} (effective rows; consumption rows carry proposed_id,
project, hull, phase_no, phase_title, shop, shop_organic, load_hours, week_start, week_end, placement, source,
performing, performing_basis, moved_weeks); DB.settings {contractor_shop, contractor_line, zoom_from, zoom_to,
moved_by}; DB.moves; GRID keyed "shop|week" with {assigned, proposed, capacity}; DB.weeks and DB.shops are the
weeks and shops the map shows (already cut to the zoom); helpers $(id), esc, csvCell, num, spanWeeks, ensureB2,
setDownload (sets btn-download's href from csvout); elements band-lo, band-hi, view-mode (option values "Assigned
only", "Assigned + proposed", "Proposed only"), map (a table inside a scroll container), farmout-summary,
farmout-list, btn-snapshot, btn-copy-image, snapshot-link, snapshot-img, snapshot-status, btn-present, csvkind,
csvout, btn-download.

Write:
1. renderFarmout(): ensureB2(). Group MOVED.consumption rows whose performing is "farm-out" by proposed_id: one row
   per job in table farmout-list, sorted by first week then id: proposed_id, project, hull, phases (count), hours
   (sum of load_hours, one decimal), first week, last week, organic shops (distinct shop_organic joined with " "),
   basis (distinct performing_basis joined with " "), and a flag column: "guess" when any basis is "analogs",
   "manual" when any is "manual", else "". A header row names the columns. farmout-summary: "<n> jobs, <h> h
   farmed out" plus, when DB.settings.contractor_line is true, "; contractor line <code>: load <L> h against
   capacity <C> h over the shown weeks" where L and C are the sums of GRID[code|week].proposed + assigned and
   capacity over DB.weeks (0 when the line has no cells). When no job is farmed out: "nothing farmed out".
2. snapshot(): draws the map as shown into a canvas and offers it as a PNG. Read the view-mode, band-lo and band-hi
   like the map. Layout: left margin 90 px for the shop codes, top margin 54 px (title line and week labels), cells
   26 px wide and 20 px high with a 2 px gap, bottom margin 36 px for a legend; width = 90 + 28 times the number of
   weeks + 16; height = 54 + 22 times the number of shops + 36. Background white, text black, 12 px sans-serif
   (fixed colors: the image must look the same in light and dark mode). Title at the top left: "Resource Map:
   <first week> to <last week>, <view mode>, <date and time of the snapshot>". Week labels M/D every column (10 px
   font). One row per DB.shops: the shop code, then one rectangle per DB.weeks filled by the band of
   GRID[shop|week]: load = assigned, assigned + proposed, or proposed by the view mode; percent = 100 * load /
   capacity; capacity 0 is gray #dddddd; below band-lo #c9d6e3; band-lo to band-hi #6f9f7f; band-hi to 125
   #e3a85a; 125 to 150 #c9562f; above 150 #8e2417. Legend at the bottom: the five colors with their labels. Then
   dataUrl = canvas.toDataURL("image/png"); snapshot-img src = dataUrl; snapshot-link href = dataUrl;
   snapshot-status "snapshot <width> x <height> px". Keep the canvas in a variable for the copy button.
3. copyImage(): canvas.toBlob, then navigator.clipboard.write([new ClipboardItem({"image/png": blob})]) inside
   try; on success snapshot-status "copied to the clipboard", on failure "copy not allowed here: use Download PNG".
4. Present mode: togglePresent(on): adds or removes the class "present" on document.body. When turning on, the map's
   container ($("map").parentNode) and a bar div id present-bar (created once, with a button id btn-present-exit
   "Exit" and the text "Resource Map, <first week> to <last week>") get the class present-keep. A <style> appended
   once: body.present > *:not(.present-keep) { display: none } ; body.present #map td, body.present #map th {
   font-size: 1.15rem; padding: 10px 12px } ; #present-bar { display: none } ; body.present #present-bar { display:
   block } (so the bar shows only in present mode). Escape key exits (keydown on document, wired with an arrow
   function). btn-present calls togglePresent(true); btn-present-exit calls togglePresent(false).
5. exportCSV(kind): for moves, consumption_moved, assigned_moved and farmout_list fill csvout, set btn-download's
   download name to <kind>.csv and call setDownload(); otherwise call exportCSVB1(kind). Every cell through
   csvCell, CRLF, one header row, built in an array of lines and joined once:
   moves: id, kind, key, weeks, performing, by, at, auto (yes or no), in DB.moves order.
   consumption_moved: the 22 contract columns in order (proposed_id, hull, project, phase_no, phase_title, shop,
   est_hours_low, est_hours_high, charged_hours_low, charged_hours_high, load_hours, week_start, week_end, placement,
   summaries_used, same_class, top_score, analog_jcns, notes, source, performing, performing_basis) then moved_weeks
   and shop_organic, one line per MOVED.consumption row.
   assigned_moved: project, shop, week_start, assigned_hours, moved_weeks, src, one line per MOVED.assigned row.
   farmout_list: the columns of the farm-out table in order.
6. Wire, inside buildLevelerPanel's elements (they exist when this block runs after MODULE 6 built the panel; if
   the panel is not there yet, wire inside a function wireModule7() that afterMap will call: declare afterMap()
   again here as: ensureB2(); buildLevelerPanel(); controlsFromSettings(); renderDropStrip(); renderProjectsStrip();
   renderMoves(); wireModule7(); renderFarmout(); renderAuto()): btn-snapshot calls snapshot(); btn-copy-image calls
   copyImage(); btn-present calls togglePresent(true). wireModule7 wires once (keep a flag variable declared with
   var at the top of the block).
7. No em dashes.

Answer with the two <script> blocks only, the one-line block first, and nothing after them.
```

## Prompt B2-4: level and farm out automatically (do not simplify)

```
Continue the same file. Write MODULE 8: one <script> block of plain global function declarations (no IIFE, no class,
no window assignment, no typeof guards, no declarations inside if blocks, no libraries, no em dashes). It computes
an automatic leveling and farm-out as SUGGESTED moves, draws a comparison, and applies the suggestions into the moves
list on request. Implement every rule below exactly as written. Do not simplify, shorten or replace any rule with an
easier one, and do not leave a comment saying a rule was simplified.

Contract reminder: MOVED = {assigned, consumption, projectShift, jobShift, performing}: the effective rows after
the manual moves (consumption rows carry proposed_id, project, shop, shop_organic, load_hours, week_start,
week_end, placement, source, performing, performing_basis). DB.projects rows {project, hull, start, end} with Monday
strings. DB.capacity rows {shop, week_start, capacity_hours}. DB.settings.contractor_shop. DB.moves rows {id, kind,
key, weeks, performing, by, at, auto}. Helpers addWeeks, weeksBetween, spanWeeks, allWeeks, lookupProject,
ensureB2, num, $(id), esc, saveStore, run. Elements band-lo and band-hi (percent), auto-panel (an empty div in the
what-if panel). Global `var LEVELED = null;` declared at the top of this block. A job = all MOVED.consumption rows
with one proposed_id. A row's share in each week of its span = load_hours / (number of weeks in the span).

Write:
1. buildAutoPanel(): fills auto-panel once (if $("btn-level") exists, return) with: a heading "6. Level and farm out
   automatically", one sentence "Unplanned proposed jobs may move anywhere inside their project's window (the
   project list's start and end), in their phase order; planned and scheduled rows stay; then whole jobs go to the
   contractor's line where a shop is still over the band. Suggestions only, until Apply.", a button id btn-level
   "Level and farm out", a button id btn-apply-auto "Apply as moves", a button id btn-discard-auto "Discard", a div
   id auto-status, a table id compare, a table id auto-moves. Wire through arrow functions: btn-level calls
   levelAndFarm(); btn-apply-auto calls applyAuto(); btn-discard-auto sets LEVELED = null and calls renderAuto().
2. windowOf(project): search DB.projects (an array of rows {project, hull, start, end}) for the row whose project
   equals project, or, failing that, equals lookupProject(project); return {start: row.start, end: row.end} (Monday
   strings), or null when no row matches. lookupProject returns a project NAME, never a row.
3. jobsOf(moved): one object per proposed_id in moved.consumption: {id, project, rows, hours (sum of load_hours),
   first (the earliest non-blank week_start), last (the latest of week_end, or week_start where week_end is blank,
   over the rows that have a week_start), movable, lo, hi, flags: []}. movable is true only when every row has a
   non-blank week_start, no row has source "planned" or placement "scheduled", and windowOf(project) is not null;
   then lo = weeksBetween(first, window.start) and hi = weeksBetween(last, window.end), NOT clamped: lo is usually
   0 or negative (the weeks the job may move earlier) and positive when the job starts before its window and must
   move later; hi is usually 0 or positive (the weeks it may move later) and negative when the job ends after its
   window and must move earlier. When lo > hi (the job sticks out of its window on both sides) the job is not
   movable and gets the flag "outside its window". A job that is not movable has lo = hi = 0. Every job starts with
   shift = 0 and score = null; levelAuto sets them on the movable jobs only.
4. Grids keyed "shop|week" over ALL weeks (allWeeks(moved), the zoom ignored): capacityGrid() from DB.capacity
   (sum of capacity_hours); fixedGrid(moved, jobs): the sum of moved.assigned hours per shop-week plus the shares of
   every row of every job that is not movable. spreadJob(grid, job, shift, sign): for each row of the job, for each
   week w of spanWeeks(row), grid[row.shop|addWeeks(w, shift)] += sign * share (creating the key when missing).
5. levelAuto(moved): jobs = jobsOf(moved); order the movable jobs by float = hi - lo ascending, then hours
   descending, then id text ascending. R = a copy of fixedGrid. For each movable job in that order: for every
   candidate shift s from lo to hi in steps of 1: score = the largest, over every row of the job and every week w
   of its span, of (R[row.shop|addWeeks(w, s)] or 0 plus the row's share) divided by capacity[row.shop|
   addWeeks(w, s)]; when that capacity is 0 or missing the score is Infinity. Choose the s with the smallest score
   rounded to 3 decimals; on a tie, the smallest Math.abs(s); on a further tie, the smaller s. If every candidate
   is Infinity, s = 0. Record on the job: shift = s, score. Then spreadJob(R, job, s, +1). Return {jobs, leveled: R,
   fixed, capacity, weeks: allWeeks(moved), shops: the sorted unique shops across capacity, fixed and jobs}.
6. farmAuto(level): hi = num($("band-hi").value) / 100 (the high band as a fraction); ctr =
   DB.settings.contractor_shop. F = a copy of level.leveled; farmed = []; overtime = []. Loop at most 10000 times:
   over the shops of level.shops except ctr and the weeks of level.weeks where capacity > 0, ratio = F / capacity;
   worst = the shop-week with the largest ratio among those with ratio > hi and not in overtime (ties: the
   earliest week, then the smallest shop text); if there is none, stop. excess = (ratio - hi) times capacity.
   Candidates: jobs (movable or not) that are not planned (no row with source "planned" or placement "scheduled"),
   not already farmed in this loop, whose effective performing is not "farm-out", and that have a row whose shop
   is the worst shop and whose shifted span (the job's shift from levelAuto, 0 for a non-movable job) covers the
   worst week; a candidate's weekly hours in that shop-week = the sum of the shares of its rows there. If there is
   no candidate, push the worst "shop|week" onto overtime and continue. Among candidates whose weekly hours >=
   excess pick the one with the smallest weekly hours; if none, pick the one with the largest weekly hours; ties:
   the smaller hours total, then id text. Mark it farmed: spreadJob(F, job, job.shift, -1) for its organic shops,
   then add its shares to F under the key ctr|week for the same weeks (so the contractor line carries it), push
   {id, project, hours, shift: job.shift, reason: "shop <shop> week <week> at <round(ratio times 100)>% over the
   band"} onto farmed. Return {farmed: F, farmedJobs: farmed, overtime}.
7. levelAndFarm(): ensureB2(); level = levelAuto(MOVED); farm = farmAuto(level); LEVELED = {level, farm, before:
   the grid of MOVED as is (fixedGrid plus every movable job at shift 0)}; renderAuto().
8. compareCounts(grid, capacity, weeks, shops): per shop: weeks over (ratio > hi), in (lo <= ratio <= hi), under
   (ratio < lo), counted over the weeks with capacity > 0, with lo and hi read from band-lo and band-hi as
   fractions. renderAuto(): ensureB2(); buildAutoPanel(); when LEVELED is null: auto-status "not run", compare and
   auto-moves emptied; else auto-status "<m> of <n> unplanned jobs moved by leveling; <f> jobs farmed out (<h> h);
   <o> shop-weeks still over the band (overtime)"; table compare: one row per shop in level.shops with, for
   before, leveled and farmed: over / in / under; table auto-moves: one row per movable job with shift not 0 ("job", id,
   shift weeks, score) and one per farmed job ("performing", id, "farm-out", reason).
9. applyAuto(): ensureB2(); drop the DB.moves entries with auto true; for each MOVABLE job whose shift is not 0
   push {id: the next id (a NUMBER, 1 + the largest id in DB.moves, the way addMove does it; never text), kind:
   "job", key: id, weeks: shift, performing: "", by: "leveler", at: now, auto: true}; for each farmed job push
   {id: the next number, kind: "performing", key: id, weeks: 0, performing: "farm-out", by: "leveler", at: now,
   auto: true}; LEVELED = null; saveStore(); run().
10. renderAuto() is declared here (replacing MODULE 6's stub); afterMap calls it, so the panel is rebuilt after
    every map draw. No em dashes.

Answer with the one <script> block only, and nothing after it.
```

## Prompt B2-5: check the assembled file (run before opening the page)

```
I have assembled the file from your B2 answers on top of the Resource Map built in B1 to B4. Without rewriting it,
check it for the mistakes that usually break a file built in pieces, and list each one with the exact fix:
1. Every function called but not defined; every name declared twice where the later one is not the intended
   replacement (importFiles, renderMap, drill, exportCSV, afterMap, renderFarmout and renderAuto are redeclared on
   purpose, each after a one-line block that captures the earlier one where a capture is needed; check those
   one-line blocks come BEFORE the redeclaration and AFTER the earlier declaration, in their own block).
2. Every element id used in JavaScript that the page does not have after buildLevelerPanel() and buildAutoPanel()
   run, and the reverse.
3. Shapes: MOVED rows carrying week_start and week_end as Monday strings, not Dates; DB.moves read and written
   under the same keys; GRID proposedRows entries read as `e.row || e`; the stored DB never holding moved rows (the
   renderMap hook puts the baseline rows back in finally).
4. Dates: every Date built with Date.UTC and read with UTC getters; addWeeks and weeksBetween used for every week
   step; no new Date(text) on a month/day/year string.
5. The rules: the leveler's candidate score uses the running load plus the job's own share and treats a missing
   or zero capacity as Infinity; a job never moves outside its project's window; a planned or scheduled row never
   moves; the farm-out loop stops when nothing is over the band or at 10,000 passes; a farmed job's hours land on
   the contractor's line, not vanish.
6. The flow: importFiles keeps non-B2 files for importFilesB1 and handles consumption itself; renderMap swaps the
   effective rows in and the baseline rows back; run never calls rebuildIndex; afterMap draws the panel after
   every map draw and rebuilds the drop strip from the shown weeks.
7. Anything blocked by the Content-Security-Policy (the snapshot uses a canvas and a data: URL, which the policy
   allows for img-src); any <script> left unclosed; any placeholder left in.
8. That importConsumption keeps every line of a file (a job has one row per phase AND shop) and, on a re-import,
   drops the file's jobs whole before appending, never matching by proposed_id and phase_no.
Then give me a five-step test using the two resource map sheets, a six-line consumption.csv with a performing
column, a two-line lookup.csv, a two-line projects.csv, a contractor capacity.csv, and what I should see after each
step: the status lines, one cell that changes after a 1-week move, the contractor line after a farm-out, and one
leveler suggestion.
```

## Debug prompts

Use the two Debug prompts of series B (`GENAI-PROMPTS-resource-map.md`) unchanged: one for an error, one for a
wrong number with no error.

## Inputs this series expects (all optional, all through the same file picker)

- `lookup.csv`: map_name, project, hull. One row per project on the workforce map, with the project id the JCN
  history and the estimator use. Prompt L in the build guide drafts it from the two name lists.
- `projects.csv`: project, hull, start, end. The windows the leveler moves inside. If the workforce map carries the
  dates (Prompt A says), the data sheet spec can make MODULE 2 produce these rows; else this small pull.
- `capacity-contractor.csv`: shop, week_start, capacity_hours, for the contractor's line when the workforce map does
  not carry it as a shop row.
- the estimator's `consumption.csv` with its 22 columns (source, performing, performing_basis are what the
  contractor line and the farm-out list read).

## What is not here

- Float per phase from a schedule export (v0.1's idea): the window is the availability. A schedule export with
  early start and late finish per phase would narrow it; that is a later prompt, once such an export exists.
- Ties between jobs (job B after job A): not honored; the leveler keeps phase order inside a job only.
- The emergent reserve (the owner, 2026-10-22: later).

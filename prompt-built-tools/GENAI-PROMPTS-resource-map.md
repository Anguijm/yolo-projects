# Prompts B: build the Resource Map app inside GenAI.mil

Version 0.6, 2026-10-25 (v0.1 to v0.5 kept in the private source). v0.6 changes one import rule in B2: a consumption file has one
line per job, phase AND shop (the estimator series v0.7 estimates per phase and shop, from the task records of the
owner's pulls), so a re-import replaces each job's lines whole, by proposed_id, instead of replacing by proposed_id
and phase_no, which kept one shop per phase and dropped the rest (found 2026-10-25 on a several-shops file: 182
lines in, 104 kept, the status line still saying 182). MODULE 2 regenerated from this text, the v0.5 harness rerun
and a several-shops import check added (the private test record, "v0.6"). v0.5 (2026-10-23) was the
first version regenerated end to end from its own text since the v0.2 fixes were written in: B1 to B4 against Gemini with no code execution, assembled as written,
and the result matched the hand check cell for cell on the first assembly, with no Debug round
(the private test record, "v0.4 regenerated"). Three small things learned there are written in:
the view mode "Assigned + proposed" is selected by default (B1), setDownload is written in full by B4 (the skeleton
had left it a stub, so the download link stayed empty), and B2 names the three long-format tables one by one. One
thing that is not a fault but worth knowing: the chat must hold the step-1 contract when B3 and B4 run (it does in
one chat; a test that fed B3 only the skeleton's code got rows keyed "week" instead of "week_start"). Series B2
(`GENAI-PROMPTS-resource-map-leveling.md`: moves, the contractor line, zoom, snapshot, automatic leveling)
runs after B4, and the style prompt (`GENAI-PROMPTS-style.md`) last. v0.4 only changed how the files get in:
Prompts X let the app take the Excel workbook itself, see `GENAI-PROMPTS-xlsx.md`; v0.3 added two
clarifications from the reviewer's review of PR 52: verdict precedence and a made-up label on the debug example.
Tested originally against Gemini with no code execution, the way the
chat inside works: the v0.1 prompts built a file that opened without errors but had four faults (the
index named two ways, consumption fields stored without underscores, dates shifted a week on a computer
in Japan time, and nothing calling the verdicts or export after import). Three were found by the check
prompt (B5) before opening the page; all four were fixed by one round of the Debug prompts; the file
then matched a hand calculation cell for cell and kept its data across a reload. v0.2 writes those
fixes into the prompts so they do not happen. Test records: the private test record.

Series B1 (this file): import the resource maps and the estimator's consumption file, keep them in a
local store, show shop by week load with drill-down, export. Series B2 (leveling, farm-out, what-if)
comes after B1 works.

Before Prompt B1, run Prompt A (`GENAI-PROMPTS-resource-map-analysis.md`) on the real workbooks and
bring out its data sheet spec. B1 and B2 paste that spec in. If the spec leaves the week-label rule
unknown, write it in yourself before pasting (which Monday "WK01" is): the app needs one rule.

How to use: one chat, prompts in order, each answer's code block pasted as the prompt says, save as
`resource-map.html`, open in Edge or Chrome. Full order for the whole app: B1, B2, B3, B4, B5 (check), then series
B2 (B2-1 to B2-5, the leveler), then Prompts X and X2 if the workbooks are to be chosen directly (X2 must come after
B2 so its hook wraps B2's importer), then Prompt S (the look) last. Without Prompts X, save each sheet as CSV (File,
Save As, CSV UTF-8) and choose those CSVs. Run Prompt B5 before opening the page; the Debug prompts at the
end are the way back from an error or a wrong number.

## Contract (repeated in every prompt)

Tables, all long format, stored in IndexedDB (database "resourcemap"):
- `assigned`: project, shop, week_start, assigned_hours, src (the sheet and row it came from)
- `capacity`: shop, week_start, capacity_hours, src
- `projects` (optional): project, hull, start, end
- `consumption` (from the estimator): proposed_id, hull, project, phase_no, phase_title, shop,
  est_hours_low, est_hours_high, charged_hours_low, charged_hours_high, load_hours, week_start, week_end,
  placement, summaries_used, same_class, top_score, analog_jcns, notes. Rows are stored under exactly
  these names, underscores included, whatever the CSV header spelled. A job has one line per phase AND
  shop (a phase worked by three shops is three lines); later columns (source, performing,
  performing_basis, tasks) ride along and are ignored here.

week_start is always the Monday, as YYYY-MM-DD text. Every Date is built with Date.UTC from parsed parts
and read with UTC getters, never with new Date(text) on a month/day/year string, so the same file gives
the same weeks on any computer.

Globals: `DB` = {assigned: [], capacity: [], projects: [], consumption: [], weeks: [sorted unique
week_start strings], shops: [sorted unique shop codes]}; `GRID` = the per-shop-week index, a plain object
keyed "shop|week" holding {assigned, proposed, capacity, assignedRows, proposedRows}, rebuilt by
renderMap(); `UNPLACED` = a plain object keyed by shop with the proposed hours that have no week_start;
`SEL` = {shop, week}.

Flow: importFiles() and loadStore() end by calling rebuildIndex(); rebuildIndex() ends by calling run();
run() draws everything (map, verdicts, export box); every view control calls run(). Nothing else calls
renderMap directly.

Global functions: parseCSV(text), importFiles(fileList), sheetToRows(name, rows) (applies the data sheet
spec), rebuildIndex(), saveStore(), loadStore(), forgetStore(), renderMap(), renderVerdicts(),
drill(shop, week), exportCSV(kind), setDownload(), run(). Helpers: $(id), esc(s), toDate(s), fmtDate(d),
mondayOf(d), num(s), csvCell(v). Every function is a plain global function declaration; events are wired
through arrow functions; no IIFE, no window assignment; no network; no libraries; no em dashes.

Element ids: files, datastatus, mapping, store-line, view-mode, band-lo, band-hi, filter-project,
filter-shop, map, drillbox, verdicts, csvkind, csvout, btn-copy, btn-download.

---

## Prompt B1: the page skeleton, with the data sheet spec

```
I am building a small offline tool for a ship repair planning department: a Resource Map. It is ONE
self-contained HTML file that runs in a browser on a work computer with no network, no installation and
no libraries. You will build it with me in steps. In this step, write only the skeleton: page, styling,
helpers, a small IndexedDB layer, and stub functions with exact names. Later steps fill the stubs.

What the tool does: it reads the command's resource map spreadsheets (saved as CSV, one per sheet) that
hold hours assigned by project, shop and week, and shop capacity by week; it reads a "consumption" CSV
from a separate estimator tool that holds hours expected for proposed work by shop and week; it keeps
all of that in the browser's local database so the import happens once; and it shows, for every shop
and week, how loaded the shop is, with the ability to click any cell and see which projects, proposed
items and source rows make up that load. It exports CSVs that open in Excel as pivot tables.

Here is the description of the real spreadsheets, produced by a structure-only analysis (no record
content). Keep it in mind for step 2, which writes the sheet reader from it:

<PASTE THE DATA SHEET SPEC HERE>

Hard rules for the file:
- Plain HTML, CSS and vanilla JavaScript only. No frameworks, no CDN links, no web fonts, no fetch, no eval.
- In the head: <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src
  'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; connect-src 'none'; form-action 'none'">
- Works in Edge and Chrome; readable on a narrow window; tables scroll sideways inside their own
  container; 16px side gutter; system font stack; light and dark via prefers-color-scheme with CSS
  variables for every color. No em dashes anywhere.
- Reads files only through <input type="file" multiple>; writes only through a download link and a
  textarea.
- Every function is a plain global function declaration at the top level of a script block; later steps
  replace a stub by declaring the same name again in a later block; never wrap code in an IIFE or assign
  to window; wire events through arrow functions (() => run()), never by passing the function itself.
- Dates: build every Date with Date.UTC(year, month - 1, day) from parsed parts and read them only with
  UTC getters (getUTCDay, getUTCDate, ...). Never call new Date(text) on a month/day/year string: it
  parses as local time and shifts a day on a computer that is not on UTC. Week keys are text,
  YYYY-MM-DD, always a Monday.

The contract every later step relies on (keep names exactly):
- Tables, all long format: assigned (project, shop, week_start, assigned_hours, src), capacity (shop,
  week_start, capacity_hours, src), projects (project, hull, start, end), consumption (proposed_id, hull,
  project, phase_no, phase_title, shop, est_hours_low, est_hours_high, charged_hours_low,
  charged_hours_high, load_hours, week_start, week_end, placement, summaries_used, same_class, top_score,
  analog_jcns, notes). Rows are stored under exactly these names, underscores included.
- Globals: let DB = {assigned: [], capacity: [], projects: [], consumption: [], weeks: [], shops: []};
  let GRID = {} (the per-shop-week index, keyed "shop|week", filled by renderMap in step 3);
  let UNPLACED = {} (proposed hours with no week, keyed by shop); let SEL = {shop: null, week: null};
  let SPEC = null.
- Flow: importFiles() and loadStore() end by calling rebuildIndex(); rebuildIndex() ends by calling
  run(); run() draws everything; every view control calls run().
- Global functions: parseCSV(text), importFiles(fileList), sheetToRows(name, rows), rebuildIndex(),
  saveStore(), loadStore(), forgetStore(), renderMap(), renderVerdicts(), drill(shop, week),
  exportCSV(kind), setDownload(), run().
- Helpers: $(id), esc(s), toDate(s) (YYYY-MM-DD, MM/DD/YYYY, DD-MON-YYYY, and an Excel serial number,
  all built with Date.UTC), fmtDate(d) (YYYY-MM-DD from UTC getters), mondayOf(d) (the Monday on or
  before d, as YYYY-MM-DD, computed with UTC getters; accepts a Date or a YYYY-MM-DD string), num(s),
  csvCell(v).
- Element ids: files, datastatus, mapping, store-line, view-mode, band-lo, band-hi, filter-project,
  filter-shop, map, drillbox, verdicts, csvkind, csvout, btn-copy, btn-download.

Write the skeleton now:
1. Sections in order: "1. Load" (file input id files, a status line id datastatus, an empty div id
   mapping, a line id store-line for the stored data and its buttons), "2. View" (a select id view-mode
   with options "Assigned only", "Assigned + proposed" (selected by default), "Proposed only"; two number inputs id band-lo
   and band-hi with defaults 80 and 100 and the label "fully loaded band, percent"; a select id
   filter-project with a first option "All projects"; a select id filter-shop with "All shops"), "3.
   Shop by week" (an empty table id map inside a scrolling container, then an empty div id drillbox
   with the hint "Click a cell to see what is in it", then an empty table id verdicts), "4. Export" (a
   select id csvkind with options assigned, capacity, consumption, shop_week_summary; a textarea id
   csvout; a button id btn-copy "Copy CSV"; a link id btn-download "Download"). One sentence under the
   title: the page works offline and nothing leaves the computer.
2. Helpers fully written, as listed. toDate must also accept an Excel serial number (days since
   1899-12-30) because CSVs saved from Excel sometimes carry dates that way.
3. A small IndexedDB layer, fully written: openStore() returning a promise of the database "resourcemap"
   with one object store "tables"; saveStore() writes one record keyed "data" holding {savedAt, DB};
   loadStore() reads it back into DB and then calls rebuildIndex() (nothing else); forgetStore() deletes
   it and empties DB, then calls rebuildIndex(). Every call wrapped so a failure only writes a message
   into store-line and never breaks the page.
4. The globals listed in the contract.
5. Stubs, one line each, for every contract function that is not a helper or the store layer; the run()
   stub is empty.
6. Event wiring at the bottom through arrow functions: files change calls importFiles(the list);
   view-mode, band-lo, band-hi, filter-project and filter-shop change call run(); csvkind change calls
   exportCSV(the selected kind); btn-copy copies csvout; setDownload() sets btn-download's href from
   csvout as a Blob URL; on load, call loadStore().
7. Placeholders after the main script: <!-- MODULE 2: import -->, <!-- MODULE 3: map and drill -->,
   <!-- MODULE 4: export and verdicts -->.

Answer with the complete file in one code block and nothing after the block.
```

## Prompt B2: import the sheets and the consumption file

```
Continue the same file. Write MODULE 2: a single <script> block to paste over <!-- MODULE 2: import -->.
It replaces the stubs parseCSV, importFiles, sheetToRows and rebuildIndex by declaring plain global
functions of the same names. Keep every contract name exactly. The data sheet spec from step 1 is the
authority for how the sheets are laid out; if this chat is long, here it is again:

<PASTE THE DATA SHEET SPEC HERE AGAIN, OR WRITE "see step 1">

Contract reminder: DB = {assigned, capacity, projects, consumption, weeks, shops}; assigned rows are
{project, shop, week_start, assigned_hours, src}; capacity rows {shop, week_start, capacity_hours, src};
projects {project, hull, start, end}; consumption rows carry the 19 contract fields under exactly those
names (proposed_id, hull, project, phase_no, phase_title, shop, est_hours_low, est_hours_high,
charged_hours_low, charged_hours_high, load_hours, week_start, week_end, placement, summaries_used,
same_class, top_score, analog_jcns, notes), with the hours as numbers and week_start, week_end as Monday
strings. A job has one line per phase AND shop (a phase worked by three shops is three lines); later columns
(source, performing, performing_basis, tasks) ride along and are ignored here. A CSV header is matched to a field by comparing both with case, spaces, underscores and
punctuation removed, but the row is stored under the contract name with its underscores, never under
the squashed header. Helpers $(id), esc, toDate, fmtDate, mondayOf, num, csvCell. Elements files,
datastatus, mapping, store-line, filter-project, filter-shop. rebuildIndex() ends by calling run().

Requirements:
1. parseCSV(text): a real CSV parser (quoted fields, doubled quotes, line breaks inside quotes, CRLF,
   leading byte-order mark), returning an array of arrays (rows of cells), because the resource map
   sheets have header blocks that are not a single header row.
2. importFiles(fileList): read each file as text in 4 MB slices (file.slice, read as text), carrying
   the incomplete last record across slices; parse; then classify the file:
   a. A consumption file: a header row that contains proposed_id and load_hours. Map by header names as
      above, keep rows as objects under the contract names, numbers through num(), week_start and
      week_end through mondayOf(toDate()). Before appending, drop every earlier DB.consumption row
      whose proposed_id (trimmed, uppercased) appears in this file, then append all of the file's rows:
      a re-import replaces each job whole. Never replace by proposed_id and phase_no: a phase has one
      line per shop, and that rule would keep one shop and drop the others.
   b. A long-format table, three kinds, each one handled: a header row containing project, shop, week_start
      and assigned_hours goes to assigned; shop, week_start and capacity_hours (no project) goes to capacity;
      project, hull, start and end (no shop, no week_start) goes to projects. Map by names, mondayOf the week
      or the dates, append to the matching table.
   c. Otherwise a resource map sheet: call sheetToRows(file name, rows). It returns {assigned: [...],
      capacity: [...], projects: [...], skipped: n, notes: [...]}; append its rows.
   After each file, write into datastatus what it was taken for and how many rows it gave, and any notes
   (for example "12 subtotal rows skipped", "week label format not recognized in column Q"). If a sheet
   could not be classified, say so and list its first header cells so the user can tell. When the last
   file is done, call rebuildIndex().
3. sheetToRows(name, rows): implement the MAPPING section of the data sheet spec exactly: find the real
   header row by the rule the spec gives; identify the key columns by their header text; identify the
   week columns and convert each week label to the Monday by the spec's rule (write that rule as one
   clearly named function, weekLabelToMonday(label), built with Date.UTC, so it can be corrected in one
   place); a week header that is a date goes through mondayOf(toDate()); carry implied values down
   through blank continuation cells where the spec says so; skip the total and subtotal rows and
   columns the spec describes; treat blank as zero only if the spec says so; use the spec's identifier
   rules so shop codes and project names come out in one consistent form across sheets (write
   normalizeShop(s) and normalizeProject(s)). Each produced row's src is "<file>:<row number>:<column
   letter>". Where the spec says a sheet holds capacity, produce capacity rows; where it says assigned,
   produce assigned rows; where a project sheet exists, produce projects rows.
4. rebuildIndex(): recompute DB.weeks (sorted unique Mondays across assigned, capacity and consumption,
   expanded so consumption rows with week_start and week_end cover every Monday between them) and
   DB.shops (sorted unique). Fill filter-project (all projects from assigned and consumption) and
   filter-shop, keeping the current selection if it still exists. Then call saveStore() and run().
5. A mapping panel in div mapping only when a long-format or consumption file is missing a required
   column: file name, field, a select of that file's headers; choosing one re-imports that file.
6. No em dashes. No network access.

Answer with the one <script> block only, and nothing after it.
```

## Prompt B3: the map and the drill-down

```
Continue the same file. Write MODULE 3: a single <script> block to paste over <!-- MODULE 3: map and
drill -->. It replaces the stubs renderMap, drill and run by declaring plain global functions of the same
names. Keep every contract name exactly.

Contract reminder: DB = {assigned, capacity, projects, consumption, weeks, shops}, rows as in step 1;
consumption rows have load_hours (number), phase_title, placement, notes, analog_jcns, project, shop,
and a week_start to week_end span (Monday strings). The index lives in the GLOBAL GRID declared in step
1 (a plain object keyed "shop|week" holding {assigned, proposed, capacity, assignedRows, proposedRows});
renderMap() refills it in place (empty it, then fill it; do not declare another variable for it). The
global UNPLACED (keyed by shop) gets the proposed hours that have no week_start. Elements: view-mode,
band-lo, band-hi, filter-project, filter-shop, map, drillbox. Helpers $(id), esc, fmtDate. Global SEL =
{shop, week}. In this step run() is simply renderMap(); step 4 declares run() again to add the verdicts
and the export. Never call rebuildIndex() from run() or renderMap(): rebuildIndex calls run.

How the map is computed:
1. Spread each consumption row's load_hours evenly over the Mondays from week_start to week_end
   inclusive (one week if they are equal or week_end is blank). Walk the weeks with UTC date
   arithmetic (setUTCDate(getUTCDate() + 7)) from a Date built by Date.UTC from the week_start text.
   Rows with a blank week_start go to UNPLACED[shop], not on the grid.
2. For each shop and week: assigned = sum of assigned_hours (filtered by project if a project filter is
   set); proposed = the spread load_hours (same filter, on consumption.project); capacity = sum of
   capacity_hours. Load percent depends on view-mode: Assigned only uses assigned; Assigned + proposed
   uses assigned + proposed; Proposed only uses proposed. Percent = 100 * load / capacity; if capacity is
   0, show "n/a" and a muted cell.
3. Colors: below band-lo = under (cool), band-lo to band-hi = in band (green), band-hi to 125 = over
   (amber), 125 to 150 = red, above 150 = dark red. Use CSS variables.
4. renderMap() draws table map: one row per shop (filtered by filter-shop), one column per week in
   DB.weeks, a month label row on top, each cell showing the percent with its color, a title attribute
   "shop, week, load/capacity hours", and a click handler that sets SEL and calls drill(shop, week). A
   last column "Unplaced" shows UNPLACED[shop].
5. drill(shop, week) fills drillbox: a heading "shop, week of <date>: assigned X h, proposed Y h,
   capacity Z h, load N%", then a table of contributors sorted by hours: for assigned, one line per
   project with its hours and a "show rows" toggle that lists the source rows (src, hours); for
   proposed, one line per proposed item showing proposed_id and phase_title, its load_hours share in
   that week, placement and notes, and a toggle listing the analog_jcns. A "close" link clears the box.
6. run() = renderMap(). Keyboard: cells are focusable and Enter opens the drill.
7. No em dashes. Keep drawing fast: build the table as one HTML string and set innerHTML once; fill
   GRID once per renderMap, not per cell.

Answer with the one <script> block only, and nothing after it.
```

## Prompt B4: export and shop verdicts

```
Continue the same file. Write MODULE 4: a single <script> block to paste over <!-- MODULE 4: export and
verdicts -->. It replaces the stubs exportCSV and renderVerdicts, and declares run() again so that
run() = renderMap(); renderVerdicts(); exportCSV(the kind selected in csvkind); setDownload(). Plain
global functions, contract names exact. Do not touch renderMap, rebuildIndex or the store layer. Also
declare setDownload() again in full, with no parameters (the skeleton may have left it a stub): it sets
btn-download's href to a Blob URL made from the text in csvout (type text/csv;charset=utf-8), revoking
the previous URL if one was made; exportCSV sets btn-download's download name before calling it.

Contract reminder as in step 1. The per-shop-week index is the global GRID (plain object keyed
"shop|week" with {assigned, proposed, capacity, ...}), filled by renderMap(), so renderVerdicts and
exportCSV must run after renderMap, which run() guarantees. Elements: verdicts, csvkind, csvout,
btn-download; helpers csvCell, setDownload, num; the band inputs band-lo and band-hi and the select
view-mode.

1. exportCSV(kind): fills csvout and calls setDownload(). kinds: assigned, capacity, consumption (each
   the table as stored, one header row in the contract's column order, every cell through csvCell,
   CRLF); shop_week_summary: one line per shop and week with shop, week_start, assigned_hours,
   proposed_hours, capacity_hours, load_percent (for the current view-mode and filters), band ("under",
   "in band", "over"). These open in Excel as pivot tables, so no merged cells, no totals rows.
2. renderVerdicts(): table verdicts, one row per shop: average load percent over the weeks that have
   capacity (total hours over total capacity), peak percent, weeks over the band, weeks under it, and
   one plain verdict: "balanced", "spare capacity: pull work in or lend people", "over in peaks:
   contractor or overtime", "short of people all year" (average above the band). Thresholds: over in
   peaks when more than 8 weeks are over. When more than one applies, the first of these wins: short of
   people all year, over in peaks, spare capacity, balanced.
3. The download file name follows the kind: assigned.csv, capacity.csv, consumption.csv,
   shop_week_summary.csv.
4. No em dashes.

Answer with the one <script> block only, and nothing after it.
```

## Prompt B5: check the assembled file (run it before opening the page)

```
I have assembled the file from your four answers. Without rewriting it, check it for the mistakes that
usually break a file built in pieces, and list each one with the exact fix:
1. Every function called but not defined, and every function defined twice where the later one is not
   the intended replacement (run is declared in step 3 and again in step 4 on purpose).
2. Every element id used in JavaScript that does not exist in the HTML, and the reverse.
3. Values used across modules under different names or shapes: the index read under a name other than
   GRID; consumption fields stored under squashed header names (loadhours) but read with underscores
   (load_hours), or the reverse; week_start as a Date in one place and a string in another; load_hours
   as text; DB.weeks containing dates that are not Mondays.
4. Any Date built with new Date(text) from a month/day/year string, or any date read with local getters
   (getDay, getDate) instead of UTC getters: either one moves weeks by a day on a computer that is not
   on UTC.
5. The flow: that importFiles and loadStore end in rebuildIndex, that rebuildIndex ends in run, that
   run draws the map, the verdicts and the export box, and that no path calls rebuildIndex from run
   (an endless loop) or leaves the verdicts stale after a view change.
6. The IndexedDB round trip: anything stored that would not come back the same (Dates, Maps, Sets).
7. Anything blocked by the Content-Security-Policy; any <script> left unclosed; any placeholder left in.
8. That a consumption file's lines are all kept (a job has one line per phase AND shop), and that
   importing the same file again leaves the same count: earlier rows of a job in the file are dropped
   whole, never matched by proposed_id and phase_no.
Then give me a five-step test using the two resource map sheets saved as CSV plus a three-line
consumption.csv, and what I should see after each step.
```

## Debug prompt, for an error

```
I opened the assembled file and did this: <what you clicked>. The browser console (F12) shows this error:

<paste the red text here, exactly>

Find the cause in the file you wrote and answer with only the corrected function or block, named so I
can paste it over the old one. Do not change anything else.
```

## Debug prompt, for a wrong number (no error shown)

```
I opened the assembled file and did this: <what you loaded and clicked>. I expected <what the sheet or
the arithmetic says, for example, with made-up figures, "shop 11 in the week of 10/05 should show 200
assigned hours against 1376 capacity, 15%">. The page shows <what it shows, for example "a column for 09/28 that is in no
sheet, and 0% in that cell">. There is no console error.

Find the cause in the file you wrote and answer with only the corrected function or block, named so I
can paste it over the old one. Do not change anything else.
```

In the test here, three of the four faults were silent and were fixed through this second form.

## Series B2 and the look

Series B2 (`GENAI-PROMPTS-resource-map-leveling.md`) adds the leveler on top of B1 to B4: moves kept as an
overlay on the dates of record (drag a job, drag a project, farm out by hand), the contractor's own line, the
project-name lookup, zoom, snapshot, present mode, the moves and farm-out exports, and an automatic level and
farm-out inside each project's window. Prompt S (`GENAI-PROMPTS-style.md`) gives the page the demo's look
and runs last.

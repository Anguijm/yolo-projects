# Prompts for GenAI.mil: build the JCN analog estimator inside the enclave

Version 0.7, 2026-10-25 (v0.1 to v0.6 kept in the private source). v0.7 moves the history to the shape of the owner's own
pulls, as he described and ruled on 2026-10-25: a job summary holds phases, and inside each phase there is a tasks
table, one record per task, with the shop, the task that shop is to do, the crew size and the man-hour estimate; the
shop's charges land on its task; the material is one record per item keyed by job summary and phase number. The pull
is ONE flat task table in which every record repeats the phase-level fields (title, description block, planned and
actual dates), and the tool derives the phases from it. The estimate is therefore built per phase AND shop: for each
phase of the newest similar job, one row per shop, that shop's tasks summed within the phase, low to high across the
similar jobs. (v0.6 keyed a phase by its title alone and assumed one shop per phase; on a phase worked by three shops
it listed three rows and gave every one the first shop's hours. Found on the third made-up data set, 2026-10-25.)
Crew size is read and not used (the owner's ruling). The `tasks` table replaces `phases` in Prompts 1 and 2;
DB.tasksByJS holds the task rows and DB.phasesByJS the derived phases; Prompt 4 is rewritten; Prompt 5 gains two
checks; the estimate CSV gains a tasks column. The tune series (v0.3), the batch series (v0.9), the planned series
(v0.6), the Resource Map (v0.6) and the leveler (v0.5) move with it, all in one round. Regenerated from this text and
tested against a Python twin on the fourth made-up data set (test record kept in the private source).
v0.6 (2026-10-24) fixed one thing from the review of PR 71
(the reviewer, 2026-10-24): maxScore() now counts W.hullNear, because hull nearness scores same-class rows, and without it a
same-class perfect match would show a strength above 100 percent once the weight test gives hull nearness a weight;
family stays out, since a row of the new JCN's own class can never score it. Prompt 3 step 7 and check 7b say so;
the matcher was regenerated from this text and the twin harness gained two checks for it. v0.5 added the owner's ruling R2 of 2026-10-24: a class-family
table and hull nearness, both typed by the planner and zero by default, as two more weighted features (family counts
only for rows of another class, so it orders the fallback rows; hull nearness only within the class). Prompt 1 gains
the family box, Prompt 3 the two features, Prompt 5 one check; the weight test (tune series v0.2) reads the feature
keys from DEFAULT_W, so it covers them without a change of its own. Regenerated from this text and tested against a
Python twin of every rule on made-up data (32 checks, 0 bad; test record kept in the private source). v0.5 also takes the review of PR 69 (the reviewer,
2026-10-24): buildWeightsPanel() stays as an alias of renderWeights() for the batch and planned series; a function
loadSavedWeights() that later modules call again after they add weight keys; the attainable score from each
group's highest weight, so the strength line cannot pass 100 percent after a fit; a recency scale of 0 means no
recency factor (the factor is exp(-age / scale), not a half-life); two blank space numbers never match; a missing
text scores 0. Known overlap, kept on purpose: the third equipment tier (same system) scores the same first SWLIN
character as the lowest SWLIN tier; it exists so the equipment gate does not fire on a same-system job. Earlier
versions are kept in the private source. v0.4 was the matcher the three-reviewer review and the owner's
rulings of 2026-10-24 asked for: the discrepancy text is matched (action words and object words, after an
editable abbreviation dictionary; this was in the design of 2026-10-20 and the v0.1 prompts had lost it); the
equipment nomenclature is scored by shared words; the SWLIN is scored by how much of its code two jobs share (one,
two, three, five characters, or all of it); the space number counts only within the class and little even there;
every past job is scored as a feature list times the weights, so the weight test (the separate tune series) can
re-weight without re-matching; an optional gate holds back jobs that match the equipment at no tier (off by
default, a weight the test can set); a match strength is shown, labeled as strength. Prompt 1 gains the text
field, the dictionary box and the tune section; Prompt 2 the optional discrepancy column; Prompt 3 is rewritten;
Prompt 4 pins the EST shape the batch series reads (rows, used, usedJcns, notes); Prompt 2 names the pieces the
batch series extends (SCHEMA, RAW_DATA, MAPPINGS, cleanCol, detectType, updateStatus, OPTIONAL_FIELDS); Prompt 5
gains three checks.
v0.3 (2026-10-23) listed material whole for grouped summaries; v0.2 (2026-10-20) closed four mismatches between
the pieces (see the private test record).

Scope of this series: load exports, enter a new JCN, list the ten closest same-class past jobs with reasons and
a match strength, build the hours estimate by phase and shop and the material estimate from the ones you tick,
write it out as CSV. The
weight test is its own prompt file (`GENAI-PROMPTS-estimator-tune.md`) and runs after Prompt 5 of this series.

## How to use

1. Start ONE new chat. Pick a model (the series is written for Gemini, GPT or Grok). Run the prompts in
   order in that same chat; each later prompt refers to the file written earlier in it.
2. Each answer ends with one code block. Copy that block into Notepad (or any plain text editor).
   Prompt 1 gives the whole file; Prompts 2, 3 and 4 each give one `<script>` block that you paste over
   the matching placeholder line in the file. Prompt 5 checks the assembled file. The tune series adds one
   more block over the MODULE T placeholder.
3. Save as `estimator.html` (plain text, UTF-8). Open it in the browser. Use the file picker on the page
   to choose your three exports (JCN history, tasks, material). Nothing leaves the computer: the page has no network access by design.
4. If something fails, press F12, copy the red error text from the Console tab, and use the Debug prompt
   at the end.

The prompts contain no record content. Your exports never go into the chat; they only go into the
browser page on your own computer. The abbreviation dictionary you build at work stays at work too.

---

## The contract (repeated inside every prompt so the pieces fit together)

Three CSV exports, identified by their columns, not their file names. After column mapping the page uses
these field names:

- `jcn_history`: jcn, job_summary, hull, ship_class, swlin, space, equipment_id, equipment_nomenclature,
  discrepancy (optional, free text), received_date
- `tasks`: one record per task. Required: job_summary, phase_no, shop, est_hours, charged_hours. Optional:
  phase_title, description (the phase's description block), task (the task text), task_no, crew_size (read, not
  used), performing (who did it, as typed), planned_start, planned_finish, actual_start, actual_finish. The
  phase-level fields (title, description, dates) repeat on every task of the phase; the first non-blank value per
  phase is used.
- `material`: job_summary, phase_no (the end-use phase), item, qty
- `phases` (optional fourth file, accepted when a pull gives the phase level separately): job_summary, phase_no,
  phase_title, description, planned_start, planned_finish, actual_start, actual_finish. Without it the phases are
  derived from the tasks.

One global object `DB`: `DB.jcns` (array of jcn_history rows), `DB.tasksByJS` (plain object, job_summary to array
of task rows in file order), `DB.phasesByJS` (plain object, job_summary to array of phase rows {phase_no,
phase_title, description, planned_start, planned_finish, actual_start, actual_finish} ordered by phase_no, derived
from the tasks unless a phases file was loaded; phase_title is never blank: "Phase 3" when the pull had none),
`DB.matByJS` (plain object, job_summary to array of material rows), `DB.jsCount` (plain object, job_summary to the
number of JCNs that share it, read as `DB.jsCount[job_summary]`), `DB.hulls` (an array of [hull, ship_class] pairs,
unique).

The unit of the estimate is the phase AND the shop (the owner's rule, 2026-10-25): a shop's charges land on its
tasks, and for estimating and comparing, a shop's tasks within a phase are summed. `EST.rows` is one row per phase
and shop of the newest similar job.

Globals declared with let in the skeleton: `DB`, `W` (weights), `DICT` (abbreviation dictionary, plain
object short to long), `FAMILY` (class families, an array of arrays of class codes), `ANALOGS`, `TICK`, `EST`,
`TUNE`. A let global is read by its name, never through
window.

`readNewJCN()` returns exactly {hull, cls, swlin, space, eid, nom, text}. `features(nj, j)` returns an object
with exactly these seventeen keys, each a number from 0 to 1: eqId, eqType, eqSys, hull, space, spaceDF,
spaceDeck, swlin, swlin5, swlin3, swlin2, swlin1, nom, textAction, textObject, family, hullNear. `scoreFrom(F, W, age)` turns a
feature object, a weight object and an age in years into a score. `findAnalogs(nj)` returns an array of exactly
{j, score, raw, reasons, note?} where j is a jcn_history row. Every function is a plain global function
declaration (no IIFE, no module, no `window.x =`); events are wired through arrow functions so a later script
block can replace a stub by declaring the same name again.

Functions: `parseCSV(text)`, `loadFiles(fileList)`, `buildDB(tables)`, `readNewJCN()`, `words(s)`,
`cleanCode(s)`, `features(nj, j)`, `scoreFrom(F, W, age)`, `maxScore(W)`, `scoreJCN(nj, j)`,
`findAnalogs(nj)`, `renderAnalogs()`, `renderWeights()`, `buildWeightsPanel()` (alias), `loadSavedWeights()`,
`buildEstimate()`, `estimateCSV()`, `run()`,
`setDownload()`, `tuneRun()`, `adoptWeights(newW)`, `tuneCSV()`, `setTuneDownload()`.
Helpers: `$(id)`, `esc(s)`, `toDate(s)`, `fmtDate(d)`, `num(s)`, `csvCell(v)`.

Element ids: `files`, `datastatus`, `mapping`, `f-hull`, `f-swlin`, `f-space`, `f-eid`, `f-nom`, `f-text`,
`btn-run`, `weights`, `dict`, `family`, `strength`, `analogs`, `estnotes`, `estimate`, `material`, `csvout`, `btn-copy`,
`btn-download`, `tune-n`, `tune-band`, `btn-tune`, `tune-status`, `tune-table`, `btn-adopt`, `tune-csv`,
`btn-tune-download`.

Weight keys (W), all editable on the page, defaults: eqId 40, eqType 20, eqSys 5, hull 5, space 5, spaceDF 3,
spaceDeck 1, swlin 10, swlin5 8, swlin3 6, swlin2 4, swlin1 2, nom 10, textAction 10, textObject 10, family 0,
hullNear 0, noEquip 1
(a factor from 0 to 1 applied when the equipment matches at no tier; 1 means no gate), recency 3 (years),
minSame 5 (same-class matches needed before other classes are shown).

---

## Prompt 1: the page skeleton

```
I am building a small offline tool for a ship repair planning department. It is ONE self-contained HTML
file that runs in a browser on a work computer with no network access, no installation and no libraries.
You will build it with me in steps. In this step, write only the skeleton: the page, its styling, shared
helper functions, and empty stub functions with exact names. Later steps fill the stubs in.

What the tool does: a planner loads three CSV exports from the maintenance system, types in a new job
(a JCN, job control number) including the discrepancy text as written, and the tool lists the ten most
similar past jobs with the reason each one matched and how strong the best match is. The planner ticks
the ones that are really the same kind of work, and the tool builds an estimate from them: the phases of
work and, within each phase, the hours by shop (each shop's tasks summed) as low-to-high ranges (both
what was estimated and what was actually charged), and the material by the phase that uses it. The estimate can be copied or downloaded as CSV. A last
section runs a weight test on the loaded history (a later step fills it in).

Hard rules for the file:
- Plain HTML, CSS and vanilla JavaScript only. No frameworks, no CDN links, no fonts from the web, no
  fetch or XMLHttpRequest, no eval.
- Put this in the head so the browser enforces it:
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline';
  style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action 'none'">
- Works in Edge and Chrome. Readable on a narrow window: sections stack in one column; tables scroll
  sideways inside their own container; a 16px side gutter; system font stack.
- Light and dark color schemes via prefers-color-scheme, using CSS variables for every color.
- No em dashes anywhere in text or comments.
- Reads files only through <input type="file" multiple>. Writes only through download links and
  textareas the user can copy from.
- Every function is a plain global function declaration at the top level of a script block. A later
  step replaces a stub by declaring a function of the same name in a later script block, so never wrap
  code in an IIFE or a module, and never assign functions to window.
- A global declared with let is read by its name (DB, W, EST), never as window.DB or window.EST.

The contract that every later step relies on (keep these names exactly):
- Three CSV exports, identified by their columns, not file names. After column mapping the page uses:
  jcn_history: jcn, job_summary, hull, ship_class, swlin, space, equipment_id, equipment_nomenclature,
  discrepancy (optional free text), received_date; tasks (one record per task of a phase): job_summary,
  phase_no, shop, est_hours, charged_hours, plus optional phase_title, description, task, task_no,
  crew_size, performing, planned_start, planned_finish, actual_start, actual_finish; material:
  job_summary, phase_no (end-use phase), item, qty. An optional fourth file, phases (job_summary,
  phase_no, phase_title, description and the four dates), may be loaded instead of repeating those
  fields on the tasks.
- One global object DB: DB.jcns (array of jcn_history rows), DB.tasksByJS (plain object, job_summary to
  array of task rows in file order), DB.phasesByJS (plain object, job_summary to array of phase rows
  {phase_no, phase_title, description, planned_start, planned_finish, actual_start, actual_finish},
  ordered by phase_no, derived from the tasks when no phases file is loaded), DB.matByJS (plain object,
  job_summary to array of material rows), DB.jsCount (plain object, job_summary to the number of JCNs
  sharing it, read as DB.jsCount[job_summary]), DB.hulls (an array of [hull, ship_class] pairs, unique).
- Global functions: parseCSV(text), loadFiles(fileList), buildDB(tables), readNewJCN(), words(s),
  cleanCode(s), features(nj, j), scoreFrom(F, W, age), maxScore(W), scoreJCN(nj, j), findAnalogs(nj),
  renderAnalogs(), renderWeights(), buildEstimate(), estimateCSV(), run(), tuneRun(), adoptWeights(newW),
  tuneCSV().
- readNewJCN() returns an object with exactly these keys: hull, cls, swlin, space, eid, nom, text.
- features(nj, j) returns an object with exactly these keys, each a number from 0 to 1: eqId, eqType,
  eqSys, hull, space, spaceDF, spaceDeck, swlin, swlin5, swlin3, swlin2, swlin1, nom, textAction,
  textObject, family, hullNear.
- findAnalogs(nj) returns an array of objects with exactly these keys: j (a jcn_history row), score,
  raw, reasons (array of strings).
- Element ids: files, datastatus, mapping, f-hull, f-swlin, f-space, f-eid, f-nom, f-text, btn-run,
  weights, dict, family, strength, analogs, estnotes, estimate, material, csvout, btn-copy, btn-download, tune-n,
  tune-band, btn-tune, tune-status, tune-table, btn-adopt, tune-csv, btn-tune-download.

Write the skeleton now:
1. The page with these sections in order, each with a short heading: "1. Load exports" (file input id
   files, a status line id datastatus, an empty div id mapping), "2. New JCN" (a select id f-hull, text
   inputs f-swlin, f-space, f-eid, f-nom with labels, a textarea id f-text labeled "Discrepancy text, as
   written on the JCN", and a button id btn-run "Find similar jobs", written with the disabled attribute
   because step 2 enables it once the exports are loaded), "3. Similar past jobs" (an empty
   div id weights, then a textarea id dict labeled "Abbreviations, one per line as short=long", then a
   textarea id family labeled "Class families, one per line, class codes separated by spaces", then an
   empty div id strength, then an empty table id analogs), "4. Estimate" (an empty div id estnotes, an
   empty table id estimate, then a sub-heading "Material by end-use phase" and an empty table id
   material), "5. Export" (a textarea id csvout, a button id btn-copy "Copy CSV", a link id btn-download
   "Download estimate.csv"), "6. Weight test" (one sentence saying the test hides each finished past job,
   estimates it from the others, and reports how far the estimates land from the charged hours under your
   weights and under weights the test tries; a number input id tune-n labeled "Jobs tested per half" with
   value 300; a number input id tune-band labeled "Exact band, percent" with value 20; a button id
   btn-tune "Run the weight test", written with the disabled attribute like btn-run; a status line id
   tune-status; an empty table id tune-table; a button id btn-adopt "Adopt suggested weights", also
   disabled; a textarea id tune-csv; a link id btn-tune-download
   "Download tune.csv"). Add one sentence under the title saying the page works offline and nothing
   leaves the computer.
2. Helper functions, fully written: $(id) returning the element; esc(s) for HTML escaping; toDate(s)
   that accepts YYYY-MM-DD, MM/DD/YYYY and DD-MON-YYYY and returns a Date or null; fmtDate(d) that
   returns YYYY-MM-DD built from the Date's local getFullYear, getMonth and getDate (never
   toISOString, which shifts the day in some time zones) or an empty string for null; num(s) that
   strips commas and returns a number or 0; csvCell(v) that quotes values containing commas, quotes or
   line breaks and prefixes a cell starting with = + - @ with an apostrophe unless it is a plain number.
3. The globals: let DB = null, let W = {} (weights, filled in step 3), let DICT = {} (abbreviations,
   filled in step 3), let FAMILY = [] (class families, filled in step 3), let ANALOGS = [], let TICK = new
   Set(), let EST = null, let TUNE = null.
4. Stubs for every contract function that is not a helper, each one line, for example
   function loadFiles(fileList) { /* step 2 */ }. features(nj, j) as a stub returns an object with the
   seventeen keys all 0. readNewJCN() as a stub returns the seven keys as empty strings.
5. Event wiring at the bottom, always through arrow functions that look the function up by name when
   the event fires, for example $('btn-run').addEventListener('click', () => run()), never
   addEventListener('click', run), because later steps replace the stubs. files change calls
   loadFiles(the file list); btn-run click calls run(); btn-copy copies csvout to the clipboard;
   btn-tune click calls tuneRun(); btn-adopt click calls adoptWeights(TUNE ? TUNE.suggested : null).
   Two global functions, fully written: setDownload() sets btn-download's href from csvout as a data:
   URL, and setTuneDownload() sets btn-tune-download's href from tune-csv the same way (later steps call
   them after filling the textareas).
6. Mark where later steps go with four placeholder lines inside the body, after the main script:
   <!-- MODULE 2: data loading -->, <!-- MODULE 3: matching -->, <!-- MODULE 4: estimate -->,
   <!-- MODULE T: tune -->.

Answer with the complete file in one code block and nothing after the block.
```

## Prompt 2: loading the exports and mapping columns

```
Continue the same file. Write MODULE 2: a single <script> block that I will paste over the line
<!-- MODULE 2: data loading -->. It replaces the stubs parseCSV, loadFiles and buildDB by declaring
plain global functions of the same names (no IIFE, no module, no assignment to window). Keep every name
in the contract from step 1 exactly.

Contract reminder: jcn_history: jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, discrepancy (optional), received_date; tasks: job_summary, phase_no, shop,
est_hours, charged_hours, and the optional phase_title, description, task, task_no, crew_size,
performing, planned_start, planned_finish, actual_start, actual_finish; material: job_summary,
phase_no, item, qty; phases (optional file): job_summary, phase_no, and the optional phase_title,
description, planned_start, planned_finish, actual_start, actual_finish. DB.jcns (array), DB.tasksByJS
(plain object), DB.phasesByJS (plain object), DB.matByJS (plain object), DB.jsCount (plain object,
DB.jsCount[job_summary] = count), DB.hulls (array of [hull, ship_class] pairs). Elements: files,
datastatus, mapping, f-hull.

How the history is shaped (so the loader fits it): a job summary holds phases; each phase has one or
more tasks, one record each, naming the shop, what that shop does, its crew and its estimated hours,
and the shop's charges land on its task; a shop is usually tasked once in a phase but can be tasked
twice. The pull is one flat task table in which the phase-level fields (title, description block,
planned and actual dates) repeat on every task of the phase. A separate phases file may exist but
usually does not.

Names the later series rely on (declare exactly these): the alias table is const SCHEMA (one entry per
table, each a plain object of field name to alias list, aliases written without spaces); the raw parsed
files live in let RAW_DATA; the chosen column mappings in let MAPPINGS; cleanCol(s) lower-cases a header
and strips everything but letters and digits; detectType(headers) returns "jcn_history", "tasks", "phases",
"material" or null for a header row; updateStatus() rewrites datastatus; OPTIONAL_FIELDS is a const array
of the optional field names (discrepancy, phase_title, description, task, task_no, crew_size, performing,
planned_start, planned_finish, actual_start, actual_finish), which later modules extend in place with push;
MODULE 2 checks that list by field name across every table, so only names that are optional wherever they
appear belong on it.

Requirements:
1. parseCSV(text): a real CSV parser, not split on commas: handles quoted fields, doubled quotes inside
   quotes, line breaks inside quotes, CRLF, and a leading byte-order mark. Returns an array of objects
   keyed by the header row, with header names trimmed.
2. loadFiles(fileList): reads each chosen file with FileReader as UTF-8, parses it, and decides which
   export it is from its columns: a file is jcn_history if it has a jcn column and an equipment column;
   tasks if it has a job summary column, a shop column and an estimated or charged hours column; material
   if it has an item, part, NIIN, NSN or stock number column and a quantity column; phases if it has a job
   summary column and a phase title or phase number column and NO shop, hours, item or quantity column.
   Test the four kinds in this order: jcn_history, tasks, material, phases, because a material file also
   has a job summary and a phase number column.
   Matching is case-insensitive, ignores spaces, underscores and punctuation, and accepts these aliases
   for each field (extend them sensibly): jcn: jcn, job control number; job_summary: job summary, js, job
   summary number; hull: hull, ship, ship name, hull number; ship_class: class, ship class; swlin: swlin,
   swlin number, swlin line item, eswbs; space: space, compartment, space number, location; equipment_id:
   equipment id, equipment, eqpt, eid, component; equipment_nomenclature: nomenclature, equipment
   nomenclature, noun name, equipment noun; discrepancy: discrepancy, discrepancy text, narrative, problem,
   problem description, deficiency, remarks, csmp narrative, description; received_date: received,
   received date, date received, jcn date; phase_no: phase, phase no, phase number, key op, keyop, key
   event; phase_title: phase title, title, phase name; description: description, description block, phase
   description, procedure, work description; task: task, task title, task description, task name, task
   text; task_no: task no, task number, task seq, seq, line; shop: shop, trade, work center, shop code;
   crew_size: crew, crew size, people, headcount; est_hours: estimated hours, est hours, planned hours,
   estimate, man hours, mh; charged_hours: charged hours, actual hours, charged, expended hours, actuals;
   performing: performing, performing activity, activity, performer, work by, in house, farm out,
   contractor, org, organic; planned_start: planned start, plan start, sched start, scheduled start;
   planned_finish: planned finish, plan finish, sched finish, scheduled finish; actual_start: actual
   start, act start, start date; actual_finish: actual finish, act finish, finish date, completed; item:
   item, part, material, nsn, niin, stock number, part number; qty: qty, quantity. The alias "description"
   belongs to discrepancy in the jcn_history table and to description in the tasks and phases tables
   (SCHEMA is per table, so both are fine).
3. Optional fields: when no column matches one, every row gets "" (or null for a date) and no mapping
   row is drawn for it. For any REQUIRED field that no column matches, do not fail: draw a small mapping
   row in div mapping with the file name, the field name, and a <select> of that file's columns; when
   the user picks one, use it and rebuild. Also list in datastatus which of the exports are loaded and
   how many rows each has (for tasks also how many phases and job summaries they hold, once buildDB has
   run), whether the history has discrepancy text, whether a phases file was given or the phases were
   derived, and name any required export still missing (jcn_history, tasks, material).
4. buildDB(tables): takes {jcn_history, tasks, material, phases (may be absent)} as arrays of mapped rows
   and builds DB. DB is null until then, so its first line is DB = {jcns: [], tasksByJS: {}, phasesByJS:
   {}, matByJS: {}, jsCount: {}, hulls: []}, assigned by name (never window.DB). Normalize: trim strings;
   uppercase jcn, job_summary, hull, swlin, space, equipment_id, shop; keep discrepancy,
   equipment_nomenclature, phase_title, description, task and performing as typed (trimmed only);
   phase_no, task_no, crew_size, hours and qty through num(); received_date and the four task dates
   through toDate() kept as Dates (null if unreadable). DB.tasksByJS[job_summary] is that summary's task
   rows in file order. DB.phasesByJS[job_summary]: when a phases file was loaded, one row per
   job_summary and phase_no from it (the first row wins on a repeat), then any phase_no present in the
   summary's tasks but missing from the file is added from the tasks; without a phases file, every
   phase is derived from the tasks: for each distinct phase_no (compared as numbers) of the summary, in
   ascending order, phase_title = the first non-blank phase_title among its task rows, description the
   first non-blank description, each of the four dates the first non-null; a blank phase_title becomes
   "Phase " + phase_no. DB.jsCount counts jcn rows per job_summary. DB.hulls is unique [hull,
   ship_class] sorted by hull. Then fill the f-hull select with one option per hull showing "hull
   (class)".
5. When jcn_history, tasks and material are loaded and mapped (phases is optional), call buildDB, then
   enable btn-run and btn-tune. Before that, both are disabled.
6. No em dashes. No network access.

Answer with the one <script> block only, starting with <script> and ending with </script>, and nothing
after it.
```

## Prompt 3: finding similar past jobs

```
Continue the same file. Write MODULE 3: a single <script> block that I will paste over the line
<!-- MODULE 3: matching -->. It replaces the stubs readNewJCN, words, cleanCode, features, scoreFrom,
maxScore, scoreJCN, findAnalogs, renderAnalogs, renderWeights and run by declaring plain global
functions of the same names (no IIFE, no module, no assignment to window), adds two more plain global
functions, loadSavedWeights and buildWeightsPanel, and fills the globals W, DICT and FAMILY. Keep every contract name exactly.

Contract reminder: DB.jcns rows have jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, discrepancy (a string, possibly empty), received_date (a Date or null). DB.hulls
is an ARRAY of [hull, ship_class] pairs: to find the class of a hull, find the pair whose first element
equals the hull and take its second element. DB.jsCount is a PLAIN OBJECT, read as
DB.jsCount[job_summary] (not a Map, so never .get()). Globals W, DICT, ANALOGS, TICK, declared with let
in the skeleton and read by name, never through window (FAMILY too). TICK is a Set of jcn strings (the skeleton
declares let TICK = new Set()): test it with TICK.has(jcn), change it with TICK.add(jcn) and
TICK.delete(jcn), and reset it with TICK = new Set([...]); never treat it as an array. Elements: f-hull,
f-swlin, f-space, f-eid, f-nom, f-text, weights, dict, family, strength, analogs. Helpers $(id), esc(s),
fmtDate(d), num(s).
readNewJCN() returns an object with exactly these keys: hull, cls, swlin, space, eid, nom, text.
features(nj, j) returns an object with exactly these seventeen keys, each a number from 0 to 1: eqId,
eqType, eqSys, hull, space, spaceDF, spaceDeck, swlin, swlin5, swlin3, swlin2, swlin1, nom, textAction,
textObject, family, hullNear.
findAnalogs(nj) returns an array of objects with exactly these keys: j (the jcn_history row), score,
raw, reasons (array of strings), and optionally note (a string, for rows from another class).

The weights. Declare const DEFAULT_W with exactly these keys and values: eqId 40, eqType 20, eqSys 5,
hull 5, space 5, spaceDF 3, spaceDeck 1, swlin 10, swlin5 8, swlin3 6, swlin2 4, swlin1 2, nom 10,
textAction 10, textObject 10, family 0, hullNear 0, noEquip 1, recency 3, minSame 5. The first seventeen
are points, one per feature key with the same name. noEquip is a factor from 0 to 1. recency is years. minSame is a count.

Also declare const W_LABELS: the plain label for every key of DEFAULT_W (for example eqId "Same
equipment ID", swlin3 "SWLIN shares 3 characters", noEquip "No equipment match factor (1 = off)",
family "Same class family (orders the other-class rows)", hullNear "Hull nearness within the class",
recency "Recency scale, years (0 = off)", minSame "Same-class matches needed before other classes are
shown"); the weights panel and a later module both read it.

The class families. The textarea family holds one family per line, class codes separated by spaces or
commas (for example "DDG CG"). Parse it into FAMILY on every change: an array of arrays of uppercased,
trimmed codes, blank lines ignored; remember the text in localStorage under "estimator.family"
(try/catch) and load it when the module runs; a change re-runs run(). Two classes are in the same
family when one line holds both. hullNumber(h): the number made of the digits at the end of the hull
string (after the last character that is not a digit), or null when the string ends in no digit.
classSpan(cls): the largest minus the smallest hullNumber over the DB.hulls pairs of that class whose
number is not null, at least 1; computed on demand and cached in a plain object keyed by class, and the
cache is cleared at the start of run().

Text helpers:
1. cleanCode(s): uppercase, then remove every character that is not a letter or a digit. Used for the
   SWLIN and the equipment ID comparisons.
2. words(s): an empty, null or undefined input returns an empty array (a job with no discrepancy text
   scores 0 on the text features, never an error). The result for a given input string is cached in a
   plain object declared at the top of the module (the cache is cleared whenever DICT changes), because
   the same strings are looked at many thousands of times. The rule: lowercase; split into tokens on every character that is not a
   letter, a digit or a slash;
   drop empty tokens; then for each token, if DICT has that token as a key, replace it by the words of
   DICT[token] (split on spaces); then drop these stop words: the, a, an, of, to, and, or, is, are, was,
   were, be, been, in, on, at, for, with, by, it, its, this, that, these, those, as, from, request,
   requested, req, please, properly, ships, ship's, force, sf, unable, able, not, no, does, do, did,
   during, found, per, iaw. Never drop the word depot (it names the level of repair). Return the array
   of distinct words in order of first appearance.
3. Declare const ACTIONS as an array of word families, each family an array of words that mean the same
   kind of work: ["replace","renew","install","replacement","renewal"], ["overhaul","rebuild","repair",
   "refurbish"], ["inspect","test","troubleshoot","calibrate","check","verify","inspection"],
   ["clean","adjust","lubricate","tighten"], ["remove","removal"]. A word is an action word when it is
   in any family.

How matching works (this is the planner's judgment, written as rules):
4. Ship class is a FILTER, not points. Only past jobs on the same class as the chosen hull are
   candidates. Other classes are shown only when the same class has fewer than W.minSame candidates with
   a score above zero, and each such row gets note = "Other class (X): shown because <class> has only N".
5. features(nj, j) computes the seventeen features. Tiers inside a group are exclusive: at most one of
   the group's keys is above 0.
   - Equipment: eqId = 1 when cleanCode(nj.eid) is not empty and equals cleanCode(j.equipment_id); else
     eqType = 1 when the type of both is the same and not empty, where the type is the text before the
     first hyphen of the equipment id, uppercased; else eqSys = 1 when the first character of
     cleanCode(nj.swlin) equals the first character of cleanCode(j.swlin) and both are not empty.
   - hull = 1 when j.hull equals nj.hull.
   - Space, only when j.ship_class equals nj.cls and both space numbers are non-empty (for a row of
     another class, or when either space is blank, all three are 0): space = 1 when the space numbers are
     equal; else spaceDF = 1 when the first two hyphen-separated parts are equal; else spaceDeck = 1 when
     the first part is equal.
   - SWLIN: let a = cleanCode(nj.swlin), b = cleanCode(j.swlin), both not empty. swlin = 1 when a equals
     b, or when one is a prefix of the other and the shorter has at least three characters (a SWLIN cut
     down to its first characters counts as a full match at the length given). Otherwise let p = the
     number of leading characters a and b share: swlin5 = 1 when p is at least 5; else swlin3 = 1 when p
     is at least 3; else swlin2 = 1 when p is at least 2; else swlin1 = 1 when p is at least 1.
   - nom = the Jaccard overlap of words(nj.nom) and words(j.equipment_nomenclature): shared words
     divided by distinct words in either, when both lists are non-empty; else 0.
   - Text: let A = words(nj.text) and B = words(j.discrepancy). actA = the action words in A, actB =
     the action words in B, objA = the other words in A, objB = the other words in B. textAction = 1
     when actA and actB share a word; else 0.6 when a word in actA and a word in actB are in the same
     family; else 0. textObject = the Jaccard overlap of objA and objB when both are non-empty; else 0.
   - family = 1 when j.ship_class differs from nj.cls and one FAMILY line holds both codes; else 0 (so it
     only ever adds points to a row of another class, which orders the fallback rows).
   - hullNear, only when j.ship_class equals nj.cls and both hullNumber(nj.hull) and hullNumber(j.hull)
     are not null: 1 - |a - b| / classSpan(nj.cls), not below 0; else 0.
6. scoreFrom(F, W, age): pts = the sum over the seventeen feature keys of W[key] times F[key]; rec = 1
   when W.recency is 0 or below (no recency factor), else 0.5 + 0.5 * exp(-age / W.recency); gate = 1
   when F.eqId + F.eqType + F.eqSys is above 0, else W.noEquip; return pts * rec * gate.
7. maxScore(W) = the highest of W.eqId, W.eqType and W.eqSys, plus W.hull, plus the highest of W.space,
   W.spaceDF and W.spaceDeck, plus the highest of W.swlin, W.swlin5, W.swlin3, W.swlin2 and W.swlin1, plus
   W.nom, W.textAction, W.textObject and W.hullNear (each group's highest weight, so the strength line
   cannot pass 100 percent whatever the weights become; recency 1 and no gate; hullNear counts because a
   same-class row can score it; family is left out because a row of the new JCN's own class never scores
   it, and the strength line describes the same-class best case).
8. scoreJCN(nj, j): F = features(nj, j); age in years from j.received_date to today, 10 when the date is
   null; score = scoreFrom(F, W, age); raw = the sum of W[key] times F[key] over the seventeen keys (points
   before recency and gate). reasons: one short plain-English string per feature above 0, such as "Same
   equipment ID", "Same equipment type (FMV)", "Same system (5)", "Same hull", "Same space", "Same deck
   and frame", "Same deck", "Same SWLIN", "SWLIN shares 5 characters (52114)", "SWLIN shares 3 characters
   (521)", "SWLIN shares 2 characters", "SWLIN shares 1 character", "Nomenclature shares: fire main
   valve" (the shared words), "Same action (replace)" or "Related action (overhaul, repair)", "Text
   shares: valve, seat" (the shared object words), "Same class family", "Hull nearness 0.93" (two
   decimals); then "No equipment match: score x 0.5" when the gate
   applied and W.noEquip is below 1; then "2.3 years ago". Do not include a reason for things that did
   not match. Return {score, raw, reasons, F}.
9. findAnalogs(nj) scores every DB.jcns row, drops raw == 0, applies the class filter and fallback above,
   and returns the top ten by score as {j, score, raw, reasons, note}.
10. readNewJCN() reads the form into {hull, cls, swlin, space, eid, nom, text}: hull from f-hull and cls
    looked up in DB.hulls as described; swlin, space, eid and nom trimmed and uppercased; text trimmed
    and otherwise as typed.
11. renderAnalogs() first fills div strength: when ANALOGS is empty, "No similar job found"; otherwise
    "Match strength: P% of the attainable score: strong" where P = round(100 * ANALOGS[0].score /
    maxScore(W)) and the word is strong when P is at least 60, medium when P is at least 30, else weak.
    Then it draws the rows into table analogs (set the table's innerHTML to a thead and a tbody; never
    put a second table inside it) with columns: Use (a checkbox, checked when TICK.has(the row's jcn);
    ticking adds the jcn to TICK, unticking deletes it, and either calls buildEstimate()), JCN, Hull and
    class, Received
    (fmtDate), Score (one decimal), Equipment (id and nomenclature), Space, SWLIN, Why it matched (the
    reasons joined with "; "), and Job summary (with "covers N JCNs" when DB.jsCount[job_summary] is
    above 1, and the note when present). Rows with a note get a muted style.
12. loadSavedWeights(): reads localStorage "estimator.weights" (try/catch) and copies into W only the
    saved keys that DEFAULT_W has at the time of the call, so a saved set from an older version can
    neither drop a key nor add one; a later module that adds keys to DEFAULT_W and W calls it again, so
    the saved values of its keys survive a reload. When the module runs: W = a copy of DEFAULT_W, then
    loadSavedWeights(). buildWeightsPanel() is a one-line alias that calls renderWeights() (an older
    series calls it by that name). renderWeights() draws the weights div: one small number input per W
    key with its plain label from W_LABELS, step 0.1 for noEquip and step 1 for the rest, plus a "Reset
    weights" button that restores DEFAULT_W, the default dictionary and an empty family box. Changing
    any value updates W, saves W to localStorage "estimator.weights" (try/catch) and re-runs run(). The
    dictionary: when the textarea dict is empty, fill it with these default lines: fmv=fire main valve,
    o/h=overhaul, repl=replace, insp=inspect, inop=inoperable, stk=stuck, lks=leaks, pmp=pump, vlv=valve,
    mtr=motor, sw=seawater, fw=freshwater, hyd=hydraulic, elec=electrical, xfer=transfer. Parse the
    textarea into DICT on every change: one entry per line, split at the first "=", key lowercased and
    trimmed, value lowercased and trimmed, lines without "=" ignored. Remember the text in localStorage
    under "estimator.dict" (try/catch) and load it when the module runs. Call renderWeights() directly at
    the end of the module (the elements already exist because the script is at the end of the body); do
    not use a DOMContentLoaded listener.
13. run() = readNewJCN, findAnalogs into ANALOGS, then TICK = new Set of the jcn values of the top
    five, renderAnalogs, buildEstimate.
14. No em dashes.

Answer with the one <script> block only, and nothing after it.
```

## Prompt 4: the estimate and the CSV

Rewritten for v0.7: the unit of the estimate is the phase and the shop, read from the task records, and the
row shape the batch series reads gains `tasks`.

```
Continue the same file. Write MODULE 4: a single <script> block that I will paste over the line
<!-- MODULE 4: estimate -->. It replaces the stubs buildEstimate and estimateCSV by declaring plain
global functions of the same names (no IIFE, no module, no assignment to window). Keep every contract
name exactly.

Contract reminder: ANALOGS is the array returned by findAnalogs, each element {j, score, raw, reasons}
where j is a jcn_history row with jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, received_date (a Date or null). An analog's JCN is a.j.jcn, its summary
a.j.job_summary and its date a.j.received_date (the row sits under j; a.jcn is undefined). TICK is the
Set of ticked jcn values. DB.tasksByJS[job_summary] is an array of task rows in file order: {phase_no, phase_title, description,
task_no, task, shop, crew_size, est_hours, charged_hours, performing, planned_start, planned_finish,
actual_start, actual_finish} (numbers through num, dates as Date or null, text as typed). A phase is
worked by one or more shops, and a shop is usually tasked once in a phase but can be tasked twice.
DB.phasesByJS[job_summary] is the array of that summary's phases {phase_no, phase_title, description,
planned_start, planned_finish, actual_start, actual_finish}, ordered by phase_no, built by MODULE 2
(phase_title is never blank there: "Phase 3" when the pull had none). DB.matByJS[job_summary] is an
array of material rows (phase_no, item, qty). DB.jsCount[job_summary] (a plain object, not a Map) is
how many JCNs share that summary. readNewJCN() returns {hull, cls, swlin, space, eid, nom, text}.
Elements: estnotes, estimate, material, csvout. Helpers esc, csvCell, fmtDate, setDownload. Global EST,
declared with let in the skeleton: read it as EST, never as window.EST (that is undefined, because a
let global is not a window property).

The unit of the estimate is the phase AND the shop. The rule from the owner of the data: a shop's
charges land on its tasks, and for estimating and comparing, a shop's tasks within a phase are summed
(a second task of the same shop in a phase is simply added in). Crew size is not used.

Write two small plain global helpers first: phaseKey(title) = the title trimmed and uppercased (phases
are matched across summaries by title); shopHours(js, title, shop) = over DB.tasksByJS[js], the rows
whose phaseKey(phase_title) equals phaseKey(title) and whose shop equals shop: null when there is no
such row, else {est: the sum of their est_hours, charged: the sum of their charged_hours, tasks: their
distinct non-blank task texts in file order}.

How the estimate is built:
1. Take the ticked analogs that have task data (DB.tasksByJS[job_summary] exists and is non-empty).
   Use each job_summary once even if two ticked JCNs share it. If none, write a note in estnotes asking
   the user to tick at least one job with task data, clear the tables and csvout, call setDownload(),
   and return.
2. Sort the used job summaries newest first by received_date. The breakdown comes from the NEWEST one:
   its phases in DB.phasesByJS order, and under each phase its shops in order of first appearance among
   that phase's task rows (the task rows whose phaseKey(phase_title) equals the phase's). One estimate
   row per phase and shop. Note in estnotes which JCN the breakdown came from, its date (fmtDate), how
   many phases and how many rows it has, and how many job summaries are behind the numbers.
3. Method change check: for each other used summary, compare its set of phaseKey titles (from
   DB.phasesByJS) with the newest one's; if fewer than 80% of the combined titles are shared, add a
   visible note "Possible method change" naming that JCN, its date and its phase count, and saying to
   check how the work is done today before trusting older hours.
4. If fewer than three summaries are used, add a note that the ranges are a starting point for the
   planner, not a forecast.
5. For each row (phase title, shop) of the newest breakdown: for every used summary js, h =
   shopHours(js, title, shop); when h is not null, collect h.est / DB.jsCount[js] and h.charged /
   DB.jsCount[js] (a summary that covered several JCNs is shared out) and count that summary in k. A
   summary that has the phase but not that shop on it is left out of the row (never counted as zero).
   est_low and est_high are the smallest and largest collected est, charged_low and charged_high the
   same for charged. The table estimate has the columns Phase (number and title), Shop, Tasks (newest
   job), Estimated hours, Charged hours, Summaries; show the hours as "a to b" (one decimal), the tasks
   as shopHours(newest, title, shop).tasks joined with "; ", and "k of n" for how many used summaries had
   that phase and shop (k is at least 1, because the newest summary has it). Set the innerHTML of table
   estimate (and of table material in step 7) to a thead and a tbody; never put a second table inside
   them. Reach every element through $(id), never through a bare element id used as a global.
6. Totals: sum the low and high of est and of charged across rows, state both ranges in estnotes, and
   if charged ran higher than estimated say by about what percent, and end with "Plan to the charged
   range." Under the notes add one <details> element titled "What the newest job's phases say" listing,
   for each phase of the newest breakdown whose description is non-blank, the phase title and its
   description block, so the planner can read what the hours were for.
7. Material: for every used summary, map each material row's phase_no to that summary's phase title
   (through DB.phasesByJS[js]; a phase_no with no phase row gets the title "Phase " + phase_no), then
   group by phaseKey and item. Quantities are taken as they are: NEVER divide a quantity by DB.jsCount.
   Hours are shared out over a grouped summary's JCNs (step 5); material is not, because a summary that
   covered four JCNs gives the new job its whole list and the planner trims it. Show a table with five
   columns: end-use phase, item, qty as low to high (the smallest and largest qty seen for that item
   across the used summaries, as "a to b"), "seen on k of n", and grouped = the largest
   DB.jsCount[job_summary] among the used summaries that carried that item (1 when none of them was
   grouped). When any used summary has DB.jsCount above 1, add a note in estnotes: "Material from a
   summary that covered N JCNs is listed whole; it may include sibling jobs' parts." (N = the largest
   count). Items whose phase title is not in the newest breakdown are listed last and marked "older
   breakdown only".
8. Set EST = {nj: readNewJCN(), rows, used, usedJcns, notes} with exactly these shapes, because the
   batch series reads them by name: rows is the array of estimate rows in the newest breakdown's order,
   each exactly {phase_no, phase_title, shop, tasks, est_low, est_high, charged_low, charged_high, k, n}
   (phase_no, the four hours, k and n as numbers; phase_title, shop and tasks as strings, tasks being the
   newest summary's task texts for that phase and shop joined with "; ", "" when blank; k = how many
   used summaries had the phase and shop, n = how many summaries were used); used is the number of job
   summaries used; usedJcns is one string of the ticked JCNs whose summaries were used, joined by single
   spaces, newest first; notes is the array of the sentences written to estnotes (a later module looks
   there for "Possible method change"). Then set $('csvout').value = estimateCSV() (the textarea's
   value) and call setDownload().
9. estimateCSV(): header new_equipment_id, new_space, new_swlin, new_hull, phase_no, phase_title, shop,
   est_hours_low, est_hours_high, charged_hours_low, charged_hours_high, summaries_with_phase,
   summaries_used, analog_jcns, tasks; one line per estimate row (phase and shop); CRLF line ends; every
   cell through csvCell; the new job's values come from EST.nj.eid, EST.nj.space, EST.nj.swlin,
   EST.nj.hull.
10. No em dashes. Tables are plain HTML with a header row; numbers right-aligned.

Answer with the one <script> block only, and nothing after it.
```

## Prompt 5: check the assembled file

```
I have assembled the file from your four answers. Without rewriting it, check it for the mistakes that
usually break a file built in pieces, and list each one with the exact fix:
1. Every function called anywhere but not defined, and every function defined twice (a stub left in
   place next to the real one is fine only if the real one comes later in the file).
2. Every element id used in JavaScript that does not exist in the HTML, and the reverse.
3. Values used across modules under different shapes: DB.jsCount read with .get() although it is a
   plain object; analogs read as a.jcn in one place and a.j.jcn in another; the new JCN read as
   equipment_id in one place and eid in another; a global declared with let read through window
   (window.EST is undefined).
4. Any <script> block left unclosed, any placeholder comment left in, and any character outside plain
   ASCII inside the JavaScript that could be a smart quote.
5. Anything that would be blocked by the Content-Security-Policy in the head.
5a. A const or let read before the line that declares it (for example a date-format branch that reads
   the match of a later pattern), and a helper that works for one date format but throws for another:
   call toDate on "2024-05-04", "05/04/2024" and "04-MAY-2024" in your head and confirm all three return
   the same day.
6. Any material quantity divided by DB.jsCount. Hours are shared out over a grouped summary's JCNs;
   material is listed whole, and the grouped column says how many JCNs the summary covered.
7. The seventeen feature keys returned by features() are exactly the seventeen point keys of DEFAULT_W,
   and scoreFrom() sums over those seventeen only (never noEquip, recency or minSame as points).
7a. family is 0 for a row of the new JCN's own class and when the family box is empty; hullNear is 0 for
   a row of another class and when either hull ends in no digit.
7b. buildWeightsPanel() exists as an alias of renderWeights(); loadSavedWeights() merges only keys that
   DEFAULT_W has; W.recency of 0 gives a recency factor of 1, not NaN; maxScore() takes each group's
   highest weight and counts W.hullNear, so no same-class analog can show a strength above 100 percent
   even after the weight test raises hullNear.
8. The three space features are 0 for a row whose ship_class differs from the new JCN's class.
9. A history without a discrepancy column still loads, with discrepancy = "" on every row, and the text
   features are then 0 rather than an error.
10. The unit of the estimate is the phase and the shop: shopHours sums a shop's tasks within a phase; a
   phase worked by three shops gives three estimate rows with their own hours, never the first shop's
   hours repeated; a used summary that has the phase but not the shop is left out of that row's range,
   not counted as zero; EST.rows carries tasks as a string.
11. buildDB derives DB.phasesByJS from the tasks when no phases file is loaded (one row per distinct
   phase_no, ascending, "Phase N" for a blank title, the first non-blank description and dates), a tasks
   file is recognized by its job summary, shop and hours columns, and the status line reports the tasks
   with their phase and job summary counts.
Then give me a short test checklist: five things to do in the opened page, in order, and what I should
see after each.
```

## Debug prompt (use as many times as needed)

```
I opened the assembled file and did this: <what you clicked>. The browser console (F12) shows this error:

<paste the red text here, exactly>

Find the cause in the file you wrote and answer with only the corrected function or block, named so I
can paste it over the old one. Do not change anything else.
```

## Column-name prompt (optional, for the real exports)

```
My three exports have these header rows (names only, no data):
jcn_history: <paste the header row>
tasks: <paste the header row>
material: <paste the header row>
Update the alias lists in loadFiles so each of these headers maps to the right contract field, and tell
me which contract fields, if any, have no matching column so I know what to add in the export. The
discrepancy field and the task table's phase title, description, task, task number, crew size,
performing and date fields are optional; say which were found.
```

## Test checklist (what the test here saw, for comparison)

1. Open the file: six numbered sections, "Find similar jobs" and "Run the weight test" greyed out.
2. Choose the three exports: the status line names all three with their row counts (the tasks with their
   phase and job summary counts, and whether the phases were derived) and says whether the history has
   discrepancy text; no mapping rows if the columns matched; both buttons turn on.
3. Pick a hull, type an equipment ID, space, SWLIN and a line of discrepancy text, click: the strength
   line, then ten rows, the exact-match job first, each with its reasons (including the shared words)
   and a tick box.
4. Untick a row: the estimate recomputes; the note says which JCN the breakdown came from; a phase worked
   by several shops shows one row per shop with different hours.
5. The CSV box fills with one line per phase and shop; Download saves estimate.csv.

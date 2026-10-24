# Build guide: the estimator and the Resource Map, from prompts, inside GenAI.mil

Version 0.3, 2026-10-24 (v0.1 and v0.2 kept beside it). v0.3: the estimator series v0.4 reads the discrepancy text and
scores the SWLIN by shared code depth, and the new weight test (GENAI-PROMPTS-estimator-tune.md) runs after Prompt 5. v0.2
(2026-10-23): the lookup column is map_name, and the leveler series is named in full where "B2" could have meant
Prompt B2 of series B (review of PR 60). This is the one page to read before building. It says what the two tools are, what files
they need, which prompt file to run in which order, how to paste the answers, how to test with made-up data, and
what to do when something breaks. Every prompt series it names has been tested here against Gemini with no code
execution and a headless browser, on made-up data only; the test records sit beside the prompt files in the
private source. Nothing in this guide or in the prompts needs a real value, and no real record should ever be pasted
into a chat: the prompts describe structure, and the tools read the real files on the work computer, offline.

## The system in one picture

```
the reporting tool pulls (workbooks or CSV)                      Workforce map workbook          
  JCN history, phases, material (history)            assigned hours by project, shop, week
  work package (future JCNs)                         shop capacity by week, the contractor as a line
  planning status (planned job summaries)                        |
  project list (start, end)                                      | Prompt A describes its layout (no content)
        |                                                        v
        v                                              Resource Map (one HTML file)
  Estimator (one HTML file)  ---consumption.csv-------->   import, store, shop by week, drill-down,
  score each future JCN against the past,                  verdicts, export (series B)
  planned jobs pass through, material list                 + the leveler: moves on top of the dates of
        |                                                    record, contractor line, lookup, zoom,
        +---material_estimate.csv (for planners)             snapshot, automatic level and farm out
                                                             (series B2), the look (Prompt S)
                                                                 |
                                                                 v
                                                  moves list, farm-out list, snapshot for the TVs,
                                                  shop_week_summary.csv for Excel pivots
```

Both tools are single HTML files that run in Edge or Chrome on the work computer with no installation, no network
and no library. The browser's own database keeps what was imported, so an import happens once. CSV files carry
data between the tools and into Excel.

## Before you start: the files

Field names stay generic here. The reader prompts (Prompt A for the workbooks, the column-name prompt in the
estimator series for the history exports) learn the real names, and the tools match columns by name with case,
spaces and punctuation ignored, so "Job Summary", "job_summary" and "JOBSUMMARY" are the same column.

| File | One row is | Columns the tools look for | Where it comes from |
|---|---|---|---|
| JCN history | a JCN | jcn, job_summary, project, hull, ship_class, swlin, space, equipment_id, equipment_nomenclature, discrepancy (the free text as written, optional), received_date | the reporting tool pull |
| Phases | a phase of a job summary | job_summary, phase_no, phase_title, shop, est_hours, charged_hours, planned_start, planned_finish, actual_start, actual_finish, performing (organic shop or contractor) | the reporting tool pull |
| Material | an order line of a phase (once per phase of a job summary, never repeated per JCN) | job_summary, phase_no, stock_number (NIIN or NSN), nomenclature, qty | the reporting tool pull |
| Work package | a future JCN | proposed_id (the JCN), hull, project, swlin, space, equipment_id, nomenclature, planned_start, job_summary, performing (the screening mark, when the pull comes from the JCN database) | the reporting tool or the JCN database |
| Planning status | a planned phase | job_summary, phase_no, phase_title, shop, planned_hours or planned_mandays, scheduled_start, scheduled_finish, performing | the reporting tool pull |
| Project list | a project | project, hull, start, end | the reporting tool pull, or the workforce map if Prompt A finds the dates there |
| Workforce map | its own layout | described by Prompt A, never retyped | the planning department's workbook |
| Lookup | a project on the workforce map | map_name, project, hull | Prompt L drafts it, you confirm each row |
| Contractor capacity | a week of the contractor's line | shop (the line's code, for example CTR), week_start, capacity_hours | the workforce map, or this small file when the map carries no such row |

Dates are read as YYYY-MM-DD, MM/DD/YYYY, DD-MON-YYYY or an Excel serial. Weeks are keyed by their Monday. Hours
are decimals. Workbooks (.xlsx) can be chosen directly once Prompts X are in a tool; otherwise save each sheet as
CSV (File, Save As, CSV UTF-8).

## The order of the prompt files

**Tool 1, the estimator** (one chat):

1. `GENAI-PROMPTS-estimator.md`: Prompts 1 to 5. The page, the history import with column mapping, the matching of a
   new JCN against the past (equipment, hull, space, the SWLIN by how much of its code is shared, the nomenclature
   and the discrepancy text by shared words after an abbreviation dictionary you keep on the page), the match
   strength, the estimate and its CSV, the check prompt. Then the optional column-name prompt when the real export
   names differ.
2. `GENAI-PROMPTS-estimator-tune.md`: Prompts T and T2, the weight test. It fills section 6 of the same page: every
   finished past job is hidden, estimated from the others and compared with its charged hours, under your weights
   and under weights the test fits on one half of the history and judges on the other. Runs after Prompt 5 and
   before the batch series, which keeps it.
3. `GENAI-PROMPTS-estimator-batch.md`: Prompts C1, C2, C2b. The whole work package at once, streamed import of big
   history files, the local store, placement of each phase in the project's weeks, one consumption CSV out.
4. `GENAI-PROMPTS-estimator-planned.md`: Prompts D1, D2, D3. Planned job summaries pass through with the planner's
   numbers, the contractor mark on every line, the material list per phase (material_estimate.csv). D runs after
   C2b and BEFORE Prompts X.
5. `GENAI-PROMPTS-xlsx.md`: Prompts X and X2, optional, to choose workbooks instead of CSVs. If X was run before D,
   run X2 again after D.
6. `GENAI-PROMPTS-style.md`: Prompt S, the estimator variant, last.

**Tool 2, the Resource Map** (one chat):

1. `GENAI-PROMPTS-resource-map-analysis.md`: Prompt A, with the workforce map workbook attached. It answers with a
   structure-only description (the "data sheet spec"). Read it, strike any value that looks real, add the week rule
   if the spec left it open (which Monday "WK01" is), and keep it: B1 and B2 paste it in.
2. `GENAI-PROMPTS-resource-map.md`: Prompts B1 to B5. The page, the sheet reader written from the spec, the
   consumption import, the shop-by-week map with drill-down, verdicts, exports, the check prompt.
3. `GENAI-PROMPTS-resource-map-leveling.md`: Prompts B2-1 to B2-5. The what-if layer: moves kept on top of the dates
   of record (drag a job, drag a project, farm out by hand), the contractor's own line, the project-name lookup,
   zoom, snapshot, present mode, the moves and farm-out exports, and the automatic level and farm-out with a
   before, leveled, farmed comparison. The leveler series (B2-1 to B2-5) runs after B4 and BEFORE Prompts X.
4. `GENAI-PROMPTS-xlsx.md`: Prompts X and X2, optional. If X was run before the leveler series, run X2 again after it.
5. `GENAI-PROMPTS-style.md`: Prompt S, last.

Why the order matters: a later hook prompt captures whatever a function is at the time and wraps it. Prompts X2, D
and B2 all wrap the file importer, so the one that must see the files first (the workbook unpacker) must be the
last to wrap.

## How to run a series

- One chat per tool. Paste a prompt as it stands in the file, including the angle-bracket placeholders only after
  you have replaced them (the data sheet spec, for example). Do not paste real data: the prompts never need any.
- The answer is a code block. Paste it into the HTML file where the prompt says: over a placeholder comment such as
  `<!-- MODULE 2: import -->`, or as the LAST scripts before `</body>`, in the order given. Some answers are two
  blocks (a one-line capture, then the module): keep them as two blocks, in that order. A capture in the same block
  as the function it captures recurses forever.
- Save the file with the name the series gives (`estimator.html`, `resource-map.html`). Open it in Edge or Chrome.
  Press F12 for the console if anything looks wrong.
- Run the check prompt (5, T2, D3, B5, B2-5) before opening the page. It lists what to fix and gives a small test.
- When a chat gets long and the model forgets an earlier module, paste that module's code back into the chat: the
  "contract reminder" paragraph in every prompt is the minimum it needs, and it is already in the prompt.
- If a step produces something that will not fit in one answer, the prompt tells the model to say so instead of
  shortening the logic. Then ask for the same step in two halves, by numbered items.

## Testing with made-up data

Every check prompt ends with a five-step test on made-up files. Make them by hand from the column lists above, a
few rows each, with numbers you can add up yourself. Then:

- Estimator: load the three history files and a two-line work package; one proposed JCN should find analogs and
  show an estimate; the batch run should write one consumption line per phase and one material line per stock
  number; a planned job summary in the planning file should come out with the planner's hours and source
  "planned". Hand-check one phase: the low and high of the analogs' hours, divided by the JCN count of a grouped
  summary.
- Resource Map: load the two workforce map sheets (as CSV) and the consumption file; pick one shop-week and add the
  sheet's hours for it yourself; the cell's percent must be that sum over the capacity. Nudge a job one week later
  from the drill-down and watch its hours move; farm a job out and see it land on the contractor's line; set the
  high band low (say 15) and press "Level and farm out" to see suggestions; export the moves list.
- Reload the page: everything comes back from the browser's store, moves included.

What "working" means here is what it meant in the tests: the page's numbers equal a calculation made by hand or by
another program on the same files.

## The weight test (section 6 of the estimator)

Nobody should guess the matching weights, so the page carries a test that fits them from the history itself. Load
the three exports, set "Jobs tested per half" (300 is plenty; fewer runs faster) and press "Run the weight test".
It splits the finished past jobs into two halves, hides each tested job, finds its closest past jobs among the
other half, estimates its hours the way the tool does (the median of the top five analogs' charged hours), and
compares with what the job actually charged. It does that under your weights, then changes one weight at a time
through a short ladder and keeps what lowers the error, fitting on one half and judging on the other, both ways.
The table shows your weights beside the fitted ones with the error under each; "(held out)" marks the honest
numbers, the ones judged on the half the weights were not fitted on. "Adopt suggested weights" writes the fitted
set into the weights panel; you can still edit any of them.

What to read: the Suggested column's error on both runs; the optimistic share (estimates more than the band under
the charged hours, the error that lets work overrun its window) matters more than the conservative share. Limits:
the test judges same-class matching only; it needs charged hours on the phases; each tested job keeps its 500
closest past rows under the starting weights (with that cap a 200,000-row made-up history ran in about 90 seconds
at 330 MB in the test here; without it the browser passed 2.8 GB and an hour); and on made-up data it only proves
that the test runs. The weights are a property
of the history, so run it again when the export grows.

## Prompt L: draft the project lookup

The workforce map names a project its own way (name, fiscal year, hull type); the JCN history and the estimator use
a project id. The lookup joins them. Paste the two name lists (they are identifiers, not records) and ask:

```
Here are two lists. List A is every project name on the workforce map. List B is every project id in the JCN
history export for future projects, with its hull. Match each name in A to the one id in B it most likely means
(same hull, same fiscal year, same availability type), and answer with a CSV of three columns, map_name, project,
hull, one row per name in A, with a fourth column "confidence" (sure, likely, guess) and a fifth "why" in a few
words. Leave project blank where nothing in B fits. Do not invent an id.

List A:
<paste>

List B:
<paste>
```

Check every "likely" and "guess" row yourself, drop the last two columns, save as `lookup.csv`, and load it into the
Resource Map with the other files. A name with no match stays as it is on the map.

## The files the tools write

| File | Written by | Columns |
|---|---|---|
| consumption.csv | estimator, batch | proposed_id, hull, project, phase_no, phase_title, shop, est_hours_low, est_hours_high, charged_hours_low, charged_hours_high, load_hours, week_start, week_end, placement, summaries_used, same_class, top_score, analog_jcns, notes, source, performing, performing_basis (22) |
| material_estimate.csv | estimator, batch | proposed_id, hull, project, job_summary, phase_no, phase_title, stock_number, nomenclature, qty_low, qty_high, seen_on, summaries_used, group_size, source, analog_jcns (15) |
| shop_week_summary.csv | Resource Map | shop, week_start, assigned_hours, proposed_hours, capacity_hours, load_percent, band |
| moves.csv | Resource Map, leveler | id, kind, key, weeks, performing, by, at, auto |
| consumption_moved.csv | Resource Map, leveler | the 22 columns above plus moved_weeks and shop_organic |
| assigned_moved.csv | Resource Map, leveler | project, shop, week_start, assigned_hours, moved_weeks, src |
| farmout_list.csv | Resource Map, leveler | proposed_id, project, hull, phases, hours, first week, last week, organic shops, basis, flag |
| resource-map-snapshot.png | Resource Map, leveler | the map as shown, for the TVs |

Every CSV opens in Excel as a pivot table: one header row, no merged cells, no totals rows.

## What is not built

- Float per phase from a schedule export: the leveler's window is the project's start and end. A schedule export
  with early start and late finish per phase would narrow it; that needs a reader prompt like A on that export.
- Ties between jobs (job B after job A): the leveler keeps phase order inside a job only.
- The emergent reserve per shop from history: deferred.
- Writing back to the schedule of record: nothing on the work computer can, so the moves list is the hand-off.
- Drag and drop needs a mouse; on a touch screen the 1-week buttons and the "Slip" box do the same thing.

## When something breaks

1. Press F12 and read the console. A red line with a function name is the usual case: use the Debug prompt "for an
   error" in `GENAI-PROMPTS-resource-map.md` (it applies to both tools) with that line pasted in.
2. A wrong number with no error: use the Debug prompt "for a wrong number" with what you expected and what you saw,
   with made-up figures.
3. The common causes, found in the tests here: a hook prompt run in the wrong order (X2 before D or B2: run X2
   again); a capture line pasted into the same block as the function it captures (split them); a module that read
   a field under a squashed name (loadhours) where the contract says load_hours; a date built with new Date(text),
   which shifts a week on a computer off UTC; a function bound to a button by name instead of through an arrow
   function, so a later redeclaration never runs (the planned-jobs prompt replaces the button with a clone for
   this reason).
4. The look (Prompt S) wrong after pasting: almost always a variable name missing from the mapping block; add it.

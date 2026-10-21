# Prompt A: analyze the resource map workbooks inside GenAI.mil

Version 0.2, 2026-10-22 (v0.1 kept; this version adds the header-label rule the yolo review asked for). Run this inside GenAI.mil with the real workbooks attached (if attachments are not
accepted for Excel, open each sheet, copy the first 15 rows including the header block, and paste them
under "Sheet text" in the prompt; the model does not need the values to be real, and you may overtype them
with made-up numbers first).

The answer it produces is a structure-only "data sheet spec". It names columns, layouts and rules, never
record content, so it can be brought out and pasted into the Resource Map build series (Prompt B1). Read the
answer before bringing it out and strike anything that quotes a value.

Suggested inputs: the project-level resource map and the shop-level map (capacity), one recent period
each. If there are several layouts in use, run the prompt once per layout.

---

## Prompt A: describe the resource map sheets so a program can read them

```
I am building an offline tool that reads resource map spreadsheets and turns them into two plain tables:
ASSIGNED (project, shop, week_start, assigned_hours) and CAPACITY (shop, week_start, capacity_hours). The
tool reads CSV files saved from these sheets, one CSV per sheet. I need you to describe the STRUCTURE of
the attached workbooks exactly enough that a program can be written from your description, without my
having to show the program any real data.

Rules for your answer: describe layout and structure only. Never quote a project name, ship name, hull
number, person, job number, hours value, date or any other cell content. Describe a value by its shape
("a four-digit number", "a code of two digits", "a date like YYYY-MM-DD", "a label like FYnn WKnn").
Where you need an example, invent one that is obviously fake.

For EACH sheet in each workbook, answer in this template, in this order:

SHEET: <workbook file name> / <sheet name>
ROLE: assigned hours by project and trade | capacity by shop | lookup (names, codes) | other: <what>
ORIENTATION: wide (weeks across columns) | long (one row per project-shop-week) | mixed
HEADER BLOCK: which rows are titles, notes or blank before the real header; the row number of the real
  header; whether the header spans two rows (for example month on one row and week on the next) and
  whether cells are merged
KEY COLUMNS: for each column before the week columns: its header text, what it identifies (project,
  shop, trade, hull, availability, phase, person, a subtotal label), the shape of its values, and
  whether it is blank on continuation rows (a value given once and implied below)
WEEK COLUMNS: the first and last column letters that hold weeks; the exact format of the week label
  (for example "FY27 WK03", "10/5/2026", "W40", a serial date); whether the label is a Monday, a Friday,
  a fiscal week number, or something else; whether every column is one week or some are months, quarters
  or totals; any column that must be skipped
UNITS: hours, man-days, head count, percent of a person; whether a blank cell means zero
TOTALS AND SUBTOTALS: rows that sum other rows (how to recognize them, for example a label containing
  "Total", bold, or a blank project cell), total columns, grand totals; all of these must be skipped
MULTIPLE BLOCKS: whether one sheet holds several blocks (for example one block per project, or
  assigned and capacity on the same sheet), and how a program tells where a block starts and ends
IDENTIFIERS: how a shop is written (two-digit code, code plus name, name only), how a project is
  written (availability name, hull plus period, job summary number), and whether the same thing is
  written differently on different sheets
TRAPS: hidden rows or columns, filters, formulas that show as errors, notes typed inside the grid,
  colors that carry meaning, cells with text where numbers belong, two sheets with the same role

Then, across all sheets, answer:

MAPPING: for each sheet with a data role, the rule that turns one cell into one row of ASSIGNED or
  CAPACITY: which key columns give project and shop, which header gives week_start and how to convert the
  week label to the Monday's date (state the rule, for example "FY27 WK01 starts on the first Monday of
  October 2026", or say it is unknown), and what number goes into hours
JOINS: whether shop codes and project names match between the assigned sheets and the capacity sheet,
  and what has to be translated
PERIOD: how many weeks one workbook covers and whether consecutive workbooks overlap

Last, give a SAMPLE for each data sheet: its header row(s) as written, followed by three made-up data rows
in the same layout, so a program can be tested on them. A header is record content when it names a
project, hull, availability, person or job (for example when projects run across the columns): replace
any such header with a made-up label of the same shape and say that you did. Mark the sample clearly as
made up.

Finish with a list of anything you could not determine and what would settle it.
```

## After the answer

1. Read it. Strike any real value that slipped through. Column headers that are field names are fine;
   a header that names a project, hull or person is a value and must be replaced.
2. Bring the spec and the samples out the way you brought the packet-structure report out.
3. Paste the whole spec into Prompt B1 of the Resource Map series where it says <PASTE THE DATA SHEET
   SPEC HERE>. The build prompts take the mapping rules from it, so the app reads your sheets as they are.
4. If the spec says the week label rule is unknown, decide it yourself (which Monday "WK01" is) and write
   it into the spec before pasting; the app needs one rule.

# Prompts X: read Excel workbooks directly (no CSV step)

Version 0.2, 2026-10-22 (v0.2 answers the yolo review of PR 54: a time or elapsed-time format such as [h]:mm was read as a date; now date styles and time styles are told apart, and a time-styled cell comes out as decimal hours). The question that started it: "For the inputs can we process in the .xlsx and output the CSV
in js in the html file?" Answer: yes. An .xlsx file is a zip of XML parts, and a browser can open both
without a library: DecompressionStream("deflate-raw") unpacks the zip entries and DOMParser reads the XML.
FACT (MDN browser-compat-data, read 2026-10-22): DecompressionStream accepts "deflate-raw" from Chrome 103
and Edge 103 (June 2022), Firefox 113 and Safari 16.4. Unverified: the Edge version on the work computers;
anything from 2023 on is fine.

Two prompts. Prompt X writes a module that turns a workbook into sheets of text cells. Prompt X2 hooks it
into a tool so a workbook chosen in the file picker is read as if each sheet were a CSV file named
"<workbook> / <sheet>.csv"; nothing else in the tool changes. The same two prompts work for the Resource
Map (`GENAI-PROMPTS-resource-map.md`) and the estimator (`GENAI-PROMPTS-estimator.md` plus `GENAI-PROMPTS-estimator-batch.md`); only one line in X2 names the tool's loader
functions. Output stays CSV (the tools already write it).

Limits: this reads workbooks up to a few tens of MB (a few hundred thousand cells per sheet) in one go.
The big JCN history export stays CSV when it is bigger than that; the resource maps, the proposed list
and the availabilities are small. Formulas are read from their cached result (what Excel saved), never
recalculated. Dates come out as YYYY-MM-DD text; a cell formatted as a time or an elapsed time (h:mm,
[h]:mm) comes out as decimal hours (1376.5), which is what such a cell means on a resource map; numbers as
plain decimals; booleans as TRUE/FALSE; error cells as blank.

Run order inside GenAI.mil: after the tool's last build prompt (B4 for the Resource Map, C2b for the
estimator), run Prompt X, paste its block after the last script block, then run Prompt X2 and paste its
two blocks after that. Then the check prompt (B5 or C3) and open the page.

---

## Prompt X: the workbook reader module

```
I am building offline tools for a ship repair planning department: single HTML files, vanilla JavaScript,
no libraries, no network, run on a work computer in Edge or Chrome. The tools read spreadsheets. Up to now
they read CSV only, which forces the planner to save every sheet as CSV first. Write MODULE X: one
<script> block that reads an Excel workbook (.xlsx or .xlsm) with nothing but built-in browser features,
so the tools can take the workbook directly. I will paste the block into each tool after its helpers.

Rules: plain global function declarations only (no IIFE, no class, no module, no window assignment); no
libraries, no fetch, no eval, no Worker; no em dashes anywhere; it must work in Edge 103 and later and
Chrome 103 and later (where DecompressionStream accepts "deflate-raw").

Functions to write, with these exact names and shapes:

1. async function readXlsx(file): takes a File (from an <input type="file">) and resolves to an array of
   sheets in workbook order: [{name: "Sheet name", rows: [[cell, cell, ...], ...]}]. Every cell is a
   string ("" for empty). Every row of a sheet is padded with "" to the width of the widest row of that
   sheet, and empty rows between used rows are kept as rows of "" so row numbers match Excel's (rows[0]
   is Excel row 1). It rejects with an Error whose message says what went wrong, for example "not a
   .xlsx workbook (no zip signature)", "unsupported compression method 12 in xl/worksheets/sheet1.xml",
   "zip64 workbook not supported, save the sheet as CSV", "sheet xl/worksheets/sheet1.xml is larger than
   150 MB, save it as CSV".

2. function sheetToTable(rows): the same row shape to {headers, data}: headers is the first row that has
   at least two non-empty cells, trimmed; data is an array of plain objects, one per later row that has
   at least one non-empty cell, keyed by header text (a blank header gets "col" + its 1-based column
   number; a duplicate header gets a suffix " 2", " 3"). This is the shape the tools' CSV reader already
   returns.

3. function isWorkbookFile(file): true when the file name ends in .xlsx or .xlsm (any case).

How readXlsx must work (the .xlsx format is a zip of XML parts):

ZIP reading, written by hand with a DataView over await file.arrayBuffer(), all integers little endian:
- Find the end of central directory record: scan backward from the end for the 4-byte signature
  0x06054b50, at most 65557 bytes from the end. In that record the total entry count is at offset 10 and
  the central directory offset at offset 16.
- Walk the central directory: each entry starts with signature 0x02014b50; compression method at offset
  10, compressed size at 20, uncompressed size at 24, file name length at 28, extra field length at 30,
  comment length at 32, local header offset at 42, file name (UTF-8) from 46. Entry size is 46 plus the
  three lengths. If a size or offset reads 0xFFFFFFFF, reject (zip64).
- To read a part: at its local header (signature 0x04034b50) read the file name length at 26 and the
  extra field length at 28; the data starts at 30 plus both lengths. Use the sizes from the central
  directory, never from the local header (it may hold zeros). Method 0: the bytes as they are. Method 8:
  new Blob([bytes]).stream().pipeThrough(new DecompressionStream("deflate-raw")), collected with new
  Response(stream).arrayBuffer(). Any other method: reject. Decode with new TextDecoder("utf-8").
- Keep part names exactly as stored; look a name up with and without a leading "/".

Workbook parts, parsed with new DOMParser().parseFromString(text, "application/xml") and read with
getElementsByTagNameNS("*", localName) so namespace prefixes do not matter:
- If xl/workbook.xml is missing, reject with "not an Excel workbook (no xl/workbook.xml)".
- xl/workbook.xml: the <sheet> elements in order give name and the relationship id (the attribute "id" in
  the namespace http://schemas.openxmlformats.org/officeDocument/2006/relationships; read it with
  getAttributeNS(that namespace, "id") and fall back to getAttribute("r:id")). A <workbookPr
  date1904="1"> or "true" means the 1904 date system.
- xl/_rels/workbook.xml.rels: <Relationship Id Target>. A Target starting with "/" is a full part name;
  otherwise it is relative to "xl/" (so "worksheets/sheet1.xml" is "xl/worksheets/sheet1.xml").
- xl/sharedStrings.xml (optional): the text of each <si> is the concatenation of every <t> inside it
  (rich text splits one string across several <r><t> runs). Keep an array in order.
- xl/styles.xml (optional): the <xf> elements under <cellXfs> in order; each has numFmtId. Two kinds of
  style matter. A DATE style: numFmtId 14 to 17, 22, 27 to 36 or 50 to 58 (built-in date formats; a few
  ids in the last two ranges are times in Asian locales, accepted), or a <numFmt> formatCode (from
  <numFmts>, matched by numFmtId) that contains y or d after stripping. A TIME style (a time of day or an
  elapsed time such as [h]:mm): numFmtId 18 to 21 or 45 to 47, or a stripped formatCode that contains h
  or s but neither y nor d. Stripping: remove quoted sections, backslash-escaped characters, and every
  [bracketed] section EXCEPT [h], [hh], [m], [mm], [s], [ss] (so colors, conditions and locale tags such
  as [$-409] go, elapsed-time markers stay), then compare in lower case. Anything else is a number style.
  Keep two arrays, isDateStyle and isTimeStyle, indexed by xf position.
- Each sheet part: for each <row>, its r attribute is the 1-based row number. For each <c> in it: the r
  attribute gives the cell address and its letters give the column (A is 0, Z is 25, AA is 26); the t
  attribute gives the type; <v> gives the stored value; <is> gives an inline string. Decide the cell's
  text in this order, first match wins:
  1. t="inlineStr": the concatenation of every <t> under <is>. Such a cell has no <v>, so this check
     comes before the next one.
  2. No <v> at all, or an empty <v></v> (a formula without a cached result, as some programs write it):
     "", never "0".
  3. t="s": sharedStrings[Number(v)].
  4. t="str": v as it is (a formula's text result).
  5. t="b": "TRUE" when v is "1", else "FALSE".
  6. t="e": "" (an error value such as #DIV/0!).
  7. t="d": the first 10 characters of v (a date written as ISO text, rare).
  8. Otherwise a number (t="n" or no t): if the cell's s attribute points at a date style, convert the
     serial to YYYY-MM-DD: the 1900 system counts days from 1899-12-30, the 1904 system from 1904-01-01;
     take Math.floor of the serial, add that many days (times 86400000) to Date.UTC of the base date, and
     format with UTC getters, zero padded. If it points at a time style, convert the serial to decimal
     hours: the serial times 24, rounded to 4 decimals, as plain text with no trailing zeros (1.5 becomes
     "36", 57.3541667 becomes "1376.5"), because such a cell holds hours on these sheets. Otherwise
     String(Number(v)), so "1.5E3" becomes "1500" and "40" stays "40".
  Always read the cached <v>; never evaluate <f>.
  A cell whose column is beyond the row's current length extends the row with "".

Performance: workbooks up to a few tens of MB (a few hundred thousand cells per sheet). Build each row
as an array; no string concatenation in loops; no querySelector per cell.

Helpers with these exact names: columnIndex(letters), serialToDate(serial, date1904), serialToHours(serial),
xmlText(element) (concatenated <t> descendants), stripFormatCode(code), isDateFormatCode(code),
isTimeFormatCode(code), parseZipDirectory(buffer) (returns a plain
object: part name to {method, compressedSize, uncompressedSize, localOffset}), readZipPart(buffer, dir,
name) (async; a string, or null when the part is missing). Also selfTestXlsx(): it needs no file; it
checks that columnIndex("A") is 0, columnIndex("AA") is 26, serialToDate(46300, false) is "2026-10-05",
serialToDate(61, false) is "1900-03-01", serialToHours(1.5) is "36", isDateFormatCode("m/d/yyyy") is true,
isDateFormatCode("[$-409]ddd m/d/yyyy") is true, isDateFormatCode("#,##0.00") is false,
isDateFormatCode("[h]:mm") is false, isTimeFormatCode("[h]:mm") is true, isTimeFormatCode("h:mm AM/PM")
is true, isTimeFormatCode("m/d/yy h:mm") is false (it is a date) and isDateFormatCode('0.00 "days"') is
false, and returns an array of the failed checks (empty when all pass).

Answer with the one <script> block only, and nothing after it.
```

## Prompt X2: hook the reader into a tool's file pickers

Before sending, replace the HANDLERS line with the tool you are in (the status element id must be
named there; without it the model guessed and sent the Resource Map's messages to an element it does not
have):
- Resource Map: `HANDLERS: importFiles(fileList), picker id files, status element id datastatus`
- Estimator: `HANDLERS: loadFiles(fileList), picker id files, status element id datastatus; and
  loadBatchFiles(files), picker id p-files, status element id batch-status`

```
Continue the same file. MODULE X (already pasted) gives readXlsx(file), which resolves to
[{name, rows}] with rows as padded arrays of strings (dates already YYYY-MM-DD, numbers plain decimals),
sheetToTable(rows), and isWorkbookFile(file). The tool's helpers include $(id) and csvCell(v) (one CSV
cell, quoted when needed). The tool's file pickers are wired through arrow functions that call the
handler by name, like (e => importFiles(e.target.files)), so a later declaration of the same handler
name is what the picker calls.

HANDLERS: <see above>

Write two small blocks to paste at the very end of the file, after MODULE X, in this order:

Block 1, a <script> holding one line per handler named in HANDLERS, capturing the current CSV-only
handler under its name plus "CSV": var <handler>CSV = <handler>;

Block 2, a <script> with plain global function declarations (no typeof guards, no function declarations
inside if blocks; the handlers in HANDLERS exist, declare them directly):
1. async function expandWorkbooks(fileList, statusId): returns a Promise of an array of File objects.
   Every file that is not a workbook (isWorkbookFile false) is passed through as it is. Every workbook is
   read with readXlsx; each sheet that has at least one non-empty cell becomes a new File made from its
   rows as CSV text (every cell through csvCell, cells joined with commas, rows with CRLF, UTF-8, type
   "text/csv"), named exactly "<workbook file name> / <sheet name>.csv", for example
   "resource-map-FY27.xlsx / Project Level.csv". The whole sheet goes into the CSV, header block and
   all, so the tool's sheet reader sees the same rows it would see from a CSV saved out of Excel. If
   readXlsx rejects, append one line "could not read <file name>: <message>" to the element with id
   statusId (when it exists) and go on with the next file. Append one line "<workbook file name>: N
   sheets read" when it succeeds.
2. A redeclaration of each handler with the same name and parameter that does nothing but:
   expandWorkbooks(list, "<that handler's status element id from HANDLERS>").then(files => <the
   captured CSV handler>(files)). The captured handler accepts a plain array, so pass the array.
3. At the bottom of the block, set accept=".csv,.xlsx,.xlsm" on each picker named in HANDLERS, guarded
   so a missing element is skipped.
No IIFE, no window assignment, no em dashes.

Answer with the two blocks only, and nothing after them.
```

## Notes for the data sheet spec

Prompt A names sheets as "<workbook> / <sheet>". The generated file names are exactly that plus ".csv",
so a sheet reader that chooses its mapping by name (for example name.indexOf("Project Level") >= 0) works
for both routes, and the src column reads "<workbook> / <sheet>.csv:<row>:<column>".

Dates differ by route: a CSV saved from Excel carries the cell's displayed text ("10/05/2026"), the
workbook route carries YYYY-MM-DD. toDate() accepts both, so nothing else changes. A week header typed
as text ("FY27 WK01") is the same on both routes.

## Test record

Tested 2026-10-22 against Gemini with no code execution (the test records stay in the private source). The final
prompts built working code first time: the reader matched openpyxl on every one of 77,654 cells across
five made-up workbooks (strings shared and inline, rich text, built-in and custom date formats, booleans,
cached formulas, error cells, stored and deflated zip entries) and rejected three bad files with the
intended messages; the estimator fed with `history.xlsx` (four sheets) and `proposed.xlsx` wrote a
consumption file identical to its CSV-input run; the Resource Map fed with the workbook drew the same map
and summary as its CSV-input run. Three earlier rounds found four prompt faults (a formula with no cached
value read as 0; typeof guards; the wrong status element; all now written into the prompts above).
v0.2 (after the yolo review of PR 54): the date-or-time rule above, and the cell rules as a numbered order
(a first draft of v0.2 put the blank-cell rule before the inline-string check and blanked every inline
string). Re-tested: 0 mismatches on 77,694 cells with six new time and date cases, and both tools still
identical to their CSV runs.

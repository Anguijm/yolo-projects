# Prompts W: the workbook converter page (Excel workbooks in, one CSV per sheet out)

Version 0.1, 2026-10-24. Built on the owner's ruling of 2026-10-24 ("Ask me": a standalone workbook converter page
replaces the X and X2 hooks). Until now a tool that had to take an .xlsx directly carried the workbook reader inside
it (Prompt X) and a hook around its file pickers (Prompt X2), and every tool needed both pasted in the right order,
which cost one wrong-order fault in the tests. This page does the conversion once, outside the tools: choose one or
more workbooks, get one CSV per sheet, named "<workbook> - <sheet>.csv", with the same cell rules the reader has
always applied (dates as YYYY-MM-DD, times as decimal hours, numbers plain, booleans TRUE/FALSE, error cells blank,
cached formula results, never a recalculation). The tools keep reading CSV, which they already do. Prompts X and X2
(`GENAI-PROMPTS-xlsx.md`) stay in the folder for tools already built with them; a new build uses this
page instead and skips X.

Tested: the page built from this text by Gemini with no earlier answers in the chat (two rounds of W2), assembled
with the proven reader, and checked in a headless browser against openpyxl on five made-up workbooks: all 77,694
cells of the twelve converted sheets equal, names, counts, CRLF, no byte-order mark, a bad file reported, Blob URLs
revoked. Test record kept in the private source.

The reader module is the one Prompt X built and the record proved on 77,694 cells against openpyxl (the same text,
reproduced here as Prompt W1 so this file stands alone; the only change is the sentence that says where the block is
pasted). The page around it is new (Prompt W2). The check is W3.

Contracts:

- Input: .xlsx or .xlsm files, any number, chosen together or in several picks (each pick replaces the list).
- Output: one CSV per sheet that has at least one non-empty cell. Every cell as the reader gives it; a cell is quoted
  only when it holds a comma, a double quote, a carriage return or a line feed, with inner quotes doubled; the text
  is never otherwise changed (no apostrophe before an equals sign, no trimming); rows end with CRLF, the last one too;
  UTF-8 without a byte-order mark. The whole sheet goes out, header block and all, so a tool's sheet reader sees the
  same rows it would see from a CSV saved out of Excel.
- File name: the workbook's name without its extension, a space, a hyphen, a space, the sheet name, ".csv"; the
  characters \ / : * ? " < > | in either part become "_".
- Element ids: w-file, w-status, w-table, btn-all, w-note.
- Globals (let, at the top of the page's own script): SHEETS (array of {workbook, sheet, rows, cols, cells, size,
  fileName, url}), plus whatever MODULE X declares.
- Functions (page): csvCell(v), sheetToCSV(rows), fileNameFor(workbook, sheet), loadWorkbooks(files),
  renderSheets(), downloadAll(). Functions (reader, from W1): readXlsx(file), sheetToTable(rows),
  isWorkbookFile(file), columnIndex, serialToDate, serialToHours, xmlText, stripFormatCode, isDateFormatCode,
  isTimeFormatCode, parseZipDirectory, readZipPart, selfTestXlsx.

---

## Prompt W1: the workbook reader module (the text of Prompt X, pasted into this page)

```
I am building offline tools for a ship repair planning department: single HTML files, vanilla JavaScript,
no libraries, no network, run on a work computer in Edge or Chrome. The tools read spreadsheets. Up to now
they read CSV only, which forces the planner to save every sheet as CSV first. Write MODULE X: one
<script> block that reads an Excel workbook (.xlsx or .xlsm) with nothing but built-in browser features,
so a converter page can turn a workbook into CSV files. I will paste the block into that page after its helpers.

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

## Prompt W2: the converter page around the reader

```
Now write the page itself: a single, self-contained HTML file, the workbook converter for a ship repair
planning department. Plain HTML, CSS and vanilla JavaScript: no library, no framework, no network call,
no CDN, no web font, no eval, no inline event attributes (onclick=""); a Content-Security-Policy meta tag
with default-src 'none', script-src 'unsafe-inline', style-src 'unsafe-inline', img-src data:,
connect-src 'none', form-action 'none'. Every function is a plain global function declaration (no IIFE,
no module, no class, never assigned through window); every global is declared with let at the top of
the page's own script block. Light and dark follow the system (prefers-color-scheme) with system fonts.
No em dashes anywhere in the file. Never use alert, confirm or prompt.

The file has two script blocks, in this order: first the line <!-- MODULE X --> on its own, after the
body's content and OUTSIDE any <script> tag, because the reader block from the previous step brings its
own <script> and </script> tags and is pasted over that line as it is (it declares readXlsx(file), which
resolves to [{name, rows}] with rows as padded arrays of strings, isWorkbookFile(file), sheetToTable(rows)
and selfTestXlsx(), which returns an array of failed self-checks); then the page's own <script>, which
may call those by name because it comes after.

Page, in order, with these exact element ids:
1. A one-line heading and one sentence: the workbooks are read in the browser and never leave the
   computer; each sheet comes out as a CSV the planning tools read.
2. "1. Choose workbooks": <input type="file" id="w-file" accept=".xlsx,.xlsm" multiple>; div id w-status.
3. "2. Sheets": table id w-table; <button id="btn-all" disabled>Download all</button>; div id w-note
   holding this sentence: "If the browser asks whether this page may download several files, allow it."

Script, in this order:
- Globals: let SHEETS = []; (array of {workbook, sheet, rows, cols, cells, size, fileName, url}).
- Helpers: $(id); esc(s) (HTML-escapes &, <, >, " and ').
- csvCell(v): v as a string; if it contains a comma, a double quote, a carriage return or a line feed,
  wrap it in double quotes with every inner double quote doubled; otherwise return it unchanged. Never
  add an apostrophe, never trim, never change the text in any other way: the CSV must carry exactly what
  the reader gave.
- sheetToCSV(rows): every row's cells through csvCell joined with commas, rows joined with CRLF, and one
  CRLF after the last row. The whole sheet, header block and all.
- fileNameFor(workbook, sheet): the workbook's file name without its last extension, then " - ", then the
  sheet name, then ".csv"; in both parts replace each of the characters \ / : * ? " < > | with "_".
- loadWorkbooks(files): revoke every url in SHEETS (URL.revokeObjectURL) and empty SHEETS and w-status.
  Then for each file in order: if isWorkbookFile is false, append the line "<name>: not a workbook,
  skipped" to w-status and go on. Otherwise await readXlsx(file); if it rejects, append "could not read
  <name>: <message>" and go on. For each sheet: if no cell is non-empty, count it as skipped; else build
  the CSV with sheetToCSV, make a Blob of it (type "text/csv;charset=utf-8", no byte-order mark), and push
  {workbook: file name, sheet: sheet name, rows: the number of rows, cols: the width, cells: the number of
  non-empty cells, size: the CSV's length in bytes (the Blob's size), fileName: fileNameFor(...), url:
  URL.createObjectURL(blob)}. Append "<name>: N sheets converted, M empty sheets skipped" to w-status.
  After the last file: renderSheets(), and enable btn-all when SHEETS is not empty.
- renderSheets(): set w-table's innerHTML to a thead and a tbody (never a table inside a table) with
  columns Workbook, Sheet, Rows, Columns, Non-empty cells, First row (the first row that has a non-empty
  cell, its first six cells joined with " | ", escaped, then " ..." when the row is wider), Size (KB, one
  decimal), Download (an <a> with href = url and download = fileName, text "Download"). One HTML string,
  set once.
- downloadAll(): click each sheet's download link in table order, 400 milliseconds apart (setTimeout),
  so a browser that allows several downloads saves them all; write "downloading N files" in w-note and
  the sentence above back after the last one.
- At the end of the script: run selfTestXlsx(); when it returns a non-empty array, write "reader
  self-test failed: <the items joined with ', '>" into w-status, else nothing. Wire w-file change to
  loadWorkbooks(Array.from(this.files)) and btn-all click to () => downloadAll(), both through arrow
  functions, at the end of the script; no DOMContentLoaded listener.

Answer with the complete HTML file in one code block, with the <!-- MODULE X --> line where the reader
goes, and nothing after it.
```

## Prompt W3: check the converter (run in the same chat; it needs the whole file)

```
I have pasted MODULE X over its placeholder. Without rewriting the file, check:
1. That the page's script comes after MODULE X and calls nothing that MODULE X does not declare, that no
   function is assigned through window, no element carries an inline event attribute, nothing calls
   alert, confirm or prompt, and the CSP meta tag is present.
2. That csvCell quotes only on a comma, a double quote, CR or LF, doubles inner quotes, and never changes
   the text otherwise; that sheetToCSV ends every row, the last included, with CRLF; that the Blob has no
   byte-order mark.
3. That a sheet with no non-empty cell is skipped and counted, that a file that is not a workbook is
   reported and skipped without stopping the others, and that a rejected workbook's message reaches
   w-status.
4. That every Blob URL from an earlier pick is revoked when a new pick is loaded, and that the file names
   follow the rule (workbook name without extension, " - ", sheet name, ".csv", forbidden characters
   replaced).
Then give me a five-step test with one made-up workbook of three sheets, one of them empty, one with a
date column, a time column and a text cell holding a comma.
```

## Debug prompts

Use the two Debug prompts at the end of `GENAI-PROMPTS-estimator-batch.md` (console error; wrong result
with no error) unchanged.

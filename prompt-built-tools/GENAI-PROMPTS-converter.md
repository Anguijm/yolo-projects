# Prompts W: the workbook converter page (Excel workbooks in, one CSV per sheet out, one zip down)

Version 0.3, 2026-10-31 (v0.1 and v0.2 kept in the private source). v0.3, from the edge-case tests of 2026-10-31
(the private test record): the reader's sheetToTable counts duplicate headers in a Map and builds its row objects
with Object.create(null) (a header named constructor came out as "constructor NaN"; the CSV output never went through
it and was right on every cell), and the page numbers file names that match without regard to case, so a zip never
holds Case.csv and case.csv side by side (the review's point on PR 87). v0.2 answers the owner's first run on a real workbook at work
(53 tabs; nothing from it came here). The instructions were vague and called the reader MODULE X inside a series
named W, so the reader is MODULE W1 and the page MODULE W2 everywhere and a "how to run it" block opens the file.
"Download all" fired 53 separate downloads and the browser kept about 50, so it is gone: every sheet row has a
checkbox (all ticked after a load) and one button zips the ticked sheets into one file, written by hand in the zip
format's uncompressed form so no library is needed and the browser asks once. A workbook that yields a single sheet
names its CSV after the workbook alone ("<workbook>.csv"); several sheets keep "<workbook> - <sheet>.csv". The
per-row Download link stays for one file at a time. W2 regenerated from this text and tested headless against
openpyxl and Python's zipfile on the made-up workbooks, a 53-tab one included; test record kept in the private source ("v0.2").

How to run it (one chat in GenAI.mil, three prompts, nothing else needed):
1. Paste Prompt W1. Save the answer (one script block, from <script> to </script>) in a text file.
2. Paste Prompt W2 in the same chat. Save the answer as converter.html, open it in a text editor, find the line
   <!-- MODULE W1 --> and paste the W1 block over that line. Open converter.html in Edge or Chrome.
3. Paste Prompt W3 and run the five-step test it gives. If something fails, use a Debug prompt (at the end).

What the page does. Choose one or more workbooks (.xlsx or .xlsm); every sheet with content becomes a CSV with the
same cell rules the tools' reader has always applied (dates as YYYY-MM-DD, times as decimal hours, numbers plain,
booleans TRUE/FALSE, error cells blank, cached formula results, never a recalculation). Tick the sheets you want and
download them as one zip, or save one sheet from its row. The planning tools keep reading CSV, which they already do.

Contracts:

- Input: .xlsx or .xlsm files, any number, chosen together or in several picks (each pick replaces the list).
- Output: one CSV per sheet that has at least one non-empty cell. Every cell as the reader gives it; a cell is quoted
  only when it holds a comma, a double quote, a carriage return or a line feed, with inner quotes doubled; the text
  is never otherwise changed (no apostrophe before an equals sign, no trimming); rows end with CRLF, the last one too;
  UTF-8 without a byte-order mark. The whole sheet goes out, header block and all, so a tool's sheet reader sees the
  same rows it would see from a CSV saved out of Excel. The ticked sheets go out together as one zip (the store form
  of the zip format, no compression, UTF-8 names), one download.
- File name: when the workbook yielded exactly one sheet with content, the workbook's name without its extension
  and ".csv"; otherwise the workbook's name without its extension, a space, a hyphen, a space, the sheet name,
  ".csv". The characters \ / : * ? " < > | in either part become "_". A name repeated inside one zip gets " (2)",
  " (3)" and so on before ".csv". The zip is named after the workbook (without its extension, ".zip") when the
  ticked sheets come from one workbook, "converted.zip" otherwise.
- Element ids: w-file, w-status, w-table, btn-on, btn-off, btn-zip, w-note.
- Globals (let, at the top of the page's own script): SHEETS (array of {workbook, sheet, rows, cols, cells, size,
  fileName, url, blob, selected}), CRC_TABLE (null until first use), plus whatever MODULE W1 declares.
- Functions (page): csvCell(v), sheetToCSV(rows), cleanName(s), fileNameFor(workbook, sheet, single),
  loadWorkbooks(files), renderSheets(), updateZipButton(), selectAll(on), crc32(bytes), zipStore(entries),
  zipNameFor(), downloadSelected(). Functions (reader, from W1): readXlsx(file), sheetToTable(rows),
  isWorkbookFile(file), columnIndex, serialToDate, serialToHours, xmlText, stripFormatCode, isDateFormatCode,
  isTimeFormatCode, parseZipDirectory, readZipPart, selfTestXlsx.

---

## Prompt W1: the workbook reader module

```
I am building offline tools for a ship repair planning department: single HTML files, vanilla JavaScript,
no libraries, no network, run on a work computer in Edge or Chrome. The tools read spreadsheets. Up to now
they read CSV only, which forces the planner to save every sheet as CSV first. Write MODULE W1: one
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
   at least two non-empty cells, trimmed; data is an array of objects created with Object.create(null)
   (never object literals: a header is free text and may read constructor or __proto__), one per later row
   that has at least one non-empty cell, keyed by header text (a blank header gets "col" + its 1-based
   column number; a duplicate header gets a suffix " 2", " 3", counted in a Map keyed by the header text,
   never in a plain object, which inherits constructor and toString and turned those headers into
   "constructor NaN" in the edge tests of 2026-10-31). This is the shape the tools' CSV reader already
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

The file has two script blocks, in this order: first the line <!-- MODULE W1 --> on its own, after the
body's content and OUTSIDE any <script> tag, because the reader block from the previous step brings its
own <script> and </script> tags and is pasted over that line as it is (it declares readXlsx(file), which
resolves to [{name, rows}] with rows as padded arrays of strings, isWorkbookFile(file), sheetToTable(rows)
and selfTestXlsx(), which returns an array of failed self-checks); then the page's own <script>, which
may call those by name because it comes after.

Page, in order, with these exact element ids:
1. A one-line heading and this sentence, capital letter and all: "The workbooks are read in the browser
   and never leave the computer; each sheet comes out as a CSV the planning tools read."
2. "1. Choose workbooks": <input type="file" id="w-file" accept=".xlsx,.xlsm" multiple>; div id w-status.
3. "2. Sheets": table id w-table; then three buttons in one line: <button id="btn-on">Select all</button>,
   <button id="btn-off">Select none</button>, <button id="btn-zip" disabled>Download the ticked sheets as
   one zip</button>; then div id w-note holding this sentence: "The ticked sheets go into one zip file, so
   the browser asks once; the Download link on a row saves that one CSV by itself."

Script, in this order:
- Globals: let SHEETS = []; (array of {workbook, sheet, rows, cols, cells, size, fileName, url, blob,
  selected}); let CRC_TABLE = null;
- Helpers: $(id); esc(s) (HTML-escapes &, <, >, " and ').
- csvCell(v): v as a string; if it contains a comma, a double quote, a carriage return or a line feed,
  wrap it in double quotes with every inner double quote doubled; otherwise return it unchanged. Never
  add an apostrophe, never trim, never change the text in any other way: the CSV must carry exactly what
  the reader gave.
- sheetToCSV(rows): every row's cells through csvCell joined with commas, rows joined with CRLF, and one
  CRLF after the last row. The whole sheet, header block and all.
- cleanName(s): s with each of the characters \ / : * ? " < > | replaced by "_".
- fileNameFor(workbook, sheet, single): base = cleanName(the workbook's file name without its last
  extension). When single is true (the workbook yielded exactly one sheet with content), return base +
  ".csv"; otherwise return base + " - " + cleanName(sheet) + ".csv".
- loadWorkbooks(files): revoke every url in SHEETS (URL.revokeObjectURL) and empty SHEETS and w-status.
  Then for each file in order: if isWorkbookFile is false, append the line "<name>: not a workbook,
  skipped" to w-status and go on. Otherwise await readXlsx(file); if it rejects, append "could not read
  <name>: <message>" and go on. Keep the sheets that have at least one non-empty cell, in workbook order,
  and count the others as skipped; single = (exactly one sheet was kept). For each kept sheet: build the
  CSV with sheetToCSV, make a Blob of it (type "text/csv;charset=utf-8", no byte-order mark), and push
  {workbook: file name, sheet: sheet name, rows: the number of rows, cols: the width, cells: the number of
  non-empty cells, size: the Blob's size, fileName: fileNameFor(file name, sheet name, single), url:
  URL.createObjectURL(blob), blob: the Blob, selected: true}. Before pushing, if that fileName, compared
  without regard to case, equals the fileName of any sheet already in SHEETS, insert " 2" (then " 3", and
  so on, the first free number) before the ".csv", because a Windows desktop treats Case.csv and case.csv
  as one file and the zip would lose one of them. Append "<name>: N sheets converted, M empty
  sheets skipped" to w-status. After the last file: renderSheets().
- renderSheets(): set w-table's innerHTML to a thead and a tbody (never a table inside a table) with
  columns: a checkbox (<input type="checkbox" data-i="<the index in SHEETS>">, checked when the sheet is
  selected), Workbook, Sheet, Rows, Columns, Non-empty cells, First row (the first row that has a
  non-empty cell, its first six cells joined with " | ", escaped, then " ..." when the row is wider), Size
  (KB, one decimal), File name (the sheet's fileName), Download (an <a> with href = url and download =
  fileName, text "Download"). One HTML string, set once. Then query the checkboxes and wire each one's
  change event (never an inline attribute) to set SHEETS[i].selected from its checked state and call
  updateZipButton(); then call updateZipButton() once.
- updateZipButton(): count the selected sheets; btn-zip is enabled when the count is at least 1 and
  disabled otherwise; its text is "Download the N ticked sheets as one zip" (for N = 1, "Download the 1
  ticked sheet as one zip"; for N = 0, "Download the ticked sheets as one zip").
- selectAll(on): set every SHEETS[i].selected to on, set every checkbox in w-table to match, then
  updateZipButton().
- crc32(bytes): the standard CRC-32 over a Uint8Array (polynomial 0xEDB88320; build the 256-entry table
  once into CRC_TABLE; start at 0xFFFFFFFF, finish with xor 0xFFFFFFFF, return the value as an unsigned
  32-bit number, so crc32 of the ASCII bytes of "123456789" is 0xCBF43926).
- zipStore(entries): entries is an array of {name, bytes} (name a string, bytes a Uint8Array); returns a
  Blob (type "application/zip") holding a ZIP file in the store form (method 0, no compression), which
  every unzipper opens. Write it by hand with DataView, every integer little endian, in this order:
  1. For each entry, a local file header, then its bytes: signature 0x04034b50 (4 bytes), version needed
     20 (2), general purpose flags 0x0800 (2; the name is UTF-8), method 0 (2), modification time (2)
     and date (2) in MS-DOS form from the current clock (time = hours shifted left 11, plus minutes
     shifted left 5, plus seconds halved; date = the year minus 1980 shifted left 9, plus the month 1 to
     12 shifted left 5, plus the day), CRC-32 of the bytes (4), compressed size (4) and uncompressed size
     (4), both the byte length, name length (2), extra field length 0 (2), then the name as UTF-8 bytes
     (TextEncoder), then the bytes themselves. Remember the offset of each entry's local header.
  2. Then the central directory, one record per entry: signature 0x02014b50 (4), version made by 20 (2),
     version needed 20 (2), flags 0x0800 (2), method 0 (2), the same time (2) and date (2), CRC-32 (4),
     compressed size (4), uncompressed size (4), name length (2), extra length 0 (2), comment length 0
     (2), disk number 0 (2), internal attributes 0 (2), external attributes 0 (4), the entry's local
     header offset (4), then the name bytes.
  3. Then the end record: signature 0x06054b50 (4), disk number 0 (2), directory disk 0 (2), entries on
     this disk (2), entries in all (2), central directory size (4), central directory offset (4),
     comment length 0 (2).
  Build the pieces as Uint8Arrays in an array and make one Blob from that array at the end (never join
  strings). Before writing, if the entries number more than 65,535, or any size or offset would not fit
  in 32 bits, throw an Error whose message says the zip would be too large and to download in smaller
  picks.
- zipNameFor(): the distinct workbook names among the selected sheets; when there is exactly one,
  cleanName(that name without its last extension) + ".zip"; otherwise "converted.zip".
- downloadSelected(): take the selected sheets in table order; if there are none, return. For each,
  bytes = new Uint8Array(await sheet.blob.arrayBuffer()); the entry name is the sheet's fileName, and
  when a name repeats inside this zip, the second gets " (2)" before ".csv", the third " (3)", and so on.
  Then zipStore(entries) inside try/catch: on an error write its message into w-note and stop. Otherwise
  make an object URL of the zip Blob, create an <a> with href = that URL and download = zipNameFor(),
  append it to the body, click it, remove it, and revoke the URL after one second (setTimeout). Write
  "zipped N files, M KB" (M one decimal, the zip Blob's size) into w-note, and put the sentence above
  back after ten seconds.
- At the end of the script: run selfTestXlsx(); when it returns a non-empty array, write "reader
  self-test failed: <the items joined with ', '>" into w-status, else nothing. Wire w-file change to
  loadWorkbooks(Array.from(this.files)), btn-on click to () => selectAll(true), btn-off click to () =>
  selectAll(false) and btn-zip click to () => downloadSelected(), all through arrow functions, at the end
  of the script; no DOMContentLoaded listener.

Answer with the complete HTML file in one code block, with the <!-- MODULE W1 --> line where the reader
goes, and nothing after it.
```

## Prompt W3: check the converter (run in the same chat; it needs the whole file)

```
I have pasted MODULE W1 over its placeholder. Without rewriting the file, check:
1. That the page's script comes after MODULE W1 and calls nothing that MODULE W1 does not declare, that
   no function is assigned through window, no element carries an inline event attribute, nothing calls
   alert, confirm or prompt, and the CSP meta tag is present.
2. That csvCell quotes only on a comma, a double quote, CR or LF, doubles inner quotes, and never changes
   the text otherwise; that sheetToCSV ends every row, the last included, with CRLF; that the Blob has no
   byte-order mark.
3. That a sheet with no non-empty cell is skipped and counted, that a file that is not a workbook is
   reported and skipped without stopping the others, and that a rejected workbook's message reaches
   w-status.
4. That every Blob URL from an earlier pick is revoked when a new pick is loaded, and that the file names
   follow the rule: a workbook that yielded one sheet gives "<workbook>.csv", otherwise "<workbook> -
   <sheet>.csv", forbidden characters replaced, a repeated name inside a zip numbered, names that match
   without regard to case included (Case.csv, then case 2.csv).
5. That the zip is the store form: every local file header, central directory record and end record
   carries the fields in the order listed, with little-endian integers and UTF-8 names (flag 0x0800);
   that crc32 of the ASCII bytes of "123456789" is 0xCBF43926; and that the zip holds exactly the ticked
   sheets in table order.
6. That btn-zip is disabled with nothing ticked and its text counts the ticked sheets, that Select all
   and Select none change both the boxes and SHEETS, and that the zip is named after the workbook when
   the ticked sheets come from one workbook and converted.zip otherwise.
Then give me a five-step test with two made-up workbooks: one with a single sheet (its CSV must be named
after the workbook alone), one with three sheets, one of them empty, one with a date column, a time
column and a text cell holding a comma; tick two sheets, download the zip, open it, and check the names
and the contents against the sheets.
```

## Debug prompts

Use the two Debug prompts at the end of `GENAI-PROMPTS-estimator-batch.md` (console error; wrong result
with no error) unchanged.

## History: Prompts X and X2

Until this page existed, a tool that had to take an .xlsx directly carried the workbook reader inside it (Prompt X)
and a hook around its file pickers (Prompt X2), and every tool needed both pasted in the right order, which cost one
wrong-order fault in the tests. Prompt W1 is that reader's text with its new name; the record proved it on 77,694
cells against openpyxl. Prompts X and X2 (`GENAI-PROMPTS-xlsx.md`) stay in the folder for tools already built
with them; a new build uses this page instead and skips X. v0.1 of this page (2026-10-24) had one Download link per
sheet and a "Download all" that clicked them 400 milliseconds apart; the page was built from its text by Gemini
(two rounds of W2) and checked against openpyxl on five made-up workbooks, all 77,694 cells equal.

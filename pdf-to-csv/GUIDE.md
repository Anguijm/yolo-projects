# PDF to CSV: usage guide

PDF to CSV is one HTML file that reads a folder of PDF records and writes a spreadsheet: one row per
record, one column per field you name. It runs in the browser, offline. Nothing leaves the computer.

Open it here: https://anguijm.github.io/yolo-projects/pdf-to-csv/index.html

This guide walks through one job from start to finish, then lists what every button does and what to do
when a value comes out wrong. Button names are written as they appear on screen.

---

## 1. Get the file onto the computer that holds the records

**Download.** Open the link above, press Ctrl+S (or the browser's Save page as) and save it as
`pdf-to-csv.html`, "Webpage, HTML only". Copy that one file across.

**Or carry it as text.** Open the link, press Ctrl+U to see the source, select all, copy, paste into a plain
text editor such as Notepad and save as `pdf-to-csv.html`. The file is pure ASCII, so it does not matter
which encoding the editor picks. It must end with `</html>`.

**Open it** by double-clicking. Chrome or Edge. If the copy is incomplete, a red notice at the top says so;
copy it again.

**What it stores on the computer.** The template (your field names and the sample's drawn lines) in the
browser's local storage, and the results of a run in the browser's database so a run can resume. The
results hold the extracted values until you press "Erase saved results from this browser" on the Results
tab. Nothing is written to disk except the files you download.

---

## 2. Build the template from one sample record

The template is the list of fields to read. You can type it from memory, but a sample record makes it far
better: the tool reads the sample's drawn lines, offers the labels it finds, and shows what each field
would read before you run anything.

On the **1. Fields** tab:

1. **Sample PDF**: choose one record. Its first page appears. Boxes outline each piece of text. If the form
   has drawn cells, red lines show the lines the tool found and the page line says how many cells they
   make, for example "44 cells from 46 drawn lines". Hatched text is a running header or footer, which is
   ignored.

2. **Set the anchor.** With Mode on "Click text = set form anchor", click the form number or title on the
   page (something printed on every copy of this form and on nothing else). It appears in "Anchor text"
   under Forms in this template. If the form number is printed on every page of the record, that is fine:
   set "Pages per form" to the number of pages one copy of the form takes and the tool will start a new
   copy only every that many pages.

3. **Pages per form.** How many pages one copy of the form covers, including pages the description box
   continues onto. For a main form whose fields are all labels, a page over is safe. Use the exact count for a
   form with a table (a table is read on every page in that range that repeats its heading row) and for an
   extra form whose copies can follow one another (no new copy is looked for inside that range).

4. **Page through the form** with the arrows, once, so the drawn lines of every page are remembered. Each
   page you look at is stored in the template. You only need to do this on the sample.

5. **Auto-detect labels on this page.** Press it on each page of the form. It adds a field for every label
   it finds. A label that appears in several blocks (Name, Date, Phone under four signature headings) is
   added as "PREPARED BY > Name", "REVIEWED BY > Name" and so on, one per block.

6. **Compare with more records.** Optional: choose two to four more records of the same form, as unlike each
   other as you can (other offices, dates, people), so that no value reads the same in all of them. Text that
   reads the same in every record at the same place is taken as part of the form; text that differs is a value
   and turns blue. The page line says how many records have a page that lines up with this one (pages pair by
   their first line, or by most of its words when the scan misread one). Press Auto-detect again afterwards. It
   adds a label the type size could not prove when the text beside or below it changes between records. It
   leaves out a short text that reads differently in the records, but only with two or more. Its message names
   both; check them.

7. **Check the Fields table.** The "Value from sample" column shows what each field reads from the sample.
   This is the real test. Rename fields by editing the Name box (that becomes the CSV column heading), tick
   "Req" for fields that must be present, and remove fields you do not want with the x.

8. **Fix what reads wrong.** The list under Fields by name is the same template as text; edit it there and
   press "Use these field names". See section 5 for the syntax and section 7 for common fixes.

9. **Save template file.** Downloads `pdf-to-csv-template.json`. Keep it with the records. Next time, "Load
   template file" brings everything back, drawn lines included. The template holds field names, labels,
   box positions and the sample's line positions, never any record content.

**Packets with two kinds of main form (v0.8).** When a record's main form is sometimes one form and sometimes
another (a short form or a long form), make both, each with Kind "Main form": to make the second one, press
"Add another form type", set its Kind to "Main form" and rename it. A main form without an anchor (the usual
long form) is chosen by page 1 alone. Page 1 decides which one a record
holds (page 1, or, when every main form has an anchor, the first page an anchor is on, unless page 2's counter
reads "2 of N", or a 2 that page 3 continues, which makes page 1 the form's own first page; a lone 2 is not enough): its anchor (printed at the top or foot of page 1; a mention mid-page counts for less), how many of its labels are on page 1, and whether page 1 has numbered outline items
("1.1", "1.2"), which the tool learns when you view page 1 of a sample that the run reads as that form, and shows under the
Forms table (a sample the run reads as the other form type teaches it nothing, and the editor says so). Give fields that mean
the same thing the same column name with `Column = label as printed`, for example `Job Number = Job Control
Number` on the long form and plain `Job Number` on the short form: both fill one CSV column.

**Where a form ends (v0.8).** Set "Form ends" to "when its page counter restarts, changes style or reaches its
total (forms whose length varies)" for forms whose length varies. The tool reads the page counter at the top or bottom of every page ("Pg 3 of 12", "3 of 12",
"3 / 12", a bare "3", "A-3") and the form ends where the counter restarts, changes style (a bare number
becoming "A-1"), or reaches its total. The page line on the sample shows the counter it found. If the form
states its own last page (an effective-pages table), name that field in "Last page from": a record where the
two disagree is listed in problems.csv as "form end unclear". Fields are read only inside the form's pages, so
labels that come back in attachments are never picked up; a value that runs off the foot of the form's last
page is not carried onto the next page, and problems.csv says "value continues past the form". Leave it on 'after "Pages per form" pages' for forms
of a fixed length. If the counter cannot be read, a main form whose anchor is printed at the top or bottom of each of its pages
is followed by that anchor instead, and problems.csv says "span followed the anchor". A page counts only if it
prints the anchor the way the form's first page does: at about the same place, with mostly the same words on that
line. So a page that only mentions the form ("Attachment to FORM SF-12") ends it, and is never taken as a page whose
header was lost. problems.csv's "values from the anchor run" names each field read from pages taken this way, with
its pages: check those values first. Following the anchor also
stops at the number of pages the counter states (a count that read "2 of 4" takes at most two more pages). In a
template with two main forms or a counter rule, an anchor matches as a whole: "FORM SF-1" does not match
"FORM SF-12" (older templates match any text that contains the anchor). Known gaps: a form number such as
"SF-12" near the page edge can be taken for a page counter when the real counter cannot be read; and a document
after the main form that has no readable counter but prints the same anchor line in the same place (a stamp on
every page, for example) is taken in when the span follows the anchor; its notes list the pages and the fields
read there. Pages per form is greyed
out when it is not used: under the counter rule, and for a main
form without an anchor, which covers the whole record. Warnings under the Forms table say when a setting
cannot work, for example an extra form with no anchor (never looked for) or a "Last page from" name that is
not one of the form's fields. "Last page from" ignores case, and can name a table column: `Effective Pages >
Pages`.

**Extra forms.** If a record may contain a second form type (a supplementary sheet that appears zero or
more times), press "Add another form type", give it its own anchor text and page count, set Kind to
"Extra form", and define its fields the same way. Its columns appear in the CSV after the main form's,
repeated for as many copies as "Max copies in CSV" allows.

**A value with no label.** Switch Mode to "Drag = add box field" and drag a rectangle around the value on
the sample. Everything inside that rectangle, at that place on that page of the form, becomes the field.

---

## 3. Run a folder

On the **2. Run the folder** tab:

1. **Choose folder.** Pick the folder of records. Subfolders are included. The count of PDF files appears.
2. **Files at once.** 3 is a good default. Raise it on a fast computer, lower it if the computer struggles.
3. **Start.** The counters show files done, read cleanly, read with fields missing, needing OCR, and
   unreadable, plus the rate and the time left. The log lists every file that was not read cleanly, with
   the reason.
4. **Pause** at any time. Closing the tab or putting the computer to sleep loses nothing: choose the same
   folder again and press Start, and files already done are skipped. Tick "Re-read files already done" to
   force a fresh pass, for example after changing the template.

Expect tens of files per second on typed-text PDFs. Scanned records with an OCR layer are the same speed:
the tool reads the text layer, not the image.

---

## 4. Get the results

On the **3. Results** tab:

- **records.csv**: one row per record that held the main form, plus the columns `file`, `pages`,
  `main_form_page` and `status`. With two main form types, or a counter-ended form, three more:
  `form_type` (which main form page 1 matched), `main_form_pages` (for example `1-14`), `page_furniture` (what was set aside as repeated header and footer text on the main form's pages, in counts
  only, and which fields were read from it anyway), `form_type_basis` (what page 1 showed for each main form type: where its anchor was, how many of its
  labels, whether there was an outline, and what the sample taught), `form_end_check` (what confirms where the main form ends: "agrees" or
  "differs: counter N, stated M" against "Last page from", "count complete", "followed anchor", "counter not
  read", "stated pages not read", or "counter only" when nothing else confirms it) and `page_map`, which
  says what every page of the packet was read as, for example `1-14 Long form; 15-17 other; 18 Deficiency 1;
  19-40 other`. A wrong cut shows up there without opening the PDF. It opens in Excel directly and shows non-English text correctly. A long
  field keeps its paragraph breaks inside the cell. Excel shows at most 32,767 characters in one cell; the
  CSV holds the whole text, and any record with a longer field is listed in problems.csv.
- **problems.csv**: every file that was not read cleanly, with the problem and the detail. Problems are:
  "could not open" (corrupt, empty or password-protected), "no text layer (needs OCR)", "main form not
  found" (the anchor or labels were not seen), "required fields empty", and "tool error while reading",
  which is a bug to report, not a bad file.
  Packet notes, also in problems.csv (the record is still read): "form type unclear" (the two main form
  types scored close on page 1, or the form chosen on its anchor does not match page 1's labels and outline,
  or the reverse; the note says in words which form page 1 fits), "anchor not read on page 1" (found on page 2 instead), "page counter
  inferred" or "page counter bridged" (a page whose counter could not be read was counted in from its
  neighbours), "page counter stopped" (a count stopped before its total, a page with no readable counter
  ended the form, or a bare page number jumped to a number that neither continues the count nor starts a new
  one, so it may be cut short), "main form read as one page" (its first page's counter was not
  continued on the next page: check both on the sample's page line), "form end unclear" (the counter and the
  "Last page from" field disagree), "value continues past the form" (a value ran off the foot of a counted form's last page; the text on the
  next page was not added), and "table may continue" (a table reached the foot of a page and the next page
  has no heading row, so rows there were not read; also written for the page after the last page read for
  the table, unless that page's counter reads 1). Notes about an extra form name it after the kind of
  note, for example `page counter inferred: Deficiency on page 18: ...`, so the problem column can be
  filtered by kind. Also: "span followed the anchor" (the counter could not be read, so a main form whose
  anchor is printed at the top or bottom of each page was followed by that anchor; the note says which pages
  and where it ended; a page that prints the anchor only on another line ends it), "values from the anchor run"
  (the fields read from pages the main form took by following its anchor rather than its counter, each with its
  pages: check those first), "main form starts mid-count" (its first page reads, say, 3 of 5, so earlier pages may be
  missing), "page counter not read" (copies of an extra form whose counter could not be followed, each read as
  one page), "extra form inside the anchor run" (an extra form started on a page the main form took by
following its anchor, so it was not read), "extra form inside the main form" (an extra form's title is printed at the top of a
page inside the main form's count, so the form may run on past its end) and "copies not written" (more copies than Max copies: records.csv holds the first ones,
  tables.csv all of them).
- **needs-ocr.txt**: the paths of files with no text layer. Run them through Acrobat Pro (Scan & OCR,
  Recognize Text, in a batch action), then run the folder again: only those files will be re-read.
- **record-text.jsonl**: optional, the main form's text per record, for a search index.
- **tables.csv**: one row per table row, for every table field (see section 5): file, form, table, row number,
  page, then the columns. It continues a table onto later pages of the form where its heading row repeats; a page without the heading
  row is not read, and problems.csv says "table may continue" when that may have cut a table short.
- **record-chunks.jsonl**: optional, the records cut up for an AI assistant's search index (retrieval) at
  three zoom levels: the whole record, each field, and paragraph-sized pieces of long fields. Every line says
  which file, form, field and pages it came from, and points to the level above it, so an assistant that
  finds one paragraph of a description can widen to the whole field or the whole record. Give this file,
  not the CSV, to a retrieval tool.

When you have downloaded what you need, press **Erase saved results from this browser**. The downloaded
files are not affected.

---

## 5. The field-name syntax

Type one field per line under Fields by name. Case, spacing and punctuation do not matter: "work item no"
finds "WORK ITEM NO.", "12. Work Item No:" and "Work Item No ........".

| You type | It means |
|---|---|
| `Date Completed` | the label Date Completed, anywhere on the form; the value beside it or below it |
| `Contract No \| Contract Number` | either spelling |
| `Control Number *` | required: a record without it is listed in problems.csv |
| `Approved By > Date` | the Date inside the Approved By block (the block is the heading's drawn cell, or its column) |
| `Job Number = Job Control Number` | CSV column "Job Number", read from the label "Job Control Number" on this form type |
| `table Material List: Item; Part Number; Qty; Description` | a table found by its column headings; its rows go to tables.csv (one CSV row per table row) and its row count to records.csv. A column heading printed differently: `Part Number = P/N` |
| `Date #3` | the third Date on the form, counting across its pages |
| `# anything` | a comment line, ignored |

A box continued on later pages under its title plus "(cont.)", "cont'd" or "continued" is read whole,
including everything on the continuation pages.

---

## 6. Reading the page display

- **Thin blue outline**: a piece of text. Hover to see it. Click it to set the anchor or add a label field,
  depending on Mode.
- **Green outline**: text that starts with one of your labels.
- **Orange outline**: the anchor text.
- **Red lines**: drawn lines the tool found. Everything between them is a cell. Values are read within
  their own cell.
- **Hatched**: a running header or footer, ignored, except that a field the template names, a box field and a
  table heading are still read from it (with a page counter rule or two main form types). On the sample this is decided over the pages read so far,
  so it can change as more pages are read; a run decides it over the whole file.
- **Blue fill**: text that differs between the compared records, that is, a value.
- **Dashed blue box**: a box field.

With compared records, the page line says how many have a page that lines up with this one. If it says none,
nothing on the page is tinted, which does not mean the page has no values.

"Show lines and headers/footers" turns the red lines and the hatching off if they get in the way.

---

## 7. When a value comes out wrong

| What you see | What to do |
|---|---|
| Auto-detect left out a label printed on every record | The message after Auto-detect lists it. If it says what the other records read, your sample's text layer misread it: type the label as the other records read it in the list under Fields by name. |
| A field reads "(not found)" | Under the page counter rule, press "Where does this form end?" to see the pages the form covers (Pages per form applies only to the pages rule). Otherwise spell the label as printed, or add the printed spelling with `\|`. Check the anchor and Pages per form: the label may be on a page outside the form's span. |
| Two neighbouring labels' values run together, or a value takes the next cell's text | Look at the red lines on that page. If a line is missing, the scan's line is too faint for the tool to find; say so and the threshold can be adjusted. If there are no red lines at all, the form has no drawn cells and the value is read by gaps. |
| A value stops at a numbered line inside a box ("2.1 Location: ...") | Make sure the page's red lines enclose the box; inside a cell nothing cuts a value short. |
| The description reads only the first page | Check that the continuation pages carry the title with a "(cont.)"-style marker and that Pages per form covers them. |
| A value stops at the foot of a page and goes on overleaf | With a page counter rule, a header or footer that reads the same on the next page no longer stops it. If it still stops, the footer reads differently on the two pages (a scan misread), or the next page starts with a line shaped like a label ("Word words:"), which is read as a new field. A box title marked "(cont.)" is followed either way. |
| A field printed in the page header or footer reads blank | With a page counter rule or two main form types, a field whose label is printed in the top or bottom 12% of the page, and any box field, is read even when that text repeats; `page_furniture` names it. With an older template, untick "Ignore repeated page headers and footers" (this puts every header and footer back into values). |
| Header or footer text appears inside a value | Tick "Ignore repeated page headers and footers" (on by default). It needs the header to repeat on at least half of the pages of a record of three or more pages. |
| A field in the page header is ignored | Untick "Ignore repeated page headers and footers". |
| Date reads from the wrong signature block | Use `Approved By > Date`, or `Date #3`. |
| A record is read as the wrong main form type | Read the "form type unclear" note and the `form_type_basis` column: they say which form page 1's labels and outline fit. Open that record's page 1 on the sample and check the form number; if it was quoted in a sentence, or lost by the scan, the note says so. Adding a label only that form has on page 1 helps. |
| The main form is cut too early or too late | On the sample, press "Where does this form end?": it says which pages it would take and why it stops. Check the counter on the sample's page line for the last page and the next page. "form end unclear" in problems.csv means the counter and the "Last page from" field disagree. |
| A label is cut short ("TOT" for "TOTAL HOURS") | On a boxed form the lines fix this; without lines, add the printed first line as an alternate spelling (`Total Hours \| TOTAL`). |
| needs-ocr for a file that has text | The text layer is on fewer than half the pages. OCR the file anyway, or report it. |
| "tool error while reading" | A bug. Note the file's page count and layout in general terms and report it. |

Nothing in the template or the problem list identifies a record, so both can be shared freely. The CSVs
and record-text.jsonl hold record content and stay where the records are.

---

## 8. Versions

The page's version is in its header comment (open the file in a text editor, first lines of the script)
and in the dashboard log. Every version is kept; a template made with an earlier version loads unchanged.

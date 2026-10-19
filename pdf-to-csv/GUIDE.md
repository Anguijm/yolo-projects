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
   continues onto. Err on the high side.

4. **Page through the form** with the arrows, once, so the drawn lines of every page are remembered. Each
   page you look at is stored in the template. You only need to do this on the sample.

5. **Auto-detect labels on this page.** Press it on each page of the form. It adds a field for every label
   it finds. A label that appears in several blocks (Name, Date, Phone under four signature headings) is
   added as "PREPARED BY > Name", "REVIEWED BY > Name" and so on, one per block.

6. **Compare with more records.** Optional but recommended: choose one to four more records of the same
   form. Text that reads the same in every record is a label, text that differs is a value. Values turn
   blue on the page. Press Auto-detect again afterwards: it now keeps labels the type size alone could not
   prove and drops short values it might have mistaken for labels.

7. **Check the Fields table.** The "Value from sample" column shows what each field reads from the sample.
   This is the real test. Rename fields by editing the Name box (that becomes the CSV column heading), tick
   "Req" for fields that must be present, and remove fields you do not want with the x.

8. **Fix what reads wrong.** The list under Fields by name is the same template as text; edit it there and
   press "Use these field names". See section 5 for the syntax and section 7 for common fixes.

9. **Save template file.** Downloads `pdf-to-csv-template.json`. Keep it with the records. Next time, "Load
   template file" brings everything back, drawn lines included. The template holds field names, labels,
   box positions and the sample's line positions, never any record content.

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
  `main_form_page` and `status`. It opens in Excel directly and shows non-English text correctly. A long
  field keeps its paragraph breaks inside the cell. Excel shows at most 32,767 characters in one cell; the
  CSV holds the whole text, and any record with a longer field is listed in problems.csv.
- **problems.csv**: every file that was not read cleanly, with the problem and the detail. Problems are:
  "could not open" (corrupt, empty or password-protected), "no text layer (needs OCR)", "main form not
  found" (the anchor or labels were not seen), "required fields empty", and "tool error while reading",
  which is a bug to report, not a bad file.
- **needs-ocr.txt**: the paths of files with no text layer. Run them through Acrobat Pro (Scan & OCR,
  Recognize Text, in a batch action), then run the folder again: only those files will be re-read.
- **record-text.jsonl**: optional, the main form's text per record, for a search index.
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
- **Hatched**: a running header or footer, ignored.
- **Blue fill**: text that differs between the compared records, that is, a value.
- **Dashed blue box**: a box field.

"Show lines and headers/footers" turns the red lines and the hatching off if they get in the way.

---

## 7. When a value comes out wrong

| What you see | What to do |
|---|---|
| A field reads "(not found)" | Spell the label as printed, or add the printed spelling with `\|`. Check the anchor and Pages per form: the label may be on a page outside the form's span. |
| Two neighbouring labels' values run together, or a value takes the next cell's text | Look at the red lines on that page. If a line is missing, the scan's line is too faint for the tool to find; say so and the threshold can be adjusted. If there are no red lines at all, the form has no drawn cells and the value is read by gaps. |
| A value stops at a numbered line inside a box ("2.1 Location: ...") | Make sure the page's red lines enclose the box; inside a cell nothing cuts a value short. |
| The description reads only the first page | Check that the continuation pages carry the title with a "(cont.)"-style marker and that Pages per form covers them. |
| Header or footer text appears inside a value | Tick "Ignore repeated page headers and footers" (on by default). It needs the header to repeat on at least half of the pages of a record of three or more pages. |
| A field in the page header is ignored | Untick "Ignore repeated page headers and footers". |
| Date reads from the wrong signature block | Use `Approved By > Date`, or `Date #3`. |
| A label is cut short ("TOT" for "TOTAL HOURS") | On a boxed form the lines fix this; without lines, add the printed first line as an alternate spelling (`Total Hours \| TOTAL`). |
| needs-ocr for a file that has text | The text layer is on fewer than half the pages. OCR the file anyway, or report it. |
| "tool error while reading" | A bug. Note the file's page count and layout in general terms and report it. |

Nothing in the template or the problem list identifies a record, so both can be shared freely. The CSVs
and record-text.jsonl hold record content and stay where the records are.

---

## 8. Versions

The page's version is in its header comment (open the file in a text editor, first lines of the script)
and in the dashboard log. Every version is kept; a template made with an earlier version loads unchanged.

# Prompts for gen.ai.mil: how to tell the forms apart, page to page

Use these with a few sample packets inside the environment. They ask the model to describe what a
PROGRAM could measure, not what a person notices, and to answer without any record content, so the
answers can come back to the developer if security agrees. Whether anything leaves is your call.

Suggested samples: 2 short-form packets and 2 long-form packets, the more ordinary the better.
Run Prompt 1 once per packet, Prompt 2 once with all of them, Prompt 3 once with all of them, then Prompt 4
on the whole conversation.

---

## Prompt 1: map one packet, page by page

```
I am building an offline tool that reads scanned work-package PDFs (scanned pages with an OCR text layer)
and extracts fields into a CSV. Each PDF is a packet: a main form first (either a "short form" or a
"long form"), then other documents (attachments, supplementary forms, other pages). I need to know how a
PROGRAM can tell where the main form ends and what each later page is.

The program can only measure these things on each page:
- each piece of text in the OCR layer, its position on the page and its type size (not font names);
- drawn lines and boxes visible in the image;
- how much text the page has and where the text block's margins are;
- text that repeats near the top or bottom of pages (running header and footer), with digits ignored;
- page numbering such as "Page 3 of 12" and where it restarts;
- the order in which labels and headings appear.

For the attached packet, give me a table with one row per page and these columns:
page | what it is (main form first page / main form continuation / attachment / supplementary form / other)
| header present (yes/no, and is it the SAME header as the previous page) | footer same as previous page
| page numbering (e.g. "n of N" restarts here, continues, none) | drawn boxes (none / few / grid)
| text amount (low / medium / high) | margins same as previous page (yes/no) | type size of body text
same as previous page (yes/no) | what changed from the previous page, in measurable terms.

Then answer: at the page where the main form ends, which of the measurable signals above change, and
which stay the same? Which signal would be most reliable to detect that boundary, and which would mislead?

Rules for your answer: describe layout and structure only. Do not quote any names, numbers, dates,
locations, descriptions or other content from the records. Label names and form titles may be described
generically ("a form number in the top right", "a bold section heading") rather than quoted.
```

## Prompt 2: short form versus long form

```
Using all the attached packets: some begin with a short form and some with a long form. The short form has
an anchor text at the top of every page. The long form was written in Word and looks similar, but its
fields differ.

1. On the FIRST page of the main form, list the measurable differences between short and long form
   (layout, drawn boxes, header/footer, type sizes, where the title sits, label shapes such as
   "Label:" vs label above a box, numbered items). Rank them by how reliably a program could use them.
2. On a CONTINUATION page (page 2 onward), how can a program tell a long-form page from a short-form page,
   and a long-form page from an attachment that follows it?
3. Does the long form have anything printed on every one of its pages (header, footer, form number,
   classification line, page numbering, a revision date)? Describe its position and shape, not its text.
4. Are the long form's field labels always in the same order from packet to packet, even when the pages
   break differently? Do any long-form labels appear again on attachment pages (for example Name, Date,
   Signature)? Which ones, in generic terms?
5. For each of these, how confident are you, and what would you need to see to be sure?

Same rules: structure only, no record content, no quoted names, numbers or dates.
```

## Prompt 3: what a program would get wrong

```
Imagine a simple program that decides where the main form ends using these rules:
(a) the short form ends when its top-of-page anchor stops appearing;
(b) the long form ends at the first page, after its last recognised field label, where the running header
    or footer changes, the page numbering restarts, the margins or body type size change, or the amount of
    text changes sharply.
On the attached packets, where would rules (a) and (b) cut correctly, and where would they cut too early or
too late? For each wrong cut, say which page, which rule fired or failed to fire, and what extra signal
would have fixed it. Also say whether any packet has the main form interrupted by other pages (an
attachment inserted in the middle) or more than one main form.

Same rules: structure only, no record content.
```

## Prompt 4: clean summary to bring back

```
Summarise everything we found in this conversation as a short, generic report for a software developer
who must never see these records. Include: how the short and long form differ on the first page and on
continuation pages; what is printed on every page of each; what changes at the end of the main form; the
signals ranked by reliability; where the simple rules (a) and (b) fail; and any oddities (interrupted
forms, repeated labels in attachments, unusual page sizes or rotations).
Remove anything that could identify a record, a person, a place, a unit, a date or a job: no quotations,
no numbers from the records, no names. Generic descriptions only, such as "a bold title centred at the
top" or "a footer with page numbering at the bottom right". If a finding cannot be stated without record
content, leave it out and say that something was left out.
```

---

## Tips
- If the model can only see the page images and not the OCR text layer, ask it to say so: what it sees and
  what the OCR layer holds can differ, and the tool reads only the OCR layer.
- Prompt 4's report is what helps most. Read it yourself before it goes anywhere.
- Pair it with what v0.7 shows on screen for the same packets: red lines found, hatched header/footer,
  and the "Value from sample" column.

# svg-fields

Drop an SVG template, fill in its fields in a left-hand column, get a populated SVG back.

## Run

```
open svg-fields/index.html
```

Single-file HTML, no build step. Works offline.

## What it does

- **Left panel**: auto-generated form, one input per field, in document order
- **Right panel**: live preview that re-renders as you type
- **Download**: exports the populated SVG as `populated.svg`

## Field markers

Two supported styles (you can mix them in the same SVG):

1. **Mustache placeholders** anywhere in text:
   ```svg
   <text>{{recipient_name}}</text>
   ```

2. **Data-field attributes** on `<text>` elements:
   ```svg
   <text data-field="signatory_title">Instructor</text>
   ```

Same field name appearing multiple times counts once in the form but updates every occurrence in the preview. The form shows `×N` next to labels that appear more than once.

## Shortcuts

- `Ctrl+O` — open file
- `Ctrl+S` — download populated SVG
- Drag/drop an SVG onto the preview
- Paste SVG from clipboard

## Example

Click **sample** to load a certificate template with 5 fields (recipient_name, course_title, completion_date, instructor_name, director_name) plus one data-field (signatory_title).

## Why

Any SVG that's essentially "layout plus a few strings" becomes a reusable template. Most common use: certificates, invoices, labels, badge templates, form SVGs.

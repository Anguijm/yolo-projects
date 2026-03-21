# File Treemap

Scan any directory and visualize disk usage as an interactive, drillable treemap.

## How to run

```bash
python3 file_treemap.py ~/some/directory
```

Generates an HTML file you open in a browser. Click directories to drill in, press Backspace to go up.

## What you'd change

- Add file type filtering
- Add "what's taking up space" sorted list alongside the treemap
- Add delete button for large files (with confirmation)

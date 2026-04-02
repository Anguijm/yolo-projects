# git-resolve

Interactive git merge conflict resolver in a single HTML file.

## What it does

Paste a file containing git conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), and the tool parses each conflict block into a side-by-side diff view. For each conflict you can:

- **Accept Ours** -- keep the HEAD version
- **Accept Theirs** -- keep the incoming branch version
- **Accept Both** -- concatenate both versions

Bulk actions ("Accept All Ours" / "Accept All Theirs") resolve every conflict at once. Once all conflicts are resolved, the clean output is generated automatically.

## Usage

1. Open `index.html` in a browser
2. Paste a file with conflict markers into the textarea (or click "Load Sample" for a demo)
3. Click "Parse Conflicts"
4. Choose Ours / Theirs / Both for each conflict block
5. Copy the resolved output

## Features

- Zero dependencies, single HTML file
- Dark industrial aesthetic (YOLO design system)
- Mobile-responsive (375px+ with stacked diff view)
- Context lines shown between conflicts for orientation
- Auto-generates resolved output when all conflicts are chosen
- Sample conflict included for quick testing

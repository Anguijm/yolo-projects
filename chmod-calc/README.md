# chmod-calc

Unix file permission calculator. Toggle checkboxes ↔ type octal ↔ see symbolic. Bidirectional sync.

## What it does

- **3 representations synced live**: octal (644), symbolic (rw-r--r--), and checkbox grid
- **Special bits**: setuid (4000), setgid (2000), sticky (1000) — colored differently in symbolic output
- **Numeric breakdown**: shows each octet digit (special / owner / group / others) highlighted when non-zero
- **chmod command line**: `chmod 644 <filename>` — copy it directly
- **Human description**: plain English explanation of what the permissions allow
- **12 presets**: 644, 755, 700, 600, 750, 640, 777, 666, 444, 400, 4755, 1755
- **Colored symbolic notation**: read=green, write=amber, execute=blue, special=red/magenta

## How to run

Open `index.html` in a browser. No server needed.

## Stack

Single HTML file, zero dependencies, no external resources.

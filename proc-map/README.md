# proc-map

A process visualization tool that snapshots all running processes and generates an interactive HTML force-directed graph showing parent-child relationships.

## Features

- Force-directed graph of all running processes with parent-child edges
- Node size proportional to memory usage (RSS)
- Node color indicates CPU usage (cool blue to hot red)
- Hover tooltips with PID, command, user, CPU%, MEM%, uptime
- Click any node to highlight its full process tree branch (ancestors + descendants)
- Sidebar with a sortable/filterable process table
- Search by process name, user, PID, or command arguments
- Single self-contained HTML file output, no web server needed

## Requirements

- Python 3.6+
- Linux (uses `ps` and `/proc` filesystem)
- Zero external dependencies (stdlib only)

## Usage

```bash
python3 proc_map.py
```

This produces `proc_map.html` in the same directory. Open it in any modern browser.

To specify a custom output path:

```bash
python3 proc_map.py /path/to/output.html
```

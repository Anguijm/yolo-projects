# log-lens

Browser-based log file viewer and analyzer. Paste or drop server logs and get instant colorized output, filtering, timeline histogram, and top error grouping — no server required.

## Features

- **Auto-detect format**: nginx access, Apache combined, syslog, JSON lines, generic timestamped, plain text
- **Severity coloring**: ERROR (red), WARN (amber), INFO (green), DEBUG/TRACE (grey)
- **Sidebar filters**: toggle severity levels independently, live text search with optional regex mode
- **Timeline canvas**: stacked frequency histogram by severity over time, hover for event counts, click to jump to that point in the log
- **Top errors panel**: groups similar error/warn messages by normalized pattern, click to search
- **Stats header**: total count, per-severity counts, time span
- **File input**: drag-and-drop, file picker, or paste modal (Ctrl+Enter to analyze)
- **Wrap/nowrap toggle**: switch between compact single-line and full message display
- **Presets**: nginx, syslog, JSON lines, Apache, mixed/plain sample logs

## Usage

Open `index.html` in any browser. No server or build step needed.

1. Drop a `.log` / `.txt` / `.json` file onto the window, or click **Load File**
2. Or click **Paste** and paste raw log text, then hit Ctrl+Enter
3. Or click a preset to load sample data
4. Use the sidebar to filter by severity and search text
5. Click the timeline to jump to a time window

## Supported Formats

| Format | Example |
|--------|---------|
| Nginx/Apache access | `192.168.1.1 - - [15/Jan/2024:10:00:01 +0000] "GET / HTTP/1.1" 200 1234` |
| Syslog | `Jan 15 10:00:01 host sshd[123]: Accepted publickey for user` |
| JSON lines | `{"timestamp":"2024-01-15T10:00:01Z","level":"ERROR","msg":"failed"}` |
| Generic timestamped | `2024-01-15 10:00:01 ERROR Failed to connect` |
| Plain text | Any text — severity detected from keywords |

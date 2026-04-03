# sql-explain

SQL formatter + plain-English query explainer. Paste any SQL query and get:
- **Formatted SQL** with syntax highlighting (keywords, strings, numbers, comments colored)
- **Plain-English explanation** breaking down SELECT columns, source tables, JOINs, filters, grouping, sorting, and limits

Runs entirely in the browser — no server, no data sent anywhere.

## How to run

Open `index.html` in any browser. No build step, no dependencies.

## Features

- Formats messy SQL: capitalizes keywords, adds clause line breaks, handles AND/OR indentation
- Detects query type: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, WITH (CTE)
- **Safety warnings**: flags UPDATE/DELETE statements missing a WHERE clause
- Warns on `SELECT *` (suggests explicit columns)
- Handles single-quoted strings, double-quoted identifiers, backtick identifiers
- Line comments (`--`) and block comments preserved in formatter
- Keyboard shortcut: `Ctrl+Enter` to format
- Copy formatted SQL to clipboard

## What to change

- Add SQL dialect selector (PostgreSQL/MySQL/SQLite) for dialect-specific keywords
- Add formatting options (indent size, comma placement)
- Improve formatter to handle nested subqueries with proper indentation levels

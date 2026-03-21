# HTTP Playground

A beautiful REST client in a single HTML file. Mini Postman with zero dependencies, zero install. Drop it anywhere, open it, send requests.

## Features

- Methods: GET, POST, PUT, DELETE, PATCH (color-coded)
- Request tabs: Headers (JSON or key:value), Body, Query Params, History
- Response tabs: Syntax-highlighted JSON Body, Headers, Raw
- Custom JSON highlighting (keys/strings/numbers/booleans/null)
- Status badge (2xx/3xx/4xx/5xx color-coded)
- Response timing in milliseconds
- CORS Proxy toggle (routes through corsproxy.io with security warning)
- Pretty Print toggle
- Auto-save to localStorage (URL, method, headers, body, history)
- Request history (last 50, clickable to reload)
- Copy response to clipboard
- 5 built-in presets: Random Joke, Pokemon, Create Post, Users List, HTTPBin
- Keyboard: Ctrl/Cmd+Enter = Send
- XSS-safe escaping
- GitHub-dark theme

## How to Run

Open `index.html` in a browser. Click a preset or type a URL.

## What You'd Change

- Request collections (save named groups of requests)
- Environment variables ({{base_url}}, {{token}})
- cURL import/export
- WebSocket support

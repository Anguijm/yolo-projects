# API Mocker

Define mock API endpoints in a browser UI, get a running server instantly. Supports path params, custom status codes, response delays, and a live request log.

## How to run

```bash
python3 api_mocker.py
```

Opens `http://localhost:8800` with an admin UI. Define endpoints there, then point your frontend at the same host.

## What you'd change

- Add response templating (dynamic values, random data)
- Add import/export endpoint configs as JSON
- Add proxy mode (forward unmatched requests to a real API)

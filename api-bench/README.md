# api-bench

Browser-based API endpoint load tester. Fire N parallel requests at a URL, measure latency percentiles, throughput, and status distribution — like a mini k6/wrk, but zero-install in the browser.

## Features

- **Configurable load**: 1–500 requests, 1–50 concurrent workers, per-request timeout
- **Real-time progress**: live progress bar with running avg latency, error count, and req/s
- **Latency stats**: min, avg, median (p50), p95, p99, max
- **Canvas histogram**: 20-bin latency distribution, color-coded by p95/p99 thresholds, dashed percentile marker lines
- **Status distribution**: per-code bar chart, color-coded (2xx green / 3xx blue / 4xx amber / 5xx red)
- **Error log**: grouped CORS/network/timeout error counts
- **Headers + body**: collapsible panel for custom JSON headers and request body (any method except GET/HEAD)
- **Presets**: 6 ready-to-run scenarios (httpbin GET, POST, delay, mixed statuses, JSONPlaceholder, high concurrency)

## Usage

Open `index.html` in any modern browser. No server required.

1. Pick a preset or enter a URL
2. Set request count, concurrency, and timeout
3. (Optional) expand Headers & Body for custom request config
4. Click **Run**

## Limitations

- Target URL must allow CORS from the browser's origin
- Browser fetch is not a low-level TCP tool — measured latency includes browser overhead
- Concurrency is capped at 50 (browser connection limits apply above that)
- Not a replacement for server-side tools (k6, wrk, hey) for high-throughput testing

## Design

Single HTML file, zero dependencies. Follows the YOLO industrial/terminal design system.

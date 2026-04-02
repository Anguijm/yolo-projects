# DNS Lookup

Browser-based DNS record lookup and visualization tool using DNS-over-HTTPS (DoH).

## Features

- Query A, AAAA, MX, NS, TXT, CNAME, and SOA records for any domain
- Two DoH providers: Cloudflare and Google
- Color-coded record type badges
- TTL display for each record
- Mobile-friendly (375px minimum width)
- Zero external dependencies, single HTML file

## Usage

Open `index.html` in a browser. Enter a domain name and click Lookup (or press Enter). Switch between Cloudflare and Google DoH providers using the buttons above the input.

## How It Works

Queries are sent to either Cloudflare's or Google's public DNS-over-HTTPS JSON API endpoints. Each record type is queried in parallel and results are displayed in a table grouped by type.

## Design

Dark industrial aesthetic per the YOLO design system. Monospace typography, ghost buttons, sharp corners, compact layout.

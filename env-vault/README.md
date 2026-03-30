# env-vault

Browser-based `.env` file manager. Parse, organize, inspect, diff, and encrypt environment variable files — entirely in the browser with zero dependencies.

## Features

- **Parse .env format** — KEY=VALUE, comments (#), blank lines, quoted values, inline comments
- **Visual grouping** — auto-groups by prefix (DB_, AUTH_, API_, APP_, REDIS_, S3_, SMTP_) or catches everything else in MISC
- **Secret visibility** — secrets (keys matching PASSWORD, TOKEN, KEY, SECRET, etc.) hidden by default with per-variable reveal toggle
- **Diff mode** — paste two .env files side-by-side, see added/removed/changed/same keys with color coding
- **Multiple export formats** — `.env`, JSON, docker-compose `environment:` block, shell `export` statements
- **AES-256-GCM encryption** — encrypt vault to a JSON blob using PBKDF2-HMAC-SHA256 (600k iterations), decrypt and re-import
- **Presets** — Node.js, Django, PostgreSQL, Redis+Queue, AWS/S3 sample configs
- **Inline editing** — click any key or value to edit in place, Enter to save, Escape to cancel

## Usage

Open `index.html` in any modern browser. No server, no install.

### Vault Tab
- Displays all variables grouped by prefix
- Click a key to rename it, click a value to edit it
- Use the add row at the bottom of each group to insert new variables
- Toggle "secrets hidden" button to show/hide all secret values at once

### Import Tab
- Paste any `.env` content and click **import** (replaces vault) or **merge** (adds new keys only)
- Use presets to load sample configurations

### Diff Tab
- Paste two `.env` files into the A/B panels — diff runs live as you type
- Color coding: green = added, red = removed, amber = changed, dim = unchanged
- Toggle "hide unchanged" to focus on differences

### Export Tab
- Choose format (.env, JSON, docker-compose, shell) and copy or download
- AES encryption: enter a passphrase, click **encrypt + copy** to get a portable encrypted blob
- To restore: paste the blob, enter the same passphrase, click **decrypt + import**

## Security Notes

- Nothing leaves the browser — no network requests, no localStorage persistence
- Encryption uses `window.crypto.subtle` (requires HTTPS or localhost)
- 600,000 PBKDF2 iterations per OWASP recommendation
- AES-256-GCM provides authenticated encryption (tamper detection)

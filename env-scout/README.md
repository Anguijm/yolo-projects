# env-scout

**.env file auditor** — finds missing keys, extra undocumented vars, and security risks in your template.

## What it does

Paste your `.env` file and your `.env.example` template side by side. env-scout shows:

- **Missing** — keys in the template not present in your `.env` (new developer will be missing these)
- **Extra** — keys in your `.env` not documented in the template (undocumented vars, potential drift)
- **Security Warnings** — template entries that look like real secret values (committed by accident)

Additional features:
- **Generate Template** — auto-creates a `.env.example` from your `.env` with smart placeholders (`https://example.com`, `your-api-key-here`, etc.)
- **Copy Report** — plain-text summary for pasting into tickets or PRs
- **Swap** — flip env and template to check the other direction
- 4 presets: Stale Template, Missing Keys, In Sync, Security Risk
- Auto-audit as you type (500ms debounce), Ctrl+Enter to force

## How to run

Open `index.html` in a browser. No server needed.

## Type inference

env-scout infers value types and uses them for smart placeholder generation:

| Type | Detection | Placeholder |
|------|-----------|-------------|
| url | contains `://` | `https://example.com` |
| email | contains `@` with dot after | `user@example.com` |
| port | all digits + key contains PORT | keeps port number |
| bool | true/false/yes/no/on/off | `false` |
| integer | all digits | `0` |
| jwt | 3 base64-ish segments with dots | `your-jwt-token` |
| hex | 16+ hex chars | `your-hex-secret` |
| path | starts with `/` or `./` | `/path/to/resource` |
| string | everything else | `your-KEY-NAME-here` |

# Secure Note

A locally encrypted notepad. AES-256-GCM encryption, PBKDF2 key derivation, auto-lock on tab switch. No server, no cloud, no account. Your notes, truly private.

## Features

- AES-256-GCM authenticated encryption via Web Crypto API
- PBKDF2 key derivation with 600,000 iterations (OWASP recommended)
- 16-byte random salt, 12-byte random IV (new IV per save)
- Non-extractable CryptoKey (can't be stolen by scripts)
- Password never stored — only encrypted payload in localStorage
- Minimum 8-character password for new notes
- Auto-save on keystroke (500ms debounce)
- Auto-lock on visibility change (tab switch, screen off)
- beforeunload warning for unsaved changes
- First-time setup vs returning user flow
- Wrong password → graceful decryption failure message
- Clear notes with confirmation
- autocomplete="new-password" prevents browser password saving
- OLED black, mobile-first, all PWA metas
- Click events only, no pointerdown

## Security Properties

- AES-GCM provides both confidentiality AND integrity (tampered ciphertext fails to decrypt)
- Random IV per save prevents nonce reuse
- PBKDF2 at 600K iterations slows brute-force attacks
- Non-extractable key prevents JS-level key theft
- Plaintext wiped from DOM on lock (editor.value = '')

## Improvements from Gemini Security Audit

- PBKDF2 iterations increased from 100K to 600K (OWASP recommendation)
- Minimum 8-character password enforced for new notes
- beforeunload warning prevents data loss on close
- autocomplete="new-password" prevents browser credential storage

## How to Run

Open `index.html` in a browser (HTTPS or localhost required for Web Crypto). Set a password, start writing.

## What You'd Change

- Export/import encrypted blob as file
- Multiple named notes (vault)
- Inactivity timeout auto-lock
- Panic password that wipes data

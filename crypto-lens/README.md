# Crypto Lens

Visual cipher explorer. Type a message, apply Caesar, Vigenere, or XOR encryption, and watch the transformation happen character by character. Step through to see the exact math at each position.

## Features

- 3 cipher types: Caesar (shift), Vigenere (polyalphabetic), XOR (bitwise)
- Step-by-step lens visualization showing the math for each character
- Caesar: shows modular arithmetic with shift value
- Vigenere: shows plaintext + key character alignment with mod 26 math
- XOR: shows binary bits side-by-side with per-bit XOR result
- Encrypt/decrypt toggle (bidirectional)
- Playback animation: auto-step through all characters
- Preserves original letter casing
- XOR output shown as hex + raw characters
- Dark terminal aesthetic, mobile-first

## How to Run

Open `index.html`. Type a message, select a cipher, adjust the key. Watch the lens visualization show how each character transforms. Use Prev/Next to step through or Play for animation. Toggle Encrypt/Decrypt to reverse.

# Ordinals Protocol Specification

## Overview

Ordinals theory assigns serial numbers to satoshis, enabling NFTs and arbitrary data inscription on Bitcoin.

## Ordinal Theory Basics

### Sat Numbering

Each satoshi has a unique ordinal number based on mining order:
- First sat of block 0: ordinal 0
- Total sats: 2,100,000,000,000,000

### Sat Rarity

| Rarity | Description | Supply |
|--------|-------------|--------|
| common | Any sat | ~2.1 quadrillion |
| uncommon | First sat of each block | ~6,929,999 |
| rare | First sat of difficulty adjustment | ~3437 |
| epic | First sat of halving | 5 (eventually 32) |
| legendary | First sat of cycle | 0 (eventually 5) |
| mythic | First sat of genesis block | 1 |

### Sat Tracking (FIFO)

Sats transfer using First-In-First-Out:
```
Input: [sat 100, sat 101, sat 102]
Output 1: 2 sats → [sat 100, sat 101]
Output 2: 1 sat  → [sat 102]
```

## Inscription Format

### Envelope Structure

Inscriptions use a taproot witness envelope:

```
OP_FALSE
OP_IF
  OP_PUSH "ord"           # Protocol marker
  OP_PUSH 1               # Content-type tag
  OP_PUSH <content_type>  # MIME type
  OP_PUSH 0               # End of metadata / start of body
  OP_PUSH <data_chunk_1>  # Content (max 520 bytes per push)
  OP_PUSH <data_chunk_2>  # Additional chunks if needed
  ...
OP_ENDIF
```

### Tags

| Tag | Meaning | Value |
|-----|---------|-------|
| 1 | content_type | MIME type string |
| 2 | pointer | sat offset to inscribe on |
| 3 | parent | parent inscription ID |
| 5 | metadata | CBOR-encoded metadata |
| 7 | metaprotocol | protocol identifier |
| 9 | content_encoding | e.g., "br" for brotli |
| 11 | delegate | delegate to another inscription |
| 13 | rune | Rune to etch (deprecated) |

### Content Types

Common MIME types:
```
text/plain;charset=utf-8     # Plain text, BRC-20
text/html;charset=utf-8      # HTML
image/png                    # PNG image
image/webp                   # WebP image
image/svg+xml                # SVG
application/json             # JSON data
audio/mpeg                   # MP3 audio
video/mp4                    # MP4 video
model/gltf-binary            # 3D model
```

### Size Limits

- Single push: 520 bytes max
- Total inscription: ~400KB practical limit
- Use content_encoding for compression

## Inscription ID

Format: `<txid>i<index>`

Example: `6fb976ab49dcec017f1e201e84395983204ae1a7c2abf7ced0a85d692e442799i0`

- txid: Transaction ID (hex, reversed byte order)
- i: Separator
- index: Inscription index within transaction (0-based)

## Creating Inscriptions

### Two-Phase Commit-Reveal

**Phase 1: Commit Transaction**
- Create output to taproot address
- Address commits to inscription content

**Phase 2: Reveal Transaction**
- Spend commit output
- Include inscription in witness
- Inscription bound to first sat of first input

### Code Example (Conceptual)

```javascript
// Using ord library or similar
const inscription = {
  contentType: 'text/plain;charset=utf-8',
  body: Buffer.from('Hello, Ordinals!'),
};

// Build envelope script
const envelope = [
  opcodes.OP_FALSE,
  opcodes.OP_IF,
  Buffer.from('ord'),
  opcodes.OP_1,           // content-type tag
  Buffer.from(inscription.contentType),
  opcodes.OP_0,           // body tag
  ...chunkData(inscription.body, 520),
  opcodes.OP_ENDIF,
];
```

## Recursive Inscriptions

Reference other inscriptions via `/content/<inscription_id>`:

```html
<html>
  <body>
    <img src="/content/abc123...i0" />
    <script src="/content/def456...i0"></script>
  </body>
</html>
```

## Parent-Child Inscriptions

Create collections with parent reference:

```
OP_FALSE
OP_IF
  OP_PUSH "ord"
  OP_PUSH 3               # Parent tag
  OP_PUSH <parent_id>     # Parent inscription ID (32 bytes)
  OP_PUSH 1
  OP_PUSH "image/png"
  OP_PUSH 0
  OP_PUSH <image_data>
OP_ENDIF
```

## Delegation

Point to another inscription's content:

```
OP_FALSE
OP_IF
  OP_PUSH "ord"
  OP_PUSH 11              # Delegate tag
  OP_PUSH <delegate_id>   # Inscription to delegate to
OP_ENDIF
```

Benefits:
- Save fees for duplicate content
- Create editions
- Update content pointers

## Metadata (CBOR)

Structured metadata using CBOR encoding:

```javascript
const metadata = {
  name: "My NFT",
  description: "A cool inscription",
  attributes: [
    { trait_type: "Background", value: "Blue" },
    { trait_type: "Rarity", value: "Rare" }
  ]
};

// Encode as CBOR, use tag 5
```

## Cursed Inscriptions

Inscriptions that violate protocol rules but still exist:
- Negative inscription numbers
- Created before certain rules
- May have special collector value

## Tools & Libraries

**ord (Rust CLI):**
```bash
ord wallet inscribe --fee-rate 10 --file image.png
```

**JavaScript:**
```javascript
// @ordjs/ord or similar
import { Inscription } from '@ordjs/ord';
```

**Indexers:**
- ord server (reference)
- Hiro ordinals API
- UniSat API
- OKX API

# Runes Protocol Specification

## Overview

Runes is a fungible token protocol on Bitcoin using OP_RETURN outputs. Unlike BRC-20, Runes are UTXO-native - token balances are tied to UTXOs, not ordinal theory.

Activated at Bitcoin block 840,000 (April 2024 halving).

## Key Concepts

### Rune ID

Format: `BLOCK:TX` (e.g., `840000:1`)
- BLOCK: Block height where rune was etched
- TX: Transaction index within that block

### Runestone

A Runestone is the protocol message in OP_RETURN:
- Max 80 bytes in OP_RETURN
- Uses LEB128 varint encoding
- Contains etching, edicts, mint info

## Operations

### Etch (创建代币)

Create a new Rune. Requires commitment transaction.

**Two-step process:**

1. **Commitment TX**: Include rune name commitment in witness
2. **Reveal TX**: Broadcast etching with OP_RETURN

**Etching fields:**
```
Runestone {
  etching: Some(Etching {
    rune: Some(Rune("UNCOMMONGOODS")),
    divisibility: Some(0),
    premine: Some(0),
    symbol: Some('⧉'),
    terms: Some(Terms {
      amount: Some(1),
      cap: Some(u128::MAX),
      height: (None, None),
      offset: (None, None),
    }),
    turbo: false,
  }),
  edicts: vec![],
  mint: None,
  pointer: None,
}
```

| Field | Description |
|-------|-------------|
| rune | Token name (A-Z only, 13+ chars initially) |
| divisibility | Decimal places (0-38) |
| premine | Amount premined to etcher |
| symbol | Display symbol (1 char) |
| terms.amount | Amount per mint |
| terms.cap | Maximum number of mints |
| terms.height | Block height range for minting |
| terms.offset | Block offset range from etch |
| turbo | Enable future protocol features |

**Name rules:**
- Only A-Z characters
- Minimum length decreases over time:
  - Block 840,000: 13+ characters
  - Decreases by 1 char every ~4 months
  - Eventually allows 1-char names

### Mint (铸造)

Mint existing Rune if mint terms allow.

```
Runestone {
  etching: None,
  edicts: vec![],
  mint: Some(RuneId { block: 840000, tx: 1 }),
  pointer: Some(0),  // Output to receive minted runes
}
```

**Rules:**
- Must be within height/offset range
- Must not exceed cap
- Amount per mint is fixed by terms

### Transfer (转账)

Use edicts to move runes between outputs.

```
Runestone {
  etching: None,
  edicts: vec![
    Edict { id: RuneId { block: 840000, tx: 1 }, amount: 1000, output: 1 },
    Edict { id: RuneId { block: 840000, tx: 1 }, amount: 500, output: 2 },
  ],
  mint: None,
  pointer: None,
}
```

| Field | Description |
|-------|-------------|
| id | Rune ID to transfer |
| amount | Amount to send to output |
| output | Output index (0-based) |

**Special values:**
- `amount: 0` = send all remaining balance
- `output` pointing to OP_RETURN = burn

### Pointer

Default destination for unallocated runes:
- If set: Unallocated runes go to pointer output
- If not set: Go to first non-OP_RETURN output
- Prevents accidental burns

## Encoding Details

### LEB128 Varint

```python
def encode_varint(n):
    result = []
    while n >= 128:
        result.append((n & 0x7F) | 0x80)
        n >>= 7
    result.append(n)
    return bytes(result)
```

### Runestone Structure

```
OP_RETURN OP_13 <encoded_runestone>
```

Tag-value pairs:
| Tag | Meaning |
|-----|---------|
| 0 | Body (edicts follow) |
| 1 | Flags |
| 2 | Rune name |
| 3 | Premine |
| 4 | Cap |
| 5 | Amount |
| 6 | Height start |
| 8 | Height end |
| 10 | Offset start |
| 12 | Offset end |
| 14 | Mint |
| 16 | Pointer |
| 20 | Cenotaph (invalid runestone marker) |
| 22 | Divisibility |
| 24 | Spacers |
| 26 | Symbol |
| 28 | Turbo |

## Cenotaph (无效铭石)

If runestone is malformed, it becomes a cenotaph:
- All input runes are burned
- Prevents protocol exploits
- Common causes: invalid encoding, unknown tags

## Libraries

**ord (Rust):**
```rust
use ordinals::{Rune, Runestone, Edict};
```

**JavaScript:**
```javascript
// runelib or @magiceden-oss/runestone-lib
import { Runestone, Edict } from 'runelib';
```

## Comparison: Runes vs BRC-20

| Aspect | Runes | BRC-20 |
|--------|-------|--------|
| Storage | OP_RETURN | Witness |
| Balance model | UTXO-native | Ordinal theory |
| Transfer | Single TX | Inscribe + Send |
| Fees | Lower | Higher |
| Indexer dependency | Lower | Higher |
| Ecosystem | Growing | Mature |

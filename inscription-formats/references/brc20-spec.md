# BRC-20 Protocol Specification

## Overview

BRC-20 is a fungible token standard on Bitcoin using Ordinals inscriptions. Tokens are represented as JSON inscriptions.

## Operations

### Deploy (创建代币)

Create a new BRC-20 token.

```json
{
  "p": "brc-20",
  "op": "deploy",
  "tick": "ordi",
  "max": "21000000",
  "lim": "1000",
  "dec": "18"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| p | Yes | Protocol identifier, must be `"brc-20"` |
| op | Yes | Operation, must be `"deploy"` |
| tick | Yes | Token ticker, exactly 4 bytes (UTF-8) |
| max | Yes | Maximum supply (string) |
| lim | No | Mint limit per inscription (string) |
| dec | No | Decimals, default 18, max 18 |

**Rules:**
- `tick` is case-insensitive for uniqueness check
- First valid deploy wins
- `max` and `lim` must be positive integers as strings

### Mint (铸造)

Mint tokens to the inscription owner.

```json
{
  "p": "brc-20",
  "op": "mint",
  "tick": "ordi",
  "amt": "1000"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| p | Yes | Protocol identifier |
| op | Yes | Must be `"mint"` |
| tick | Yes | Token ticker to mint |
| amt | Yes | Amount to mint (string) |

**Rules:**
- `amt` must be ≤ `lim` from deploy
- Total minted cannot exceed `max`
- Tokens go to first sat of inscription

### Transfer (转账)

Transfer tokens. Two-step process:

**Step 1: Inscribe transfer**
```json
{
  "p": "brc-20",
  "op": "transfer",
  "tick": "ordi",
  "amt": "100"
}
```

**Step 2: Send the inscription** to recipient address

| Field | Required | Description |
|-------|----------|-------------|
| p | Yes | Protocol identifier |
| op | Yes | Must be `"transfer"` |
| tick | Yes | Token ticker |
| amt | Yes | Amount to transfer (string) |

**Rules:**
- Must have sufficient balance
- Transfer inscription creates a "transferable" balance
- Sending the inscription executes the transfer
- If sent to self, returns to available balance

## BRC-20 Variants

### 5-byte Tickers (brc-20-5byte)

Extended ticker length for more token names:

```json
{
  "p": "brc-20-5byte",
  "op": "deploy",
  "tick": "sats5",
  "max": "21000000000000"
}
```

### 6-byte Tickers (Fractal Network)

On Fractal Bitcoin network, BRC-20 supports 6-byte tickers:

```json
{
  "p": "brc-20",
  "op": "deploy",
  "tick": "potato",
  "max": "21000000000000"
}
```

**Note:** 6-byte tickers are only valid on Fractal network, not on Bitcoin mainnet.

### Self-Mint (brc-20-s)

Allow ongoing minting by deployer:

```json
{
  "p": "brc-20",
  "op": "deploy",
  "tick": "self",
  "max": "0",
  "self_mint": "true"
}
```

## Validation Checklist

- [ ] `p` field matches protocol exactly
- [ ] `op` is valid operation
- [ ] `tick` is correct byte length
- [ ] All numeric values are strings
- [ ] No extra whitespace in JSON
- [ ] Content-type is `text/plain` or `application/json`

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid tick length | Not 4 bytes | Check UTF-8 byte count |
| Numeric amt | Using number instead of string | Wrap in quotes |
| Exceed lim | amt > lim | Reduce mint amount |
| Already deployed | Duplicate ticker | Use different ticker |

## Indexer Differences

Different indexers may have slight variations:
- **UniSat**: Most widely used reference
- **OKX**: Compatible with UniSat
- **Best-in-Slot**: May have stricter validation

Always test against target indexer before mainnet deployment.

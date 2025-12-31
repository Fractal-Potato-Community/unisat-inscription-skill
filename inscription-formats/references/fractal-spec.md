# Fractal Bitcoin Specification

## Overview

Fractal Bitcoin is a Bitcoin Layer 2 scaling solution using recursive virtualization. It maintains 100% Bitcoin Core compatibility while enabling faster blocks and experimental opcodes like OP_CAT.

## Network Parameters

| Parameter | Fractal Mainnet | Bitcoin Mainnet |
|-----------|-----------------|-----------------|
| Block time | 30 seconds | 10 minutes |
| Block height | Independent | Independent |
| Address format | Same (bc1...) | Same |
| OP_CAT | Enabled | Disabled |
| Launch | Sept 2024 | Jan 2009 |

## BRC-20 on Fractal

Fractal supports standard BRC-20 with same format:

```json
{
  "p": "brc-20",
  "op": "deploy",
  "tick": "fb20",
  "max": "21000000",
  "lim": "1000"
}
```

**Key differences:**
- Faster confirmation (30s blocks)
- Lower fees
- Separate indexer state from Bitcoin mainnet
- Same ticker can exist on both chains

## CAT20 Protocol

CAT20 uses OP_CAT for enhanced functionality:

### Deploy
```json
{
  "p": "cat-20",
  "op": "deploy",
  "tick": "cat",
  "max": "21000000",
  "lim": "1000",
  "dec": "2"
}
```

### Mint
```json
{
  "p": "cat-20",
  "op": "mint",
  "tick": "cat",
  "amt": "1000"
}
```

### Transfer
CAT20 uses OP_CAT scripts for atomic transfers - different from BRC-20's inscribe-then-send model.

## CAT721 (NFT Standard)

NFT standard using OP_CAT:

```json
{
  "p": "cat-721",
  "op": "deploy",
  "tick": "cats",
  "max": "10000"
}
```

```json
{
  "p": "cat-721", 
  "op": "mint",
  "tick": "cats",
  "id": "1"
}
```

## OP_CAT Applications

OP_CAT concatenates stack elements, enabling:

### Covenants
Restrict how UTXOs can be spent:
```
<condition> OP_CAT OP_SHA256 <expected_hash> OP_EQUAL
```

### Vaults
Time-locked spending conditions with recovery options.

### Bridges
Trustless verification of external chain state.

## FIP Proposals

### FIP-101: Indexer Service

Proposal for decentralized indexer infrastructure:
- Standardized indexer API
- Incentivized data providers
- Proof of correct indexing

Status: Under discussion

### FIP-102: CAT20 Standard

Formalization of CAT20 protocol:
- Official operation formats
- Indexer compatibility requirements
- Migration path from BRC-20

## Fractal vs Bitcoin Mainnet

### When to use Fractal:
- Experimentation with OP_CAT
- Lower fee environment needed
- Faster finality required
- Building CAT20/CAT721 projects

### When to use Bitcoin Mainnet:
- Maximum security required
- Liquidity access
- Existing BRC-20/Runes ecosystem
- Long-term value storage

## Development Setup

### Indexer APIs

**UniSat Fractal:**
```
https://open-api-fractal.unisat.io/v1/indexer/
```

**Self-hosted ord:**
```bash
ord --chain fractal server
```

### RPC Endpoints

```javascript
const fractalRPC = {
  mainnet: "https://rpc.fractalbitcoin.io",
  testnet: "https://rpc-testnet.fractalbitcoin.io"
};
```

## Bridging Assets

### Bitcoin → Fractal (Peg-in)
1. Send BTC to federation address
2. Wait for confirmations
3. Receive FB (Fractal Bitcoin) 1:1

### Fractal → Bitcoin (Peg-out)
1. Burn FB on Fractal
2. Submit proof to federation
3. Receive BTC after verification

## Common Patterns

### Cross-chain Token
Deploy on both chains with same ticker:
```json
// On Bitcoin mainnet
{"p":"brc-20","op":"deploy","tick":"dual","max":"10500000"}

// On Fractal
{"p":"brc-20","op":"deploy","tick":"dual","max":"10500000"}
```

### CAT20 with Bonding Curve
Combine inscription with OP_CAT covenant for AMM-like mechanics.

## Resources

- Fractal Docs: https://docs.fractalbitcoin.io
- UniSat Fractal: https://fractal.unisat.io
- OP_CAT BIP: BIP-347 (proposed)

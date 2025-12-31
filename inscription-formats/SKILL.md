---
name: inscription-formats
description: "Bitcoin inscription protocol and API helper for BRC-20, Runes, Ordinals, and UniSat API. Use when user asks to: (1) Generate deploy/mint/transfer inscription JSON, (2) Validate inscription format, (3) Explain inscription protocol differences, (4) Debug inscription encoding issues, (5) Query inscription data via UniSat API, (6) Build inscription transactions. Triggers on keywords: BRC-20, brc20, Runes, Ordinals, inscription, 铭文, deploy, mint, transfer, tick, UTXO, UniSat, indexer, API."
---

# Inscription Formats Helper

Help developers generate and validate Bitcoin inscription formats for BRC-20, Runes, and Ordinals protocols.

## Quick Reference

### BRC-20 Formats

**Deploy:**
```json
{"p":"brc-20","op":"deploy","tick":"ordi","max":"21000000","lim":"1000"}
```

**Mint:**
```json
{"p":"brc-20","op":"mint","tick":"ordi","amt":"1000"}
```

**Transfer:**
```json
{"p":"brc-20","op":"transfer","tick":"ordi","amt":"100"}
```

### Runes Format

Runes use OP_RETURN with Runestone encoding, not JSON. Key operations:
- Etching (deploy): Define name, symbol, divisibility, premine
- Mint: Reference rune_id + amount
- Transfer: Edict with (rune_id, amount, output_index)

### Ordinals

Raw data inscribed via witness with envelope format:
```
OP_FALSE OP_IF
  OP_PUSH "ord"
  OP_PUSH 1        # content-type tag
  OP_PUSH "text/plain;charset=utf-8"
  OP_PUSH 0        # end of metadata
  OP_PUSH <data>
OP_ENDIF
```

## Workflow

1. **Identify protocol**: Ask user which protocol (BRC-20 / Runes / Ordinals)
2. **Identify operation**: deploy / mint / transfer / etch
3. **Collect parameters**: ticker, amount, limits, etc.
4. **Generate format**: Output correct JSON or encoding
5. **Validate**: Run `scripts/validate_inscription.py` if needed

## Protocol Selection Guide

| Need | Recommended | Reason |
|------|-------------|--------|
| Fungible token, simple | BRC-20 | Widest support, JSON-based |
| Fungible token, efficient | Runes | Native UTXO, lower fees |
| NFT / arbitrary data | Ordinals | Flexible content types |
| Fractal Bitcoin | BRC-20 or CAT20 | Ecosystem compatibility |

## Common Mistakes to Avoid

- BRC-20 `tick` must be exactly 4 characters (or 5 for brc-20-5byte)
- BRC-20 amounts are strings, not numbers
- Runes names cannot contain certain characters
- Ordinals content-type must match actual data

## References

- For detailed BRC-20 specification: See `references/brc20-spec.md`
- For Runes protocol details: See `references/runes-spec.md`
- For Ordinals envelope format: See `references/ordinals-spec.md`
- For Fractal Bitcoin specifics: See `references/fractal-spec.md`
- For UniSat API usage: See `references/unisat-api.md`

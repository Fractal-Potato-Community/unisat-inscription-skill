# Bitcoin Inscription Development Skill

A Claude Code Skill for Bitcoin and Fractal Bitcoin inscription protocol development, with comprehensive UniSat API documentation.

[中文文档](README_CN.md)

## About

This skill is contributed by the **Fractal Potato Community**. It includes practical tips and insights from daily experience working with UniSat API integration and inscription development.

## Features

### Protocol Specifications
- **BRC-20**: Deploy/mint/transfer operations, 4-byte and 5-byte ticks, validation rules
- **Runes**: UTXO-native model, Runestone encoding, etching/mint/transfer
- **Ordinals**: Sat numbering, envelope format, recursive inscriptions, parent-child
- **CAT20**: Fractal Bitcoin's OP_CAT-based token standard

### UniSat API Coverage
- **Bitcoin Mainnet**: Full indexer (BRC-20, Runes, Alkanes, Collections), Inscribe service, Marketplace v3
- **Fractal Network**: BRC20-Swap (gasless transfers), CAT20-DEX, Runes support, Collection management

### Validation Tools
- Python script for BRC-20/CAT20 format validation
- Rune name validation

## Installation

### Option 1: Import .skill file (Recommended)

Download `inscription-formats.skill` and import it into Claude Code.

### Option 2: Manual Installation

Copy the `inscription-formats/` folder to one of these locations:

```bash
# Project-level (current project only)
.claude/skills/inscription-formats/

# Global (all projects)
~/.claude/skills/inscription-formats/
```

## Usage

Once installed, Claude will automatically use this skill when you ask about:

- BRC-20, Runes, Ordinals, or CAT20 protocols
- UniSat API endpoints and integration
- Inscription format validation
- Fractal Bitcoin development

### Example Queries

```
"Generate a BRC-20 deploy inscription for token TEST with max supply 21000000"

"How do I use UniSat API to get BRC-20 balance?"

"Show me the BRC20-Swap transfer flow on Fractal"

"Validate this inscription JSON format"
```

## File Structure

```
inscription-formats/
├── SKILL.md                           # Main skill instructions
├── references/
│   ├── brc20-spec.md                  # BRC-20 protocol specification
│   ├── runes-spec.md                  # Runes protocol specification
│   ├── ordinals-spec.md               # Ordinals protocol specification
│   ├── fractal-spec.md                # Fractal Bitcoin specifics
│   └── unisat-api.md                  # UniSat API documentation (1000+ lines)
└── scripts/
    └── validate_inscription.py        # Format validation script
```

## API Coverage Summary

| Category | Bitcoin Mainnet | Fractal |
|----------|----------------|---------|
| BRC-20 Indexer | ✅ | ✅ |
| Runes Indexer | ✅ | ✅ |
| Alkanes | ✅ | ❌ |
| BRC20-Swap | ❌ | ✅ |
| CAT20-DEX | ❌ | ✅ |
| Inscribe Service | ✅ | ✅ |
| Marketplace v3 | ✅ | ✅ |

## Contributing

Issues and pull requests are welcome. Please ensure any protocol updates are verified against official documentation.

## Resources

- [UniSat API Swagger UI](https://open-api.unisat.io)
- [UniSat Developer Docs](https://docs.unisat.io)
- [UniSat GitHub](https://github.com/unisat-wallet/unisat-dev-docs)
- [Ordinals Protocol](https://docs.ordinals.com)
- [Runes Protocol](https://docs.ordinals.com/runes.html)

## License

MIT License - see [LICENSE](LICENSE) file.

## Changelog

### v1.0.0 (2025-12)
- Initial release
- BRC-20, Runes, Ordinals, CAT20 protocol specs
- UniSat API documentation for Bitcoin and Fractal networks
- BRC20-Swap implementation guide with production code examples
- Format validation scripts

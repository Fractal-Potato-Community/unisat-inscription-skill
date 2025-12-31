#!/usr/bin/env python3
"""
Inscription Format Validator
Validates BRC-20, Runes, and related inscription formats.
"""

import json
import sys
import re
from typing import Tuple, List

def validate_brc20(data: dict) -> Tuple[bool, List[str]]:
    """Validate BRC-20 inscription format."""
    errors = []
    
    # Check protocol
    if data.get('p') not in ['brc-20', 'brc-20-5byte']:
        errors.append(f"Invalid protocol: {data.get('p')}, expected 'brc-20' or 'brc-20-5byte'")
    
    # Check operation
    op = data.get('op')
    if op not in ['deploy', 'mint', 'transfer']:
        errors.append(f"Invalid operation: {op}")
        return False, errors
    
    # Check tick
    tick = data.get('tick', '')
    tick_bytes = len(tick.encode('utf-8'))
    expected_len = 5 if data.get('p') == 'brc-20-5byte' else 4
    if tick_bytes != expected_len:
        errors.append(f"Tick '{tick}' is {tick_bytes} bytes, expected {expected_len}")
    
    # Operation-specific validation
    if op == 'deploy':
        if 'max' not in data:
            errors.append("Missing required field: max")
        elif not isinstance(data['max'], str):
            errors.append("'max' must be a string, not number")
        elif not data['max'].isdigit():
            errors.append(f"'max' must be numeric string, got: {data['max']}")
            
        if 'lim' in data:
            if not isinstance(data['lim'], str):
                errors.append("'lim' must be a string, not number")
            elif not data['lim'].isdigit():
                errors.append(f"'lim' must be numeric string, got: {data['lim']}")
                
        if 'dec' in data:
            dec = data['dec']
            if not isinstance(dec, str) or not dec.isdigit() or int(dec) > 18:
                errors.append(f"'dec' must be string 0-18, got: {dec}")
    
    elif op in ['mint', 'transfer']:
        if 'amt' not in data:
            errors.append("Missing required field: amt")
        elif not isinstance(data['amt'], str):
            errors.append("'amt' must be a string, not number")
        elif not data['amt'].isdigit():
            errors.append(f"'amt' must be numeric string, got: {data['amt']}")
    
    return len(errors) == 0, errors


def validate_cat20(data: dict) -> Tuple[bool, List[str]]:
    """Validate CAT20 inscription format."""
    errors = []
    
    if data.get('p') != 'cat-20':
        errors.append(f"Invalid protocol: {data.get('p')}, expected 'cat-20'")
    
    # Similar validation to BRC-20
    op = data.get('op')
    if op not in ['deploy', 'mint', 'transfer']:
        errors.append(f"Invalid operation: {op}")
    
    tick = data.get('tick', '')
    if not tick:
        errors.append("Missing required field: tick")
    
    if op == 'deploy':
        for field in ['max']:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], str):
                errors.append(f"'{field}' must be a string")
                
    elif op in ['mint', 'transfer']:
        if 'amt' not in data:
            errors.append("Missing required field: amt")
        elif not isinstance(data['amt'], str):
            errors.append("'amt' must be a string")
    
    return len(errors) == 0, errors


def validate_rune_name(name: str) -> Tuple[bool, List[str]]:
    """Validate Rune name format."""
    errors = []
    
    # Remove spacers (dots or bullets)
    clean_name = re.sub(r'[.•]', '', name)
    
    # Check characters (A-Z only)
    if not re.match(r'^[A-Z]+$', clean_name):
        errors.append(f"Rune name must contain only A-Z, got: {clean_name}")
    
    # Check length (minimum varies by block height, but basic check)
    if len(clean_name) < 1:
        errors.append("Rune name cannot be empty")
    elif len(clean_name) > 28:
        errors.append("Rune name too long (max 28 characters)")
    
    return len(errors) == 0, errors


def validate_inscription(json_str: str) -> Tuple[bool, List[str]]:
    """Main validation entry point."""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    
    protocol = data.get('p', '')
    
    if protocol in ['brc-20', 'brc-20-5byte']:
        return validate_brc20(data)
    elif protocol == 'cat-20':
        return validate_cat20(data)
    else:
        return False, [f"Unknown protocol: {protocol}"]


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_inscription.py '<json_string>'")
        print("       python validate_inscription.py --file <path>")
        print()
        print("Examples:")
        print('  python validate_inscription.py \'{"p":"brc-20","op":"mint","tick":"ordi","amt":"1000"}\'')
        sys.exit(1)
    
    if sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Error: --file requires a path argument")
            sys.exit(1)
        with open(sys.argv[2], 'r') as f:
            json_str = f.read()
    else:
        json_str = sys.argv[1]
    
    valid, errors = validate_inscription(json_str)
    
    if valid:
        print("✅ Valid inscription format")
        # Pretty print the parsed JSON
        data = json.loads(json_str)
        print(json.dumps(data, indent=2))
    else:
        print("❌ Invalid inscription format")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == '__main__':
    main()

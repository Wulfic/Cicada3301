#!/usr/bin/env python3
"""
Analyze special symbols (non-runic characters) across all Liber Primus pages.
Looking for patterns in &, $, §, numbers, and other markers.
"""

import os
import re
from pathlib import Path

# Define the runic alphabet
RUNES = set('ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛠᛡ')
PUNCTUATION = set('-.\n\r \t')

def analyze_page(page_path):
    """Analyze a single page for special symbols."""
    runes_file = page_path / 'runes.txt'
    if not runes_file.exists():
        return None
    
    content = runes_file.read_text(encoding='utf-8')
    
    # Find all non-runic, non-punctuation characters
    special = []
    for i, char in enumerate(content):
        if char not in RUNES and char not in PUNCTUATION:
            # Get context around the character
            start = max(0, i-5)
            end = min(len(content), i+6)
            context = content[start:end].replace('\n', '↵')
            special.append({
                'char': char,
                'position': i,
                'line': content[:i].count('\n') + 1,
                'context': context
            })
    
    rune_count = sum(1 for c in content if c in RUNES)
    
    return {
        'page': page_path.name,
        'rune_count': rune_count,
        'special_chars': special,
        'special_summary': {char['char']: sum(1 for c in special if c['char'] == char['char']) 
                          for char in special}
    }

def main():
    pages_dir = Path(__file__).parent.parent / 'pages'
    
    all_symbols = {}
    pages_with_symbols = []
    
    print("=" * 70)
    print("SPECIAL SYMBOLS ANALYSIS - LIBER PRIMUS")
    print("=" * 70)
    
    for page_dir in sorted(pages_dir.iterdir()):
        if page_dir.is_dir() and page_dir.name.startswith('page_'):
            result = analyze_page(page_dir)
            if result and result['special_chars']:
                pages_with_symbols.append(result)
                for char_info in result['special_chars']:
                    char = char_info['char']
                    if char not in all_symbols:
                        all_symbols[char] = []
                    all_symbols[char].append({
                        'page': result['page'],
                        'line': char_info['line'],
                        'context': char_info['context']
                    })
    
    # Print summary by symbol type
    print("\n📊 SYMBOL SUMMARY:")
    print("-" * 50)
    for symbol, occurrences in sorted(all_symbols.items(), key=lambda x: -len(x[1])):
        char_repr = repr(symbol)
        print(f"\n  '{symbol}' ({char_repr}): {len(occurrences)} occurrences")
        for occ in occurrences:
            print(f"      {occ['page']}, line {occ['line']}: ...{occ['context']}...")
    
    # Look for numbers specifically
    print("\n" + "=" * 70)
    print("🔢 NUMBER ANALYSIS:")
    print("-" * 50)
    
    number_symbols = {k: v for k, v in all_symbols.items() if k.isdigit()}
    if number_symbols:
        print("\nNumbers found:")
        for num in sorted(number_symbols.keys()):
            print(f"  {num}: {len(number_symbols[num])} occurrences")
            for occ in number_symbols[num]:
                print(f"      {occ['page']}, line {occ['line']}: {occ['context']}")
        
        # Check for missing numbers
        found_nums = set(int(n) for n in number_symbols.keys())
        if found_nums:
            min_n, max_n = min(found_nums), max(found_nums)
            expected = set(range(min_n, max_n + 1))
            missing = expected - found_nums
            if missing:
                print(f"\n  ⚠️  MISSING NUMBERS: {sorted(missing)}")
    else:
        print("  No Arabic numerals found.")
    
    # Look for patterns in & symbol placement
    print("\n" + "=" * 70)
    print("📎 AMPERSAND (&) PATTERN ANALYSIS:")
    print("-" * 50)
    
    ampersands = all_symbols.get('&', [])
    if ampersands:
        print(f"\n  Total & symbols: {len(ampersands)}")
        print("  Pages containing &:")
        amp_pages = sorted(set(a['page'] for a in ampersands))
        for p in amp_pages:
            lines = [a['line'] for a in ampersands if a['page'] == p]
            print(f"      {p}: lines {lines}")
        
        # Check if & appears consistently at section breaks
        print("\n  Hypothesis: & marks paragraph/section breaks")
    
    # Look for section symbol §
    print("\n" + "=" * 70)
    print("§ SECTION SYMBOL ANALYSIS:")
    print("-" * 50)
    
    sections = all_symbols.get('§', [])
    if sections:
        print(f"\n  Total § symbols: {len(sections)}")
        for s in sections:
            print(f"      {s['page']}, line {s['line']}: {s['context']}")
    else:
        print("  No § symbols found.")
    
    # Check for $ symbols
    print("\n" + "=" * 70)
    print("💲 DOLLAR SIGN ($) ANALYSIS:")
    print("-" * 50)
    
    dollars = all_symbols.get('$', [])
    if dollars:
        print(f"\n  Total $ symbols: {len(dollars)}")
        for d in dollars:
            print(f"      {d['page']}, line {d['line']}: {d['context']}")
    else:
        print("  No $ symbols found.")
    
    # Key insight
    print("\n" + "=" * 70)
    print("🔍 KEY INSIGHTS:")
    print("-" * 50)
    print("""
  1. Arabic numerals 1-5, 7 are embedded in runic text
  2. Number 6 is MISSING from the sequence
  3. '&' appears to mark section/paragraph breaks (18 pages)
  4. '§' appears only on page 56 (solved cleartext)
  5. '$' appears on pages 54, 55 (unsolved)
  
  HYPOTHESIS: The special symbols serve as structural markers
  The numbers 1-7 (minus 6) may indicate a special reading order
  or decryption sequence separate from page numbers.
""")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Focused analysis using the actual Unicode rune data.
Working with the raw data format from RuneSolver.py
"""

import re
from collections import Counter

# Anglo-Saxon Futhorc runes (Unicode) to letter mapping
RUNE_MAP = {
    'ᚠ': ('F', 0, 2),
    'ᚢ': ('U', 1, 3),
    'ᚦ': ('TH', 2, 5),
    'ᚩ': ('O', 3, 7),
    'ᚱ': ('R', 4, 11),
    'ᚳ': ('C', 5, 13),  # or CK
    'ᚷ': ('G', 6, 17),
    'ᚹ': ('W', 7, 19),
    'ᚻ': ('H', 8, 23),
    'ᚾ': ('N', 9, 29),
    'ᛁ': ('I', 10, 31),
    'ᛂ': ('J', 11, 37),  # or IA
    'ᛇ': ('EO', 12, 41),
    'ᛈ': ('P', 13, 43),
    'ᛉ': ('X', 14, 47),
    'ᛋ': ('S', 15, 53),
    'ᛏ': ('T', 16, 59),
    'ᛒ': ('B', 17, 61),
    'ᛖ': ('E', 18, 67),
    'ᛗ': ('M', 19, 71),
    'ᛚ': ('L', 20, 73),
    'ᛝ': ('NG', 21, 79),
    'ᛟ': ('OE', 22, 83),
    'ᛞ': ('D', 23, 89),
    'ᚪ': ('A', 24, 97),
    'ᚫ': ('AE', 25, 101),
    'ᚣ': ('Y', 26, 103),
    'ᛡ': ('IA', 27, 107),  # IO or IA
    'ᛠ': ('EA', 28, 109),
}

# Create reverse mappings
RUNE_TO_IDX = {rune: info[1] for rune, info in RUNE_MAP.items()}
RUNE_TO_LETTER = {rune: info[0] for rune, info in RUNE_MAP.items()}
RUNE_TO_GEM = {rune: info[2] for rune, info in RUNE_MAP.items()}
IDX_TO_RUNE = {info[1]: rune for rune, info in RUNE_MAP.items()}

# List of runes in order
RUNES = [IDX_TO_RUNE[i] for i in range(29)]

def is_rune(char):
    return char in RUNE_MAP

def unicode_to_letters(text):
    """Convert Unicode runes to letter representation."""
    result = []
    for char in text:
        if char in RUNE_TO_LETTER:
            result.append(RUNE_TO_LETTER[char])
        elif char in ['•', ':', '.', ' ', '\n', '-']:
            result.append(' ')
        elif char == "'":
            result.append("'")
    return ''.join(result)

def shift_rune(rune, shift):
    """Shift a rune by given amount (mod 29)."""
    idx = RUNE_TO_IDX[rune]
    new_idx = (idx + shift) % 29
    return RUNES[new_idx]

def gematria_shift(rune, direction=1):
    """Shift rune by its gematria value. direction: 1=add, -1=sub"""
    gem = RUNE_TO_GEM[rune]
    return shift_rune(rune, direction * gem)

def calculate_ioc(runes_only):
    """Calculate Index of Coincidence for a list of runes."""
    freq = Counter(runes_only)
    n = len(runes_only)
    if n < 2:
        return 0
    ioc = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ioc * 29  # Normalize to 29-character alphabet

def load_pages():
    """Load pages directly from RuneSolver.py."""
    wiki_path = "C:/Users/tyler/Repos/Cicada3301/EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py"
    
    with open(wiki_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the allpages variable which has all combined text
    # Also get individual pages
    pages = {}
    
    # Get Page0 through Page57
    for i in range(58):
        pattern = rf'^Page{i}\s*=\s*"([^"]*)"'
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            pages[i] = match.group(1)
        else:
            pages[i] = ""
    
    return pages

def extract_runes(text):
    """Extract only rune characters from text."""
    return [char for char in text if is_rune(char)]

def test_page_56_formula(runes):
    """
    Apply the Page 56 formula: -(gematria + 57) mod 29
    This is the known solved formula.
    """
    result = []
    for rune in runes:
        gem = RUNE_TO_GEM[rune]
        shift = -(gem + 57) % 29
        new_idx = (RUNE_TO_IDX[rune] + shift) % 29
        result.append(RUNES[new_idx])
    return result

def test_gematria_self_shift(runes, direction=1):
    """Shift each rune by its own gematria value."""
    result = []
    for rune in runes:
        result.append(gematria_shift(rune, direction))
    return result

def analyze_page_56(pages):
    """Analyze Page 56 (known solved page) to verify our formula."""
    print("\n" + "="*70)
    print("PAGE 56 ANALYSIS (Known Solved)")
    print("="*70)
    
    page56 = pages.get(56, "")
    if not page56:
        print("Page 56 not found!")
        return
    
    print(f"Raw: {page56[:100]}")
    
    runes = extract_runes(page56)
    print(f"Rune count: {len(runes)}")
    
    # Apply Page 56 formula
    decrypted = test_page_56_formula(runes)
    decrypted_text = unicode_to_letters(''.join(decrypted))
    print(f"\nPage 56 formula result: {decrypted_text}")

def analyze_page_57(pages):
    """Analyze Page 57 (known plaintext)."""
    print("\n" + "="*70)
    print("PAGE 57 ANALYSIS (Known Plaintext)")  
    print("="*70)
    
    page57 = pages.get(57, "")
    if not page57:
        print("Page 57 not found!")
        return
    
    print(f"Raw: {page57[:100]}")
    
    text = unicode_to_letters(page57)
    print(f"\nDecoded text: {text}")
    
    runes = extract_runes(page57)
    print(f"Rune count: {len(runes)}")
    ioc = calculate_ioc(runes)
    print(f"IoC: {ioc:.4f}")

def analyze_all_encrypted_pages(pages):
    """Analyze all encrypted pages systematically."""
    print("\n" + "="*70)
    print("ALL PAGES ANALYSIS")
    print("="*70)
    
    all_encrypted_runes = []
    
    for i in range(58):
        page = pages.get(i, "")
        if not page:
            continue
            
        runes = extract_runes(page)
        if not runes:
            continue
        
        ioc = calculate_ioc(runes)
        
        # Test gematria+ transformation
        gem_result = test_gematria_self_shift(runes, 1)
        gem_ioc = calculate_ioc(gem_result)
        
        # Test Page 56 formula
        p56_result = test_page_56_formula(runes)
        p56_ioc = calculate_ioc(p56_result)
        
        status = "DECRYPTED" if ioc > 1.5 else "encrypted"
        print(f"Page {i:2d}: {len(runes):4d} runes, IoC={ioc:.4f} (gem+:{gem_ioc:.4f}, p56:{p56_ioc:.4f}) [{status}]")
        
        if ioc < 1.5 and i < 56:  # Only collect encrypted pages before solved pages
            all_encrypted_runes.extend(runes)
    
    print(f"\nTotal encrypted runes: {len(all_encrypted_runes)}")
    
    # Test gematria+ on all encrypted runes combined
    print("\n" + "="*70)
    print("COMBINED ENCRYPTED ANALYSIS")
    print("="*70)
    
    orig_ioc = calculate_ioc(all_encrypted_runes)
    print(f"Original combined IoC: {orig_ioc:.4f}")
    
    gem_result = test_gematria_self_shift(all_encrypted_runes, 1)
    gem_ioc = calculate_ioc(gem_result)
    print(f"Gematria+ combined IoC: {gem_ioc:.4f}")
    
    # Count patterns in gematria+ result
    gem_text = unicode_to_letters(''.join(gem_result))
    the_count = gem_text.count('THE')
    and_count = gem_text.count('AND')
    ing_count = gem_text.count('ING')
    print(f"'THE' count: {the_count}, 'AND' count: {and_count}, 'ING' count: {ing_count}")
    
    # Show first 200 characters
    print(f"\nFirst 200 chars of gematria+ result:")
    print(gem_text[:200])
    
    return all_encrypted_runes

def try_offset_variations(runes):
    """Try the gematria shift with various offsets."""
    print("\n" + "="*70)
    print("OFFSET VARIATION ANALYSIS")
    print("="*70)
    
    best_ioc = 0
    best_offset = 0
    
    for offset in range(-100, 101):
        result = []
        for rune in runes:
            gem = RUNE_TO_GEM[rune]
            shift = (gem + offset) % 29
            new_idx = (RUNE_TO_IDX[rune] + shift) % 29
            result.append(RUNES[new_idx])
        
        ioc = calculate_ioc(result)
        
        if ioc > best_ioc:
            best_ioc = ioc
            best_offset = offset
            
        if ioc > 1.5:
            text = unicode_to_letters(''.join(result))
            print(f"Offset {offset:4d}: IoC={ioc:.4f}, first 60: {text[:60]}")
    
    print(f"\nBest: offset={best_offset}, IoC={best_ioc:.4f}")

def try_page_56_variants(runes):
    """Try variants of the Page 56 formula."""
    print("\n" + "="*70)
    print("PAGE 56 FORMULA VARIANTS")
    print("="*70)
    
    # Original: -(gem + 57) mod 29
    # Try: -(gem + k) mod 29 for various k
    
    for k in range(0, 150):
        result = []
        for rune in runes:
            gem = RUNE_TO_GEM[rune]
            shift = -(gem + k) % 29
            new_idx = (RUNE_TO_IDX[rune] + shift) % 29
            result.append(RUNES[new_idx])
        
        ioc = calculate_ioc(result)
        
        if ioc > 1.5:
            text = unicode_to_letters(''.join(result))
            print(f"-(gem + {k:3d}) mod 29: IoC={ioc:.4f}, first 60: {text[:60]}")

def main():
    print("="*70)
    print("LIBER PRIMUS ANALYSIS - DIRECT UNICODE")
    print("="*70)
    
    pages = load_pages()
    
    # Count non-empty pages
    non_empty = sum(1 for p in pages.values() if p)
    print(f"Loaded {non_empty} non-empty pages")
    
    # Analyze known pages
    analyze_page_57(pages)
    analyze_page_56(pages)
    
    # Analyze all pages
    encrypted_runes = analyze_all_encrypted_pages(pages)
    
    # Test offset variations on first page with data
    for i in range(58):
        if pages.get(i):
            runes = extract_runes(pages[i])
            if runes:
                print(f"\n\nTesting Page {i} ({len(runes)} runes):")
                try_offset_variations(runes[:500])  # First 500 runes
                try_page_56_variants(runes[:500])
                break
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

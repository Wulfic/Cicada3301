#!/usr/bin/env python3
"""
Attack Page 20: Use Page 18's plaintext as key for composite positions

Page 18 plaintext: "BEING OF ALL I WILL ASC THE OATH IS SWORN TO THE ONE WITHIN THE ABOVE THE WAY"
Page 19 hint: "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"

Hypothesis: The pages chain together:
- P18 plaintext is the key for P19 or P20
- P19 tells us HOW to use Deor for P20
- The composite positions might use P18 as key!
"""

import os
from collections import Counter

# Gematria Primus mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X',
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

CHAR_TO_IDX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
    'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28, 'K': 5
}

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    indices = []
    for c in content:
        if c in RUNE_MAP:
            indices.append(RUNE_MAP[c])
    return indices

def string_to_indices(s):
    """Convert a string to Gematria indices, handling digraphs."""
    indices = []
    i = 0
    s = s.upper().replace(' ', '').replace('-', '')
    while i < len(s):
        matched = False
        if i + 1 < len(s):
            digraph = s[i:i+2]
            if digraph in CHAR_TO_IDX:
                indices.append(CHAR_TO_IDX[digraph])
                i += 2
                matched = True
        if not matched:
            c = s[i]
            if c in CHAR_TO_IDX:
                indices.append(CHAR_TO_IDX[c])
            i += 1
    return indices

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    # Load P20
    cipher = load_runes(p20_path)
    print(f"Loaded {len(cipher)} runes from Page 20")
    
    # Page 18 plaintext (converted to Runeglish)
    p18_plaintext = "BEING OF ALL I WILL ASC THE OATH IS SWORN TO THE ONE WITHIN THE ABOVE THE WAY"
    p18_key = string_to_indices(p18_plaintext)
    print(f"P18 key: {len(p18_key)} indices")
    
    # P19 plaintext
    p19_plaintext = "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR"
    p19_key = string_to_indices(p19_plaintext)
    print(f"P19 key: {len(p19_key)} indices")
    
    # Get composite positions
    n = len(cipher)
    composites = [i for i in range(4, n) if not is_prime(i)]
    composite_runes = [cipher[i] for i in composites]
    print(f"\nComposite positions: {len(composites)}")
    
    # Also get all non-prime (including 0, 1)
    non_primes = [i for i in range(n) if not is_prime(i)]
    non_prime_runes = [cipher[i] for i in non_primes]
    print(f"Non-prime positions (incl 0,1): {len(non_primes)}")
    
    results = []
    
    # Test 1: P18 as cycling key for composites
    for mode in ['sub', 'add', 'beaufort']:
        stream = []
        for i, c in enumerate(composite_runes):
            k = p18_key[i % len(p18_key)]
            if mode == 'sub':
                stream.append((c - k) % 29)
            elif mode == 'add':
                stream.append((c + k) % 29)
            else:
                stream.append((k - c) % 29)
        ioc = calc_ioc(stream)
        results.append(('P18_composite_' + mode, ioc, indices_to_latin(stream)))
    
    # Test 2: P18 as key for ALL non-primes
    for mode in ['sub', 'add', 'beaufort']:
        stream = []
        for i, c in enumerate(non_prime_runes):
            k = p18_key[i % len(p18_key)]
            if mode == 'sub':
                stream.append((c - k) % 29)
            elif mode == 'add':
                stream.append((c + k) % 29)
            else:
                stream.append((k - c) % 29)
        ioc = calc_ioc(stream)
        results.append(('P18_all_nonprime_' + mode, ioc, indices_to_latin(stream)))
    
    # Test 3: P19 as key for composites
    for mode in ['sub', 'add', 'beaufort']:
        stream = []
        for i, c in enumerate(composite_runes):
            k = p19_key[i % len(p19_key)]
            if mode == 'sub':
                stream.append((c - k) % 29)
            elif mode == 'add':
                stream.append((c + k) % 29)
            else:
                stream.append((k - c) % 29)
        ioc = calc_ioc(stream)
        results.append(('P19_composite_' + mode, ioc, indices_to_latin(stream)))
    
    # Test 4: P18 + P19 concatenated as key
    combined_key = p18_key + p19_key
    for mode in ['sub', 'add', 'beaufort']:
        stream = []
        for i, c in enumerate(composite_runes):
            k = combined_key[i % len(combined_key)]
            if mode == 'sub':
                stream.append((c - k) % 29)
            elif mode == 'add':
                stream.append((c + k) % 29)
            else:
                stream.append((k - c) % 29)
        ioc = calc_ioc(stream)
        results.append(('P18+P19_composite_' + mode, ioc, indices_to_latin(stream)))
    
    # Test 5: FULL page 20 with P18 as key
    for mode in ['sub', 'add', 'beaufort']:
        stream = []
        for i, c in enumerate(cipher):
            k = p18_key[i % len(p18_key)]
            if mode == 'sub':
                stream.append((c - k) % 29)
            elif mode == 'add':
                stream.append((c + k) % 29)
            else:
                stream.append((k - c) % 29)
        ioc = calc_ioc(stream)
        results.append(('P18_full_' + mode, ioc, indices_to_latin(stream)))
    
    # Test 6: Various keywords from P63 grid
    keywords = [
        ("VOID", [1, 3, 10, 23]),
        ("AETHEREAL", [25, 2, 18, 4, 18, 24, 20]),
        ("CARNAL", [5, 24, 4, 9, 24, 20]),
        ("MOURNFUL", [19, 3, 1, 4, 9, 0, 1, 20]),
        ("CABAL", [5, 24, 17, 24, 20]),
        ("MOBIUS", [19, 3, 17, 10, 1, 15]),
        ("OBSCURA", [3, 17, 15, 5, 1, 4, 24]),
        ("SHADOWS", [15, 8, 24, 23, 3, 7, 15]),
        ("ANALOG", [24, 9, 24, 20, 3, 6]),
        ("THELONE", [2, 18, 20, 3, 9, 18]),
        ("DEOR", [23, 18, 3, 4]),
        ("SEFA", [15, 18, 0, 24]),
        ("EODE", [18, 3, 23, 18]),
    ]
    
    for name, key in keywords:
        for mode in ['sub', 'beaufort']:
            stream = []
            for i, c in enumerate(composite_runes):
                k = key[i % len(key)]
                if mode == 'sub':
                    stream.append((c - k) % 29)
                else:
                    stream.append((k - c) % 29)
            ioc = calc_ioc(stream)
            results.append((f'{name}_composite_{mode}', ioc, indices_to_latin(stream)))
    
    # Sort and display
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*80)
    print("RESULTS (sorted by IoC, English ~1.73, Random ~1.0)")
    print("="*80)
    
    for method, ioc, text in results[:20]:
        print(f"\n[{method}] IoC: {ioc:.4f}")
        print(f"  Preview: {text[:100]}")
    
    # Check for hits
    for method, ioc, text in results:
        if ioc > 1.3:
            print(f"\n*** POTENTIAL HIT: {method} IoC: {ioc:.4f} ***")
            print(f"Text: {text[:200]}")

if __name__ == '__main__':
    main()

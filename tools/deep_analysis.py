#!/usr/bin/env python3
"""
Deep analysis of what's actually happening with Pages 27-31

Let's examine:
1. What the raw cipher text looks like
2. Compare with Page 0's pattern
3. Test if these pages might use a DIFFERENT cipher
"""

import re
from pathlib import Path
from collections import Counter

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

PARABLE = "PARABLELIKETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def analyze_distribution(runes, label):
    """Analyze rune frequency distribution"""
    indices = [rune_to_idx(r) for r in runes if rune_to_idx(r) >= 0]
    counter = Counter(indices)
    
    # English frequency order (approximate)
    english_order = [24, 18, 5, 10, 16, 9, 15, 20, 7, 23]  # A, E, C, I, T, N, S, L, W, D
    
    top5 = counter.most_common(5)
    print(f"{label}:")
    print(f"  Length: {len(indices)}")
    print(f"  Top 5 runes: {[(LETTERS[i], c) for i, c in top5]}")
    print(f"  Index of Coincidence: {calc_ioc(indices):.4f}")
    return indices

def calc_ioc(indices):
    """Calculate Index of Coincidence"""
    n = len(indices)
    if n < 2:
        return 0
    freqs = Counter(indices)
    total = sum(f * (f - 1) for f in freqs.values())
    return total / (n * (n - 1))

def test_vigenere_variants(cipher, page_num):
    """Test different Vigenère decryption approaches"""
    print(f"\n{'='*60}")
    print(f"PAGE {page_num} - DEEP ANALYSIS")
    print(f"{'='*60}")
    
    print(f"\n1. RAW CIPHER (first 50 runes as letters):")
    raw_letters = ''.join(idx_to_letter(rune_to_idx(r)) for r in cipher[:50])
    print(f"   {raw_letters}")
    
    print(f"\n2. RAW INDICES (first 30):")
    indices = [rune_to_idx(r) for r in cipher[:30]]
    print(f"   {indices}")
    
    # Test autokey cipher
    print(f"\n3. AUTOKEY DECRYPTION (key primes plaintext):")
    result = []
    for i, r in enumerate(cipher):
        c_idx = rune_to_idx(r)
        if i < len(MASTER_KEY):
            k = MASTER_KEY[i]
        else:
            # Use previous plaintext as key
            k = rune_to_idx(RUNE_ORDER[result[-len(MASTER_KEY)] % 29])
        plain_idx = (c_idx - k) % 29
        result.append(plain_idx)
    decrypted = ''.join(idx_to_letter(p) for p in result)
    print(f"   {decrypted[:60]}...")
    
    # Test running key cipher with Parable
    print(f"\n4. RUNNING KEY WITH PARABLE (repeating):")
    parable_indices = [RUNE_ORDER.index(RUNE_ORDER[ord(c) - ord('A')]) if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' else -1 
                       for c in PARABLE]
    # Convert Parable letters to rune indices
    letter_to_idx = {L: i for i, L in enumerate(LETTERS)}
    parable_indices = []
    i = 0
    while i < len(PARABLE):
        for length in [2, 1]:  # Try 2-char letters first (TH, NG, etc)
            substr = PARABLE[i:i+length]
            if substr in letter_to_idx:
                parable_indices.append(letter_to_idx[substr])
                i += length
                break
    
    result = []
    for i, r in enumerate(cipher[:60]):
        c_idx = rune_to_idx(r)
        k = parable_indices[i % len(parable_indices)]
        plain_idx = (c_idx - k) % 29
        result.append(idx_to_letter(plain_idx))
    print(f"   {' '.join(result)}...")
    
    # Test if might be Caesar (constant shift)
    print(f"\n5. CAESAR (constant shift) - best shift:")
    best_shift = 0
    best_score = 0
    for shift in range(29):
        shifted = ''.join(idx_to_letter((rune_to_idx(r) - shift) % 29) for r in cipher)
        score = sum(1 for c in shifted if c in 'AEIOU')
        if score > best_score:
            best_score = score
            best_shift = shift
    shifted = ''.join(idx_to_letter((rune_to_idx(r) - best_shift) % 29) for r in cipher)
    print(f"   Shift {best_shift}: {shifted[:60]}...")

def main():
    pages = load_pages()
    
    # First, let's verify Page 0 decrypts correctly
    print("="*60)
    print("VERIFICATION: Page 0 → Parable")
    print("="*60)
    page0 = pages[0]
    page57 = pages[57]
    
    # Decrypt Page 0 with key
    decrypted = []
    for i in range(min(len(page0), len(MASTER_KEY))):
        c_idx = rune_to_idx(page0[i])
        k = MASTER_KEY[i]
        plain_idx = (c_idx - k) % 29
        decrypted.append(idx_to_letter(plain_idx))
    print(f"Page 0 decrypted: {''.join(decrypted[:60])}...")
    print(f"Parable:          {PARABLE[:60]}...")
    
    # Analyze a few pages
    print("\n" + "="*60)
    print("FREQUENCY ANALYSIS")
    print("="*60)
    
    analyze_distribution(page0, "Page 0 (encrypted Parable)")
    analyze_distribution(page57, "Page 57 (plaintext Parable)")
    
    for p in [27, 28, 29, 30, 31]:
        if p in pages:
            analyze_distribution(pages[p], f"Page {p} (unsolved)")
    
    # Deep analysis of key pages
    for p in [27, 28]:
        if p in pages:
            test_vigenere_variants(pages[p], p)

if __name__ == "__main__":
    main()

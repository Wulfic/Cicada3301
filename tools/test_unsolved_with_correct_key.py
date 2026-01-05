#!/usr/bin/env python3
"""
Test unsolved pages with the VERIFIED CORRECT key (sum=1331)

Key derived from (Page0 - Page57) mod 29
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# The VERIFIED correct master key (sum = 1331 = 11³)
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# Parable text (for reference)
PARABLE = "PARABLELIKETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

# Parable words with their starting positions
WORDS = [
    (0, "PARABLE"),
    (7, "LIKE"),  
    (11, "THE"),
    (14, "INSTAR"),
    (20, "TUNNELNG"),
    (28, "TO"),
    (30, "THE"),
    (33, "SURFACE"),
    (40, "WE"),
    (42, "MUST"),
    (46, "SHED"),
    (50, "OUR"),
    (53, "OWN"),
    (56, "CIRCUMFERENCES"),
    (70, "FIND"),
    (74, "THE"),
    (77, "DIUINITY"),
    (85, "WITHIN"),
    (91, "AND"),
    (94, "EMERGE"),
]

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

def score_english(text):
    """Score how English-like the text is."""
    common = set('AEIOURSNTLCD')
    return sum(1 for c in text.upper() if c in common)

def decrypt_page(cipher_runes, key, offset=0):
    """Decrypt a page using the given key with offset."""
    result = []
    for i, r in enumerate(cipher_runes):
        c_idx = rune_to_idx(r)
        if c_idx < 0:
            continue
        k = key[(i + offset) % len(key)]
        plain_idx = (c_idx - k) % 29
        result.append(idx_to_letter(plain_idx))
    return ''.join(result)

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("TESTING UNSOLVED PAGES WITH CORRECT KEY (SUM=1331)")
    print("=" * 70)
    
    # Unsolved pages to test
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("\n1. BRUTE FORCE ALL OFFSETS:")
    print("-" * 70)
    
    for page_num in unsolved:
        if page_num not in pages:
            continue
        
        cipher = pages[page_num]
        best_score = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(95):
            decrypted = decrypt_page(cipher, MASTER_KEY, offset)
            score = score_english(decrypted)
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = decrypted
        
        pct = (best_score / len(cipher)) * 100 if cipher else 0
        print(f"Page {page_num:2d}: offset={best_offset:2d}, score={best_score:3d}/{len(cipher):3d} ({pct:.0f}%)")
        print(f"         {best_text[:60]}...")
    
    print("\n" + "=" * 70)
    print("2. TESTING 2016 CLUE: Page N → Word (N-20)")
    print("   'Numbers are the direction'")
    print("-" * 70)
    
    # Theory: Page N should use key starting at word position (N-20) mod 20
    for page_num in [27, 28, 29, 30, 31]:
        if page_num not in pages:
            continue
        
        word_idx = (page_num - 20) % len(WORDS)
        word_pos, word = WORDS[word_idx]
        
        cipher = pages[page_num]
        decrypted = decrypt_page(cipher, MASTER_KEY, word_pos)
        score = score_english(decrypted)
        
        print(f"Page {page_num} → Word {word_idx} '{word}' (pos {word_pos})")
        print(f"   Score: {score}/{len(cipher)}, Text: {decrypted[:50]}...")

    print("\n" + "=" * 70)
    print("3. TESTING GEMATRIA AS DIRECTION")
    print("-" * 70)
    
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    # Theory: Use cumulative Gematria sum as key index
    for page_num in [27, 28, 29, 30, 31]:
        if page_num not in pages:
            continue
        
        cipher = pages[page_num]
        result = []
        gem_sum = 0
        
        for i, r in enumerate(cipher):
            c_idx = rune_to_idx(r)
            if c_idx < 0:
                continue
            # Use cumulative Gematria as key index
            gem_sum += PRIMES[c_idx]
            k = MASTER_KEY[gem_sum % 95]
            plain_idx = (c_idx - k) % 29
            result.append(idx_to_letter(plain_idx))
        
        decrypted = ''.join(result)
        score = score_english(decrypted)
        print(f"Page {page_num}: Cumulative Gematria method")
        print(f"   Score: {score}/{len(cipher)}, Text: {decrypted[:50]}...")

if __name__ == "__main__":
    main()

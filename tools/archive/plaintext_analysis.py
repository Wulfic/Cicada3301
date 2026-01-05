#!/usr/bin/env python3
"""
ASSUMING MASTER KEY IS CORRECT - WHAT IS THE PLAINTEXT?

If the master key is correct, then for each page:
- Plaintext = (Ciphertext - Master_Key) mod 29

Let's look at what we get and see if there's a pattern or structure
that suggests an additional transformation.
"""

import re
from pathlib import Path
import numpy as np
from collections import Counter

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
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

def decrypt_with_key(cipher_indices, key, offset=0):
    """Decrypt cipher using key with offset"""
    result = []
    for i, c in enumerate(cipher_indices):
        k = key[(i + offset) % len(key)]
        p = (c - k) % 29
        result.append(p)
    return result

def analyze_distribution(indices, name):
    """Analyze frequency distribution of indices"""
    freq = Counter(indices)
    total = len(indices)
    
    # English letter frequency order (adapted)
    # E, T, A, O, I, N, S, R, H, L are most common
    english_order = [18, 16, 24, 3, 10, 9, 15, 4, 8, 20]  # E, T, A, O, I, N, S, R, H, L
    
    top5 = freq.most_common(5)
    top5_letters = [idx_to_letter(idx) for idx, _ in top5]
    
    # Check how many of top 5 are common English letters
    common_match = sum(1 for idx, _ in top5 if idx in english_order)
    
    print(f"  {name}:")
    print(f"    Top 5: {top5_letters}")
    print(f"    Common English match: {common_match}/5")
    return common_match

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("PLAINTEXT ANALYSIS ASSUMING MASTER KEY")
    print("=" * 70)
    
    # First verify Page 0
    print("\n1. VERIFICATION: Page 0 decrypts to Parable")
    print("-" * 60)
    
    p0_indices = [rune_to_idx(r) for r in pages[0]]
    p0_plain = decrypt_with_key(p0_indices, MASTER_KEY)
    p0_text = ''.join(idx_to_letter(p) for p in p0_plain[:95])
    print(f"Page 0 plaintext: {p0_text}")
    
    # Now analyze what we get for unsolved pages
    print("\n2. UNSOLVED PAGES DECRYPTED WITH MASTER KEY")
    print("-" * 60)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher_indices = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Try all 95 offsets and find best
        best_offset = 0
        best_score = 0
        
        for offset in range(95):
            plain = decrypt_with_key(cipher_indices, MASTER_KEY, offset)
            # Count common English letters
            common_count = sum(1 for p in plain if p in [18, 16, 24, 3, 10, 9, 15, 4, 8, 20])
            if common_count > best_score:
                best_score = common_count
                best_offset = offset
        
        # Decrypt with best offset
        plain = decrypt_with_key(cipher_indices, MASTER_KEY, best_offset)
        text = ''.join(idx_to_letter(p) for p in plain)
        
        print(f"\nPage {pg_num} (offset={best_offset}):")
        print(f"  Text: {text[:60]}...")
        analyze_distribution(plain, "frequency")
    
    # What if plaintext needs to be re-arranged?
    print("\n" + "=" * 70)
    print("3. LOOKING FOR ANAGRAM/TRANSPOSITION PATTERNS")
    print("=" * 70)
    
    for pg_num in [27, 28]:
        if pg_num not in pages:
            continue
        
        cipher_indices = [rune_to_idx(r) for r in pages[pg_num]]
        plain = decrypt_with_key(cipher_indices, MASTER_KEY, 0)
        text = ''.join(idx_to_letter(p) for p in plain)
        
        n = len(text)
        print(f"\nPage {pg_num} (n={n}):")
        
        # Check for repeated patterns in plaintext
        for pattern_len in [2, 3, 4, 5]:
            patterns = {}
            for i in range(len(text) - pattern_len + 1):
                pat = text[i:i+pattern_len]
                if pat not in patterns:
                    patterns[pat] = 0
                patterns[pat] += 1
            
            repeated = {k: v for k, v in patterns.items() if v > 2}
            if repeated:
                top_repeated = sorted(repeated.items(), key=lambda x: -x[1])[:5]
                print(f"  Repeated {pattern_len}-grams: {top_repeated}")
    
    # What if pages are encoded differently?
    print("\n" + "=" * 70)
    print("4. TRYING ADDITIVE INSTEAD OF SUBTRACTIVE")
    print("=" * 70)
    
    for pg_num in [27, 28, 29]:
        if pg_num not in pages:
            continue
        
        cipher_indices = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Decrypt additively: plain = cipher + key
        plain_add = [(c + MASTER_KEY[i % 95]) % 29 for i, c in enumerate(cipher_indices)]
        text_add = ''.join(idx_to_letter(p) for p in plain_add)
        
        print(f"Page {pg_num} (additive): {text_add[:60]}...")
        
        # Decrypt with key inversion
        inv_key = [(29 - k) % 29 for k in MASTER_KEY]
        plain_inv = decrypt_with_key(cipher_indices, inv_key)
        text_inv = ''.join(idx_to_letter(p) for p in plain_inv)
        
        print(f"Page {pg_num} (inverted): {text_inv[:60]}...")

if __name__ == "__main__":
    main()

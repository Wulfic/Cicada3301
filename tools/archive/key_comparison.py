#!/usr/bin/env python3
"""
COMPARE CRACKED KEYS TO MASTER KEY

The Kasiski analysis found that key length 95 gives highest scores.
Let's compare the cracked keys to the master key to see the relationship.
"""

import re
from pathlib import Path
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

def crack_single_column(column_indices):
    """Try to crack a single column (Caesar shift)."""
    common_indices = [24, 18, 10, 9, 3, 4, 15, 16]  # A, E, I, N, O, R, S, T
    
    best_shift = 0
    best_score = 0
    
    for shift in range(29):
        shifted = [(idx - shift) % 29 for idx in column_indices]
        freqs = Counter(shifted)
        top5 = [idx for idx, count in freqs.most_common(5)]
        score = sum(1 for idx in top5 if idx in common_indices)
        
        if score > best_score:
            best_score = score
            best_shift = shift
    
    return best_shift, best_score

def crack_vigenere(indices, key_length):
    """Attempt to crack Vigenère with given key length"""
    columns = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        columns[i % key_length].append(idx)
    
    key = []
    for col in columns:
        shift, _ = crack_single_column(col)
        key.append(shift)
    
    return key

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("KEY COMPARISON: CRACKED vs MASTER")
    print("=" * 70)
    
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        indices = [rune_to_idx(r) for r in cipher]
        
        cracked_key = crack_vigenere(indices, 95)
        
        print(f"\nPage {pg_num}:")
        print(f"  Cipher length: {len(indices)}")
        
        # Compare first 30 positions
        print(f"\n  Position comparison (first 30):")
        print(f"  {'Pos':<4} {'Master':<7} {'Cracked':<8} {'Diff':<5} {'Match'}")
        print(f"  {'-'*35}")
        
        matches = 0
        diffs = []
        for i in range(30):
            m = MASTER_KEY[i]
            c = cracked_key[i]
            diff = (c - m) % 29
            match = "✓" if m == c else ""
            if m == c:
                matches += 1
            diffs.append(diff)
            print(f"  {i:<4} {m:<7} {c:<8} {diff:<5} {match}")
        
        print(f"\n  Matches in first 30: {matches}/30")
        print(f"  Differences: {diffs[:15]}...")
        
        # Check if diffs are constant (would mean just offset)
        if len(set(diffs[:15])) <= 2:
            print(f"  NOTE: Differences are mostly constant - might be offset!")
        
        # Try applying master key at different offsets
        print(f"\n  Testing master key at different offsets:")
        best_offset = 0
        best_matches = 0
        
        for offset in range(95):
            offset_matches = sum(1 for i in range(min(len(cracked_key), 95)) 
                                if cracked_key[i] == MASTER_KEY[(i + offset) % 95])
            if offset_matches > best_matches:
                best_matches = offset_matches
                best_offset = offset
        
        print(f"    Best offset: {best_offset}, matches: {best_matches}/95")
        
        # Show decryption with master key at best offset
        decrypted = []
        for i, c_idx in enumerate(indices):
            k = MASTER_KEY[(i + best_offset) % 95]
            plain_idx = (c_idx - k) % 29
            decrypted.append(idx_to_letter(plain_idx))
        
        print(f"    Decrypted (offset {best_offset}): {''.join(decrypted[:50])}...")

    print("\n" + "=" * 70)
    print("WHAT IF THE KEY IS MODIFIED BY PAGE NUMBER?")
    print("=" * 70)
    
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        indices = [rune_to_idx(r) for r in cipher]
        
        # Theory 1: Add page number to each key element
        modified_key = [(k + pg_num) % 29 for k in MASTER_KEY]
        
        decrypted = []
        for i, c_idx in enumerate(indices):
            k = modified_key[i % 95]
            plain_idx = (c_idx - k) % 29
            decrypted.append(idx_to_letter(plain_idx))
        
        print(f"\nPage {pg_num}: Key + {pg_num} (mod 29)")
        print(f"  Text: {''.join(decrypted[:50])}...")
        
        # Theory 2: XOR page number with each key element
        modified_key2 = [(k ^ pg_num) % 29 for k in MASTER_KEY]
        
        decrypted2 = []
        for i, c_idx in enumerate(indices):
            k = modified_key2[i % 95]
            plain_idx = (c_idx - k) % 29
            decrypted2.append(idx_to_letter(plain_idx))
        
        print(f"  Key XOR {pg_num}: {''.join(decrypted2[:50])}...")
        
        # Theory 3: Multiply key by page number mod 29
        modified_key3 = [(k * pg_num) % 29 for k in MASTER_KEY]
        
        decrypted3 = []
        for i, c_idx in enumerate(indices):
            k = modified_key3[i % 95]
            plain_idx = (c_idx - k) % 29
            decrypted3.append(idx_to_letter(plain_idx))
        
        print(f"  Key * {pg_num}: {''.join(decrypted3[:50])}...")

if __name__ == "__main__":
    main()

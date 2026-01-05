#!/usr/bin/env python3
"""
PERMUTED COLUMN TRANSPOSITION
==============================

The columnar transposition might have a specific column order.
Let's try all permutations of column read-order for small column counts.
"""

import re
import numpy as np
from pathlib import Path
from itertools import permutations

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def load_all_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def word_score(text):
    score = 0
    words = {
        'THE': 9, 'AND': 9, 'THAT': 12, 'HAVE': 12, 'FOR': 9, 'NOT': 9, 'WITH': 12, 'THIS': 12,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
        'FROM': 12, 'ARE': 9, 'BUT': 9, 'ONE': 9, 'ALL': 9, 'OUT': 9, 'THEIR': 15, 'THEY': 12,
        'WHAT': 12, 'WHO': 9, 'WHICH': 15, 'WHEN': 12, 'THERE': 15, 'BEEN': 12, 'SOME': 12,
        'THAN': 12, 'ONLY': 12, 'WILL': 12, 'WAY': 9, 'THROUGH': 21, 'BEING': 15, 'WHERE': 15,
        'BEFORE': 18, 'BETWEEN': 21, 'EACH': 12, 'FIND': 12, 'SELF': 12, 'MUST': 12, 'UPON': 12,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

def columnar_transpose_decrypt_perm(indices, cols, perm):
    """Decrypt columnar transposition with permuted column order"""
    n = len(indices)
    rows = (n + cols - 1) // cols
    remainder = n % cols if n % cols != 0 else cols
    
    # Calculate column lengths based on permuted order
    col_lens = []
    for c in perm:
        col_lens.append(rows if c < remainder else rows - 1)
    
    # Build column starts
    col_starts = {}
    idx = 0
    for i, c in enumerate(perm):
        col_starts[c] = idx
        idx += col_lens[i]
    
    # Read by rows with original column order
    result = []
    for r in range(rows):
        for c in range(cols):
            col_len = rows if c < remainder else rows - 1
            if r < col_len:
                source_idx = col_starts[c] + r
                if source_idx < n:
                    result.append(indices[source_idx])
    
    return np.array(result, dtype=np.int32)

def xor_decrypt(indices, key):
    n = len(indices)
    key_ext = np.tile(key, (n // len(key) + 1))[:n]
    return (indices ^ key_ext) % 29

def vigenere_decrypt(indices, key):
    n = len(indices)
    key_ext = np.tile(key, (n // len(key) + 1))[:n]
    return (indices - key_ext) % 29

def main():
    print("="*70)
    print("PERMUTED COLUMN TRANSPOSITION")
    print("="*70)
    
    pages = load_all_pages()
    p30 = runes_to_indices(pages[30])
    n = len(p30)
    
    print(f"\nPage 30: {n} runes")
    
    # Try all permutations of 4-column transposition (24 permutations)
    print("\n" + "="*70)
    print("TEST 1: 4-COLUMN PERMUTATIONS (24 total)")
    print("="*70)
    
    best_4 = (0, None, 0, "")
    for perm in permutations(range(4)):
        transposed = columnar_transpose_decrypt_perm(p30, 4, perm)
        for offset in range(len(MASTER_KEY)):
            key = np.roll(MASTER_KEY, -offset)
            xored = xor_decrypt(transposed, key)
            text = indices_to_text(xored)
            score = word_score(text)
            
            if score > best_4[0]:
                best_4 = (score, perm, offset, text)
            
            if score > 280:
                print(f"Perm={perm} Offset={offset:2d} | Score: {score}")
                print(f"  {text[:80]}")
    
    print(f"\nBest 4-col: perm={best_4[1]}, offset={best_4[2]}, score={best_4[0]}")
    print(f"  {best_4[3][:80]}")
    
    # Try 5-column permutations (120 total)
    print("\n" + "="*70)
    print("TEST 2: 5-COLUMN PERMUTATIONS (120 total)")
    print("="*70)
    
    best_5 = (0, None, 0, "")
    for perm in permutations(range(5)):
        transposed = columnar_transpose_decrypt_perm(p30, 5, perm)
        for offset in range(len(MASTER_KEY)):
            key = np.roll(MASTER_KEY, -offset)
            xored = xor_decrypt(transposed, key)
            text = indices_to_text(xored)
            score = word_score(text)
            
            if score > best_5[0]:
                best_5 = (score, perm, offset, text)
    
    print(f"Best 5-col: perm={best_5[1]}, offset={best_5[2]}, score={best_5[0]}")
    print(f"  {best_5[3][:80]}")
    
    # Try Vigenère instead of XOR
    print("\n" + "="*70)
    print("TEST 3: COLUMNAR + VIGENÈRE (instead of XOR)")
    print("="*70)
    
    best_vig = (0, 0, 0, "")
    for cols in range(2, 15):
        transposed = columnar_transpose_decrypt_perm(p30, cols, tuple(range(cols)))
        for offset in range(len(MASTER_KEY)):
            key = np.roll(MASTER_KEY, -offset)
            dec = vigenere_decrypt(transposed, key)
            text = indices_to_text(dec)
            score = word_score(text)
            
            if score > best_vig[0]:
                best_vig = (score, cols, offset, text)
            
            if score > 280:
                print(f"Cols={cols:2d} Offset={offset:2d} | Score: {score}")
                print(f"  {text[:80]}")
    
    print(f"\nBest Vigenère: cols={best_vig[1]}, offset={best_vig[2]}, score={best_vig[0]}")
    print(f"  {best_vig[3][:80]}")
    
    # Try prime number column counts
    print("\n" + "="*70)
    print("TEST 4: PRIME NUMBER COLUMN COUNTS")
    print("="*70)
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    
    for cols in primes:
        if cols >= n:
            continue
        transposed = columnar_transpose_decrypt_perm(p30, cols, tuple(range(cols)))
        for offset in range(len(MASTER_KEY)):
            key = np.roll(MASTER_KEY, -offset)
            xored = xor_decrypt(transposed, key)
            text = indices_to_text(xored)
            score = word_score(text)
            
            if score > 250:
                print(f"Cols={cols:2d} (prime) Offset={offset:2d} | Score: {score}")
                print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

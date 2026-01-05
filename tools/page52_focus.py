#!/usr/bin/env python3
"""
FOCUSED PAGE 52 ANALYSIS

Page 52 at offset 72 shows: THE, AND, ARE at positions 3, 32, 39
This is very promising - let's see if we can find more structure.
"""

import re
from pathlib import Path
import math

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

def decrypt_with_offset(cipher_indices, offset):
    result = []
    for i, c in enumerate(cipher_indices):
        k = MASTER_KEY[(i + offset) % 95]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def read_in_columns(text, cols):
    """Read text column by column instead of row by row"""
    rows = math.ceil(len(text) / cols)
    padded = text + ' ' * (rows * cols - len(text))
    
    result = []
    for col in range(cols):
        for row in range(rows):
            idx = row * cols + col
            if idx < len(text):
                result.append(text[idx])
    return ''.join(result)

def read_by_column(text, cols):
    """Inverse: text was written column-wise, read row-wise"""
    rows = math.ceil(len(text) / cols)
    result = [''] * len(text)
    idx = 0
    for col in range(cols):
        for row in range(rows):
            pos = row * cols + col
            if pos < len(text) and idx < len(text):
                result[pos] = text[idx]
                idx += 1
    return ''.join(result)

def word_score(text):
    WORDS = {'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
             'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
             'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
             'YOU', 'WE', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
             'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
             'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("FOCUSED ANALYSIS: PAGE 52")
    print("=" * 70)
    
    cipher = [rune_to_idx(r) for r in pages[52]]
    n = len(cipher)
    
    print(f"Page 52: {n} runes = {n} characters")
    print(f"Prime factorization: 263 is prime")
    
    # Decrypt at offset 72 (best word match)
    text = decrypt_with_offset(cipher, 72)
    print(f"\nDecrypted at offset 72:")
    print(f"  {text}")
    
    print("\n" + "-" * 60)
    print("TRYING TRANSPOSITIONS ON DECRYPTED TEXT")
    print("-" * 60)
    
    best_score = 0
    best_config = None
    
    for cols in range(2, 50):
        # Try reading column-wise
        transposed = read_in_columns(text, cols)
        score = word_score(transposed)
        if score > best_score:
            best_score = score
            best_config = ('col_read', cols, transposed)
        
        # Try inverse column
        transposed = read_by_column(text, cols)
        score = word_score(transposed)
        if score > best_score:
            best_score = score
            best_config = ('col_write', cols, transposed)
    
    # Try reverse
    reversed_text = text[::-1]
    score = word_score(reversed_text)
    if score > best_score:
        best_score = score
        best_config = ('reverse', 0, reversed_text)
    
    if best_config:
        method, param, result = best_config
        print(f"Best: {method}({param}), score={best_score}")
        print(f"Result: {result[:100]}...")
    
    print("\n" + "=" * 70)
    print("ANALYZING ALL PAGES AT THEIR BEST OFFSETS")
    print("=" * 70)
    
    # Best offsets from previous analysis
    best_offsets = {
        27: 59, 28: 13, 29: 91, 30: 1, 31: 9,
        40: 81, 41: 49, 44: 23, 45: 50, 46: 56,
        47: 67, 48: 12, 52: 72
    }
    
    for pg_num, offset in best_offsets.items():
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        text = decrypt_with_offset(cipher, offset)
        
        # Find the relationship between page number and offset
        print(f"Page {pg_num}: offset={offset}, diff={pg_num - offset}, sum={pg_num + offset}")
    
    print("\n" + "=" * 70)
    print("PATTERN ANALYSIS: OFFSET VS PAGE NUMBER")
    print("=" * 70)
    
    # Check if there's a formula: offset = f(page_number)
    for pg_num, offset in sorted(best_offsets.items()):
        # Check various transformations
        mod29 = pg_num % 29
        mod95 = pg_num % 95
        times2 = (pg_num * 2) % 95
        times3 = (pg_num * 3) % 95
        plus_k = [(pg_num + k) % 95 for k in range(10)]
        
        # Find which transformation matches offset
        match = ""
        if mod95 == offset:
            match = f"offset = page mod 95"
        elif offset in plus_k:
            k = plus_k.index(offset)
            if k > 0:
                match = f"offset = (page + {k}) mod 95"
        
        for mult in range(1, 10):
            if (pg_num * mult) % 95 == offset:
                match = f"offset = (page * {mult}) mod 95"
                break
        
        print(f"Page {pg_num}: offset={offset}, {match if match else 'no simple formula'}")

if __name__ == "__main__":
    main()

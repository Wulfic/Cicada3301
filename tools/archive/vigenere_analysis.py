#!/usr/bin/env python3
"""
COMPREHENSIVE VIGENERE CIPHER TEST
==================================

Maybe it's Vigenère (repeating key) instead of autokey.
Test many key lengths and find the best decryptions.
"""

import re
import numpy as np
from pathlib import Path
from itertools import product
from collections import Counter

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

# English letter frequencies (approximate for this alphabet)
# We focus on the single letters: F U O R C G W H N I J P X S T B E M L D A Y
# High freq: E T A O I N S R H L
# Mapped: E(18), T(16), A(24), O(3), I(10), N(9), S(15), R(4), H(8), L(20)
ENGLISH_FREQ = {
    0: 0.022,  # F
    1: 0.028,  # U
    2: 0.020,  # TH
    3: 0.075,  # O
    4: 0.060,  # R
    5: 0.028,  # C
    6: 0.020,  # G
    7: 0.024,  # W
    8: 0.061,  # H
    9: 0.067,  # N
    10: 0.070, # I
    11: 0.001, # J
    12: 0.015, # EO
    13: 0.019, # P
    14: 0.001, # X
    15: 0.063, # S
    16: 0.091, # T
    17: 0.015, # B
    18: 0.127, # E (highest!)
    19: 0.024, # M
    20: 0.040, # L
    21: 0.010, # NG
    22: 0.010, # OE
    23: 0.043, # D
    24: 0.082, # A
    25: 0.015, # AE
    26: 0.020, # Y
    27: 0.005, # IA
    28: 0.010, # EA
}

def word_to_indices(word):
    word = word.upper()
    indices = []
    i = 0
    while i < len(word):
        if i + 1 < len(word):
            digraph = word[i:i+2]
            if digraph in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        letter = word[i]
        if letter == 'K': letter = 'C'
        if letter == 'Q': letter = 'C'
        if letter == 'V': letter = 'U'
        if letter == 'Z': letter = 'S'
        if letter in LETTER_TO_IDX:
            indices.append(LETTER_TO_IDX[letter])
        i += 1
    return np.array(indices, dtype=np.int32)

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

def vigenere_decrypt(indices, key):
    """Vigenère decryption with repeating key"""
    key_len = len(key)
    result = np.zeros(len(indices), dtype=np.int32)
    for i in range(len(indices)):
        result[i] = (indices[i] - key[i % key_len]) % 29
    return result

def chi_squared_score(indices):
    """Chi-squared test for English-like distribution"""
    counts = Counter(indices)
    n = len(indices)
    chi_sq = 0.0
    for i in range(29):
        expected = n * ENGLISH_FREQ.get(i, 0.01)
        observed = counts.get(i, 0)
        chi_sq += ((observed - expected) ** 2) / expected
    # Lower is better for chi-squared
    return -chi_sq  # Return negative so higher is better

def word_score(text):
    """Score based on English words found"""
    score = 0
    words = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
             'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
             'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO',
             'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
             'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM']
    for word in words:
        count = text.count(word)
        score += count * len(word) * 3
    return score

def find_best_key_length(indices, max_len=20):
    """Use Index of Coincidence to find probable key length"""
    n = len(indices)
    ic_scores = []
    
    for key_len in range(1, min(max_len + 1, n // 2)):
        total_ic = 0.0
        for offset in range(key_len):
            # Get every key_len-th character starting at offset
            slice_indices = [indices[i] for i in range(offset, n, key_len)]
            if len(slice_indices) < 2:
                continue
            counts = Counter(slice_indices)
            m = len(slice_indices)
            ic = sum(c * (c - 1) for c in counts.values()) / (m * (m - 1)) if m > 1 else 0
            total_ic += ic
        avg_ic = total_ic / key_len
        ic_scores.append((key_len, avg_ic))
    
    # English IC is around 0.065-0.070, random is 1/29 ≈ 0.034
    return sorted(ic_scores, key=lambda x: -x[1])

def recover_key_for_length(indices, key_len):
    """Given key length, find most likely key by frequency analysis"""
    n = len(indices)
    key = []
    
    for offset in range(key_len):
        slice_indices = [indices[i] for i in range(offset, n, key_len)]
        if not slice_indices:
            key.append(0)
            continue
        
        # Try each possible key value and find the one giving best chi-squared
        best_k = 0
        best_score = float('-inf')
        for k in range(29):
            decrypted = [(x - k) % 29 for x in slice_indices]
            score = chi_squared_score(decrypted)
            if score > best_score:
                best_score = score
                best_k = k
        key.append(best_k)
    
    return np.array(key, dtype=np.int32)

def main():
    print("="*70)
    print("COMPREHENSIVE VIGENÈRE CIPHER ANALYSIS")
    print("="*70)
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("\n" + "="*70)
    print("INDEX OF COINCIDENCE ANALYSIS FOR KEY LENGTH")
    print("="*70)
    
    for pg_num in unsolved[:5]:  # Analyze first 5 pages
        pg_idx = runes_to_indices(pages[pg_num])
        ic_scores = find_best_key_length(pg_idx, max_len=30)
        
        print(f"\nPage {pg_num} - Top 5 key lengths by IC:")
        for key_len, ic in ic_scores[:5]:
            print(f"  Key length {key_len:2d}: IC = {ic:.4f}")
    
    print("\n" + "="*70)
    print("FREQUENCY-BASED KEY RECOVERY")
    print("="*70)
    
    results = []
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Try key lengths from 1 to 20
        for key_len in range(1, 21):
            key = recover_key_for_length(pg_idx, key_len)
            decrypted = vigenere_decrypt(pg_idx, key)
            text = indices_to_text(decrypted)
            score = word_score(text)
            
            if score > 100:
                key_str = indices_to_text(key)
                results.append((pg_num, key_len, key_str, score, text[:80]))
    
    results.sort(key=lambda x: -x[3])
    
    print("\nTop Vigenère decryptions by word score (>100):")
    for pg, klen, key_str, score, text in results[:20]:
        print(f"\nPage {pg} | Key length {klen} | Key: {key_str[:20]}... | Score: {score}")
        print(f"  {text}")
    
    # Try specific word keys
    print("\n" + "="*70)
    print("VIGENÈRE WITH WORD KEYS")
    print("="*70)
    
    word_keys = [
        "DIVINITY", "PARABLE", "INSTAR", "TRUTH", "WISDOM", "CICADA",
        "PRIME", "EMERGE", "SURFACE", "PILGRIM", "SHED", "CIRCUMFERENCE",
        "THE", "AND", "FOR", "THELEMA", "NUIT", "HADIT", "CROWLEY",
        "LIBER", "PRIMUS", "LIBERPRIMUS", "CONSCIOUSNESS", "ENLIGHTENMENT",
        "THIRTEENELEVEN", "THREETHREE", "ELEVEN", "THIRTEEN", "SEVENTEEN"
    ]
    
    word_results = []
    
    for word in word_keys:
        key = word_to_indices(word)
        if len(key) == 0:
            continue
        
        for pg_num in unsolved:
            pg_idx = runes_to_indices(pages[pg_num])
            decrypted = vigenere_decrypt(pg_idx, key)
            text = indices_to_text(decrypted)
            score = word_score(text)
            
            if score > 50:
                word_results.append((word, pg_num, score, text[:80]))
    
    word_results.sort(key=lambda x: -x[2])
    
    print("\nTop word-key Vigenère decryptions:")
    for word, pg, score, text in word_results[:20]:
        print(f"\nKey: {word:20s} | Page {pg} | Score: {score}")
        print(f"  {text}")
    
    # Try the MASTER KEY as Vigenère key
    print("\n" + "="*70)
    print("USING MASTER KEY AS VIGENÈRE KEY")
    print("="*70)
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Use master key as repeating Vigenère key
        decrypted = vigenere_decrypt(pg_idx, MASTER_KEY)
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"\nPage {pg_num} | Score: {score}")
        print(f"  {text[:100]}")
    
    # Try first N characters of master key
    print("\n" + "="*70)
    print("PARTIAL MASTER KEY AS VIGENÈRE")
    print("="*70)
    
    partial_results = []
    
    for key_len in range(1, 30):
        partial_key = MASTER_KEY[:key_len]
        
        for pg_num in unsolved:
            pg_idx = runes_to_indices(pages[pg_num])
            decrypted = vigenere_decrypt(pg_idx, partial_key)
            text = indices_to_text(decrypted)
            score = word_score(text)
            
            if score > 100:
                partial_results.append((key_len, pg_num, score, text[:80]))
    
    partial_results.sort(key=lambda x: -x[2])
    
    print("\nPartial master key Vigenère (top results):")
    for klen, pg, score, text in partial_results[:15]:
        print(f"\nKey length {klen} | Page {pg} | Score: {score}")
        print(f"  {text}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GEMATRIA PRIME KEY TESTING
===========================

Test using the actual Gematria Primus prime VALUES as the key,
not just the indices.
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Gematria Primus prime values (F=2, U=3, TH=5, O=7, ...)
GEMATRIA = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                      53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109], dtype=np.int32)

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_gematria(indices):
    """Convert rune indices to their Gematria prime values"""
    return GEMATRIA[indices]

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
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

# Master key indices and their Gematria values
MASTER_KEY_IDX = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

# Convert master key to Gematria values
MASTER_KEY_GEMATRIA = GEMATRIA[MASTER_KEY_IDX]

def main():
    print("="*70)
    print("GEMATRIA PRIME KEY TESTING")
    print("="*70)
    
    print("\nMaster Key as indices (first 20):")
    print(list(MASTER_KEY_IDX[:20]))
    
    print("\nMaster Key as Gematria primes (first 20):")
    print(list(MASTER_KEY_GEMATRIA[:20]))
    
    print(f"\nSum of master key indices: {sum(MASTER_KEY_IDX)} = 11³ = 1331")
    print(f"Sum of master key Gematria: {sum(MASTER_KEY_GEMATRIA)}")
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Test 1: Use Gematria values for subtraction (mod 29)
    print("\n" + "="*70)
    print("TEST 1: GEMATRIA KEY SUBTRACTION (mod 29)")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        best = (0, 0, "")
        for offset in range(len(MASTER_KEY_GEMATRIA)):
            key = np.tile(np.roll(MASTER_KEY_GEMATRIA, -offset), (n // len(MASTER_KEY_GEMATRIA) + 1))[:n]
            dec = (pg_idx - key) % 29
            text = indices_to_text(dec)
            score = word_score(text)
            
            if score > best[0]:
                best = (score, offset, text)
        
        print(f"Page {pg_num}: offset={best[1]:2d} | Score: {best[0]}")
        print(f"  {best[2][:80]}")
    
    # Test 2: Convert ciphertext to Gematria, subtract key, convert back
    print("\n" + "="*70)
    print("TEST 2: GEMATRIA DOMAIN SUBTRACTION")
    print("="*70)
    
    # In this test, we operate in the Gematria domain:
    # 1. Convert cipher indices to Gematria values
    # 2. Subtract key (which is also Gematria)
    # 3. Find nearest Gematria value
    
    for pg_num in [30, 47]:  # Test on best pages
        pg_idx = runes_to_indices(pages[pg_num])
        pg_gem = indices_to_gematria(pg_idx)
        n = len(pg_idx)
        
        best = (0, 0, "")
        for offset in range(len(MASTER_KEY_GEMATRIA)):
            key = np.tile(np.roll(MASTER_KEY_GEMATRIA, -offset), (n // len(MASTER_KEY_GEMATRIA) + 1))[:n]
            
            # Subtract in Gematria domain
            result_gem = pg_gem - key
            
            # Find closest Gematria value for each result
            dec = []
            for g in result_gem:
                # Find index of closest Gematria value
                diffs = np.abs(GEMATRIA - (g % 113))  # Modulo by sum of all primes or some value
                dec.append(np.argmin(diffs))
            
            text = indices_to_text(np.array(dec))
            score = word_score(text)
            
            if score > best[0]:
                best = (score, offset, text)
        
        print(f"Page {pg_num}: offset={best[1]:2d} | Score: {best[0]}")
        print(f"  {best[2][:80]}")
    
    # Test 3: XOR in Gematria domain
    print("\n" + "="*70)
    print("TEST 3: GEMATRIA XOR")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        pg_gem = indices_to_gematria(pg_idx)
        n = len(pg_idx)
        
        best = (0, 0, "")
        for offset in range(len(MASTER_KEY_GEMATRIA)):
            key = np.tile(np.roll(MASTER_KEY_GEMATRIA, -offset), (n // len(MASTER_KEY_GEMATRIA) + 1))[:n]
            
            # XOR in Gematria domain
            result_gem = pg_gem ^ key
            
            # Find closest Gematria value
            dec = []
            for g in result_gem:
                diffs = np.abs(GEMATRIA - (g % 113))
                dec.append(np.argmin(diffs))
            
            text = indices_to_text(np.array(dec))
            score = word_score(text)
            
            if score > best[0]:
                best = (score, offset, text)
        
        print(f"Page {pg_num}: offset={best[1]:2d} | Score: {best[0]}")
        print(f"  {best[2][:80]}")
    
    # Test 4: Use the SUM of Gematria values (1331)
    print("\n" + "="*70)
    print("TEST 4: USING SUM OF KEY (1331) AS MODULUS")
    print("="*70)
    
    for pg_num in [30, 47]:
        pg_idx = runes_to_indices(pages[pg_num])
        pg_gem = indices_to_gematria(pg_idx)
        n = len(pg_idx)
        
        best = (0, 0, "")
        for offset in range(len(MASTER_KEY_IDX)):
            key = np.tile(np.roll(MASTER_KEY_IDX, -offset), (n // len(MASTER_KEY_IDX) + 1))[:n]
            
            # Subtract and mod 1331, then reduce to 0-28
            result = (pg_gem - GEMATRIA[key]) % 1331
            dec = result % 29
            
            text = indices_to_text(dec)
            score = word_score(text)
            
            if score > best[0]:
                best = (score, offset, text)
        
        print(f"Page {pg_num}: offset={best[1]:2d} | Score: {best[0]}")
        print(f"  {best[2][:80]}")

if __name__ == "__main__":
    main()

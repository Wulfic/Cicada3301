#!/usr/bin/env python3
"""
MULTI-LAYER CIPHER TESTS
========================

Try combinations:
1. Affine → then Master Key Vigenère
2. Master Key Vigenère → then Affine
3. Affine → Transposition
4. Different combinations
"""

import re
import numpy as np
from pathlib import Path
from math import gcd
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

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(indices, a, b):
    a_inv = mod_inverse(a, 29)
    if a_inv is None:
        return None
    return np.array([(a_inv * (x - b)) % 29 for x in indices], dtype=np.int32)

def vigenere_decrypt(indices, key):
    key_len = len(key)
    return np.array([(indices[i] - key[i % key_len]) % 29 for i in range(len(indices))], dtype=np.int32)

def caesar_decrypt(indices, shift):
    return (indices - shift) % 29

def word_score(text):
    score = 0
    words = {'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
             'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
             'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO',
             'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
             'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM'}
    for word in words:
        count = text.count(word)
        score += count * len(word) * 3
    return score

def main():
    print("="*70)
    print("MULTI-LAYER CIPHER COMBINATIONS")
    print("="*70)
    
    pages = load_all_pages()
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    valid_a = [a for a in range(1, 29) if gcd(a, 29) == 1]
    
    # Test 1: Affine → Master Key
    print("\n" + "="*70)
    print("TEST 1: AFFINE → MASTER KEY VIGENÈRE")
    print("="*70)
    
    results = []
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        for a in valid_a:
            for b in range(29):
                step1 = affine_decrypt(pg_idx, a, b)
                if step1 is None:
                    continue
                step2 = vigenere_decrypt(step1, MASTER_KEY)
                text = indices_to_text(step2)
                score = word_score(text)
                if score > 200:
                    results.append((pg_num, a, b, "affine→vig", score, text[:60]))
    
    results.sort(key=lambda x: -x[4])
    for pg, a, b, method, score, text in results[:15]:
        print(f"Page {pg} | a={a:2d} b={b:2d} | {score:3d} | {text}")
    
    # Test 2: Master Key → Affine
    print("\n" + "="*70)
    print("TEST 2: MASTER KEY VIGENÈRE → AFFINE")
    print("="*70)
    
    results = []
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        step1 = vigenere_decrypt(pg_idx, MASTER_KEY)
        
        for a in valid_a:
            for b in range(29):
                step2 = affine_decrypt(step1, a, b)
                if step2 is None:
                    continue
                text = indices_to_text(step2)
                score = word_score(text)
                if score > 200:
                    results.append((pg_num, a, b, "vig→affine", score, text[:60]))
    
    results.sort(key=lambda x: -x[4])
    for pg, a, b, method, score, text in results[:15]:
        print(f"Page {pg} | a={a:2d} b={b:2d} | {score:3d} | {text}")
    
    # Test 3: Caesar + Master Key combinations
    print("\n" + "="*70)
    print("TEST 3: CAESAR → MASTER KEY")
    print("="*70)
    
    results = []
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        for shift in range(29):
            step1 = caesar_decrypt(pg_idx, shift)
            step2 = vigenere_decrypt(step1, MASTER_KEY)
            text = indices_to_text(step2)
            score = word_score(text)
            if score > 200:
                results.append((pg_num, shift, "caesar→vig", score, text[:60]))
    
    results.sort(key=lambda x: -x[3])
    for pg, shift, method, score, text in results[:15]:
        print(f"Page {pg} | shift={shift:2d} | {score:3d} | {text}")
    
    # Test 4: Atbash + Master Key
    print("\n" + "="*70)
    print("TEST 4: ATBASH → MASTER KEY")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Atbash: swap 0↔28, 1↔27, etc.
        step1 = (28 - pg_idx) % 29
        step2 = vigenere_decrypt(step1, MASTER_KEY)
        text = indices_to_text(step2)
        score = word_score(text)
        
        if score > 150:
            print(f"Page {pg_num} | {score:3d} | {text[:60]}")
    
    # Test 5: Try known good affine params with additional Caesar shift
    print("\n" + "="*70)
    print("TEST 5: AFFINE (best params) → CAESAR")
    print("="*70)
    
    best_params = {
        30: (7, 10),
        46: (2, 25),
        29: (6, 27),
        48: (7, 7),
    }
    
    for pg_num, (a, b) in best_params.items():
        pg_idx = runes_to_indices(pages[pg_num])
        step1 = affine_decrypt(pg_idx, a, b)
        
        for shift in range(29):
            step2 = caesar_decrypt(step1, shift)
            text = indices_to_text(step2)
            score = word_score(text)
            
            if score > 200:
                print(f"Page {pg_num} | a={a} b={b} → shift={shift} | {score:3d} | {text[:60]}")
    
    # Test 6: XOR the page with master key (bitwise on indices)
    print("\n" + "="*70)
    print("TEST 6: XOR WITH MASTER KEY")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        for offset in range(len(MASTER_KEY)):
            key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
            xored = (pg_idx ^ key) % 29
            text = indices_to_text(xored)
            score = word_score(text)
            
            if score > 150:
                print(f"Page {pg_num} | offset={offset} | {score:3d} | {text[:60]}")

if __name__ == "__main__":
    main()

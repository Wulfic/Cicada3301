#!/usr/bin/env python3
"""
EXHAUSTIVE NO-KEY BRUTE FORCE
=============================

Since the master key approach hasn't worked, let's try ALL possible simple ciphers
without relying on any key at all:

1. Simple Caesar shift (all 29 rotations)
2. Simple XOR with a single value (all 29 values)
3. Atbash (reverse alphabet)
4. All columnar transpositions (all widths 2-20)
5. Skip ciphers (skip patterns)
6. Autokey variants
7. Running key with known texts

This uses massive parallelism to test everything quickly.
"""

import re
import numpy as np
from pathlib import Path
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import itertools

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

# English text scoring
COMMON_WORDS = {'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
                'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
                'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO',
                'ARE', 'BUT', 'OUT', 'ALL', 'WHO', 'CAN', 'HAS', 'ONE', 'OUR',
                'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL', 'FROM', 'EACH', 'WHICH'}
CICADA_WORDS = {'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
                'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM',
                'SELF', 'MIND', 'CONSCIOUSNESS', 'ENLIGHTENMENT', 'PILGRIM'}

# English letter frequencies (normalized for 29-letter alphabet)
ENGLISH_FREQ = np.array([
    0.02,  # F
    0.03,  # U  
    0.10,  # TH (common)
    0.08,  # O
    0.06,  # R
    0.02,  # C
    0.02,  # G
    0.02,  # W
    0.06,  # H
    0.07,  # N
    0.07,  # I
    0.00,  # J (rare)
    0.00,  # EO (rare)
    0.02,  # P
    0.00,  # X (rare)
    0.06,  # S
    0.09,  # T
    0.01,  # B
    0.13,  # E (most common)
    0.02,  # M
    0.04,  # L
    0.02,  # NG
    0.00,  # OE (rare)
    0.04,  # D
    0.08,  # A
    0.01,  # AE
    0.02,  # Y
    0.00,  # IA (rare)
    0.00,  # EA (rare)
])

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

def score_text(text):
    """Score how English-like the text is"""
    score = 0
    
    # Word detection
    for word in COMMON_WORDS:
        count = text.count(word)
        score += count * len(word) * 2
    for word in CICADA_WORDS:
        count = text.count(word)
        score += count * len(word) * 5  # Bonus for Cicada words
    
    # Frequency analysis - bonus for English-like distribution
    indices = [LETTERS.index(text[i:i+2]) if i+1 < len(text) and text[i:i+2] in LETTERS 
               else (LETTERS.index(text[i]) if text[i] in 'FUORCGWHNIJPXSTBEMLDAYF' and text[i] in [L[0] if len(L)==1 else '' for L in LETTERS] else -1) 
               for i in range(len(text))]
    
    return score

def score_indices(indices):
    """Score how English-like the indices are using n-gram patterns"""
    if len(indices) < 2:
        return 0
    
    text = indices_to_text(indices)
    score = 0
    
    # Common English 2-letter combinations
    common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND',
                      'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR']
    for bg in common_bigrams:
        score += text.count(bg) * 2
    
    # Common words
    for word in COMMON_WORDS:
        count = text.count(word)
        score += count * len(word) * 3
    
    for word in CICADA_WORDS:
        count = text.count(word)
        score += count * len(word) * 10
    
    # Check for THE - most important word
    score += text.count('THE') * 15
    
    return score

# ============== CIPHER TESTS ==============

def test_caesar(indices, shift):
    """Simple Caesar shift"""
    return (indices - shift) % 29

def test_xor_single(indices, value):
    """XOR with single value"""
    return indices ^ value

def test_atbash(indices):
    """Atbash: reverse the alphabet"""
    return (28 - indices) % 29

def test_columnar(indices, width):
    """Columnar transposition with given width"""
    n = len(indices)
    rows = (n + width - 1) // width
    padded = np.pad(indices, (0, rows * width - n), mode='constant', constant_values=0)
    matrix = padded.reshape(rows, width)
    return matrix.T.flatten()[:n]

def test_columnar_reverse(indices, width):
    """Reverse columnar transposition"""
    n = len(indices)
    rows = (n + width - 1) // width
    # Read down columns
    result = []
    padded = np.pad(indices, (0, rows * width - n), mode='constant', constant_values=0)
    matrix = padded.reshape(width, rows).T
    return matrix.flatten()[:n]

def test_skip(indices, skip):
    """Skip cipher with given skip value"""
    n = len(indices)
    result = np.zeros(n, dtype=np.int32)
    pos = 0
    for i in range(n):
        result[i] = indices[pos]
        pos = (pos + skip) % n
    return result

def test_affine(indices, a, b):
    """Affine cipher: x -> ax + b mod 29"""
    return (a * indices + b) % 29

def test_double_shift(indices, shift1, shift2):
    """Apply two shifts with interleaving"""
    result = np.zeros_like(indices)
    result[0::2] = (indices[0::2] - shift1) % 29
    result[1::2] = (indices[1::2] - shift2) % 29
    return result

def test_polyalphabetic(indices, key):
    """Polyalphabetic with short key"""
    key_arr = np.array(key, dtype=np.int32)
    extended = np.tile(key_arr, (len(indices) // len(key_arr) + 1))[:len(indices)]
    return (indices - extended) % 29

# ============== MAIN TESTING ==============

def test_page_single(args):
    """Test a single cipher on a page"""
    pg_num, indices, cipher_type, params = args
    
    try:
        if cipher_type == 'caesar':
            decrypted = test_caesar(indices, params[0])
        elif cipher_type == 'xor':
            decrypted = test_xor_single(indices, params[0])
        elif cipher_type == 'atbash':
            decrypted = test_atbash(indices)
        elif cipher_type == 'columnar':
            decrypted = test_columnar(indices, params[0])
        elif cipher_type == 'columnar_rev':
            decrypted = test_columnar_reverse(indices, params[0])
        elif cipher_type == 'skip':
            decrypted = test_skip(indices, params[0])
        elif cipher_type == 'affine':
            decrypted = test_affine(indices, params[0], params[1])
        elif cipher_type == 'double':
            decrypted = test_double_shift(indices, params[0], params[1])
        elif cipher_type == 'poly':
            decrypted = test_polyalphabetic(indices, params)
        else:
            return None
        
        score = score_indices(decrypted)
        text = indices_to_text(decrypted)
        
        if score > 50:
            return (pg_num, cipher_type, params, score, text[:100])
    except:
        pass
    return None

def main():
    print("="*70)
    print("EXHAUSTIVE NO-KEY BRUTE FORCE")
    print("="*70)
    
    pages = load_all_pages()
    
    # Unsolved pages
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print(f"\nTesting {len(unsolved)} unsolved pages with ALL simple ciphers...")
    
    all_tests = []
    
    for pg_num in unsolved:
        indices = runes_to_indices(pages[pg_num])
        
        # 1. Caesar shifts (29 tests)
        for shift in range(29):
            all_tests.append((pg_num, indices, 'caesar', (shift,)))
        
        # 2. XOR single (29 tests)
        for val in range(29):
            all_tests.append((pg_num, indices, 'xor', (val,)))
        
        # 3. Atbash (1 test)
        all_tests.append((pg_num, indices, 'atbash', ()))
        
        # 4. Columnar transposition (widths 2-20)
        for width in range(2, 21):
            all_tests.append((pg_num, indices, 'columnar', (width,)))
            all_tests.append((pg_num, indices, 'columnar_rev', (width,)))
        
        # 5. Skip cipher (various skip values)
        for skip in range(2, 30):
            if skip < len(indices):
                all_tests.append((pg_num, indices, 'skip', (skip,)))
        
        # 6. Affine (a must be coprime with 29 - since 29 is prime, any a works)
        for a in range(1, 29):
            for b in range(29):
                all_tests.append((pg_num, indices, 'affine', (a, b)))
        
        # 7. Double shift (interleaved)
        for s1 in range(29):
            for s2 in range(29):
                all_tests.append((pg_num, indices, 'double', (s1, s2)))
        
        # 8. Short polyalphabetic keys (2-5 length)
        for key_len in range(2, 6):
            for key in itertools.product(range(0, 29, 3), repeat=key_len):  # Sample
                all_tests.append((pg_num, indices, 'poly', key))
    
    print(f"Total tests to run: {len(all_tests):,}")
    
    # Run tests
    results = []
    
    num_workers = multiprocessing.cpu_count()
    print(f"Using {num_workers} workers...")
    
    batch_size = 10000
    for i in range(0, len(all_tests), batch_size):
        batch = all_tests[i:i+batch_size]
        
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            for result in executor.map(test_page_single, batch):
                if result is not None:
                    results.append(result)
        
        print(f"Progress: {min(i+batch_size, len(all_tests)):,}/{len(all_tests):,} ({len(results)} hits so far)")
    
    # Sort results by score
    results.sort(key=lambda x: -x[3])
    
    print("\n" + "="*70)
    print("TOP RESULTS")
    print("="*70)
    
    for pg, cipher, params, score, text in results[:50]:
        print(f"\nPage {pg} | {cipher} | params={params} | Score={score}")
        print(f"  {text}")
    
    # Save results
    with open('tools/archive/outputs/no_key_results.txt', 'w', encoding='utf-8') as f:
        for pg, cipher, params, score, text in results:
            f.write(f"Page {pg} | {cipher} | params={params} | Score={score}\n")
            f.write(f"  {text}\n\n")
    
    print(f"\nSaved {len(results)} results to tools/archive/outputs/no_key_results.txt")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
COMPREHENSIVE BRUTE FORCE - ALL COMBINATIONS
=============================================

Testing every possible cipher combination systematically.
"""

import re
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def affine_decrypt(indices, a, b):
    a_inv = mod_inverse(a, 29)
    if a_inv is None:
        return None
    return (a_inv * (indices - b)) % 29

def vigenere_decrypt(indices, key):
    n = len(indices)
    key_ext = np.tile(key, (n // len(key) + 1))[:n]
    return (indices - key_ext) % 29

def xor_decrypt(indices, key):
    n = len(indices)
    key_ext = np.tile(key, (n // len(key) + 1))[:n]
    return (indices ^ key_ext) % 29

def columnar_transpose_decrypt(indices, cols):
    n = len(indices)
    rows = (n + cols - 1) // cols
    remainder = n % cols if n % cols != 0 else cols
    
    result = np.zeros(n, dtype=np.int32)
    idx = 0
    col_starts = []
    
    for c in range(cols):
        col_len = rows if c < remainder else rows - 1
        col_starts.append(idx)
        idx += col_len
    
    idx = 0
    for r in range(rows):
        for c in range(cols):
            col_len = rows if c < remainder else rows - 1
            if r < col_len:
                source_idx = col_starts[c] + r
                if source_idx < n and idx < n:
                    result[idx] = indices[source_idx]
                    idx += 1
    
    return result

def test_all_combinations(page_data):
    pg_num, page_runes = page_data
    pg_idx = runes_to_indices(page_runes)
    n = len(pg_idx)
    
    results = []
    
    # 1. Affine only
    for a in range(1, 29):
        if gcd(a, 29) != 1:
            continue
        for b in range(29):
            dec = affine_decrypt(pg_idx, a, b)
            if dec is not None:
                text = indices_to_text(dec)
                score = word_score(text)
                if score > 180:
                    results.append((score, f"Affine a={a} b={b}", text[:80]))
    
    # 2. XOR with master key at different offsets
    for offset in range(len(MASTER_KEY)):
        key = np.roll(MASTER_KEY, -offset)
        dec = xor_decrypt(pg_idx, key)
        text = indices_to_text(dec)
        score = word_score(text)
        if score > 180:
            results.append((score, f"XOR offset={offset}", text[:80]))
    
    # 3. XOR then transpose
    for offset in range(len(MASTER_KEY)):
        key = np.roll(MASTER_KEY, -offset)
        dec = xor_decrypt(pg_idx, key)
        for cols in range(2, 30):
            trans = columnar_transpose_decrypt(dec, cols)
            text = indices_to_text(trans)
            score = word_score(text)
            if score > 220:
                results.append((score, f"XOR offset={offset} → Cols={cols}", text[:80]))
    
    # 4. Transpose then XOR
    for cols in range(2, 30):
        trans = columnar_transpose_decrypt(pg_idx, cols)
        for offset in range(len(MASTER_KEY)):
            key = np.roll(MASTER_KEY, -offset)
            dec = xor_decrypt(trans, key)
            text = indices_to_text(dec)
            score = word_score(text)
            if score > 220:
                results.append((score, f"Cols={cols} → XOR offset={offset}", text[:80]))
    
    # 5. Affine then Vigenere
    for a in [7, 11, 13]:
        for b in range(29):
            dec = affine_decrypt(pg_idx, a, b)
            if dec is not None:
                for offset in range(len(MASTER_KEY)):
                    key = np.roll(MASTER_KEY, -offset)
                    dec2 = vigenere_decrypt(dec, key)
                    text = indices_to_text(dec2)
                    score = word_score(text)
                    if score > 220:
                        results.append((score, f"Affine a={a} b={b} → Vig offset={offset}", text[:80]))
    
    # 6. Vigenere then Affine
    for offset in range(len(MASTER_KEY)):
        key = np.roll(MASTER_KEY, -offset)
        dec = vigenere_decrypt(pg_idx, key)
        for a in [7, 11, 13]:
            for b in range(29):
                dec2 = affine_decrypt(dec, a, b)
                if dec2 is not None:
                    text = indices_to_text(dec2)
                    score = word_score(text)
                    if score > 220:
                        results.append((score, f"Vig offset={offset} → Affine a={a} b={b}", text[:80]))
    
    results.sort(reverse=True, key=lambda x: x[0])
    return pg_num, results[:10]

def main():
    print("="*70)
    print("COMPREHENSIVE BRUTE FORCE - ALL COMBINATIONS")
    print("="*70)
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print(f"\nTesting {len(unsolved)} unsolved pages with all cipher combinations...")
    print("This may take a few minutes...\n")
    
    page_data_list = [(pg, pages[pg]) for pg in unsolved]
    
    all_results = {}
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = {executor.submit(test_all_combinations, pd): pd[0] for pd in page_data_list}
        
        for future in as_completed(futures):
            pg_num, results = future.result()
            all_results[pg_num] = results
            print(f"Page {pg_num} completed - {len(results)} high-scoring results")
    
    print("\n" + "="*70)
    print("TOP RESULTS FOR EACH PAGE")
    print("="*70)
    
    for pg_num in unsolved:
        if pg_num in all_results and all_results[pg_num]:
            print(f"\n--- PAGE {pg_num} ---")
            for score, method, text in all_results[pg_num][:5]:
                print(f"  Score: {score} | {method}")
                print(f"    {text}")
    
    print("\n" + "="*70)
    print("OVERALL BEST RESULTS (TOP 20)")
    print("="*70)
    
    all_combined = []
    for pg_num, results in all_results.items():
        for score, method, text in results:
            all_combined.append((score, pg_num, method, text))
    
    all_combined.sort(reverse=True, key=lambda x: x[0])
    
    for score, pg_num, method, text in all_combined[:20]:
        print(f"\nPage {pg_num} | Score: {score}")
        print(f"  Method: {method}")
        print(f"  Text: {text}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
NUMBERS AS DIRECTION - Final Analysis
======================================

"Its words are the map, their meaning is the road, and their NUMBERS are the direction"

The NUMBERS = Gematria values. Direction = how to read/traverse.

Hypothesis: Use each rune's Gematria value to determine the NEXT position to read.
"""

import re
from pathlib import Path
import numpy as np
from itertools import permutations

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def word_score(text):
    score = 0
    words = {
        'THE': 9, 'AND': 9, 'THAT': 12, 'HAVE': 12, 'FOR': 9, 'NOT': 9, 'WITH': 12, 'THIS': 12,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

def load_pages():
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

def gematria_walk(page_runes, start=0):
    """Walk through runes using Gematria values as step size"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    
    result = []
    visited = set()
    pos = start
    
    while len(result) < n:
        if pos not in visited:
            result.append(idx[pos])
            visited.add(pos)
        # Next position = current position + Gematria value of current rune
        step = GEMATRIA[idx[pos]]
        pos = (pos + step) % n
        
        # Prevent infinite loops
        if len(result) < n and pos in visited:
            # Find next unvisited
            for i in range(n):
                if i not in visited:
                    pos = i
                    break
    
    return np.array(result)

def gematria_backward_walk(page_runes, start=-1):
    """Walk backward using Gematria values"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    
    result = []
    visited = set()
    pos = start % n
    
    while len(result) < n:
        if pos not in visited:
            result.append(idx[pos])
            visited.add(pos)
        step = GEMATRIA[idx[pos]]
        pos = (pos - step) % n  # Subtract instead of add
        
        if len(result) < n and pos in visited:
            for i in range(n):
                if i not in visited:
                    pos = i
                    break
    
    return np.array(result)

def gematria_index_sort(page_runes):
    """Sort runes by their position's Gematria value"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    
    # Each position has a Gematria "weight" = sum of Gematria values up to that position
    weights = []
    running_sum = 0
    for i, rune_idx in enumerate(idx):
        running_sum = (running_sum + GEMATRIA[rune_idx]) % n
        weights.append((i, running_sum))
    
    # Sort by weight
    sorted_positions = sorted(weights, key=lambda x: x[1])
    result = idx[[p[0] for p in sorted_positions]]
    
    return result

def prime_step_walk(page_runes):
    """Walk using prime numbers as steps"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    result = []
    visited = set()
    pos = 0
    prime_idx = 0
    
    while len(result) < n:
        if pos not in visited:
            result.append(idx[pos])
            visited.add(pos)
        pos = (pos + primes[prime_idx % len(primes)]) % n
        prime_idx += 1
        
        if len(result) < n and pos in visited:
            for i in range(n):
                if i not in visited:
                    pos = i
                    break
    
    return np.array(result)

def main():
    pages = load_pages()
    
    print("="*70)
    print("NUMBERS AS DIRECTION - GEMATRIA TRAVERSAL")
    print("="*70)
    
    best_results = []
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
            
        pg_runes = pages[pg_num]
        n = len(runes_to_indices(pg_runes))
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        
        # Method 1: Gematria forward walk from position 0
        walked = gematria_walk(pg_runes, 0)
        decrypted = (walked - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Gematria walk(0)", text[:60]))
        
        # Try different starting positions
        for start in [0, 1, 10, n//2, n-1]:
            walked = gematria_walk(pg_runes, start)
            decrypted = (walked - key_ext) % 29
            text = indices_to_text(decrypted)
            score = word_score(text)
            if score >= 130:
                best_results.append((score, pg_num, f"Gematria walk({start})", text[:60]))
        
        # Method 2: Backward walk
        walked = gematria_backward_walk(pg_runes)
        decrypted = (walked - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Gematria backward", text[:60]))
        
        # Method 3: Index sort
        sorted_idx = gematria_index_sort(pg_runes)
        decrypted = (sorted_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Gematria index sort", text[:60]))
        
        # Method 4: Prime step walk
        walked = prime_step_walk(pg_runes)
        decrypted = (walked - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Prime step walk", text[:60]))
        
        # Method 5: Use Gematria value mod 29 as new rune index (Gematria shift)
        pg_idx = runes_to_indices(pg_runes)
        gem_values = np.array([GEMATRIA[i] for i in pg_idx])
        shifted = (pg_idx + gem_values) % 29
        decrypted = (shifted - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Gematria shift +", text[:60]))
        
        shifted = (pg_idx - gem_values) % 29
        decrypted = (shifted - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Gematria shift -", text[:60]))
    
    # Test with NO master key (maybe pages decrypt differently)
    print("\n" + "="*70)
    print("TESTING WITHOUT MASTER KEY")
    print("="*70)
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
            
        pg_runes = pages[pg_num]
        pg_idx = runes_to_indices(pg_runes)
        n = len(pg_idx)
        
        # Just Gematria walk, no key
        walked = gematria_walk(pg_runes, 0)
        text = indices_to_text(walked)
        score = word_score(text)
        if score >= 80:
            print(f"Page {pg_num} Gematria walk (no key): {score}")
            print(f"  {text[:70]}")
        
        # Sorted by Gematria value
        sorted_order = np.argsort([GEMATRIA[i] for i in pg_idx])
        sorted_idx = pg_idx[sorted_order]
        text = indices_to_text(sorted_idx)
        score = word_score(text)
        if score >= 80:
            print(f"Page {pg_num} sorted by Gematria (no key): {score}")
            print(f"  {text[:70]}")
    
    # Summary
    print("\n" + "="*70)
    print("BEST RESULTS SUMMARY")
    print("="*70)
    
    best_results.sort(reverse=True)
    for score, pg, method, text in best_results[:20]:
        print(f"Score {score}: Page {pg} - {method}")
        print(f"  {text}")
    
    # Try one more thing: Use the MASTER KEY as step values
    print("\n" + "="*70)
    print("MASTER KEY AS STEP PATTERN")
    print("="*70)
    
    for pg_num in [30, 31, 46, 47]:
        if pg_num not in pages:
            continue
            
        pg_runes = pages[pg_num]
        pg_idx = runes_to_indices(pg_runes)
        n = len(pg_idx)
        
        result = []
        visited = set()
        pos = 0
        key_idx = 0
        
        while len(result) < n:
            if pos not in visited:
                result.append(pg_idx[pos])
                visited.add(pos)
            # Step by master key value
            step = MASTER_KEY[key_idx % 95]
            pos = (pos + step + 1) % n  # +1 to ensure progress
            key_idx += 1
            
            if len(result) < n and pos in visited:
                for i in range(n):
                    if i not in visited:
                        pos = i
                        break
        
        result = np.array(result)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (result - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} master key steps: {score}")
        print(f"  {text[:70]}")

if __name__ == "__main__":
    main()

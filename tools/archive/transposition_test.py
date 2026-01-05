#!/usr/bin/env python3
"""
TRANSPOSITION CIPHER TESTING
=============================

The XOR results contain recognizable words but in wrong order.
Maybe there's a transposition cipher applied after substitution.
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
    words = {'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
             'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
             'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO',
             'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
             'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM',
             'FROM', 'ARE', 'BUT', 'ONE', 'ALL', 'OUT', 'THEIR', 'THEY'}
    for word in words:
        count = text.count(word)
        score += count * len(word) * 3
    return score

def columnar_transpose_decrypt(text_indices, cols):
    """Decrypt columnar transposition cipher with 'cols' columns"""
    n = len(text_indices)
    rows = (n + cols - 1) // cols
    
    # Create matrix and read column by column
    result = np.zeros(n, dtype=np.int32)
    idx = 0
    
    # Fill by columns
    grid = np.zeros((rows, cols), dtype=np.int32)
    for col in range(cols):
        col_len = rows if col < n % cols or n % cols == 0 else rows - 1
        for row in range(col_len):
            if idx < n:
                grid[row, col] = text_indices[idx]
                idx += 1
    
    # Read by rows
    result_idx = 0
    for row in range(rows):
        for col in range(cols):
            if row < rows and (col < n % cols or n % cols == 0 or row < rows - 1):
                if result_idx < n:
                    result[result_idx] = grid[row, col]
                    result_idx += 1
    
    return result[:result_idx]

def rail_fence_decrypt(text_indices, rails):
    """Decrypt rail fence cipher"""
    n = len(text_indices)
    result = np.zeros(n, dtype=np.int32)
    
    # Calculate the zigzag pattern
    cycle = 2 * rails - 2
    if cycle == 0:
        return text_indices
    
    # Determine lengths of each rail
    rail_lens = []
    for r in range(rails):
        if r == 0 or r == rails - 1:
            rail_lens.append((n + cycle - 1 - r) // cycle + ((n + cycle - 1 - cycle + r) // cycle if r == 0 else 0))
        else:
            rail_lens.append(sum(1 for i in range(n) if i % cycle == r or (cycle - i % cycle) % cycle == r))
    
    # Simpler approach: simulate
    fence = [[] for _ in range(rails)]
    direction = 1
    row = 0
    
    for i in range(n):
        fence[row].append(None)
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction
    
    # Fill the fence with the cipher text
    idx = 0
    for r in range(rails):
        for j in range(len(fence[r])):
            if idx < n:
                fence[r][j] = text_indices[idx]
                idx += 1
    
    # Read off
    result = []
    direction = 1
    row = 0
    col_indices = [0] * rails
    
    for i in range(n):
        if col_indices[row] < len(fence[row]):
            result.append(fence[row][col_indices[row]])
            col_indices[row] += 1
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction
    
    return np.array(result, dtype=np.int32)

def reverse_every_n(indices, n):
    """Reverse every n characters"""
    result = indices.copy()
    for i in range(0, len(result), n):
        result[i:i+n] = result[i:i+n][::-1]
    return result

def main():
    print("="*70)
    print("TRANSPOSITION CIPHER TESTING")
    print("="*70)
    
    pages = load_all_pages()
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    # Get Page 47 XOR result (our best result)
    p47 = runes_to_indices(pages[47])
    n = len(p47)
    key = np.tile(np.roll(MASTER_KEY, -45), (n // len(MASTER_KEY) + 1))[:n]
    xored = (p47 ^ key) % 29
    
    print("\n" + "="*70)
    print("BASE: PAGE 47 XOR OFFSET 45")
    print("="*70)
    text = indices_to_text(xored)
    print(f"Score: {word_score(text)}")
    print(f"Text: {text[:100]}")
    
    # Test columnar transposition
    print("\n" + "="*70)
    print("TEST 1: COLUMNAR TRANSPOSITION (2-20 columns)")
    print("="*70)
    
    best_col = (0, 0, "")
    for cols in range(2, 21):
        transposed = columnar_transpose_decrypt(xored, cols)
        text = indices_to_text(transposed)
        score = word_score(text)
        if score > best_col[1]:
            best_col = (cols, score, text[:100])
        if score > 200:
            print(f"Cols={cols:2d} | Score: {score}")
            print(f"  {text[:80]}")
    
    print(f"\nBest: cols={best_col[0]}, score={best_col[1]}")
    print(f"  {best_col[2][:80]}")
    
    # Test rail fence
    print("\n" + "="*70)
    print("TEST 2: RAIL FENCE (2-10 rails)")
    print("="*70)
    
    best_rail = (0, 0, "")
    for rails in range(2, 11):
        decrypted = rail_fence_decrypt(xored, rails)
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score > best_rail[1]:
            best_rail = (rails, score, text[:100])
        if score > 200:
            print(f"Rails={rails:2d} | Score: {score}")
            print(f"  {text[:80]}")
    
    print(f"\nBest: rails={best_rail[0]}, score={best_rail[1]}")
    print(f"  {best_rail[2][:80]}")
    
    # Test reverse every N
    print("\n" + "="*70)
    print("TEST 3: REVERSE EVERY N CHARACTERS")
    print("="*70)
    
    best_rev = (0, 0, "")
    for n in range(2, 50):
        reversed_idx = reverse_every_n(xored, n)
        text = indices_to_text(reversed_idx)
        score = word_score(text)
        if score > best_rev[1]:
            best_rev = (n, score, text[:100])
        if score > 200:
            print(f"Reverse every {n:2d} | Score: {score}")
            print(f"  {text[:80]}")
    
    print(f"\nBest: n={best_rev[0]}, score={best_rev[1]}")
    print(f"  {best_rev[2][:80]}")
    
    # Test complete reversal
    print("\n" + "="*70)
    print("TEST 4: COMPLETE REVERSAL")
    print("="*70)
    
    reversed_complete = xored[::-1]
    text = indices_to_text(reversed_complete)
    score = word_score(text)
    print(f"Score: {score}")
    print(f"Text: {text[:100]}")
    
    # Test interleaving (read every 2nd, then every other 2nd)
    print("\n" + "="*70)
    print("TEST 5: DE-INTERLEAVE")
    print("="*70)
    
    for step in range(2, 10):
        result = np.zeros_like(xored)
        pos = 0
        for start in range(step):
            for i in range(start, len(xored), step):
                if pos < len(result):
                    result[pos] = xored[i]
                    pos += 1
        
        text = indices_to_text(result)
        score = word_score(text)
        if score > 150:
            print(f"De-interleave step={step} | Score: {score}")
            print(f"  {text[:80]}")
    
    # Try all these on the raw page WITHOUT XOR first
    print("\n" + "="*70)
    print("TEST 6: TRANSPOSE FIRST, THEN XOR")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        for cols in range(2, 15):
            transposed = columnar_transpose_decrypt(pg_idx, cols)
            
            for offset in [0, 45]:
                key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
                xored = (transposed ^ key) % 29
                text = indices_to_text(xored)
                score = word_score(text)
                
                if score > 200:
                    print(f"Page {pg_num} | Transpose cols={cols:2d} → XOR offset={offset:2d} | Score: {score}")
                    print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

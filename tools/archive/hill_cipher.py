#!/usr/bin/env python3
"""
HILL CIPHER AND MATRIX-BASED ATTACK
====================================

Try Hill cipher (matrix multiplication mod 29) which is known in cryptographic
literature. Also try other algebraic approaches.
"""

import re
import numpy as np
from pathlib import Path
from itertools import product, permutations
from math import gcd

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
             'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM'}
    for word in words:
        count = text.count(word)
        score += count * len(word) * 3
    return score

def mod_inverse(a, m):
    """Find modular multiplicative inverse of a mod m"""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(indices, a, b):
    """Affine cipher: D(x) = a^-1 * (x - b) mod 29"""
    a_inv = mod_inverse(a, 29)
    if a_inv is None:
        return None
    return np.array([(a_inv * (x - b)) % 29 for x in indices], dtype=np.int32)

def hill_2x2_decrypt(indices, matrix):
    """Hill cipher with 2x2 matrix"""
    # Check if matrix is invertible mod 29
    det = (matrix[0,0] * matrix[1,1] - matrix[0,1] * matrix[1,0]) % 29
    det_inv = mod_inverse(det, 29)
    if det_inv is None:
        return None
    
    # Calculate inverse matrix
    inv_matrix = np.array([
        [matrix[1,1], -matrix[0,1]],
        [-matrix[1,0], matrix[0,0]]
    ], dtype=np.int64)
    inv_matrix = (det_inv * inv_matrix) % 29
    
    # Pad if necessary
    if len(indices) % 2 != 0:
        indices = np.append(indices, 0)
    
    result = []
    for i in range(0, len(indices), 2):
        pair = np.array([indices[i], indices[i+1]], dtype=np.int64)
        decrypted = inv_matrix @ pair
        result.extend(decrypted % 29)
    
    return np.array(result, dtype=np.int32)

def main():
    print("="*70)
    print("HILL CIPHER AND AFFINE CIPHER ATTACK")
    print("="*70)
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Affine cipher test
    print("\n" + "="*70)
    print("AFFINE CIPHER: D(x) = a^-1 * (x - b) mod 29")
    print("="*70)
    
    # Valid 'a' values (coprime with 29)
    valid_a = [a for a in range(1, 29) if gcd(a, 29) == 1]
    print(f"Valid 'a' values: {valid_a}")
    
    affine_results = []
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        for a in valid_a:
            for b in range(29):
                dec = affine_decrypt(pg_idx, a, b)
                if dec is None:
                    continue
                text = indices_to_text(dec)
                score = word_score(text)
                if score > 100:
                    affine_results.append((pg_num, a, b, score, text[:60]))
    
    affine_results.sort(key=lambda x: -x[3])
    
    print(f"\nTop Affine cipher results:")
    for pg, a, b, score, text in affine_results[:20]:
        print(f"  Page {pg} | a={a:2d} b={b:2d} | score={score:3d} | {text}")
    
    # Hill cipher 2x2 test
    print("\n" + "="*70)
    print("HILL CIPHER (2x2 MATRIX)")
    print("="*70)
    
    # Generate all invertible 2x2 matrices mod 29 (too many - sample instead)
    # Actually let's try some common matrices and patterns
    
    test_matrices = []
    
    # Identity and simple variations
    for k in range(1, 29):
        if gcd(k, 29) == 1:
            test_matrices.append(np.array([[k, 0], [0, k]], dtype=np.int64))  # Scaling
    
    # Simple matrices
    for a in range(1, 10):
        for b in range(0, 10):
            for c in range(0, 10):
                for d in range(1, 10):
                    det = (a * d - b * c) % 29
                    if gcd(det, 29) == 1:
                        test_matrices.append(np.array([[a, b], [c, d]], dtype=np.int64))
    
    print(f"Testing {len(test_matrices)} 2x2 matrices...")
    
    hill_results = []
    
    for pg_num in unsolved[:5]:  # Test first 5 pages
        pg_idx = runes_to_indices(pages[pg_num])
        
        for matrix in test_matrices[:500]:  # Limit
            dec = hill_2x2_decrypt(pg_idx, matrix)
            if dec is None:
                continue
            text = indices_to_text(dec)
            score = word_score(text)
            if score > 80:
                mat_str = f"[[{matrix[0,0]},{matrix[0,1]}],[{matrix[1,0]},{matrix[1,1]}]]"
                hill_results.append((pg_num, mat_str, score, text[:60]))
    
    hill_results.sort(key=lambda x: -x[2])
    
    print(f"\nTop Hill cipher results:")
    for pg, mat, score, text in hill_results[:20]:
        print(f"  Page {pg} | {mat} | score={score:3d} | {text}")
    
    # Try "untwisting" - perhaps there's a permutation
    print("\n" + "="*70)
    print("SIMPLE TRANSPOSITION ANALYSIS")
    print("="*70)
    
    for pg_num in unsolved[:3]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Try reading in different column orders for various widths
        for width in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]:
            # Read column by column
            height = (n + width - 1) // width
            grid = np.zeros((height, width), dtype=np.int32)
            
            idx = 0
            for c in range(width):
                for r in range(height):
                    if idx < n:
                        grid[r, c] = pg_idx[idx]
                        idx += 1
            
            # Read row by row
            transposed = grid.flatten()[:n]
            text = indices_to_text(transposed)
            score = word_score(text)
            
            if score > 50:
                print(f"Page {pg_num} | width={width:2d} (col→row) | score={score} | {text[:50]}")
            
            # Also try reverse
            idx = 0
            for r in range(height):
                for c in range(width):
                    if idx < n:
                        grid[r, c] = pg_idx[idx]
                        idx += 1
            
            transposed = []
            for c in range(width):
                for r in range(height):
                    if r * width + c < n:
                        transposed.append(grid[r, c])
            transposed = np.array(transposed, dtype=np.int32)
            text = indices_to_text(transposed)
            score = word_score(text)
            
            if score > 50:
                print(f"Page {pg_num} | width={width:2d} (row→col) | score={score} | {text[:50]}")

if __name__ == "__main__":
    main()

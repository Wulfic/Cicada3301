#!/usr/bin/env python3
"""
VISUAL DESIGN ANALYSIS
======================

Cicada emphasized: "their NUMBERS are the direction"

Key design elements to analyze:
1. Magic Square pages (10-13) with values 10, 12, 14, etc.
2. Page 27 = 234 runes = 9 × 26 = 13 × 18 (perfect grid!)
3. The orientation of pages (some rotated, some mirror)
4. Gematria values determining READING ORDER

Let's use numbers as the DIRECTION for reading!
"""

import numpy as np
import re
from pathlib import Path

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

def indices_to_gematria(indices):
    return np.array([GEMATRIA[i] for i in indices], dtype=np.int32)

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
        'BEING': 15, 'SOUL': 12, 'MIND': 12, 'KNOW': 12, 'ONE': 9, 'ALL': 9, 'WAY': 9,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

def gematria_sorted_read(page_runes):
    """Read runes sorted by their Gematria values"""
    idx = runes_to_indices(page_runes)
    gem = indices_to_gematria(idx)
    
    # Sort indices by Gematria value
    sorted_order = np.argsort(gem)  # ascending
    sorted_idx = idx[sorted_order]
    
    return sorted_idx, indices_to_text(sorted_idx)

def gematria_position_read(page_runes):
    """Use Gematria value of position n to determine next read position"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    gem = indices_to_gematria(idx)
    
    result = []
    visited = set()
    pos = 0  # Start at position 0
    
    while len(result) < n and pos not in visited:
        visited.add(pos)
        result.append(idx[pos])
        # Next position is determined by Gematria value at current position
        pos = gem[pos] % n
    
    # Fill remaining with unvisited
    for i in range(n):
        if i not in visited:
            result.append(idx[i])
    
    return np.array(result), indices_to_text(result[:n])

def spiral_read(page_runes, cols):
    """Read in spiral pattern"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    rows = (n + cols - 1) // cols
    
    # Pad to fill grid
    padded = np.zeros(rows * cols, dtype=np.int32)
    padded[:n] = idx
    grid = padded.reshape(rows, cols)
    
    result = []
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    
    while top <= bottom and left <= right:
        # Top row
        for c in range(left, right + 1):
            result.append(grid[top, c])
        top += 1
        
        # Right column  
        for r in range(top, bottom + 1):
            result.append(grid[r, right])
        right -= 1
        
        # Bottom row
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(grid[bottom, c])
            bottom -= 1
        
        # Left column
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(grid[r, left])
            left += 1
    
    return np.array(result[:n]), indices_to_text(result[:n])

def boustrophedon_read(page_runes, cols):
    """Read alternating left-right, right-left (snake pattern)"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    rows = (n + cols - 1) // cols
    
    padded = np.zeros(rows * cols, dtype=np.int32)
    padded[:n] = idx
    grid = padded.reshape(rows, cols)
    
    result = []
    for r in range(rows):
        if r % 2 == 0:
            # Left to right
            result.extend(grid[r, :])
        else:
            # Right to left
            result.extend(grid[r, ::-1])
    
    return np.array(result[:n]), indices_to_text(result[:n])

def diagonal_read(page_runes, cols):
    """Read diagonally"""
    idx = runes_to_indices(page_runes)
    n = len(idx)
    rows = (n + cols - 1) // cols
    
    padded = np.zeros(rows * cols, dtype=np.int32)
    padded[:n] = idx
    grid = padded.reshape(rows, cols)
    
    result = []
    # Top-left to bottom-right diagonals
    for d in range(rows + cols - 1):
        r_start = max(0, d - cols + 1)
        c_start = max(0, cols - 1 - d)
        r, c = r_start, c_start
        while r < rows and c < cols:
            result.append(grid[r, c])
            r += 1
            c += 1
    
    return np.array(result[:n]), indices_to_text(result[:n])

def main():
    pages = load_all_pages()
    
    print("="*70)
    print("VISUAL DESIGN ANALYSIS: NUMBERS AS DIRECTION")
    print("="*70)
    
    # Focus on pages with nice grid dimensions
    print("\n" + "="*70)
    print("GRID DIMENSIONS ANALYSIS")
    print("="*70)
    
    for pg_num in [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]:
        n = len(pages[pg_num])
        factors = []
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                factors.append((i, n // i))
        print(f"Page {pg_num}: {n} runes -> factors: {factors}")
    
    # Test different reading patterns
    print("\n" + "="*70)
    print("READING PATTERN TESTS")
    print("="*70)
    
    best_results = []
    
    for pg_num in [27, 30, 31]:
        print(f"\n--- Page {pg_num} ---")
        pg_runes = pages[pg_num]
        n = len(pg_runes)
        
        # Gematria sorted reading
        sorted_idx, sorted_text = gematria_sorted_read(pg_runes)
        # Apply master key
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (sorted_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"  Gematria sorted + key: {score} | {text[:60]}")
        best_results.append((score, pg_num, "Gematria sorted + key"))
        
        # Gematria position reading
        pos_idx, pos_text = gematria_position_read(pg_runes)
        decrypted = (pos_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"  Gematria position + key: {score} | {text[:60]}")
        best_results.append((score, pg_num, "Gematria position + key"))
        
        # Test grid patterns with different dimensions
        for cols in [9, 13, 18, 26]:
            if n >= cols:
                # Spiral
                spiral_idx, _ = spiral_read(pg_runes, cols)
                if len(spiral_idx) == n:
                    decrypted = (spiral_idx - key_ext) % 29
                    text = indices_to_text(decrypted)
                    score = word_score(text)
                    if score > 100:
                        print(f"  Spiral cols={cols} + key: {score} | {text[:60]}")
                        best_results.append((score, pg_num, f"Spiral cols={cols}"))
                
                # Boustrophedon (snake)
                snake_idx, _ = boustrophedon_read(pg_runes, cols)
                if len(snake_idx) == n:
                    decrypted = (snake_idx - key_ext) % 29
                    text = indices_to_text(decrypted)
                    score = word_score(text)
                    if score > 100:
                        print(f"  Snake cols={cols} + key: {score} | {text[:60]}")
                        best_results.append((score, pg_num, f"Snake cols={cols}"))
                
                # Diagonal
                diag_idx, _ = diagonal_read(pg_runes, cols)
                if len(diag_idx) == n:
                    decrypted = (diag_idx - key_ext) % 29
                    text = indices_to_text(decrypted)
                    score = word_score(text)
                    if score > 100:
                        print(f"  Diagonal cols={cols} + key: {score} | {text[:60]}")
                        best_results.append((score, pg_num, f"Diagonal cols={cols}"))
    
    # Use MAGIC SQUARE numbers (10, 12, 14)
    print("\n" + "="*70)
    print("MAGIC SQUARE NUMBERS AS PARAMETERS")
    print("="*70)
    
    magic_numbers = [10, 12, 14]
    
    for pg_num in [27, 28, 29, 30, 31]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        
        # Use magic numbers as column widths
        for cols in magic_numbers:
            spiral_idx, _ = spiral_read(pages[pg_num], cols)
            decrypted = (spiral_idx - key_ext) % 29
            text = indices_to_text(decrypted)
            score = word_score(text)
            if score >= 100:
                print(f"Page {pg_num} spiral cols={cols}: {score}")
                print(f"  {text[:70]}")
        
        # Use magic numbers as skip distance
        for skip in magic_numbers:
            # Read every 'skip' rune
            reordered = pg_idx[::skip]
            if len(reordered) > 50:
                key_ext2 = key_ext[:len(reordered)]
                decrypted = (reordered - key_ext2) % 29
                text = indices_to_text(decrypted)
                score = word_score(text)
                if score >= 30:
                    print(f"Page {pg_num} skip={skip}: {score}")
    
    # Test reverse reading
    print("\n" + "="*70)
    print("REVERSE READING (mirror pages)")
    print("="*70)
    
    for pg_num in [27, 28, 29, 30, 31]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Reverse the entire page
        reversed_idx = pg_idx[::-1]
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (reversed_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score >= 100:
            print(f"Page {pg_num} reversed + key: {score}")
            print(f"  {text[:70]}")
    
    # Summary
    print("\n" + "="*70)
    print("BEST RESULTS SUMMARY")
    print("="*70)
    
    best_results.sort(reverse=True)
    for score, pg, method in best_results[:10]:
        print(f"  Score {score}: Page {pg} - {method}")

if __name__ == "__main__":
    main()

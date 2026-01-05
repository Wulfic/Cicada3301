#!/usr/bin/env python3
"""
FOCUSED BREAKTHROUGH ATTEMPT
=============================

Best results so far:
- Page 31 Gematria index sort: 174
- Page 30 Gematria index sort: 168  
- Page 46 Gematria shift -: 159
- Page 46 Gematria walk (no key): 150

Let's focus on these and try more variations.
"""

import re
from pathlib import Path
import numpy as np

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
        'THERE': 15, 'THEIR': 15, 'THEY': 12, 'THEM': 12, 'THEN': 12, 'THESE': 15,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
        'SELF': 12, 'SOUL': 12, 'MIND': 12, 'KNOW': 12, 'KNOWLEDGE': 27, 'BEING': 15,
        'YOU': 9, 'YOUR': 12, 'YOURSELF': 24, 'ONE': 9, 'ALL': 9, 'WAY': 9,
        'ING': 6, 'TION': 9, 'FROM': 12, 'WHICH': 15, 'WOULD': 15, 'WHEN': 12, 'WHAT': 12,
        'WERE': 12, 'MUST': 12, 'WILL': 12, 'BECOME': 18, 'UNDERSTAND': 30,
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
    idx = runes_to_indices(page_runes)
    n = len(idx)
    
    result = []
    visited = set()
    pos = start
    
    while len(result) < n:
        if pos not in visited:
            result.append(idx[pos])
            visited.add(pos)
        step = GEMATRIA[idx[pos]]
        pos = (pos + step) % n
        
        if len(result) < n and pos in visited:
            for i in range(n):
                if i not in visited:
                    pos = i
                    break
    
    return np.array(result)

def main():
    pages = load_pages()
    
    print("="*70)
    print("FOCUSED ANALYSIS ON BEST METHODS")
    print("="*70)
    
    best_results = []
    
    # Focus on pages with highest scores
    focus_pages = [30, 31, 46, 47, 52]
    
    for pg_num in focus_pages:
        if pg_num not in pages:
            continue
            
        pg_runes = pages[pg_num]
        pg_idx = runes_to_indices(pg_runes)
        n = len(pg_idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        
        print(f"\n{'='*70}")
        print(f"PAGE {pg_num} DEEP ANALYSIS")
        print(f"{'='*70}")
        
        # 1. Gematria index sort (best so far)
        weights = []
        running_sum = 0
        for i, rune_idx in enumerate(pg_idx):
            running_sum = (running_sum + GEMATRIA[rune_idx]) % n
            weights.append((i, running_sum))
        
        sorted_positions = sorted(weights, key=lambda x: x[1])
        sorted_idx = pg_idx[[p[0] for p in sorted_positions]]
        
        decrypted = (sorted_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Gematria index sort + key: {score}")
        print(f"  {text[:80]}")
        best_results.append((score, pg_num, "Gematria index sort", text))
        
        # Without key
        text_nokey = indices_to_text(sorted_idx)
        score_nokey = word_score(text_nokey)
        print(f"Gematria index sort (no key): {score_nokey}")
        print(f"  {text_nokey[:80]}")
        
        # 2. Gematria shift
        gem_values = np.array([GEMATRIA[i] for i in pg_idx])
        shifted = (pg_idx - gem_values) % 29
        decrypted = (shifted - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Gematria shift - + key: {score}")
        print(f"  {text[:80]}")
        best_results.append((score, pg_num, "Gematria shift -", text))
        
        # 3. Gematria walk from different starts
        best_walk = (0, 0, "")
        for start in range(min(50, n)):
            walked = gematria_walk(pg_runes, start)
            text_nokey = indices_to_text(walked)
            score_nokey = word_score(text_nokey)
            if score_nokey > best_walk[0]:
                best_walk = (score_nokey, start, text_nokey)
        
        print(f"Best Gematria walk start={best_walk[1]} (no key): {best_walk[0]}")
        print(f"  {best_walk[2][:80]}")
        
        # Apply key to best walk
        walked = gematria_walk(pg_runes, best_walk[1])
        decrypted = (walked - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Best Gematria walk start={best_walk[1]} + key: {score}")
        print(f"  {text[:80]}")
        
        # 4. Combine: Gematria walk + Gematria shift
        walked = gematria_walk(pg_runes, 0)
        gem_values = np.array([GEMATRIA[i] for i in walked])
        shifted = (walked - gem_values) % 29
        text = indices_to_text(shifted)
        score = word_score(text)
        print(f"Gematria walk + shift: {score}")
        print(f"  {text[:80]}")
        
        # 5. Sort runes by Gematria value directly (not cumulative)
        sorted_order = np.argsort([GEMATRIA[i] for i in pg_idx])
        sorted_idx = pg_idx[sorted_order]
        
        text_nokey = indices_to_text(sorted_idx)
        score_nokey = word_score(text_nokey)
        print(f"Direct Gematria sort (no key): {score_nokey}")
        print(f"  {text_nokey[:80]}")
        
        decrypted = (sorted_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Direct Gematria sort + key: {score}")
        print(f"  {text[:80]}")
        
        # 6. Reverse sort
        sorted_order = np.argsort([-GEMATRIA[i] for i in pg_idx])
        sorted_idx = pg_idx[sorted_order]
        
        decrypted = (sorted_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Reverse Gematria sort + key: {score}")
        print(f"  {text[:80]}")
    
    # Test the SOLVED pages with Gematria walk to validate
    print("\n" + "="*70)
    print("VALIDATION: Testing Gematria methods on SOLVED pages")
    print("="*70)
    
    # Page 0 (solved - Parable)
    if 0 in pages:
        pg_runes = pages[0]
        pg_idx = runes_to_indices(pg_runes)
        n = len(pg_idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        
        # Standard decryption
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"\nPage 0 (Parable) - Standard + key: {score}")
        print(f"  {text[:80]}")
        
        # Gematria walk
        walked = gematria_walk(pg_runes, 0)
        text_nokey = indices_to_text(walked)
        score_nokey = word_score(text_nokey)
        print(f"Page 0 - Gematria walk (no key): {score_nokey}")
        print(f"  {text_nokey[:80]}")
    
    # Summary
    print("\n" + "="*70)
    print("TOP RESULTS SUMMARY")
    print("="*70)
    
    best_results.sort(reverse=True)
    for score, pg, method, text in best_results[:10]:
        print(f"\nScore {score}: Page {pg} - {method}")
        print(f"Full text: {text[:150]}...")
        
        # Try to identify word boundaries
        # Insert spaces where common words might be
        text_with_spaces = text
        for word in ['THE', 'AND', 'OF', 'IN', 'TO', 'IS', 'BE', 'THAT', 'FOR', 'IT']:
            text_with_spaces = text_with_spaces.replace(word, f' {word} ')
        print(f"With spaces: {text_with_spaces[:150]}...")

if __name__ == "__main__":
    main()

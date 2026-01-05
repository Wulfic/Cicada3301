#!/usr/bin/env python3
"""
DEEP ANALYSIS OF TOP AFFINE CIPHER RESULTS
==========================================

Page 30 with a=7, b=10 scored 255 - our highest score yet!
Let's analyze this thoroughly.
"""

import re
import numpy as np
from pathlib import Path
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

def segment_text(text):
    words = [
        'CONSCIOUSNESS', 'CIRCUMFERENCE', 'ENLIGHTENMENT', 'UNDERSTANDING',
        'DIVINITY', 'PARABLE', 'THROUGH', 'BETWEEN', 'BECAUSE', 'SHOULD', 
        'BEFORE', 'THERE', 'INSTAR', 'EMERGE', 'SURFACE', 'WISDOM', 'WITHIN',
        'TRUTH', 'WHERE', 'WHICH', 'THEIR', 'BEING', 'THESE', 'THOSE', 'ABOUT',
        'WORLD', 'WOULD', 'COULD', 'AFTER', 'FIRST', 'OTHER', 'THING',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
        'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'WHAT', 'THAT', 'WITH',
        'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'MUST', 'SHED', 'FIND',
        'LIKE', 'SELF', 'MIND', 'EACH', 'ONLY', 'JUST', 'WHEN', 'INTO', 'SUCH',
        'THAN', 'SOME', 'TIME', 'VERY', 'THEN', 'MADE', 'OVER', 'MANY', 'MOST',
        'KNOW', 'SEEN', 'SEEK', 'FEEL', 'DOES', 'DONE', 'GOOD', 'LOOK', 'TAKE',
        'GIVE', 'KEEP', 'EVEN', 'ALSO', 'COME', 'CAME', 'BACK', 'WORK', 'WELL',
        'WAY', 'DAY', 'MAY', 'SAY', 'SEE', 'NOW', 'NEW', 'OLD', 'MAN', 'MEN',
        'TWO', 'OWN', 'PUT', 'SET', 'LET', 'GET', 'SAW', 'GOT', 'TOO', 'USE',
        'WAR', 'END', 'USE', 'FAR', 'FEW', 'BIG', 'BAD', 'RUN', 'AWAY', 'BACK',
        'OPEN', 'ONCE', 'EVER', 'UPON', 'LONG', 'MUCH', 'NEXT', 'LAST', 'LEFT',
        'STILL', 'SMALL', 'GREAT', 'THREE', 'EVERY', 'NEVER', 'UNDER', 'MIGHT',
        'WHILE', 'PLACE', 'POINT', 'FOUND', 'THINK', 'RIGHT', 'AGAIN', 'ALONG',
        'BEING', 'LIGHT', 'NIGHT', 'WORDS', 'YEARS', 'TIMES', 'YOUNG', 'WATER',
        'BE', 'AT', 'OR', 'AS', 'IT', 'IF', 'WE', 'IN', 'IS', 'TO', 'OF', 'AN',
        'HE', 'SO', 'NO', 'BY', 'UP', 'ON', 'MY', 'DO', 'GO', 'ME', 'NG', 'TH',
        'EA', 'IA', 'AE', 'EO', 'OE', 'A', 'I'
    ]
    
    result = []
    i = 0
    while i < len(text):
        matched = False
        for word in words:
            if text[i:].startswith(word):
                result.append(word)
                i += len(word)
                matched = True
                break
        if not matched:
            result.append(f"[{text[i]}]")
            i += 1
    return ' '.join(result)

def main():
    print("="*70)
    print("DEEP ANALYSIS OF TOP AFFINE CIPHER RESULTS")
    print("="*70)
    
    pages = load_all_pages()
    
    # Top results to analyze
    top_results = [
        (30, 7, 10, 255),
        (46, 2, 25, 228),
        (29, 6, 27, 219),
        (30, 23, 14, 219),
        (48, 7, 7, 219),
    ]
    
    for pg_num, a, b, score in top_results:
        pg_idx = runes_to_indices(pages[pg_num])
        dec = affine_decrypt(pg_idx, a, b)
        text = indices_to_text(dec)
        
        print("\n" + "="*70)
        print(f"PAGE {pg_num} | a={a}, b={b} | Score: {score}")
        print("="*70)
        print(f"\nFull decrypted text ({len(text)} chars):")
        print(text)
        print(f"\nAttempted segmentation:")
        print(segment_text(text))
        
        # Verify score calculation
        print(f"\nWords found:")
        words_found = {}
        for word in ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
                     'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
                     'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO']:
            count = text.count(word)
            if count > 0:
                words_found[word] = count
        print(words_found)
    
    # Apply best parameters (a=7, b=10) to all unsolved pages
    print("\n" + "="*70)
    print("APPLYING a=7, b=10 TO ALL UNSOLVED PAGES")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        dec = affine_decrypt(pg_idx, 7, 10)
        text = indices_to_text(dec)
        score = word_score(text)
        
        print(f"\nPage {pg_num} | Score: {score}")
        print(f"  {text[:100]}")
    
    # What if each page uses different (a, b)?
    print("\n" + "="*70)
    print("BEST (a, b) FOR EACH UNSOLVED PAGE")
    print("="*70)
    
    valid_a = [a for a in range(1, 29) if gcd(a, 29) == 1]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        best = (0, 0, 0, "")
        
        for a in valid_a:
            for b in range(29):
                dec = affine_decrypt(pg_idx, a, b)
                if dec is None:
                    continue
                text = indices_to_text(dec)
                score = word_score(text)
                if score > best[2]:
                    best = (a, b, score, text[:80])
        
        a, b, score, text = best
        print(f"\nPage {pg_num}: Best a={a:2d}, b={b:2d} | Score: {score}")
        print(f"  {text}")
    
    # Affine + transposition combo
    print("\n" + "="*70)
    print("AFFINE + SIMPLE TRANSPOSITION COMBINATIONS")
    print("="*70)
    
    for pg_num in [30, 46]:  # Test on best pages
        pg_idx = runes_to_indices(pages[pg_num])
        
        for a in [7, 2]:
            for b in [10, 25]:
                dec = affine_decrypt(pg_idx, a, b)
                if dec is None:
                    continue
                
                for width in [2, 3, 4, 5, 6, 7, 8]:
                    n = len(dec)
                    height = (n + width - 1) // width
                    
                    # Try columnar transposition
                    grid = np.zeros((height, width), dtype=np.int32)
                    idx = 0
                    for r in range(height):
                        for c in range(width):
                            if idx < n:
                                grid[r, c] = dec[idx]
                                idx += 1
                    
                    transposed = []
                    for c in range(width):
                        for r in range(height):
                            transposed.append(grid[r, c])
                    transposed = np.array(transposed[:n], dtype=np.int32)
                    
                    text = indices_to_text(transposed)
                    score = word_score(text)
                    
                    if score > 200:
                        print(f"Page {pg_num} | a={a} b={b} | width={width} | Score: {score}")
                        print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

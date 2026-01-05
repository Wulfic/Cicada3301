#!/usr/bin/env python3
"""
ANALYZE TOP AUTOKEY RESULTS
============================

Page 31 with key (20, 15, 15) scored 249 - our best result!
Let's see if this produces readable English and explore similar keys.
"""

import re
import numpy as np
from pathlib import Path
from itertools import product

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

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

def score_text(text):
    """Score how English-like the text is"""
    score = 0
    
    common_words = {'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
                    'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
                    'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO'}
    cicada_words = {'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
                    'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM',
                    'SELF', 'MIND', 'CONSCIOUSNESS', 'ENLIGHTENMENT', 'PILGRIM'}
    
    for word in common_words:
        count = text.count(word)
        score += count * len(word) * 3
    for word in cicada_words:
        count = text.count(word)
        score += count * len(word) * 10
    
    return score

def autokey_decrypt(indices, init_key):
    """Autokey decryption with a given initial key"""
    result = np.zeros(len(indices), dtype=np.int32)
    init_len = len(init_key)
    
    for i in range(len(indices)):
        if i < init_len:
            k = init_key[i]
        else:
            k = result[i - init_len]
        result[i] = (indices[i] - k) % 29
    
    return result

def try_segment(text):
    """Try to segment text into words"""
    words = [
        'CONSCIOUSNESS', 'ENLIGHTENMENT', 'CIRCUMFERENCE',
        'UNDERSTANDING', 'INTELLIGENCE', 'DIVINITY', 'PARABLE',
        'THROUGH', 'BETWEEN', 'BECAUSE', 'SHOULD', 'BEFORE', 'THERE',
        'INSTAR', 'EMERGE', 'SURFACE', 'WISDOM', 'WITHIN', 'TRUTH',
        'WHERE', 'WHICH', 'THEIR', 'BEING', 'THESE', 'THOSE',
        'ABOUT', 'WORLD', 'WOULD', 'COULD', 'AFTER', 'FIRST',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'WHAT',
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY',
        'MUST', 'SHED', 'FIND', 'LIKE', 'SELF', 'MIND', 'EACH',
        'BE', 'AT', 'OR', 'AS', 'IT', 'IF', 'WE', 'IN', 'IS', 'TO', 'OF',
        'AN', 'HE', 'SO', 'NO', 'BY', 'UP', 'ON', 'MY', 'DO', 'GO', 'ME',
        'A', 'I'
    ]
    
    remaining = text
    result = []
    skipped = 0
    
    while remaining:
        matched = False
        for word in words:
            if remaining.startswith(word):
                if skipped > 0:
                    result.append(f"[{skipped}]")
                    skipped = 0
                result.append(word)
                remaining = remaining[len(word):]
                matched = True
                break
        if not matched:
            skipped += 1
            remaining = remaining[1:]
    
    if skipped > 0:
        result.append(f"[{skipped}]")
    
    return result

def main():
    print("="*70)
    print("ANALYZING TOP AUTOKEY RESULT: Page 31 with key (20, 15, 15)")
    print("="*70)
    
    pages = load_all_pages()
    
    # The top result
    p31 = runes_to_indices(pages[31])
    init_key = np.array([20, 15, 15], dtype=np.int32)  # M, S, S
    
    decrypted = autokey_decrypt(p31, init_key)
    text = indices_to_text(decrypted)
    
    print(f"\nFull decrypted text:")
    print(text)
    
    print(f"\nAttempted word segmentation:")
    segments = try_segment(text)
    print(' '.join(segments))
    
    # What does init_key (20, 15, 15) correspond to?
    print(f"\nInit key as letters: {LETTERS[20]}, {LETTERS[15]}, {LETTERS[15]} = L, S, S")
    
    # Try variations around this key
    print("\n" + "="*70)
    print("SEARCHING FOR BETTER KEYS NEAR (20, 15, 15)")
    print("="*70)
    
    best_results = []
    
    # Search in a neighborhood of the best key
    for k0 in range(18, 23):
        for k1 in range(13, 18):
            for k2 in range(13, 18):
                init_key = np.array([k0, k1, k2], dtype=np.int32)
                decrypted = autokey_decrypt(p31, init_key)
                text = indices_to_text(decrypted)
                score = score_text(text)
                best_results.append((tuple(init_key), score, text))
    
    best_results.sort(key=lambda x: -x[1])
    
    for key, score, text in best_results[:10]:
        print(f"\nKey {key} ({LETTERS[key[0]]}{LETTERS[key[1]]}{LETTERS[key[2]]}) score={score}:")
        print(f"  {text[:100]}...")
    
    # Try the best key on ALL pages
    print("\n" + "="*70)
    print("APPLYING BEST KEY (20, 15, 15) TO ALL UNSOLVED PAGES")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        init_key = np.array([20, 15, 15], dtype=np.int32)
        
        decrypted = autokey_decrypt(pg_idx, init_key)
        text = indices_to_text(decrypted)
        score = score_text(text)
        
        print(f"\nPage {pg_num} (score={score}):")
        print(f"  {text[:100]}...")
    
    # Exhaustive 3-length key search for Page 31
    print("\n" + "="*70)
    print("EXHAUSTIVE 3-LENGTH KEY SEARCH FOR PAGE 31")
    print("="*70)
    
    best_p31 = []
    for k0 in range(29):
        for k1 in range(29):
            for k2 in range(29):
                init_key = np.array([k0, k1, k2], dtype=np.int32)
                decrypted = autokey_decrypt(p31, init_key)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score > 180:
                    best_p31.append((k0, k1, k2, score, text[:80]))
    
    best_p31.sort(key=lambda x: -x[3])
    
    print(f"\nTop 20 3-length keys for Page 31 (score > 180):\n")
    for k0, k1, k2, score, text in best_p31[:20]:
        key_str = f"{LETTERS[k0]}{LETTERS[k1]}{LETTERS[k2]}"
        print(f"Key ({k0},{k1},{k2}) = {key_str:8s} | score={score}")
        print(f"  {text}")
    
    # Check if any of these look like words
    print("\n" + "="*70)
    print("CHECKING IF KEYS FORM WORDS")
    print("="*70)
    
    for k0, k1, k2, score, text in best_p31[:20]:
        key_str = f"{LETTERS[k0]}{LETTERS[k1]}{LETTERS[k2]}"
        print(f"  {key_str}")

if __name__ == "__main__":
    main()

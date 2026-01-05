#!/usr/bin/env python3
"""
FOCUS ON PAGE 28
================

Page 28 with partial master key (24 chars) gives score 234.
Let's analyze this more carefully.
"""

import re
import numpy as np
from pathlib import Path
from collections import Counter

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
    with open(data_file, 'r', encoding='utf-8')as f:
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

def vigenere_decrypt(indices, key):
    key_len = len(key)
    result = np.zeros(len(indices), dtype=np.int32)
    for i in range(len(indices)):
        result[i] = (indices[i] - key[i % key_len]) % 29
    return result

def word_score(text):
    score = 0
    words = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
             'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
             'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO',
             'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
             'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM']
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
    print("FOCUS ON PAGE 28")
    print("="*70)
    
    pages = load_all_pages()
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    p28 = runes_to_indices(pages[28])
    
    print(f"\nPage 28 length: {len(p28)} runes")
    print(f"Master key length: {len(MASTER_KEY)}")
    
    # Full master key as Vigenère
    print("\n" + "="*70)
    print("FULL MASTER KEY (95) AS VIGENÈRE ON PAGE 28")
    print("="*70)
    
    dec = vigenere_decrypt(p28, MASTER_KEY)
    text = indices_to_text(dec)
    print(f"\nFull text:\n{text}")
    print(f"\nScore: {word_score(text)}")
    print(f"\nSegmented:\n{segment_text(text)}")
    
    # Partial master key (24 chars)
    print("\n" + "="*70)
    print("PARTIAL MASTER KEY (24) AS VIGENÈRE ON PAGE 28")
    print("="*70)
    
    partial_key = MASTER_KEY[:24]
    dec = vigenere_decrypt(p28, partial_key)
    text = indices_to_text(dec)
    print(f"\nFull text:\n{text}")
    print(f"\nScore: {word_score(text)}")
    print(f"\nSegmented:\n{segment_text(text)}")
    
    # Try different partial key lengths
    print("\n" + "="*70)
    print("DIFFERENT PARTIAL KEY LENGTHS")
    print("="*70)
    
    for key_len in range(10, 50):
        partial_key = MASTER_KEY[:key_len]
        dec = vigenere_decrypt(p28, partial_key)
        text = indices_to_text(dec)
        score = word_score(text)
        if score > 150:
            print(f"\nKey length {key_len}: Score {score}")
            print(f"  {text[:100]}")
    
    # What if the key needs an offset?
    print("\n" + "="*70)
    print("TRYING KEY WITH OFFSET")
    print("="*70)
    
    for offset in range(len(MASTER_KEY) - 20):
        for key_len in range(15, 35):
            if offset + key_len > len(MASTER_KEY):
                continue
            partial_key = MASTER_KEY[offset:offset+key_len]
            dec = vigenere_decrypt(p28, partial_key)
            text = indices_to_text(dec)
            score = word_score(text)
            if score > 200:
                print(f"\nOffset {offset}, Key length {key_len}: Score {score}")
                print(f"  {text[:100]}")
    
    # What if each page uses a DIFFERENT offset of the master key?
    print("\n" + "="*70)
    print("TESTING ALL PAGES WITH KEY OFFSET")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        best = (0, 0, 0, "")
        
        for offset in range(len(MASTER_KEY)):
            # Use key starting from offset (and wrapping)
            key = np.concatenate([MASTER_KEY[offset:], MASTER_KEY[:offset]])
            
            for key_len in [len(MASTER_KEY), len(pg_idx), 24, 47, 95]:
                if key_len > len(MASTER_KEY):
                    continue
                partial_key = key[:key_len]
                dec = vigenere_decrypt(pg_idx, partial_key)
                text = indices_to_text(dec)
                score = word_score(text)
                if score > best[2]:
                    best = (offset, key_len, score, text[:80])
        
        offset, klen, score, text = best
        print(f"\nPage {pg_num}: Best offset={offset}, key_len={klen}, score={score}")
        print(f"  {text}")

if __name__ == "__main__":
    main()

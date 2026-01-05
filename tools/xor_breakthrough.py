#!/usr/bin/env python3
"""
BREAKTHROUGH ANALYSIS: PAGE 47 XOR OFFSET 45
=============================================

Page 47 with XOR key (master key offset 45) gives score 237!
This is our best result yet. Let's analyze it thoroughly.
"""

import re
import numpy as np
from pathlib import Path

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

def segment_text(text):
    words = [
        'CONSCIOUSNESS', 'CIRCUMFERENCE', 'ENLIGHTENMENT', 'UNDERSTANDING',
        'INTELLIGENCE', 'DIVINITY', 'PARABLE', 'THROUGH', 'BETWEEN', 'BECAUSE',
        'SHOULD', 'BEFORE', 'THERE', 'INSTAR', 'EMERGE', 'SURFACE', 'WISDOM',
        'WITHIN', 'TRUTH', 'WHERE', 'WHICH', 'THEIR', 'BEING', 'THESE', 'THOSE',
        'ABOUT', 'WORLD', 'WOULD', 'COULD', 'AFTER', 'FIRST', 'OTHER', 'THING',
        'BEHOLD', 'DIVINE', 'SACRED', 'SECRET', 'HIDDEN', 'LIGHT', 'NIGHT',
        'BENEATH', 'BEYOND', 'ABOVE', 'BELOW', 'INSIDE', 'OUTSIDE', 'AROUND',
        'ALWAYS', 'NEVER', 'SOMETIMES', 'OFTEN', 'RARELY', 'ONCE', 'TWICE',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
        'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'WHAT', 'THAT', 'WITH',
        'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'MUST', 'SHED', 'FIND',
        'LIKE', 'SELF', 'MIND', 'EACH', 'ONLY', 'JUST', 'WHEN', 'INTO', 'SUCH',
        'THAN', 'SOME', 'TIME', 'VERY', 'THEN', 'MADE', 'OVER', 'MANY', 'MOST',
        'KNOW', 'SEEN', 'SEEK', 'FEEL', 'DOES', 'DONE', 'GOOD', 'LOOK', 'TAKE',
        'GIVE', 'KEEP', 'EVEN', 'ALSO', 'COME', 'CAME', 'BACK', 'WORK', 'WELL',
        'WAY', 'DAY', 'MAY', 'SAY', 'SEE', 'NOW', 'NEW', 'OLD', 'MAN', 'MEN',
        'TWO', 'OWN', 'PUT', 'SET', 'LET', 'GET', 'SAW', 'GOT', 'TOO', 'USE',
        'WAR', 'END', 'FAR', 'FEW', 'BIG', 'BAD', 'RUN', 'AWAY', 'FEAT',
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
    print("BREAKTHROUGH ANALYSIS: PAGE 47 XOR OFFSET 45")
    print("="*70)
    
    pages = load_all_pages()
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Best result: Page 47 with offset 45
    print("\n" + "="*70)
    print("PAGE 47 XOR WITH MASTER KEY (OFFSET 45)")
    print("="*70)
    
    p47 = runes_to_indices(pages[47])
    n = len(p47)
    
    offset = 45
    key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
    xored = (p47 ^ key) % 29
    text = indices_to_text(xored)
    
    print(f"\nFull decrypted text ({len(text)} chars):")
    print(text)
    print(f"\nScore: {word_score(text)}")
    print(f"\nSegmented:")
    print(segment_text(text))
    
    # What is the key at offset 45?
    print("\n" + "="*70)
    print("ANALYZING THE KEY STARTING AT OFFSET 45")
    print("="*70)
    
    key_from_45 = MASTER_KEY[45:]
    print(f"Key indices from offset 45: {list(key_from_45[:20])}...")
    print(f"As letters: {indices_to_text(key_from_45[:20])}...")
    
    # Apply the same offset 45 XOR to ALL unsolved pages
    print("\n" + "="*70)
    print("APPLYING OFFSET 45 XOR TO ALL UNSOLVED PAGES")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key = np.tile(np.roll(MASTER_KEY, -45), (n // len(MASTER_KEY) + 1))[:n]
        xored = (pg_idx ^ key) % 29
        text = indices_to_text(xored)
        score = word_score(text)
        
        print(f"\nPage {pg_num} | Score: {score}")
        print(f"  {text[:100]}")
        print(f"  Segmented: {segment_text(text[:80])}")
    
    # Find the BEST offset for each page
    print("\n" + "="*70)
    print("BEST XOR OFFSET FOR EACH UNSOLVED PAGE")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        best = (0, 0, "")
        for offset in range(len(MASTER_KEY)):
            key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
            xored = (pg_idx ^ key) % 29
            text = indices_to_text(xored)
            score = word_score(text)
            if score > best[1]:
                best = (offset, score, text[:80])
        
        offset, score, text = best
        print(f"\nPage {pg_num}: Best offset={offset:2d} | Score: {score}")
        print(f"  {text}")
    
    # Try combining XOR with other operations
    print("\n" + "="*70)
    print("XOR (OFFSET 45) → CAESAR SHIFT")
    print("="*70)
    
    for pg_num in [47]:  # Focus on best page
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key = np.tile(np.roll(MASTER_KEY, -45), (n // len(MASTER_KEY) + 1))[:n]
        xored = (pg_idx ^ key) % 29
        
        for shift in range(29):
            shifted = (xored - shift) % 29
            text = indices_to_text(shifted)
            score = word_score(text)
            
            if score > 200:
                print(f"Page {pg_num} | XOR 45 → shift={shift:2d} | Score: {score}")
                print(f"  {text[:80]}")
    
    # What happens if we DON'T mod 29 after XOR?
    print("\n" + "="*70)
    print("TRYING PURE SUBTRACTION (not XOR)")
    print("="*70)
    
    for pg_num in [47]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key = np.tile(np.roll(MASTER_KEY, -45), (n // len(MASTER_KEY) + 1))[:n]
        
        # Subtraction instead of XOR
        subtracted = (pg_idx - key) % 29
        text = indices_to_text(subtracted)
        score = word_score(text)
        
        print(f"Page {pg_num} | Subtraction | Score: {score}")
        print(f"  {text[:100]}")
        print(f"  Segmented: {segment_text(text[:80])}")

if __name__ == "__main__":
    main()

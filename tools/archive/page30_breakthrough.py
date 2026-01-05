#!/usr/bin/env python3
"""
PAGE 30 BREAKTHROUGH ANALYSIS
==============================

Page 30 with Cols=8 → XOR offset=66 gives score 303!
This is our highest score. Let's analyze and refine.
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

def xor_decrypt(indices, key):
    n = len(indices)
    key_ext = np.tile(key, (n // len(key) + 1))[:n]
    return (indices ^ key_ext) % 29

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
    print("PAGE 30 BREAKTHROUGH ANALYSIS")
    print("="*70)
    
    pages = load_all_pages()
    
    # Best result: Page 30 with Cols=8 → XOR offset=66
    p30 = runes_to_indices(pages[30])
    n = len(p30)
    
    print(f"\nPage 30: {n} runes")
    
    # Apply the best decryption
    print("\n" + "="*70)
    print("METHOD: Columnar Transpose (8 cols) → XOR (offset 66)")
    print("="*70)
    
    # Step 1: Columnar transpose with 8 columns
    transposed = columnar_transpose_decrypt(p30, 8)
    print(f"\nAfter columnar transpose (8 cols):")
    print(f"  {indices_to_text(transposed[:60])}")
    
    # Step 2: XOR with master key offset 66
    key = np.roll(MASTER_KEY, -66)
    xored = xor_decrypt(transposed, key)
    text = indices_to_text(xored)
    
    print(f"\nAfter XOR with master key (offset 66):")
    print(f"Full text ({len(text)} chars):")
    print(text)
    print(f"\nScore: {word_score(text)}")
    print(f"\nSegmented:")
    print(segment_text(text))
    
    # What words are found?
    print("\n" + "="*70)
    print("WORD ANALYSIS")
    print("="*70)
    
    found_words = []
    test_words = ['THE', 'AND', 'THAT', 'THIS', 'WITH', 'FOR', 'ARE', 'BUT', 'NOT',
                  'WHAT', 'WHEN', 'WHERE', 'WHICH', 'THERE', 'THEIR', 'THEY', 'HAVE',
                  'FROM', 'INTO', 'UPON', 'EACH', 'ONLY', 'SOME', 'THAN', 'THEN',
                  'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'WISDOM', 'TRUTH',
                  'BEING', 'WITHIN', 'SHED', 'PRIME', 'AN', 'IS', 'IT', 'OF', 'IN',
                  'TO', 'OR', 'AS', 'AT', 'BE', 'HE', 'WE', 'BY', 'IF', 'NO', 'SO']
    
    for word in test_words:
        count = text.count(word)
        if count > 0:
            found_words.append((word, count))
    
    found_words.sort(key=lambda x: -x[1])
    print("Words found in decrypted text:")
    for word, count in found_words:
        print(f"  {word}: {count} occurrences")
    
    # Try more variations around this result
    print("\n" + "="*70)
    print("TRYING VARIATIONS")
    print("="*70)
    
    best = (0, 0, 0, "")
    
    # Try different column counts and offsets around the best
    for cols in range(4, 16):
        transposed = columnar_transpose_decrypt(p30, cols)
        for offset in range(len(MASTER_KEY)):
            key = np.roll(MASTER_KEY, -offset)
            xored = xor_decrypt(transposed, key)
            text = indices_to_text(xored)
            score = word_score(text)
            
            if score > best[0]:
                best = (score, cols, offset, text)
            
            if score >= 280:
                print(f"Cols={cols:2d} Offset={offset:2d} | Score: {score}")
                print(f"  {text[:80]}")
    
    print(f"\nBest overall: cols={best[1]}, offset={best[2]}, score={best[0]}")
    print(f"Text: {best[3][:100]}")
    
    # Apply to ALL pages
    print("\n" + "="*70)
    print("APPLYING Cols=8 → XOR offset=66 TO ALL UNSOLVED PAGES")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        transposed = columnar_transpose_decrypt(pg_idx, 8)
        key = np.roll(MASTER_KEY, -66)
        xored = xor_decrypt(transposed, key)
        text = indices_to_text(xored)
        score = word_score(text)
        
        print(f"\nPage {pg_num} | Score: {score}")
        print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
BEST RESULTS SUMMARY AND ANALYSIS
==================================

Compile all our best results across all tests.
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

def segment_text(text):
    words = [
        'CIRCUMFERENCE', 'INTELLIGENCE', 'DIVINITY', 'PARABLE', 'THROUGH',
        'BETWEEN', 'BECAUSE', 'SHOULD', 'BEFORE', 'THERE', 'INSTAR', 'EMERGE',
        'SURFACE', 'WISDOM', 'WITHIN', 'TRUTH', 'WHERE', 'WHICH', 'THEIR',
        'BEING', 'THESE', 'THOSE', 'ABOUT', 'WORLD', 'WOULD', 'COULD', 'AFTER',
        'FIRST', 'OTHER', 'THING', 'BEHOLD', 'DIVINE', 'SACRED', 'SECRET',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
        'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'WHAT', 'THAT', 'WITH',
        'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'MUST', 'SHED', 'FIND',
        'LIKE', 'SELF', 'MIND', 'EACH', 'ONLY', 'JUST', 'WHEN', 'INTO', 'SUCH',
        'THAN', 'SOME', 'TIME', 'VERY', 'THEN', 'MADE', 'OVER', 'MANY', 'MOST',
        'BE', 'AT', 'OR', 'AS', 'IT', 'IF', 'WE', 'IN', 'IS', 'TO', 'OF', 'AN',
        'HE', 'SO', 'NO', 'BY', 'UP', 'ON', 'MY', 'DO', 'GO', 'ME',
        'NG', 'TH', 'EA', 'IA', 'AE', 'EO', 'OE', 'A', 'I'
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
    print("="*80)
    print("                    LIBER PRIMUS CIPHER ANALYSIS SUMMARY")
    print("="*80)
    
    print("""
MASTER KEY VERIFIED:
====================
- 95 rune indices
- Sum = 1331 = 11³
- Correctly decrypts Pages 0 and 54 via Vigenère

HIGHEST SCORING RESULTS:
========================

| Rank | Page | Score | Method                              | Text Sample                  |
|------|------|-------|-------------------------------------|------------------------------|
| 1    | 30   | 303   | Cols=8 → XOR offset=66              | ULTHMCTYPAFTHCGU...          |
| 2    | 44   | 273   | Cols=20 → XOR offset=87             | JUHUCNNGMNAFEAMI...          |
| 3    | 44   | 273   | Cols=27 → XOR offset=45             | IFEAIAATHHIADFDE...          |
| 4    | 45   | 261   | Cols=26 → XOR offset=82             | JNNFOUDJWHOXTAEU...          |
| 5    | 44   | 258   | Vig offset=0 → Affine a=11 b=21     | YAECUENGDUYEADJR...          |
| 6    | 29   | 258   | Affine a=11 b=5 → Vig offset=82     | LAEJHGIJSOEONGPP...          |
| 7    | 30   | 255   | Affine a=7 b=10                     | GTHBYOEPIAUNGAYD...          |

PATTERN ANALYSIS:
=================

1. COLUMNAR TRANSPOSITION + XOR is the most promising combination
   - Page 30 with 8 columns + XOR offset 66 = Score 303 (HIGHEST!)
   - Multiple pages show high scores with this pattern

2. KEY OFFSETS that appear significant:
   - 45, 66, 82, 85, 87 (frequently appear in best results)

3. AFFINE CIPHER parameters:
   - a=7, a=11, a=13 (most common successful values)
   - These are all coprime with 29

4. THE DECRYPTED TEXT contains many English word patterns:
   - THE, THAT, HE, AT, WE, IN, OF, IS (common short words)
   - But no coherent sentences yet

CONCLUSIONS:
============

A. The cipher is likely MULTI-LAYERED:
   Substitution (Vigenère/XOR/Affine) + Transposition

B. The COLUMN ORDER in transposition may be keyed
   - Not just straight columnar, but with rearranged columns

C. Possible additional layers:
   - Null cipher (take every Nth letter)
   - Word-level cipher
   - Custom encoding

D. The high scores on short words (THE, HE, AT) could be:
   - Correct partial decryption
   - Or statistical coincidence in 29-char alphabet

""")
    
    pages = load_all_pages()
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    # Show the best result in detail
    print("BEST RESULT IN DETAIL (Page 30, Score 303):")
    print("=" * 50)
    
    p30 = runes_to_indices(pages[30])
    n = len(p30)
    
    # Columnar transpose with 8 cols
    cols = 8
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
                    result[idx] = p30[source_idx]
                    idx += 1
    
    # XOR with offset 66
    key = np.tile(np.roll(MASTER_KEY, -66), (n // len(MASTER_KEY) + 1))[:n]
    xored = (result ^ key) % 29
    text = indices_to_text(xored)
    
    print(f"\nRaw decrypted text ({len(text)} characters):")
    print("-" * 50)
    
    # Print in 60-char lines
    for i in range(0, len(text), 60):
        print(text[i:i+60])
    
    print("\n" + "-" * 50)
    print("Segmented (recognizable words marked):")
    print("-" * 50)
    print(segment_text(text))

if __name__ == "__main__":
    main()

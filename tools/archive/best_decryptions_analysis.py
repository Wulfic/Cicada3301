#!/usr/bin/env python3
"""
DETAILED ANALYSIS OF BEST DECRYPTIONS
======================================

Examine the top-scoring decryptions in detail.
"""

import numpy as np
from pathlib import Path
import re

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                       20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                       17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                       5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                       14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def extend_key(key, length):
    return np.tile(key, (length // len(key) + 1))[:length]

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
            pages[page_num] = runes_to_indices(runes_only)
    return pages

def analyze_detailed():
    pages = load_all_pages()
    
    print("="*80)
    print("🔍 DETAILED DECRYPTION ANALYSIS")
    print("="*80)
    
    # Best configurations found
    configs = [
        (47, "rot=page, off=page", 47, 18, 'sub', 102),
        (29, "rot=page+1, off=page+1", 30, 1, 'sub', 99),
        (28, "rot=95-page, off=page", 67, 28, 'xor', 95),
        (45, "rot=page, off=page*3", 45, 19, 'sub', 89),
        (44, "rot=page, off=0", 44, 0, 'xor', 87),
        (31, "rot=page*11, off=page*11", 56, 22, 'sub', 87),
        (52, "rot=page, off=page", 52, 23, 'sub', 87),
        (30, "rot=page, off=0", 30, 0, 'sub', 86),
    ]
    
    for pg_num, formula, rot, off, op, score in configs:
        pg_idx = pages[pg_num]
        
        rotated = np.roll(MASTER_KEY, rot)
        key = (rotated + off) % 29
        extended = extend_key(key, len(pg_idx))
        
        if op == 'xor':
            decrypted = (pg_idx ^ extended) % 29
        else:
            decrypted = (pg_idx - extended) % 29
        
        text = indices_to_text(decrypted)
        
        print(f"\n{'='*80}")
        print(f"📄 PAGE {pg_num}")
        print(f"{'='*80}")
        print(f"Formula: {formula}")
        print(f"Parameters: rot={rot}, off={off}, op={op}")
        print(f"Score: {score}")
        print(f"Length: {len(text)} characters")
        print()
        print("FULL DECRYPTED TEXT:")
        print("-" * 60)
        
        # Word wrap at 60 chars for readability
        for i in range(0, len(text), 60):
            print(text[i:i+60])
        
        print("-" * 60)
        
        # Search for meaningful words
        meaningful_words = [
            'THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'FOR', 'BE', 'AS',
            'TRUTH', 'WISDOM', 'DIVINE', 'DIVINITY', 'EMERGE', 'INSTAR',
            'PARABLE', 'CIRCUMFERENCE', 'LIGHT', 'DARKNESS', 'SOUL', 'MIND',
            'PRIME', 'PATH', 'KNOWLEDGE', 'ENLIGHTEN', 'BEING', 'BECOMING',
            'YOU', 'YOUR', 'WE', 'OUR', 'THEY', 'THEIR', 'HIS', 'HER',
            'WILL', 'WITH', 'FROM', 'THAT', 'THIS', 'WHAT', 'WHICH',
            'NOT', 'BUT', 'ALL', 'SOME', 'ONE', 'TWO', 'THREE',
            'FIND', 'SEEK', 'KNOW', 'UNDERSTAND', 'SEE', 'HEAR',
            'WITHIN', 'WITHOUT', 'ABOVE', 'BELOW'
        ]
        
        found_words = []
        for word in meaningful_words:
            count = text.upper().count(word)
            if count > 0:
                found_words.append((word, count))
        
        found_words.sort(key=lambda x: -x[1])
        
        print("\nWords found:")
        for word, count in found_words[:15]:
            print(f"  {word}: {count}x")
    
    # Test if there's a consistent formula pattern
    print("\n" + "="*80)
    print("📐 FORMULA PATTERN ANALYSIS")
    print("="*80)
    
    print("""
    Based on our analysis, the best formulas appear to be:
    
    1. rot = page_number (mod 95)
       off = page_number (mod 29)
       operation = subtraction
       → Works well for pages 47, 52
    
    2. rot = page_number + 1 (mod 95)
       off = page_number + 1 (mod 29)
       operation = subtraction
       → Works well for pages 29, 48
    
    3. rot = 95 - page_number (mod 95)
       off = page_number (mod 29)
       operation = XOR
       → Works well for page 28
    
    4. rot = page_number (mod 95)
       off = page_number * 3 (mod 29)
       operation = subtraction
       → Works well for pages 45, 46
    
    5. rot = page_number * 11 (mod 95)
       off = page_number * 11 (mod 29)
       operation = subtraction
       → Works well for page 31 (11 is special: key sum = 11³)
    """)

if __name__ == "__main__":
    analyze_detailed()

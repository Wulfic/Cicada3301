#!/usr/bin/env python3
"""
ANALYZE TOP RESULTS
===================

Our intensive batch found:
- Page 29: Score 101 (xor, rot=6, off=17)
- Page 47: Score 101 (xor, rot=52, off=16)
- Page 28: Score 99 (xor, rot=34, off=14)

Let's analyze these more closely and see if we can improve them further.
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

def add_spaces(text):
    """Try to add spaces to make text more readable"""
    # Known word boundaries
    known_words = ['THE', 'AND', 'THAT', 'THIS', 'WITH', 'THEY', 'HAVE', 'FROM', 
                   'WILL', 'WHAT', 'WHEN', 'KNOW', 'YOUR', 'WOULD', 'THEIR', 'WHICH',
                   'THESE', 'ABOUT', 'OTHER', 'THERE', 'BEING', 'THOSE',
                   'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
                   'WITHIN', 'SURFACE', 'TUNNELING', 'WISDOM', 'TRUTH', 'PRIME',
                   'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR', 
                   'AS', 'AT', 'SO', 'NO', 'DO', 'MY', 'UP', 'IF', 'GO', 'BY',
                   'FOR', 'NOT', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 
                   'OUT', 'ARE', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY', 'WHO']
    
    # Sort by length (longest first) to avoid partial matches
    known_words.sort(key=len, reverse=True)
    
    result = text.upper()
    # Simple word boundary finding (very basic)
    for word in known_words:
        if word in result:
            result = result.replace(word, f' {word} ')
    
    # Clean up extra spaces
    while '  ' in result:
        result = result.replace('  ', ' ')
    
    return result.strip()

def main():
    print("="*70)
    print("🔍 ANALYZING TOP RESULTS")
    print("="*70)
    
    pages = load_all_pages()
    
    # Top results from intensive batch
    top_results = [
        (29, 'xor', 6, 17),
        (47, 'xor', 52, 16),
        (28, 'xor', 34, 14),
        (31, 'xor', 70, 17),
        (45, 'xor', 75, 2),
        (44, 'xor', 36, 24),
        (48, 'xor', 5, 15),
        (52, 'xor', 21, 11),  # Contains TRUTH!
        (30, 'xor', 12, 6),
        (27, 'xor', 34, 5),
    ]
    
    for pg_num, op, rotation, offset in top_results:
        print(f"\n{'='*70}")
        print(f"📄 PAGE {pg_num}")
        print(f"{'='*70}")
        
        pg_idx = pages[pg_num]
        
        # Apply transformation
        rotated = np.roll(MASTER_KEY, rotation)
        key = (rotated + offset) % 29
        extended = extend_key(key, len(pg_idx))
        
        if op == 'xor':
            decrypted = (pg_idx ^ extended) % 29
        else:
            decrypted = (pg_idx - extended) % 29
        
        text = indices_to_text(decrypted)
        
        print(f"\nOperation: {op}")
        print(f"Rotation: {rotation}, Offset: {offset}")
        print(f"Length: {len(text)} characters")
        
        print(f"\n📝 Raw text:")
        # Print in chunks of 70
        for i in range(0, len(text), 70):
            print(f"   {text[i:i+70]}")
        
        print(f"\n📝 With spacing attempt:")
        spaced = add_spaces(text)
        for i in range(0, len(spaced), 70):
            print(f"   {spaced[i:i+70]}")
        
        # Count specific high-value words
        for word in ['PARABLE', 'INSTAR', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE', 
                     'WISDOM', 'TRUTH', 'PRIME', 'TUNNELING', 'SURFACE', 'WITHIN']:
            count = text.upper().count(word)
            if count > 0:
                print(f"   ⭐ Found '{word}' {count} time(s)!")
    
    # Investigate Page 52 TRUTH finding
    print("\n" + "="*70)
    print("🎯 SPECIAL FOCUS: Page 52 (Contains TRUTH!)")
    print("="*70)
    
    pg_idx = pages[52]
    rotated = np.roll(MASTER_KEY, 21)
    key = (rotated + 11) % 29
    extended = extend_key(key, len(pg_idx))
    decrypted = (pg_idx ^ extended) % 29
    text = indices_to_text(decrypted)
    
    print(f"\nFull decrypted text:")
    for i in range(0, len(text), 60):
        print(f"   {text[i:i+60]}")
    
    # Find where TRUTH appears
    pos = text.upper().find('TRUTH')
    if pos >= 0:
        context = text[max(0,pos-20):pos+25]
        print(f"\n   TRUTH found at position {pos}")
        print(f"   Context: ...{context}...")
    
    # Try fine-tuning around these best parameters
    print("\n" + "="*70)
    print("🔧 FINE-TUNING: Testing nearby parameters")
    print("="*70)
    
    # For Page 52, try rotations 19-23 with offsets 9-13
    best_score = 0
    best_params = None
    best_text = ""
    
    for rot in range(15, 28):
        for off in range(6, 16):
            rotated = np.roll(MASTER_KEY, rot)
            key = (rotated + off) % 29
            extended = extend_key(key, len(pg_idx))
            decrypted = (pg_idx ^ extended) % 29
            text = indices_to_text(decrypted)
            
            # Score
            score = 0
            for word in ['TRUTH', 'WISDOM', 'DIVINE', 'PRIME', 'SACRED', 'PARABLE']:
                score += text.upper().count(word) * len(word) * 5
            for word in ['THE', 'AND', 'THAT', 'WITH']:
                score += text.upper().count(word) * len(word) * 2
            
            if score > best_score:
                best_score = score
                best_params = (rot, off)
                best_text = text
    
    if best_params:
        print(f"\nPage 52 - Best fine-tuned parameters:")
        print(f"   Rotation: {best_params[0]}, Offset: {best_params[1]}")
        print(f"   Score: {best_score}")
        print(f"   Text: {best_text[:100]}...")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
PAGE-NUMBER FORMULA INVESTIGATION
==================================

Based on our deep analysis, we found promising results when:
- Rotation = page_number mod 95
- Offset = calculated from page_number

Let's test ALL pages with page-number-based formulas systematically.
"""

import numpy as np
from pathlib import Path
import re
from collections import Counter

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

COMMON_WORDS = {
    'THE', 'OF', 'AND', 'A', 'TO', 'IN', 'IS', 'IT', 'YOU', 'THAT', 
    'HE', 'WAS', 'FOR', 'ON', 'ARE', 'AS', 'WITH', 'HIS', 'THEY', 
    'I', 'AT', 'BE', 'THIS', 'HAVE', 'FROM', 'OR', 'ONE', 'HAD', 
    'BY', 'NOT', 'BUT', 'WHAT', 'ALL', 'WERE', 'WE', 'WHEN', 'YOUR',
    'CAN', 'SAID', 'EACH', 'WHICH', 'SHE', 'DO', 'HOW', 'THEIR',
    'WISDOM', 'TRUTH', 'DIVINE', 'DIVINITY', 'SOUL', 'MIND', 'LIGHT',
    'DARKNESS', 'PATH', 'KNOWLEDGE', 'ENLIGHTEN', 'EMERGE', 'PRIME',
    'CIRCUMFERENCE', 'INSTAR', 'PARABLE', 'BEING', 'BECOMING'
}

def count_word_matches(text):
    count = 0
    text_upper = text.upper()
    for word in COMMON_WORDS:
        count += text_upper.count(word)
    return count

def test_formulas():
    pages = load_all_pages()
    
    print("="*80)
    print("📐 PAGE-NUMBER FORMULA TESTING")
    print("="*80)
    
    # Define different formulas to test
    formulas = [
        ("rot=page, off=0", lambda p: (p % 95, 0)),
        ("rot=page, off=page", lambda p: (p % 95, p % 29)),
        ("rot=page, off=29-page", lambda p: (p % 95, (29 - p) % 29)),
        ("rot=page*2, off=page", lambda p: ((p * 2) % 95, p % 29)),
        ("rot=page, off=page*3", lambda p: (p % 95, (p * 3) % 29)),
        ("rot=95-page, off=page", lambda p: ((95 - p) % 95, p % 29)),
        ("rot=page-1, off=page-1", lambda p: ((p-1) % 95, (p-1) % 29)),
        ("rot=page+1, off=page+1", lambda p: ((p+1) % 95, (p+1) % 29)),
        ("rot=page*11, off=page*11", lambda p: ((p * 11) % 95, (p * 11) % 29)),  # 11 is special (key sum = 11^3)
        ("rot=page, off=11", lambda p: (p % 95, 11)),  # Fixed offset of 11
        ("rot=page+11, off=11", lambda p: ((p + 11) % 95, 11)),
    ]
    
    best_results = []
    
    for formula_name, formula_fn in formulas:
        print(f"\n📊 Formula: {formula_name}")
        print("-" * 60)
        
        formula_results = []
        
        for pg_num, pg_idx in sorted(pages.items()):
            if pg_num in [0, 54, 56, 57]:
                continue
            
            rot, off = formula_fn(pg_num)
            
            rotated = np.roll(MASTER_KEY, rot)
            key = (rotated + off) % 29
            extended = extend_key(key, len(pg_idx))
            
            # Test both operations
            for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                                ('xor', lambda x, k: (x ^ k) % 29)]:
                decrypted = op(pg_idx, extended)
                text = indices_to_text(decrypted)
                score = count_word_matches(text)
                
                formula_results.append((pg_num, op_name, rot, off, score, text[:40]))
                
                if score >= 70:
                    print(f"  ⭐ Page {pg_num}: {op_name}, rot={rot}, off={off} -> {score} words")
                    best_results.append((pg_num, formula_name, op_name, rot, off, score, text))
    
    # Sort best results
    best_results.sort(key=lambda x: -x[5])
    
    print("\n" + "="*80)
    print("🏆 TOP RESULTS ACROSS ALL FORMULAS")
    print("="*80)
    
    for pg, formula, op, rot, off, score, text in best_results[:20]:
        print(f"  Page {pg}: {formula}, {op}, rot={rot}, off={off} -> {score} words")
        print(f"       Text: {text}...")
        print()
    
    # Export best per page
    print("\n" + "="*80)
    print("📋 BEST FORMULA PER PAGE")
    print("="*80)
    
    best_per_page = {}
    for pg, formula, op, rot, off, score, text in best_results:
        if pg not in best_per_page or score > best_per_page[pg][0]:
            best_per_page[pg] = (score, formula, op, rot, off, text)
    
    for pg in sorted(best_per_page.keys()):
        score, formula, op, rot, off, text = best_per_page[pg]
        print(f"Page {pg}: Score {score}, {formula}, {op}")
        
        # Check for special words
        for word in ['TRUTH', 'WISDOM', 'DIVINE', 'EMERGE', 'INSTAR', 'PARABLE', 'CIRCUMFERENCE']:
            if word in text.upper():
                print(f"  ⭐ Contains '{word}'!")

if __name__ == "__main__":
    test_formulas()

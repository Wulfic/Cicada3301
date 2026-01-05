#!/usr/bin/env python3
"""
ANALYZE TOP NO-KEY RESULTS
==========================

Looking deeper at the most promising results from the no-key brute force.
"""

import re
import numpy as np
from pathlib import Path

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

def test_skip(indices, skip):
    """Skip cipher with given skip value"""
    n = len(indices)
    result = np.zeros(n, dtype=np.int32)
    pos = 0
    for i in range(n):
        result[i] = indices[pos]
        pos = (pos + skip) % n
    return result

def test_polyalphabetic(indices, key):
    """Polyalphabetic with short key"""
    key_arr = np.array(key, dtype=np.int32)
    extended = np.tile(key_arr, (len(indices) // len(key_arr) + 1))[:len(indices)]
    return (indices - extended) % 29

def manual_segment(text):
    """Try to manually segment text into words"""
    # Common English words sorted by length (longer first)
    words = [
        'CONSCIOUSNESS', 'ENLIGHTENMENT', 'CIRCUMFERENCE',
        'UNDERSTANDING', 'INTELLIGENCE', 'DIVINITY',
        'PARABLE', 'INSTAR', 'EMERGE', 'SURFACE', 'WISDOM', 'WITHIN',
        'THROUGH', 'BETWEEN', 'BECAUSE', 'SHOULD', 'BEFORE', 'THERE',
        'TRUTH', 'WHERE', 'WHICH', 'THEIR', 'BEING', 'THESE', 'THOSE',
        'ABOUT', 'WORLD', 'WOULD', 'COULD', 'AFTER', 'FIRST',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'WHAT',
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY',
        'BE', 'AT', 'OR', 'AS', 'IT', 'IF', 'WE', 'IN', 'IS', 'TO', 'OF',
        'AN', 'HE', 'SO', 'NO', 'BY', 'UP', 'ON', 'MY', 'DO', 'GO', 'ME',
        'A', 'I'
    ]
    
    found = []
    remaining = text
    pos = 0
    
    while remaining and len(found) < 100:
        matched = False
        for word in words:
            if remaining.startswith(word):
                found.append(word)
                remaining = remaining[len(word):]
                matched = True
                break
        if not matched:
            # Skip one character
            remaining = remaining[1:]
    
    return found

def main():
    print("="*70)
    print("ANALYZING TOP NO-KEY RESULTS")
    print("="*70)
    
    pages = load_all_pages()
    
    # Analyze Page 46 skip=27
    print("\n" + "="*70)
    print("PAGE 46 - Skip Cipher (skip=27)")
    print("="*70)
    
    p46 = runes_to_indices(pages[46])
    print(f"Page 46 length: {len(p46)}")
    
    result = test_skip(p46, 27)
    text = indices_to_text(result)
    print(f"Full text: {text}")
    
    # The pattern repeats - let's find the period
    for period in range(5, 50):
        chunk1 = text[:period]
        chunk2 = text[period:2*period]
        if chunk1 == chunk2:
            print(f"Found repeating pattern with period {period}: {chunk1}")
            break
    
    # This is likely a characteristic of the skip interacting with page length
    print(f"\nGCD(page_length={len(p46)}, skip=27) = {np.gcd(len(p46), 27)}")
    
    # Analyze Page 47 with poly key that shows TRUTH
    print("\n" + "="*70)
    print("PAGE 47 - Polyalphabetic with key (24, 3, 27, 15, 15)")
    print("="*70)
    
    p47 = runes_to_indices(pages[47])
    print(f"Page 47 length: {len(p47)}")
    
    key = [24, 3, 27, 15, 15]
    result = test_polyalphabetic(p47, key)
    text = indices_to_text(result)
    print(f"Full text:\n{text}")
    
    # Look for word patterns
    print(f"\nWord segmentation attempt:")
    words = manual_segment(text)
    print(f"Found {len(words)} potential words: {' '.join(words[:30])}")
    
    # Count specific words
    for word in ['THE', 'TRUTH', 'AND', 'IS', 'OF', 'TO', 'BE', 'IN', 'IT', 'WE', 'AN']:
        count = text.count(word)
        if count > 0:
            print(f"  {word}: {count} occurrences")
    
    # Analyze Page 29 with XOR 11
    print("\n" + "="*70)
    print("PAGE 29 - XOR with value 11")
    print("="*70)
    
    p29 = runes_to_indices(pages[29])
    print(f"Page 29 length: {len(p29)}")
    
    result = p29 ^ 11
    text = indices_to_text(result)
    print(f"Full text:\n{text}")
    
    print(f"\nWord segmentation attempt:")
    words = manual_segment(text)
    print(f"Found {len(words)} potential words: {' '.join(words[:30])}")
    
    # Try different polyalphabetic keys on Page 29
    print("\n" + "="*70)
    print("PAGE 29 - Testing various short keys")
    print("="*70)
    
    # Best keys from the results
    test_keys = [
        (9, 6, 3, 9, 18),
        (9, 6, 3, 9, 24),
        (9, 6, 3, 21, 27),
    ]
    
    for key in test_keys:
        result = test_polyalphabetic(p29, list(key))
        text = indices_to_text(result)
        
        word_count = 0
        for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'BE', 'IN', 'IT', 'WE', 'AN', 'OR', 'SO', 'NO']:
            word_count += text.count(word)
        
        print(f"\nKey {key}:")
        print(f"  Text: {text[:100]}...")
        print(f"  Common words found: {word_count}")
        
        # Try adding Caesar shift on top
        for shift in range(29):
            shifted = (result - shift) % 29
            shifted_text = indices_to_text(shifted)
            
            words_found = []
            for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'BE', 'IN', 'IT', 'WE', 'AN']:
                count = shifted_text.count(word)
                if count > 0:
                    words_found.append(f"{word}={count}")
            
            if len(words_found) > 5:
                print(f"    +shift {shift}: {shifted_text[:60]}... [{', '.join(words_found)}]")
    
    # Let's try finding patterns in what works
    print("\n" + "="*70)
    print("PATTERN ANALYSIS - What makes Page 46 skip=27 work?")
    print("="*70)
    
    # Page 46 has high score because of THE appearing in repetition
    # Let's see what other skip values produce THE
    
    for pg_num in [27, 28, 29, 30, 31]:
        pg_idx = runes_to_indices(pages[pg_num])
        print(f"\nPage {pg_num} (length={len(pg_idx)}):")
        
        for skip in range(2, 30):
            if skip < len(pg_idx):
                result = test_skip(pg_idx, skip)
                text = indices_to_text(result)
                the_count = text.count('THE')
                if the_count > 2:
                    print(f"  skip={skip}: {the_count}× THE - {text[:60]}...")

if __name__ == "__main__":
    main()

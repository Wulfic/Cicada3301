#!/usr/bin/env python3
"""
SHIFTED KEY ATTACK
==================

We discovered that Pages 0 and 54 use a 95-character key.
What if other pages use the SAME key but shifted by their page number?

Try: Key_for_page_N = Key rotated by N positions

Also try: Key + PageNumber as offset
"""

import re
import numpy as np
from pathlib import Path
from collections import Counter

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

# Common English words + Cicada vocabulary
COMMON_WORDS = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
               'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
               'YOU', 'WAS', 'ARE', 'BUT', 'ALL', 'CAN', 'HER', 'ONE', 'OUR',
               'THEM', 'THEN', 'FROM', 'THEY', 'WILL', 'WHAT', 'WHEN', 'KNOW']
CICADA_WORDS = ['INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
               'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM',
               'DIVINE', 'SACRED', 'LIBER', 'PRIMUS', 'CIPHER', 'GNOSIS']

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def calculate_ioc(indices):
    n = len(indices)
    if n < 2:
        return 0.0
    counts = np.bincount(indices % 29, minlength=29)
    numerator = np.sum(counts * (counts - 1))
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0.0

def score_english(text):
    text_upper = text.upper()
    score = 0
    words_found = []
    for word in COMMON_WORDS + CICADA_WORDS:
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word) * (2 if word in CICADA_WORDS else 1)
            words_found.append(f"{word}({count})")
    return score, words_found

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

def main():
    print("="*70)
    print("🔄 SHIFTED KEY ATTACK")
    print("="*70)
    
    pages = load_all_pages()
    
    # The master key (derived from Page0 - Page57)
    master_key = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                           20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                           17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                           5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                           14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)
    
    key_len = len(master_key)
    print(f"\nMaster key length: {key_len}")
    
    # Skip already solved/known pages
    skip_pages = [0, 54, 56, 57]
    
    best_results = []
    
    print("\n" + "="*70)
    print("STRATEGY 1: Rotate key by page number")
    print("="*70)
    
    for pg_num in sorted(pages.keys()):
        if pg_num in skip_pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Try different rotations
        best_score = 0
        best_rotation = 0
        best_text = ""
        
        for rotation in range(key_len):
            # Rotate the key
            rotated_key = np.roll(master_key, rotation)
            
            # Extend key to page length
            extended_key = np.tile(rotated_key, (len(pg_idx) // key_len + 1))[:len(pg_idx)]
            
            # Decrypt
            decrypted = (pg_idx - extended_key) % 29
            text = indices_to_text(decrypted)
            score, words = score_english(text)
            
            if score > best_score:
                best_score = score
                best_rotation = rotation
                best_text = text
                best_words = words
        
        if best_score > 30:
            print(f"\n⚠️ Page {pg_num}: Best rotation = {best_rotation}, Score = {best_score}")
            print(f"   Words: {', '.join(best_words[:10])}")
            print(f"   Text: {best_text[:80]}...")
            best_results.append(('rotate', pg_num, best_rotation, best_score, best_text))
    
    print("\n" + "="*70)
    print("STRATEGY 2: Add page number to key values")
    print("="*70)
    
    for pg_num in sorted(pages.keys()):
        if pg_num in skip_pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Try different offsets
        best_score = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(29):
            # Add offset to key
            modified_key = (master_key + offset) % 29
            
            # Extend key to page length
            extended_key = np.tile(modified_key, (len(pg_idx) // key_len + 1))[:len(pg_idx)]
            
            # Decrypt
            decrypted = (pg_idx - extended_key) % 29
            text = indices_to_text(decrypted)
            score, words = score_english(text)
            
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = text
                best_words = words
        
        if best_score > 30:
            print(f"\n⚠️ Page {pg_num}: Best offset = {best_offset}, Score = {best_score}")
            print(f"   Words: {', '.join(best_words[:10])}")
            print(f"   Text: {best_text[:80]}...")
            best_results.append(('offset', pg_num, best_offset, best_score, best_text))
    
    print("\n" + "="*70)
    print("STRATEGY 3: Rotate AND add offset")
    print("="*70)
    
    for pg_num in sorted(pages.keys()):
        if pg_num in skip_pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        
        best_score = 0
        best_params = (0, 0)
        best_text = ""
        
        # Try rotation by page number, plus various offsets
        rotation = pg_num % key_len
        rotated_key = np.roll(master_key, rotation)
        
        for offset in range(29):
            modified_key = (rotated_key + offset) % 29
            extended_key = np.tile(modified_key, (len(pg_idx) // key_len + 1))[:len(pg_idx)]
            
            decrypted = (pg_idx - extended_key) % 29
            text = indices_to_text(decrypted)
            score, words = score_english(text)
            
            if score > best_score:
                best_score = score
                best_params = (rotation, offset)
                best_text = text
                best_words = words
        
        if best_score > 30:
            print(f"\n⚠️ Page {pg_num}: Rotation={best_params[0]}, Offset={best_params[1]}, Score={best_score}")
            print(f"   Words: {', '.join(best_words[:10])}")
            print(f"   Text: {best_text[:80]}...")
            best_results.append(('rot+off', pg_num, best_params, best_score, best_text))
    
    print("\n" + "="*70)
    print("STRATEGY 4: Use page number as starting position in key")
    print("="*70)
    
    for pg_num in sorted(pages.keys()):
        if pg_num in skip_pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        
        best_score = 0
        best_start = 0
        best_text = ""
        
        for start_pos in range(key_len):
            # Use key starting from position 'start_pos'
            key_stream = np.concatenate([master_key[start_pos:], master_key[:start_pos]])
            extended_key = np.tile(key_stream, (len(pg_idx) // key_len + 1))[:len(pg_idx)]
            
            decrypted = (pg_idx - extended_key) % 29
            text = indices_to_text(decrypted)
            score, words = score_english(text)
            
            if score > best_score:
                best_score = score
                best_start = start_pos
                best_text = text
                best_words = words
        
        if best_score > 40:  # Higher threshold for this strategy
            print(f"\n⚠️ Page {pg_num}: Start position = {best_start}, Score = {best_score}")
            print(f"   Words: {', '.join(best_words[:10])}")
            print(f"   Text: {best_text[:80]}...")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY OF BEST RESULTS")
    print("="*70)
    
    if best_results:
        best_results.sort(key=lambda x: -x[3])
        for strategy, pg_num, params, score, text in best_results[:10]:
            print(f"\n{strategy.upper()}: Page {pg_num} - Score {score}")
            print(f"   Params: {params}")
            print(f"   Text: {text[:100]}...")
    else:
        print("\nNo results with score > 30 found with shifted key strategies.")
        print("\nThe key may need a different transformation, or")
        print("each page may have its own unique key derivation.")

if __name__ == "__main__":
    main()

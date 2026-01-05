#!/usr/bin/env python3
"""
DEEP ANALYSIS OF AUTOKEY RESULTS
=================================

The running key attack found promising autokey results:
- Page 27: init_len=6, init_val=28 → score=177
- Page 29: init_len=6, init_val=14 → score=192
- Page 31: init_len=4, init_val=14 → score=195

Let's analyze these in detail and try to find complete decryptions.
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

def main():
    print("="*70)
    print("DEEP ANALYSIS OF AUTOKEY RESULTS")
    print("="*70)
    
    pages = load_all_pages()
    
    # Analyze the top autokey findings
    top_autokey = [
        (27, 6, 28),  # score 177
        (29, 6, 14),  # score 192
        (31, 4, 14),  # score 195
        (29, 2, 14),  # score 159
        (31, 8, 14),  # score 150
        (29, 8, 7),   # score 180
        (31, 9, 7),   # score 147
        (29, 9, 28),  # score 150
    ]
    
    for pg_num, init_len, init_val in top_autokey:
        pg_idx = runes_to_indices(pages[pg_num])
        init_key = np.full(init_len, init_val, dtype=np.int32)
        
        decrypted = autokey_decrypt(pg_idx, init_key)
        text = indices_to_text(decrypted)
        score = score_text(text)
        
        print(f"\n" + "="*70)
        print(f"Page {pg_num} | init_len={init_len} | init_val={init_val} | score={score}")
        print("="*70)
        print(f"Full text:\n{text}")
        
        # Count words
        word_counts = {}
        for word in ['THE', 'AND', 'OF', 'TO', 'IN', 'BE', 'IT', 'IS', 'AN', 'HE', 'WE', 'OR', 'AT', 'IF', 'NO', 'SO', 'BY', 'MY', 'DO', 'AS']:
            count = text.count(word)
            if count > 0:
                word_counts[word] = count
        print(f"Words found: {word_counts}")
    
    # Now let's do exhaustive autokey search
    print("\n" + "="*70)
    print("EXHAUSTIVE AUTOKEY SEARCH")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    best_results = []
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Try all initial key lengths 1-10 and all values 0-28
        for init_len in range(1, 12):
            for init_val in range(29):
                init_key = np.full(init_len, init_val, dtype=np.int32)
                decrypted = autokey_decrypt(pg_idx, init_key)
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score > 150:
                    best_results.append((pg_num, init_len, init_val, score, text[:80]))
    
    best_results.sort(key=lambda x: -x[3])
    
    print(f"\nTop 20 autokey results (score > 150):\n")
    for pg, init_len, init_val, score, text in best_results[:20]:
        print(f"Page {pg} | init_len={init_len} | init_val={init_val} | score={score}")
        print(f"  {text}")
    
    # Try varying initial keys (not all same value)
    print("\n" + "="*70)
    print("VARIABLE INITIAL KEY AUTOKEY SEARCH")
    print("="*70)
    
    # For short keys (length 2-4), try all combinations
    best_variable = []
    
    for pg_num in [27, 28, 29, 30, 31]:  # Focus on promising pages
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Length 2 keys - all combinations
        for k0 in range(0, 29, 2):  # Step of 2 to reduce search space
            for k1 in range(0, 29, 2):
                init_key = np.array([k0, k1], dtype=np.int32)
                decrypted = autokey_decrypt(pg_idx, init_key)
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score > 120:
                    best_variable.append((pg_num, tuple(init_key), score, text[:80]))
        
        # Length 3 keys - sample
        for k0 in range(0, 29, 5):
            for k1 in range(0, 29, 5):
                for k2 in range(0, 29, 5):
                    init_key = np.array([k0, k1, k2], dtype=np.int32)
                    decrypted = autokey_decrypt(pg_idx, init_key)
                    text = indices_to_text(decrypted)
                    score = score_text(text)
                    
                    if score > 120:
                        best_variable.append((pg_num, tuple(init_key), score, text[:80]))
    
    best_variable.sort(key=lambda x: -x[2])
    
    print(f"\nTop 15 variable initial key autokey results:\n")
    for pg, init_key, score, text in best_variable[:15]:
        print(f"Page {pg} | init_key={init_key} | score={score}")
        print(f"  {text}")
    
    # Analyze Page 31 with init_val=14 more deeply
    print("\n" + "="*70)
    print("PAGE 31 DEEP ANALYSIS (best autokey result)")
    print("="*70)
    
    p31 = runes_to_indices(pages[31])
    
    # Try all init_lengths with value 14
    for init_len in range(1, 15):
        init_key = np.full(init_len, 14, dtype=np.int32)
        decrypted = autokey_decrypt(p31, init_key)
        text = indices_to_text(decrypted)
        score = score_text(text)
        
        if score > 100:
            print(f"\ninit_len={init_len}: score={score}")
            print(f"  {text}")
    
    # What about using "THE" as initial key?
    print("\n" + "="*70)
    print("USING COMMON WORDS AS INITIAL KEY")
    print("="*70)
    
    word_keys = {
        'THE': [16, 8, 18],  # T, H, E
        'AND': [24, 9, 23],  # A, N, D
        'INSTAR': [10, 9, 15, 16, 24, 4],  # I, N, S, T, A, R
        'PARABLE': [13, 24, 4, 24, 17, 20, 18],  # P, A, R, A, B, L, E
        'TRUTH': [16, 4, 1, 16, 8],  # T, R, U, T, H
        'DIVINITY': [23, 10, 26, 10, 9, 10, 16, 26],  # D, I, V, I, N, I, T, Y
    }
    
    for word, key in word_keys.items():
        init_key = np.array(key, dtype=np.int32)
        
        for pg_num in unsolved:
            pg_idx = runes_to_indices(pages[pg_num])
            decrypted = autokey_decrypt(pg_idx, init_key)
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > 100:
                print(f"\nPage {pg_num} with '{word}' as key (score={score}):")
                print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

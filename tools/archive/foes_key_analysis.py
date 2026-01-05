#!/usr/bin/env python3
"""
DEEP ANALYSIS OF THE "FOES" KEY RESULT
======================================

Page 31 with "FOES" as key produces text starting with "THE..."
This is very promising! Let's explore this more.
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
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

def word_to_indices(word):
    """Convert English word to Gematria indices"""
    word = word.upper()
    indices = []
    i = 0
    while i < len(word):
        if i + 1 < len(word):
            digraph = word[i:i+2]
            if digraph in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        letter = word[i]
        if letter == 'K':
            letter = 'C'
        if letter == 'Q':
            letter = 'C'
        if letter == 'V':
            letter = 'U'
        if letter == 'Z':
            letter = 'S'
        if letter in LETTER_TO_IDX:
            indices.append(LETTER_TO_IDX[letter])
        i += 1
    return np.array(indices, dtype=np.int32)

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

def autokey_decrypt(indices, init_key):
    result = np.zeros(len(indices), dtype=np.int32)
    init_len = len(init_key)
    
    for i in range(len(indices)):
        if i < init_len:
            k = init_key[i]
        else:
            k = result[i - init_len]
        result[i] = (indices[i] - k) % 29
    
    return result

def segment_text(text):
    """Try to segment text into words and show best reading"""
    words_dict = [
        'CONSCIOUSNESS', 'ENLIGHTENMENT', 'CIRCUMFERENCE', 'UNDERSTANDING',
        'INTELLIGENCE', 'DIVINITY', 'PARABLE', 'THROUGH', 'BETWEEN', 'BECAUSE',
        'SHOULD', 'BEFORE', 'THERE', 'INSTAR', 'EMERGE', 'SURFACE', 'WISDOM',
        'WITHIN', 'TRUTH', 'WHERE', 'WHICH', 'THEIR', 'BEING', 'THESE', 'THOSE',
        'ABOUT', 'WORLD', 'WOULD', 'COULD', 'AFTER', 'FIRST', 'OTHER', 'THING',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
        'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'WHAT', 'THAT', 'WITH',
        'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'MUST', 'SHED', 'FIND',
        'LIKE', 'SELF', 'MIND', 'EACH', 'ONLY', 'JUST', 'WHEN', 'INTO', 'SUCH',
        'THAN', 'SOME', 'TIME', 'VERY', 'THEN', 'MADE', 'OVER', 'MANY', 'MOST',
        'BE', 'AT', 'OR', 'AS', 'IT', 'IF', 'WE', 'IN', 'IS', 'TO', 'OF', 'AN',
        'HE', 'SO', 'NO', 'BY', 'UP', 'ON', 'MY', 'DO', 'GO', 'ME', 'OE', 'NG',
        'TH', 'EA', 'IA', 'AE', 'EO', 'A', 'I'
    ]
    
    result = []
    i = 0
    while i < len(text):
        matched = False
        for word in words_dict:
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
    print("DEEP ANALYSIS: PAGE 31 WITH KEY 'FOES'")
    print("="*70)
    
    pages = load_all_pages()
    
    # Page 31 with FOES
    p31_runes = pages[31]
    p31_idx = runes_to_indices(p31_runes)
    
    foes_key = word_to_indices("FOES")
    print(f"\nFOES as indices: {list(foes_key)}")  # [0, 22, 18, 15] = F, OE, E, S
    
    decrypted = autokey_decrypt(p31_idx, foes_key)
    text = indices_to_text(decrypted)
    
    print(f"\nFull decrypted text ({len(text)} chars):")
    print(text)
    
    print(f"\nSegmented:")
    print(segment_text(text))
    
    # Try variations on FOES
    print("\n" + "="*70)
    print("TRYING VARIATIONS ON 'FOES' KEY")
    print("="*70)
    
    variations = [
        "FOES", "FOE", "FRIEND", "FRIENDS", "ENEMY", "ENEMIES",
        "FOESOF", "FOESAND", "FOESARE", "THEFOES", "OURFOES",
        "YOURFOES", "ALLFOES", "MANYFOES",
        
        # Other 4-letter words starting with F-O-E/OE
        "FORE", "FORM", "FORD", "FOLK", "FOOD", "FOOT", "FOOL",
        "FOWL", "FOLD", "FONT", "FOUL", "FOUR",
        
        # Try F, OE, E, S separately as parts of longer keys
    ]
    
    for var in variations:
        key = word_to_indices(var)
        if len(key) == 0:
            continue
        dec = autokey_decrypt(p31_idx, key)
        txt = indices_to_text(dec)
        
        # Check if starts with THE
        if txt.startswith("THE"):
            print(f"\nKey: {var}")
            print(f"  Indices: {list(key)}")
            print(f"  Text: {txt[:100]}")
            print(f"  Segmented: {segment_text(txt[:100])}")
    
    # What if the key is (0, 22, 18, 15) for F, OE, E, S? 
    # But what about 4-letter keys with different index interpretations?
    print("\n" + "="*70)
    print("EXHAUSTIVE 4-INDEX KEYS THAT START WITH 'THE...'")
    print("="*70)
    
    good_keys = []
    for k0 in range(29):
        for k1 in range(29):
            for k2 in range(29):
                for k3 in range(29):
                    key = np.array([k0, k1, k2, k3], dtype=np.int32)
                    dec = autokey_decrypt(p31_idx, key)
                    txt = indices_to_text(dec)
                    
                    # Check for good English patterns
                    if txt.startswith("THE") or txt.startswith("AND") or txt.startswith("FOR"):
                        # Score the rest
                        score = 0
                        for word in ['THE', 'AND', 'FOR', 'TO', 'OF', 'IS', 'IN', 'IT', 'BE',
                                     'AS', 'AT', 'BY', 'WE', 'AN', 'OR', 'NO', 'SO', 'IF']:
                            score += txt.count(word) * len(word)
                        if score > 30:
                            good_keys.append((k0, k1, k2, k3, score, txt[:100]))
    
    good_keys.sort(key=lambda x: -x[4])
    
    for k0, k1, k2, k3, score, txt in good_keys[:20]:
        key_letters = f"{LETTERS[k0]} {LETTERS[k1]} {LETTERS[k2]} {LETTERS[k3]}"
        print(f"\nKey: ({k0},{k1},{k2},{k3}) = {key_letters} | score={score}")
        print(f"  {txt}")
        print(f"  Segmented: {segment_text(txt[:80])}")
    
    # Apply best key to all pages
    print("\n" + "="*70)
    print("APPLYING FOES KEY TO ALL UNSOLVED PAGES")
    print("="*70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        dec = autokey_decrypt(pg_idx, foes_key)
        txt = indices_to_text(dec)
        
        print(f"\nPage {pg_num}:")
        print(f"  {txt[:100]}")
        print(f"  Segmented: {segment_text(txt[:80])}")

if __name__ == "__main__":
    main()

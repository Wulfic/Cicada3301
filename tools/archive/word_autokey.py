#!/usr/bin/env python3
"""
WORD-BASED AUTOKEY ATTACK
=========================

Test actual English words as the initial key for autokey cipher.
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
        # Check for digraphs first
        if i + 1 < len(word):
            digraph = word[i:i+2]
            if digraph in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        # Single letter - handle K as C
        letter = word[i]
        if letter == 'K':
            letter = 'C'
        if letter == 'Q':
            letter = 'C'  # or skip?
        if letter == 'V':
            letter = 'U'  # Old English convention
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
    print("WORD-BASED AUTOKEY ATTACK")
    print("="*70)
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Dictionary of potential Cicada-related words
    words = [
        # Cicada themes
        "INSTAR", "PARABLE", "DIVINITY", "EMERGENCE", "CONSCIOUSNESS",
        "ENLIGHTENMENT", "WISDOM", "TRUTH", "PRIME", "PILGRIM", "SELF",
        "MIND", "SURFACE", "SHED", "CIRCUMFERENCE", "WITHIN", "CICADA",
        
        # Numbers as words
        "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT",
        "NINE", "TEN", "ELEVEN", "THIRTEEN", "SEVENTEEN", "NINETEEN",
        
        # Liber AL references
        "NUIT", "HADIT", "RA", "HOOR", "KHUIT", "CROWLEY", "THELEMA",
        "WILL", "LOVE", "LAW", "THOU", "UNTO", "LIGHT", "DARKNESS",
        "STAR", "NIGHT", "HEAVEN", "EARTH", "SECRET", "KEY",
        
        # Philosophy
        "KNOW", "THYSELF", "ORACLE", "DELPHI", "SOCRATES", "PLATO",
        "FREEDOM", "NATURE", "REASON", "SOUL", "SPIRIT", "BODY",
        
        # Common short words (as tests)
        "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN",
        "HER", "WAS", "ONE", "OUR", "OUT", "HAS", "HIS", "HAD", "WHAT",
        "THAT", "WITH", "HAVE", "THIS", "FROM", "THEY", "BEEN", "MORE",
        "WHEN", "SOME", "SAID", "EACH", "WHICH", "THEIR", "TIME", "WILL",
        
        # Common prefixes/beginnings
        "ATHE", "ANTHE", "INTHE", "OFTHE", "TOTHE", "FORTHE",
        "WHENAT", "THOSE", "THESE", "THERE", "WHERE", "ABOUT",
        
        # The word that scored well: FOES and variants
        "FOES", "FRIEND", "FRIENDS", "FOE",
        
        # Other Cicada references
        "LIBER", "PRIMUS", "LIBER PRIMUS", "LIBERPRIMUS",
        "RUNES", "GEMATRIA", "FUTHORC", "ANGLO", "SAXON",
        
        # Latin
        "COGITO", "ERGO", "SUM", "CARPE", "DIEM", "MEMENTO", "MORI",
        "AD", "ASTRA", "PER", "ASPERA", "VENI", "VIDI", "VICI",
        
        # Mystical
        "ADEPT", "INITIATE", "NEOPHYTE", "MAGUS", "MAGE", "OCCULT",
        "HERMETIC", "ESOTERIC", "GNOSIS", "KABBALAH", "TREE", "LIFE",
        
        # Tech
        "CIPHER", "ENCRYPT", "DECRYPT", "CODE", "MESSAGE", "SIGNAL",
        "PROGRAM", "ALGORITHM", "DATA", "INFORMATION",
        
        # Specific phrases
        "BEGIN", "START", "END", "FINISH", "SOLVE", "FIND",
        "SEEK", "SEARCH", "LOOK", "SEE", "HEAR", "FEEL",
        
        # Numbers in Liber Primus context
        "THIRTYTHREE", "FIFTYEIGHT", "NINETYFIVE",
    ]
    
    best_results = []
    
    print(f"\nTesting {len(words)} word-based keys on {len(unsolved)} pages...")
    
    for word in words:
        init_key = word_to_indices(word)
        if len(init_key) == 0:
            continue
            
        for pg_num in unsolved:
            pg_idx = runes_to_indices(pages[pg_num])
            decrypted = autokey_decrypt(pg_idx, init_key)
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > 150:
                best_results.append((word, pg_num, score, text[:100]))
    
    best_results.sort(key=lambda x: -x[2])
    
    print("\n" + "="*70)
    print("TOP WORD-BASED AUTOKEY RESULTS (score > 150)")
    print("="*70)
    
    for word, pg, score, text in best_results[:30]:
        print(f"\nPage {pg} | Key: {word:15s} | score={score}")
        print(f"  {text}")
    
    # Now try some 2-word combinations
    print("\n" + "="*70)
    print("TRYING 2-WORD COMBINATIONS")
    print("="*70)
    
    base_words = ["THE", "AND", "FOR", "NOT", "ARE", "BUT", "YOU", "ALL", 
                  "THAT", "WITH", "THIS", "FROM", "THEY", "MORE", "WHEN",
                  "INSTAR", "PARABLE", "DIVINITY", "TRUTH", "WISDOM"]
    
    combos = []
    for w1 in base_words:
        for w2 in base_words:
            combos.append(w1 + w2)
    
    combo_results = []
    
    for combo in combos:
        init_key = word_to_indices(combo)
        if len(init_key) == 0:
            continue
            
        for pg_num in unsolved:
            pg_idx = runes_to_indices(pages[pg_num])
            decrypted = autokey_decrypt(pg_idx, init_key)
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > 200:
                combo_results.append((combo, pg_num, score, text[:100]))
    
    combo_results.sort(key=lambda x: -x[2])
    
    for combo, pg, score, text in combo_results[:20]:
        print(f"\nPage {pg} | Key: {combo:20s} | score={score}")
        print(f"  {text}")
    
    # Test the Parable opening as a key
    print("\n" + "="*70)
    print("TESTING PARABLE TEXT AS AUTOKEY STARTING KEY")
    print("="*70)
    
    parable_starts = [
        "LIKETHEINSTAREMERGES",
        "LIKETHEINSTAR",
        "LIKETHE",
        "INSTAR",
        "EMERGES",
        "FROMTHESURFACE",
        "OFITSCIRCUMFERENCE",
        "SOTOOMUST"
    ]
    
    for parable_key in parable_starts:
        init_key = word_to_indices(parable_key)
        if len(init_key) == 0:
            continue
            
        for pg_num in unsolved:
            pg_idx = runes_to_indices(pages[pg_num])
            decrypted = autokey_decrypt(pg_idx, init_key)
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > 150:
                print(f"\nPage {pg_num} | Key: {parable_key}")
                print(f"Score: {score}")
                print(f"  {text[:100]}")

if __name__ == "__main__":
    main()

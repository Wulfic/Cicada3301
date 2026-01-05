#!/usr/bin/env python3
"""
EXHAUSTIVE CIPHER ANALYSIS

Let's step back and try ALL possible cipher combinations:
1. Different key derivation methods
2. Different cipher modes (additive, subtractive, XOR-like)
3. Running key cipher with Parable text
4. Autokey cipher

The fact that we see scattered English words means we're CLOSE.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def letter_to_idx(letter):
    """Convert English letter(s) to rune index"""
    letter = letter.upper()
    mapping = {
        'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
        'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
        'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
        'Y': 26, 'Z': 15
    }
    return mapping.get(letter, -1)

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

# The Parable text (Page 57) as plaintext for running key cipher
PARABLE_TEXT = """PARABLEANINSTAREMERGENCELIKETHEOTERSHAVSHEDMYSKINMANYTIMESBEFOREWISDOMSBODYISCOVEREDWITHEYESSOMEOFWHICHAREDEADTHOUGHTHEYSTILLSEEANDTHERESOMETHATREMAINAWAKETHERCOMEATIMEWHENONEMUST ABANDONTHEIDEAOFSELFTHESURFACEWEMUSTHEDOUREOS"""

def text_to_indices(text):
    """Convert English text to rune indices"""
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Handle digraphs
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA']:
                idx = LETTERS.index(digraph)
                result.append(idx)
                i += 2
                continue
        
        char = text[i]
        if char.isalpha():
            idx = letter_to_idx(char)
            if idx >= 0:
                result.append(idx)
        i += 1
    return result

def word_score(text):
    WORDS = {'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
             'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
             'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
             'YOU', 'WE', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
             'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
             'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR',
             'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def decrypt_autokey(cipher, start_key, use_plaintext=True):
    """Autokey cipher where key is the plaintext or ciphertext"""
    result = []
    key = list(start_key)
    
    for i, c in enumerate(cipher):
        k = key[i % len(key)] if i < len(key) else (result[i - len(key)] if use_plaintext else cipher[i - len(key)])
        p = (c - k) % 29
        result.append(p)
    
    return ''.join(idx_to_letter(p) for p in result)

def decrypt_running_key(cipher, key_text_indices, offset=0):
    """Running key cipher using Parable text as key"""
    result = []
    key_len = len(key_text_indices)
    
    for i, c in enumerate(cipher):
        k = key_text_indices[(i + offset) % key_len]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    
    return ''.join(result)

def decrypt_double_key(cipher, primary_key, secondary_key, offset1=0, offset2=0):
    """Two layers of Vigenère"""
    # First layer
    temp = []
    for i, c in enumerate(cipher):
        k = primary_key[(i + offset1) % len(primary_key)]
        temp.append((c - k) % 29)
    
    # Second layer
    result = []
    for i, t in enumerate(temp):
        k = secondary_key[(i + offset2) % len(secondary_key)]
        p = (t - k) % 29
        result.append(idx_to_letter(p))
    
    return ''.join(result)

def main():
    pages = load_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Get Page 57 (Parable) for reference
    page57_indices = [rune_to_idx(r) for r in pages[57]]
    
    print("=" * 70)
    print("TEST 1: RUNNING KEY CIPHER WITH PARABLE AS KEY")
    print("=" * 70)
    
    for pg_num in unsolved[:3]:  # Test first 3
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(95):
            text = decrypt_running_key(cipher, page57_indices, offset)
            score = word_score(text)
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = text[:60]
        
        print(f"Page {pg_num}: offset={best_offset}, score={best_score}")
        print(f"  {best_text}...")
    
    print("\n" + "=" * 70)
    print("TEST 2: AUTOKEY CIPHER WITH MASTER KEY SEED")
    print("=" * 70)
    
    for pg_num in unsolved[:3]:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        for seed_len in [5, 10, 15, 20, 29, 30, 40, 50, 95]:
            for offset in range(min(95, 95 - seed_len + 1)):
                seed = MASTER_KEY[offset:offset + seed_len]
                
                # Autokey with plaintext
                text = decrypt_autokey(cipher, seed, use_plaintext=True)
                score = word_score(text)
                if score > best_score:
                    best_score = score
                    best_config = (seed_len, offset, 'plaintext')
                    best_text = text[:60]
                
                # Autokey with ciphertext
                text = decrypt_autokey(cipher, seed, use_plaintext=False)
                score = word_score(text)
                if score > best_score:
                    best_score = score
                    best_config = (seed_len, offset, 'ciphertext')
                    best_text = text[:60]
        
        print(f"Page {pg_num}: best config={best_config}, score={best_score}")
        print(f"  {best_text}...")
    
    print("\n" + "=" * 70)
    print("TEST 3: DOUBLE VIGENÈRE (KEY + PAGE NUMBER OFFSET)")
    print("=" * 70)
    
    # Try using page number in gematria as second key
    for pg_num in unsolved[:3]:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Create secondary key from page number
        # Example: Page 27 = 2, 7 = PRIMES[2], PRIMES[7] = 5, 19
        secondary_keys = [
            [pg_num % 29],  # Just page number
            [pg_num // 10, pg_num % 10],  # Digits
            [PRIMES[pg_num % 29] % 29],  # Prime of page number
            [(pg_num * 2) % 29, (pg_num * 3) % 29],  # Multiples
        ]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        for sk_idx, sec_key in enumerate(secondary_keys):
            for off1 in range(95):
                for off2 in range(len(sec_key)):
                    text = decrypt_double_key(cipher, MASTER_KEY, sec_key, off1, off2)
                    score = word_score(text)
                    if score > best_score:
                        best_score = score
                        best_config = (sk_idx, off1, off2)
                        best_text = text[:60]
        
        print(f"Page {pg_num}: best config={best_config}, score={best_score}")
        print(f"  {best_text}...")
    
    print("\n" + "=" * 70)
    print("TEST 4: KEY MULTIPLICATION BY PAGE NUMBER")
    print("=" * 70)
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        # Try key * page_num mod 29
        for mult in [pg_num, pg_num % 29, PRIMES[pg_num % 29] if pg_num < 29 else pg_num]:
            modified_key = [(k * mult) % 29 for k in MASTER_KEY]
            
            for offset in range(95):
                result = []
                for i, c in enumerate(cipher):
                    k = modified_key[(i + offset) % 95]
                    p = (c - k) % 29
                    result.append(idx_to_letter(p))
                text = ''.join(result)
                score = word_score(text)
                
                if score > best_score:
                    best_score = score
                    best_config = (mult, offset)
                    best_text = text[:60]
        
        if best_score >= 15:
            print(f"Page {pg_num}: mult={best_config[0]}, offset={best_config[1]}, score={best_score}")
            print(f"  {best_text}...")
    
    print("\n" + "=" * 70)
    print("TEST 5: AFFINE TRANSFORMATION OF KEY")
    print("=" * 70)
    
    # Affine: new_key[i] = (a * key[i] + b) mod 29
    # Only coprime a values work: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
    # (All except 29's divisors - but 29 is prime so all work)
    
    for pg_num in [28, 52]:  # Test most promising pages
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        for a in range(1, 29):
            for b in range(29):
                affine_key = [(a * k + b) % 29 for k in MASTER_KEY]
                
                for offset in range(95):
                    result = []
                    for i, c in enumerate(cipher):
                        k = affine_key[(i + offset) % 95]
                        p = (c - k) % 29
                        result.append(idx_to_letter(p))
                    text = ''.join(result)
                    score = word_score(text)
                    
                    if score > best_score:
                        best_score = score
                        best_config = (a, b, offset)
                        best_text = text[:80]
        
        print(f"Page {pg_num}: a={best_config[0]}, b={best_config[1]}, offset={best_config[2]}, score={best_score}")
        print(f"  {best_text}...")

if __name__ == "__main__":
    main()

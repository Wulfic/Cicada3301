#!/usr/bin/env python3
"""
TRANSPOSITION ANALYSIS

What if the pages are:
1. First transposed (reordered)  
2. Then Vigenère encrypted

Or the other direction - we need to untranspose after Vigenère decrypt.

The high IoC after Vigenère decryption (~92-98% letter frequency match)
suggests we're CLOSE but there may be a transposition step.
"""

import re
from pathlib import Path
from itertools import permutations
import math

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

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

def decrypt_page(cipher_runes, key, offset=0):
    """Decrypt a page using the given key with offset."""
    result = []
    for i, r in enumerate(cipher_runes):
        c_idx = rune_to_idx(r)
        if c_idx < 0:
            continue
        k = key[(i + offset) % len(key)]
        plain_idx = (c_idx - k) % 29
        result.append(plain_idx)
    return result

def word_score(text):
    """Score based on English word detection"""
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST',
             'SURFACE', 'TUNNEL', 'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME', 'NOT']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word) * 2
    return score

def columnar_transpose_read(text, cols):
    """Read text in columnar fashion"""
    rows = math.ceil(len(text) / cols)
    padded = text + ' ' * (rows * cols - len(text))
    
    # Read column by column
    result = []
    for col in range(cols):
        for row in range(rows):
            idx = row * cols + col
            if idx < len(text):
                result.append(text[idx])
    return ''.join(result)

def columnar_transpose_write(text, cols):
    """Write text in columnar fashion (inverse of read)"""
    rows = math.ceil(len(text) / cols)
    result = [''] * len(text)
    idx = 0
    for col in range(cols):
        for row in range(rows):
            pos = row * cols + col
            if pos < len(text) and idx < len(text):
                result[pos] = text[idx]
                idx += 1
    return ''.join(result)

def zigzag_transpose(text, rails):
    """Rail fence cipher transposition"""
    if rails < 2:
        return text
    
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    return ''.join(''.join(rail) for rail in fence)

def reverse_zigzag(text, rails):
    """Reverse rail fence transposition"""
    if rails < 2:
        return text
    
    n = len(text)
    # Calculate lengths of each rail
    pattern = list(range(rails)) + list(range(rails-2, 0, -1))
    pattern_len = len(pattern)
    
    rail_lens = [0] * rails
    for i in range(n):
        rail_lens[pattern[i % pattern_len]] += 1
    
    # Split text into rails
    rails_data = []
    pos = 0
    for l in rail_lens:
        rails_data.append(list(text[pos:pos+l]))
        pos += l
    
    # Read off in zigzag pattern
    result = []
    for i in range(n):
        rail = pattern[i % pattern_len]
        if rails_data[rail]:
            result.append(rails_data[rail].pop(0))
    
    return ''.join(result)

def indices_to_text(indices):
    return ''.join(idx_to_letter(i) for i in indices)

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("TRANSPOSITION ANALYSIS - DECRYPT THEN TRANSPOSE")
    print("=" * 70)
    
    # First decrypt with best offset, then try transpositions
    test_pages = [27, 28, 29, 30, 31]
    best_offsets = [49, 7, 52, 8, 47]  # From previous analysis
    
    for pg_num, best_offset in zip(test_pages, best_offsets):
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        n = len(cipher)
        
        # Decrypt
        decrypted_indices = decrypt_page(cipher, MASTER_KEY, best_offset)
        decrypted_text = indices_to_text(decrypted_indices)
        
        print(f"\n{'='*60}")
        print(f"PAGE {pg_num} (n={n})")
        print(f"{'='*60}")
        print(f"After Vigenère (offset={best_offset}): {decrypted_text[:50]}...")
        
        # Try columnar transpositions
        print("\nColumnar transposition (different column counts):")
        best_score = 0
        best_config = None
        
        for cols in range(2, 30):
            if n % cols == 0 or cols <= 15:  # Try exact factors and small values
                transposed = columnar_transpose_read(decrypted_text, cols)
                score = word_score(transposed)
                if score > best_score:
                    best_score = score
                    best_config = ('col_read', cols, transposed)
                
                transposed = columnar_transpose_write(decrypted_text, cols)
                score = word_score(transposed)
                if score > best_score:
                    best_score = score
                    best_config = ('col_write', cols, transposed)
        
        # Try rail fence
        for rails in range(2, 10):
            transposed = zigzag_transpose(decrypted_text, rails)
            score = word_score(transposed)
            if score > best_score:
                best_score = score
                best_config = ('zigzag', rails, transposed)
            
            transposed = reverse_zigzag(decrypted_text, rails)
            score = word_score(transposed)
            if score > best_score:
                best_score = score
                best_config = ('rev_zigzag', rails, transposed)
        
        # Try simple reverse
        reversed_text = decrypted_text[::-1]
        score = word_score(reversed_text)
        if score > best_score:
            best_score = score
            best_config = ('reverse', 0, reversed_text)
        
        if best_config:
            method, param, text = best_config
            print(f"  Best: {method}({param}), score={best_score}")
            print(f"  Text: {text[:60]}...")
        else:
            print(f"  No improvement found")

    print("\n" + "=" * 70)
    print("TRANSPOSE BEFORE DECRYPT")
    print("=" * 70)
    
    for pg_num in [27, 28]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        cipher_text = ''.join(idx_to_letter(rune_to_idx(r)) for r in cipher)
        n = len(cipher)
        
        print(f"\nPage {pg_num}:")
        best_score = 0
        best_config = None
        
        # Try transposing before Vigenère decrypt
        for cols in [9, 13, 18, 26]:  # Common grid sizes for 234 = 9×26 = 13×18
            for offset in range(95):
                # Transpose cipher text
                transposed_cipher = columnar_transpose_read(cipher, cols)
                # Decrypt
                decrypted_indices = decrypt_page(transposed_cipher, MASTER_KEY, offset)
                decrypted_text = indices_to_text(decrypted_indices)
                score = word_score(decrypted_text)
                if score > best_score:
                    best_score = score
                    best_config = (cols, offset, decrypted_text)
        
        if best_config:
            cols, offset, text = best_config
            print(f"  Best: cols={cols}, offset={offset}, score={best_score}")
            print(f"  Text: {text[:60]}...")

if __name__ == "__main__":
    main()

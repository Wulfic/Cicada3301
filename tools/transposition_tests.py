#!/usr/bin/env python3
"""
TRANSPOSITION CIPHER TESTS

The letter frequencies are wrong for English. This could mean:
1. Text is transposed after encryption
2. Text is in a different language (Latin?)
3. There's a different encoding scheme

Let's try various transposition methods.
"""

import re
from pathlib import Path
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

def decrypt_with_offset(cipher_indices, offset):
    result = []
    for i, c in enumerate(cipher_indices):
        k = MASTER_KEY[(i + offset) % 95]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def columnar_decrypt(text, cols):
    """Read text column by column"""
    rows = math.ceil(len(text) / cols)
    padded = text + ' ' * (rows * cols - len(text))
    
    result = []
    for row in range(rows):
        for col in range(cols):
            idx = col * rows + row
            if idx < len(text):
                result.append(text[idx])
    return ''.join(result)

def rail_fence_decrypt(text, rails):
    """Rail fence cipher decryption"""
    if rails <= 1:
        return text
    
    n = len(text)
    cycle = 2 * (rails - 1)
    
    # Calculate how many chars in each rail
    rail_lengths = [0] * rails
    for i in range(n):
        rail = min(i % cycle, cycle - i % cycle)
        rail_lengths[rail] += 1
    
    # Build rails from ciphertext
    rail_texts = []
    idx = 0
    for length in rail_lengths:
        rail_texts.append(text[idx:idx + length])
        idx += length
    
    # Read back in zig-zag order
    result = []
    rail_indices = [0] * rails
    for i in range(n):
        rail = min(i % cycle, cycle - i % cycle)
        if rail_indices[rail] < len(rail_texts[rail]):
            result.append(rail_texts[rail][rail_indices[rail]])
            rail_indices[rail] += 1
    
    return ''.join(result)

def word_score(text):
    WORDS = {'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
             'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
             'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
             'YOU', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
             'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
             'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR',
             'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN', 'WE', 'OF'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def spiral_read(text, cols):
    """Read text in spiral from outside to inside"""
    rows = math.ceil(len(text) / cols)
    grid = []
    for i in range(rows):
        row = list(text[i*cols:(i+1)*cols])
        if len(row) < cols:
            row.extend([' '] * (cols - len(row)))
        grid.append(row)
    
    result = []
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    
    while top <= bottom and left <= right:
        # Right
        for i in range(left, right + 1):
            if grid[top][i] != ' ':
                result.append(grid[top][i])
        top += 1
        
        # Down
        for i in range(top, bottom + 1):
            if grid[i][right] != ' ':
                result.append(grid[i][right])
        right -= 1
        
        # Left
        if top <= bottom:
            for i in range(right, left - 1, -1):
                if grid[bottom][i] != ' ':
                    result.append(grid[bottom][i])
            bottom -= 1
        
        # Up
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if grid[i][left] != ' ':
                    result.append(grid[i][left])
            left += 1
    
    return ''.join(result)

def main():
    pages = load_pages()
    
    # Test on page 28 at offset 13 (best so far)
    cipher = [rune_to_idx(r) for r in pages[28]]
    text = decrypt_with_offset(cipher, 13)
    n = len(text)
    
    print("=" * 80)
    print(f"PAGE 28 TRANSPOSITION TESTS (length = {n})")
    print("=" * 80)
    
    print(f"\nFactors of {n}: ", end="")
    factors = [i for i in range(1, n+1) if n % i == 0]
    print(factors)
    
    print("\n" + "-" * 60)
    print("COLUMNAR TRANSPOSITION")
    print("-" * 60)
    
    best_score = 0
    best_config = None
    
    for cols in range(2, min(50, n)):
        result = columnar_decrypt(text, cols)
        score = word_score(result)
        
        if score > best_score:
            best_score = score
            best_config = ('columnar', cols, result)
    
    print(f"Best columnar: cols={best_config[1]}, score={best_config[0] if best_config else 0}")
    if best_config:
        print(f"  {best_config[2][:80]}...")
    
    print("\n" + "-" * 60)
    print("RAIL FENCE")
    print("-" * 60)
    
    for rails in range(2, 20):
        result = rail_fence_decrypt(text, rails)
        score = word_score(result)
        
        if score > best_score:
            best_score = score
            best_config = ('rail_fence', rails, result)
        
        if score > 30:
            print(f"  Rails={rails}, score={score}")
    
    print("\n" + "-" * 60)
    print("REVERSE")
    print("-" * 60)
    
    result = text[::-1]
    score = word_score(result)
    print(f"Reversed: score={score}")
    print(f"  {result[:80]}...")
    
    print("\n" + "-" * 60)
    print("TRYING TRANSPOSITION BEFORE VIGENÈRE")
    print("-" * 60)
    
    # What if the original runes were transposed BEFORE encryption?
    # Then we'd need to apply transposition to cipher first, then decrypt
    
    raw_cipher = pages[28]
    
    for cols in [5, 7, 10, 13, 17, 19, 23, 25]:
        # Transpose the raw runes
        rows = math.ceil(len(raw_cipher) / cols)
        transposed = []
        for row in range(rows):
            for col in range(cols):
                idx = col * rows + row
                if idx < len(raw_cipher):
                    transposed.append(raw_cipher[idx])
        transposed_str = ''.join(transposed)
        
        # Now decrypt
        cipher_indices = [rune_to_idx(r) for r in transposed_str]
        
        for offset in range(95):
            text = decrypt_with_offset(cipher_indices, offset)
            score = word_score(text)
            
            if score > 35:
                print(f"  cols={cols}, offset={offset}, score={score}")
                print(f"    {text[:60]}...")
    
    print("\n" + "=" * 80)
    print("TESTING DIFFERENT RUNE ORDER (ATBASH-LIKE)")
    print("=" * 80)
    
    # What if the runes are in reverse order?
    REVERSE_RUNE = ''.join(reversed(RUNE_ORDER))
    
    def rune_to_idx_reverse(r):
        return REVERSE_RUNE.index(r) if r in REVERSE_RUNE else -1
    
    cipher = [rune_to_idx_reverse(r) for r in pages[28]]
    
    for offset in range(95):
        text = decrypt_with_offset(cipher, offset)
        score = word_score(text)
        
        if score > 30:
            print(f"Reverse rune order, offset={offset}, score={score}")
            print(f"  {text[:60]}...")

if __name__ == "__main__":
    main()

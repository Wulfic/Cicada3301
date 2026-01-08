#!/usr/bin/env python3
"""
CROSS-PAGE HINT ANALYSIS
========================

From the solved pages (visible in images), we have:

SOME WISDOM:
- THE PRIMES ARE SACRED
- THE TOTIENT FUNCTION IS SACRED  
- ALL THINGS SHOULD BE ENCRYPTED

KNOW THIS (number grid with labels):
272  138  shadows  131   151
aethereal  buffers  void  carnal  18
226  obscura  form  245  mobius
18  analog  void  mournful  aethereal
151  131  cabal  138  272

And a 5x5 numeric grid:
272 138 341 131 151
366 199 130 320 18
226 245 91 245 226
18 320 130 199 366
151 131 341 138 272

Note: This is a SYMMETRIC matrix! It reads the same forward/backward

Hypothesis: These numbers might be:
1. Prime sums that decode to words (keys for other pages)
2. Positions/indices for extracting chars
3. Running keys for decryption
"""

import os
from collections import Counter

# Gematria Primus
RUNE_DATA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101), 'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107), 'ᛠ': (28, 'EA', 109)
}

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
LETTERS = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"]
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}
INDEX_TO_LETTER = {i: L for i, L in enumerate(LETTERS)}
RUNE_TO_INDEX = {k: v[0] for k, v in RUNE_DATA.items()}

def word_to_prime_sum(word):
    """Convert word to sum of prime values"""
    word = word.upper()
    total = 0
    i = 0
    while i < len(word):
        if i < len(word) - 1:
            digraph = word[i:i+2]
            if digraph in LETTER_TO_INDEX:
                total += PRIMES[LETTER_TO_INDEX[digraph]]
                i += 2
                continue
        if word[i] in LETTER_TO_INDEX:
            total += PRIMES[LETTER_TO_INDEX[word[i]]]
        i += 1
    return total

def prime_sum_to_possible_words(target, max_len=6):
    """Find all words that could sum to target (brute force for short words)"""
    # This is computationally expensive, so just check known words
    pass

def text_to_indices(text):
    """Convert text to indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        matched = False
        for length in [2, 1]:
            if i + length <= len(text):
                segment = text[i:i+length]
                if segment in LETTER_TO_INDEX:
                    indices.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return indices

def indices_to_text(indices):
    return "".join(INDEX_TO_LETTER.get(i, '?') for i in indices)

print("=" * 70)
print("CROSS-PAGE HINT ANALYSIS")
print("=" * 70)

# The symmetric number grid from solved pages
grid = [
    [272, 138, 341, 131, 151],
    [366, 199, 130, 320, 18],
    [226, 245, 91, 245, 226],
    [18, 320, 130, 199, 366],
    [151, 131, 341, 138, 272]
]

print("\n=== THE NUMBER GRID ===")
for row in grid:
    print("  " + "  ".join(f"{n:3d}" for n in row))

print("\n=== GRID PROPERTIES ===")
# Check symmetry
is_symmetric = all(grid[i][j] == grid[4-i][4-j] for i in range(5) for j in range(5))
print(f"Symmetric (point reflection): {is_symmetric}")

# Unique values
unique = sorted(set(n for row in grid for n in row))
print(f"Unique values: {unique}")

# Check if any are prime sums
print("\n=== CHECKING IF VALUES ARE PRIME SUMS ===")
words_to_check = [
    'SHADOWS', 'VOID', 'CARNAL', 'AETHEREAL', 'BUFFERS', 
    'OBSCURA', 'FORM', 'MOBIUS', 'ANALOG', 'MOURNFUL', 'CABAL',
    'PRIMUS', 'LIBER', 'CICADA', 'TRUTH', 'WISDOM', 'SACRED',
    'PRIME', 'TOTIENT', 'ENCRYPT', 'PILGRIM', 'WELCOME',
    'DIVINITY', 'WITHIN', 'EMERGE', 'INSTAR', 'CIRCUMFERENCE',
    'SELF', 'BEING', 'LAW', 'HOLY', 'INSTRUCTION', 'COMMAND'
]

for word in words_to_check:
    prime_sum = word_to_prime_sum(word)
    if prime_sum in unique:
        print(f"  {word} = {prime_sum} <- MATCH!")
    else:
        # Check if close
        closest = min(unique, key=lambda x: abs(x - prime_sum))
        if abs(closest - prime_sum) <= 10:
            print(f"  {word} = {prime_sum} (close to {closest})")

# The labeled pairs from the image
labeled = {
    272: 'aethereal',
    138: 'buffers', 
    131: 'shadows',
    151: 'void',
    226: 'obscura',
    245: 'form',
    18: 'carnal/analog',
    320: 'mobius/carnal',
    341: 'cabal/shadows',
    366: 'aethereal',
    199: 'buffers/mournful',
    130: '?',
    91: '?'
}

print("\n=== LABELED VALUES FROM IMAGE ===")
for val, label in sorted(labeled.items()):
    actual = word_to_prime_sum(label.split('/')[0]) if label != '?' else None
    print(f"  {val} labeled '{label}' -> actual prime sum: {actual}")

# Test if the grid row sums or column sums mean something
print("\n=== ROW AND COLUMN SUMS ===")
row_sums = [sum(row) for row in grid]
col_sums = [sum(grid[i][j] for i in range(5)) for j in range(5)]
print(f"Row sums: {row_sums}")
print(f"Col sums: {col_sums}")
print(f"Total: {sum(row_sums)}")

# The grid might be a running key or position hints
print("\n=== TESTING GRID AS RUNNING KEY ===")

# Key lengths for pages
KEY_LENGTHS = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

base_path = os.path.dirname(os.path.abspath(__file__))

# Read a page and try using grid values as shifts
for page_num in [2, 3]:
    rune_path = os.path.join(base_path, '..', 'pages', f'page_{page_num:02d}', 'runes.txt')
    if not os.path.exists(rune_path):
        continue
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        runes = f.read().replace('-', '').replace('.', '').replace('\n', '').replace('&', '').replace('$', '').replace('/', '')
    
    indices = [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]
    key_len = KEY_LENGTHS[page_num]
    
    # First layer
    first_layer = [(idx - (i % key_len)) % 29 for i, idx in enumerate(indices)]
    
    # Try using the grid values mod 29 as additional key
    flat_grid = [n for row in grid for n in row]  # 25 values
    grid_key = [n % 29 for n in flat_grid]
    
    # Apply grid key
    decrypted = [(idx + grid_key[i % len(grid_key)]) % 29 for i, idx in enumerate(first_layer)]
    text = indices_to_text(decrypted)
    
    the_count = text.count('THE')
    print(f"\nPage {page_num} + grid key (mod 29): THE count = {the_count}")
    print(f"  Sample: {text[:80]}...")

print("\n=== TESTING WORD LABELS AS KEYS ===")
# The word labels might BE the keys for unsolved pages
label_words = ['SHADOWS', 'VOID', 'CARNAL', 'AETHEREAL', 'BUFFERS', 
               'OBSCURA', 'FORM', 'MOBIUS', 'ANALOG', 'MOURNFUL', 'CABAL']

for page_num in [2, 3, 4]:
    rune_path = os.path.join(base_path, '..', 'pages', f'page_{page_num:02d}', 'runes.txt')
    if not os.path.exists(rune_path):
        continue
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        runes = f.read().replace('-', '').replace('.', '').replace('\n', '').replace('&', '').replace('$', '').replace('/', '')
    
    indices = [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]
    key_len = KEY_LENGTHS[page_num]
    
    # First layer
    first_layer = [(idx - (i % key_len)) % 29 for i, idx in enumerate(indices)]
    
    print(f"\nPage {page_num} with label word keys:")
    best_word = None
    best_score = 0
    
    for word in label_words:
        word_key = text_to_indices(word)
        if not word_key:
            continue
        
        # Try add and sub
        for op in ['add', 'sub']:
            if op == 'add':
                decrypted = [(idx + word_key[i % len(word_key)]) % 29 for i, idx in enumerate(first_layer)]
            else:
                decrypted = [(idx - word_key[i % len(word_key)]) % 29 for i, idx in enumerate(first_layer)]
            
            text = indices_to_text(decrypted)
            the_count = text.count('THE')
            
            if the_count > best_score:
                best_score = the_count
                best_word = f"{word} ({op})"
    
    print(f"  Best: {best_word} with THE count = {best_score}")

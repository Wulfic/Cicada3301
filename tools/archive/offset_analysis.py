#!/usr/bin/env python3
"""
Investigate the offset patterns that give best starting words.
"""

import re

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

def rune_to_letters(runes):
    return ''.join(RUNE_TO_LETTER.get(r, '?') for r in runes)

def get_runes_only(page):
    return ''.join(c for c in page if c in RUNE_TO_IDX)

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

# Best offsets found
best_offsets = {
    27: 12,   # Starts with TO
    28: 30,   # Starts with OF
    29: 32,   # Starts with OR
    30: 3,    # Starts with A
    31: 24,   # Starts with WE
    40: 35,   # Starts with IN
    41: 22,   # Starts with IN
    44: 84,   # Starts with THE
    45: 61,   # Starts with THE
    46: 13,   # Starts with BE
    47: 22,   # Starts with IN
    48: 20,   # Starts with BE
    52: 12,   # Starts with IN
}

print("="*70)
print("OFFSET PATTERN ANALYSIS")
print("="*70)

print("\nPage | Offset | Start | Offset relation to page")
print("-" * 60)
for pg, offset in best_offsets.items():
    cipher = get_runes_only(PAGES[pg])
    decrypted = decrypt_vigenere(cipher, MASTER_KEY, offset)
    text = rune_to_letters(decrypted)[:2]
    
    # Various relationships
    diff = (offset - pg) % 95
    ratio = offset / pg if pg != 0 else 0
    
    print(f" {pg:2d}  |   {offset:2d}   |  {text:2s}   | diff={(offset-pg)%95:2d}, pg*2%95={(pg*2)%95:2d}, pg+offset={pg+offset}")

print("\n" + "="*70)
print("DETAILED LOOK AT PAGE 44 (offset=84, starts 'THE')")
print("="*70)

pg = 44
cipher = get_runes_only(PAGES[pg])
decrypted = decrypt_vigenere(cipher, MASTER_KEY, 84)
text = rune_to_letters(decrypted)

# Split by word boundaries from original
original = PAGES[pg]
words = []
current_word = []
rune_idx = 0
for char in original:
    if char in RUNE_TO_IDX:
        if rune_idx < len(decrypted):
            current_word.append(decrypted[rune_idx])
            rune_idx += 1
    elif char in ['•', '.', ':', '\n']:
        if current_word:
            words.append(''.join(current_word))
            current_word = []
if current_word:
    words.append(''.join(current_word))

print("Words (first 30):")
for i, w in enumerate(words[:30]):
    latin = rune_to_letters(w)
    print(f"  {i+1}: {latin}")

print("\n" + "="*70)
print("CHECK: Maybe different cipher for unsolved pages?")
print("="*70)

# What if unsolved pages use a DIFFERENT cipher entirely?
# Let's check the Index of Coincidence

def index_of_coincidence(text):
    from collections import Counter
    n = len(text)
    if n <= 1:
        return 0
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic

print("\nIndex of Coincidence:")
print("  Expected for random: ~0.0345 (1/29)")
print("  Expected for English in runes: ~0.065-0.070")

# Check solved pages
for pg in [0, 54]:
    cipher = get_runes_only(PAGES[pg])
    ic = index_of_coincidence(cipher)
    print(f"\n  Page {pg} (solved cipher): {ic:.4f}")

# Check unsolved pages
for pg in [27, 28, 29, 44, 45]:
    cipher = get_runes_only(PAGES[pg])
    ic = index_of_coincidence(cipher)
    print(f"  Page {pg} (unsolved):       {ic:.4f}")

print("\n" + "="*70)
print("KASISKI TEST FOR KEY LENGTH CONFIRMATION")
print("="*70)

def kasiski_test(text, min_len=3):
    """Find repeated sequences and their distances."""
    distances = []
    for seq_len in range(min_len, 6):
        for i in range(len(text) - seq_len):
            seq = text[i:i+seq_len]
            for j in range(i+1, len(text) - seq_len):
                if text[j:j+seq_len] == seq:
                    dist = j - i
                    distances.append(dist)
    return distances

from math import gcd
from functools import reduce

for pg in [27, 44, 45]:
    cipher = get_runes_only(PAGES[pg])
    distances = kasiski_test(cipher)
    
    if distances:
        # Find GCD of distances
        common_gcd = reduce(gcd, distances[:20])  # Use first 20 distances
        print(f"\nPage {pg}: {len(distances)} repeated sequences found")
        print(f"  Sample distances: {distances[:10]}")
        print(f"  GCD of first 20: {common_gcd}")

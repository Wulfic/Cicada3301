#!/usr/bin/env python3
"""
Deep Investigation of Page 25 with Liber AL Attack
===================================================
The initial attack showed Page 25 scored 14,875 at offset 900 with ADD mode.
This script performs a detailed investigation.
"""

import os
import re
from collections import Counter

# Gematria Primus mapping
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_INDEX_TO_RUNE = {v: k for k, v in GP_RUNE_TO_INDEX.items()}

LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8,
    'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'Z': 15, 'T': 16,
    'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24,
    'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28, 'Q': 5
}

INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

def read_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [c for c in content if c in GP_RUNE_TO_INDEX]

def text_to_key_indices(text):
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        char = text[i]
        if char in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[char])
        i += 1
    return indices

def decrypt_add(cipher_indices, key_indices):
    result = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (c + k) % 29
        result.append(p)
    return result

def decrypt_sub(cipher_indices, key_indices):
    result = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (c - k) % 29
        result.append(p)
    return result

def indices_to_runeglish(indices):
    return ''.join(INDEX_TO_RUNEGLISH[i] for i in indices)

def load_liber_al():
    with open("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/research/liber_al_vel_legis.txt", 'r', encoding='utf-8') as f:
        return f.read()

# Load data
liber_al = load_liber_al()
key_indices = text_to_key_indices(liber_al)

# Load Page 25
runes = read_runes("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_25/runes.txt")
cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]

print("="*70)
print("PAGE 25 DETAILED INVESTIGATION")
print("="*70)
print(f"Page 25 has {len(runes)} runes")
print(f"Liber AL key has {len(key_indices)} indices")

# Show what Liber AL text is at offset 900
print("\n--- Liber AL text around offset 900 ---")
# Need to map back to original text position
# This is approximate since we're working with indices
chars_per_100_indices = len(liber_al) // (len(key_indices) // 100)
approx_text_pos = (900 * len(liber_al)) // len(key_indices)
print(liber_al[approx_text_pos:approx_text_pos+200])

# Fine-tune around offset 900
print("\n--- Fine-tuning around offset 900 ---")
for offset in range(850, 951, 5):
    key_segment = key_indices[offset:]
    plain = decrypt_add(cipher_indices, key_segment)
    runeglish = indices_to_runeglish(plain)
    
    # Count common words
    word_count = 0
    for word in ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT', 'IT', 'FOR', 'AS', 'WITH', 'BE', 'WAS', 'ARE']:
        word_count += runeglish.count(word)
    
    print(f"Offset {offset}: Words={word_count} | {runeglish[:80]}")

# Try all operations at offset 900
print("\n--- Testing all operations at offset 900 ---")
key_segment = key_indices[900:]

ops = {
    'ADD': lambda c, k: (c + k) % 29,
    'SUB': lambda c, k: (c - k) % 29,
    'REV_SUB': lambda c, k: (k - c) % 29,
    'XOR': lambda c, k: c ^ k if c ^ k < 29 else (c ^ k) % 29,
}

for op_name, op_func in ops.items():
    plain = [op_func(cipher_indices[i], key_segment[i % len(key_segment)]) for i in range(len(cipher_indices))]
    runeglish = indices_to_runeglish(plain)
    print(f"\n{op_name}:")
    print(runeglish[:100])

# Check for Atbash transformation
print("\n--- Testing with Atbash on key ---")
atbash_key = [(28 - k) for k in key_segment]
plain = decrypt_add(cipher_indices, atbash_key)
runeglish = indices_to_runeglish(plain)
print(f"Atbash+ADD: {runeglish[:100]}")

plain = decrypt_sub(cipher_indices, atbash_key)
runeglish = indices_to_runeglish(plain)
print(f"Atbash+SUB: {runeglish[:100]}")

# Try shifting the result by each possible value
print("\n--- Testing post-decryption shifts ---")
key_segment = key_indices[900:]
base_plain = decrypt_add(cipher_indices, key_segment)

for shift in range(29):
    shifted = [(p + shift) % 29 for p in base_plain]
    runeglish = indices_to_runeglish(shifted)
    
    word_count = 0
    for word in ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT']:
        word_count += runeglish.count(word)
    
    if word_count > 0:
        print(f"Shift {shift}: Words={word_count} | {runeglish[:80]}")

# Also investigate Page 20
print("\n" + "="*70)
print("PAGE 20 INVESTIGATION (Score 4715 at offset 0)")
print("="*70)

runes20 = read_runes("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt")
cipher20 = [GP_RUNE_TO_INDEX[r] for r in runes20]
print(f"Page 20 has {len(runes20)} runes")

# Test offset 0 with SUB
plain20 = decrypt_sub(cipher20, key_indices)
runeglish20 = indices_to_runeglish(plain20)
print(f"\nSUB at offset 0:")
print(runeglish20[:200])

# Test with first verse of Liber AL only ("Had! The manifestation of Nuit")
verse_key = text_to_key_indices("Had The manifestation of Nuit")
print(f"\nUsing just verse 1 as repeating key ({len(verse_key)} indices):")
plain20_v1 = decrypt_sub(cipher20, verse_key)
print(indices_to_runeglish(plain20_v1)[:100])

# Check IoC of results
def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counter = Counter(indices)
    n = len(indices)
    num = sum(c * (c-1) for c in counter.values())
    den = n * (n-1)
    return num/den if den > 0 else 0

print(f"\nIoC of Page 20 ciphertext: {calc_ioc(cipher20):.4f}")
print(f"IoC of Page 20 after SUB offset 0: {calc_ioc(plain20):.4f}")

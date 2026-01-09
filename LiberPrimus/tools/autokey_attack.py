#!/usr/bin/env python3
"""
Autokey Cipher Attack on Pages 18-54
=====================================
Since the frequency distribution is almost perfectly flat, this strongly
suggests a running key or AUTOKEY cipher.

Autokey cipher: The key starts with a seed, then the PLAINTEXT is used
to continue the key. This makes standard frequency analysis impossible.

Attack method: Try short seed words and see if extending with plaintext works.
"""

import os
from collections import Counter

# Gematria Primus mapping
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8,
    'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'Z': 15, 'T': 16,
    'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24,
    'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28, 'Q': 5
}

INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

def text_to_indices(text):
    """Convert runeglish text to indices."""
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

def decrypt_autokey(cipher_indices, seed_indices):
    """
    Decrypt autokey cipher.
    Key starts with seed, then each decrypted character extends the key.
    plaintext[i] = (cipher[i] - key[i]) mod 29
    key[i] = seed[i] for i < len(seed), else plaintext[i - len(seed)]
    """
    plaintext = []
    
    for i, c in enumerate(cipher_indices):
        if i < len(seed_indices):
            k = seed_indices[i]
        else:
            k = plaintext[i - len(seed_indices)]
        
        p = (c - k) % 29
        plaintext.append(p)
    
    return plaintext

def indices_to_runeglish(indices):
    return ''.join(INDEX_TO_RUNEGLISH[i] for i in indices)

def score_english(text):
    """Score based on English word detection."""
    score = 0
    common_words = ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT', 'IT', 'FOR', 
                    'AS', 'WITH', 'BE', 'WAS', 'ARE', 'THIS', 'TRUTH', 'SACRED',
                    'PRIMES', 'WISDOM', 'KNOWLEDGE', 'DIVINITY', 'PILGRIM',
                    'WITHIN', 'SEEK', 'FIND', 'BELIEVE', 'NOTHING']
    
    for word in common_words:
        if len(word) >= 3:
            count = text.count(word)
            score += count * len(word) * 10
    
    return score

def read_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [c for c in content if c in GP_RUNE_TO_INDEX]

# Load page 18
runes = read_runes("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_18/runes.txt")
cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]

print("="*70)
print("AUTOKEY CIPHER ATTACK")
print("="*70)
print(f"Page 18 has {len(runes)} runes")

# Seed words to try (from Cicada/LP context)
seed_words = [
    'DIVINITY', 'CICADA', 'PRIMES', 'SACRED', 'TRUTH', 'WISDOM',
    'PILGRIM', 'WELCOME', 'THEPRIMES', 'TOTIENT', 'PARABLE',
    'INSTAR', 'CIRCUMFERENCE', 'CONSUMPTION', 'INTUS', 'KOAN',
    'SELFRELIANCE', 'EMERSON', 'THELEMA', 'NUIT', 'HADIT',
    'ANEND', 'WITHIN', 'DEEPWEB', 'LIBER', 'PRIMUS',
    'THE', 'AND', 'OF', 'TO', 'A', 'IT', 'IS',
    'ANARNING', 'BELIEVENOTHING', 'FROMTHISBOOK',
    'WELCOMEPILGRIM', 'THEPRIMESARESACRED',
]

print("\n--- Testing seed words ---")
results = []

for seed in seed_words:
    seed_indices = text_to_indices(seed)
    if not seed_indices:
        continue
    
    plaintext = decrypt_autokey(cipher_indices, seed_indices)
    runeglish = indices_to_runeglish(plaintext)
    score = score_english(runeglish)
    
    results.append((seed, score, runeglish[:80]))
    
    if score > 0:
        print(f"Seed '{seed}': Score={score}")
        print(f"  {runeglish[:80]}")

# Sort by score
results.sort(key=lambda x: -x[1])
print("\n--- Top 10 Results ---")
for seed, score, preview in results[:10]:
    print(f"Seed '{seed}': Score={score}")
    print(f"  {preview}")

# Try using solved page content as seed
print("\n" + "="*70)
print("TESTING SOLVED PAGE CONTENT AS AUTOKEY SEED")
print("="*70)

# Read solved page content
solved_texts = {
    1: "A WARNING BELIEVE NOTHING FROM THIS BOOK EXCEPT WHAT YOU KNOW TO BE TRUE",
    3: "WELCOME PILGRIM TO THE GREAT JOURNEY",
    5: "THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED",
    55: "AN END WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO",
}

for page_num, text in solved_texts.items():
    seed_indices = text_to_indices(text.replace(' ', ''))
    plaintext = decrypt_autokey(cipher_indices, seed_indices)
    runeglish = indices_to_runeglish(plaintext)
    score = score_english(runeglish)
    
    print(f"\nUsing Page {page_num} as seed ({len(seed_indices)} chars):")
    print(f"  Score: {score}")
    print(f"  {runeglish[:100]}")

# Also test plaintext autokey starting with single letters
print("\n" + "="*70)
print("SINGLE-LETTER SEED AUTOKEY ATTACK")
print("="*70)

best_single = []
for start_idx in range(29):
    seed = [start_idx]
    plaintext = decrypt_autokey(cipher_indices, seed)
    runeglish = indices_to_runeglish(plaintext)
    score = score_english(runeglish)
    best_single.append((INDEX_TO_RUNEGLISH[start_idx], score, runeglish[:80]))

best_single.sort(key=lambda x: -x[1])
print("Top 5 single-letter seeds:")
for letter, score, preview in best_single[:5]:
    print(f"  Starting with '{letter}': Score={score}")
    print(f"    {preview}")

# Try ciphertext autokey (key = previous ciphertext, not plaintext)
print("\n" + "="*70)
print("CIPHERTEXT AUTOKEY ATTACK")
print("="*70)

for seed in ['DIVINITY', 'CICADA', 'PRIMES', 'THE']:
    seed_indices = text_to_indices(seed)
    
    plaintext = []
    for i, c in enumerate(cipher_indices):
        if i < len(seed_indices):
            k = seed_indices[i]
        else:
            k = cipher_indices[i - len(seed_indices)]  # Use ciphertext as key
        
        p = (c - k) % 29
        plaintext.append(p)
    
    runeglish = indices_to_runeglish(plaintext)
    score = score_english(runeglish)
    print(f"Ciphertext autokey with seed '{seed}': Score={score}")
    print(f"  {runeglish[:80]}")

# Test Vigenere with progressive/interrupted key
print("\n" + "="*70)
print("PROGRESSIVE KEY VIGENERE (Key increments)")
print("="*70)

for seed in ['DIVINITY', 'CICADA', 'PRIMES']:
    seed_indices = text_to_indices(seed)
    
    # Progressive: key[i] = (seed[i % len(seed)] + i) mod 29
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = (seed_indices[i % len(seed_indices)] + i) % 29
        p = (c - k) % 29
        plaintext.append(p)
    
    runeglish = indices_to_runeglish(plaintext)
    score = score_english(runeglish)
    print(f"Progressive key with seed '{seed}': Score={score}")
    print(f"  {runeglish[:80]}")

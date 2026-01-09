#!/usr/bin/env python3
"""
PAGE 63 KEY ATTACK
==================
Use the mysterious terms from Page 63 as Vigenère keys for unsolved pages.

Terms found:
- MOBIUS (Möbius strip/function)
- SUOID (unknown - anagram?)
- ANALOGUOID (analog-like entity?)
- CABAL (secret group)
- AETHEREAL (ethereal)
- CARNAL (of the flesh)
- OBSCURA (dark/hidden)
- SHADOWS
- BUFFER

Also try the numbers:
- 272138, 131151, 226, 245, 18, 151131, 138272
- 4768 (138272 / 29)
- 464 (3301 is the 464th prime)

Author: Wulfic
Date: January 2026
"""

import os
import sys
from pathlib import Path

# Gematria Primus
GEMATRIA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101),'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107),'ᛠ': (28, 'EA', 109)
}

ALPHABET_SIZE = 29
RUNE_TO_INDEX = {k: v[0] for k, v in GEMATRIA.items()}
INDEX_TO_LATIN = {v[0]: v[1] for k, v in GEMATRIA.items()}

# Latin to Index
LATIN_TO_INDEX = {}
for k, v in GEMATRIA.items():
    latin = v[1]
    idx = v[0]
    if latin not in LATIN_TO_INDEX:
        LATIN_TO_INDEX[latin] = idx
    if len(latin) == 1:
        LATIN_TO_INDEX[latin] = idx
LATIN_TO_INDEX['K'] = LATIN_TO_INDEX['C']

def text_to_key(text):
    """Convert text to list of indices (key values)."""
    text = text.upper().replace(' ', '')
    result = []
    i = 0
    while i < len(text):
        # Try digraphs first (TH, NG, OE, EO, AE, IA, EA)
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_INDEX:
                result.append(LATIN_TO_INDEX[digraph])
                i += 2
                continue
        # Single character
        if text[i] in LATIN_TO_INDEX:
            result.append(LATIN_TO_INDEX[text[i]])
        i += 1
    return result

def runes_to_indices(rune_text):
    """Convert rune string to list of indices."""
    indices = []
    for char in rune_text:
        if char in RUNE_TO_INDEX:
            indices.append(RUNE_TO_INDEX[char])
    return indices

def indices_to_latin(indices):
    """Convert indices to Latin text."""
    return ''.join(INDEX_TO_LATIN.get(i, '?') for i in indices)

def vigenere_decrypt(cipher, key, mode='SUB'):
    """Vigenère decrypt with different modes."""
    if not key:
        return cipher
    result = []
    key_len = len(key)
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        if mode == 'SUB':
            result.append((c - k) % ALPHABET_SIZE)
        elif mode == 'ADD':
            result.append((c + k) % ALPHABET_SIZE)
        elif mode == 'SUB_REV':
            result.append((k - c) % ALPHABET_SIZE)
    return result

def calculate_ioc(indices):
    """Calculate Index of Coincidence."""
    if len(indices) < 2:
        return 0.0
    freq = [0] * ALPHABET_SIZE
    for idx in indices:
        freq[idx] += 1
    n = len(indices)
    ioc = sum(f * (f - 1) for f in freq) / (n * (n - 1))
    return ioc

# Common English trigrams
TRIGRAMS = {
    'THE': 100, 'AND': 80, 'ING': 75, 'HER': 65, 'HAT': 60,
    'HIS': 55, 'THA': 50, 'ERE': 48, 'FOR': 45, 'ENT': 43,
    'ION': 42, 'TER': 40, 'WAS': 38, 'YOU': 37, 'ITH': 36,
    'VER': 35, 'ALL': 34, 'WIT': 33, 'THI': 32, 'TIO': 31
}

COMMON_WORDS = [
    'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'YOU',
    'THIS', 'BUT', 'HIS', 'FROM', 'THEY', 'SAY', 'HER', 'SHE',
    'WILL', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
    'PRIMES', 'SACRED', 'WISDOM', 'TRUTH', 'DIVINITY', 'CIRCUMFERENCE',
    'CONSUMPTION', 'BELIEF', 'KNOWLEDGE', 'ENLIGHTENMENT'
]

def score_text(text):
    """Score decrypted text."""
    score = 0
    # Trigram scoring
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in TRIGRAMS:
            score += TRIGRAMS[trigram]
    
    # Word matching
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    
    return score

def load_page(page_num):
    """Load runes from a page."""
    page_dir = Path(__file__).parent.parent / 'pages' / f'page_{page_num:02d}'
    runes_file = page_dir / 'runes.txt'
    if runes_file.exists():
        with open(runes_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# KEYS FROM PAGE 63
MYSTERIOUS_TERMS = [
    'MOBIUS',
    'SUOID',
    'ANALOGUOID',
    'CABAL',
    'AETHEREAL',
    'CARNAL',
    'OBSCURA',
    'SHADOWS',
    'BUFFER',
    'MOBIUSANALOGUID',  # Combined
    'AETHEREALCABAL',
    'SUOIDCARNAL',
    'OBSCURAFORM',
    'SHADOWSAETHEREAL',
    # Reversed versions
    'SUIBOM',  # MOBIUS reversed
    'DIUOS',   # SUOID reversed
    # Anagrams of SUOID
    'DUIOS',
    'DIOUS',
    'IOUDS',
    'ODIUS',
    # Numbers as text (prime indices)
    'DIVINITY',  # Known key
    'CONSUMPTION',  # From page 68
    'CIRCUMFERENCE',
]

# Numbers from page 63
PAGE_63_NUMBERS = [272138, 131151, 226, 245, 18, 151131, 138272, 4768, 464]

def main():
    print("=" * 70)
    print("PAGE 63 MYSTERIOUS TERMS AS KEYS ATTACK")
    print("=" * 70)
    
    # Unsolved pages (18-54 are the hardest ones)
    test_pages = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    results = []
    
    for page_num in test_pages:
        rune_text = load_page(page_num)
        if not rune_text:
            continue
        
        cipher = runes_to_indices(rune_text)
        if len(cipher) < 50:
            continue
        
        print(f"\n--- PAGE {page_num} ({len(cipher)} runes) ---")
        
        best_score = 0
        best_result = None
        
        for term in MYSTERIOUS_TERMS:
            key = text_to_key(term)
            if not key:
                continue
            
            for mode in ['SUB', 'ADD', 'SUB_REV']:
                plaintext = vigenere_decrypt(cipher, key, mode)
                text = indices_to_latin(plaintext)
                score = score_text(text)
                ioc = calculate_ioc(plaintext)
                
                if score > best_score or ioc > 0.06:
                    best_score = score
                    best_result = (term, mode, score, ioc, text[:100])
                
                if score > 500 or ioc > 0.06:
                    print(f"  {term:20} {mode:8} Score={score:5} IoC={ioc:.4f}")
                    print(f"    {text[:80]}...")
        
        if best_result:
            results.append((page_num, best_result))
    
    # Also try numbers as key indices
    print("\n" + "=" * 70)
    print("TRYING PAGE 63 NUMBERS AS PRIME START INDICES")
    print("=" * 70)
    
    # Generate primes
    def sieve(n):
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n**0.5) + 1):
            if is_prime[i]:
                for j in range(i*i, n + 1, i):
                    is_prime[j] = False
        return [i for i, p in enumerate(is_prime) if p]
    
    primes = sieve(300000)  # Need enough primes for large indices
    
    for page_num in [18, 19, 20, 25, 32, 50]:  # Focus on key pages
        rune_text = load_page(page_num)
        if not rune_text:
            continue
        
        cipher = runes_to_indices(rune_text)
        if len(cipher) < 50:
            continue
        
        print(f"\n--- PAGE {page_num} (Numbers as Prime Indices) ---")
        
        for num in PAGE_63_NUMBERS:
            if num >= len(primes):
                continue
            
            # Use number as prime index, create key from consecutive primes
            for key_len in [7, 11, 13, 17, 23, 29, 31]:  # Prime key lengths
                if num + key_len > len(primes):
                    continue
                
                key = [primes[num + i] % ALPHABET_SIZE for i in range(key_len)]
                
                for mode in ['SUB', 'ADD']:
                    plaintext = vigenere_decrypt(cipher, key, mode)
                    text = indices_to_latin(plaintext)
                    score = score_text(text)
                    ioc = calculate_ioc(plaintext)
                    
                    if score > 500 or ioc > 0.055:
                        print(f"  NumIdx={num:6} L={key_len:2} {mode:4} Score={score:4} IoC={ioc:.4f}")
                        print(f"    {text[:80]}...")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF BEST RESULTS")
    print("=" * 70)
    if results:
        for page_num, (term, mode, score, ioc, text) in sorted(results, key=lambda x: -x[1][2]):
            print(f"Page {page_num}: {term} {mode} Score={score} IoC={ioc:.4f}")
    else:
        print("No significant results found.")

if __name__ == '__main__':
    main()

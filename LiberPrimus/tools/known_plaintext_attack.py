#!/usr/bin/env python3
"""
Known Plaintext Attack - Using common opening phrases

If the unsolved pages follow similar patterns to solved ones, they might start with:
- "WELCOME PILGRIM..."
- "AN INSTRUCTION..."
- "KNOW THIS..."
- "THE PRIMES ARE SACRED..."
- etc.

We'll try assuming various starting phrases and extract the required key.
"""

import os
import re
from collections import Counter

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                   'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
                   'A', 'AE', 'Y', 'IA', 'EA']

LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6,
    'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20,
    'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26,
    'IA': 27, 'IO': 27, 'EA': 28, 'V': 1, 'Q': 5, 'Z': 15
}

def text_to_indices(text):
    """Convert English text to Gematria Primus indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        if text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
        i += 1
    return indices

def runes_to_indices(runes):
    return [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

def read_page_runes(page_num):
    """Read all runes from a page as a flat list"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return runes_to_indices(content)

def read_page_words(page_num):
    """Read page as list of word rune sequences"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    words = re.split(r'[-\n]+', content)
    return [[RUNE_TO_INDEX[r] for r in w if r in RUNE_TO_INDEX] for w in words if any(r in RUNE_TO_INDEX for r in w)]

def derive_key(cipher_indices, plain_indices, operation='sub'):
    """
    Derive key from known plaintext
    If cipher = (plain + key) mod 29, then key = (cipher - plain) mod 29
    If cipher = (plain - key) mod 29, then key = (plain - cipher) mod 29
    """
    key = []
    for c, p in zip(cipher_indices, plain_indices):
        if operation == 'add':  # cipher = (plain + key) mod 29
            k = (c - p) % 29
        else:  # cipher = (plain - key) mod 29
            k = (p - c) % 29
        key.append(k)
    return key

def apply_key(cipher_indices, key, operation='sub'):
    """Apply key to decrypt"""
    decrypted = []
    for i, c in enumerate(cipher_indices):
        k = key[i % len(key)]
        if operation == 'add':
            d = (c - k) % 29
        else:
            d = (c + k) % 29
        decrypted.append(d)
    return decrypted

def find_key_period(key, max_period=50):
    """Check if key has a repeating pattern"""
    for period in range(1, min(len(key), max_period) + 1):
        is_periodic = True
        for i in range(len(key)):
            if key[i] != key[i % period]:
                is_periodic = False
                break
        if is_periodic:
            return period, key[:period]
    return len(key), key

def test_plaintext_hypothesis(page_num, hypothetical_start, operation='add'):
    """
    Test if a hypothetical starting plaintext produces a sensible key
    """
    cipher = read_page_runes(page_num)
    plain = text_to_indices(hypothetical_start)
    
    # Derive the key for the first N characters
    key = derive_key(cipher[:len(plain)], plain, operation)
    
    # Check for periodicity
    period, pattern = find_key_period(key)
    
    # Apply this pattern as a repeating key
    decrypted = apply_key(cipher, pattern, operation)
    decrypted_text = indices_to_text(decrypted)
    
    return {
        'hypothesis': hypothetical_start,
        'key_derived': key,
        'period': period,
        'pattern': pattern,
        'pattern_letters': indices_to_text(pattern),
        'decrypted': decrypted_text[:200]
    }

def main():
    print("=" * 70)
    print("KNOWN PLAINTEXT ATTACK - Testing Opening Phrase Hypotheses")
    print("=" * 70)
    
    # Possible opening phrases based on solved pages and Cicada themes
    hypotheses = [
        "WELCOME PILGRIM TO THE GREAT JOURNEY",
        "WELCOME SEEKER OF TRUTH",
        "KNOW THIS THE PRIMES ARE SACRED",
        "AN INSTRUCTION COMMAND YOUR OWN SELF",
        "THE TRUTH IS WITHIN YOU",
        "BEHOLD THE SACRED PRIMES",
        "SEEK AND YOU SHALL FIND",
        "THE PATH TO WISDOM",
        "VERILY I SAY UNTO YOU",
        "THE CIRCUMFERENCE OF THE SOUL",
        "LIKE THE INSTAR TUNNELING",
        "IN THE BEGINNING WAS THE WORD",
        "THERE IS A TRUTH TO BE FOUND",
        "THE DIVINE WITHIN",
        "CONSUME MY KNOWLEDGE",
        "THE SACRED GEOMETRY",
        "WISDOM IS THE PRINCIPAL THING",
        "UNDERSTANDING IS THE KEY",
    ]
    
    for page_num in [0, 2]:
        print(f"\n{'='*70}")
        print(f"PAGE {page_num}")
        print(f"{'='*70}")
        
        cipher = read_page_runes(page_num)
        words = read_page_words(page_num)
        
        # Show word structure
        word_lengths = [len(w) for w in words[:15]]
        print(f"First 15 word lengths: {word_lengths}")
        
        for hyp in hypotheses[:10]:  # Test first 10
            for op in ['add', 'sub']:
                result = test_plaintext_hypothesis(page_num, hyp, op)
                
                # Check if decrypted text looks promising
                dec = result['decrypted'].upper()
                
                # Score: count common patterns
                score = 0
                for pattern in ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'A ']:
                    score += dec.count(pattern)
                
                if score >= 3 or result['period'] <= 10:
                    print(f"\n  Hypothesis: '{hyp}' ({op})")
                    print(f"  Key pattern: {result['pattern_letters']} (period={result['period']})")
                    print(f"  Score: {score}")
                    print(f"  Decrypted: {result['decrypted'][:100]}...")

if __name__ == '__main__':
    main()

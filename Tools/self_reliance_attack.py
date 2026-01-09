#!/usr/bin/env python3
"""
Self-Reliance Running Key Attack
Using Emerson's Self-Reliance as a running key for Liber Primus pages 18-54

The MASTER_SOLVING_DOC notes: "Self-Reliance Connection - Emerson's essay is 
referenced in solved pages ('shed our circumferences') - may be running key source"
"""

import os
import re
from collections import Counter

# Gematria Primus mapping
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_RUNE = {v: k for k, v in RUNE_TO_INDEX.items()}

# Runeglish letter to index
LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18,
    'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

INDEX_TO_LETTER = {v: k for k, v in LETTER_TO_INDEX.items()}

# Common English words for scoring
COMMON_WORDS = {'THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'AS', 'WITH', 'WAS', 
                'HIS', 'BE', 'AT', 'BY', 'THIS', 'HAD', 'NOT', 'ARE', 'BUT', 'FROM',
                'OR', 'HAVE', 'AN', 'THEY', 'WHICH', 'ONE', 'YOU', 'WERE', 'HER', 'ALL',
                'SHE', 'THERE', 'WOULD', 'THEIR', 'WE', 'HIM', 'BEEN', 'HAS', 'WHEN',
                'WHO', 'WILL', 'NO', 'MORE', 'IF', 'OUT', 'SO', 'SAID', 'WHAT', 'UP',
                'DIVINITY', 'WITHIN', 'PRIMES', 'SACRED', 'PILGRIM', 'WISDOM', 'TRUTH',
                'CIRCUMFERENCE', 'EMERGE', 'INSTAR', 'CONSUMPTION', 'PRESERVATION'}

def load_runes(page_num):
    """Load runes from a page's runes.txt file"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_file = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if not os.path.exists(rune_file):
        return None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract only rune characters
    runes = [c for c in content if c in RUNE_TO_INDEX]
    return runes

def load_self_reliance():
    """Load and process Self-Reliance text as key"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sr_file = os.path.join(base_path, 'reference', 'research', 'Self-Reliance.txt')
    
    with open(sr_file, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    
    # Convert to runeglish indices
    # Handle digraphs first
    key_indices = []
    i = 0
    while i < len(text):
        # Check for digraphs
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph == 'TH':
                key_indices.append(LETTER_TO_INDEX['TH'])
                i += 2
                continue
            elif digraph == 'NG':
                key_indices.append(LETTER_TO_INDEX['NG'])
                i += 2
                continue
            elif digraph == 'EA':
                key_indices.append(LETTER_TO_INDEX['EA'])
                i += 2
                continue
            elif digraph == 'EO':
                key_indices.append(LETTER_TO_INDEX['EO'])
                i += 2
                continue
            elif digraph == 'OE':
                key_indices.append(LETTER_TO_INDEX['OE'])
                i += 2
                continue
            elif digraph == 'AE':
                key_indices.append(LETTER_TO_INDEX['AE'])
                i += 2
                continue
            elif digraph == 'IA':
                key_indices.append(LETTER_TO_INDEX['IA'])
                i += 2
                continue
        
        # Single letters
        c = text[i]
        if c in LETTER_TO_INDEX:
            key_indices.append(LETTER_TO_INDEX[c])
        elif c == 'K':
            key_indices.append(LETTER_TO_INDEX['C'])  # K -> C
        elif c == 'Q':
            key_indices.append(LETTER_TO_INDEX['C'])  # Q -> C
        elif c == 'V':
            key_indices.append(LETTER_TO_INDEX['U'])  # V -> U
        elif c == 'Z':
            key_indices.append(LETTER_TO_INDEX['S'])  # Z -> S
        i += 1
    
    return key_indices

def decrypt(cipher_runes, key_indices, offset=0, mode='SUB'):
    """Decrypt using running key cipher"""
    plaintext = []
    
    for i, rune in enumerate(cipher_runes):
        key_pos = (offset + i) % len(key_indices)
        key_val = key_indices[key_pos]
        cipher_val = RUNE_TO_INDEX[rune]
        
        if mode == 'SUB':
            plain_val = (cipher_val - key_val) % 29
        elif mode == 'ADD':
            plain_val = (cipher_val + key_val) % 29
        else:  # XOR
            plain_val = cipher_val ^ key_val
            if plain_val >= 29:
                plain_val = plain_val % 29
        
        plaintext.append(INDEX_TO_LETTER[plain_val])
    
    return ''.join(plaintext)

def score_text(text):
    """Score plaintext by common word matches"""
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def calculate_ioc(text):
    """Calculate Index of Coincidence for runeglish text"""
    # Convert to indices for counting
    counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    
    ioc = sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))
    return ioc

def main():
    print("=" * 70)
    print("SELF-RELIANCE RUNNING KEY ATTACK")
    print("=" * 70)
    
    # Load Self-Reliance key
    key_indices = load_self_reliance()
    print(f"Loaded Self-Reliance: {len(key_indices)} key characters")
    print(f"First 20 key indices: {key_indices[:20]}")
    
    # Test on multiple pages
    best_results = []
    
    for page_num in range(18, 55):
        runes = load_runes(page_num)
        if not runes:
            continue
        
        # Test various offsets
        page_best = None
        
        # Test starting offsets every 100 characters
        for offset in range(0, min(len(key_indices), 20000), 100):
            for mode in ['SUB', 'ADD']:
                plaintext = decrypt(runes, key_indices, offset, mode)
                score = score_text(plaintext)
                
                if score > 0 and (page_best is None or score > page_best[1]):
                    page_best = (offset, score, mode, plaintext[:100])
        
        if page_best and page_best[1] > 30:
            best_results.append((page_num, page_best))
            print(f"\nPage {page_num}: Score={page_best[1]}, Offset={page_best[0]}, Mode={page_best[2]}")
            print(f"  Preview: {page_best[3]}")
    
    # Also try specific significant offsets
    print("\n" + "=" * 70)
    print("TESTING SPECIFIC OFFSETS (Significant phrases in Self-Reliance)")
    print("=" * 70)
    
    # Key phrases and their approximate positions
    key_phrases = [
        (0, "Start of text"),
        (100, "Early essay"),
        (500, "Trust thyself section"),
        (1000, "Every heart vibrates"),
        (2000, "Mid-essay"),
        (3000, "Later section"),
        (5000, "Near end"),
        (7000, "Final thoughts"),
    ]
    
    # Focus on page 18 with detailed testing
    runes = load_runes(18)
    if runes:
        print(f"\nDetailed analysis of Page 18 ({len(runes)} runes):")
        
        for offset, desc in key_phrases:
            if offset < len(key_indices):
                for mode in ['SUB', 'ADD']:
                    plaintext = decrypt(runes, key_indices, offset, mode)
                    score = score_text(plaintext)
                    ioc = calculate_ioc(plaintext)
                    print(f"  Offset {offset} ({desc}) - {mode}: Score={score}, IoC={ioc:.4f}")
                    print(f"    Preview: {plaintext[:80]}")
    
    # Try extracting only letters at prime positions in Self-Reliance
    print("\n" + "=" * 70)
    print("PRIME-INDEXED KEY EXTRACTION FROM SELF-RELIANCE")
    print("=" * 70)
    
    def sieve_primes(n):
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n**0.5) + 1):
            if is_prime[i]:
                for j in range(i*i, n + 1, i):
                    is_prime[j] = False
        return [i for i in range(n + 1) if is_prime[i]]
    
    primes = sieve_primes(len(key_indices))
    prime_key = [key_indices[p] for p in primes if p < len(key_indices)]
    print(f"Extracted {len(prime_key)} characters at prime positions")
    
    if runes:
        for mode in ['SUB', 'ADD']:
            plaintext = decrypt(runes, prime_key, 0, mode)
            score = score_text(plaintext)
            ioc = calculate_ioc(plaintext)
            print(f"  {mode} mode: Score={score}, IoC={ioc:.4f}")
            print(f"    Preview: {plaintext[:80]}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if best_results:
        print("\nBest results found:")
        for page, result in sorted(best_results, key=lambda x: -x[1][1])[:10]:
            print(f"  Page {page}: Score={result[1]}, Offset={result[0]}, Mode={result[2]}")
    else:
        print("\nNo significant results found with Self-Reliance as key.")

if __name__ == '__main__':
    main()

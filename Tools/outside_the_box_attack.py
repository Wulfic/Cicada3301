#!/usr/bin/env python3
"""
OUTSIDE THE BOX ATTACK
======================

Using insights from solved pages to crack unsolved ones.

Key Insights:
1. IoC analysis shows unsolved pages have PRIME key lengths
2. Page 56 references Self-Reliance: "shed our circumferences"
3. Page 05 hints: "PRIMES ARE SACRED, TOTIENT FUNCTION IS SACRED"
4. Page 55+ uses φ(prime) shift cipher
5. Word boundaries (hyphens) are preserved

Attack Strategies:
A. Running Key with Self-Reliance text
B. φ(prime) based keys like page 55
C. Autokey cipher (plaintext extends key)
D. Page-number-based key modifications
E. Known plaintext from thematic content

Author: Wulfic
"""

import sys
from pathlib import Path
from collections import Counter
import math

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
GEMATRIA['ᛄ'] = (11, 'J', 37)

RUNE_TO_IDX = {k: v[0] for k, v in GEMATRIA.items()}
IDX_TO_LATIN = {v[0]: v[1] for k, v in GEMATRIA.items()}
IDX_TO_PRIME = {v[0]: v[2] for k, v in GEMATRIA.items()}

LATIN_TO_IDX = {}
for k, v in GEMATRIA.items():
    latin = v[1]
    idx = v[0]
    if len(latin) == 1:
        LATIN_TO_IDX[latin] = idx
    else:
        LATIN_TO_IDX[latin] = idx
        LATIN_TO_IDX[latin[0]] = idx
LATIN_TO_IDX['K'] = LATIN_TO_IDX['C']
LATIN_TO_IDX['V'] = LATIN_TO_IDX['U']
LATIN_TO_IDX['Q'] = LATIN_TO_IDX['C']
LATIN_TO_IDX['Z'] = LATIN_TO_IDX['S']

MOD = 29

# First 200 primes
def sieve(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(limit + 1) if sieve[i]]

PRIMES = sieve(3000)

def phi(p):
    """Euler's totient - for primes, φ(p) = p-1"""
    return p - 1

def load_page(page_num):
    """Load runes from page file"""
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    rune_file = page_dir / "runes.txt"
    if not rune_file.exists():
        return None
    with open(rune_file, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_key(text):
    """Convert text to key indices"""
    key = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_IDX:
                key.append(LATIN_TO_IDX[digraph])
                i += 2
                continue
        if text[i] in LATIN_TO_IDX:
            key.append(LATIN_TO_IDX[text[i]])
        i += 1
    return key

def indices_to_latin(indices):
    """Convert indices to Latin text"""
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def decrypt_vigenere(cipher_indices, key, mode='SUB'):
    """Decrypt using Vigenère-like cipher"""
    result = []
    key_len = len(key)
    for i, c in enumerate(cipher_indices):
        k = key[i % key_len]
        if mode == 'SUB':
            p = (c - k) % MOD
        elif mode == 'ADD':
            p = (c + k) % MOD
        elif mode == 'SUB_REV':
            p = (k - c) % MOD
        else:
            p = (c - k) % MOD
        result.append(p)
    return result

def decrypt_phi_prime(cipher_indices, offset=0):
    """Decrypt using φ(prime) shift like page 55"""
    result = []
    prime_idx = 0
    for c in cipher_indices:
        key_val = (phi(PRIMES[prime_idx]) + offset) % MOD
        p = (c - key_val) % MOD
        result.append(p)
        prime_idx += 1
    return result

def decrypt_prime_direct(cipher_indices, offset=0):
    """Decrypt using prime values directly"""
    result = []
    for i, c in enumerate(cipher_indices):
        key_val = (PRIMES[i] + offset) % MOD
        p = (c - key_val) % MOD
        result.append(p)
    return result

def decrypt_autokey(cipher_indices, seed_key, mode='SUB'):
    """Autokey cipher - plaintext extends key"""
    result = []
    key = list(seed_key)  # Start with seed
    
    for i, c in enumerate(cipher_indices):
        if i < len(seed_key):
            k = seed_key[i]
        else:
            k = result[i - len(seed_key)]
        
        if mode == 'SUB':
            p = (c - k) % MOD
        else:
            p = (c + k) % MOD
        result.append(p)
    
    return result

def score_english(text):
    """Score text for English-likeness"""
    # Common English bigrams
    BIGRAMS = {
        'TH': 15, 'HE': 12, 'IN': 11, 'ER': 10, 'AN': 10, 'RE': 9, 'ON': 9,
        'AT': 8, 'EN': 8, 'ND': 8, 'TI': 8, 'ES': 8, 'OR': 8, 'TE': 7,
        'OF': 7, 'ED': 7, 'IS': 7, 'IT': 7, 'AL': 7, 'AR': 7, 'ST': 7,
        'TO': 7, 'NT': 7, 'NG': 6, 'SE': 6, 'HA': 6, 'AS': 6, 'OU': 6,
    }
    
    COMMON_WORDS = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                    'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS'}
    
    score = 0
    text = text.upper().replace('-', ' ').replace('.', ' ')
    
    # Bigram score
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        if bg in BIGRAMS:
            score += BIGRAMS[bg]
    
    # Word score
    words = text.split()
    for word in words:
        if word in COMMON_WORDS:
            score += 50
        if len(word) == 3:  # Common word length
            score += 2
    
    return score

def analyze_word_structure(rune_text):
    """Analyze word lengths from hyphen-separated text"""
    words = []
    current = []
    for c in rune_text:
        if c == '-':
            if current:
                words.append(len(current))
                current = []
        elif c == '.':
            if current:
                words.append(len(current))
                current = []
        elif c in RUNE_TO_IDX:
            current.append(c)
    if current:
        words.append(len(current))
    return words

def main():
    print("=" * 80)
    print("OUTSIDE THE BOX ATTACK - Liber Primus")
    print("=" * 80)
    
    # Test pages
    test_pages = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    # Keys derived from solved pages and thematic content
    THEMATIC_KEYS = {
        'DIVINITY': text_to_key('DIVINITY'),
        'CIRCUMFERENCE': text_to_key('CIRCUMFERENCE'),
        'CIRCUMFERENCES': text_to_key('CIRCUMFERENCES'),
        'SELFRELIANCE': text_to_key('SELFRELIANCE'),
        'INSTAR': text_to_key('INSTAR'),
        'CONSUMPTION': text_to_key('CONSUMPTION'),
        'ENLIGHTENMENT': text_to_key('ENLIGHTENMENT'),
        'EMERGENCE': text_to_key('EMERGENCE'),
        'PILGRIM': text_to_key('PILGRIM'),
        'JOURNEY': text_to_key('JOURNEY'),
        'SACRED': text_to_key('SACRED'),
        'PRIMES': text_to_key('PRIMES'),
        'TOTIENT': text_to_key('TOTIENT'),
        'YAHEOOPYJ': text_to_key('YAHEOOPYJ'),  # From page 17
        'FIRFUMFERENFE': text_to_key('FIRFUMFERENFE'),  # From pages 14-15
        'KOAN': text_to_key('KOAN'),
        'PARABLE': text_to_key('PARABLE'),
        'EMERSON': text_to_key('EMERSON'),
        'DEEPWEB': text_to_key('DEEPWEB'),
        'ANEND': text_to_key('ANEND'),
        'CICADA': text_to_key('CICADA'),
    }
    
    for page_num in test_pages:
        print(f"\n{'='*80}")
        print(f"PAGE {page_num}")
        print(f"{'='*80}")
        
        rune_text = load_page(page_num)
        if not rune_text:
            print(f"  Could not load page {page_num}")
            continue
        
        # Extract cipher indices
        cipher = [RUNE_TO_IDX[c] for c in rune_text if c in RUNE_TO_IDX]
        print(f"  Rune count: {len(cipher)}")
        
        # Analyze word structure
        word_lens = analyze_word_structure(rune_text)
        print(f"  Word count: {len(word_lens)}")
        print(f"  Word lengths: {word_lens[:20]}...")
        
        # Look for common patterns (3-letter words = THE, AND, FOR, etc.)
        three_letter_count = sum(1 for w in word_lens if w == 3)
        print(f"  3-letter words: {three_letter_count}")
        
        best_results = []
        
        # Strategy 1: φ(prime) shift with page-number offset
        print(f"\n  --- Strategy 1: φ(prime) + page offset ---")
        for offset in range(-30, 30):
            result = decrypt_phi_prime(cipher, offset)
            text = indices_to_latin(result)
            score = score_english(text)
            if score > 100:
                best_results.append(('PHI_PRIME', f'offset={offset}', score, text[:80]))
        
        # Strategy 2: Thematic keys with different modes
        print(f"  --- Strategy 2: Thematic keys ---")
        for key_name, key in THEMATIC_KEYS.items():
            for mode in ['SUB', 'ADD', 'SUB_REV']:
                result = decrypt_vigenere(cipher, key, mode)
                text = indices_to_latin(result)
                score = score_english(text)
                if score > 100:
                    best_results.append((f'VIGENERE_{mode}', key_name, score, text[:80]))
                
                # Also try with page number offset
                key_shifted = [(k + page_num) % MOD for k in key]
                result = decrypt_vigenere(cipher, key_shifted, mode)
                text = indices_to_latin(result)
                score = score_english(text)
                if score > 100:
                    best_results.append((f'VIGENERE_{mode}+PG', key_name, score, text[:80]))
        
        # Strategy 3: Autokey with thematic seeds
        print(f"  --- Strategy 3: Autokey ---")
        for key_name, key in THEMATIC_KEYS.items():
            for mode in ['SUB', 'ADD']:
                result = decrypt_autokey(cipher, key, mode)
                text = indices_to_latin(result)
                score = score_english(text)
                if score > 100:
                    best_results.append((f'AUTOKEY_{mode}', key_name, score, text[:80]))
        
        # Strategy 4: Prime values as key (direct)
        print(f"  --- Strategy 4: Prime direct ---")
        for offset in range(-30, 30):
            result = decrypt_prime_direct(cipher, offset)
            text = indices_to_latin(result)
            score = score_english(text)
            if score > 100:
                best_results.append(('PRIME_DIRECT', f'offset={offset}', score, text[:80]))
        
        # Sort and display best results
        best_results.sort(key=lambda x: x[2], reverse=True)
        print(f"\n  TOP RESULTS:")
        for method, key_info, score, preview in best_results[:10]:
            print(f"    [{score:>6.1f}] {method:20s} | {key_info:20s}")
            print(f"            {preview}")
        
        if not best_results:
            print("    No promising results found")

if __name__ == '__main__':
    main()

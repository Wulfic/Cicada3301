#!/usr/bin/env python3
"""
Page 0 Analysis - Testing All Community-Proven Cipher Methods

Based on solved Onion pages and LP Pages 56-57, these ciphers work:
1. Atbash: decimal[i] = 28 - decimal[i]
2. Atbash + Shift: decimal[i] = (28 - decimal[i] + shift) % 29
3. Vigenère with meaningful keys (DIVINITY, CIRCUMFERENCE, etc.)
4. Prime shift: -(prime[i] + 57) mod 29
5. Direct translation (some pages are plaintext)

This script systematically tests all methods.
"""

import sys
from collections import Counter
from pathlib import Path

# Gematria Primus mapping
RUNE_TO_INDEX = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛂ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LETTER = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# First 300 primes for prime-based ciphers
def get_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

PRIMES = get_primes(300)

def load_runes(filepath):
    """Load runes from file and extract cipher indices"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    indices = []
    for char in text:
        if char in RUNE_TO_INDEX:
            indices.append(RUNE_TO_INDEX[char])
    return indices, text

def indices_to_text(indices):
    """Convert indices to Latin text"""
    return ''.join(INDEX_TO_LETTER.get(i, '?') for i in indices)

def score_english(text):
    """Score English-likeness using trigrams and common words"""
    text = text.upper()
    score = 0.0
    
    # Common trigrams
    trigrams = {'THE': 50, 'AND': 30, 'ING': 25, 'ION': 20, 'ENT': 20, 
                'FOR': 18, 'TIO': 18, 'ERE': 15, 'HER': 15, 'ATE': 12,
                'VER': 12, 'TER': 12, 'THA': 12, 'ATI': 10, 'HAT': 10,
                'ERS': 10, 'HIS': 10, 'RES': 8, 'ILL': 8, 'ARE': 8,
                'CON': 8, 'NCE': 8, 'ALL': 8, 'EVE': 8, 'ITH': 8}
    
    for tri, weight in trigrams.items():
        score += text.count(tri) * weight
    
    # Common Cicada words
    cicada_words = ['DIVINITY', 'WISDOM', 'TRUTH', 'WITHIN', 'PRIMES', 
                    'SACRED', 'CIRCUMFERENCE', 'INSTAR', 'EMERGE', 'PARABLE',
                    'WARNING', 'BELIEVE', 'NOTHING', 'INSTRUCTION', 'KOAN',
                    'MASTER', 'PILGRIM', 'JOURNEY', 'WELCOME', 'DEATH',
                    'CONSCIOUSNESS', 'SELF', 'BEING', 'LOSS']
    
    for word in cicada_words:
        if word in text:
            score += len(word) * 20
    
    # Common short words
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
                    'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HIS', 'HAS',
                    'WITH', 'THAT', 'THIS', 'FROM', 'THEY', 'HAVE', 'BEEN',
                    'WILL', 'YOUR', 'WHAT', 'WHEN', 'MAKE', 'LIKE', 'TIME',
                    'WHO', 'WE', 'IS', 'IT', 'TO', 'OF', 'IN', 'AS', 'BE']
    
    for word in common_words:
        # Check for word boundaries (rough approximation)
        score += text.count(word) * len(word) * 2
    
    return score

# ============================================================================
# CIPHER METHODS FROM SOLVED PAGES
# ============================================================================

def cipher_direct(indices):
    """Direct translation (no cipher)"""
    return indices

def cipher_atbash(indices):
    """Atbash: swap first with last, etc."""
    return [(28 - i) % 29 for i in indices]

def cipher_atbash_shift(indices, shift):
    """Atbash followed by constant shift"""
    return [(28 - i + shift) % 29 for i in indices]

def cipher_caesar(indices, shift):
    """Simple Caesar shift"""
    return [(i - shift) % 29 for i in indices]

def cipher_vigenere(indices, key_str):
    """Vigenère with a string key"""
    key = [RUNE_TO_INDEX.get(c, ord(c.upper()) - ord('A')) 
           if c in RUNE_TO_INDEX else 
           (ord(c.upper()) - ord('A')) % 29 
           for c in key_str if c.isalpha() or c in RUNE_TO_INDEX]
    
    if not key:
        return indices
    
    result = []
    for i, idx in enumerate(indices):
        k = key[i % len(key)]
        result.append((idx - k) % 29)
    return result

def cipher_prime_shift_57(indices):
    """Page 56 method: -(prime[i] + 57) mod 29"""
    result = []
    for i, idx in enumerate(indices):
        if i < len(PRIMES):
            shift = (PRIMES[i] + 57) % 29
            result.append((idx + shift) % 29)  # Reverse of -(prime+57)
        else:
            result.append(idx)
    return result

def cipher_prime_shift(indices, offset):
    """Generic prime shift with variable offset"""
    result = []
    for i, idx in enumerate(indices):
        if i < len(PRIMES):
            shift = (PRIMES[i] + offset) % 29
            result.append((idx + shift) % 29)
        else:
            result.append(idx)
    return result

def cipher_sub(indices, key):
    """SUB mod 29 with key array (our proven method)"""
    result = []
    for i, idx in enumerate(indices):
        k = key[i % len(key)]
        result.append((idx - k) % 29)
    return result

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def analyze_page(indices):
    """Test all community-proven cipher methods"""
    results = []
    
    # 1. Direct translation (is it plaintext?)
    text = indices_to_text(cipher_direct(indices))
    score = score_english(text)
    results.append(('Direct (plaintext)', score, text[:100]))
    
    # 2. Atbash only
    text = indices_to_text(cipher_atbash(indices))
    score = score_english(text)
    results.append(('Atbash', score, text[:100]))
    
    # 3. Atbash + shifts 1-28
    for shift in range(1, 29):
        text = indices_to_text(cipher_atbash_shift(indices, shift))
        score = score_english(text)
        results.append((f'Atbash+Shift({shift})', score, text[:100]))
    
    # 4. Caesar shifts 1-28
    for shift in range(1, 29):
        text = indices_to_text(cipher_caesar(indices, shift))
        score = score_english(text)
        results.append((f'Caesar({shift})', score, text[:100]))
    
    # 5. Vigenère with known keys
    known_keys = [
        'DIVINITY', 'CIRCUMFERENCE', 'INSTAR', 'PARABLE', 'WISDOM',
        'TRUTH', 'PRIMES', 'SACRED', 'PILGRIM', 'JOURNEY', 'LIBER',
        'PRIMUS', 'CICADA', 'EMERGENCE', 'WELCOME', 'WARNING',
        'FIRFUMFERENFE', 'KOAN', 'MASTER', 'DEATH', 'SELF'
    ]
    for key in known_keys:
        text = indices_to_text(cipher_vigenere(indices, key))
        score = score_english(text)
        results.append((f'Vigenère({key})', score, text[:100]))
    
    # 6. Prime shift with offset 57 (Page 56 method)
    text = indices_to_text(cipher_prime_shift_57(indices))
    score = score_english(text)
    results.append(('Prime+57 shift', score, text[:100]))
    
    # 7. Prime shift with other offsets
    for offset in [0, 1, 29, 56, 58]:
        text = indices_to_text(cipher_prime_shift(indices, offset))
        score = score_english(text)
        results.append((f'Prime+{offset} shift', score, text[:100]))
    
    return results

def main():
    # Load Page 0 runes
    rune_file = Path(__file__).parent.parent / 'runes.txt'
    
    if not rune_file.exists():
        print(f"Error: {rune_file} not found")
        return
    
    indices, raw_text = load_runes(rune_file)
    
    print(f"=" * 80)
    print("PAGE 0 ANALYSIS - Community-Proven Cipher Methods")
    print(f"=" * 80)
    print(f"Rune count: {len(indices)}")
    print(f"Raw text preview: {raw_text[:100]}...")
    print()
    
    # Run analysis
    results = analyze_page(indices)
    
    # Sort by score
    results.sort(key=lambda x: -x[1])
    
    # Print top 20 results
    print(f"\n{'=' * 80}")
    print("TOP 20 RESULTS (sorted by English-likeness score)")
    print(f"{'=' * 80}")
    
    for i, (method, score, preview) in enumerate(results[:20], 1):
        print(f"\n{i}. {method}")
        print(f"   Score: {score:.1f}")
        print(f"   Preview: {preview}")
    
    # Print best result in full
    best_method, best_score, _ = results[0]
    print(f"\n{'=' * 80}")
    print(f"BEST RESULT: {best_method} (Score: {best_score:.1f})")
    print(f"{'=' * 80}")
    
    # Regenerate full text for best method
    if 'Atbash+Shift' in best_method:
        shift = int(best_method.split('(')[1].rstrip(')'))
        full_text = indices_to_text(cipher_atbash_shift(indices, shift))
    elif 'Atbash' in best_method:
        full_text = indices_to_text(cipher_atbash(indices))
    elif 'Caesar' in best_method:
        shift = int(best_method.split('(')[1].rstrip(')'))
        full_text = indices_to_text(cipher_caesar(indices, shift))
    elif 'Vigenère' in best_method:
        key = best_method.split('(')[1].rstrip(')')
        full_text = indices_to_text(cipher_vigenere(indices, key))
    elif 'Prime+57' in best_method:
        full_text = indices_to_text(cipher_prime_shift_57(indices))
    elif 'Prime+' in best_method:
        offset = int(best_method.split('+')[1].split()[0])
        full_text = indices_to_text(cipher_prime_shift(indices, offset))
    else:
        full_text = indices_to_text(indices)
    
    print(full_text)
    
    # Save results
    output_file = Path(__file__).parent / 'PAGE0_COMMUNITY_METHODS_RESULTS.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"PAGE 0 ANALYSIS - Community-Proven Cipher Methods\n")
        f.write(f"=" * 80 + "\n")
        f.write(f"Rune count: {len(indices)}\n\n")
        
        f.write("ALL RESULTS (sorted by score):\n")
        f.write("-" * 80 + "\n")
        for method, score, preview in results:
            f.write(f"{method}: {score:.1f}\n")
            f.write(f"  {preview}\n\n")
        
        f.write(f"\n{'=' * 80}\n")
        f.write(f"BEST RESULT: {best_method}\n")
        f.write(f"{'=' * 80}\n")
        f.write(full_text + "\n")
    
    print(f"\nResults saved to: {output_file}")

if __name__ == '__main__':
    main()

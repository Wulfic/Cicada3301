#!/usr/bin/env python3
"""
Gematria Prime Value Analysis
Tests if the cipher uses Gematria PRIME VALUES instead of indices.

From RuneSolver.py:
F=2, U=3, TH=5, O=7, R=11, C=13, G=17, W=19, H=23, N=29, I=31, J=37,
EO=41, P=43, X=47, S=53, T=59, B=61, E=67, M=71, L=73, NG=79, OE=83,
D=89, A=97, AE=101, Y=103, IO=107, EA=109
"""

import os
import sys
from pathlib import Path

# Gematria Primus - PRIME values (from RuneSolver.py)
GEMATRIA_PRIMES = {
    'F': 2,   'U': 3,   'TH': 5,   'O': 7,   'R': 11,  'C': 13,  'G': 17,
    'W': 19,  'H': 23,  'N': 29,   'I': 31,  'J': 37,  'EO': 41, 'P': 43,
    'X': 47,  'S': 53,  'T': 59,   'B': 61,  'E': 67,  'M': 71,  'L': 73,
    'NG': 79, 'OE': 83, 'D': 89,   'A': 97,  'AE': 101,'Y': 103, 'IO': 107,
    'EA': 109
}

# Index to prime mapping
INDEX_TO_PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                  53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Prime to index mapping
PRIME_TO_INDEX = {p: i for i, p in enumerate(INDEX_TO_PRIME)}

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    indices = []
    for char in content:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    
    return indices

def indices_to_primes(indices):
    """Convert index list to prime value list."""
    return [INDEX_TO_PRIME[i] for i in indices]

def primes_to_indices(primes):
    """Convert prime values back to indices (mod operation needed)."""
    result = []
    for p in primes:
        # Find the closest prime in our set
        if p in PRIME_TO_INDEX:
            result.append(PRIME_TO_INDEX[p])
        else:
            # Use modular approach
            result.append(p % 29)
    return result

def indices_to_text(indices):
    """Convert indices to text."""
    result = []
    for i in indices:
        if 0 <= i < 29:
            result.append(LETTERS[i])
        else:
            result.append('?')
    return ''.join(result)

def score_text(text):
    """Score for English."""
    COMMON = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
              'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS',
              'HIS', 'HIM', 'HOW', 'TWO', 'WAY', 'WHO', 'ITS', 'SAY',
              'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM',
              'THOU', 'THEE', 'THINE', 'HATH', 'UNTO', 'PATH', 'SHED',
              'WITHIN', 'TRUTH', 'WISDOM', 'DIVINITY', 'EMERGE'}
    
    score = 0
    for word in COMMON:
        count = text.count(word)
        score += count * len(word) * 10
    
    return score

def test_prime_cipher(page_num):
    """Test various prime-based cipher methods."""
    print(f"\n{'='*70}")
    print(f"PRIME CIPHER ANALYSIS: Page {page_num}")
    print(f"{'='*70}")
    
    indices = load_runes(page_num)
    if not indices:
        print(f"Could not load page {page_num}")
        return
    
    primes = indices_to_primes(indices)
    
    print(f"Cipher indices: {indices[:20]}...")
    print(f"Cipher primes:  {primes[:20]}...")
    
    # Method 1: Subtract prime from prime, result mod largest prime (109)
    print("\nMethod 1: (cipher_prime - key_prime) mod 109")
    for key_prime in [2, 3, 5, 7, 11, 13]:
        result_primes = [(p - key_prime) % 109 for p in primes]
        # Map back to closest valid prime
        result_indices = []
        for rp in result_primes:
            if rp in PRIME_TO_INDEX:
                result_indices.append(PRIME_TO_INDEX[rp])
            else:
                # Find closest prime
                closest = min(INDEX_TO_PRIME, key=lambda x: abs(x - rp))
                result_indices.append(PRIME_TO_INDEX[closest])
        
        text = indices_to_text(result_indices)
        score = score_text(text)
        print(f"  Key prime {key_prime}: score={score}, text={text[:60]}")
    
    # Method 2: Use prime index, subtract mod 29 (like normal)
    print("\nMethod 2: Standard index subtraction")
    for key in range(0, 29, 5):
        result = [(i - key) % 29 for i in indices]
        text = indices_to_text(result)
        score = score_text(text)
        print(f"  Key {key}: score={score}, text={text[:60]}")
    
    # Method 3: Sum of prime values mod something
    print("\nMethod 3: Cumulative prime sum analysis")
    cumsum = 0
    cumulative = []
    for p in primes[:50]:
        cumsum += p
        cumulative.append(cumsum)
    
    print(f"  Cumulative prime sums: {cumulative[:15]}...")
    print(f"  Mod 29: {[c % 29 for c in cumulative[:15]]}")
    print(f"  Mod 109: {[c % 109 for c in cumulative[:15]]}")
    
    # Method 4: XOR-like operation with primes
    print("\nMethod 4: Prime XOR-like (p1 XOR p2 mod max_prime)")
    key_sequence = INDEX_TO_PRIME[:len(primes)]  # Use alphabet primes as key
    result = []
    for i, p in enumerate(primes):
        k = key_sequence[i % len(key_sequence)]
        xor_result = (p ^ k) % 109
        if xor_result in PRIME_TO_INDEX:
            result.append(PRIME_TO_INDEX[xor_result])
        else:
            closest = min(INDEX_TO_PRIME, key=lambda x: abs(x - xor_result))
            result.append(PRIME_TO_INDEX[closest])
    
    text = indices_to_text(result)
    score = score_text(text)
    print(f"  XOR with alphabet: score={score}, text={text[:80]}")
    
    # Method 5: Division/modular multiplicative inverse
    print("\nMethod 5: Multiplicative operations")
    for key_prime in [2, 3, 5, 7]:
        # p * key mod 109 then map back
        result = []
        for p in primes:
            mult_result = (p * key_prime) % 109
            if mult_result in PRIME_TO_INDEX:
                result.append(PRIME_TO_INDEX[mult_result])
            else:
                closest = min(INDEX_TO_PRIME, key=lambda x: abs(x - mult_result))
                result.append(PRIME_TO_INDEX[closest])
        
        text = indices_to_text(result)
        score = score_text(text)
        print(f"  p * {key_prime} mod 109: score={score}, text={text[:60]}")

def analyze_prime_patterns():
    """Analyze patterns in the Gematria prime sequence."""
    print("\n" + "="*70)
    print("GEMATRIA PRIME PATTERNS")
    print("="*70)
    
    primes = INDEX_TO_PRIME
    print(f"Primes: {primes}")
    
    # Gaps between consecutive primes
    gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
    print(f"Gaps:   {gaps}")
    
    # Prime factorization patterns
    print("\nPrime indices mod small primes:")
    for mod in [2, 3, 5, 7, 11]:
        mods = [p % mod for p in primes]
        print(f"  mod {mod}: {mods}")
    
    # Is there a pattern where cipher[i] - plain[i] relates to primes?
    print("\nExample: if 'THE' (T=59, H=23, E=67) encrypts to something...")
    print("  T (prime=59, idx=16)")
    print("  H (prime=23, idx=8)")
    print("  E (prime=67, idx=18)")
    
    # From earlier analysis, THE at position 42-43 has keys [10, 7] (I, W indices)
    # Cipher at positions 42-43 was [12, 25] (EO, AE indices = primes 41, 101)
    # Plaintext THE is [2, 18] (TH=5, E=67)
    
    print("\nFrom earlier: cipher [12,25] (primes 41,101) -> THE [2,18] (primes 5,67)")
    print(f"  41 - 5 = 36 (not a GP prime)")
    print(f"  101 - 67 = 34 (not a GP prime)")
    print(f"  But index: 12 - 2 = 10, 25 - 18 = 7")
    print("  Key indices [10, 7] = I, W")

def main():
    print("=" * 70)
    print("GEMATRIA PRIME VALUE CIPHER ANALYSIS")
    print("=" * 70)
    
    # Show the prime mapping
    print("\nGematria Primus prime values:")
    for i, (letter, prime) in enumerate(zip(LETTERS, INDEX_TO_PRIME)):
        print(f"  {i:2}: {letter:3} = {prime}")
    
    # Test on our pages
    for page in [8, 13, 46]:
        test_prime_cipher(page)
    
    # Analyze patterns
    analyze_prime_patterns()

if __name__ == "__main__":
    main()

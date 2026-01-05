#!/usr/bin/env python3
"""
Advanced Liber Primus Decryption Strategies
===========================================
Novel approaches based on cryptanalysis findings:
1. The IoC is ~1.0 (random) - standard ciphers don't work
2. This suggests: transposition, book cipher, or custom mathematical cipher
3. Try gematria-based, Fibonacci-based, and self-referential keys

Author: Cicada Solver
"""

import numpy as np
from collections import Counter
from pathlib import Path
import math
from itertools import permutations

# =============================================================================
# CONSTANTS
# =============================================================================

ALPHABET_SIZE = 29

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

# Gematria primes
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Fibonacci sequence
def fibonacci(n):
    fibs = [1, 1]
    for _ in range(n - 2):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

FIBONACCI = fibonacci(1000)

# =============================================================================
# UTILITIES
# =============================================================================

def load_liber_primus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_RUNE[int(i) % 29] for i in indices)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def english_score(text):
    """Score based on common patterns."""
    text_upper = text.upper()
    score = 0
    # Common digraphs
    for dg in ['TH', 'HE', 'IN', 'ER', 'AN', 'ND', 'ED', 'THE', 'ING', 'AND']:
        score += text_upper.count(dg) * len(dg)
    return score / max(1, len(text))

# =============================================================================
# NOVEL DECRYPTION APPROACHES
# =============================================================================

def gematria_self_shift(ciphertext):
    """
    Shift each rune by its OWN gematria value mod 29.
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        gem = GEMATRIA[idx]
        result[i] = (idx - gem) % 29
    return result

def gematria_cumulative_shift(ciphertext):
    """
    Running key based on cumulative gematria sum.
    """
    result = np.zeros_like(ciphertext)
    cumsum = 0
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - cumsum) % 29
        cumsum = (cumsum + GEMATRIA[idx]) % 29
    return result

def fibonacci_shift(ciphertext):
    """
    Shift by Fibonacci numbers instead of primes.
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - FIBONACCI[i]) % 29
    return result

def fibonacci_shift_with_offset(ciphertext, offset):
    """
    Shift by Fibonacci numbers with an offset (like Page 56's +57).
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - (FIBONACCI[i] + offset)) % 29
    return result

def totient_shift(ciphertext):
    """
    Shift by Euler's totient of primes.
    For prime p, φ(p) = p-1
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        totient = GEMATRIA[i % len(GEMATRIA)] - 1  # φ(p) = p-1 for prime
        result[i] = (idx - totient) % 29
    return result

def atbash_runes(ciphertext):
    """
    Atbash cipher: reverse the alphabet.
    F -> EA, U -> IA, etc.
    """
    return (28 - ciphertext) % 29

def interleave_decrypt(ciphertext, page57_indices):
    """
    Try using Page 57 (The Parable) as a repeating key.
    """
    key_len = len(page57_indices)
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - page57_indices[i % key_len]) % 29
    return result

def columnar_transposition_test(ciphertext, width):
    """
    Read text in columns of given width.
    """
    n = len(ciphertext)
    height = (n + width - 1) // width
    
    # Pad if needed
    padded = np.pad(ciphertext, (0, height * width - n), constant_values=0)
    
    # Reshape into grid and read by columns
    grid = padded.reshape(height, width)
    result = grid.T.flatten()[:n]
    return result

def rail_fence_decrypt(ciphertext, rails):
    """
    Rail fence cipher decryption.
    """
    n = len(ciphertext)
    
    # Calculate the pattern
    pattern = list(range(rails)) + list(range(rails-2, 0, -1))
    
    # Count characters per rail
    rail_counts = [0] * rails
    for i in range(n):
        rail_counts[pattern[i % len(pattern)]] += 1
    
    # Split ciphertext by rails
    rail_texts = []
    pos = 0
    for count in rail_counts:
        rail_texts.append(list(ciphertext[pos:pos+count]))
        pos += count
    
    # Read off in zigzag pattern
    result = []
    for i in range(n):
        rail = pattern[i % len(pattern)]
        if rail_texts[rail]:
            result.append(rail_texts[rail].pop(0))
    
    return np.array(result, dtype=np.int32)

def prime_sum_key(ciphertext):
    """
    Key is the sum of all previous gematria values.
    """
    result = np.zeros_like(ciphertext)
    total = 0
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - total) % 29
        total += GEMATRIA[idx]
    return result

def xor_with_position(ciphertext):
    """
    XOR (addition mod 29) with position index.
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - i) % 29
    return result

def reverse_text(ciphertext):
    """
    Simply reverse the text.
    """
    return ciphertext[::-1]

def skip_cipher(ciphertext, skip):
    """
    Read every nth character (skip cipher).
    """
    n = len(ciphertext)
    result = []
    for start in range(skip):
        for i in range(start, n, skip):
            result.append(ciphertext[i])
    return np.array(result, dtype=np.int32)

def twin_prime_shift(ciphertext):
    """
    Use twin primes as key (primes that differ by 2).
    Twin primes: (3,5), (5,7), (11,13), (17,19), (29,31)...
    """
    twin_primes = [3, 5, 5, 7, 11, 13, 17, 19, 29, 31, 41, 43, 59, 61, 71, 73]
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - twin_primes[i % len(twin_primes)]) % 29
    return result

def gematria_product_mod(ciphertext):
    """
    Running product of gematria values mod 29.
    """
    result = np.zeros_like(ciphertext)
    product = 1
    for i, idx in enumerate(ciphertext):
        result[i] = (idx - product) % 29
        product = (product * GEMATRIA[idx]) % 29
    return result

# =============================================================================
# PAGE 56 ANALYSIS - UNDERSTANDING THE SOLVED CIPHER
# =============================================================================

def analyze_page_56():
    """
    Page 56 was solved. Let's understand exactly what happened.
    """
    print("="*60)
    print("PAGE 56 ANALYSIS - Understanding the solved cipher")
    print("="*60)
    
    # Page 56 ciphertext (from RuneSolver.py)
    page56 = "ᚫᛂ•ᛟᛋᚱ:ᛗᚣᛚᚩᚻ•ᚩᚫ•ᚳᚦᚷᚹ•ᚹᛚᚫ,ᛉᚩᚪᛈ•ᛗᛞᛞᚢᚷᚹ•ᛚ•ᛞᚾᚣᛂ•ᚳᚠᛡ•ᚫᛏᛈᛇᚪᚦ•ᚳᚫ:ᚳᛞ•ᚠᚾ•ᛡᛖ•ᚠᚾᚳᛝ•ᚱᚠ•ᚫᛁᚱᛞᛖ•ᛋᚣᛂᛠᚢᛝᚹ•ᛉᚩ•ᛗᛠᚹᚠ•ᚱᚷᛡ•ᛝᚱᛒ•ᚫᚾᚢᛋ:"
    
    # Expected plaintext (from solving plan)
    # "AN OST: MYLOEH OA CTHGW WLA, XOAP MDDUGW L DNYJ CFI ATPEOTH CA:CD FN IE FNCNG RF AIRDE SYJEUNG XO MEWF RGI NRB ANUS:"
    # This decrypts to something about consumption
    
    print(f"\nPage 56 ciphertext sample:")
    print(page56[:100])
    
    cipher_idx = text_to_indices(page56)
    print(f"\nRune count: {len(cipher_idx)}")
    print(f"IoC: {compute_ioc_normalized(cipher_idx):.4f}")
    
    # Apply the known Page 56 cipher: -(prime_n + 57) mod 29
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    plaintext = np.zeros_like(cipher_idx)
    for i, idx in enumerate(cipher_idx):
        if i < len(primes):
            shift = (primes[i] + 57) % 29
        else:
            shift = (primes[i % len(primes)] + 57) % 29
        plaintext[i] = (idx - shift) % 29
    
    print(f"\nDecrypted with prime+57 method:")
    print(indices_to_english(plaintext[:50]))
    print(f"IoC after: {compute_ioc_normalized(plaintext):.4f}")

# =============================================================================
# MAIN TESTING
# =============================================================================

def test_all_approaches(ciphertext, name="Test"):
    """Test all novel decryption approaches."""
    
    print(f"\n{'='*70}")
    print(f"TESTING NOVEL APPROACHES: {name}")
    print(f"{'='*70}")
    print(f"Input length: {len(ciphertext)}")
    print(f"Input IoC: {compute_ioc_normalized(ciphertext):.4f}")
    
    approaches = [
        ("Gematria self-shift", lambda c: gematria_self_shift(c)),
        ("Gematria cumulative", lambda c: gematria_cumulative_shift(c)),
        ("Fibonacci shift", lambda c: fibonacci_shift(c)),
        ("Fibonacci +57", lambda c: fibonacci_shift_with_offset(c, 57)),
        ("Fibonacci +29", lambda c: fibonacci_shift_with_offset(c, 29)),
        ("Totient shift", lambda c: totient_shift(c)),
        ("Atbash", lambda c: atbash_runes(c)),
        ("Prime sum key", lambda c: prime_sum_key(c)),
        ("XOR position", lambda c: xor_with_position(c)),
        ("Reverse", lambda c: reverse_text(c)),
        ("Twin prime shift", lambda c: twin_prime_shift(c)),
        ("Gematria product mod", lambda c: gematria_product_mod(c)),
        ("Skip-2", lambda c: skip_cipher(c, 2)),
        ("Skip-3", lambda c: skip_cipher(c, 3)),
        ("Skip-5", lambda c: skip_cipher(c, 5)),
        ("Skip-7", lambda c: skip_cipher(c, 7)),
        ("Columnar-7", lambda c: columnar_transposition_test(c, 7)),
        ("Columnar-11", lambda c: columnar_transposition_test(c, 11)),
        ("Columnar-13", lambda c: columnar_transposition_test(c, 13)),
        ("Columnar-29", lambda c: columnar_transposition_test(c, 29)),
        ("Rail-3", lambda c: rail_fence_decrypt(c, 3)),
        ("Rail-5", lambda c: rail_fence_decrypt(c, 5)),
    ]
    
    results = []
    
    for name, func in approaches:
        try:
            result = func(ciphertext)
            ioc = compute_ioc_normalized(result)
            eng = indices_to_english(result[:40])
            eng_score = english_score(eng)
            
            results.append((name, ioc, eng_score, result))
            print(f"{name:25s}: IoC={ioc:.4f} | {eng}...")
        except Exception as e:
            print(f"{name:25s}: ERROR - {e}")
    
    # Sort by IoC
    results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n{'='*70}")
    print("TOP 5 BY IoC:")
    print(f"{'='*70}")
    for name, ioc, eng_score, result in results[:5]:
        eng = indices_to_english(result[:60])
        print(f"{name:25s}: IoC={ioc:.4f}")
        print(f"  {eng}")
    
    return results

def test_combined_ciphers(ciphertext):
    """
    Test combinations of ciphers - maybe Cicada used multiple layers.
    """
    print(f"\n{'='*70}")
    print("TESTING COMBINED CIPHER APPROACHES")
    print(f"{'='*70}")
    
    combinations = [
        ("Atbash + Prime shift", lambda c: gematria_cumulative_shift(atbash_runes(c))),
        ("Reverse + Gematria", lambda c: gematria_self_shift(reverse_text(c))),
        ("Fibonacci + Atbash", lambda c: atbash_runes(fibonacci_shift(c))),
        ("Skip-2 + Prime", lambda c: gematria_cumulative_shift(skip_cipher(c, 2))),
        ("Columnar + Fibonacci", lambda c: fibonacci_shift(columnar_transposition_test(c, 7))),
    ]
    
    for name, func in combinations:
        try:
            result = func(ciphertext)
            ioc = compute_ioc_normalized(result)
            eng = indices_to_english(result[:50])
            print(f"{name:30s}: IoC={ioc:.4f} | {eng}...")
        except Exception as e:
            print(f"{name:30s}: ERROR - {e}")

def look_for_patterns(text):
    """
    Look for structural patterns that might hint at the cipher.
    """
    print(f"\n{'='*70}")
    print("PATTERN ANALYSIS")
    print(f"{'='*70}")
    
    indices = text_to_indices(text)
    n = len(indices)
    
    # Look at distribution of differences between consecutive runes
    diffs = np.diff(indices)
    print("\nConsecutive rune differences (mod 29):")
    diff_counts = Counter((d % 29) for d in diffs)
    for diff, count in sorted(diff_counts.items())[:10]:
        print(f"  Diff {diff:2d}: {count:4d}")
    
    # Look for repeated patterns
    print("\nLooking for repeated substrings (potential cribs)...")
    rune_str = indices_to_text(indices)
    
    for length in [3, 4, 5]:
        patterns = {}
        for i in range(n - length):
            pattern = rune_str[i:i+length]
            if pattern not in patterns:
                patterns[pattern] = []
            patterns[pattern].append(i)
        
        # Filter to repeated patterns
        repeated = {p: pos for p, pos in patterns.items() if len(pos) > 1}
        if repeated:
            print(f"\n  {length}-rune repeated patterns: {len(repeated)}")
            for pattern, positions in list(repeated.items())[:5]:
                eng = indices_to_english(text_to_indices(pattern))
                print(f"    {pattern} ({eng}): at positions {positions[:5]}...")
    
    # Look at word boundaries
    words = text.split('•')
    word_lengths = [len(text_to_indices(w)) for w in words if any(c in RUNES for c in w)]
    print(f"\nWord length distribution:")
    for length, count in sorted(Counter(word_lengths).items()):
        print(f"  Length {length:2d}: {count:4d} words")

def main():
    print("="*70)
    print("ADVANCED LIBER PRIMUS DECRYPTION")
    print("="*70)
    
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    if not lp_path.exists():
        print(f"Error: Could not find {lp_path}")
        return
    
    lp_text = load_liber_primus(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    print(f"Loaded {len(lp_indices)} runes")
    
    # First understand Page 56
    analyze_page_56()
    
    # Test with first 500 runes
    sample = lp_indices[:500]
    
    # Test all novel approaches
    results = test_all_approaches(sample, "First 500 runes")
    
    # Test combined ciphers
    test_combined_ciphers(sample)
    
    # Look for patterns
    look_for_patterns(lp_text[:5000])
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

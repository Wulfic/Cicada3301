#!/usr/bin/env python3
"""
New approach: Maybe the encryption is NOT gematria-based at all.
The high IoC from gematria+ might be a mathematical artifact, not meaningful decryption.

Let's investigate:
1. Is the ciphertext a transposition of English?
2. Can we use known-plaintext attacks from solved pages?
3. Pattern analysis to identify cipher type
"""

import numpy as np
from collections import Counter
from pathlib import Path
import re

ALPHABET_SIZE = 29

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 89, 83, 89, 97, 101, 103, 107, 109]

def load_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def analyze_transposition_possibility(indices):
    """
    If the cipher is a transposition, frequency should match English.
    Check if frequency matches English letter frequencies.
    """
    print("\n" + "="*60)
    print("TRANSPOSITION CIPHER ANALYSIS")
    print("="*60)
    
    # English letter frequencies (approx, for 26 letters):
    english_freqs = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
                     'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3}
    
    n = len(indices)
    counts = Counter(indices)
    
    print("\nRune frequencies (sorted by count):")
    for idx, count in counts.most_common():
        letter = LETTERS[idx]
        pct = count / n * 100
        print(f"  {letter} ({idx}): {count} ({pct:.2f}%)")
    
    # Check if frequencies are flat (polyalphabetic) or peaked (simple sub/transposition)
    freqs = np.array([counts.get(i, 0) for i in range(29)])
    freq_std = np.std(freqs)
    freq_mean = np.mean(freqs)
    cv = freq_std / freq_mean  # Coefficient of variation
    
    print(f"\nFrequency stats:")
    print(f"  Mean: {freq_mean:.1f}")
    print(f"  Std Dev: {freq_std:.1f}")
    print(f"  CV (coefficient of variation): {cv:.4f}")
    print(f"\n  CV < 0.1 suggests flat distribution (polyalphabetic/random)")
    print(f"  CV > 0.3 suggests peaked distribution (simple substitution)")

def analyze_kappa_test_detailed(indices, max_period=50):
    """Detailed Kappa test to find periodicity."""
    print("\n" + "="*60)
    print("DETAILED KAPPA (IC) TEST FOR PERIODICITY")
    print("="*60)
    
    n = len(indices)
    
    # Calculate IC for different assumed periods
    results = []
    for period in range(1, max_period + 1):
        # Split into period-length columns
        total_ic = 0
        for col in range(period):
            column = indices[col::period]
            col_n = len(column)
            if col_n <= 1:
                continue
            counts = np.bincount(column, minlength=29)
            col_ic = np.sum(counts * (counts - 1)) / (col_n * (col_n - 1)) * 29
            total_ic += col_ic
        
        avg_ic = total_ic / period
        results.append((period, avg_ic))
    
    # Sort by IC and show top periods
    results.sort(key=lambda x: -x[1])
    
    print("\nTop 20 periods by average IC:")
    for period, ic in results[:20]:
        bar = '*' * int(ic * 10)
        print(f"  Period {period:2d}: IC={ic:.4f} {bar}")
    
    return results

def try_page56_method_variations(indices):
    """
    Page 56 used: -(prime_n + 57) mod 29
    Try variations of this formula.
    """
    print("\n" + "="*60)
    print("PAGE 56 METHOD VARIATIONS")
    print("="*60)
    
    # Original page 56: -(prime_n + 57) mod 29
    # Where prime_n = GEMATRIA[rune_index]
    
    best_ioc = 0
    best_offset = 0
    
    for offset in range(-150, 150):
        result = np.zeros_like(indices)
        for i, idx in enumerate(indices):
            prime_n = GEMATRIA[idx]
            result[i] = (-(prime_n + offset)) % 29
        
        ioc = compute_ioc_normalized(result)
        if ioc > best_ioc:
            best_ioc = ioc
            best_offset = offset
    
    print(f"\nBest offset: {best_offset}, IoC: {best_ioc:.4f}")
    
    # Apply best
    result = np.zeros_like(indices)
    for i, idx in enumerate(indices):
        prime_n = GEMATRIA[idx]
        result[i] = (-(prime_n + best_offset)) % 29
    
    text = ''.join(LETTERS[int(r)] for r in result[:100])
    print(f"  Sample: {text}")
    
    # Try positive version
    print("\nTrying positive variant: (prime_n + offset) mod 29")
    for offset in range(-150, 150):
        result = np.zeros_like(indices)
        for i, idx in enumerate(indices):
            prime_n = GEMATRIA[idx]
            result[i] = (prime_n + offset) % 29
        
        ioc = compute_ioc_normalized(result)
        if ioc > best_ioc:
            best_ioc = ioc
            best_offset = offset
            print(f"  Found better: offset={offset}, IoC={ioc:.4f}")

def analyze_solved_page_56():
    """Read and analyze page 56 to understand the cipher."""
    print("\n" + "="*60)
    print("ANALYZING SOLVED PAGE 56 CONTENT")
    print("="*60)
    
    # Page 56 content from wiki - already solved
    # Let's read the runes file and extract page 56
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    lp_text = load_file(lp_path)
    
    # Find page markers
    pages = lp_text.split('&')
    print(f"\nTotal pages found: {len(pages)}")
    
    # Page 56 should be near the end
    for i, page in enumerate(pages[-5:]):
        page_num = len(pages) - 5 + i
        runes = text_to_indices(page)
        n = len(runes)
        if n > 0:
            ioc = compute_ioc_normalized(runes)
            print(f"\nPage {page_num}: {n} runes, IoC={ioc:.4f}")
            sample = page[:200].replace('\n', ' ')
            print(f"  Sample: {sample[:100]}")

def try_running_key_with_solved_text(unsolved_indices):
    """
    Maybe the cipher uses solved pages as running key.
    """
    print("\n" + "="*60)
    print("RUNNING KEY WITH SOLVED PAGE TEXT")
    print("="*60)
    
    # Page 56 decrypted content (from wiki):
    # "A PRIMORDIAL WORD EMERGES FROM THE GERM..."
    # But we need the rune version
    
    # Try using the LP text itself as running key
    key = unsolved_indices.copy()
    np.random.shuffle(key)  # Random permutation
    
    # Try subtract
    result = (unsolved_indices - key) % 29
    ioc = compute_ioc_normalized(result)
    print(f"Subtract shuffled self as key: IoC={ioc:.4f}")
    
    # Use first N runes as key for last N runes
    n = len(unsolved_indices)
    half = n // 2
    
    key_first = unsolved_indices[:half]
    cipher_last = unsolved_indices[half:half + len(key_first)]
    
    result = (cipher_last - key_first) % 29
    ioc = compute_ioc_normalized(result)
    print(f"First half as key for second half: IoC={ioc:.4f}")

def analyze_prime_properties(indices):
    """Analyze properties related to prime numbers."""
    print("\n" + "="*60)
    print("PRIME NUMBER PROPERTIES")
    print("="*60)
    
    # What if positions matter?
    n = len(indices)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
              59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
              127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
              191, 193, 197, 199]
    
    # Get prime-position runes
    prime_positions = [p - 1 for p in primes if p <= n]  # 0-indexed
    prime_runes = indices[prime_positions]
    
    ioc = compute_ioc_normalized(prime_runes)
    print(f"\nRunes at prime positions ({len(prime_runes)} runes): IoC={ioc:.4f}")
    
    # Fibonacci positions
    fib = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946]
    fib_positions = [f - 1 for f in fib if f <= n]
    fib_runes = indices[fib_positions]
    
    ioc = compute_ioc_normalized(fib_runes)
    print(f"Runes at Fibonacci positions ({len(fib_runes)} runes): IoC={ioc:.4f}")
    text = ''.join(LETTERS[int(r)] for r in fib_runes)
    print(f"  Fibonacci runes: {text}")

def main():
    print("="*70)
    print("FRESH ANALYSIS - RETHINKING THE CIPHER")
    print("="*70)
    
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    lp_text = load_file(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    print(f"\nTotal runes: {len(lp_indices)}")
    print(f"Original IoC: {compute_ioc_normalized(lp_indices):.4f}")
    
    # Run analyses
    analyze_transposition_possibility(lp_indices)
    analyze_kappa_test_detailed(lp_indices)
    try_page56_method_variations(lp_indices)
    analyze_solved_page_56()
    try_running_key_with_solved_text(lp_indices)
    analyze_prime_properties(lp_indices)
    
    # Critical insight
    print("\n" + "="*60)
    print("CRITICAL OBSERVATION")
    print("="*60)
    print("""
The near-random IoC (1.03-1.04 for 29 symbols) strongly suggests:

1. NOT simple substitution cipher (would preserve letter frequencies)
2. NOT simple transposition (would preserve letter frequencies)
3. LIKELY polyalphabetic with very long/random key
4. OR stream cipher (each position has different shift)
5. OR multiple layers of encryption

The solved page 56 used: -(gematria(rune) + 57) mod 29
But this formula applied to unsolved pages produces ~1.03 IoC.

This means:
- Different pages likely use different methods/keys
- Or there's additional layer we haven't identified
- Or the key varies per-page or per-segment
""")

if __name__ == "__main__":
    main()

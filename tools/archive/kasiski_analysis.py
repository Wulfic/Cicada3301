#!/usr/bin/env python3
"""
KASISKI-STYLE KEY LENGTH ANALYSIS

The unsolved pages have IOC ~0.033-0.034 which indicates Vigenère.
Let's try to determine the KEY LENGTH using Kasiski examination
and then attempt to crack each page independently.
"""

import re
from pathlib import Path
from collections import Counter
import numpy as np

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def calc_ioc(indices):
    """Calculate Index of Coincidence"""
    n = len(indices)
    if n < 2:
        return 0
    freqs = Counter(indices)
    total = sum(f * (f - 1) for f in freqs.values())
    return total / (n * (n - 1))

def kasiski_examination(indices, max_length=20):
    """Find probable key lengths using Kasiski examination"""
    # Find repeated trigrams and their distances
    text = ''.join(str(i).zfill(2) for i in indices)  # Create string representation
    
    trigrams = {}
    for i in range(len(indices) - 2):
        tri = tuple(indices[i:i+3])
        if tri in trigrams:
            trigrams[tri].append(i)
        else:
            trigrams[tri] = [i]
    
    # Find distances between repetitions
    distances = []
    for tri, positions in trigrams.items():
        if len(positions) > 1:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    distances.append(positions[j] - positions[i])
    
    if not distances:
        return []
    
    # Find common factors
    factor_counts = Counter()
    for d in distances:
        for f in range(2, min(d + 1, max_length + 1)):
            if d % f == 0:
                factor_counts[f] += 1
    
    return factor_counts.most_common(10)

def ioc_test_key_length(indices, key_length):
    """Test a key length by calculating IOC for each column"""
    columns = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        columns[i % key_length].append(idx)
    
    iocs = [calc_ioc(col) for col in columns if len(col) > 1]
    return sum(iocs) / len(iocs) if iocs else 0

def crack_single_column(column_indices):
    """
    Try to crack a single column (Caesar shift).
    Returns best shift and score.
    """
    # Expected frequencies for English (adapted for 29-char alphabet)
    # A, E, I, N, O, R, S, T are common
    common_indices = [24, 18, 10, 9, 3, 4, 15, 16]  # A, E, I, N, O, R, S, T
    
    best_shift = 0
    best_score = 0
    
    for shift in range(29):
        shifted = [(idx - shift) % 29 for idx in column_indices]
        freqs = Counter(shifted)
        
        # Score: how many of the top 5 frequent letters are common letters
        top5 = [idx for idx, count in freqs.most_common(5)]
        score = sum(1 for idx in top5 if idx in common_indices)
        
        if score > best_score:
            best_score = score
            best_shift = shift
    
    return best_shift, best_score

def crack_vigenere(indices, key_length):
    """Attempt to crack Vigenère with given key length"""
    columns = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        columns[i % key_length].append(idx)
    
    key = []
    total_score = 0
    for col in columns:
        shift, score = crack_single_column(col)
        key.append(shift)
        total_score += score
    
    # Decrypt with found key
    decrypted = []
    for i, idx in enumerate(indices):
        plain_idx = (idx - key[i % key_length]) % 29
        decrypted.append(idx_to_letter(plain_idx))
    
    return key, ''.join(decrypted), total_score

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("KASISKI KEY LENGTH ANALYSIS")
    print("=" * 70)
    
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        indices = [rune_to_idx(r) for r in cipher]
        
        print(f"\n{'='*60}")
        print(f"PAGE {pg_num} ({len(indices)} runes)")
        print(f"{'='*60}")
        
        # Kasiski examination
        factors = kasiski_examination(indices)
        print(f"\nKasiski factors: {factors[:5]}")
        
        # IOC test for different key lengths
        print("\nIOC by key length:")
        for kl in range(2, 30):
            avg_ioc = ioc_test_key_length(indices, kl)
            if avg_ioc > 0.045:  # Higher than random (0.034) suggests correct length
                print(f"  len={kl:2d}: IOC={avg_ioc:.4f} {'<-- POSSIBLE' if avg_ioc > 0.055 else ''}")
        
        # Try cracking with top key lengths
        print("\nCracking attempts:")
        for kl in [5, 7, 10, 13, 14, 17, 19, 29, 95]:
            key, decrypted, score = crack_vigenere(indices, kl)
            if score >= kl * 2:  # At least 2 common letters per column on average
                print(f"\n  Key length {kl}:")
                print(f"    Key: {key[:20]}{'...' if len(key) > 20 else ''}")
                print(f"    Text: {decrypted[:50]}...")
                print(f"    Score: {score}")

    print("\n" + "=" * 70)
    print("TRYING KEY LENGTH = PRIME FACTORS OF PAGE LENGTH")
    print("=" * 70)
    
    def prime_factors(n):
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        n = len(cipher)
        indices = [rune_to_idx(r) for r in cipher]
        
        factors = prime_factors(n)
        print(f"\nPage {pg_num}: n={n}, prime factors={factors}")
        
        for f in set(factors):
            key, decrypted, score = crack_vigenere(indices, f)
            print(f"  Key len {f}: key={key}, text={decrypted[:40]}...")

if __name__ == "__main__":
    main()

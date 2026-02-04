#!/usr/bin/env python3
"""
BREAKTHROUGH INVESTIGATION: Iterated φ substitution

The φ(GP[value]) substitution applied iteratively shows increasing IoC!
Let's find the optimal number of iterations and examine the output.
"""

from collections import Counter
import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"
PRIMES_29 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
RUNEGLISH = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"

def totient(n):
    if n == 1: return 1
    result = n
    temp_n = n
    p = 2
    while p * p <= temp_n:
        if temp_n % p == 0:
            while temp_n % p == 0:
                temp_n //= p
            result -= result // p
        p += 1
    if temp_n > 1:
        result -= result // temp_n
    return result

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [c for c in text if c in RUNES]

def rune_to_idx(r):
    return RUNES.index(r) if r in RUNES else -1

def idx_to_text(indices):
    return ''.join(RUNEGLISH[i % 29] for i in indices)

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1) / 29) if n > 1 else 0

# φ(GP[i]) mod 29 lookup table
phi_gp_mod29 = [totient(PRIMES_29[i]) % 29 for i in range(29)]

def apply_phi_substitution(indices):
    """Apply single iteration of φ(GP[value]) substitution"""
    return [phi_gp_mod29[i] for i in indices]

def main():
    print("=" * 70)
    print("ITERATED φ SUBSTITUTION INVESTIGATION")
    print("=" * 70)
    
    print(f"φ(GP) mod29 table: {phi_gp_mod29}")
    
    # Load Page 20
    p20 = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    p20_idx = [rune_to_idx(r) for r in p20]
    
    print(f"\nPage 20: {len(p20)} runes")
    print(f"Original IoC: {calc_ioc(p20_idx):.2f}")
    
    # Iterate many times to find pattern
    print("\n" + "=" * 70)
    print("ITERATION ANALYSIS")
    print("=" * 70)
    
    current = p20_idx.copy()
    max_ioc = 0
    best_iter = 0
    best_text = ""
    
    for iteration in range(1, 30):
        current = apply_phi_substitution(current)
        ioc = calc_ioc(current)
        text = idx_to_text(current[:100])
        
        if ioc > max_ioc:
            max_ioc = ioc
            best_iter = iteration
            best_text = idx_to_text(current)
        
        # Check frequency distribution
        counts = Counter(current)
        unique_vals = len(counts)
        
        print(f"Iter {iteration:2d}: IoC = {ioc:.2f}, Unique values: {unique_vals}, Preview: {text[:40]}")
        
        # Stop if we converge to a single value
        if unique_vals <= 3:
            print("  -> Converged to very few values!")
            break
    
    print(f"\nBest iteration: {best_iter} with IoC = {max_ioc:.2f}")
    
    # Examine the frequency at convergence
    print("\n" + "=" * 70)
    print(f"EXAMINING BEST RESULT (Iteration {best_iter})")
    print("=" * 70)
    
    # Re-apply to get best result
    current = p20_idx.copy()
    for _ in range(best_iter):
        current = apply_phi_substitution(current)
    
    counts = Counter(current)
    print("Frequency distribution:")
    for val, count in sorted(counts.items()):
        pct = count / len(current) * 100
        print(f"  {RUNEGLISH[val]} (idx {val:2d}): {count:4d} ({pct:5.1f}%)")
    
    print(f"\nFull text ({len(best_text)} chars):")
    for i in range(0, len(best_text), 80):
        print(f"  {best_text[i:i+80]}")
    
    # Now let's try: combine iteration with Deor key
    print("\n" + "=" * 70)
    print("COMBINE ITERATED φ WITH DEOR KEY")
    print("=" * 70)
    
    # Load Deor
    deor_path = 'c:/Users/tyler/Repos/Cicada3301/Analysis/Reference_Docs/deor_poem.txt'
    with open(deor_path, 'r', encoding='utf-8') as f:
        deor_text = f.read().upper()
    
    # Simple Deor encoding
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    alt_map = {'A': 24, 'E': 18, 'O': 4, 'Y': 26, 'K': 5}
    deor = []
    i = 0
    while i < len(deor_text):
        if i < len(deor_text) - 1:
            digraph = deor_text[i:i+2]
            if digraph == 'TH': 
                deor.append(2)
                i += 2
                continue
        c = deor_text[i]
        if c in mapping:
            deor.append(mapping.index(c))
        elif c in alt_map:
            deor.append(alt_map[c])
        elif c.isalpha():
            deor.append((ord(c) - ord('A')) % 29)
        i += 1
    
    # Try: first iterate φ, then apply Deor Vigenere
    for num_iters in [1, 2, 3, 4, 5]:
        current = p20_idx.copy()
        for _ in range(num_iters):
            current = apply_phi_substitution(current)
        
        # Now apply Deor as Vigenere key
        decrypted = [(c - deor[i % len(deor)]) % 29 for i, c in enumerate(current)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:60])
        print(f"φ×{num_iters} then Deor SUB: IoC = {ioc:.2f} | {text[:50]}...")
    
    # Try: first apply Deor, then iterate φ
    print("\nReverse order (Deor first, then φ):")
    deor_first = [(c - deor[i % len(deor)]) % 29 for i, c in enumerate(p20_idx)]
    
    current = deor_first
    for iteration in range(1, 6):
        current = apply_phi_substitution(current)
        ioc = calc_ioc(current)
        text = idx_to_text(current[:60])
        print(f"Deor then φ×{iteration}: IoC = {ioc:.2f} | {text[:50]}...")

if __name__ == '__main__':
    main()

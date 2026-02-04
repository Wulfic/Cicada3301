#!/usr/bin/env python3
"""
Follow up on IoC = 1.62 finding!

The key φ(GP[rune_value]) where GP is Gematria Primus primes 
showed elevated IoC.

φ(GP primes) = [1, 2, 4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58, 60, 66, 70, 72, 78, 82, 88, 96, 100, 102, 106, 108]
Mod 29: [1, 2, 4, 6, 10, 12, 16, 18, 22, 28, 1, 7, 11, 13, 17, 23, 0, 2, 8, 12, 14, 20, 24, 1, 9, 13, 15, 19, 21]

This creates a self-referential key where each cipher rune's value 
determines its own decryption shift!
"""

from collections import Counter
import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"
PRIMES_29 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
RUNEGLISH = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"

def totient(n):
    if n == 1: return 1
    result = n
    p = 2
    temp_n = n
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

def main():
    print("=" * 70)
    print("DEEP DIVE: φ(GP[rune_value]) KEY")
    print("=" * 70)
    
    # φ(GP[i]) for each rune index
    phi_gp = [totient(PRIMES_29[i]) for i in range(29)]
    phi_gp_mod29 = [p % 29 for p in phi_gp]
    
    print(f"φ(GP) raw:   {phi_gp}")
    print(f"φ(GP) mod29: {phi_gp_mod29}")
    
    # This is essentially a substitution table!
    # Rune at index i → shift by φ(GP[i]) mod 29
    
    print("\n" + "=" * 70)
    print("TEST ON PAGE 20")
    print("=" * 70)
    
    p20 = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    p20_idx = [rune_to_idx(r) for r in p20]
    
    # Apply self-referential φ key
    key = [phi_gp_mod29[c] for c in p20_idx]
    
    # Try different operations
    operations = [
        ("C - φ(GP[C])", lambda c, k: (c - k) % 29),
        ("φ(GP[C]) - C", lambda c, k: (k - c) % 29),
        ("C + φ(GP[C])", lambda c, k: (c + k) % 29),
        ("C XOR φ(GP[C])", lambda c, k: c ^ k if (c ^ k) < 29 else c ^ k % 29),
    ]
    
    for name, op in operations:
        decrypted = [op(c, k) for c, k in zip(p20_idx, key)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:100])
        
        print(f"\n{name}:")
        print(f"  IoC: {ioc:.2f}")
        print(f"  Preview: {text[:80]}")
        
        # Look for words
        if ioc > 1.4:
            print(f"  FULL TEXT: {idx_to_text(decrypted)}")
    
    # Also test: use φ as a SUBSTITUTION cipher, not additive
    print("\n" + "=" * 70)
    print("SUBSTITUTION: Map rune index i → φ(GP[i]) mod 29")
    print("=" * 70)
    
    substituted = [phi_gp_mod29[c] for c in p20_idx]
    ioc = calc_ioc(substituted)
    text = idx_to_text(substituted[:100])
    print(f"IoC after substitution: {ioc:.2f}")
    print(f"Preview: {text[:80]}")
    
    # Test on other pages too
    print("\n" + "=" * 70)
    print("TEST ON ALL UNSOLVED PAGES")
    print("=" * 70)
    
    base = 'c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages'
    
    for page_num in range(20, 55):
        path = os.path.join(base, f'page_{page_num:02d}', 'runes.txt')
        if not os.path.exists(path):
            continue
        
        runes = load_runes(path)
        if len(runes) < 10:
            continue
        
        rune_idx = [rune_to_idx(r) for r in runes]
        key = [phi_gp_mod29[c] for c in rune_idx]
        
        # Try C - φ(GP[C])
        decrypted = [(c - k) % 29 for c, k in zip(rune_idx, key)]
        ioc = calc_ioc(decrypted)
        
        if ioc > 1.4:
            text = idx_to_text(decrypted[:60])
            print(f"Page {page_num}: IoC = {ioc:.2f} ** {text}")
        elif ioc > 1.2:
            print(f"Page {page_num}: IoC = {ioc:.2f}")
    
    # What if we iterate? Apply the φ substitution multiple times?
    print("\n" + "=" * 70)
    print("ITERATED φ SUBSTITUTION")
    print("=" * 70)
    
    current = p20_idx.copy()
    for iteration in range(1, 6):
        current = [phi_gp_mod29[c] for c in current]
        ioc = calc_ioc(current)
        text = idx_to_text(current[:60])
        print(f"Iteration {iteration}: IoC = {ioc:.2f} | {text[:40]}...")

if __name__ == '__main__':
    main()

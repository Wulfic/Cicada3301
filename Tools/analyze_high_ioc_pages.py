#!/usr/bin/env python3
"""
Deeper analysis of the high-IoC pages found in the prime-only test:
- Page 47: IoC = 1.40
- Page 49: IoC = 1.90
- Page 51: IoC = 1.37
- Page 54: IoC = 1.38

Also verify Page 20's 2×83 transposition claim.
"""

import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [c for c in text if c in RUNES]

def rune_to_idx(r):
    return RUNES.index(r) if r in RUNES else -1

def load_deor():
    filepath = 'c:/Users/tyler/Repos/Cicada3301/Analysis/Reference_Docs/deor_poem.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    alt_map = {'A': 24, 'E': 18, 'O': 4, 'Y': 28}
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph == 'TH': 
                indices.append(2)
                i += 2
                continue
            elif digraph == 'EA':
                indices.append(27)
                i += 2
                continue
            elif digraph == 'NG':
                indices.append(21)
                i += 2
                continue
        c = text[i]
        if c in mapping:
            indices.append(mapping.index(c))
        elif c in alt_map:
            indices.append(alt_map[c])
        elif c.isalpha():
            idx = ord(c) - ord('A')
            indices.append(idx % 29)
        i += 1
    return indices

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    from collections import Counter
    counts = Counter(indices)
    n = len(indices)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1) / 29) if n > 1 else 0

def decrypt_beaufort(cipher, key):
    return [(key[i % len(key)] - c) % 29 for i, c in enumerate(cipher)]

def decrypt_vigenere_sub(cipher, key):
    return [(c - key[i % len(key)]) % 29 for i, c in enumerate(cipher)]

def indices_to_text(indices):
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    return ''.join(mapping[i % 29] for i in indices)

def transpose_2xN(indices, cols):
    """Apply 2×N transposition: fill row-by-row, read column-by-column"""
    if len(indices) != cols * 2:
        return indices
    result = []
    for c in range(cols):
        result.append(indices[c])           # Row 0
        result.append(indices[cols + c])    # Row 1
    return result

def main():
    deor = load_deor()
    print(f"Deor length: {len(deor)}")
    
    base_path = 'c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages'
    
    # Pages of interest
    pages = [20, 47, 49, 51, 54]
    
    for page_num in pages:
        print("\n" + "=" * 70)
        print(f"PAGE {page_num} DEEP ANALYSIS")
        print("=" * 70)
        
        rune_file = os.path.join(base_path, f'page_{page_num:02d}', 'runes.txt')
        if not os.path.exists(rune_file):
            print("File not found")
            continue
        
        runes = load_runes(rune_file)
        print(f"Total runes: {len(runes)}")
        
        rune_indices = [rune_to_idx(r) for r in runes]
        
        # Get primes
        primes = [i for i in range(2, len(runes) + 1) if is_prime(i)]
        print(f"Prime positions (count): {len(primes)}")
        
        # Extract prime-position runes (1-indexed in the primes list)
        prime_runes = [(p, runes[p-1], rune_to_idx(runes[p-1])) for p in primes if p <= len(runes)]
        prime_indices = [idx for p, r, idx in prime_runes]
        
        print(f"\nPRIME POSITIONS ({len(prime_indices)} chars):")
        
        # Try raw decryption
        for cipher_name, cipher_func in [('Beaufort', decrypt_beaufort), 
                                          ('Vigenère SUB', decrypt_vigenere_sub)]:
            decrypted = cipher_func(prime_indices, deor)
            ioc = calc_ioc(decrypted)
            text = indices_to_text(decrypted)
            print(f"  {cipher_name:15}: IoC = {ioc:.2f}")
            print(f"    Text: {text}")
        
        # For Page 20, try 2×83 transposition
        if page_num == 20 and len(prime_indices) == 166:
            print(f"\nWITH 2×83 TRANSPOSITION:")
            transposed = transpose_2xN(prime_indices, 83)
            
            for cipher_name, cipher_func in [('Beaufort', decrypt_beaufort), 
                                              ('Vigenère SUB', decrypt_vigenere_sub)]:
                decrypted = cipher_func(transposed, deor)
                ioc = calc_ioc(decrypted)
                text = indices_to_text(decrypted)
                print(f"  {cipher_name:15}: IoC = {ioc:.2f}")
                print(f"    Text: {text[:80]}...")
        
        # Also check if no cipher at all gives good IoC (maybe it's already plaintext)
        raw_ioc = calc_ioc(prime_indices)
        raw_text = indices_to_text(prime_indices)
        print(f"\n  RAW (no cipher)  : IoC = {raw_ioc:.2f}")
        print(f"    Text: {raw_text[:60]}...")
        
        # Check all positions (not just primes)
        print(f"\nALL POSITIONS ({len(rune_indices)} chars):")
        for cipher_name, cipher_func in [('Beaufort', decrypt_beaufort), 
                                          ('Vigenère SUB', decrypt_vigenere_sub)]:
            decrypted = cipher_func(rune_indices, deor)
            ioc = calc_ioc(decrypted)
            print(f"  {cipher_name:15}: IoC = {ioc:.2f}")
        
        all_raw_ioc = calc_ioc(rune_indices)
        print(f"  RAW (no cipher)  : IoC = {all_raw_ioc:.2f}")

if __name__ == '__main__':
    main()

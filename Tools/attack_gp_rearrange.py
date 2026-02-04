#!/usr/bin/env python3
"""
Attack based on "REARRANGING THE PRIMES NUMBERS"

Hypothesis: The Gematria Primus primes (2,3,5,7,...,109) can be 
rearranged to create a substitution cipher.

We try various rearrangements based on prime properties.
"""

from collections import Counter
import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"
PRIMES_29 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
RUNEGLISH = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIAŒEA"[:29]

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

def digit_sum(n):
    return sum(int(d) for d in str(n))

def create_substitution_by_sort(sort_key_func, name):
    """
    Create a substitution by sorting the 29 primes by some property,
    then mapping original index -> sorted position.
    """
    # Pair each prime with its original index
    indexed_primes = [(i, p) for i, p in enumerate(PRIMES_29)]
    
    # Sort by the key function
    sorted_primes = sorted(indexed_primes, key=lambda x: sort_key_func(x[1]))
    
    # Create mapping: original index -> new position
    mapping = [0] * 29
    for new_pos, (orig_idx, prime) in enumerate(sorted_primes):
        mapping[orig_idx] = new_pos
    
    return mapping, name

def apply_substitution(indices, mapping):
    """Apply a substitution mapping."""
    return [mapping[i] for i in indices]

def main():
    print("=" * 70)
    print("GEMATRIA PRIMUS REARRANGEMENT ATTACK")
    print("=" * 70)
    
    # Load Page 20
    p20 = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    p20_idx = [rune_to_idx(r) for r in p20]
    
    print(f"Loaded {len(p20)} runes")
    print(f"Raw IoC: {calc_ioc(p20_idx):.2f}")
    
    # Create various substitutions
    substitutions = []
    
    # 1. Sort by digit sum
    substitutions.append(create_substitution_by_sort(digit_sum, "Digit sum"))
    
    # 2. Sort by last digit
    substitutions.append(create_substitution_by_sort(lambda p: p % 10, "Last digit"))
    
    # 3. Sort by p mod 29
    substitutions.append(create_substitution_by_sort(lambda p: p % 29, "p mod 29"))
    
    # 4. Sort by p mod 7
    substitutions.append(create_substitution_by_sort(lambda p: p % 7, "p mod 7"))
    
    # 5. Reverse order
    substitutions.append(([28-i for i in range(29)], "Reverse"))
    
    # 6. Sort by number of factors in (p-1)
    def num_factors(n):
        count = 0
        for i in range(1, int(n**0.5)+1):
            if n % i == 0:
                count += 2 if i != n // i else 1
        return count
    substitutions.append(create_substitution_by_sort(lambda p: num_factors(p-1), "Factors of p-1"))
    
    # 7. Sort by prime gap (difference from previous prime)
    prev_primes = [0] + PRIMES_29[:-1]
    gaps = [PRIMES_29[i] - prev_primes[i] for i in range(29)]
    substitutions.append(create_substitution_by_sort(lambda p: gaps[PRIMES_29.index(p)], "Prime gap"))
    
    # 8. Sort by number of 1-bits in binary representation
    substitutions.append(create_substitution_by_sort(lambda p: bin(p).count('1'), "Bit count"))
    
    # 9. Sort descending
    substitutions.append(create_substitution_by_sort(lambda p: -p, "Descending"))
    
    # 10. Prime index mod 29
    prime_indices = {p: i for i, p in enumerate(PRIMES_29)}
    substitutions.append(([i for i in range(29)], "Identity (control)"))
    
    print("\n" + "=" * 70)
    print("TESTING SUBSTITUTIONS ON PAGE 20")
    print("=" * 70)
    
    for mapping, name in substitutions:
        substituted = apply_substitution(p20_idx, mapping)
        ioc = calc_ioc(substituted)
        text = idx_to_text(substituted[:60])
        
        if ioc > 1.2:
            print(f"\n{name:20}: IoC = {ioc:.2f} ** PROMISING **")
            print(f"  Mapping: {mapping}")
            print(f"  Preview: {text}")
        else:
            print(f"{name:20}: IoC = {ioc:.2f}")
    
    # Also test on the 166-char decoded stream
    print("\n" + "=" * 70)
    print("TESTING SUBSTITUTIONS ON 166-CHAR STREAM")
    print("=" * 70)
    
    stream_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"
    
    # Parse stream to indices (simplified)
    simple_map = {'F':0,'U':1,'T':16,'H':8,'O':3,'R':4,'C':5,'G':6,'W':7,'N':9,'I':10,
                  'J':11,'E':18,'P':13,'X':14,'Z':14,'S':15,'B':17,'M':19,'L':20,
                  'D':23,'A':24,'Y':26}
    stream_idx = [simple_map.get(c, 0) for c in stream_166]
    
    for mapping, name in substitutions:
        substituted = apply_substitution(stream_idx, mapping)
        ioc = calc_ioc(substituted)
        text = idx_to_text(substituted[:60])
        
        if ioc > 1.3:
            print(f"\n{name:20}: IoC = {ioc:.2f} ** PROMISING **")
            print(f"  Preview: {text}")
    
    # Now try: use the rearranged substitution as a CIPHER KEY
    print("\n" + "=" * 70)
    print("USING REARRANGEMENT AS VIGENERE KEY")
    print("=" * 70)
    
    for mapping, name in substitutions[:5]:  # Just first few
        key = mapping  # The rearrangement IS the key
        
        # Apply Vigenere with this key
        decrypted_sub = [(c - key[i % len(key)]) % 29 for i, c in enumerate(p20_idx)]
        ioc = calc_ioc(decrypted_sub)
        
        if ioc > 1.2:
            text = idx_to_text(decrypted_sub[:60])
            print(f"{name} as Vigenere key: IoC = {ioc:.2f}")
            print(f"  Preview: {text}")

if __name__ == '__main__':
    main()

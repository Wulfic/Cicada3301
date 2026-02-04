#!/usr/bin/env python3
"""
Attack Pages 20-54 using Totient Function φ(n) as the cipher hint.

From Page 63: "THE TOTIENT FUNCTION IS SACRED"
From Page 19: "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"

Hypothesis: The cipher uses φ(prime) values as key shifts.

For each position i:
- If position is prime p, use φ(p) = p-1 as the shift
- Apply to decrypt with Deor

Or: Use running sequence of φ values from Gematria Primus primes.
"""

from collections import Counter
import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"
PRIMES_29 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
RUNEGLISH = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def totient(n):
    """Euler's totient function φ(n)"""
    if n == 1: return 1
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
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

def load_deor():
    filepath = 'c:/Users/tyler/Repos/Cicada3301/Analysis/Reference_Docs/deor_poem.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    alt_map = {'A': 24, 'E': 18, 'O': 4, 'Y': 26, 'K': 5}
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

def main():
    print("=" * 70)
    print("TOTIENT FUNCTION ATTACK")
    print("φ(n) is Euler's totient function - count of coprime integers <= n")
    print("=" * 70)
    
    # Load Page 20
    p20 = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    p20_idx = [rune_to_idx(r) for r in p20]
    deor = load_deor()
    
    print(f"Page 20: {len(p20)} runes")
    print(f"Deor key: {len(deor)} chars")
    
    # Create φ-based key sequences
    print("\n" + "=" * 70)
    print("METHOD 1: φ(position+1) as shift value")
    print("=" * 70)
    
    # For each position, shift by φ(position+1)
    key_phi_pos = [totient(i+1) % 29 for i in range(len(p20))]
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, key_phi_pos)]
    ioc = calc_ioc(decrypted)
    text = idx_to_text(decrypted[:80])
    print(f"Vigenère SUB with φ(pos): IoC = {ioc:.2f}")
    print(f"Preview: {text}")
    
    decrypted2 = [(k - c) % 29 for c, k in zip(p20_idx, key_phi_pos)]
    ioc2 = calc_ioc(decrypted2)
    text2 = idx_to_text(decrypted2[:80])
    print(f"Beaufort with φ(pos): IoC = {ioc2:.2f}")
    print(f"Preview: {text2}")
    
    print("\n" + "=" * 70)
    print("METHOD 2: φ(Gematria prime at position)")
    print("GP primes: 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109")
    print("=" * 70)
    
    # For each rune value (0-28), get the corresponding GP prime, then φ of that
    phi_of_gp = [totient(PRIMES_29[i]) for i in range(29)]
    print(f"φ(GP primes): {phi_of_gp}")
    
    # Apply: key[i] = φ(GP_prime_for_rune_value_at_i)
    key_phi_gp = [phi_of_gp[c] % 29 for c in p20_idx]
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, key_phi_gp)]
    ioc = calc_ioc(decrypted)
    text = idx_to_text(decrypted[:80])
    print(f"Vigenère SUB with φ(GP[value]): IoC = {ioc:.2f}")
    print(f"Preview: {text}")
    
    print("\n" + "=" * 70)
    print("METHOD 3: Combine Deor + φ")
    print("Key = (Deor[i] + φ(i)) mod 29")
    print("=" * 70)
    
    combined_key = [(deor[i % len(deor)] + totient(i+1)) % 29 for i in range(len(p20))]
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, combined_key)]
    ioc = calc_ioc(decrypted)
    text = idx_to_text(decrypted[:80])
    print(f"Vigenère SUB with (Deor+φ): IoC = {ioc:.2f}")
    print(f"Preview: {text}")
    
    decrypted2 = [(k - c) % 29 for c, k in zip(p20_idx, combined_key)]
    ioc2 = calc_ioc(decrypted2)
    text2 = idx_to_text(decrypted2[:80])
    print(f"Beaufort with (Deor+φ): IoC = {ioc2:.2f}")
    print(f"Preview: {text2}")
    
    print("\n" + "=" * 70)
    print("METHOD 4: Prime positions use φ(prime) shift")
    print("=" * 70)
    
    # At prime positions, shift by φ of that prime number
    key_conditional = []
    for i in range(len(p20)):
        pos = i + 1  # 1-indexed position
        if is_prime(pos):
            key_conditional.append(totient(pos) % 29)
        else:
            key_conditional.append(deor[i % len(deor)])
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, key_conditional)]
    ioc = calc_ioc(decrypted)
    text = idx_to_text(decrypted[:80])
    print(f"Hybrid (φ at primes, Deor elsewhere): IoC = {ioc:.2f}")
    print(f"Preview: {text}")
    
    print("\n" + "=" * 70)
    print("METHOD 5: Key = sequence of φ(2), φ(3), φ(5), ...")
    print("Running through first N primes")
    print("=" * 70)
    
    # Generate sequence of primes
    primes = [i for i in range(2, 1000) if is_prime(i)][:500]
    phi_primes_seq = [totient(p) % 29 for p in primes]
    
    key_phi_seq = [phi_primes_seq[i % len(phi_primes_seq)] for i in range(len(p20))]
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, key_phi_seq)]
    ioc = calc_ioc(decrypted)
    text = idx_to_text(decrypted[:80])
    print(f"Vigenère SUB with φ(prime_sequence): IoC = {ioc:.2f}")
    print(f"Preview: {text}")
    
    # Also try φ-1 pattern
    phi_minus_1 = [(p - 1) % 29 for p in primes][:500]
    key_phi_m1 = [phi_minus_1[i % len(phi_minus_1)] for i in range(len(p20))]
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, key_phi_m1)]
    ioc = calc_ioc(decrypted)
    print(f"Vigenère SUB with (prime-1) sequence: IoC = {ioc:.2f}")
    
    print("\n" + "=" * 70)
    print("METHOD 6: Deor at φ-indexed positions only")
    print("Read Deor[φ(1)], Deor[φ(2)], Deor[φ(3)], ...")
    print("=" * 70)
    
    phi_indexed_deor = [deor[totient(i+1) % len(deor)] for i in range(len(p20))]
    
    decrypted = [(c - k) % 29 for c, k in zip(p20_idx, phi_indexed_deor)]
    ioc = calc_ioc(decrypted)
    text = idx_to_text(decrypted[:80])
    print(f"Vigenère SUB with Deor[φ(pos)]: IoC = {ioc:.2f}")
    print(f"Preview: {text}")

if __name__ == '__main__':
    main()

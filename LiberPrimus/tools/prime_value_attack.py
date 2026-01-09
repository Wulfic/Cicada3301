#!/usr/bin/env python3
"""
Prime-Value Based Cipher Attack
================================
Each rune in Gematria Primus has a prime value (2-109).
What if the cipher operates on these prime values?
"""

import os
from collections import Counter

GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# Prime values for each rune (by index)
INDEX_TO_PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
                  59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

PRIME_TO_INDEX = {p: i for i, p in enumerate(INDEX_TO_PRIME)}

INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

def read_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [c for c in content if c in GP_RUNE_TO_INDEX]

def indices_to_runeglish(indices):
    return ''.join(INDEX_TO_RUNEGLISH[i % 29] for i in indices)

def score_english(text):
    score = 0
    common_words = ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT', 'IT', 'FOR', 
                    'AS', 'WITH', 'BE', 'WAS', 'ARE', 'THIS', 'TRUTH', 'SACRED',
                    'PRIMES', 'WISDOM', 'DIVINITY', 'PILGRIM', 'WELCOME']
    
    for word in common_words:
        if len(word) >= 3:
            count = text.count(word)
            score += count * len(word) * 10
    
    return score

# Load page 18
runes = read_runes("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_18/runes.txt")
cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]
cipher_primes = [INDEX_TO_PRIME[i] for i in cipher_indices]

print("="*70)
print("PRIME-VALUE BASED CIPHER ATTACK")
print("="*70)
print(f"Page 18: {len(runes)} runes")
print(f"First 20 prime values: {cipher_primes[:20]}")

# Strategy 1: Subtract sequential primes
print("\n" + "="*70)
print("STRATEGY 1: Subtract sequential primes from cipher primes")
print("="*70)

# Generate enough primes
def generate_primes(n):
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

all_primes = generate_primes(500)

# Decrypt by subtracting sequential primes
result1 = []
for i, cp in enumerate(cipher_primes):
    kp = all_primes[i]
    # Find difference and map back
    diff = (cp - kp) % 110  # Max prime value is 109
    # Try to find nearest prime in our set
    if diff in PRIME_TO_INDEX:
        result1.append(PRIME_TO_INDEX[diff])
    else:
        # Find closest prime
        closest = min(INDEX_TO_PRIME, key=lambda x: abs(x - diff))
        result1.append(PRIME_TO_INDEX[closest])

runeglish1 = indices_to_runeglish(result1)
print(f"Result: {runeglish1[:100]}")
print(f"Score: {score_english(runeglish1)}")

# Strategy 2: XOR prime values
print("\n" + "="*70)
print("STRATEGY 2: XOR prime values with sequential primes")
print("="*70)

result2 = []
for i, cp in enumerate(cipher_primes):
    kp = all_primes[i % len(all_primes)]
    xor_val = cp ^ kp
    if xor_val in PRIME_TO_INDEX:
        result2.append(PRIME_TO_INDEX[xor_val])
    else:
        closest = min(INDEX_TO_PRIME, key=lambda x: abs(x - xor_val))
        result2.append(PRIME_TO_INDEX[closest])

runeglish2 = indices_to_runeglish(result2)
print(f"Result: {runeglish2[:100]}")
print(f"Score: {score_english(runeglish2)}")

# Strategy 3: Modular arithmetic on primes
print("\n" + "="*70)
print("STRATEGY 3: (cipher_prime - key_prime) mod 113 (next prime after 109)")
print("="*70)

result3 = []
for i, cp in enumerate(cipher_primes):
    kp = all_primes[i]
    diff = (cp - kp) % 113
    if diff in PRIME_TO_INDEX:
        result3.append(PRIME_TO_INDEX[diff])
    else:
        closest = min(INDEX_TO_PRIME, key=lambda x: abs(x - diff))
        result3.append(PRIME_TO_INDEX[closest])

runeglish3 = indices_to_runeglish(result3)
print(f"Result: {runeglish3[:100]}")
print(f"Score: {score_english(runeglish3)}")

# Strategy 4: Use totient function on prime keys
print("\n" + "="*70)
print("STRATEGY 4: Use φ(prime) as key (φ(p) = p - 1 for primes)")
print("="*70)

# For primes, φ(p) = p - 1
result4 = []
for i, idx in enumerate(cipher_indices):
    prime = all_primes[i]
    totient = prime - 1  # φ(prime) = prime - 1
    plain_idx = (idx - (totient % 29)) % 29
    result4.append(plain_idx)

runeglish4 = indices_to_runeglish(result4)
print(f"Result: {runeglish4[:100]}")
print(f"Score: {score_english(runeglish4)}")

# Strategy 5: Sum of first N primes modulo 29
print("\n" + "="*70)
print("STRATEGY 5: Use sum of first N primes as key")
print("="*70)

# Key[i] = sum(primes[0:i+1]) mod 29
prime_sums = [sum(all_primes[:i+1]) for i in range(len(cipher_indices))]
result5 = [(cipher_indices[i] - (prime_sums[i] % 29)) % 29 for i in range(len(cipher_indices))]

runeglish5 = indices_to_runeglish(result5)
print(f"Result: {runeglish5[:100]}")
print(f"Score: {score_english(runeglish5)}")

# Strategy 6: Product of primes modulo 29
print("\n" + "="*70)
print("STRATEGY 6: Use product of primes mod 29 as key")
print("="*70)

prime_products = []
prod = 1
for i, p in enumerate(all_primes[:len(cipher_indices)]):
    prod = (prod * p) % 29
    prime_products.append(prod)

result6 = [(cipher_indices[i] - prime_products[i]) % 29 for i in range(len(cipher_indices))]
runeglish6 = indices_to_runeglish(result6)
print(f"Result: {runeglish6[:100]}")
print(f"Score: {score_english(runeglish6)}")

# Strategy 7: Use the prime INDEX as key (0,1,2,3... for prime 2,3,5,7...)
print("\n" + "="*70)
print("STRATEGY 7: Use prime's index as key (counting primes)")
print("="*70)

result7 = [(cipher_indices[i] - (i % 29)) % 29 for i in range(len(cipher_indices))]
runeglish7 = indices_to_runeglish(result7)
print(f"Result: {runeglish7[:100]}")
print(f"Score: {score_english(runeglish7)}")

# Strategy 8: Combine with page number
print("\n" + "="*70)
print("STRATEGY 8: Include page number in key (18)")
print("="*70)

page_num = 18
result8 = [(cipher_indices[i] - (all_primes[i] + page_num) % 29) % 29 for i in range(len(cipher_indices))]
runeglish8 = indices_to_runeglish(result8)
print(f"With page 18 offset: {runeglish8[:100]}")
print(f"Score: {score_english(runeglish8)}")

# IoC check on best results
print("\n" + "="*70)
print("IoC ANALYSIS")
print("="*70)

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counter = Counter(indices)
    n = len(indices)
    num = sum(c*(c-1) for c in counter.values())
    den = n*(n-1)
    return num/den if den > 0 else 0

print(f"Ciphertext IoC: {calc_ioc(cipher_indices):.4f}")
print(f"Strategy 4 (φ(prime)) IoC: {calc_ioc(result4):.4f}")
print(f"Strategy 5 (sum primes) IoC: {calc_ioc(result5):.4f}")
print(f"Strategy 7 (prime index) IoC: {calc_ioc(result7):.4f}")

#!/usr/bin/env python3
"""
Totient Function Key Generator

Based on the hint from Page 05: 
"THE PRIMES ARE SACRED, THE TOTIENT FUNCTION IS SACRED"

This script explores using Euler's totient function φ(n) to generate keys.

φ(n) = count of integers 1 to n that are coprime to n
For prime p: φ(p) = p - 1

Hypotheses:
1. Key derived from φ of page number
2. Key derived from φ of prime values in Gematria
3. Key is sequence of φ values modulo 29
4. Pages are encrypted with φ(n) shift pattern
"""

import math
import os

# Gematria Primus prime values
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 
             41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 
             97, 101, 103, 107, 109]

GP_CHARS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
            'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
            'A', 'AE', 'Y', 'IA', 'EA']

def euler_totient(n):
    """Calculate Euler's totient function φ(n)"""
    if n < 1:
        return 0
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

def sieve_totient(n):
    """Calculate φ(1) to φ(n) using sieve method"""
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi

# Calculate totients for first 200 numbers
phi = sieve_totient(200)

print("=" * 70)
print("TOTIENT FUNCTION ANALYSIS FOR LIBER PRIMUS")
print("=" * 70)

# Show φ values for page numbers
print("\n--- Totient values for page numbers 18-54 ---")
for page in range(18, 55):
    print(f"φ({page:2d}) = {phi[page]:2d}", end="   ")
    if (page - 17) % 6 == 0:
        print()

# Show φ values for Gematria primes
print("\n\n--- Totient values for Gematria Primus primes ---")
for i, p in enumerate(GP_PRIMES):
    print(f"φ({p:3d}) = {phi[p]:3d}  [{GP_CHARS[i]:2s}]", end="   ")
    if (i + 1) % 5 == 0:
        print()

# Generate key from φ(primes) mod 29
print("\n\n--- Key from φ(GP_PRIMES) mod 29 ---")
key_from_phi = [phi[p] % 29 for p in GP_PRIMES]
print(f"Raw: {key_from_phi}")
key_chars = [GP_CHARS[k] for k in key_from_phi]
print(f"As runeglish: {''.join(key_chars)}")

# Try φ of consecutive primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
print("\n--- Key from φ of consecutive primes ---")
phi_primes = [(p - 1) % 29 for p in primes]  # φ(p) = p-1 for prime p
print(f"φ(primes) mod 29: {phi_primes}")
phi_key_chars = [GP_CHARS[k] for k in phi_primes]
print(f"As runeglish: {''.join(phi_key_chars)}")

# Now let's try decrypting a sample page with totient-based key
print("\n" + "=" * 70)
print("TESTING TOTIENT KEY ON PAGE 18")
print("=" * 70)

# Read page 18 runes
page18_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt"

if os.path.exists(page18_path):
    with open(page18_path, 'r', encoding='utf-8') as f:
        runes = f.read().strip()
    
    # Convert runes to indices
    RUNE_TO_IDX = {
        'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
        'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
        'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
    }
    IDX_TO_GP = GP_CHARS
    
    rune_chars = [c for c in runes if c in RUNE_TO_IDX]
    rune_indices = [RUNE_TO_IDX[r] for r in rune_chars]
    
    print(f"Page 18 has {len(rune_indices)} runes")
    
    # Method 1: φ(i+1) mod 29 as key (i = position)
    print("\n--- Method 1: Key = φ(position+1) mod 29 ---")
    decoded1 = []
    for i, cipher_idx in enumerate(rune_indices[:100]):
        key_val = phi[i + 1] % 29
        plain_idx = (cipher_idx - key_val) % 29
        decoded1.append(IDX_TO_GP[plain_idx])
    print(f"First 100: {''.join(decoded1)}")
    
    # Method 2: φ(prime[i mod 29]) mod 29 as key
    print("\n--- Method 2: Key = φ(GP_PRIME[i mod 29]) mod 29 ---")
    decoded2 = []
    for i, cipher_idx in enumerate(rune_indices[:100]):
        key_val = phi[GP_PRIMES[i % 29]] % 29
        plain_idx = (cipher_idx - key_val) % 29
        decoded2.append(IDX_TO_GP[plain_idx])
    print(f"First 100: {''.join(decoded2)}")
    
    # Method 3: Key = sequence of φ(p) for consecutive primes p
    print("\n--- Method 3: Key = φ(consecutive primes) cycling ---")
    prime_seq = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    decoded3 = []
    for i, cipher_idx in enumerate(rune_indices[:100]):
        key_val = phi[prime_seq[i % len(prime_seq)]] % 29
        plain_idx = (cipher_idx - key_val) % 29
        decoded3.append(IDX_TO_GP[plain_idx])
    print(f"First 100: {''.join(decoded3)}")
    
    # Method 4: φ(cipher_index + 2) - the Gematria value's totient
    print("\n--- Method 4: Key = φ(GP_PRIME[cipher_idx]) ---")
    decoded4 = []
    for i, cipher_idx in enumerate(rune_indices[:100]):
        # The cipher rune has a Gematria prime value - use its totient
        gp_value = GP_PRIMES[cipher_idx]
        key_val = phi[gp_value] % 29
        plain_idx = (cipher_idx - key_val) % 29
        decoded4.append(IDX_TO_GP[plain_idx])
    print(f"First 100: {''.join(decoded4)}")
    
    # Method 5: φ(page_number) = φ(18) = 6, constant shift
    print("\n--- Method 5: Constant shift by φ(page_number) = φ(18) = 6 ---")
    decoded5 = []
    shift = phi[18]  # φ(18) = 6
    for cipher_idx in rune_indices[:100]:
        plain_idx = (cipher_idx - shift) % 29
        decoded5.append(IDX_TO_GP[plain_idx])
    print(f"First 100: {''.join(decoded5)}")
    
    # Method 6: Progressive φ shift - φ(18+i) for position i
    print("\n--- Method 6: Progressive φ shift - φ(page + position) ---")
    decoded6 = []
    base_page = 18
    for i, cipher_idx in enumerate(rune_indices[:100]):
        key_val = phi[base_page + i] % 29
        plain_idx = (cipher_idx - key_val) % 29
        decoded6.append(IDX_TO_GP[plain_idx])
    print(f"First 100: {''.join(decoded6)}")

else:
    print("Page 18 runes.txt not found")

# Additional insight: Sum of φ values
print("\n" + "=" * 70)
print("SPECIAL TOTIENT SEQUENCES")
print("=" * 70)

# Sum φ(1) + φ(2) + ... + φ(n) ≈ 3n²/π²
print("\nCumulative φ sums:")
cumsum = 0
for n in [10, 20, 29, 50, 100]:
    cumsum = sum(phi[1:n+1])
    print(f"Σφ(1..{n}) = {cumsum}")

# φ values that are prime
print("\nφ(n) values that are prime (first 100):")
prime_phi = [(n, phi[n]) for n in range(2, 101) if all(phi[n] % p != 0 for p in range(2, int(phi[n]**0.5)+1)) and phi[n] > 1]
print(prime_phi[:20])

# The number 29 is special - φ(29) = 28
print(f"\nφ(29) = {phi[29]} (this is the modulus we use!)")
print(f"φ(30) = {phi[30]}")
print(f"φ(58) = {phi[58]} (2 × 29)")
print(f"φ(87) = {phi[87]} (3 × 29)")

"""
Page 20 - Use Decoded Artifact as Key
======================================
The 166->83 decoded stream might be the key for the rest of P20.
"""

import os
from collections import Counter

# Gematria Primus
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def to_int(text):
    """Convert Runeglish to list of indices"""
    res = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text) and text[i:i+2] in GP_MAP:
            res.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            res.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return res

def to_str(nums):
    return "".join([RUNEGLISH[n] for n in nums])

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    freq = Counter(indices)
    n = len(indices)
    return sum(f * (f-1) for f in freq.values()) / (n * (n-1) / 29)

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def get_primes_up_to(n):
    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]

# The decoded artifact (83 tokens)
ARTIFACT = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIRSIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"
artifact_ints = to_int(ARTIFACT)
print(f"Artifact: {len(artifact_ints)} tokens")
print(f"  {ARTIFACT[:50]}...")

# Load P20
os.chdir(r"c:\Users\tyler\Repos\Cicada3301")
p20 = load_runes("LiberPrimus/pages/page_20/runes.txt")
print(f"\nPage 20: {len(p20)} runes, IoC: {calc_ioc(p20):.4f}")

# Get prime and non-prime indices
primes = get_primes_up_to(len(p20))
prime_indices = [i for i in primes if i < len(p20)]
non_prime_indices = [i for i in range(len(p20)) if i not in prime_indices]

p20_primes = [p20[i] for i in prime_indices]
p20_non_primes = [p20[i] for i in non_prime_indices]

print(f"\nPrime-indexed runes: {len(p20_primes)}")
print(f"Non-prime-indexed runes: {len(p20_non_primes)}")

# Try using artifact as key for non-prime runes
print("\n=== ARTIFACT AS KEY FOR NON-PRIMES ===")

key = artifact_ints

# Extend key cyclically
key_ext = (key * (len(p20_non_primes) // len(key) + 1))[:len(p20_non_primes)]

# Vigenere decrypt: P = C - K mod 29
decrypted = [(c - k) % 29 for c, k in zip(p20_non_primes, key_ext)]
ioc = calc_ioc(decrypted)
print(f"Vigenere (C-K): IoC = {ioc:.4f}")
print(f"  First 50: {to_str(decrypted[:50])}")

# Vigenere add: P = C + K mod 29
decrypted2 = [(c + k) % 29 for c, k in zip(p20_non_primes, key_ext)]
ioc2 = calc_ioc(decrypted2)
print(f"Vigenere (C+K): IoC = {ioc2:.4f}")
print(f"  First 50: {to_str(decrypted2[:50])}")

# Beaufort: P = K - C mod 29
decrypted3 = [(k - c) % 29 for c, k in zip(p20_non_primes, key_ext)]
ioc3 = calc_ioc(decrypted3)
print(f"Beaufort (K-C): IoC = {ioc3:.4f}")
print(f"  First 50: {to_str(decrypted3[:50])}")

# Try artifact as key for ALL of P20
print("\n=== ARTIFACT AS KEY FOR ALL P20 ===")

key_full = (key * (len(p20) // len(key) + 1))[:len(p20)]

for name, op in [("C-K", lambda c, k: (c-k)%29), 
                 ("C+K", lambda c, k: (c+k)%29),
                 ("K-C", lambda c, k: (k-c)%29)]:
    dec = [op(c, k) for c, k in zip(p20, key_full)]
    ioc = calc_ioc(dec)
    print(f"{name}: IoC = {ioc:.4f}  First 40: {to_str(dec[:40])}")

# Try different starting positions
print("\n=== KEY OFFSET SEARCH ===")
best_ioc = 0
best_offset = 0
for offset in range(len(key)):
    key_shifted = key[offset:] + key[:offset]
    key_ext = (key_shifted * (len(p20) // len(key) + 1))[:len(p20)]
    dec = [(c - k) % 29 for c, k in zip(p20, key_ext)]
    ioc = calc_ioc(dec)
    if ioc > best_ioc:
        best_ioc = ioc
        best_offset = offset

print(f"Best offset: {best_offset}, IoC: {best_ioc:.4f}")

# Try reversed artifact
print("\n=== REVERSED ARTIFACT ===")
key_rev = artifact_ints[::-1]
key_ext = (key_rev * (len(p20) // len(key) + 1))[:len(p20)]
dec = [(c - k) % 29 for c, k in zip(p20, key_ext)]
print(f"Reversed key: IoC = {calc_ioc(dec):.4f}")

# What about using the 166-rune stream directly?
print("\n=== 166-RUNE STREAM AS KEY ===")
# Load the 166-rune stream
stream_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"
stream_ints = to_int(stream_166)
print(f"166-stream: {len(stream_ints)} tokens")

# Use as key
key_166 = (stream_ints * (len(p20) // len(stream_ints) + 1))[:len(p20)]
dec = [(c - k) % 29 for c, k in zip(p20, key_166)]
print(f"166-stream key: IoC = {calc_ioc(dec):.4f}")
print(f"  First 50: {to_str(dec[:50])}")

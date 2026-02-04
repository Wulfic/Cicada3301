"""
Debug Page 73 decryption step by step
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def totient(n):
    if n == 1:
        return 1
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

def rune_to_index(rune):
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

# Load Page 73
page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_73"
with open(os.path.join(page_dir, "runes.txt"), 'r', encoding='utf-8') as f:
    content = f.read()
    runes = [c for c in content if c in GP_RUNES]

print(f"Page 73 rune count: {len(runes)}")
print(f"First 10 runes: {runes[:10]}")

# Decode first 10 positions step by step
primes = generate_primes(100)
print("\nStep-by-step decryption:")
print("Pos | Rune | CipherIdx | Prime | phi(p) | Shift | PlainIdx | Latin")
print("-" * 70)

result = []
prime_idx = 0
for i, rune in enumerate(runes[:20]):
    cipher_idx = rune_to_index(rune)
    prime = primes[prime_idx]
    phi = totient(prime)
    shift = phi % 29
    plain_idx = (cipher_idx - shift) % 29
    latin = index_to_latin(plain_idx)
    result.append(latin)
    print(f"{i:3} | {rune}    | {cipher_idx:9} | {prime:5} | {phi:6} | {shift:5} | {plain_idx:8} | {latin}")
    prime_idx += 1

print(f"\nFirst 20 chars: {''.join(result)}")
print(f"Expected: ANENDWITHINTHEDEEPWE")

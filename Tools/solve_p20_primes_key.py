import collections

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
INV_RUNE_MAP = {v: k for k, v in RUNE_MAP.items()}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def get_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_p = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_p = False
                break
        if is_p:
            primes.append(candidate)
        candidate += 1
    return primes

def decrypt(cipher_indices, key_shifts):
    plain = []
    for c, k in zip(cipher_indices, key_shifts):
        p = (c - k) % 29
        plain.append(INV_RUNE_MAP[p])
    return "".join(plain)

def decrypt_add(cipher_indices, key_shifts):
    plain = []
    for c, k in zip(cipher_indices, key_shifts):
        p = (c + k) % 29
        plain.append(INV_RUNE_MAP[p])
    return "".join(plain)

# Check English
def score_english(text):
    # Simple check for common trigrams like 'THE', 'AND', 'ING'
    # Converted to approx runes
    # THE = ᛏᚻᛖ
    score = 0
    common = ['ᛏᚻᛖ', 'ᚪᚾᛞ', 'ᛁᚾᚷ']
    for tri in common:
        score += text.count(tri)
    return score

p20_nums = load_runes('LiberPrimus/pages/page_20/runes.txt')
key_len = len(p20_nums)

# Generate Primes
primes = get_primes(key_len)
# Primes mod 29
primes_mod = [p % 29 for p in primes]

# Attempt 1: SUBTRACT Key (Standard Vigenere)
d1 = decrypt(p20_nums, primes_mod)
print(f"Decryption (C - Primes):")
print(d1[:100])

# Attempt 2: ADD Key
d2 = decrypt_add(p20_nums, primes_mod)
print(f"\nDecryption (C + Primes):")
print(d2[:100])

# Attempt 3: Primes in Reverse (Descending from Nth prime)
primes_rev = primes[::-1]
primes_rev_mod = [p % 29 for p in primes_rev]

d3 = decrypt(p20_nums, primes_rev_mod)
print(f"\nDecryption (C - ReversedPrimes):")
print(d3[:100])


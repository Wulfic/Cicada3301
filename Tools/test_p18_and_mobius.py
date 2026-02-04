"""
Test using Page 18 solution as key for Pages 21-30
And test Möbius function cipher
"""

import os
from collections import Counter

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Gematria Primus
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# GP primes
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Page 18 solution (from SOLUTION.md)
P18_PLAINTEXT = "BEINGOFALLIWILASC THEOATHISSWORN TOTHEONE WITHINTHEABOFETHEWAY"
# Clean version (Runeglish compatible)
P18_CLEAN = "BEINGOFALLIWILASCTHEOATHISSWORNTOTHEONEWITHINTHEA BOFETHEWAY"
# Actually the exact text is:
P18_EXACT = "BEINGOFALLIWILASCTHEOATHISSWORNTOTHEONEWITHINTHEABOFETHEWAY"

def tokenize(text):
    """Convert text to GP indices with digraph handling"""
    text = text.upper().replace(' ', '')
    values = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in GP_MAP:
            values.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            values.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return values

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def to_str(indices):
    return "".join(INV_MAP[i % 29] for i in indices)

def load_page(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def mobius(n):
    """Möbius function μ(n)"""
    if n == 1:
        return 1
    
    # Factorize and check for squares
    prime_factors = 0
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            temp //= p
            prime_factors += 1
            if temp % p == 0:  # Squared factor
                return 0
        p += 1
    if temp > 1:
        prime_factors += 1
    
    return 1 if prime_factors % 2 == 0 else -1

def totient(n):
    """Euler's totient function φ(n)"""
    if n < 2:
        return 1
    # For primes, φ(p) = p - 1
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

# Convert P18 plaintext to key
P18_KEY = tokenize(P18_EXACT)
print(f"Page 18 plaintext as key: {len(P18_KEY)} values")
print(f"Key: {to_str(P18_KEY)}")

print("\n" + "="*70)
print("TEST 1: P18 PLAINTEXT AS KEY FOR PAGES 21-30")
print("="*70)

WORDS = ['THE', 'LONE', 'HER', 'ONE', 'ALT', 'MET', 'ODE', 'AM', 'BID', 'SAY', 'OF',
         'DEATH', 'PATH', 'SELF', 'AND', 'FOR', 'YOU', 'ALL', 'ARE', 'BEING', 'WITHIN',
         'THIS', 'THAT', 'WITH', 'HAVE', 'WILL', 'FROM', 'THEY', 'BEEN', 'SWORN', 'OATH']

def find_words(text, words):
    return [w for w in words if w in text]

for page_num in range(21, 31):
    page_runes = load_page(page_num)
    if page_runes is None:
        continue
    
    # Vigenere SUB
    dec_sub = [(page_runes[i] - P18_KEY[i % len(P18_KEY)]) % 29 for i in range(len(page_runes))]
    text_sub = to_str(dec_sub)
    ioc_sub = calc_ioc(dec_sub)
    words_sub = find_words(text_sub, WORDS)
    
    # Vigenere ADD  
    dec_add = [(page_runes[i] + P18_KEY[i % len(P18_KEY)]) % 29 for i in range(len(page_runes))]
    text_add = to_str(dec_add)
    ioc_add = calc_ioc(dec_add)
    words_add = find_words(text_add, WORDS)
    
    # Beaufort
    dec_beau = [(P18_KEY[i % len(P18_KEY)] - page_runes[i]) % 29 for i in range(len(page_runes))]
    text_beau = to_str(dec_beau)
    ioc_beau = calc_ioc(dec_beau)
    words_beau = find_words(text_beau, WORDS)
    
    print(f"\nPage {page_num} ({len(page_runes)} runes):")
    if ioc_sub > 1.1 or words_sub:
        print(f"  SUB: IoC={ioc_sub:.4f}, Words={words_sub}")
        print(f"    '{text_sub[:60]}...'")
    if ioc_add > 1.1 or words_add:
        print(f"  ADD: IoC={ioc_add:.4f}, Words={words_add}")
        print(f"    '{text_add[:60]}...'")
    if ioc_beau > 1.1 or words_beau:
        print(f"  BEAU: IoC={ioc_beau:.4f}, Words={words_beau}")
        print(f"    '{text_beau[:60]}...'")
    if not (words_sub or words_add or words_beau or ioc_sub > 1.1 or ioc_add > 1.1 or ioc_beau > 1.1):
        print(f"  No promising results (IoC < 1.1)")

print("\n" + "="*70)
print("TEST 2: MÖBIUS + TOTIENT CIPHER")
print("="*70)

# For each rune, try: P = C - μ(prime_value) mod 29
# or P = C - φ(prime_value) mod 29 (φ mod 29)

for page_num in [21, 22, 23, 24, 25]:
    page_runes = load_page(page_num)
    if page_runes is None:
        continue
    
    # Möbius function shift
    dec_mobius = []
    for c in page_runes:
        prime = GP_PRIMES[c]
        mu = mobius(prime)
        # μ(prime) = -1 for all primes > 1
        # So this is just a Caesar shift by 1 (or -1, which is +28)
        p = (c - mu) % 29
        dec_mobius.append(p)
    
    text_mob = to_str(dec_mobius)
    ioc_mob = calc_ioc(dec_mobius)
    words_mob = find_words(text_mob, WORDS)
    
    # Totient function shift (φ(prime) mod 29)
    dec_phi = []
    for c in page_runes:
        prime = GP_PRIMES[c]
        phi = totient(prime)
        p = (c - (phi % 29)) % 29
        dec_phi.append(p)
    
    text_phi = to_str(dec_phi)
    ioc_phi = calc_ioc(dec_phi)
    words_phi = find_words(text_phi, WORDS)
    
    print(f"\nPage {page_num}:")
    print(f"  Möbius shift: IoC={ioc_mob:.4f}, Words={words_mob}")
    if words_mob:
        print(f"    '{text_mob[:60]}...'")
    print(f"  Totient shift: IoC={ioc_phi:.4f}, Words={words_phi}")
    if words_phi:
        print(f"    '{text_phi[:60]}...'")

print("\n" + "="*70)
print("TEST 3: P19 HINT 'REARRANGING PRIMES' - DIFFERENT INTERPRETATION")
print("="*70)

# What if "rearranging the primes numbers" means sorting positions by prime value?
for page_num in [21, 22, 23]:
    page_runes = load_page(page_num)
    if page_runes is None:
        continue
    
    # Sort runes by their prime value
    indexed_runes = list(enumerate(page_runes))
    sorted_by_prime = sorted(indexed_runes, key=lambda x: GP_PRIMES[x[1]])
    
    # Read in sorted order
    sorted_text = to_str([r for _, r in sorted_by_prime])
    sorted_ioc = calc_ioc([r for _, r in sorted_by_prime])
    
    # Group by prime value and read
    grouped = {}
    for i, r in enumerate(page_runes):
        p = GP_PRIMES[r]
        if p not in grouped:
            grouped[p] = []
        grouped[p].append(r)
    
    # Read low primes first (F=2, U=3, TH=5...)
    by_prime_text = []
    for p in sorted(grouped.keys()):
        by_prime_text.extend(grouped[p])
    
    by_prime_str = to_str(by_prime_text)
    by_prime_ioc = calc_ioc(by_prime_text)
    
    print(f"\nPage {page_num}:")
    print(f"  Sorted by prime value: IoC={sorted_ioc:.4f}")
    print(f"    '{sorted_text[:60]}...'")
    print(f"  Grouped by prime: IoC={by_prime_ioc:.4f}")
    print(f"    '{by_prime_str[:60]}...'")

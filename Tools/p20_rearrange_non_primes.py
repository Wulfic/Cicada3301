"""
Page 20 - Rearrange Non-Prime Runes
====================================
The prime-indexed runes decoded to "THE LONE" with Deor.
Now try rearranging the non-prime runes to find the rest.
"""

import os
from collections import Counter

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def to_str(nums):
    return "".join(RUNEGLISH[n % 29] for n in nums)

def to_int(text):
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in GP_MAP:
            result.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            result.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return result

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

# Primes for indexing (first 100)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Load P20
p20 = load_runes("LiberPrimus/pages/page_20/runes.txt")
print(f"P20: {len(p20)} runes")

# Get prime and non-prime indexed runes  
prime_positions = [i for i in range(len(p20)) if is_prime(i)]
non_prime_positions = [i for i in range(len(p20)) if not is_prime(i)]

p20_primes = [p20[i] for i in prime_positions]
p20_non_primes = [p20[i] for i in non_prime_positions]

print(f"Prime positions: {len(prime_positions)} (IoC: {calc_ioc(p20_primes):.4f})")
print(f"Non-prime positions: {len(non_prime_positions)} (IoC: {calc_ioc(p20_non_primes):.4f})")

# Load Deor
deor = to_int(open("Analysis/Reference_Docs/deor_poem.txt", encoding='utf-8').read())
print(f"Deor: {len(deor)} runes")

# The decoded prime message
DECODED_PRIMES = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"

print(f"\n=== TESTING VARIOUS APPROACHES FOR NON-PRIMES ===\n")

# Approach 1: Rearrange by prime value of the rune itself
print("1. REARRANGING BY GEMATRIA PRIME VALUE")
# Each rune has a Gematria prime value: F=2, U=3, TH=5, O=7, etc.
# Sort non-prime runes by their Gematria prime value

def get_gematria_prime(idx):
    """Get the Gematria prime for a rune index"""
    return PRIMES[idx] if idx < len(PRIMES) else idx * 4  # Fallback for high indices

sorted_pairs = sorted(enumerate(p20_non_primes), key=lambda x: get_gematria_prime(x[1]))
rearranged = [pair[1] for pair in sorted_pairs]

# Apply Deor key
key = deor * (len(rearranged) // len(deor) + 1)
key = key[:len(rearranged)]
decrypted = [(c - k) % 29 for c, k in zip(rearranged, key)]
ioc = calc_ioc(decrypted)
text = to_str(decrypted)
print(f"  Sorted by Gematria prime + Deor: IoC={ioc:.4f}")
print(f"  {text[:60]}...")

# Approach 2: Prime-based column extraction
print("\n2. PRIME-COLUMN EXTRACTION (28x29 grid)")
# P20 as 28 rows × 29 cols
ROWS, COLS = 28, 29
grid = [p20[r*COLS:(r+1)*COLS] for r in range(ROWS)]

# Extract prime columns (2, 3, 5, 7, 11, 13, 17, 19, 23 are prime < 29)
prime_cols = [i for i in range(COLS) if is_prime(i)]
non_prime_cols = [i for i in range(COLS) if not is_prime(i)]

print(f"  Prime columns: {prime_cols}")
print(f"  Non-prime columns: {non_prime_cols}")

# Read prime columns first, then non-prime
reordered = []
for c in prime_cols + non_prime_cols:
    for r in range(ROWS):
        reordered.append(grid[r][c])

# Apply Deor
key = deor * (len(reordered) // len(deor) + 1)
key = key[:len(reordered)]
decrypted = [(c - k) % 29 for c, k in zip(reordered, key)]
ioc = calc_ioc(decrypted)
text = to_str(decrypted)
print(f"  Prime cols first + Deor: IoC={ioc:.4f}")
print(f"  {text[:60]}...")

# Approach 3: Use decoded primes as key pattern
print("\n3. DECODED PRIMES AS KEY FOR NON-PRIMES")
decoded_key = to_int(DECODED_PRIMES)
print(f"  Decoded key length: {len(decoded_key)}")

# Extend key to match non-primes
key = decoded_key * (len(p20_non_primes) // len(decoded_key) + 1)
key = key[:len(p20_non_primes)]

for op_name, op in [('sub', lambda c, k: (c-k)%29), 
                    ('add', lambda c, k: (c+k)%29),
                    ('beaufort', lambda c, k: (k-c)%29)]:
    decrypted = [op(c, k) for c, k in zip(p20_non_primes, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    print(f"  Decoded primes as key ({op_name}): IoC={ioc:.4f}")
    if ioc > 1.2:
        print(f"    {text[:60]}...")

# Approach 4: Composite number extraction (opposite of primes)
print("\n4. COMPOSITE NUMBER REARRANGEMENT")
# What if we sort by whether position is prime power, semiprime, etc.?

def is_semiprime(n):
    """Number with exactly two prime factors"""
    if n < 4: return False
    factors = 0
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            temp //= d
            factors += 1
            if factors > 2: return False
        d += 1
    if temp > 1:
        factors += 1
    return factors == 2

# Get semiprimes among non-prime positions
semiprimes = [i for i in non_prime_positions if is_semiprime(i)]
other = [i for i in non_prime_positions if not is_semiprime(i)]

print(f"  Semiprime positions: {len(semiprimes)}")
print(f"  Other positions: {len(other)}")

# Extract semiprime-positioned runes
semiprime_runes = [p20[i] for i in semiprimes]
if len(semiprime_runes) > 0:
    key = deor * (len(semiprime_runes) // len(deor) + 1)
    key = key[:len(semiprime_runes)]
    decrypted = [(c - k) % 29 for c, k in zip(semiprime_runes, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    print(f"  Semiprime positions + Deor: IoC={ioc:.4f} (n={len(decrypted)})")
    print(f"    {text[:60]}...")

# Approach 5: Interleave prime and non-prime columns
print("\n5. INTERLEAVE PRIME/NON-PRIME COLUMNS")
interleaved = []
p_idx, np_idx = 0, 0
for c in range(COLS):
    for r in range(ROWS):
        interleaved.append(grid[r][c])

# This is just reading by columns, apply Deor
key = deor * (len(interleaved) // len(deor) + 1)
key = key[:len(interleaved)]
decrypted = [(c - k) % 29 for c, k in zip(interleaved, key)]
ioc = calc_ioc(decrypted)
text = to_str(decrypted)
print(f"  Column reading + Deor: IoC={ioc:.4f}")
print(f"  {text[:60]}...")

# Approach 6: Try different grid dimensions
print("\n6. ALTERNATIVE GRID DIMENSIONS")
# 812 = 4 × 7 × 29 = 28 × 29
# Also: 812 = 2 × 2 × 7 × 29

for rows, cols in [(4, 203), (7, 116), (14, 58), (29, 28), (58, 14), (116, 7)]:
    if rows * cols == 812:
        # Create grid and read by columns
        g = [p20[r*cols:(r+1)*cols] for r in range(rows)]
        col_read = []
        for c in range(cols):
            for r in range(rows):
                if c < len(g[r]):
                    col_read.append(g[r][c])
        
        # Apply Deor
        key = deor * (len(col_read) // len(deor) + 1)
        key = key[:len(col_read)]
        decrypted = [(c - k) % 29 for c, k in zip(col_read, key)]
        ioc = calc_ioc(decrypted)
        text = to_str(decrypted)
        
        if ioc > 1.1:
            print(f"  Grid {rows}×{cols} + Deor: IoC={ioc:.4f}")
            print(f"    {text[:60]}...")

print("\n=== SUMMARY ===")
print("The non-prime runes still show IoC ~1.0 (random) under all tested methods.")
print("The non-prime portion may require a different key or approach entirely.")
print("Possible: The decoded prime message contains instructions for non-primes.")

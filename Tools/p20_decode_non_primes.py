"""
Page 20 - Decode Non-Prime Runes
=================================
We decoded the 166 prime-indexed runes.
Now let's try the 646 non-prime indexed runes.
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

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def to_str(nums):
    return "".join(RUNEGLISH[n % 29] for n in nums)

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

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Load P20 and Deor
p20 = load_runes("LiberPrimus/pages/page_20/runes.txt")
print(f"P20: {len(p20)} runes")

# Load Deor
deor_path = "LiberPrimus/reference/deor.txt"
try:
    deor = load_runes(deor_path)
except:
    # Use the known Deor text if file not found
    DEOR_TEXT = """WELUND HIM BE WURMAN WRAECES CUNNADE ANHYDIG EORL EARFOTHA DREAG
HAEFDE HIM TO GESITHE SORGE OND LONGATH WINTERCEALDE WRAECE WEAN OFT ONFOND
SITHTHAN HINE NITHHAD ON NEDE LEGDE SWONCRE SEONOBENDE ON SYLLAN MONN
THAES OFEREODE THISSES SWA MAEG"""
    from itertools import chain
    GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
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
    deor = to_int(DEOR_TEXT)

print(f"Deor: {len(deor)} runes")

# Extract prime and non-prime indexed runes
prime_indices = [i for i in range(len(p20)) if is_prime(i)]
non_prime_indices = [i for i in range(len(p20)) if not is_prime(i)]

p20_primes = [p20[i] for i in prime_indices]
p20_non_primes = [p20[i] for i in non_prime_indices]

print(f"\nPrime-indexed: {len(p20_primes)} runes (positions: {prime_indices[:10]}...)")
print(f"Non-prime-indexed: {len(p20_non_primes)} runes (positions: {non_prime_indices[:10]}...)")
print(f"  IoC of non-primes: {calc_ioc(p20_non_primes):.4f}")

# Try different decryption methods on non-prime runes
print("\n=== TESTING DECRYPTION METHODS ON NON-PRIME RUNES ===\n")

# Method 1: Direct Deor key (cycling)
key = deor * (len(p20_non_primes) // len(deor) + 1)
key = key[:len(p20_non_primes)]

for op_name, op in [('sub', lambda c, k: (c-k)%29), 
                    ('add', lambda c, k: (c+k)%29),
                    ('beaufort', lambda c, k: (k-c)%29)]:
    decrypted = [op(c, k) for c, k in zip(p20_non_primes, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    print(f"Deor cycling ({op_name}): IoC={ioc:.4f}")
    print(f"  {text[:60]}...")

# Method 2: Use the decoded prime message as key
# The 166-stream decoded to "THE LONE" etc.
DECODED_PRIMES = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"
GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}

def text_to_nums(text):
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

decoded_key = text_to_nums(DECODED_PRIMES)
print(f"\nUsing decoded prime message as key ({len(decoded_key)} values):")

key = decoded_key * (len(p20_non_primes) // len(decoded_key) + 1)
key = key[:len(p20_non_primes)]

for op_name, op in [('sub', lambda c, k: (c-k)%29), 
                    ('beaufort', lambda c, k: (k-c)%29)]:
    decrypted = [op(c, k) for c, k in zip(p20_non_primes, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    print(f"Decoded primes as key ({op_name}): IoC={ioc:.4f}")
    print(f"  {text[:60]}...")

# Method 3: Try different grid transpositions on non-prime runes
print("\n=== GRID TRANSPOSITIONS ON NON-PRIME RUNES ===")

def col_read_grid(values, rows, cols):
    """Column-major reading of row-major filled grid"""
    result = []
    for c in range(cols):
        for r in range(rows):
            idx = r * cols + c
            if idx < len(values):
                result.append(values[idx])
    return result

# Find divisors of 646
divisors = [(r, 646//r) for r in range(2, 324) if 646 % r == 0]
print(f"Divisors of 646: {divisors}")

best_ioc = 0
best_result = None

for rows, cols in divisors[:10]:  # Test first 10
    transposed = col_read_grid(p20_non_primes, rows, cols)
    
    # Apply Deor key
    key = deor * (len(transposed) // len(deor) + 1)
    key = key[:len(transposed)]
    
    decrypted = [(c - k) % 29 for c, k in zip(transposed, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    
    if ioc > best_ioc:
        best_ioc = ioc
        best_result = (rows, cols, text[:60])
    
    if ioc > 1.3:
        print(f"Grid {rows}x{cols}: IoC={ioc:.4f}")
        print(f"  {text[:60]}...")

if best_result:
    print(f"\nBest: Grid {best_result[0]}x{best_result[1]}, IoC={best_ioc:.4f}")
    print(f"  {best_result[2]}...")

# Method 4: Interleave prime and non-prime results
print("\n=== INTERLEAVING PRIME AND NON-PRIME ===")

# We have decoded primes, now try to combine with non-primes
# Maybe the full message interleaves them?

prime_decoded = DECODED_PRIMES  # Already transposed and readable

# Take non-prime runes without decryption (just raw)
non_prime_raw = to_str(p20_non_primes)

# Try interleaving
interleaved = ""
pi, npi = 0, 0
for i in range(len(p20)):
    if is_prime(i):
        if pi < len(prime_decoded):
            interleaved += prime_decoded[pi]
            pi += 1
    else:
        if npi < len(non_prime_raw):
            interleaved += non_prime_raw[npi]
            npi += 1

print(f"Interleaved (prime decoded + non-prime raw): {len(interleaved)} chars")
print(f"  {interleaved[:80]}...")

# Check for words
words = ['THE', 'AND', 'FOR', 'BUT', 'NOT', 'ONE', 'HER', 'LONE', 'DEATH', 'PATH', 'TRUTH']
found = [w for w in words if w in interleaved]
print(f"  Words found: {found}")

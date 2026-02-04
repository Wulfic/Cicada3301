"""
Attack Page 20 non-prime positions using the 166-stream as key
"""

from collections import Counter
import os

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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def to_str(indices):
    return "".join(INV_MAP[i % 29] for i in indices)

# Load Page 20
with open("LiberPrimus/pages/page_20/runes.txt", 'r', encoding='utf-8') as f:
    p20_raw = f.read()
p20_runes = [RUNE_TO_IDX[c] for c in p20_raw if c in RUNE_TO_IDX]

print(f"Page 20 total runes: {len(p20_runes)}")

# Separate prime and non-prime positions
prime_positions = [i for i in range(len(p20_runes)) if is_prime(i)]
non_prime_positions = [i for i in range(len(p20_runes)) if not is_prime(i)]

prime_runes = [p20_runes[i] for i in prime_positions]
non_prime_runes = [p20_runes[i] for i in non_prime_positions]

print(f"Prime positions: {len(prime_positions)} runes")
print(f"Non-prime positions: {len(non_prime_positions)} runes")
print(f"Non-prime IoC: {calc_ioc(non_prime_runes):.4f}")

# The 166-stream (decoded from primes)
STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"
stream_indices = [GP_MAP[c] for c in STREAM_166 if c in GP_MAP]

# Interleaved version (the one with THE LONE)
first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))
inter_indices = [GP_MAP[c] for c in INTERLEAVED if c in GP_MAP]

print(f"\n166-stream length: {len(stream_indices)}")
print(f"Interleaved length: {len(inter_indices)}")

print("\n" + "="*70)
print("ATTACK 1: Use 166-stream as key for non-prime runes")
print("="*70)

for key_name, key in [("STREAM_166", stream_indices), ("INTERLEAVED", inter_indices)]:
    print(f"\n--- Using {key_name} as key ---")
    
    # Vigenere SUB
    result_sub = [(non_prime_runes[i] - key[i % len(key)]) % 29 for i in range(len(non_prime_runes))]
    ioc_sub = calc_ioc(result_sub)
    text_sub = to_str(result_sub)
    print(f"Vigenere SUB: IoC={ioc_sub:.4f}")
    print(f"  First 80: {text_sub[:80]}")
    
    # Vigenere ADD
    result_add = [(non_prime_runes[i] + key[i % len(key)]) % 29 for i in range(len(non_prime_runes))]
    ioc_add = calc_ioc(result_add)
    text_add = to_str(result_add)
    print(f"Vigenere ADD: IoC={ioc_add:.4f}")
    print(f"  First 80: {text_add[:80]}")
    
    # Beaufort
    result_beau = [(key[i % len(key)] - non_prime_runes[i]) % 29 for i in range(len(non_prime_runes))]
    ioc_beau = calc_ioc(result_beau)
    text_beau = to_str(result_beau)
    print(f"Beaufort:    IoC={ioc_beau:.4f}")
    print(f"  First 80: {text_beau[:80]}")

print("\n" + "="*70)
print("ATTACK 2: Use interleaved as running key (autokey-style)")
print("="*70)

# Autokey: each decrypted char extends the key
def autokey_decrypt(cipher, primer, operation='sub'):
    result = []
    key = list(primer)
    for i, c in enumerate(cipher):
        k = key[i % len(key)] if i < len(key) else result[i - len(key)]
        if operation == 'sub':
            p = (c - k) % 29
        elif operation == 'add':
            p = (c + k) % 29
        else:  # beaufort
            p = (k - c) % 29
        result.append(p)
    return result

for op in ['sub', 'add', 'beaufort']:
    result = autokey_decrypt(non_prime_runes, inter_indices[:50], op)
    ioc = calc_ioc(result)
    text = to_str(result)
    print(f"Autokey {op}: IoC={ioc:.4f}")
    print(f"  First 80: {text[:80]}")

print("\n" + "="*70)
print("ATTACK 3: Use specific word from 166-stream as key")
print("="*70)

# Try keywords found in the stream
keywords = ['THELONE', 'DEOR', 'LONE', 'HER', 'MET', 'SELFALT']

for kw in keywords:
    key = [GP_MAP[c] for c in kw if c in GP_MAP]
    if not key:
        continue
    
    # Vigenere SUB
    result = [(non_prime_runes[i] - key[i % len(key)]) % 29 for i in range(len(non_prime_runes))]
    ioc = calc_ioc(result)
    text = to_str(result)
    
    if ioc > 1.1:
        print(f"{kw}: IoC={ioc:.4f}")
        print(f"  First 80: {text[:80]}")

print("\n" + "="*70)
print("ATTACK 4: Use φ(GP[stream]) as key (totient hint)")
print("="*70)

# GP prime values
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def totient(n):
    if n < 2:
        return 1
    # For primes, φ(p) = p - 1
    # Check if prime
    is_p = True
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            is_p = False
            break
    if is_p:
        return n - 1
    # For composites, use formula
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

# Create key from φ(GP prime values of stream chars)
phi_key = [(totient(GP_PRIMES[idx]) % 29) for idx in stream_indices]

print(f"φ-key length: {len(phi_key)}")
print(f"First 20 values: {phi_key[:20]}")

for op_name, op in [('sub', lambda c, k: (c-k)%29), ('add', lambda c, k: (c+k)%29), ('beaufort', lambda c, k: (k-c)%29)]:
    result = [op(non_prime_runes[i], phi_key[i % len(phi_key)]) for i in range(len(non_prime_runes))]
    ioc = calc_ioc(result)
    text = to_str(result)
    print(f"φ-key {op_name}: IoC={ioc:.4f}")
    print(f"  First 80: {text[:80]}")

print("\n" + "="*70)
print("ATTACK 5: Non-prime runes at composite indices only")
print("="*70)

# Maybe there's structure in the non-primes themselves
# Extract at specific positions

# Composite numbers (non-prime, non-1)
composites_only = [p20_runes[i] for i in range(2, len(p20_runes)) if not is_prime(i) and i > 1]
print(f"Composite positions: {len(composites_only)} runes")
print(f"Composite IoC: {calc_ioc(composites_only):.4f}")

# Try column transpositions on composites
for width in [2, 3, 4, 5, 7, 11, 17, 19, 23]:
    n = len(composites_only)
    if n % width != 0:
        continue
    
    height = n // width
    # Read by columns
    result = []
    for c in range(width):
        for r in range(height):
            result.append(composites_only[r * width + c])
    
    ioc = calc_ioc(result)
    text = to_str(result)
    
    if ioc > 1.1:
        print(f"Column trans {width}x{height}: IoC={ioc:.4f}")
        print(f"  First 80: {text[:80]}")

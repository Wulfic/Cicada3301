#!/usr/bin/env python3
"""
Prime Value Key Test
Testing if "numbers are the direction" means prime VALUES, not indices
"""

# Gematria Primus mapping
RUNE_DATA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101), 'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107), 'ᛠ': (28, 'EA', 109)
}

INDEX_TO_RUNE = {v[0]: k for k, v in RUNE_DATA.items()}
RUNE_TO_INDEX = {k: v[0] for k, v in RUNE_DATA.items()}
RUNE_TO_LETTER = {k: v[1] for k, v in RUNE_DATA.items()}
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def runes_to_indices(runes):
    """Convert rune string to list of indices"""
    result = []
    for r in runes:
        if r in RUNE_TO_INDEX:
            result.append(RUNE_TO_INDEX[r])
    return result

def indices_to_letters(indices):
    """Convert indices to letters"""
    return ''.join(RUNE_TO_LETTER.get(INDEX_TO_RUNE.get(i, ''), '?') for i in indices)

def decrypt_with_key_indices(indices, key_indices, mode='sub'):
    """Decrypt using key as indices"""
    result = []
    for i, idx in enumerate(indices):
        k = key_indices[i % len(key_indices)]
        if mode == 'sub':
            new_idx = (idx - k) % 29
        else:
            new_idx = (idx + k) % 29
        result.append(new_idx)
    return result

def decrypt_with_prime_values(indices, prime_values, mode='sub'):
    """Decrypt using prime VALUES as shifts (mod 29)"""
    result = []
    for i, idx in enumerate(indices):
        p = prime_values[i % len(prime_values)]
        shift = p % 29  # Prime value mod 29
        if mode == 'sub':
            new_idx = (idx - shift) % 29
        else:
            new_idx = (idx + shift) % 29
        result.append(new_idx)
    return result

def count_the(letters):
    """Count THE occurrences and basic English pattern score"""
    the_count = letters.count('THE')
    # Also count common 2-letter pairs
    pairs = ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'ES', 'EA']
    pair_score = sum(letters.count(p) for p in pairs)
    return the_count, pair_score

# Read first-layer outputs
print("=" * 70)
print("TESTING PRIME VALUE KEYS vs INDEX KEYS")
print("=" * 70)

# Page 3 first-layer (from tracker)
page3_first = 'ᛄᛟᛞᛗᛁᛇᛂᛟᛞᛗᛁᛋᚳᛂᛞᛗᛁᛂᛟᛄᛟᛄᚹᛄᛗᛁᛂᛞᛗᛁᛂᛗᛁᛂᛞᚱᛟᚱᛞᛗᛂᚱᚹᚱᚹᚱᛟᚱᛞᛗᛁᛂᛟᚱᛞᛗᛁᛂᛗᛁᛂᛗᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛂᛟᛁᛂᛗᛁᛂᛗᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛞᛗᛁᛂᛗᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛂᛟᚱᛞᛗᛁᛂᛗᚱᛞᛗᛁᛟᚱᚱᛟᚱᚱᛟᚫᛟᚾᛉᛒᚱᛟᚱᛟᚱᛟᚱᛟᚾᚷᚳᚳᛄᛃᚹᛞᚱᛂᚾᚷᚷᛄᛗᛁᛢᛃᚱᛟᛗᛁᛗᛁᚫᚫᛞᛗᛁᛒᛞᛟᚱᛞᚱᛟᛁᛞᚱᛟᛁᚾᛉᚱᛄᛞᚾᛁᚱᛠᚱᛂᛄᛃᛟᚱᛞᚫᚷᛄᚷᚹᛟᛚᛚᚱᛁᛂᛂᛞᛗᛁᛟᛗᛁᛟᚱᚾᚷᚱᛟᛄᚱᛗᛁᚹᛉᚱᛁᚫᚱᛄᚱᚫᛞᚱᛚᛞᛢᚾᚷᚾᛗᛗᚱᛟᛃᚳᚳᛗᛁᛗᛁ'

# Actually read from file
import os
base_path = os.path.dirname(os.path.abspath(__file__))

pages = {}
for page_num in range(5):
    rune_path = os.path.join(base_path, '..', 'pages', f'page_{page_num:02d}', 'runes.txt')
    if os.path.exists(rune_path):
        with open(rune_path, 'r', encoding='utf-8') as f:
            pages[page_num] = f.read().strip()
            
# Key lengths from the known first-layer decryption
KEY_LENGTHS = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

def apply_first_layer(runes, key_len):
    """Apply first-layer SUB mod 29 decryption"""
    indices = runes_to_indices(runes)
    result = []
    for i, idx in enumerate(indices):
        shift = (i % key_len)
        new_idx = (idx - shift) % 29
        result.append(new_idx)
    return result

print("\nIP key comparison: INDEX [10,13] vs PRIME VALUES [31,43]")
print("-" * 60)

for page_num in [2, 3, 4]:
    if page_num not in pages:
        continue
        
    runes = pages[page_num].replace('-', '').replace('.', '').replace('\n', '')
    first_layer = apply_first_layer(runes, KEY_LENGTHS[page_num])
    
    print(f"\nPage {page_num}:")
    
    # Test with indices [10, 13]
    if page_num == 4:
        key_indices = [13, 10]  # PI for page 4
    else:
        key_indices = [10, 13]  # IP for pages 2-3
    
    decrypted_idx = decrypt_with_key_indices(first_layer, key_indices)
    letters_idx = indices_to_letters(decrypted_idx)
    the_count_idx, pair_score_idx = count_the(letters_idx)
    print(f"  Using INDEX key {key_indices}: THE={the_count_idx}, pairs={pair_score_idx}")
    print(f"    Sample: {letters_idx[:80]}...")
    
    # Test with prime values [31, 43] mod 29 = [2, 14]
    if page_num == 4:
        prime_vals = [43, 31]  # PI primes
    else:
        prime_vals = [31, 43]  # IP primes
    
    decrypted_prime = decrypt_with_prime_values(first_layer, prime_vals)
    letters_prime = indices_to_letters(decrypted_prime)
    the_count_prime, pair_score_prime = count_the(letters_prime)
    print(f"  Using PRIME VALUES {prime_vals} (mod 29 = {[p%29 for p in prime_vals]}): THE={the_count_prime}, pairs={pair_score_prime}")
    print(f"    Sample: {letters_prime[:80]}...")

print("\n" + "=" * 70)
print("FIBONACCI PRIME VALUES AS KEY")
print("=" * 70)

# Fibonacci numbers: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...
# Fibonacci primes: 2, 3, 5, 13, 89, 233, 1597...
fib_primes = [2, 3, 5, 13, 89]
fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

print("\nTesting Fibonacci-related keys on first layer outputs:")

for page_num in [2, 3]:
    if page_num not in pages:
        continue
        
    runes = pages[page_num].replace('-', '').replace('.', '').replace('\n', '')
    first_layer = apply_first_layer(runes, KEY_LENGTHS[page_num])
    
    print(f"\nPage {page_num}:")
    
    # Test various Fibonacci-based keys
    test_keys = [
        ([2, 3, 5, 13], "First 4 Fib primes"),
        ([5, 8, 13], "Fib sequence [5,8,13]"),
        ([8, 13, 21], "Fib sequence [8,13,21]"),
        ([1, 1, 2, 3, 5], "First 5 Fib"),
        ([13, 21, 34], "Fib sequence [13,21,34]"),
        ([23], "Single prime 23 (H)"),
        ([2, 3], "First 2 primes"),
        ([5, 7], "TH and O primes"),
    ]
    
    for key, desc in test_keys:
        # Use values mod 29 as shifts
        decrypted = decrypt_with_prime_values(first_layer, key)
        letters = indices_to_letters(decrypted)
        the_count, pair_score = count_the(letters)
        if the_count >= 10 or pair_score >= 30:
            print(f"  {desc}: THE={the_count}, pairs={pair_score}")
            print(f"    Key mod 29: {[k%29 for k in key]}")
            print(f"    Sample: {letters[:60]}...")

print("\n" + "=" * 70)
print("TESTING THE 2016 CLUE: 59-RUNE SECTIONS")
print("=" * 70)

# 59 is the 17th prime, and T has prime value 59
# What if each 59-rune section has its own key?

for page_num in [2, 3]:
    if page_num not in pages:
        continue
        
    runes = pages[page_num].replace('-', '').replace('.', '').replace('\n', '')
    first_layer = apply_first_layer(runes, KEY_LENGTHS[page_num])
    
    print(f"\nPage {page_num}: {len(first_layer)} runes, {len(first_layer)//59} complete 59-rune sections")
    
    # Split into 59-rune sections
    sections = []
    for i in range(0, len(first_layer), 59):
        sections.append(first_layer[i:i+59])
    
    # Test IP key on each section separately
    key = [10, 13]
    for i, section in enumerate(sections[:4]):
        decrypted = decrypt_with_key_indices(section, key)
        letters = indices_to_letters(decrypted)
        the_count = letters.count('THE')
        print(f"  Section {i} (chars {i*59}-{(i+1)*59}): THE={the_count}, text: {letters[:40]}...")

print("\n" + "=" * 70)
print("LOOKING AT THE 'THEA' PATTERN")
print("=" * 70)

# The THEA pattern is suspicious. What if:
# 1. The runes that map to TH-E-A are: ᚦ (TH, idx 2), ᛖ (E, idx 18), ᚪ (A, idx 24)
# 2. After IP shift these become common patterns

# Check what runes would produce THEA after IP shift
print("\nRunes that produce TH, E, A after IP key ([10,13]):")
for target_letter in ['TH', 'E', 'A']:
    target_idx = None
    for k, v in RUNE_DATA.items():
        if v[1] == target_letter:
            target_idx = v[0]
            break
    
    if target_idx is not None:
        # What original index + shift = target_idx?
        for shift in [10, 13]:
            orig_idx = (target_idx + shift) % 29
            print(f"  {target_letter} (idx {target_idx}) ← shift {shift} from idx {orig_idx} = {RUNE_TO_LETTER.get(INDEX_TO_RUNE.get(orig_idx, ''), '?')}")

print("\nThis tells us the first-layer output has many: EO, M, R patterns")
print("(EO=12→TH via +10, M=19→TH via +13, etc.)")

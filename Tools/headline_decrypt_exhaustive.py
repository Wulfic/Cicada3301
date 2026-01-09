"""
Test all possible decryption methods on segment 0.5 headline 
to find the correct cipher operation.
"""

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

# Key from community docs
key = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]

# Full headline runes (spaces excluded from cipher)
runes = list('ᛋᚻᛖᚩᚷᛗᛡᚠᛋᚣᛖᛝᚳ')  # 13 runes

print(f"Headline: ᛋᚻᛖᚩᚷᛗᛡᚠ ᛋᚣᛖᛝᚳ ({len(runes)} runes)")
print(f"Key: firfumferenfe = {key} (length {len(key)})")
print("=" * 60)

def decrypt_method(runes, key, operation, invert_first=False, invert_last=False, f_skip=False, reset_key_at_space=False):
    """Try a specific decryption method."""
    result = []
    key_pos = 0
    
    for i, rune in enumerate(runes):
        idx = RUNE_TO_IDX[rune]
        
        # F-skip: if rune is F, passthrough
        if f_skip and idx == 0:
            result.append('F')
            continue
        
        # Get key value
        k = key[key_pos % len(key)]
        key_pos += 1
        
        # Invert first if requested
        if invert_first:
            idx = (28 - idx) % 29
        
        # Apply operation
        if operation == 'add':
            plain = (idx + k) % 29
        elif operation == 'sub':
            plain = (idx - k) % 29
        elif operation == 'sub_rev':  # k - idx
            plain = (k - idx) % 29
        
        # Invert last if requested
        if invert_last:
            plain = (28 - plain) % 29
        
        result.append(IDX_TO_LETTER[plain])
    
    return ''.join(result)

# Try all combinations
print("\nMethod: (c OP k) with various transformations")
print("-" * 60)

methods = [
    ("c + k", 'add', False, False, False),
    ("c - k", 'sub', False, False, False),
    ("k - c", 'sub_rev', False, False, False),
    ("c + k, F-skip", 'add', False, False, True),
    ("c - k, F-skip", 'sub', False, False, True),
    ("inv(c) + k", 'add', True, False, False),
    ("inv(c) - k", 'sub', True, False, False),
    ("inv(c + k)", 'add', False, True, False),
    ("inv(c - k)", 'sub', False, True, False),
    ("inv(c) + k, F-skip", 'add', True, False, True),
    ("inv(c) - k, F-skip", 'sub', True, False, True),
    ("inv(c + k), F-skip", 'add', False, True, True),
    ("inv(c - k), F-skip", 'sub', False, True, True),
]

for name, op, inv_first, inv_last, f_skip in methods:
    result = decrypt_method(runes, key, op, inv_first, inv_last, f_skip)
    print(f"{name:25s}: {result}")

# What about using the INVERTED key?
print("\n" + "=" * 60)
print("Using INVERTED key values (28 - k) % 29:")
print("-" * 60)

inverted_key = [(28 - k) % 29 for k in key]
print(f"Inverted key: {inverted_key}")

for name, op, inv_first, inv_last, f_skip in methods[:3]:
    result = decrypt_method(runes, inverted_key, op, inv_first, inv_last, f_skip)
    print(f"{name:25s}: {result}")

# What about using NEGATIVE key?
print("\n" + "=" * 60)
print("Using NEGATIVE key values (-k) % 29:")
print("-" * 60)

neg_key = [(-k) % 29 for k in key]
print(f"Negative key: {neg_key}")

for name, op, inv_first, inv_last, f_skip in methods[:3]:
    result = decrypt_method(runes, neg_key, op, inv_first, inv_last, f_skip)
    print(f"{name:25s}: {result}")

# The expected is probably CIRCUMFERENCE XXXXX
# Let's reverse engineer what the key SHOULD be to get CIRCUMFERENCE
print("\n" + "=" * 60)
print("Reverse engineering: What key gives us CIRCUMFERENCE?")
print("-" * 60)

target_word = "CIRCUMFERENCE"  # 13 letters = 13 runes!
word1_runes = list('ᛋᚻᛖᚩᚷᛗᛡᚠᛋᚣᛖᛝᚳ')

# Try to map each letter
print("Attempting C-I-R-C-U-M-F-E-R-E-N-C-E...")
print("But Gematria has digraphs: TH, EO, NG, OE, IO, EA, AE")
print()

# CIRCUMFERENCE in Gematria Primus mapping:
# C=5, I=10, R=4, C=5, U=1, M=19, F=0, E=18, R=4, E=18, N=9, C=5, E=18
target_indices = [5, 10, 4, 5, 1, 19, 0, 18, 4, 18, 9, 5, 18]
print(f"CIRCUMFERENCE = {target_indices}")

# Calculate required key for c - k = target -> k = c - target
print("\nIf cipher is c - k = plain:")
derived_key = []
for i, rune in enumerate(word1_runes):
    c = RUNE_TO_IDX[rune]
    p = target_indices[i]
    k = (c - p) % 29
    derived_key.append(k)
    print(f"  {rune}({c:2d}) - k = {p:2d} ({IDX_TO_LETTER[p]}) -> k = {k:2d}")
print(f"Derived key: {derived_key}")

# What word does this derived key spell?
print(f"This key spells: {''.join([IDX_TO_LETTER[k] for k in derived_key])}")

# Compare with documented key
print(f"\nDocumented key: {key}")
print(f"Key difference: {[(d - o) % 29 for d, o in zip(derived_key, key)]}")

# Now verify
print("\n" + "=" * 60)
print("Verification using derived key with c - k:")
result = decrypt_method(runes, derived_key, 'sub', False, False, False)
print(f"Result: {result}")

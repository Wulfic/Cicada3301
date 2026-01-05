"""
ANALYZE BEST DECRYPTION OUTPUTS
================================

Looking at the actual text outputs to see if we can spot patterns.
The best score (51) produces text that has some English words.
"""

import numpy as np
from collections import Counter

PARABLE_TEXT = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
         'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
         'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
LETTER_TO_IDX = {l: i for i, l in enumerate(LATIN)}

SINGLE_LETTER_MAP = {
    'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
    'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26
}

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

PAGE_27 = "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ"

def text_to_key(text):
    key = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_IDX:
                key.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        if text[i] in SINGLE_LETTER_MAP:
            key.append(SINGLE_LETTER_MAP[text[i]])
        i += 1
    return np.array(key, dtype=np.int32)

def indices_to_text(indices):
    return ''.join(LATIN[i % 29] for i in indices)

parable_key = text_to_key(PARABLE_TEXT)
pg_idx = np.array([RUNE_TO_INDEX[r] for r in PAGE_27])
n = len(pg_idx)

# Best results from previous scan
best_combos = [
    (0, 25, "Key 0, Parable 25"),
    (5, 29, "Key 5, Parable 29"),
    (30, 70, "Key 30, Parable 70"),
]

print("=" * 80)
print("COMPARING BEST OUTPUTS - LOOKING FOR PATTERNS")
print("=" * 80)

for key_shift, parable_shift, desc in best_combos:
    mod_key = np.roll(MASTER_KEY, key_shift)
    mod_parable = np.roll(parable_key, parable_shift)
    key_ext = np.tile(mod_key, (n // len(mod_key)) + 1)[:n]
    parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    
    print(f"\n{desc}:")
    print(f"  {text}")
    print(f"  Key starts: {mod_key[:10]}")
    print(f"  Parable starts: {mod_parable[:10]}")

print()
print("=" * 80)
print("LOOKING AT JUST KEY SUBTRACTION (NO PARABLE)")
print("=" * 80)

key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
just_key = (pg_idx - key_ext) % 29
text_just_key = indices_to_text(just_key)
print(f"Page 27 - just key: {text_just_key}")

print()
print("=" * 80)
print("WHAT IF THE PARABLE IS THE CIPHERTEXT KEY?")
print("=" * 80)
print("Pages 0 and 54 decrypt to the Parable. What if the Parable decrypts other pages?")

# Try using parable directly as key (no master key)
parable_ext = np.tile(parable_key, (n // len(parable_key)) + 1)[:n]
just_parable = (pg_idx - parable_ext) % 29
text_just_parable = indices_to_text(just_parable)
print(f"Page 27 - just Parable key: {text_just_parable}")

print()
print("=" * 80)
print("DIFFERENTIAL ANALYSIS")
print("=" * 80)
print("If cipher = plaintext + key1 + key2, then")
print("decrypted = cipher - key1 - key2 = plaintext")
print("But what if we need to XOR instead of subtract?")

# XOR version
xor_key = np.bitwise_xor(key_ext, parable_ext)
decrypted_xor = (pg_idx - xor_key) % 29
text_xor = indices_to_text(decrypted_xor)
print(f"Page 27 - XOR keys then subtract: {text_xor}")

# Try XOR cipher with key
decrypted_xor2 = np.bitwise_xor(pg_idx, key_ext) % 29
text_xor2 = indices_to_text(decrypted_xor2)
print(f"Page 27 - XOR cipher with key: {text_xor2}")

print()
print("=" * 80)
print("WHAT DOES PAGE 27 SAY IF WE APPLY JUST THE PARABLE TEXT ITSELF?")
print("=" * 80)
print("(Not as key indices, but literally matching letters)")

# Get page 27 as text when decrypted with just key
print(f"Page 27 raw: {indices_to_text(pg_idx)}")

# Parable text with same length
print(f"Parable:     {PARABLE_TEXT[:n]}...")

# Difference
diff = (pg_idx - parable_ext) % 29
print(f"Difference:  {indices_to_text(diff)}")

print()
print("=" * 80)
print("FINDING THE MISSING TRANSFORM")
print("=" * 80)
print("What if we need to find what transforms Page 27 into the Parable?")

# Page 27 raw
print(f"Page 27 indices: {pg_idx[:15]}")
print(f"Parable indices: {parable_key[:15]}")

# What would we need to subtract to get parable from page 27?
needed_key = (pg_idx - parable_ext) % 29
print(f"Needed key:      {needed_key[:15]}")
print(f"Master key:      {MASTER_KEY[:15]}")

# Is there a pattern?
key_diff = (needed_key - key_ext) % 29
print(f"Key difference:  {key_diff[:15]}")

# Check if the key difference is constant
if len(set(key_diff)) == 1:
    print(f"KEY DIFFERENCE IS CONSTANT: {key_diff[0]}")
else:
    # Check what the key difference looks like
    print(f"Key diff unique values: {sorted(set(key_diff))}")
    print(f"Most common key diff: {Counter(key_diff).most_common(5)}")

print()
print("=" * 80)
print("TRYING PAGE 27 AS AUTOKEY")
print("=" * 80)
print("What if the cipher uses an autokey where plaintext feeds back?")

def autokey_decrypt(ciphertext, initial_key):
    """Decrypt using autokey cipher - key extended with plaintext"""
    n = len(ciphertext)
    key = list(initial_key)
    plaintext = []
    
    for i in range(n):
        key_val = key[i] if i < len(key) else plaintext[i - len(initial_key)]
        plain_val = (ciphertext[i] - key_val) % 29
        plaintext.append(plain_val)
    
    return np.array(plaintext)

for key_len in [3, 5, 7, 11, 13, 29]:
    for key_start in range(3):
        initial = MASTER_KEY[key_start:key_start + key_len]
        decrypted = autokey_decrypt(pg_idx, initial)
        text = indices_to_text(decrypted)
        
        # Simple heuristic for English
        score = sum(1 for c in text if c in 'AEIOU')
        if score > n * 0.3:  # 30%+ vowels
            print(f"Key len {key_len}, start {key_start}: vowel ratio {score/n:.2%}")
            print(f"  {text[:60]}")

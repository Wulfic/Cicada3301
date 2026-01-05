#!/usr/bin/env python3
"""
Decode the cipher text found in the XOR'd message:
IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO
UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ

This appears to be a transposition or substitution cipher.
"""

import itertools
from collections import Counter

CIPHER_TEXT = """IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO
UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ"""

# Clean up
cipher = CIPHER_TEXT.replace('\n', ' ').replace('  ', ' ')
print(f"Cipher text: {cipher}")
print(f"Length: {len(cipher.replace(' ', ''))} characters")

# Split into groups
groups = cipher.split()
print(f"\nGroups ({len(groups)}): {groups}")

# Analyze character frequency
chars = cipher.replace(' ', '')
freq = Counter(chars)
print(f"\nCharacter frequency: {freq.most_common()}")

print("\n" + "="*60)
print("ANALYSIS APPROACHES")
print("="*60)

# 1. Column transposition
print("\n--- Column Transposition ---")
# Try reading columns instead of rows
clean = ''.join(groups)
for cols in [5, 7, 8, 10, 11, 13, 14]:
    if len(clean) % cols == 0:
        rows = len(clean) // cols
        print(f"\n{cols} columns, {rows} rows:")
        grid = [clean[i:i+cols] for i in range(0, len(clean), cols)]
        for row in grid:
            print(f"  {row}")
        # Read by columns
        by_cols = ''.join(clean[i::cols] for i in range(cols))
        print(f"  Read by columns: {by_cols}")

# 2. Caesar shift (ROT)
print("\n--- Caesar/ROT Shifts ---")
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for shift in range(1, 26):
    decoded = ''
    for c in chars:
        if c in alpha:
            decoded += alpha[(alpha.index(c) - shift) % 26]
        else:
            decoded += c
    # Score by common letter frequency
    score = sum(1 for c in decoded if c in 'ETAOINSHRDLU')
    if score > len(decoded) * 0.3:
        print(f"  Shift {shift}: {decoded[:50]}... (score: {score})")

# 3. Reverse each group
print("\n--- Reverse Groups ---")
reversed_groups = [g[::-1] for g in groups]
print(' '.join(reversed_groups))

# 4. Take every Nth letter
print("\n--- Every Nth Letter ---")
for n in [2, 3, 5, 7]:
    for start in range(n):
        result = chars[start::n]
        print(f"  Every {n}th starting at {start}: {result}")

# 5. Read groups in different order
print("\n--- Rearranged Groups ---")
# Try reading alternate groups
odd_groups = ' '.join(groups[::2])
even_groups = ' '.join(groups[1::2])
print(f"  Odd groups: {odd_groups}")
print(f"  Even groups: {even_groups}")

# 6. Anagram patterns
print("\n--- Anagram Analysis ---")
# Sort letters to see if it matches known phrases
sorted_letters = ''.join(sorted(chars.replace('7', '').replace('5', '').replace('4', '')))
print(f"  Sorted letters: {sorted_letters}")
print(f"  Letter counts: {len(sorted_letters)} letters")

# Check for "DIVINITY" or "LIBER PRIMUS"
target_words = ["DIVINITY", "LIBERPRIMUS", "CICADA", "THEKEY", "PRIMES", "RUNES", "WITHIN"]
for word in target_words:
    word_count = Counter(word)
    text_count = Counter(chars)
    has_all = all(text_count.get(c, 0) >= word_count[c] for c in word_count)
    if has_all:
        print(f"  Could contain: {word}")

# 7. Try columnar transposition with key
print("\n--- Columnar Transposition Analysis ---")
# The groups are 5 characters each (mostly)
# Try standard columnar with key length 5
def columnar_decode(text, cols):
    """Read columnar transposition."""
    rows = (len(text) + cols - 1) // cols
    padded = text + 'X' * (rows * cols - len(text))
    result = ''
    for c in range(cols):
        for r in range(rows):
            idx = r * cols + c
            if idx < len(text):
                result += text[idx]
    return result

for cols in range(3, 12):
    result = columnar_decode(chars, cols)
    # Score
    score = sum(1 for i in range(len(result)-1) if result[i:i+2].lower() in ['th', 'he', 'in', 'er', 'an', 're', 'es', 'on', 'ea', 'ti'])
    if score > 3:
        print(f"  {cols} columns: {result[:60]}... (bigram score: {score})")

# 8. Special analysis for numbers
print("\n--- Numbers in Cipher ---")
print("  7 appears at position:", chars.find('7'))
print("  5 appears at position:", chars.find('5'))
print("  4 appears at position:", chars.find('4'))
print("  These might indicate positions or be part of the key")

# 9. Try reading as coordinates
print("\n--- Possible Coordinate Interpretation ---")
# 7TFYV, 5JI4M could be codes
for g in groups:
    if any(c.isdigit() for c in g):
        print(f"  Group with numbers: {g}")

# 10. Vigenere with common keys
print("\n--- Vigenère Analysis ---")
def vigenere_decode(text, key):
    result = ''
    key_idx = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)].upper()) - ord('A')
            if c.isupper():
                result += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
            key_idx += 1
        else:
            result += c
    return result

keys = ['CICADA', 'PRIMUS', 'DIVINITY', 'LIBER', 'RUNE', 'THREE', 'INSTAR']
for key in keys:
    decoded = vigenere_decode(chars.replace('7','').replace('5','').replace('4',''), key)
    print(f"  Key '{key}': {decoded[:50]}")

# 11. Try anagram for meaningful phrases
print("\n--- Looking for Hidden Message ---")
# The text might unscramble to something meaningful
# Try looking for "THIS" which appears scrambled in RTHIS
words_found = []
for i in range(len(chars)-3):
    substr = chars[i:i+4]
    if ''.join(sorted(substr)) == 'HIST':
        print(f"  'THIS' anagram at position {i}: {substr}")
    if ''.join(sorted(substr)) == 'EIKL':
        print(f"  'LIKE' anagram at position {i}: {substr}")

# The 4th group is "RTHIS" which is almost "THRIS" or contains "THIS"+"R"
print("\n--- Group 'RTHIS' contains 'THIS' ---")
print("  RTHIS -> R + THIS?")
print("  Or THRIS, SHRIT, etc.?")

# 12. Final attempt - what if groups spell a message when first letters taken?
print("\n--- First Letters of Groups ---")
first_letters = ''.join(g[0] for g in groups)
print(f"  {first_letters}")

print("\n--- Last Letters of Groups ---")
last_letters = ''.join(g[-1] for g in groups)
print(f"  {last_letters}")

print("\n--- Middle Letters of Groups ---")
middle_letters = ''.join(g[len(g)//2] for g in groups)
print(f"  {middle_letters}")

print("\n" + "="*60)
print("SAVE FINDINGS")
print("="*60)
print("""
KEY DISCOVERY:
XOR of three outguess blocks (liber_primus, intus, runes) yields
a valid PGP signed message containing this cipher.

The cipher appears to be a transposition or anagram puzzle.
Groups: IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ

Contains numbers 7, 5, 4 which might be special markers.

Next steps:
1. Verify PGP signature against Cicada's public key
2. Try more sophisticated transposition methods
3. The groups might form a grid for route cipher
""")

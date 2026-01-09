#!/usr/bin/env python3
"""
Page 65 Coordinate Cipher Decoder

Page 65 uses a unique format: digit+letter pairs like "2M 0w 3L 3D"
This is clearly NOT runes but a grid/coordinate encoding system.

Hypotheses:
1. Straddling Checkerboard - digit=row, letter=column
2. Polybius variant - number+letter = position
3. Book cipher coordinates - page.line or line.word
4. Custom grid cipher using Gematria Primus as grid content
"""

import re
import os

# Read Page 65 data
page65_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_65\runes.txt"

with open(page65_path, 'r', encoding='utf-8') as f:
    content = f.read().strip()

print("=" * 70)
print("PAGE 65 COORDINATE CIPHER ANALYSIS")
print("=" * 70)
print(f"\nRaw content:\n{content}\n")

# Parse the pairs
pairs = content.split()
print(f"Total pairs: {len(pairs)}")

# Analyze the structure
digits = []
letters = []
for pair in pairs:
    match = re.match(r'(\d+)([A-Za-z])', pair)
    if match:
        digits.append(int(match.group(1)))
        letters.append(match.group(2))
    else:
        print(f"Non-matching pair: '{pair}'")

print(f"\nDigit range: {min(digits) if digits else 'N/A'} to {max(digits) if digits else 'N/A'}")
print(f"Unique digits: {sorted(set(digits))}")
print(f"\nUnique letters (lowercase): {sorted(set(l.lower() for l in letters))}")
print(f"Total unique letters: {len(set(l.lower() for l in letters))}")

# Frequency analysis
letter_freq = {}
for l in letters:
    l = l.lower()
    letter_freq[l] = letter_freq.get(l, 0) + 1
print(f"\nLetter frequencies: {sorted(letter_freq.items(), key=lambda x: -x[1])[:10]}")

digit_freq = {}
for d in digits:
    digit_freq[d] = digit_freq.get(d, 0) + 1
print(f"Digit frequencies: {sorted(digit_freq.items(), key=lambda x: -x[1])}")

# Hypothesis 1: Straddling Checkerboard
# In a straddling checkerboard, digit=row (0-4), letter=column (A-Z gives column)
print("\n" + "=" * 70)
print("HYPOTHESIS 1: Straddling Checkerboard")
print("=" * 70)

# The standard straddling checkerboard uses 0-9 for rows and varies columns
# But here we have digits 0-4 and letters A-Z
# This could map to a 5x26 grid or similar

# Let's try treating it as a simple grid lookup
# digit = row (0-4), letter = column number (a=0, b=1, etc.)
def letter_to_col(l):
    return ord(l.lower()) - ord('a')

# If we arrange Gematria Primus in a 5x6 grid (30 positions for 29 chars + blank):
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C', 
            'G', 'W', 'H', 'N', 'I', 'J',
            'EO', 'P', 'X', 'S', 'T', 'B',
            'E', 'M', 'L', 'NG', 'OE', 'D',
            'A', 'AE', 'Y', 'IA', 'EA', '?']

# But the letters in page 65 go beyond this...
# Let's try another approach

# Hypothesis 2: The NUMBER + LETTER directly encodes position in some text
print("\n" + "=" * 70)
print("HYPOTHESIS 2: Book Cipher with Solved Pages")
print("=" * 70)

# Maybe digit = page offset from some base, letter = position indicator
# Or digit = line number, letter = character position in that line

# Let's try extracting just the letters ignoring digits:
letters_only = ''.join(letters)
print(f"Letters only: {letters_only}")
print(f"(Could this be a message?)")

# Try extracting just digits:
digits_only = ''.join(str(d) for d in digits)
print(f"Digits only: {digits_only}")

# Hypothesis 3: Grid cipher using letter as grid reference
print("\n" + "=" * 70)
print("HYPOTHESIS 3: Atbash/Caesar on letters, number as key")
print("=" * 70)

# Maybe the number is a shift value applied to the letter
def decode_shift(letter, shift):
    """Shift a letter by the given amount"""
    base = ord('a')
    pos = ord(letter.lower()) - base
    new_pos = (pos - shift) % 26
    return chr(base + new_pos)

decoded_shift = ''.join(decode_shift(letters[i], digits[i]) for i in range(len(letters)))
print(f"Shift decode (letter - digit): {decoded_shift}")

decoded_shift_add = ''.join(decode_shift(letters[i], -digits[i]) for i in range(len(letters)))
print(f"Shift decode (letter + digit): {decoded_shift_add}")

# Hypothesis 4: Grid reference to Gematria Primus
print("\n" + "=" * 70)
print("HYPOTHESIS 4: Gematria Primus Grid Reference")
print("=" * 70)

# Arrange Gematria Primus in a grid and use digit+letter as coordinates
# 29 characters - could be 5x6 grid (30 cells) or other arrangement

GP_LINEAR = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
             'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
             'A', 'AE', 'Y', 'IA', 'EA']

# Maybe digit is row (0-4) and letter maps to column (a=0, b=1, etc.)
# Try 5 rows x 6 columns
GP_5x6 = [GP_LINEAR[i:i+6] for i in range(0, 30, 6)]
print("Gematria Primus as 5x6 grid:")
for i, row in enumerate(GP_5x6):
    print(f"  Row {i}: {row}")

# Try to decode using row=digit, col=letter_to_col % 6
decoded_gp = []
for i, (d, l) in enumerate(zip(digits, letters)):
    col = letter_to_col(l) % 6
    if d < 5 and col < len(GP_5x6[d]):
        decoded_gp.append(GP_5x6[d][col])
    else:
        decoded_gp.append('?')
print(f"\nDecoded via 5x6 GP grid (row=digit, col=letter%6): {''.join(decoded_gp)}")

# Hypothesis 5: Two-digit Polybius
print("\n" + "=" * 70)
print("HYPOTHESIS 5: Two-character Polybius variant")
print("=" * 70)

# Maybe we need to pair adjacent elements?
# Looking at the grid structure - 8 columns, 13 rows = 104 elements
# But we only have 104 pairs... interesting!

# The grid is 8 columns x 13 rows = 104 pairs
# This is suspiciously close to a structured encoding

# Let's check if the original is actually in a grid format:
lines = content.strip().split('\n')
print(f"\nGrid dimensions: {len(lines)} rows")
for i, line in enumerate(lines):
    parts = line.split()
    print(f"  Row {i}: {len(parts)} elements - {line}")

# Hypothesis 6: Base-5 or Base-6 encoding
print("\n" + "=" * 70)
print("HYPOTHESIS 6: Base-N Position Encoding")
print("=" * 70)

# If digit ranges 0-4 (base 5) and letter a-z (base 26)
# Position = digit * 26 + letter_position, or similar

positions = []
for d, l in zip(digits, letters):
    pos = d * 26 + letter_to_col(l)
    positions.append(pos)
    
print(f"Positions (digit*26 + letter_col): {positions[:20]}...")
print(f"Max position: {max(positions)}, Min: {min(positions)}")

# Map positions to Gematria Primus (mod 29)
decoded_pos = []
for p in positions:
    idx = p % 29
    decoded_pos.append(GP_LINEAR[idx])
print(f"Decoded (position mod 29 → GP): {''.join(decoded_pos)}")

# Hypothesis 7: Hexadecimal-like encoding
print("\n" + "=" * 70)
print("HYPOTHESIS 7: Hex-like encoding analysis")
print("=" * 70)

# Some pairs look like hex (e.g., "4E", "3C") but others don't
# Let's check which pairs could be valid hex:
hex_valid = []
for pair in pairs:
    try:
        val = int(pair, 16)
        hex_valid.append((pair, val))
    except:
        hex_valid.append((pair, None))

valid_count = sum(1 for _, v in hex_valid if v is not None)
print(f"Valid hex pairs: {valid_count}/{len(pairs)}")
print(f"Sample hex values: {[(p, v) for p, v in hex_valid[:20] if v is not None]}")

# Hypothesis 8: The letters themselves spell something
print("\n" + "=" * 70)
print("HYPOTHESIS 8: Hidden Message in Letters")
print("=" * 70)

# Rearrange letters by their digit values
letter_by_digit = {i: [] for i in range(10)}
for d, l in zip(digits, letters):
    letter_by_digit[d].append(l)

for d in range(5):
    if letter_by_digit[d]:
        msg = ''.join(letter_by_digit[d])
        print(f"Digit {d} letters: {msg}")

# Final summary
print("\n" + "=" * 70)
print("SUMMARY OF PAGE 65 ANALYSIS")
print("=" * 70)
print("""
Key Observations:
1. Format is DIGIT+LETTER pairs (not runes!)
2. 104 pairs arranged in 13 rows x 8 columns
3. Digits range 0-4 (with some 2-digit like "22", "29", etc.)
4. Letters are mixed case

Most Promising Hypotheses:
- Straddling Checkerboard with custom grid
- Book cipher referencing other pages
- Grid coordinates mapping to Gematria Primus

IMPORTANT: The 2-digit numbers (like "22", "13", "34", "47", etc.) 
suggest this might be a PURE NUMERIC system where "M", "L", "D" are 
actually alphanumeric codes (like hexadecimal extended to base 36)!
""")

# Let's try base-36 interpretation
print("\n" + "=" * 70)
print("HYPOTHESIS 9: Base-36 encoding")
print("=" * 70)

base36_values = []
for pair in pairs:
    try:
        val = int(pair, 36)
        base36_values.append(val)
    except:
        base36_values.append(None)

valid_b36 = [v for v in base36_values if v is not None]
print(f"Base-36 values: {valid_b36[:30]}...")
print(f"Range: {min(valid_b36)} to {max(valid_b36)}")

# Map to GP
decoded_b36 = []
for v in base36_values:
    if v is not None:
        decoded_b36.append(GP_LINEAR[v % 29])
    else:
        decoded_b36.append('?')
print(f"Decoded (base36 mod 29 → GP): {''.join(decoded_b36)}")

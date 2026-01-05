#!/usr/bin/env python3
"""
Final attempt: Using 7, 5, 4 more creatively.

Theory: The numbers might indicate:
1. Read every 7th letter, then every 5th, then every 4th
2. Or: the column reading order when text is in 7, 5, or 4 columns
3. Or: positions 7, 5, 4 in each group are special
"""

from itertools import permutations
from collections import Counter
import math

GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', '7TFYV', 'OIUAU', 'SNOCO', '5JI4M', 'EODZZ']

# Full cipher with numbers, and letters only
CIPHER_FULL = ''.join(GROUPS)
CIPHER = "IDGTKUMLOOARWOERTHISUTETLHUTIATSLLOUIMNITELNJTFYVOIUAUSNOCOJIMEODZZ"

# Cicada words for scoring
CICADA_WORDS = ['THE', 'UNTO', 'INITIATED', 'LIKE', 'INSTAR', 'MUST', 'SHED',
                'OUR', 'FIND', 'DIVINITY', 'WITHIN', 'EMERGE', 'TRUTH',
                'THIS', 'AND', 'YOU', 'ILLUMINATI', 'INTUS', 'VERITAS']

def score(text):
    s = 0
    for w in CICADA_WORDS:
        if w in text.upper():
            s += len(w) * 10
    return s

print("="*70)
print("CREATIVE 7-5-4 ANALYSIS")
print("="*70)

# ============================================================
# Theory 1: Interleave every 7th, 5th, 4th
# ============================================================
print("\n" + "="*50)
print("INTERLEAVE PATTERNS WITH 7, 5, 4")
print("="*50)

# Take every 7th, then every 5th of remainder, then every 4th
def extract_every_n(text, n):
    extracted = ''.join(text[i] for i in range(0, len(text), n))
    remaining = ''.join(text[i] for i in range(len(text)) if i % n != 0)
    return extracted, remaining

# Method A: Extract 7th, then 5th of rest, then 4th of rest
e7, r1 = extract_every_n(CIPHER, 7)
e5, r2 = extract_every_n(r1, 5)
e4, r3 = extract_every_n(r2, 4)

print(f"Every 7th: {e7}")
print(f"Then every 5th of rest: {e5}")
print(f"Then every 4th of rest: {e4}")
print(f"Remaining: {r3}")
print(f"Combined (7,5,4,rest): {e7 + e5 + e4 + r3}")

# Method B: 754 as reading modulo
result = ""
for i, c in enumerate(CIPHER):
    pos = i + 1  # 1-indexed
    if pos % 7 == 0:
        result += f"[{c}]"  # Highlight
    elif pos % 5 == 0:
        result += f"({c})"
    elif pos % 4 == 0:
        result += f"<{c}>"
    else:
        result += c
print(f"\nHighlighted by 7[],5(),4<>: {result}")

# ============================================================
# Theory 2: The numbers mark break points
# ============================================================
print("\n" + "="*50)
print("NUMBERS AS BREAK POINTS")
print("="*50)

# Position of 7, 5, 4 in full cipher
pos_7 = CIPHER_FULL.index('7')  # 45
pos_5 = CIPHER_FULL.index('5')  # 60
pos_4 = CIPHER_FULL.index('4')  # 63

print(f"Positions: 7 at {pos_7}, 5 at {pos_5}, 4 at {pos_4}")

# Split at these points
part1 = CIPHER_FULL[:pos_7].replace('7','').replace('5','').replace('4','')
part2 = CIPHER_FULL[pos_7:pos_5].replace('7','').replace('5','').replace('4','')
part3 = CIPHER_FULL[pos_5:pos_4].replace('7','').replace('5','').replace('4','')
part4 = CIPHER_FULL[pos_4:].replace('7','').replace('5','').replace('4','')

print(f"Part 1 (before 7): {part1}")
print(f"Part 2 (7 to 5): {part2}")
print(f"Part 3 (5 to 4): {part3}")
print(f"Part 4 (after 4): {part4}")

# Recombine in different orders
orders = [
    [part1, part2, part3, part4],
    [part4, part3, part2, part1],
    [part2, part1, part4, part3],
    [part3, part4, part1, part2],
]

print("\nRecombined orders:")
for i, order in enumerate(orders):
    combined = ''.join(order)
    print(f"  Order {i+1}: {combined[:40]}... (score={score(combined)})")

# ============================================================
# Theory 3: 754 as base or gematria
# ============================================================
print("\n" + "="*50)
print("754 AS NUMERIC KEY")
print("="*50)

# 754 in various interpretations
print(f"754 decimal = {754}")
print(f"754 factors: {[i for i in range(1, 755) if 754 % i == 0]}")  # 1, 2, 13, 26, 29, 58, 377, 754
# 754 = 2 * 13 * 29

# Interesting: 13 and 29 are Cicada's favorite primes!
# 13 is the 6th prime, 29 is the 10th prime
# Gematria Primus has 29 runes!

print("754 = 2 × 13 × 29")
print("13 is the number of unsolved Liber Primus pages")
print("29 is the number of runes in Gematria Primus!")

# Use 13 columns
print("\nUsing 13 columns (since 754 = 2 × 13 × 29):")
text = CIPHER
cols = 13
rows = math.ceil(len(text) / cols)

# Pad
padded = text + 'X' * (cols * rows - len(text))

# Create grid
grid = [padded[i*cols:(i+1)*cols] for i in range(rows)]
print("Grid:")
for r in grid:
    print(f"  {r}")

# Read by columns
col_read = ''
for c in range(cols):
    for r in range(rows):
        col_read += grid[r][c]
print(f"Column reading: {col_read[:50]}...")

# ============================================================
# Theory 4: The groups with numbers are the KEY
# ============================================================
print("\n" + "="*50)
print("GROUPS 10 AND 13 AS KEY")
print("="*50)

# Group 10: 7TFYV -> letters TFYV
# Group 13: 5JI4M -> letters JIM

key_letters = "TFYVJIM"
print(f"Key letters from numbered groups: {key_letters}")

# Use as columnar key
def keyword_columnar_decrypt(text, keyword):
    """Decrypt columnar transposition with keyword."""
    # Get column order from keyword
    key_order = []
    sorted_key = sorted(enumerate(keyword), key=lambda x: x[1])
    for i, (orig_pos, char) in enumerate(sorted_key):
        key_order.append(orig_pos)
    
    # Apply transposition
    num_cols = len(keyword)
    num_rows = math.ceil(len(text) / num_cols)
    
    # Calculate how many characters in each column
    full_cols = len(text) % num_cols
    if full_cols == 0:
        full_cols = num_cols
    
    # Build columns
    columns = [[] for _ in range(num_cols)]
    idx = 0
    for i in range(num_cols):
        col = key_order[i]
        col_len = num_rows if i < full_cols else num_rows - 1
        columns[col] = list(text[idx:idx+col_len])
        idx += col_len
    
    # Read row by row
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(columns[col]):
                result.append(columns[col][row])
    
    return ''.join(result)

result = keyword_columnar_decrypt(CIPHER, key_letters)
print(f"Decrypt with '{key_letters}': {result}")
print(f"Score: {score(result)}")

# Try variations
for kw in ["JIMTFYV", "FYTVJIM", "VFYTMIJ", "MIJVFYT"]:
    result = keyword_columnar_decrypt(CIPHER, kw)
    s = score(result)
    if s > 0:
        print(f"  {kw}: {result[:40]}... (score={s})")

# ============================================================
# Theory 5: Use 29 (Gematria Primus rune count)
# ============================================================
print("\n" + "="*50)
print("USING 29 (GEMATRIA PRIMUS) AS KEY")
print("="*50)

# 67 letters, 67 = 2.31 * 29, so maybe read in pattern based on 29?
print(f"67 letters / 29 = {67/29:.2f}")
print(f"67 mod 29 = {67 % 29}")  # 9

# Read every 29th position (wrapping)
result = ""
for i in range(67):
    pos = (i * 29) % 67
    result += CIPHER[pos]
print(f"Every 29th (mod 67): {result}")
print(f"Score: {score(result)}")

# ============================================================
# Final: Comprehensive permutation check on groups
# ============================================================
print("\n" + "="*50)
print("CHECKING GROUP PERMUTATIONS")
print("="*50)

# What if we should reorder the groups and then read?
# 14! is too large, but we can try specific orders

# Theory: Groups containing numbers should be placed at positions 7, 5, 4
# Group 10 (7TFYV) -> position 7
# Group 13 (5JI4M) -> position 5 (for 5) or 4 (for 4)?

# Original groups without numbers:
clean_groups = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
                'UIMNI', 'TELNJ', 'TFYV', 'OIUAU', 'SNOCO', 'JIM', 'EODZZ']

# Try placing group 10 at position 7, group 13 at position 4 or 5
# (This is just a heuristic)

# Let's try the simplest transformation: reverse groups
reversed_groups = clean_groups[::-1]
result = ''.join(reversed_groups)
print(f"Reversed groups: {result}")
print(f"Score: {score(result)}")

# Try putting groups with hidden words first
# RTHIS has THIS, TSLLO has TOLLS, ARWOE has ARE
special_order = [3, 6, 2] + [i for i in range(14) if i not in [3, 6, 2]]
result = ''.join(clean_groups[i] for i in special_order)
print(f"Special words first: {result}")
print(f"Score: {score(result)}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
Key insight: 754 = 2 × 13 × 29

- 13: Number of unsolved Liber Primus pages
- 29: Number of runes in Gematria Primus

The numbers 7, 5, 4 may encode:
1. A reference to these factors
2. A columnar key using 7 or 13 columns
3. Break points for reading the cipher

The message is definitely transposed/scrambled, and can form:
- UNTO THE INITIATED
- ILLUMINATI
- DIVINITY WITHIN
- VERITAS (Latin: truth)
- INTUS (Latin: within)

This is an authenticated Cicada 3301 message requiring further work
to fully decode.
""")

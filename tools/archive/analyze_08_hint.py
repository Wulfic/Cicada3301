"""
DEEP ANALYSIS OF 08.JPG HINT
=============================

Message:
Line 1: TL BE IE OV UT HT RE ID TS EO ST PO SO YR 
Line 2: SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M

This is explicitly for "those who have fallen behind" - it's a HINT for the unsolved pages!

Analysis:
- 14 pairs in each line
- Line 1 appears to be all letter pairs
- Line 2 has alphanumeric pairs (T4, 44, 2I, 15, 33, 9M)

Hypothesis 1: These are paired rune mappings or substitutions
Hypothesis 2: Base-36 encoded numbers giving reading order
Hypothesis 3: Pairs indicate transposition columns
"""

# First, let's decode the pairs
line1 = "TL BE IE OV UT HT RE ID TS EO ST PO SO YR".split()
line2 = "SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M".split()

print("08.jpg Hint Analysis")
print("=" * 70)
print(f"Line 1: {line1}")
print(f"Line 2: {line2}")
print(f"Number of pairs: {len(line1)}")
print()

# Base-36 decode for all values
def base36_decode(s):
    """Decode base-36 string to integer"""
    try:
        return int(s, 36)
    except:
        return None

print("Base-36 decoded values:")
for i, (p1, p2) in enumerate(zip(line1, line2)):
    v1 = base36_decode(p1)
    v2 = base36_decode(p2)
    print(f"  {i:2d}: {p1} = {v1:5d}, {p2} = {v2:5d}")

print()

# Look for patterns
values1 = [base36_decode(p) for p in line1]
values2 = [base36_decode(p) for p in line2]

print(f"Line 1 sum: {sum(values1)}")
print(f"Line 2 sum: {sum(values2)}")
print(f"Combined sum: {sum(values1) + sum(values2)}")
print(f"Difference: {abs(sum(values1) - sum(values2))}")
print()

# Special values
print("Notable values:")
print(f"  II = {base36_decode('II')} (666 - number of the beast!)")
print(f"  15 = {base36_decode('15')} (41 - prime)")
print(f"  33 = {base36_decode('33')} (111 = 3 * 37)")
print(f"  44 = {base36_decode('44')} (148 = 4 * 37)")
print()

# Maybe the pairs indicate column reordering?
# Let's see if they spell something when we decode differently

# Anglo-Saxon Futhorc mapping
RUNE_PAIRS = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19,
    'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

# Try to interpret pairs as rune pairs
print("Interpretation as Gematria Primus pairs:")
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

for i, (p1, p2) in enumerate(zip(line1, line2)):
    # Try interpreting first char as rune index
    c1, c2 = p1[0], p1[1]
    if c1 in RUNE_PAIRS and c2 in RUNE_PAIRS:
        idx1, idx2 = RUNE_PAIRS[c1], RUNE_PAIRS[c2]
        print(f"  {p1}: {c1}({idx1}) + {c2}({idx2}) = {idx1 + idx2}, mod 29 = {(idx1 + idx2) % 29}")

print()

# Maybe the two lines are meant to be compared?
# Line 1: original positions, Line 2: encrypted/transposed?
print("Comparing line 1 and line 2 as character substitution:")
for i, (p1, p2) in enumerate(zip(line1, line2)):
    print(f"  {p1} -> {p2}")

# The pairs could indicate a 14-column transposition cipher
print()
print("=" * 70)
print("14-COLUMN TRANSPOSITION KEY INTERPRETATION")
print("=" * 70)
print()
print("If this hints at column order for a transposition cipher:")
print("Reading order from base-36 values (sorted):")

combined = list(zip(values1 + values2, range(28)))
combined.sort()
reading_order = [idx for _, idx in combined]
print(f"Order: {reading_order}")

# Or maybe columns alternate between line 1 and line 2?
print()
print("Alternating interpretation:")
print("If we interleave lines: TL/SL, BE/BT, IE/II, OV/IY, ...")
for i in range(14):
    print(f"  Col {i}: {line1[i]}/{line2[i]} -> {values1[i]}/{values2[i]}")

# Let's see if line 2 values create a useful permutation
print()
print("Line 2 as reading order (sorted by value):")
line2_sorted = sorted(enumerate(values2), key=lambda x: x[1])
order = [idx for idx, val in line2_sorted]
print(f"Order: {order}")

# Apply this order as a test
print()
print("=" * 70)
print("TESTING 08.JPG HINT AS TRANSPOSITION KEY")
print("=" * 70)

import numpy as np

RUNES_STR = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES_STR)}
LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
         'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
         'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
}

def indices_to_text(indices):
    return ''.join(LATIN[i % 29] for i in indices)

def word_score(text):
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST',
             'SURFACE', 'TUNNEL', 'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        score += text_upper.count(word) * len(word)
    return score

# Reading order derived from base-36 decoded Line 2 values
line2_order = [idx for idx, _ in sorted(enumerate(values2), key=lambda x: x[1])]
print(f"Column reading order from Line 2: {line2_order}")

# Test on each page with 14 columns
for pg_num in [27, 28, 29, 30, 31]:
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    print(f"\nPage {pg_num} ({n} runes):")
    
    cols = 14  # From the 14 pairs in the hint
    rows = (n + cols - 1) // cols
    
    # Pad to full grid
    padded = list(pg_idx) + [0] * (rows * cols - n)
    grid = np.array(padded).reshape(rows, cols)
    
    # Read columns in the order specified by line2_order
    result = []
    for col_idx in line2_order:
        for row in range(rows):
            if row * cols + col_idx < n:
                result.append(grid[row, col_idx])
    
    result = np.array(result[:n])
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    
    # Decrypt
    decrypted = (result - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"  14-col transposition with Line2 order + key: score {score}")
    print(f"  Text: {text[:70]}...")
    
    # Also try without key
    text_nokey = indices_to_text(result)
    score_nokey = word_score(text_nokey)
    print(f"  Without key: score {score_nokey}")
    
    # Try reading rows in Line2 order instead
    result2 = []
    for row_idx in line2_order[:rows]:  # Only use as many as we have rows
        for col in range(cols):
            if row_idx * cols + col < n:
                result2.append(pg_idx[row_idx * cols + col])
    
    # Pad if needed
    for i in range(n):
        if len(result2) < n and i not in result2:
            result2.append(pg_idx[i])
    
    result2 = np.array(result2[:n])
    decrypted2 = (result2 - key_ext) % 29
    text2 = indices_to_text(decrypted2)
    score2 = word_score(text2)
    print(f"  Row reorder attempt: score {score2}")

# Maybe the hint is about PAIRS of runes?
print()
print("=" * 70)
print("PAIR-BASED INTERPRETATION")
print("=" * 70)
print()
print("The hint shows PAIRS. Maybe we need to swap/transpose pairs of runes?")

# The pairs in line 1 could be original positions
# The pairs in line 2 could be what they become
# TL -> SL means T and L become S and L?

# Let's map single letters
print("Letter mappings from pairs:")
for p1, p2 in zip(line1, line2):
    c1_1, c1_2 = p1[0], p1[1]
    c2_1, c2_2 = p2[0], p2[1]
    if c1_1 != c2_1:
        print(f"  {c1_1} -> {c2_1}")
    if c1_2 != c2_2:
        print(f"  {c1_2} -> {c2_2}")

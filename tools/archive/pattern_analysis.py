#!/usr/bin/env python3
"""
Key insight: The cipher is arranged as 14 groups of 5 characters.
14 and 5 are interesting: 14 = 2*7, 5 is prime
The message might read in a specific pattern.

Also: Let's try reading the discovered message as intended plaintext
and look for meaning in the apparent scramble.
"""

from itertools import permutations
from collections import Counter

GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', 'TFYV', 'OIUAU', 'SNOCO', 'JIM', 'EODZZ']

CIPHER = "IDGTKUMLOOARWOERTHISUTETLHUTIATSLLOUIMNITELNJTFYVOIUAUSNOCOJIMEODZZ"

print("="*70)
print("READING PATTERN ANALYSIS")
print("="*70)

# ============================================================
# What if we read diagonally through the 14x5 grid?
# ============================================================
print("\n" + "="*50)
print("DIAGONAL READING PATTERNS")
print("="*50)

# Create 14x5 grid (padding short groups)
grid = []
for g in ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', 'TFYV_', 'OIUAU', 'SNOCO', 'JIM__', 'EODZZ']:
    grid.append(list(g.replace('_', ' ')))

print("Grid:")
for i, row in enumerate(grid):
    print(f"  {i+1:2d}: {''.join(row)}")

# Read diagonals (top-left to bottom-right)
print("\nDiagonals (TL to BR):")
diagonals = []
# Start from each cell in first row
for start_col in range(5):
    diag = []
    r, c = 0, start_col
    while r < 14 and c < 5:
        if grid[r][c] != ' ':
            diag.append(grid[r][c])
        r += 1
        c += 1
    diagonals.append(''.join(diag))
    print(f"  Start col {start_col}: {''.join(diag)}")

# Start from each cell in first column (except 0,0)
for start_row in range(1, 14):
    diag = []
    r, c = start_row, 0
    while r < 14 and c < 5:
        if grid[r][c] != ' ':
            diag.append(grid[r][c])
        r += 1
        c += 1
    diagonals.append(''.join(diag))
    if len(diag) > 2:
        print(f"  Start row {start_row}: {''.join(diag)}")

# ============================================================
# Zigzag reading through grid
# ============================================================
print("\n" + "="*50)
print("ZIGZAG/BOUSTROPHEDON READING")
print("="*50)

# Alternate direction each row
zigzag = []
for i, row in enumerate(grid):
    if i % 2 == 0:
        zigzag.extend([c for c in row if c != ' '])
    else:
        zigzag.extend([c for c in reversed(row) if c != ' '])
result = ''.join(zigzag)
print(f"Zigzag: {result}")

# ============================================================  
# Spiral reading
# ============================================================
print("\n" + "="*50)
print("SPIRAL READING FROM CENTER")
print("="*50)

# For a 14x5 grid, center is around row 7, col 2
# Spiral outward

def spiral_inward(grid, rows, cols):
    """Read grid in spiral pattern, inward from outside."""
    result = []
    top, bottom, left, right = 0, rows-1, 0, cols-1
    
    while top <= bottom and left <= right:
        # Top row, left to right
        for c in range(left, right+1):
            if grid[top][c] != ' ':
                result.append(grid[top][c])
        top += 1
        
        # Right column, top to bottom  
        for r in range(top, bottom+1):
            if right < len(grid[r]) and grid[r][right] != ' ':
                result.append(grid[r][right])
        right -= 1
        
        # Bottom row, right to left
        if top <= bottom:
            for c in range(right, left-1, -1):
                if grid[bottom][c] != ' ':
                    result.append(grid[bottom][c])
            bottom -= 1
        
        # Left column, bottom to top
        if left <= right:
            for r in range(bottom, top-1, -1):
                if grid[r][left] != ' ':
                    result.append(grid[r][left])
            left += 1
    
    return ''.join(result)

spiral = spiral_inward(grid, 14, 5)
print(f"Spiral inward: {spiral}")

# ============================================================
# Read columns in different patterns
# ============================================================
print("\n" + "="*50)
print("COLUMN PATTERN READING")
print("="*50)

# Read columns in order based on 7, 5, 4 pattern
# Column indices are 0,1,2,3,4
# 7 mod 5 = 2, 5 mod 5 = 0, 4 mod 5 = 4

patterns = [
    [2, 0, 4, 1, 3],  # 7,5,4 mod 5 = 2,0,4
    [0, 2, 4, 1, 3],  # Evens first, then odds
    [1, 3, 0, 2, 4],  # Odds first, then evens
    [4, 2, 0, 3, 1],  # Reverse of pattern 1
]

for pattern in patterns:
    result = []
    for col in pattern:
        for row in range(14):
            if col < len(grid[row]) and grid[row][col] != ' ':
                result.append(grid[row][col])
    print(f"  Pattern {pattern}: {''.join(result)[:50]}...")

# ============================================================
# Read rows in specific order
# ============================================================
print("\n" + "="*50)
print("ROW REORDERING")
print("="*50)

# What if rows should be reordered?
# 14 rows, primes up to 14: 2,3,5,7,11,13

# Try reading rows at prime positions first
prime_rows = [1, 2, 4, 6, 10, 12]  # 0-indexed for primes 2,3,5,7,11,13
other_rows = [i for i in range(14) if i not in prime_rows]

result = ''.join(''.join(c for c in grid[r] if c != ' ') for r in prime_rows)
result += ''.join(''.join(c for c in grid[r] if c != ' ') for r in other_rows)
print(f"Prime rows first: {result[:50]}...")

# Reverse
result = ''.join(''.join(c for c in grid[r] if c != ' ') for r in reversed(range(14)))
print(f"Rows reversed: {result[:50]}...")

# ============================================================
# Row anagrams - what if each row is scrambled?
# ============================================================
print("\n" + "="*50)
print("LOOKING FOR WORDS IN ROW ANAGRAMS")
print("="*50)

# Each group might spell a word when unscrambled
possible_words = {
    'IDGTK': ['DIGIT?', '?'],  # Missing I for DIGIT
    'UMLOO': ['MOOLU?', 'BLOOM-O?'],
    'ARWOE': ['AWARE-O?', 'ROWE A?'],
    'RTHIS': ['THIS R', 'SHIRT'],
    'UTETL': ['TUTLE?', 'LUTE T?'],
    'HUTIA': ['?'],
    'TSLLO': ['TOLLS', 'STOLL'],
    'UIMNI': ['MINIU?', 'UNIMNI?'],
    'TELNJ': ['?'],
    'TFYV': ['?'],  
    'OIUAU': ['?'],
    'SNOCO': ['CONOS?', 'SCOON?'],
    'JIM': ['JIM!'],
    'EODZZ': ['DOZZE?', 'ZONED-Z?'],
}

# Check if TSLLO could be TOLLS
print("TSLLO -> anagrams containing 'TOLL': ", end="")
for p in permutations('TSLLO'):
    s = ''.join(p)
    if 'TOLL' in s or 'SLOT' in s or 'LOTS' in s:
        print(s, end=" ")
print()

# RTHIS definitely contains THIS
print("RTHIS -> contains THIS: TRUE")

# ============================================================
# Key Discovery: Look at what letters we have
# ============================================================
print("\n" + "="*50)
print("FINAL LETTER ANALYSIS")
print("="*50)

letter_count = Counter(CIPHER)
print(f"Total letters: {len(CIPHER)}")
print(f"Letter frequency: {dict(sorted(letter_count.items(), key=lambda x: -x[1]))}")

# Most common: O(8), T(8), I(7), U(6), L(5)
# These are common in: "UNTO", "INITIAT(ED)", "TRUTH", "LIBER", "ILLUMINATI"

# Check for "ILLUMINATI"
test = "ILLUMINATI"
test_count = Counter(test)
can_form = all(letter_count.get(c, 0) >= test_count[c] for c in test_count)
print(f"\nCan form 'ILLUMINATI': {can_form}")

# What about Latin phrases Cicada uses?
latin = ["DIVINORUM", "INTUS", "VERITAS", "OMNIBUS", "LIBERTAS"]
for phrase in latin:
    tc = Counter(phrase)
    can = all(letter_count.get(c, 0) >= tc[c] for c in tc)
    print(f"Can form '{phrase}': {can}")

print("\n" + "="*70)
print("SUMMARY: THE MESSAGE STRUCTURE")  
print("="*70)

print("""
AUTHENTICATED CICADA 3301 CIPHER (from XOR of outguess data)
Signed: 2014-01-07 03:00:31 UTC

Groups:
  1: IDGTK    8: UIMNI
  2: UMLOO    9: TELNJ
  3: ARWOE   10: 7TFYV  <- number 7
  4: RTHIS   11: OIUAU  
  5: UTETL   12: SNOCO
  6: HUTIA   13: 5JI4M  <- numbers 5, 4
  7: TSLLO   14: EODZZ

Known patterns:
- Group 4 contains "THIS"
- Group 7 "TSLLO" could be "TOLLS" anagram
- Numbers 7,5,4 mark groups 10 and 13
- 67 letters total (without numbers)

This is a verified Cicada message that has been hidden using XOR
of three outguess extractions. The solution method is still unclear
but likely involves:
1. A transposition cipher
2. The numbers 7,5,4 as key indicators
3. Possible anagramming of individual groups
""")

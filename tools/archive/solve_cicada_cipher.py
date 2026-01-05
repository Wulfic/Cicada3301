#!/usr/bin/env python3
"""
Comprehensive solver for the Cicada 3301 authenticated cipher:

IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO
UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ

Signed by Cicada 3301 on 2014-01-07.
"""

import itertools
from collections import Counter
import re

# The authenticated cipher
GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', '7TFYV', 'OIUAU', 'SNOCO', '5JI4M', 'EODZZ']

CIPHER = ''.join(GROUPS)
CIPHER_LETTERS = CIPHER.replace('7', '').replace('5', '').replace('4', '')

print("="*70)
print("CICADA 3301 CIPHER SOLVER")
print("="*70)
print(f"\nOriginal: {' '.join(GROUPS)}")
print(f"Letters only: {CIPHER_LETTERS} ({len(CIPHER_LETTERS)} chars)")

# Key observations:
# 1. 14 groups of 5 characters
# 2. Numbers 7, 5, 4 appear in groups 10 and 13 (0-indexed: 9 and 12)
# 3. "THIS" appears in RTHIS (group 4)
# 4. Total: 67 letters + 3 numbers = 70 characters

# Cicada loves primes and mathematical patterns
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

def score_english(text):
    """Score text based on English word patterns."""
    text = text.upper()
    score = 0
    
    # Common English words
    words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 
             'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'WILL', 'YOUR', 'THEY',
             'INTO', 'UNTO', 'FIND', 'TRUTH', 'WITHIN', 'DIVINITY', 'WISDOM',
             'LIKE', 'MUST', 'SHED', 'OUR', 'OWN', 'EMERGE', 'INSTAR', 'KEY',
             'LIBER', 'PRIMUS', 'RUNE', 'CICADA', 'SEEK', 'PATH', 'WAY']
    
    for word in words:
        if word in text:
            score += len(word) * 10
    
    # Common bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND',
               'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR']
    for bg in bigrams:
        score += text.count(bg) * 2
    
    return score

# ============================================================
# METHOD 1: Grid-based transposition
# ============================================================
print("\n" + "="*60)
print("METHOD 1: GRID-BASED READING")
print("="*60)

# Arrange as 14 rows x 5 columns (as given)
print("\n14x5 Grid (as presented):")
for i, g in enumerate(GROUPS):
    print(f"  {i+1:2d}: {g}")

# Read by columns
print("\nReading columns:")
for col in range(5):
    column = ''.join(g[col] if col < len(g) else ' ' for g in GROUPS)
    print(f"  Col {col+1}: {column}")

# Column-first reading
col_read = ''
for col in range(5):
    for g in GROUPS:
        if col < len(g):
            col_read += g[col]
print(f"\nColumn reading: {col_read}")
print(f"Score: {score_english(col_read)}")

# ============================================================
# METHOD 2: Numeric markers as instructions
# ============================================================
print("\n" + "="*60)
print("METHOD 2: NUMERIC MARKERS ANALYSIS")
print("="*60)

# Groups with numbers:
# Group 10 (index 9): 7TFYV - starts with 7
# Group 13 (index 12): 5JI4M - has 5 and 4

print("Groups with numbers:")
print("  Group 10: 7TFYV -> remove 7 -> TFYV")
print("  Group 13: 5JI4M -> remove 5,4 -> JIM")

# Maybe 7, 5, 4 indicate positions or a key?
print("\n7, 5, 4 could indicate:")
print("  - Column order: read columns 7,5,4,... (but only 5 columns)")
print("  - Row positions to swap or prioritize")
print("  - Modular arithmetic (mod 7, mod 5, mod 4)")

# Let's try removing those groups and see what's left
print("\nWithout numbered groups:")
clean_groups = [g for i, g in enumerate(GROUPS) if i not in [9, 12]]
print(' '.join(clean_groups))

# ============================================================
# METHOD 3: Anagram approach
# ============================================================
print("\n" + "="*60)
print("METHOD 3: ANAGRAM ANALYSIS")
print("="*60)

# What words could this contain?
letter_counts = Counter(CIPHER_LETTERS)
print(f"Letter counts: {dict(letter_counts)}")

# Check for specific phrases
def can_form(phrase, available):
    """Check if phrase can be formed from available letters."""
    phrase = phrase.upper().replace(' ', '')
    phrase_count = Counter(phrase)
    return all(available.get(c, 0) >= phrase_count[c] for c in phrase_count)

phrases_to_check = [
    "UNTO THE INITIATED",
    "TRUTH LIES WITHIN",
    "DIVINITY WITHIN",
    "THE KEY IS",
    "LIKE THE INSTAR",
    "FIND THE DIVINITY",
    "LIBER PRIMUS",
    "THIS IS THE KEY",
    "YOU MUST SEEK",
    "WISDOM AWAITS",
]

print("\nPossible phrases:")
for phrase in phrases_to_check:
    if can_form(phrase, letter_counts):
        remaining = CIPHER_LETTERS
        for c in phrase.upper().replace(' ', ''):
            remaining = remaining.replace(c, '', 1)
        print(f"  ✓ '{phrase}' (remaining: {remaining})")

# ============================================================
# METHOD 4: Rail fence cipher
# ============================================================
print("\n" + "="*60)
print("METHOD 4: RAIL FENCE CIPHER")
print("="*60)

def rail_fence_decrypt(text, rails):
    """Decrypt rail fence cipher."""
    if rails <= 1:
        return text
    
    # Create the fence pattern
    fence = [[None] * len(text) for _ in range(rails)]
    
    # Mark positions in zigzag pattern
    rail = 0
    direction = 1
    for i in range(len(text)):
        fence[rail][i] = True
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    # Fill with cipher text
    idx = 0
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c]:
                fence[r][c] = text[idx]
                idx += 1
    
    # Read in zigzag order
    result = []
    rail = 0
    direction = 1
    for i in range(len(text)):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    return ''.join(result)

print("Rail fence decryption:")
for rails in range(2, 10):
    result = rail_fence_decrypt(CIPHER_LETTERS, rails)
    score = score_english(result)
    if score > 30:
        print(f"  {rails} rails (score={score}): {result[:50]}...")

# ============================================================
# METHOD 5: Route cipher (spiral, snake, etc.)
# ============================================================
print("\n" + "="*60)
print("METHOD 5: ROUTE CIPHER")
print("="*60)

def route_read(text, rows, cols, route_type):
    """Read text arranged in grid using different routes."""
    # Pad if needed
    text = text.ljust(rows * cols)[:rows*cols]
    
    # Create grid
    grid = []
    for r in range(rows):
        grid.append(list(text[r*cols:(r+1)*cols]))
    
    result = []
    
    if route_type == 'col':
        # Column by column
        for c in range(cols):
            for r in range(rows):
                result.append(grid[r][c])
    
    elif route_type == 'col_rev':
        # Columns, alternating direction
        for c in range(cols):
            if c % 2 == 0:
                for r in range(rows):
                    result.append(grid[r][c])
            else:
                for r in range(rows-1, -1, -1):
                    result.append(grid[r][c])
    
    elif route_type == 'spiral':
        # Spiral inward from top-left
        top, bottom, left, right = 0, rows-1, 0, cols-1
        while top <= bottom and left <= right:
            # Top row
            for c in range(left, right+1):
                if top < rows and c < cols:
                    result.append(grid[top][c])
            top += 1
            # Right column
            for r in range(top, bottom+1):
                if r < rows and right < cols:
                    result.append(grid[r][right])
            right -= 1
            # Bottom row
            if top <= bottom:
                for c in range(right, left-1, -1):
                    if bottom < rows and c < cols and c >= 0:
                        result.append(grid[bottom][c])
                bottom -= 1
            # Left column
            if left <= right:
                for r in range(bottom, top-1, -1):
                    if r < rows and r >= 0 and left < cols:
                        result.append(grid[r][left])
                left += 1
    
    return ''.join(result)[:len(text.strip())]

print("Route cipher attempts:")
for rows in [5, 7, 10, 14]:
    for cols in [5, 7, 10, 14]:
        if rows * cols >= len(CIPHER_LETTERS):
            for route in ['col', 'col_rev', 'spiral']:
                result = route_read(CIPHER_LETTERS, rows, cols, route)
                score = score_english(result)
                if score > 40:
                    print(f"  {rows}x{cols} {route} (score={score}): {result[:50]}...")

# ============================================================
# METHOD 6: Keyword columnar transposition
# ============================================================
print("\n" + "="*60)
print("METHOD 6: COLUMNAR TRANSPOSITION WITH KEYWORDS")
print("="*60)

def columnar_decrypt(text, key_order):
    """Decrypt columnar transposition given column order."""
    num_cols = len(key_order)
    num_rows = (len(text) + num_cols - 1) // num_cols
    
    # Calculate column lengths
    full_cols = len(text) % num_cols
    if full_cols == 0:
        full_cols = num_cols
    
    # Create grid
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Fill columns in key order
    idx = 0
    for col in sorted(range(num_cols), key=lambda x: key_order[x]):
        col_len = num_rows if col < full_cols or full_cols == num_cols else num_rows - 1
        for row in range(col_len):
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    # Read row by row
    return ''.join(''.join(row) for row in grid)

# Try common Cicada-related keywords
keywords = ['CICADA', 'PRIMUS', 'LIBER', 'RUNE', 'INSTAR', 'DIVINITY', 'TRUTH']

def keyword_to_order(keyword):
    """Convert keyword to column order."""
    chars = [(c, i) for i, c in enumerate(keyword)]
    chars.sort()
    return [i for c, i in sorted(chars, key=lambda x: x[1])]

print("Trying keywords:")
for kw in keywords:
    order = keyword_to_order(kw)
    result = columnar_decrypt(CIPHER_LETTERS, order)
    score = score_english(result)
    print(f"  {kw}: {result[:40]}... (score={score})")

# ============================================================
# METHOD 7: Prime-based reading
# ============================================================
print("\n" + "="*60)
print("METHOD 7: PRIME-BASED PATTERNS")
print("="*60)

# Read characters at prime positions
print("Characters at prime positions (1-indexed):")
prime_chars = ''.join(CIPHER_LETTERS[p-1] for p in PRIMES if p <= len(CIPHER_LETTERS))
print(f"  {prime_chars}")

# Read characters at non-prime positions
print("\nCharacters at non-prime positions:")
non_prime_chars = ''.join(CIPHER_LETTERS[i] for i in range(len(CIPHER_LETTERS)) if (i+1) not in PRIMES)
print(f"  {non_prime_chars}")

# Interleave prime and non-prime
print("\nPrime positions first, then rest:")
combined = prime_chars + non_prime_chars
print(f"  {combined}")
print(f"  Score: {score_english(combined)}")

# ============================================================
# METHOD 8: Reorder groups by different patterns
# ============================================================
print("\n" + "="*60)
print("METHOD 8: GROUP REORDERING")
print("="*60)

# Try reordering groups based on numbers found
# 7, 5, 4 might indicate group positions

# Try: groups at positions 7, 5, 4 (1-indexed) first
reorder_754 = [6, 4, 3] + [i for i in range(14) if i not in [6, 4, 3]]  # 0-indexed: 6, 4, 3
result = ''.join(GROUPS[i] for i in reorder_754)
print(f"Groups 7,5,4 first: {result}")
print(f"Score: {score_english(result)}")

# Try reverse order
reverse = ''.join(GROUPS[i] for i in range(13, -1, -1))
print(f"\nReversed: {reverse}")
print(f"Score: {score_english(reverse)}")

# ============================================================
# METHOD 9: Looking for "UNTO THE INITIATED"
# ============================================================
print("\n" + "="*60)
print("METHOD 9: TARGETED PHRASE SEARCH")
print("="*60)

# The phrase "UNTO THE INITIATED" appears in other Cicada messages
# Let's check if our text can form it

target = "UNTOTHEINITIATEDLIKETHEINSTARTUNNELINGTOTHESURFACEWEMUSTSHEDO UROWNCIRCUMFERENCESFINDTHEDIVINITYWITHINANDEMERGE"

# Check what letters we have vs what we need
our_letters = Counter(CIPHER_LETTERS)
print(f"Our letters: {len(CIPHER_LETTERS)} characters")
print(f"Unique: {len(our_letters)}")

# "UNTO" check
if can_form("UNTO", our_letters):
    print("Can form: UNTO")
if can_form("THE", our_letters):
    print("Can form: THE")
if can_form("INITIATED", our_letters):
    print("Can form: INITIATED")
else:
    # What's missing?
    needed = Counter("INITIATED")
    missing = []
    for c, count in needed.items():
        if our_letters.get(c, 0) < count:
            missing.append(f"{c}({count - our_letters.get(c, 0)})")
    print(f"Cannot form INITIATED, missing: {', '.join(missing)}")

# ============================================================
# METHOD 10: The 7, 5, 4 as base conversion
# ============================================================
print("\n" + "="*60)
print("METHOD 10: NUMERIC INTERPRETATION")
print("="*60)

# What if 7TFYV and 5JI4M encode something?
# 7 in position 0, 5 in position 0, 4 in position 3

# Positions: 7 at index 45, 5 at index 60, 4 at index 63
pos_7 = CIPHER.find('7')
pos_5 = CIPHER.find('5')
pos_4 = CIPHER.find('4')
print(f"Position of 7: {pos_7}")
print(f"Position of 5: {pos_5}")
print(f"Position of 4: {pos_4}")

# Differences
print(f"5 - 7 = {pos_5 - pos_7}")
print(f"4 - 5 = {pos_4 - pos_5}")

# Perhaps remove characters at these positions?
removed = CIPHER[:pos_7] + CIPHER[pos_7+1:pos_5] + CIPHER[pos_5+1:pos_4] + CIPHER[pos_4+1:]
print(f"\nWith numbers removed: {removed}")

# ============================================================
# BEST RESULTS SUMMARY
# ============================================================
print("\n" + "="*60)
print("ANALYSIS SUMMARY")
print("="*60)

print("""
Key observations:
1. This is a verified Cicada 3301 message from 2014-01-07
2. Contains 67 letters + 3 numbers (7, 5, 4)
3. "THIS" is embedded in group 4 (RTHIS)
4. Can form phrases: DIVINITY, WITHIN, TRUTH, etc.

The numbers 7, 5, 4 appear to be markers or instructions.
The solution likely involves a transposition cipher.

Next steps to try:
1. Brute force columnar transposition with 5-7 columns
2. Try Cicada's known references as keywords
3. Look for "UNTO THE INITIATED" or similar phrases
""")

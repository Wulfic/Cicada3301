"""
Page 20 - Diagonal Reading Analysis
===================================
The decoded artifact ends with "DIAG" suggesting diagonal reading.
P20 is a 29×28 grid (812 runes). Let's try diagonal reads.
"""

import math
from collections import Counter

# Gematria Primus mapping
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Page 20 runes (812 total, 29 per line, 28 lines)
p20_runes = [
    "ᚠᛁᛝᛈᛗᚩᛡᛇᛁᛡᚦᛗᛡᚢᛋᚳᛄᚹᛋᛗᛖᛈᚫᛚᚾᚻᚦᚱ",  # Line 1
    "ᛈᛁᚠᚾᚢᛏᚪᛋᛒᚢᚳᚳᛋᛖᛏᛠᚾᛗᛠᛡᚢᛒᛏᚣᛖᚱᚦᛋᛉ",  # Line 2
    "ᛡᛇᛖᚻᛗᚢᚦᛖᛚᚹᛋᛠᛖᛄᚾᛏᛖᛡᚣᚾᚳᚳᛒᛇᚠᛗᚦᛝᛠ",  # Line 3
    "ᛁᚦᚾᛄᚪᛞᚣᚾᚻᛉᚪᛋᚷᛒᛖᛇᛟᛇᛗᚾᛈᛒᚪᛠᛚᛖᚳᚪᛋ",  # Line 4
    "ᛗᛠᛁᛄᛁᚫᛋᛈᛁᛚᚢᚳᛈᛖᛡᛈᛡᛖᛋᛚᛄᚦᚠᛁᚷᚫᛒᛇᛞ",  # Line 5
    "ᛒᛗᚣᚹᛄᚱᛚᛁᛋᛈᛈᛁᚾᛋᛈᚠᛠᛖᚣᛚᛖᛚᚾᛉᛁᛏᛡᚻᚦ",  # Line 6
    "ᛖᛈᚷᚢᚱᛏᛖᛖᚣᛟᛈᛡᛗᛝᛒᛚᛏᛟᛁᚫᚹᚦᛒᚣᚳᛉᛏᛇᛗ",  # Line 7
    "ᛁᛒᚢᛖᛠᚠᚦᛁᚠᛈᛇᚷᛗᛈᛁᚻᛟᛈᛡᚳᛗᛇᛈᚠᛈᛄᚣᛡᛠ",  # Line 8
    "ᛁᛄᚩᛈᛟᚷᚣᚠᛋᚾᚱᚢᛞᚫᛒᛈᛁᛝᚩᛉᚹᛟᛏᛁᚳᚫᛞᛋᛏ",  # Line 9
    "ᚠᛏᛡᛉᚾᛡᛇᚪᛋᛄᛄᛇᛞᚪᛁᛝᚠᚣᛄᛄᚪᛒᛈᛋᛠᛞᛁᛇᛈ",  # Line 10
    "ᚱᚫᚳᛉᛠᛁᚱᛒᛖᛠᛝᛉᛁᛏᛟᛖᚻᛁᚳᚷᛠᛗᚩᛄᛏᛇᚷᛏᛒ",  # Line 11
    "ᚹᚳᛟᚠᛗᛄᛈᛁᚩᛈᛝᛡᛗᛚᛄᚷᛖᚠᛗᛁᛖᛈᚪᛒᚠᚫᛈᛞᛁ",  # Line 12
    "ᛝᛄᚢᛗᛗᛠᛟᛇᛞᛏᚣᛄᛄᛗᚣᚻᚣᛡᛋᚫᛠᛗᚦᚾᛗᚾᚪᛟᛖ",  # Line 13
    "ᚣᛋᛠᚣᛝᛄᚦᛒᛖᚫᛞᚾᛈᚢᚣᛚᛉᛞᚦᛠᚱᛖᛠᛗᛒᛈᚦᚩᛏ",  # Line 14
    "ᚷᚹᛟᚳᛝᛋᚢᚦᛖᛡᛒᚢᚢᛁᚢᛈᛉᛉᛁᚱᛏᛠᚾᛡᛚᛈᛠᛇᛇ",  # Line 15
    "ᛋᛖᛝᛄᛗᚳᚹᛟᛖᛁᚢᛝᛈᚦᛄᛒᛡᚷᛡᚩᚳᛠᛗᛈᛏᛗᛈᛋᚹ",  # Line 16
    "ᛖᛏᛁᚠᚢᛟᚩᛠᛗᚷᛇᛁᛒᚳᚠᛁᛋᛠᛞᛖᛡᛁᚾᛚᛗᛈᛄᛏᛁ",  # Line 17
    "ᛗᛋᛈᚦᚷᚢᚫᚣᛝᚣᛚᚱᚻᛒᛏᛞᛗᛖᚦᛈᛁᚳᛠᚠᛄᚣᚢᛉᛟ",  # Line 18
    "ᚱᛏᚦᛟᛁᛇᛖᚫᛡᛖᛠᛞᛄᛝᚣᛈᛁᚫᛒᛁᛒᛗᛈᛈᛗᛏᛏᛠᚩ",  # Line 19
    "ᛟᛁᚩᛡᚠᛇᛗᚷᛝᚢᛡᚠᛄᛗᛗᛄᚣᛚᛁᛉᛁᛁᚠᛉᛒᚢᚹᚻᛝ",  # Line 20
    "ᚷᛏᛋᛚᛗᛒᛈᛟᛈᚢᛁᛟᛇᛖᛞᛋᛚᛁᛟᛈᚦᚻᛗᛒᚱᚹᛋᚱᛡ",  # Line 21
    "ᛁᚫᛝᚾᛟᚣᛈᛟᛖᛗᛝᛚᛄᛈᚦᛠᚠᚫᛇᛋᛞᛡᛇᛏᛖᛈᛒᛡᛏ",  # Line 22
    "ᚪᛈᚩᛋᛋᛈᛇᛇᛏᚷᛋᚱᛄᛋᚹᛇᛞᚠᛖᛝᛡᛚᛈᛋᛋᛄᛞᛟᛋ",  # Line 23
    "ᛚᛚᚻᛡᛗᛒᛄᚠᛁᛟᛋᚷᚦᛒᚣᛁᚾᚪᛈᚢᛈᛄᛠᛏᚫᛋᛒᛞᛁ",  # Line 24
    "ᚪᛏᚹᛋᛖᛞᛄᛝᚠᚦᛖᛚᚢᛞᛈᛚᛡᚫᛈᛡᚣᛟᛉᛗᛚᚦᛈᛁᛏ",  # Line 25
    "ᛒᛡᛈᛈᛈᛖᛒᚢᛋᛁᚫᚦᚫᛈᛠᛈᛞᚢᚷᛈᛏᛋᛖᛁᛄᛟᛝᚾᚦ",  # Line 26
    "ᚪᛄᛁᚱᛋᚾᚠᛋᚦᛁᚦᛄᚠᛚᛋᛗᛡᚫᛈᛞᛠᛈᛁᚫᛄᛠᛏᛈᛚ",  # Line 27
    "ᛋᛒᛋᛠᛞᛠᛚᛠᛁᛖᛋᛁᛈᛄᛄᛁᛒᛇᚠᛋᛁᛏᛈᛒᚹᛝᛠᛈᛁ"   # Line 28
]

# Rune to index mapping
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def rune_to_runeglish(idx):
    return RUNEGLISH[idx]

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    freq = Counter(indices)
    n = len(indices)
    return sum(f * (f-1) for f in freq.values()) / (n * (n-1) / 29)

# Parse grid
grid = []
for line in p20_runes:
    row = [RUNE_TO_IDX[r] for r in line]
    grid.append(row)

ROWS = len(grid)  # 28
COLS = len(grid[0])  # 29

print(f"Grid dimensions: {ROWS} rows × {COLS} cols = {ROWS * COLS} runes")

# Flatten for reference
flat = [grid[r][c] for r in range(ROWS) for c in range(COLS)]
print(f"Raw IoC: {calc_ioc(flat):.4f}")

# Diagonal reads
print("\n=== DIAGONAL READING PATTERNS ===")

# Main diagonals (top-left to bottom-right)
def read_main_diagonals():
    """Read all main diagonals (TL to BR)"""
    result = []
    # Start from first column
    for start_row in range(ROWS-1, -1, -1):
        r, c = start_row, 0
        while r < ROWS and c < COLS:
            result.append(grid[r][c])
            r += 1
            c += 1
    # Start from first row (skip corner, already done)
    for start_col in range(1, COLS):
        r, c = 0, start_col
        while r < ROWS and c < COLS:
            result.append(grid[r][c])
            r += 1
            c += 1
    return result

# Anti-diagonals (top-right to bottom-left)
def read_anti_diagonals():
    """Read all anti-diagonals (TR to BL)"""
    result = []
    # Start from first column
    for start_row in range(ROWS):
        r, c = start_row, 0
        while r >= 0 and c < COLS:
            result.append(grid[r][c])
            r -= 1
            c += 1
    # Start from bottom row (skip corner)
    for start_col in range(1, COLS):
        r, c = ROWS - 1, start_col
        while r >= 0 and c < COLS:
            result.append(grid[r][c])
            r -= 1
            c += 1
    return result

# Single long diagonal wrap-around
def read_wrap_diagonal():
    """Read diagonal with wrap-around"""
    result = []
    r, c = 0, 0
    for _ in range(ROWS * COLS):
        result.append(grid[r][c])
        r = (r + 1) % ROWS
        c = (c + 1) % COLS
    return result

main_diag = read_main_diagonals()
anti_diag = read_anti_diagonals()
wrap_diag = read_wrap_diagonal()

print(f"\nMain diagonals: {len(main_diag)} runes, IoC: {calc_ioc(main_diag):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in main_diag[:40])}")

print(f"\nAnti-diagonals: {len(anti_diag)} runes, IoC: {calc_ioc(anti_diag):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in anti_diag[:40])}")

print(f"\nWrap diagonal: {len(wrap_diag)} runes, IoC: {calc_ioc(wrap_diag):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in wrap_diag[:40])}")

# Try different diagonal step patterns
print("\n=== STEPPED DIAGONAL PATTERNS ===")

def read_stepped_diagonal(step_r, step_c):
    """Read with custom step pattern"""
    result = []
    r, c = 0, 0
    visited = set()
    while len(result) < ROWS * COLS:
        if (r, c) not in visited and r < ROWS and c < COLS:
            result.append(grid[r][c])
            visited.add((r, c))
        r = (r + step_r) % ROWS
        c = (c + step_c) % COLS
        # Detect full cycle
        if len(visited) > 0 and (r, c) == (0, 0):
            break
    return result

for step_r in [1, 2, 3, 5, 7]:
    for step_c in [1, 2, 3, 5, 7]:
        if step_r == 1 and step_c == 1:
            continue  # Already done
        stepped = read_stepped_diagonal(step_r, step_c)
        if len(stepped) > 100:
            ioc = calc_ioc(stepped)
            if ioc > 1.1:
                print(f"Step ({step_r},{step_c}): {len(stepped)} runes, IoC: {ioc:.4f}")
                print(f"  First 30: {''.join(rune_to_runeglish(i) for i in stepped[:30])}")

# Spiral reading
print("\n=== SPIRAL READING ===")

def read_spiral():
    """Read grid in spiral pattern"""
    result = []
    top, bottom, left, right = 0, ROWS-1, 0, COLS-1
    while top <= bottom and left <= right:
        # Right
        for c in range(left, right+1):
            result.append(grid[top][c])
        top += 1
        # Down
        for r in range(top, bottom+1):
            result.append(grid[r][right])
        right -= 1
        # Left
        if top <= bottom:
            for c in range(right, left-1, -1):
                result.append(grid[bottom][c])
            bottom -= 1
        # Up
        if left <= right:
            for r in range(bottom, top-1, -1):
                result.append(grid[r][left])
            left += 1
    return result

spiral = read_spiral()
print(f"Spiral: {len(spiral)} runes, IoC: {calc_ioc(spiral):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in spiral[:40])}")

# Prime-indexed diagonal
print("\n=== PRIME-INDEXED DIAGONAL ===")

def get_primes_up_to(n):
    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]

primes = get_primes_up_to(812)

# Extract primes from diagonal reads
for name, data in [("Main diag", main_diag), ("Anti diag", anti_diag), ("Spiral", spiral)]:
    prime_extract = [data[p] for p in primes if p < len(data)]
    ioc = calc_ioc(prime_extract)
    print(f"{name} @ primes: {len(prime_extract)} runes, IoC: {ioc:.4f}")
    print(f"  First 30: {''.join(rune_to_runeglish(i) for i in prime_extract[:30])}")

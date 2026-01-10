"""
Page 20 - Diagonal Analysis (Corrected)
========================================
Uses actual rune file loading with dots removed.
Tests diagonal reading based on "DIAG" hint from decoded artifact.
"""

import os
import sys
from collections import Counter

# Gematria Primus
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(filepath):
    """Load runes from file, stripping dots/spaces/newlines"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract only rune characters
    runes = [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]
    return runes

def rune_to_runeglish(idx):
    return RUNEGLISH[idx]

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    freq = Counter(indices)
    n = len(indices)
    return sum(f * (f-1) for f in freq.values()) / (n * (n-1) / 29)

def get_primes_up_to(n):
    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]

# Load P20
os.chdir(r"c:\Users\tyler\Repos\Cicada3301")
runes = load_runes("LiberPrimus/pages/page_20/runes.txt")
N = len(runes)
print(f"Loaded {N} runes from Page 20")
print(f"Raw IoC: {calc_ioc(runes):.4f}")

# Find best grid dimensions
print("\n=== GRID DIMENSIONS ===")
for rows in range(20, 35):
    cols = N // rows
    remainder = N % rows
    if remainder == 0 and cols > 20:
        print(f"  {rows} x {cols} = {rows * cols}")

# Try 28 x 29 grid (28 rows, 29 cols)
ROWS = 28
COLS = 29
if ROWS * COLS != N:
    print(f"WARNING: {ROWS}x{COLS}={ROWS*COLS} != {N}")
    # Pad if needed
    runes = runes + [0] * (ROWS * COLS - N)

# Create grid
grid = []
for r in range(ROWS):
    row = runes[r * COLS : (r + 1) * COLS]
    grid.append(row)

print(f"\nUsing {ROWS}x{COLS} grid")

# Diagonal reads
print("\n=== DIAGONAL READING PATTERNS ===")

# Main diagonal with wrap
def read_diag_wrap(step_r, step_c, start_r=0, start_c=0):
    """Read diagonal with wrap, collecting all unique positions"""
    result = []
    visited = set()
    r, c = start_r, start_c
    
    # Use LCM to determine cycle length
    import math
    cycle_len = (ROWS * COLS) // math.gcd(ROWS * step_c, COLS * step_r) if step_r > 0 else COLS
    
    for _ in range(ROWS * COLS):
        if (r, c) not in visited:
            result.append(grid[r][c])
            visited.add((r, c))
        r = (r + step_r) % ROWS
        c = (c + step_c) % COLS
        if len(visited) == ROWS * COLS:
            break
    return result

# Try various diagonal steps
print("\n--- Wrap Diagonal Patterns ---")
best_ioc = 0
best_pattern = None

for step_r in range(1, 8):
    for step_c in range(1, 8):
        diag = read_diag_wrap(step_r, step_c)
        if len(diag) < N // 2:
            continue  # Skip patterns that don't cover enough
        ioc = calc_ioc(diag)
        if ioc > best_ioc:
            best_ioc = ioc
            best_pattern = (step_r, step_c, diag)
        if ioc > 1.2:
            runeglish = "".join(rune_to_runeglish(i) for i in diag[:40])
            print(f"Step ({step_r},{step_c}): {len(diag)} runes, IoC: {ioc:.4f}")
            print(f"  First 40: {runeglish}")

if best_pattern:
    step_r, step_c, diag = best_pattern
    print(f"\nBest: Step ({step_r},{step_c}) IoC: {best_ioc:.4f}")

# Column reading
print("\n=== COLUMN READING PATTERNS ===")

def read_columns():
    """Read grid by columns"""
    result = []
    for c in range(COLS):
        for r in range(ROWS):
            result.append(grid[r][c])
    return result

cols = read_columns()
print(f"Column read: {len(cols)} runes, IoC: {calc_ioc(cols):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in cols[:40])}")

# Boustrophedon (alternating direction)
def read_boustrophedon():
    """Read alternating row directions"""
    result = []
    for r in range(ROWS):
        if r % 2 == 0:
            result.extend(grid[r])
        else:
            result.extend(reversed(grid[r]))
    return result

boust = read_boustrophedon()
print(f"\nBoustrophedon: {len(boust)} runes, IoC: {calc_ioc(boust):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in boust[:40])}")

# Key-based reorder using decoded artifact hint
print("\n=== USING DECODED ARTIFACT KEY ===")
# The decoded artifact contains "DIAG" and possibly "SIX", "MEAN", etc.
# "SIX" might mean step=6, "MEAN" might be mathematical operation

# Try step 6 diagonal
diag6 = read_diag_wrap(1, 6)
print(f"Diagonal step (1,6): {len(diag6)} runes, IoC: {calc_ioc(diag6):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in diag6[:40])}")

diag6r = read_diag_wrap(6, 1)
print(f"Diagonal step (6,1): {len(diag6r)} runes, IoC: {calc_ioc(diag6r):.4f}")
print(f"  First 40: {''.join(rune_to_runeglish(i) for i in diag6r[:40])}")

# Prime-step diagonal
primes = get_primes_up_to(30)
for p in primes[:5]:
    diag_p = read_diag_wrap(1, p)
    if len(diag_p) > N // 2:
        ioc = calc_ioc(diag_p)
        print(f"Diagonal step (1,{p}): {len(diag_p)} runes, IoC: {ioc:.4f}")

# Extract primes from diagonal reads
print("\n=== PRIME EXTRACTION FROM DIAGONALS ===")
primes_list = get_primes_up_to(N)

for name, data in [("Rows", runes), ("Columns", cols), ("Boustrophedon", boust)]:
    prime_extract = [data[p] for p in primes_list if p < len(data)]
    ioc = calc_ioc(prime_extract)
    print(f"{name} @ prime indices: {len(prime_extract)} runes, IoC: {ioc:.4f}")
    print(f"  First 30: {''.join(rune_to_runeglish(i) for i in prime_extract[:30])}")

"""
Page 20 - Deor Key Discovery
=============================
Looking for the Deor key hidden in the grid itself.
"REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"
"""

import collections

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

PRIMES_29 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
IDX_TO_PRIME = {i: p for i, p in enumerate(PRIMES_29)}
PRIME_TO_IDX = {p: i for i, p in enumerate(PRIMES_29)}

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def decrypt_vigenere(cipher, key, mode='sub'):
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        else:
            result.append((c + k) % 29)
    return result

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def main():
    print("="*60)
    print("PAGE 20 - DEOR KEY DISCOVERY")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    # Look for "DEOR" pattern anywhere in the grid
    print("\n--- Searching for DEOR pattern ---")
    
    # DEOR in rune indices: D=23, E=18, O=3, R=4
    DEOR = [23, 18, 3, 4]
    
    # Search rows
    for r in range(rows):
        row_latin = runes_to_latin(grid[r])
        if "DEOR" in row_latin or "DEOE" in row_latin:
            print(f"Found in row {r}: {row_latin}")
    
    # Search columns
    for c in range(cols):
        col = [grid[r][c] for r in range(rows)]
        col_latin = runes_to_latin(col)
        if "DEOR" in col_latin or "DEOE" in col_latin:
            print(f"Found in col {c}: {col_latin}")
    
    # Search diagonals
    for start_r in range(rows):
        diag = []
        for d in range(min(rows - start_r, cols)):
            diag.append(grid[start_r + d][d])
        diag_latin = runes_to_latin(diag)
        if "DEOR" in diag_latin:
            print(f"Found in diag starting ({start_r}, 0): {diag_latin}")
    
    # What if we extract runes at prime positions and that spells something?
    print("\n--- Prime Position Extraction ---")
    
    # First 30 prime positions
    primes_under_812 = [p for p in range(2, 812) if is_prime(p)]
    prime_runes = [runes[p] for p in primes_under_812 if p < len(runes)]
    
    print(f"Runes at prime positions (first 50):")
    print(runes_to_latin(prime_runes[:50]))
    
    # What about extracting every Nth rune where N is each prime?
    print("\n--- Rearranging by Prime Values ---")
    
    # The Gematria primes are 2,3,5,...,109
    # Maybe we read every 2nd, then every 3rd, then every 5th, etc.
    
    rearranged = []
    used = set()
    for p in PRIMES_29:
        for i in range(p-1, len(runes), p):
            if i not in used:
                rearranged.append(runes[i])
                used.add(i)
    # Add remaining
    for i in range(len(runes)):
        if i not in used:
            rearranged.append(runes[i])
    
    print(f"Rearranged by prime multiples: {len(rearranged)}")
    print(runes_to_latin(rearranged[:100]))
    ioc = calculate_ioc(rearranged)
    print(f"IoC: {ioc:.4f}")
    
    # Try: Sort positions by their prime value (rune value)
    print("\n--- Sort Positions by Rune Prime Value ---")
    
    positions_by_value = sorted(range(len(runes)), key=lambda i: IDX_TO_PRIME[runes[i]])
    sorted_runes = [runes[i] for i in positions_by_value]
    
    print(f"Sorted by prime value (first 50 positions): {positions_by_value[:50]}")
    print(f"Text: {runes_to_latin(sorted_runes[:100])}")
    
    # What if the PATH is through coordinates?
    print("\n--- Prime Coordinate Path ---")
    
    # Visit (2,3), (5,7), (11,13), etc.
    path_positions = []
    for i in range(0, 29, 2):
        if i + 1 < 29:
            r, c = PRIMES_29[i] % 28, PRIMES_29[i+1] % 29
            if r < rows and c < cols:
                path_positions.append((r, c))
    
    print(f"Path: {path_positions}")
    path_runes = [grid[r][c] for r, c in path_positions]
    print(f"Runes on path: {runes_to_latin(path_runes)}")
    
    # What if columns are permuted by primes?
    print("\n--- Column Permutation by Primes ---")
    
    # Permute columns: column i goes to position primes[i] % 29
    perm = [(PRIMES_29[i] % 29) for i in range(29)]
    print(f"Permutation: {perm}")
    
    permuted_grid = []
    for r in range(rows):
        new_row = [0] * cols
        for c in range(cols):
            new_row[perm[c]] = grid[r][c]
        permuted_grid.append(new_row)
    
    permuted_runes = []
    for r in range(rows):
        permuted_runes.extend(permuted_grid[r])
    
    ioc = calculate_ioc(permuted_runes)
    print(f"Column-permuted grid IoC: {ioc:.4f}")
    print(f"Text: {runes_to_latin(permuted_runes[:100])}")
    
    # What if we sort columns by prime value of their first rune?
    print("\n--- Sort Columns by Prime Value of Header ---")
    
    col_order = sorted(range(cols), key=lambda c: IDX_TO_PRIME[grid[0][c]])
    print(f"Column order by header prime: {col_order}")
    
    reordered = []
    for r in range(rows):
        for c in col_order:
            reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {runes_to_latin(reordered[:100])}")
    
    # What about reading columns in prime order: column 2, 3, 5, 7, 11...
    print("\n--- Read Columns in Prime Order ---")
    
    prime_cols = [p for p in PRIMES_29 if p < 29]  # 2,3,5,7,11,13,17,19,23
    non_prime_cols = [c for c in range(cols) if c not in prime_cols]
    
    col_read_order = prime_cols + non_prime_cols
    print(f"Column read order: {col_read_order}")
    
    reordered = []
    for c in col_read_order:
        for r in range(rows):
            reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {runes_to_latin(reordered[:100])}")
    
    # Try rows in prime order too
    print("\n--- Read Rows in Prime Order ---")
    
    prime_rows = [p for p in PRIMES_29 if p < 28]  # 2,3,5,7,11,13,17,19,23
    non_prime_rows = [r for r in range(rows) if r not in prime_rows]
    
    row_read_order = prime_rows + non_prime_rows
    print(f"Row read order: {row_read_order}")
    
    reordered = []
    for r in row_read_order:
        for c in range(cols):
            reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {runes_to_latin(reordered[:100])}")

if __name__ == "__main__":
    main()

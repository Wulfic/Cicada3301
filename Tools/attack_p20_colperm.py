"""
Page 20 - Column Permutation Deep Dive
======================================
Column permutation by primes gave IoC 1.78! Investigate!
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

def main():
    print("="*60)
    print("PAGE 20 - COLUMN PERMUTATION DEEP DIVE")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    # The buggy permutation that gave high IoC
    buggy_perm = [(PRIMES_29[i] % 29) for i in range(29)]
    print(f"\nBuggy permutation (has duplicates): {buggy_perm}")
    print(f"Unique values: {len(set(buggy_perm))}")
    
    # Count which target positions get overwritten
    counts = collections.Counter(buggy_perm)
    print(f"Overwritten positions: {[(k, v) for k, v in counts.items() if v > 1]}")
    
    # The high IoC is because we're duplicating columns!
    # Let's see what the actual permuted text looks like
    permuted_grid = []
    for r in range(rows):
        new_row = [0] * cols
        for c in range(cols):
            new_row[buggy_perm[c]] = grid[r][c]  # Later columns overwrite earlier
        permuted_grid.append(new_row)
    
    permuted_runes = []
    for r in range(rows):
        permuted_runes.extend(permuted_grid[r])
    
    print(f"\nPermuted text (first 200 chars):")
    print(runes_to_latin(permuted_runes[:200]))
    
    # What columns ended up where?
    print("\n\nWhat column ended up in each position:")
    final_source = {}
    for c in range(cols):
        final_source[buggy_perm[c]] = c  # Last one to write wins
    print(f"Position -> Source Column: {dict(sorted(final_source.items()))}")
    
    # PROPER approach: Create valid permutations
    print("\n" + "="*60)
    print("PROPER COLUMN PERMUTATIONS")
    print("="*60)
    
    # Method 1: Sort columns by their prime value
    col_primes = [PRIMES_29[i] for i in range(29)]
    sorted_indices = sorted(range(29), key=lambda i: col_primes[i])
    print(f"\nMethod 1 - Sort by prime value: {sorted_indices}")
    
    reordered = []
    for r in range(rows):
        for c in sorted_indices:
            reordered.append(grid[r][c])
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")
    
    # Method 2: Use primes as permutation key
    # Column i goes to position (prime[i] - 1) mod 29
    perm = [(PRIMES_29[i] - 1) % 29 for i in range(29)]
    print(f"\nMethod 2 - prime[i]-1 mod 29: {perm}")
    print(f"Unique: {len(set(perm))}")
    
    if len(set(perm)) == 29:
        reordered = []
        for r in range(rows):
            new_row = [0] * cols
            for c in range(cols):
                new_row[perm[c]] = grid[r][c]
            reordered.extend(new_row)
        ioc = calculate_ioc(reordered)
        print(f"IoC: {ioc:.4f}")
    
    # Method 3: Use inverse permutation - where does each column number appear?
    # Column c goes to position where prime c appears
    print(f"\nMethod 3 - Inverse prime permutation:")
    
    # The first 29 primes, find position of each index
    # Index i -> position of prime[i] in sorted list
    sorted_primes = sorted(enumerate(PRIMES_29), key=lambda x: x[1])
    print(f"Sorted: {sorted_primes}")
    
    # Method 4: Use totient function
    print(f"\nMethod 4 - Euler totient of primes:")
    def totient(n):
        result = 0
        for i in range(1, n + 1):
            from math import gcd
            if gcd(i, n) == 1:
                result += 1
        return result
    
    perm = [totient(PRIMES_29[i]) % 29 for i in range(29)]
    print(f"Totient perm: {perm}")
    print(f"Unique: {len(set(perm))}")
    
    # Method 5: Use indices of primes mod 29 as permutation
    # But only using the primes that map to unique positions
    print(f"\nMethod 5 - Primes that give unique positions mod 29:")
    
    # Find which primes map uniquely
    seen = set()
    unique_mapping = []
    for i, p in enumerate(PRIMES_29):
        pos = p % 29
        if pos not in seen:
            unique_mapping.append((i, pos))
            seen.add(pos)
    
    print(f"Unique mappings (first 29): {unique_mapping}")
    
    # Method 6: Try different mod values
    print("\n" + "="*60)
    print("TRYING DIFFERENT MOD VALUES")
    print("="*60)
    
    for mod in [28, 29, 30, 31, 37, 41]:
        perm = [PRIMES_29[i] % mod for i in range(29)]
        unique = len(set(perm))
        if unique == 29:
            print(f"\nMod {mod}: All unique! Permutation = {perm}")
            
            reordered = []
            for r in range(rows):
                new_row = [0] * mod
                for c in range(cols):
                    if perm[c] < len(new_row):
                        new_row[perm[c]] = grid[r][c]
                reordered.extend(new_row[:cols])
            
            ioc = calculate_ioc(reordered)
            print(f"  IoC: {ioc:.4f}")
            print(f"  Text: {runes_to_latin(reordered[:80])}")
    
    # The KEY insight: Let's try reading columns in the order given by prime values
    print("\n" + "="*60)
    print("READ COLUMNS IN PRIME VALUE ORDER")
    print("="*60)
    
    # Sort column indices by their corresponding prime
    col_order = list(range(29))  # 0,1,2,...28
    # Now read them sorted by prime: 2,3,5,7,...
    # So read column 0 (prime 2), column 1 (prime 3), etc - already in order
    
    # What if we map column number to its prime value and sort?
    col_order = sorted(range(29), key=lambda c: PRIMES_29[c])
    print(f"Columns sorted by prime: {col_order}")  # Should be 0,1,2...28
    
    # Try: Read column p where p is each prime mod 29
    print("\nRead columns in prime-mod-29 order:")
    col_read_order = [(PRIMES_29[i] % 29) for i in range(29)]
    print(f"Order (with duplicates): {col_read_order}")
    
    # Remove duplicates but keep order
    seen = set()
    unique_order = []
    for c in col_read_order:
        if c not in seen:
            unique_order.append(c)
            seen.add(c)
    # Add missing columns
    for c in range(29):
        if c not in seen:
            unique_order.append(c)
            seen.add(c)
    
    print(f"Unique order: {unique_order}")
    
    reordered = []
    for c in unique_order:
        for r in range(rows):
            reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {runes_to_latin(reordered[:100])}")

if __name__ == "__main__":
    main()

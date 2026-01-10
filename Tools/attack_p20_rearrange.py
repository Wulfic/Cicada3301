"""
Page 20 - "Rearranging Primes" Interpretation Attack
=====================================================
Exploring different interpretations of the P19 hint.

Key insight: "Rearranging the primes numbers will show a path to the Deor K"

Interpretations:
1. The SEQUENCE of primes (2,3,5,7,11...) defines a reading order
2. "Rearranging" means SORTING or PERMUTING the primes
3. The "path" could be a grid traversal order
4. "Deor K" likely means "Deor Key" - use after transposition
"""

import collections
import itertools

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

ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def get_primes_up_to(n):
    return [i for i in range(2, n+1) if is_prime(i)]

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

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    try:
        with open(deor_path, 'r', encoding='utf-8') as f:
            text = f.read().upper()
    except:
        return []
    return [ENGLISH_TO_IDX.get(c, 0) for c in text if c in ENGLISH_TO_IDX]

def main():
    print("="*60)
    print("PAGE 20 - PRIME REARRANGEMENT ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    
    print(f"Loaded {len(runes)} runes")
    print(f"Deor length: {len(deor)}")
    
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    primes_812 = get_primes_up_to(10000)[:812]
    primes_29 = get_primes_up_to(120)[:29]
    primes_28 = get_primes_up_to(120)[:28]
    
    results = []
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 1: Read positions in order of prime value at that position")
    print("="*60)
    # For each position, assign value (row_prime * col_prime), then sort
    
    positions = []
    for r in range(rows):
        for c in range(cols):
            # Prime number for row and column
            row_prime = primes_28[r] if r < len(primes_28) else r + 2
            col_prime = primes_29[c] if c < len(primes_29) else c + 2
            product = row_prime * col_prime
            positions.append((product, r, c))
    
    positions.sort()  # Sort by prime product
    
    reordered = []
    for _, r, c in positions:
        if c < len(grid[r]):
            reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    results.append(("Sort by row*col prime product", ioc, reordered))
    print(f"IoC: {ioc:.4f}")
    print(f"Preview: {runes_to_latin(reordered[:100])}")
    
    # Apply Deor
    key = deor * (len(reordered) // len(deor) + 1)
    key = key[:len(reordered)]
    decrypted = [(reordered[i] - key[i]) % 29 for i in range(len(reordered))]
    ioc2 = calculate_ioc(decrypted)
    print(f"After Deor SUB: IoC={ioc2:.4f}")
    print(f"Preview: {runes_to_latin(decrypted[:100])}")
    results.append(("Prime product sort + Deor", ioc2, decrypted))
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 2: Read columns in order of nth prime")
    print("="*60)
    # Column 0 at position prime(0)=2, column 1 at position prime(1)=3, etc.
    
    col_order = list(range(29))
    col_order.sort(key=lambda c: primes_29[c] if c < len(primes_29) else 1000)
    
    reordered = []
    for r in range(rows):
        for c in col_order:
            if c < len(grid[r]):
                reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    results.append(("Columns sorted by prime(col)", ioc, reordered))
    print(f"IoC: {ioc:.4f}")
    print(f"Column order: {col_order}")
    print(f"Preview: {runes_to_latin(reordered[:100])}")
    
    # Apply Deor
    decrypted = [(reordered[i] - key[i]) % 29 for i in range(len(reordered))]
    ioc2 = calculate_ioc(decrypted)
    print(f"After Deor SUB: IoC={ioc2:.4f}")
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 3: Use prime permutation (mod 29) for column order")
    print("="*60)
    # Order columns by their prime VALUE mod 29
    
    col_order = list(range(29))
    col_order.sort(key=lambda c: primes_29[c] % 29 if c < len(primes_29) else 1000)
    
    reordered = []
    for r in range(rows):
        for c in col_order:
            if c < len(grid[r]):
                reordered.append(grid[r][c])
    
    ioc = calculate_ioc(reordered)
    results.append(("Columns sorted by prime(col) mod 29", ioc, reordered))
    print(f"IoC: {ioc:.4f}")
    print(f"Column order: {col_order}")
    
    # Apply Deor
    decrypted = [(reordered[i] - key[i]) % 29 for i in range(len(reordered))]
    ioc2 = calculate_ioc(decrypted)
    print(f"After Deor SUB: IoC={ioc2:.4f}")
    print(f"Preview: {runes_to_latin(decrypted[:100])}")
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 4: Discrete log permutation")
    print("="*60)
    # 29 is prime. Find primitive root g, then column order is g^0, g^1, g^2...
    
    # Primitive roots mod 29: 2, 3, 8, 10, 11, 14, 15, 18, 19, 21, 26, 27
    primitive_roots = [2, 3, 8, 10, 11, 14, 15, 18, 19, 21, 26, 27]
    
    for g in primitive_roots[:4]:  # Test first few
        col_order = []
        seen = set()
        power = 1
        for _ in range(28):
            col = power % 29
            if col not in seen and col < 29:
                col_order.append(col)
                seen.add(col)
            power = (power * g) % 29
        
        # Add column 0 if not seen
        if 0 not in seen:
            col_order.append(0)
        
        if len(col_order) != 29:
            continue
        
        reordered = []
        for r in range(rows):
            for c in col_order:
                if c < len(grid[r]):
                    reordered.append(grid[r][c])
        
        ioc = calculate_ioc(reordered)
        print(f"Primitive root g={g}: IoC={ioc:.4f}")
        
        # Apply Deor
        decrypted = [(reordered[i] - key[i]) % 29 for i in range(len(reordered))]
        ioc2 = calculate_ioc(decrypted)
        print(f"  After Deor SUB: IoC={ioc2:.4f}")
        print(f"  Preview: {runes_to_latin(decrypted[:80])}")
        results.append((f"Discrete log g={g} + Deor", ioc2, decrypted))
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 5: Interleave by prime residue classes")
    print("="*60)
    # Positions where index mod small_prime == k
    
    for p in [2, 3, 5, 7]:
        for k in range(p):
            subset = [runes[i] for i in range(len(runes)) if i % p == k]
            if len(subset) > 50:
                ioc = calculate_ioc(subset)
                if ioc > 1.1:
                    print(f"Positions where idx mod {p} == {k}: n={len(subset)}, IoC={ioc:.4f}")
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 6: Read in prime-gap order")
    print("="*60)
    # Read position 2, then skip gap(2)=1, then 3, skip gap(3)=2...
    
    prime_gaps = [primes_812[i+1] - primes_812[i] for i in range(len(primes_812)-1)]
    
    reordered = []
    pos = 0
    visited = set()
    for gap in prime_gaps[:len(runes)]:
        if pos < len(runes) and pos not in visited:
            reordered.append(runes[pos])
            visited.add(pos)
        pos = (pos + gap) % len(runes)
    
    # Fill in unvisited
    for i in range(len(runes)):
        if i not in visited:
            reordered.append(runes[i])
    
    ioc = calculate_ioc(reordered)
    print(f"Prime gap traversal: IoC={ioc:.4f}")
    print(f"Preview: {runes_to_latin(reordered[:80])}")
    
    # Apply Deor
    decrypted = [(reordered[i] - key[i]) % 29 for i in range(len(reordered))]
    ioc2 = calculate_ioc(decrypted)
    print(f"After Deor SUB: IoC={ioc2:.4f}")
    print(f"Preview: {runes_to_latin(decrypted[:80])}")
    
    # ====================================================================
    print("\n" + "="*60)
    print("ATTACK 7: Sieve-based column extraction")
    print("="*60)
    # Use Sieve of Eratosthenes pattern on grid
    
    # Mark positions as "crossed out" like in sieve
    sieved = []
    crossed_out = set()
    
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        for i in range(p, len(runes), p):
            crossed_out.add(i)
    
    not_crossed = [i for i in range(len(runes)) if i not in crossed_out]
    crossed = [i for i in range(len(runes)) if i in crossed_out]
    
    print(f"Not crossed out: {len(not_crossed)}")
    print(f"Crossed out: {len(crossed)}")
    
    # Read not-crossed positions
    subset_nc = [runes[i] for i in not_crossed]
    ioc = calculate_ioc(subset_nc)
    print(f"Not-crossed positions: IoC={ioc:.4f}")
    print(f"Preview: {runes_to_latin(subset_nc[:80])}")
    
    # ====================================================================
    print("\n" + "="*60)
    print("TOP RESULTS")
    print("="*60)
    
    results.sort(key=lambda x: x[1], reverse=True)
    for name, ioc, text in results[:10]:
        print(f"\n{name}: IoC={ioc:.4f}")
        print(f"  {runes_to_latin(text[:100])}")

if __name__ == "__main__":
    main()

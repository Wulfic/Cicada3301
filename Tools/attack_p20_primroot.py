"""
Page 20 - Primitive Root Path Attack
=====================================
29 is prime, use primitive roots to create "rearranging" permutations.
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

ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

PRIMES_29 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    with open(deor_path, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    return [ENGLISH_TO_IDX.get(c, 0) for c in text if c in ENGLISH_TO_IDX]

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

def primitive_roots(p):
    """Find all primitive roots of prime p."""
    roots = []
    for g in range(2, p):
        # Check if g is a primitive root
        powers = set()
        val = 1
        for _ in range(p - 1):
            val = (val * g) % p
            powers.add(val)
        if len(powers) == p - 1:
            roots.append(g)
    return roots

def generate_permutation(g, p):
    """Generate permutation using primitive root g mod p."""
    perm = []
    val = 1
    for _ in range(p - 1):
        perm.append(val)
        val = (val * g) % p
    return perm

def main():
    print("="*60)
    print("PAGE 20 - PRIMITIVE ROOT PATH ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    # Find primitive roots of 29
    roots = primitive_roots(29)
    print(f"\nPrimitive roots of 29: {roots}")
    
    # Test each primitive root
    best_ioc = 0
    best_config = None
    
    for g in roots:
        perm = generate_permutation(g, 29)  # Values 1-28
        
        # Use as column order (subtract 1 to get 0-27, add 28 for col 28)
        col_order = [p - 1 for p in perm]  # 0-27
        col_order.append(28)  # Add column 28 at the end
        
        # Also try: use permutation to read columns
        for method in ['col_order', 'row_order']:
            if method == 'col_order':
                # Read columns in primitive root order
                reordered = []
                for c in col_order:
                    for r in range(rows):
                        reordered.append(grid[r][c])
            else:
                # Read rows using primitive root order
                row_order = [p - 1 for p in perm[:28]]
                reordered = []
                for r in row_order:
                    for c in range(cols):
                        reordered.append(grid[r][c])
            
            ioc = calculate_ioc(reordered)
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_config = (g, method, reordered)
        
        # Try applying Deor after rearrangement
        col_order = [p - 1 for p in perm]
        col_order.append(28)
        
        reordered = []
        for c in col_order:
            for r in range(rows):
                reordered.append(grid[r][c])
        
        extended_deor = deor * (len(reordered) // len(deor) + 1)
        extended_deor = extended_deor[:len(reordered)]
        
        for mode in ['sub', 'add']:
            result = decrypt_vigenere(reordered, extended_deor, mode)
            ioc = calculate_ioc(result)
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_config = (f"g={g}, {method}, Deor {mode}", 'combined', result)
    
    print(f"\nBest result: IoC={best_ioc:.4f}")
    if best_config:
        print(f"Config: {best_config[0]}, {best_config[1]}")
        print(f"Text: {runes_to_latin(best_config[2][:150])}")
    
    # Try a more sophisticated approach: Use primitive root to create spiral/path
    print("\n" + "="*60)
    print("SPIRAL/PATH USING PRIMITIVE ROOTS")
    print("="*60)
    
    for g in [2, 3]:  # Most common primitive roots
        perm = generate_permutation(g, 29)
        print(f"\ng={g}: {perm}")
        
        # Path: visit (row[i], col[i]) where row and col follow primitive root
        path_runes = []
        visited = set()
        
        for r_idx in range(28):
            r = (perm[r_idx % 28] - 1) if r_idx < 28 else r_idx
            for c_idx in range(29):
                c = perm[c_idx % 28] - 1 if c_idx < 28 else c_idx
                pos = r * cols + c
                if pos not in visited and r < rows and c < cols:
                    path_runes.append(grid[r][c])
                    visited.add(pos)
        
        # Add any missed
        for i in range(len(runes)):
            if i not in visited:
                path_runes.append(runes[i])
        
        ioc = calculate_ioc(path_runes)
        print(f"Spiral path IoC: {ioc:.4f}")
        print(f"Text: {runes_to_latin(path_runes[:80])}")
        
        # Apply Deor
        extended_deor = deor * (len(path_runes) // len(deor) + 1)
        extended_deor = extended_deor[:len(path_runes)]
        
        result = decrypt_vigenere(path_runes, extended_deor, 'sub')
        ioc = calculate_ioc(result)
        print(f"After Deor: IoC={ioc:.4f}")
        print(f"Text: {runes_to_latin(result[:80])}")
    
    # What if "rearranging primes" means sorting runes BY THEIR PRIME VALUES?
    print("\n" + "="*60)
    print("SORT RUNES BY PRIME VALUE, THEN APPLY DEOR")
    print("="*60)
    
    # Create list of (position, rune_index, prime_value)
    rune_data = [(i, runes[i], PRIMES_29[runes[i]]) for i in range(len(runes))]
    
    # Sort by prime value
    sorted_by_prime = sorted(rune_data, key=lambda x: x[2])
    sorted_positions = [x[0] for x in sorted_by_prime]
    sorted_runes = [x[1] for x in sorted_by_prime]
    
    print(f"First 20 positions after sorting: {sorted_positions[:20]}")
    print(f"Original positions: Those with F (prime 2) come first, then U (prime 3), etc.")
    
    # Now read the ciphertext in this sorted order
    rearranged = sorted_runes
    
    ioc = calculate_ioc(rearranged)
    print(f"\nSorted runes IoC: {ioc:.4f}")
    
    # The sorted runes are just FFFFF...UUUU...THTH... (grouped by letter)
    # Not useful directly. But what if we use the POSITIONS as a reading order?
    
    print("\nUsing sorted positions as reading order for ORIGINAL text:")
    # Read original text in the order given by sorted positions
    reordered = [runes[p] for p in sorted_positions]
    
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")
    # This is same as above... 
    
    # What about: Sort positions, then read the rune at the INVERSE position?
    print("\nInverse permutation:")
    inverse_perm = [0] * len(runes)
    for new_pos, old_pos in enumerate(sorted_positions):
        inverse_perm[old_pos] = new_pos
    
    reordered = [runes[inverse_perm[i]] for i in range(len(runes))]
    ioc = calculate_ioc(reordered)
    print(f"IoC: {ioc:.4f}")

if __name__ == "__main__":
    main()

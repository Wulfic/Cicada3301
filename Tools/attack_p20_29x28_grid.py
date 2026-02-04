#!/usr/bin/env python3
"""
Attack Page 20 using a 29×28 grid approach.
812 runes = 29 × 28, where 29 is the Gematria Primus alphabet size.

This explores various reading paths through the grid.
"""

import sys
sys.path.insert(0, 'c:/Users/tyler/Repos/Cicada3301/Tools')

# Gematria Primus - runes and their values
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"
RUNEGLISH = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIAŒEA"  # Simplified

def load_runes(filepath):
    """Load runes from file, remove delimiters."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    runes = [c for c in text if c in RUNES]
    return runes

def rune_to_idx(r):
    """Convert rune to index 0-28."""
    return RUNES.index(r) if r in RUNES else -1

def idx_to_runeglish(idx):
    """Convert index to runeglish character."""
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIAŒEA"[:29]
    return mapping[idx % 29] if 0 <= idx < 29 else '?'

def calc_ioc(indices):
    """Calculate Index of Coincidence."""
    if len(indices) < 2:
        return 0
    from collections import Counter
    counts = Counter(indices)
    n = len(indices)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1) / 29) if n > 1 else 0

def load_deor():
    """Load Deor poem as runeglish indices."""
    filepath = 'c:/Users/tyler/Repos/Cicada3301/Analysis/Reference_Docs/deor_poem.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    # Map to indices
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIAŒEA"[:29]
    alt_map = {'A': 24, 'E': 18, 'O': 4, 'Y': 28}  # Vowel mappings
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in ['TH', 'EA', 'NG', 'OE', 'AE', 'IO', 'IA', 'EO']:
                if digraph == 'TH': indices.append(2)
                elif digraph == 'EA': indices.append(27)
                elif digraph == 'NG': indices.append(21)
                elif digraph == 'OE': indices.append(27)  
                elif digraph == 'AE': indices.append(25)
                elif digraph == 'IO': indices.append(12)
                elif digraph == 'IA': indices.append(26)
                elif digraph == 'EO': indices.append(12)
                i += 2
                continue
        c = text[i]
        if c in mapping:
            indices.append(mapping.index(c))
        elif c in alt_map:
            indices.append(alt_map[c])
        elif c.isalpha():
            # Simple fallback
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                idx = ord(c) - ord('A')
                indices.append(idx % 29)
        i += 1
    return indices

def decrypt_beaufort(cipher_indices, key_indices):
    """Beaufort: P = (K - C) mod 29"""
    result = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (k - c) % 29
        result.append(p)
    return result

def decrypt_vigenere_sub(cipher_indices, key_indices):
    """Vigenère SUB: P = (C - K) mod 29"""
    result = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (c - k) % 29
        result.append(p)
    return result

def indices_to_text(indices):
    """Convert indices to text."""
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    return ''.join(mapping[i % 29] for i in indices)

def read_grid_path(runes, rows, cols, path_type):
    """Read runes from grid in various paths."""
    grid = []
    idx = 0
    for r in range(rows):
        row = []
        for c in range(cols):
            if idx < len(runes):
                row.append(runes[idx])
                idx += 1
            else:
                row.append(None)
        grid.append(row)
    
    result = []
    
    if path_type == 'col_major':
        # Read column by column
        for c in range(cols):
            for r in range(rows):
                if grid[r][c] is not None:
                    result.append(grid[r][c])
                    
    elif path_type == 'col_major_reverse':
        # Read column by column, columns in reverse
        for c in range(cols-1, -1, -1):
            for r in range(rows):
                if grid[r][c] is not None:
                    result.append(grid[r][c])
                    
    elif path_type == 'snake_row':
        # Snake pattern by rows
        for r in range(rows):
            if r % 2 == 0:
                for c in range(cols):
                    if grid[r][c] is not None:
                        result.append(grid[r][c])
            else:
                for c in range(cols-1, -1, -1):
                    if grid[r][c] is not None:
                        result.append(grid[r][c])
                        
    elif path_type == 'snake_col':
        # Snake pattern by columns
        for c in range(cols):
            if c % 2 == 0:
                for r in range(rows):
                    if grid[r][c] is not None:
                        result.append(grid[r][c])
            else:
                for r in range(rows-1, -1, -1):
                    if grid[r][c] is not None:
                        result.append(grid[r][c])
                        
    elif path_type == 'diagonal_down':
        # Diagonal reading (top-left to bottom-right diagonals)
        for d in range(rows + cols - 1):
            for r in range(rows):
                c = d - r
                if 0 <= c < cols and grid[r][c] is not None:
                    result.append(grid[r][c])
                    
    elif path_type == 'diagonal_up':
        # Anti-diagonal reading
        for d in range(rows + cols - 1):
            for r in range(rows-1, -1, -1):
                c = d - (rows - 1 - r)
                if 0 <= c < cols and grid[r][c] is not None:
                    result.append(grid[r][c])
                    
    elif path_type == 'spiral_in':
        # Spiral inward
        top, bottom, left, right = 0, rows-1, 0, cols-1
        while top <= bottom and left <= right:
            for c in range(left, right+1):
                if grid[top][c] is not None:
                    result.append(grid[top][c])
            top += 1
            for r in range(top, bottom+1):
                if grid[r][right] is not None:
                    result.append(grid[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left-1, -1):
                    if grid[bottom][c] is not None:
                        result.append(grid[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top-1, -1):
                    if grid[r][left] is not None:
                        result.append(grid[r][left])
                left += 1
    
    return result

def main():
    print("=" * 60)
    print("Page 20 - 29×28 Grid Attack")
    print("812 runes = 29 × 28 (29 = alphabet size)")
    print("=" * 60)
    
    # Load Page 20 runes
    p20_runes = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    print(f"\nLoaded {len(p20_runes)} runes from Page 20")
    
    if len(p20_runes) != 812:
        print(f"WARNING: Expected 812 runes, got {len(p20_runes)}")
    
    # Load Deor
    deor = load_deor()
    print(f"Loaded {len(deor)} chars from Deor")
    
    # Grid configurations
    configs = [
        (29, 28, "29 rows × 28 cols"),
        (28, 29, "28 rows × 29 cols"),
        (14, 58, "14 rows × 58 cols"),
        (58, 14, "58 rows × 14 cols"),
        (7, 116, "7 rows × 116 cols"),
        (116, 7, "116 rows × 7 cols"),
    ]
    
    paths = ['col_major', 'col_major_reverse', 'snake_row', 'snake_col', 
             'diagonal_down', 'diagonal_up', 'spiral_in']
    
    best_ioc = 0
    best_config = None
    
    for rows, cols, desc in configs:
        print(f"\n{'='*50}")
        print(f"Grid: {desc}")
        print("=" * 50)
        
        for path in paths:
            # Read in path order
            reordered = read_grid_path(p20_runes, rows, cols, path)
            reordered_indices = [rune_to_idx(r) for r in reordered]
            
            # Try different ciphers
            for cipher_name, cipher_func in [
                ('Beaufort', decrypt_beaufort),
                ('Vigenère SUB', decrypt_vigenere_sub),
            ]:
                decrypted = cipher_func(reordered_indices, deor)
                ioc = calc_ioc(decrypted)
                
                if ioc > 1.5:
                    text = indices_to_text(decrypted[:100])
                    print(f"  {path:20} + {cipher_name:12}: IoC = {ioc:.2f} ** PROMISING **")
                    print(f"    Preview: {text[:60]}")
                    
                    if ioc > best_ioc:
                        best_ioc = ioc
                        best_config = (desc, path, cipher_name, decrypted)
                        
                elif ioc > 1.2:
                    print(f"  {path:20} + {cipher_name:12}: IoC = {ioc:.2f}")
    
    # Also try: sort primes by rune value as reordering
    print("\n" + "=" * 60)
    print("BONUS: Sort prime positions by rune value")
    print("=" * 60)
    
    def is_prime(n):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5)+1, 2):
            if n % i == 0: return False
        return True
    
    primes = [i for i in range(2, 813) if is_prime(i)][:166]
    p20_indices = [rune_to_idx(r) for r in p20_runes]
    
    # Sort primes by the rune value at that position
    prime_with_value = [(p, p20_indices[p] if p < len(p20_indices) else 0) for p in primes]
    sorted_by_value = sorted(prime_with_value, key=lambda x: x[1])
    
    reordered_primes = [p for p, v in sorted_by_value]
    
    # Read prime positions in this new order
    prime_stream = [p20_indices[p] for p in reordered_primes if p < len(p20_indices)]
    
    # Decrypt with Deor
    for cipher_name, cipher_func in [
        ('Beaufort', decrypt_beaufort),
        ('Vigenère SUB', decrypt_vigenere_sub),
    ]:
        decrypted = cipher_func(prime_stream, deor)
        ioc = calc_ioc(decrypted)
        text = indices_to_text(decrypted[:100])
        print(f"Primes sorted by rune value + {cipher_name}: IoC = {ioc:.2f}")
        print(f"  Preview: {text[:60]}")
    
    # Try sorting primes by prime value modulo various numbers
    print("\n" + "=" * 60)
    print("BONUS 2: Sort primes by p mod N")
    print("=" * 60)
    
    for mod in [29, 28, 7, 11, 13, 17, 19, 23]:
        sorted_primes = sorted(primes, key=lambda p: (p % mod, p))
        prime_stream = [p20_indices[p] for p in sorted_primes if p < len(p20_indices)]
        
        decrypted = decrypt_beaufort(prime_stream, deor)
        ioc = calc_ioc(decrypted)
        
        if ioc > 1.2:
            text = indices_to_text(decrypted[:60])
            print(f"Primes sorted by p mod {mod:2}: IoC = {ioc:.2f}")
            print(f"  Preview: {text}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if best_config:
        desc, path, cipher, decrypted = best_config
        print(f"Best IoC: {best_ioc:.2f}")
        print(f"Config: {desc}, Path: {path}, Cipher: {cipher}")
        print(f"Full text:\n{indices_to_text(decrypted)}")
    else:
        print("No configuration achieved IoC > 1.5")
        print("Highest grid IoC likely around 1.0-1.2")

if __name__ == '__main__':
    main()

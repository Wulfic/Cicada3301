"""
Page 20 - Prime Coordinate Path
===============================
Follow prime numbers as (row, col) coordinates through the grid.
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

def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

PRIMES = sieve_of_eratosthenes(10000)

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    with open(deor_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return ''.join(c for c in text.upper() if c.isalpha())

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
    print("PAGE 20 - PRIME COORDINATE PATH")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    rows, cols = 28, 29
    grid = [[runes[r*cols + c] for c in range(cols)] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    deor_key = [ENGLISH_TO_IDX.get(c, 0) for c in deor]
    
    # Method 1: Use consecutive primes as (row, col) pairs
    print("\n--- Method 1: Prime pairs as (row, col) ---")
    
    path = []
    for i in range(0, len(PRIMES)-1, 2):
        r = PRIMES[i] % rows
        c = PRIMES[i+1] % cols
        path.append((r, c))
        if len(path) >= len(runes):
            break
    
    print(f"First 10 coordinates: {path[:10]}")
    
    path_runes = [grid[r][c] for r, c in path[:len(runes)]]
    ioc = calculate_ioc(path_runes)
    print(f"Path reading: IoC={ioc:.4f}")
    
    # Method 2: Use prime[i] mod rows as row, prime[i+1] mod cols as col
    # But read ENTIRE grid following this path order
    print("\n--- Method 2: Full grid traversal using prime path ---")
    
    visited = set()
    path_runes = []
    for i in range(len(PRIMES)):
        r = PRIMES[i] % rows
        c = PRIMES[i] % cols
        if (r, c) not in visited:
            path_runes.append(grid[r][c])
            visited.add((r, c))
    
    # Fill in remaining
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                path_runes.append(grid[r][c])
    
    ioc = calculate_ioc(path_runes)
    print(f"Full grid via prime path: IoC={ioc:.4f}")
    
    # Apply Deor
    extended_deor = deor_key * (len(path_runes) // len(deor_key) + 1)
    extended_deor = extended_deor[:len(path_runes)]
    
    result = decrypt_vigenere(path_runes, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"After Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 3: Row = prime[i] mod 28, Col = prime[j] for all combinations
    print("\n--- Method 3: Prime row × Prime col intersection ---")
    
    prime_rows = [p % rows for p in PRIMES[:10]]  # First 10 primes mod 28
    prime_cols = [p for p in PRIMES if p < cols]  # Primes < 29
    
    print(f"Prime rows: {prime_rows}")
    print(f"Prime cols: {prime_cols}")
    
    intersection_runes = []
    for r in prime_rows:
        for c in prime_cols:
            intersection_runes.append(grid[r][c])
    
    print(f"Intersection cells: {len(intersection_runes)}")
    print(f"Text: {runes_to_latin(intersection_runes)}")
    
    ioc = calculate_ioc(intersection_runes)
    print(f"IoC: {ioc:.4f}")
    
    # Method 4: Read at positions where linear index is prime
    print("\n--- Method 4: Linear prime positions ---")
    
    primes_under_812 = [p for p in PRIMES if p < len(runes)]
    non_primes = [i for i in range(len(runes)) if i not in primes_under_812]
    
    prime_pos_runes = [runes[p] for p in primes_under_812]
    print(f"Prime positions: {len(prime_pos_runes)}")
    print(f"Text: {runes_to_latin(prime_pos_runes[:80])}")
    
    ioc = calculate_ioc(prime_pos_runes)
    print(f"IoC: {ioc:.4f}")
    
    # Use prime positions as key for non-prime positions
    non_prime_runes = [runes[i] for i in non_primes]
    
    extended_key = prime_pos_runes * (len(non_prime_runes) // len(prime_pos_runes) + 1)
    extended_key = extended_key[:len(non_prime_runes)]
    
    result = decrypt_vigenere(non_prime_runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Non-prime positions with prime-positions-key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Method 5: Rearrange by sorting positions based on their smallest prime factor
    print("\n--- Method 5: Sort by smallest prime factor ---")
    
    def smallest_prime_factor(n):
        if n < 2:
            return 0
        for p in PRIMES:
            if p > n:
                return n
            if n % p == 0:
                return p
        return n
    
    positions = list(range(len(runes)))
    sorted_positions = sorted(positions, key=lambda x: (smallest_prime_factor(x), x))
    
    reordered = [runes[p] for p in sorted_positions]
    ioc = calculate_ioc(reordered)
    print(f"Sorted by SPF: IoC={ioc:.4f}")
    
    # Apply Deor
    result = decrypt_vigenere(reordered, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"After Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")

if __name__ == "__main__":
    main()

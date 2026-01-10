"""
Page 20 - Prime Path Attack
============================
Use primes to define a reading path through the 29x28 grid.
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

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def get_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

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
    print("PAGE 20 - PRIME PATH ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    deor_key = [ENGLISH_TO_IDX.get(c, 0) for c in deor]
    
    rows, cols = 28, 29
    grid = [[runes[r*cols + c] for c in range(cols)] for r in range(rows)]
    
    primes = get_primes(1000)  # First 1000 primes
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    print(f"812 = 28 × 29 = 4 × 7 × 29")
    print(f"28 = 4 × 7 (7 = Deor strophes)")
    print(f"29 = alphabet size = 10th prime")
    
    # Method 1: prime[i] mod 812 as reading order
    print("\n--- Method 1: Read positions prime[i] mod 812 ---")
    
    positions = [primes[i] % 812 for i in range(812)]
    # Check if we have all positions (likely not)
    unique_pos = set(positions)
    print(f"Unique positions: {len(unique_pos)} / 812")
    
    # Just extract the first 200 unique positions
    seen = set()
    path = []
    for p in positions:
        if p not in seen:
            path.append(p)
            seen.add(p)
        if len(path) >= 300:
            break
    
    extracted = [runes[p] for p in path]
    key_ext = deor_key[:len(extracted)]
    result = decrypt_vigenere(extracted, key_ext, 'sub')
    ioc = calculate_ioc(result)
    print(f"prime[i]%%812 path + Deor: IoC={ioc:.4f} (n={len(result)})")
    print(f"Text: {runes_to_latin(result[:60])}")
    
    # Method 2: (prime[i] mod 28, prime[i] mod 29) as (row, col)
    print("\n--- Method 2: (prime[i]%%28, prime[i]%%29) as (row, col) ---")
    
    coords = []
    seen = set()
    for i, p in enumerate(primes[:812]):
        r, c = p % 28, p % 29
        if (r, c) not in seen:
            coords.append((r, c))
            seen.add((r, c))
    
    extracted = [grid[r][c] for r, c in coords]
    print(f"Unique cells: {len(extracted)}")
    
    key_ext = deor_key[:len(extracted)]
    result = decrypt_vigenere(extracted, key_ext, 'sub')
    ioc = calculate_ioc(result)
    print(f"(r,c) from prime + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:60])}")
    
    # Method 3: Sort runes by their Gematria prime value
    print("\n--- Method 3: Sort grid by Gematria prime values ---")
    
    GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                       53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    # Each rune has a Gematria prime value
    rune_primes = [(GEMATRIA_PRIMES[r], i, r) for i, r in enumerate(runes)]
    sorted_runes = sorted(rune_primes)
    sorted_indices = [r for _, _, r in sorted_runes]
    
    key_ext = deor_key[:len(sorted_indices)]
    result = decrypt_vigenere(sorted_indices, key_ext, 'sub')
    ioc = calculate_ioc(result)
    print(f"Sorted by Gematria prime + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:60])}")
    
    # Method 4: Inverse - sort positions by prime value
    print("\n--- Method 4: Read in order sorted by prime[position] ---")
    
    # For each position, compute prime[position], then sort by that
    pos_primes = [(primes[i], i, runes[i]) for i in range(len(runes))]
    sorted_by_pos_prime = sorted(pos_primes)
    reordered = [r for _, _, r in sorted_by_pos_prime]
    
    key_ext = deor_key[:len(reordered)]
    result = decrypt_vigenere(reordered, key_ext, 'sub')
    ioc = calculate_ioc(result)
    print(f"Sorted by prime[pos] + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:60])}")
    
    # Method 5: Read columns in prime order [2,3,5,7,11,13,17,19,23] then non-primes
    print("\n--- Method 5: Prime columns first, then non-prime columns ---")
    
    prime_cols = [c for c in range(29) if is_prime(c)]  # [2,3,5,7,11,13,17,19,23]
    non_prime_cols = [c for c in range(29) if not is_prime(c)]
    col_order = prime_cols + non_prime_cols
    print(f"Column order: {col_order}")
    
    reordered = []
    for c in col_order:
        for r in range(rows):
            reordered.append(grid[r][c])
    
    key_ext = deor_key[:len(reordered)]
    result = decrypt_vigenere(reordered, key_ext, 'sub')
    ioc = calculate_ioc(result)
    print(f"Prime cols first + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:60])}")
    
    # Method 6: What if "rearranging" means inverse permutation?
    print("\n--- Method 6: Inverse prime permutation ---")
    
    # The first 29 primes mod 29: [2,3,5,7,11,13,17,19,23,0,2,8,12,14,18,24,1,3,9,13,15,21,25,2,10,14,16,20,22]
    perm = [primes[i] % 29 for i in range(29)]
    print(f"Perm: {perm}")
    
    # Create inverse: for each value 0-28, find first index where it appears
    inverse = {}
    for i, v in enumerate(perm):
        if v not in inverse:
            inverse[v] = i
    
    # Fill in missing with remaining indices
    remaining = [i for i in range(29) if i not in inverse.values()]
    for v in range(29):
        if v not in inverse:
            if remaining:
                inverse[v] = remaining.pop(0)
            else:
                inverse[v] = v  # fallback
    
    inv_perm = [inverse[i] for i in range(29)]
    print(f"Inv perm: {inv_perm}")
    
    # Apply inverse permutation to columns
    reordered = []
    for r in range(rows):
        for c in range(cols):
            new_c = inv_perm[c]
            reordered.append(grid[r][new_c])
    
    key_ext = deor_key[:len(reordered)]
    result = decrypt_vigenere(reordered, key_ext, 'sub')
    ioc = calculate_ioc(result)
    print(f"Inverse perm + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:60])}")

if __name__ == "__main__":
    main()

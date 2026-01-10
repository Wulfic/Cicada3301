"""
Page 20 - Deep Deor Analysis
============================
Looking for any systematic relationship between primes and Deor.
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

GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

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

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    with open(deor_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def main():
    print("="*60)
    print("PAGE 20 - DEEP DEOR ANALYSIS")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor_text = load_deor()
    deor_clean = ''.join(c for c in deor_text.upper() if c.isalpha())
    
    print(f"Page 20: {len(runes)} runes")
    print(f"Deor: {len(deor_clean)} letters")
    
    # Try reading Deor at positions defined by the GRID positions
    print("\n" + "="*60)
    print("METHOD 1: Grid position mod Deor length")
    print("="*60)
    
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    # For each grid position (r, c), read Deor at position (r*29 + c) % len(deor)
    key_from_grid = []
    for r in range(rows):
        for c in range(cols):
            pos = (r * cols + c) % len(deor_clean)
            char = deor_clean[pos]
            key_from_grid.append(ENGLISH_TO_IDX.get(char, 0))
    
    result = decrypt_vigenere(runes, key_from_grid, 'sub')
    ioc = calculate_ioc(result)
    print(f"Grid position -> Deor position: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Try: Position is (row prime * col prime) mod deor_len
    print("\n" + "="*60)
    print("METHOD 2: (Row prime × Col prime) mod Deor")
    print("="*60)
    
    key_from_primes = []
    for r in range(rows):
        row_prime = GEMATRIA_PRIMES[r] if r < 29 else GEMATRIA_PRIMES[r % 29]
        for c in range(cols):
            col_prime = GEMATRIA_PRIMES[c]
            pos = (row_prime * col_prime) % len(deor_clean)
            char = deor_clean[pos]
            key_from_primes.append(ENGLISH_TO_IDX.get(char, 0))
    
    result = decrypt_vigenere(runes, key_from_primes, 'sub')
    ioc = calculate_ioc(result)
    print(f"Row_prime × Col_prime -> Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Try: Cipher rune value is the step size through Deor
    print("\n" + "="*60)
    print("METHOD 3: Cipher value as step through Deor")
    print("="*60)
    
    pos = 0
    result = []
    for c in runes:
        char = deor_clean[pos % len(deor_clean)]
        key_val = ENGLISH_TO_IDX.get(char, 0)
        result.append((c - key_val) % 29)
        pos += c + 1  # Step by cipher value + 1
    
    ioc = calculate_ioc(result)
    print(f"Step by cipher+1: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Try stepping by prime value of cipher
    pos = 0
    result = []
    for c in runes:
        char = deor_clean[pos % len(deor_clean)]
        key_val = ENGLISH_TO_IDX.get(char, 0)
        result.append((c - key_val) % 29)
        pos += GEMATRIA_PRIMES[c]
    
    ioc = calculate_ioc(result)
    print(f"Step by cipher prime: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if the "rearranging" means we permute the Deor poem characters?
    print("\n" + "="*60)
    print("METHOD 4: Permute Deor by prime sequence")
    print("="*60)
    
    # Rearrange Deor: take chars at prime positions, then non-prime
    prime_chars = []
    non_prime_chars = []
    for i, c in enumerate(deor_clean):
        if is_prime(i + 1):  # 1-indexed
            prime_chars.append(c)
        else:
            non_prime_chars.append(c)
    
    rearranged_deor = ''.join(prime_chars) + ''.join(non_prime_chars)
    print(f"Rearranged Deor: primes first ({len(prime_chars)}), then non-primes ({len(non_prime_chars)})")
    
    # Use as running key
    key = [ENGLISH_TO_IDX.get(c, 0) for c in rearranged_deor]
    extended_key = key * (len(runes) // len(key) + 1)
    extended_key = extended_key[:len(runes)]
    
    result = decrypt_vigenere(runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Rearranged Deor as key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Try: Sort Deor chars by their position's prime value
    print("\n" + "="*60)
    print("METHOD 5: Sort Deor positions by prime factors")
    print("="*60)
    
    # Sort positions by (smallest_prime_factor, position)
    def smallest_prime_factor(n):
        if n < 2:
            return float('inf')
        for p in range(2, int(n**0.5) + 1):
            if n % p == 0:
                return p
        return n  # n is prime
    
    positions = list(range(len(deor_clean)))
    sorted_positions = sorted(positions, key=lambda x: (smallest_prime_factor(x + 1), x))
    
    rearranged_deor = ''.join(deor_clean[p] for p in sorted_positions)
    print(f"First 50 positions after sort: {sorted_positions[:50]}")
    
    key = [ENGLISH_TO_IDX.get(c, 0) for c in rearranged_deor]
    extended_key = key * (len(runes) // len(key) + 1)
    extended_key = extended_key[:len(runes)]
    
    result = decrypt_vigenere(runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Sorted Deor as key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")

if __name__ == "__main__":
    main()

"""
Page 20 - Prime Column Extraction
=================================
Extract content from prime-indexed columns and analyze.
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
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

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
    print("PAGE 20 - PRIME COLUMN EXTRACTION")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    rows, cols = 28, 29
    grid = [[runes[r*cols + c] for c in range(cols)] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    # Prime column indices
    prime_cols = [c for c in range(cols) if is_prime(c)]
    non_prime_cols = [c for c in range(cols) if not is_prime(c)]
    
    print(f"\nPrime columns: {prime_cols}")  # [2, 3, 5, 7, 11, 13, 17, 19, 23]
    print(f"Non-prime columns: {non_prime_cols}")
    
    # Extract prime columns
    prime_col_runes = []
    for r in range(rows):
        for c in prime_cols:
            prime_col_runes.append(grid[r][c])
    
    print(f"\nPrime column content ({len(prime_col_runes)} runes):")
    print(runes_to_latin(prime_col_runes))
    
    ioc = calculate_ioc(prime_col_runes)
    print(f"IoC: {ioc:.4f}")
    
    # Could this BE the key?
    print("\n" + "="*60)
    print("USING PRIME COLUMNS AS KEY")
    print("="*60)
    
    # The prime column content as key for the non-prime columns
    non_prime_runes = []
    for r in range(rows):
        for c in non_prime_cols:
            non_prime_runes.append(grid[r][c])
    
    print(f"Non-prime columns: {len(non_prime_runes)} runes")
    
    extended_key = prime_col_runes * (len(non_prime_runes) // len(prime_col_runes) + 1)
    extended_key = extended_key[:len(non_prime_runes)]
    
    result = decrypt_vigenere(non_prime_runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Non-primes decrypted with prime-cols key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if prime columns are the ciphertext and non-prime cols are the key?
    extended_key = non_prime_runes * (len(prime_col_runes) // len(non_prime_runes) + 1)
    extended_key = extended_key[:len(prime_col_runes)]
    
    result = decrypt_vigenere(prime_col_runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Prime-cols decrypted with non-prime key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if we interleave prime and non-prime columns?
    print("\n" + "="*60)
    print("INTERLEAVING PRIME AND NON-PRIME COLUMNS")
    print("="*60)
    
    # Read: prime col 2, non-prime col 0, prime col 3, non-prime col 1, ...
    interleaved = []
    pi, ni = 0, 0
    while pi < len(prime_cols) or ni < len(non_prime_cols):
        if pi < len(prime_cols):
            for r in range(rows):
                interleaved.append(grid[r][prime_cols[pi]])
            pi += 1
        if ni < len(non_prime_cols):
            for r in range(rows):
                interleaved.append(grid[r][non_prime_cols[ni]])
            ni += 1
    
    ioc = calculate_ioc(interleaved)
    print(f"Interleaved: IoC={ioc:.4f}")
    
    # Apply Deor
    deor_key = [ENGLISH_TO_IDX.get(c, 0) for c in deor]
    extended_deor = deor_key * (len(interleaved) // len(deor_key) + 1)
    extended_deor = extended_deor[:len(interleaved)]
    
    result = decrypt_vigenere(interleaved, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"After Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if we read prime columns, apply Deor, then combine with non-prime?
    print("\n" + "="*60)
    print("PRIME COLS + DEOR -> COMBINE WITH NON-PRIME")
    print("="*60)
    
    extended_deor = deor_key * (len(prime_col_runes) // len(deor_key) + 1)
    extended_deor = extended_deor[:len(prime_col_runes)]
    
    decrypted_prime = decrypt_vigenere(prime_col_runes, extended_deor, 'sub')
    ioc = calculate_ioc(decrypted_prime)
    print(f"Prime cols + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(decrypted_prime[:80])}")
    
    # Now use decrypted prime cols as key for non-prime cols
    extended_key = decrypted_prime * (len(non_prime_runes) // len(decrypted_prime) + 1)
    extended_key = extended_key[:len(non_prime_runes)]
    
    result = decrypt_vigenere(non_prime_runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Non-prime cols with decrypted-prime-key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Extract the first row as potential key indicator
    print("\n" + "="*60)
    print("FIRST ROW ANALYSIS")
    print("="*60)
    
    first_row = grid[0]
    print(f"First row: {runes_to_latin(first_row)}")
    print(f"Indices: {first_row}")
    
    # Prime positions in first row
    prime_first_row = [first_row[c] for c in prime_cols]
    print(f"First row at prime positions: {runes_to_latin(prime_first_row)}")

if __name__ == "__main__":
    main()

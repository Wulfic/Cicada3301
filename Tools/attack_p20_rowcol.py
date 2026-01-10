"""
Page 20 - Grid Row/Column Key Analysis
======================================
Row 12 as key gave IoC 1.06 - investigate further.
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
        text = f.read().upper()
    return [ENGLISH_TO_IDX.get(c, 0) for c in text if c in ENGLISH_TO_IDX]

def main():
    print("="*60)
    print("PAGE 20 - ROW/COLUMN KEY ANALYSIS")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    # Test ALL rows as keys
    print("\n--- All Rows as Keys (Sorted by IoC) ---")
    
    row_results = []
    for key_row in range(rows):
        row_key = grid[key_row]
        extended_key = row_key * (len(runes) // len(row_key) + 1)
        extended_key = extended_key[:len(runes)]
        
        for mode in ['sub', 'add']:
            result = decrypt_vigenere(runes, extended_key, mode)
            ioc = calculate_ioc(result)
            row_results.append((key_row, mode, ioc, result))
    
    row_results.sort(key=lambda x: x[2], reverse=True)
    
    for key_row, mode, ioc, result in row_results[:10]:
        print(f"\nRow {key_row} ({mode}): IoC={ioc:.4f}")
        print(f"  Key: {runes_to_latin(grid[key_row])}")
        print(f"  Text: {runes_to_latin(result[:100])}")
    
    # Check row 12 specifically
    print("\n" + "="*60)
    print("ROW 12 DETAILED ANALYSIS")
    print("="*60)
    
    row12_key = grid[12]
    print(f"Row 12 key: {runes_to_latin(row12_key)}")
    print(f"Row 12 indices: {row12_key}")
    
    # Is row 12 special? Check its properties
    print(f"\nRow 12 properties:")
    print(f"  Sum of indices: {sum(row12_key)}")
    print(f"  12 is NOT prime, but 12 = 2² × 3")
    print(f"  Row 12 is the 13th row (0-indexed), and 13 is prime!")
    
    # Try combining row 12 with Deor
    extended_row = row12_key * (len(runes) // len(row12_key) + 1)
    extended_row = extended_row[:len(runes)]
    
    extended_deor = deor * (len(runes) // len(deor) + 1)
    extended_deor = extended_deor[:len(runes)]
    
    # Row 12 then Deor
    step1 = decrypt_vigenere(runes, extended_row, 'sub')
    step2 = decrypt_vigenere(step1, extended_deor, 'sub')
    ioc = calculate_ioc(step2)
    print(f"\nRow 12 SUB, then Deor SUB: IoC={ioc:.4f}")
    print(f"  Text: {runes_to_latin(step2[:150])}")
    
    # Deor then Row 12
    step1 = decrypt_vigenere(runes, extended_deor, 'sub')
    step2 = decrypt_vigenere(step1, extended_row, 'sub')
    ioc = calculate_ioc(step2)
    print(f"\nDeor SUB, then Row 12 SUB: IoC={ioc:.4f}")
    print(f"  Text: {runes_to_latin(step2[:150])}")
    
    # Try prime-indexed rows combined
    print("\n" + "="*60)
    print("PRIME-INDEXED ROWS AS KEY")
    print("="*60)
    
    prime_rows = [2, 3, 5, 7, 11, 13, 17, 19, 23]  # Prime row indices
    prime_row_key = []
    for pr in prime_rows:
        if pr < rows:
            prime_row_key.extend(grid[pr])
    
    print(f"Prime rows {prime_rows[:9]} combined: {len(prime_row_key)} chars")
    
    extended_key = prime_row_key * (len(runes) // len(prime_row_key) + 1)
    extended_key = extended_key[:len(runes)]
    
    result = decrypt_vigenere(runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Prime rows SUB: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:150])}")
    
    # Try columns
    print("\n" + "="*60)
    print("COLUMN ANALYSIS")
    print("="*60)
    
    col_results = []
    for key_col in range(cols):
        col_key = [grid[r][key_col] for r in range(rows)]
        extended_key = col_key * (len(runes) // len(col_key) + 1)
        extended_key = extended_key[:len(runes)]
        
        result = decrypt_vigenere(runes, extended_key, 'sub')
        ioc = calculate_ioc(result)
        col_results.append((key_col, ioc, result, col_key))
    
    col_results.sort(key=lambda x: x[1], reverse=True)
    
    print("Top 5 columns as keys:")
    for key_col, ioc, result, col_key in col_results[:5]:
        is_prime = key_col in [2, 3, 5, 7, 11, 13, 17, 19, 23]
        print(f"\nCol {key_col} {'(PRIME)' if is_prime else ''}: IoC={ioc:.4f}")
        print(f"  Key: {runes_to_latin(col_key)}")
        print(f"  Text: {runes_to_latin(result[:80])}")
    
    # Try using the "path" literally - read following prime positions
    print("\n" + "="*60)
    print("PRIME POSITION PATH")
    print("="*60)
    
    def is_prime(n):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5)+1, 2):
            if n % i == 0: return False
        return True
    
    # Path: visit position 2, then 3, then 5, then 7...
    prime_positions = [p for p in range(len(runes)) if is_prime(p)]
    non_prime_positions = [p for p in range(len(runes)) if not is_prime(p)]
    
    # Read primes first, then non-primes
    path_order = prime_positions + non_prime_positions
    path_runes = [runes[i] for i in path_order]
    
    ioc = calculate_ioc(path_runes)
    print(f"Read prime positions first: IoC={ioc:.4f}")
    
    # Apply Deor
    result = decrypt_vigenere(path_runes, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"After Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Try the inverse - read non-primes first
    path_order = non_prime_positions + prime_positions
    path_runes = [runes[i] for i in path_order]
    
    result = decrypt_vigenere(path_runes, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"\nRead non-prime positions first + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")

if __name__ == "__main__":
    main()

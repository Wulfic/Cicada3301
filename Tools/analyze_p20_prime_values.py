"""
Page 20 - Prime Value Investigation
====================================
The runes with prime index values (0-13) showed IoC 2.06 - investigate further.
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

# Gematria Primus prime values
IDX_TO_PRIME = {
    0: 2, 1: 3, 2: 5, 3: 7, 4: 11, 5: 13, 6: 17, 7: 19,
    8: 23, 9: 29, 10: 31, 11: 37, 12: 41, 13: 43, 14: 47, 15: 53,
    16: 59, 17: 61, 18: 67, 19: 71, 20: 73, 21: 79, 22: 83, 23: 89,
    24: 97, 25: 101, 26: 103, 27: 107, 28: 109
}

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
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
    return numerator / denominator * len(set(text))

def main():
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    
    print("PAGE 20 - PRIME VALUE ANALYSIS")
    print("=" * 60)
    print(f"Total runes: {len(runes)}")
    print()
    
    # Separate into low-index (0-13) and high-index (14-28)
    low_idx = [r for r in runes if r <= 13]
    high_idx = [r for r in runes if r > 13]
    
    print(f"Low index runes (0-13): {len(low_idx)}")
    print(f"High index runes (14-28): {len(high_idx)}")
    
    # IoC for each
    def ioc_norm(text, alphabet_size):
        if len(text) < 2: return 0
        counts = collections.Counter(text)
        numerator = sum(n * (n - 1) for n in counts.values())
        denominator = len(text) * (len(text) - 1)
        return numerator / denominator * alphabet_size
    
    print(f"\nIoC (low, norm by 14): {ioc_norm(low_idx, 14):.4f}")
    print(f"IoC (high, norm by 15): {ioc_norm(high_idx, 15):.4f}")
    
    # Frequency of low-index runes
    print("\nLow-index rune frequencies:")
    counts = collections.Counter(low_idx)
    for idx in range(14):
        cnt = counts.get(idx, 0)
        print(f"  {IDX_TO_LATIN[idx]:3s} ({idx:2d}): {cnt:3d} ({cnt/len(low_idx)*100:.1f}%)")
    
    # Check if the low-index subset, when extracted with positions, forms a pattern
    print("\n" + "=" * 60)
    print("EXTRACTING BY POSITION")
    print("=" * 60)
    
    # Positions where low-index runes appear
    low_positions = [i for i, r in enumerate(runes) if r <= 13]
    high_positions = [i for i, r in enumerate(runes) if r > 13]
    
    print(f"\nLow-index rune positions (first 50): {low_positions[:50]}")
    print(f"High-index rune positions (first 50): {high_positions[:50]}")
    
    # Check if positions are related to primes
    prime_positions = [p for p in low_positions if is_prime(p)]
    print(f"\nHow many low-index positions are prime? {len(prime_positions)}/{len(low_positions)}")
    
    # Try interleaving: use low-index as key for high-index
    print("\n" + "=" * 60)
    print("INTERLEAVING TEST")
    print("=" * 60)
    
    # Extract in order of appearance
    low_stream = []
    high_stream = []
    
    for r in runes:
        if r <= 13:
            low_stream.append(r)
        else:
            high_stream.append(r)
    
    # Try using low as key
    min_len = min(len(low_stream), len(high_stream))
    
    result_sub = [(high_stream[i] - low_stream[i]) % 29 for i in range(min_len)]
    result_add = [(high_stream[i] + low_stream[i]) % 29 for i in range(min_len)]
    
    print(f"\nHigh - Low (mod 29), first {min_len} pairs:")
    print(f"  IoC: {ioc_norm(result_sub, 29):.4f}")
    print(f"  Text: {runes_to_latin(result_sub[:100])}")
    
    print(f"\nHigh + Low (mod 29):")
    print(f"  IoC: {ioc_norm(result_add, 29):.4f}")
    print(f"  Text: {runes_to_latin(result_add[:100])}")
    
    # Try the opposite: low - high
    result_sub2 = [(low_stream[i] - high_stream[i]) % 29 for i in range(min_len)]
    print(f"\nLow - High (mod 29):")
    print(f"  IoC: {ioc_norm(result_sub2, 29):.4f}")
    print(f"  Text: {runes_to_latin(result_sub2[:100])}")
    
    # Check the 29x28 grid structure
    print("\n" + "=" * 60)
    print("GRID ANALYSIS - LOW VS HIGH")
    print("=" * 60)
    
    rows, cols = 28, 29
    grid = []
    for r in range(rows):
        row = runes[r*cols:(r+1)*cols]
        grid.append(row)
    
    # Count low-index per row
    print("\nLow-index runes per row:")
    for r in range(rows):
        low_count = sum(1 for x in grid[r] if x <= 13)
        print(f"  Row {r:2d}: {low_count:2d} low / {cols-low_count:2d} high")
    
    # Count low-index per column
    print("\nLow-index runes per column:")
    for c in range(cols):
        low_count = sum(1 for r in range(rows) if grid[r][c] <= 13)
        print(f"  Col {c:2d}: {low_count:2d} low / {rows-low_count:2d} high", end="")
        if is_prime(c):
            print(" (PRIME)", end="")
        print()

if __name__ == "__main__":
    main()

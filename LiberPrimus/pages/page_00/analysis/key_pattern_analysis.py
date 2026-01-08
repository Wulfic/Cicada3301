#!/usr/bin/env python3
"""
Key Pattern Analysis
====================
Analyze the keys found for Pages 0-4 to see if there's a pattern.
- Page 0: key length 113
- Page 1: key length 71
- Page 2: key length 83
- Page 3: key length 83
- Page 4: key length 103

All are primes or close to primes. Do the keys themselves encode something?
"""

import math

# Keys found through hill climbing
PAGE0_KEY = [19, 6, 23, 16, 10, 22, 9, 27, 26, 11, 16, 3, 19, 0, 12, 7, 23, 17, 7, 1, 1, 5, 28, 7, 20, 21, 15, 1, 17, 20, 23, 8, 22, 9, 20, 16, 7, 8, 13, 22, 15, 10, 2, 11, 22, 22, 4, 9, 19, 24, 1, 8, 12, 18, 21, 11, 21, 22, 21, 12, 7, 6, 13, 1, 14, 12, 26, 11, 11, 5, 27, 21, 25, 8, 22, 15, 20, 4, 20, 4, 19, 26, 0, 19, 1, 6, 2, 3, 22, 26, 24, 1, 19, 22, 12, 0, 21, 18, 20, 5, 17, 4, 24, 10, 19, 14, 19, 7, 12, 12, 14, 16, 2]

PAGE1_KEY = [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7]

PAGE2_KEY = [4, 23, 28, 26, 20, 28, 4, 15, 21, 18, 25, 2, 10, 4, 5, 6, 3, 27, 5, 24, 27, 15, 15, 12, 10, 15, 0, 14, 5, 11, 11, 8, 25, 21, 28, 16, 20, 11, 2, 14, 10, 10, 15, 14, 4, 0, 19, 1, 8, 26, 19, 7, 19, 20, 14, 10, 7, 4, 26, 2, 20, 18, 7, 8, 3, 16, 27, 1, 2, 1, 3, 6, 10, 19, 10, 12, 14, 28, 4, 8, 16, 10, 16]

PAGE3_KEY = [6, 0, 11, 19, 27, 27, 22, 2, 4, 16, 28, 1, 11, 14, 1, 19, 21, 0, 2, 17, 23, 5, 3, 18, 23, 9, 18, 14, 19, 3, 11, 21, 22, 15, 20, 19, 12, 13, 18, 8, 20, 26, 28, 17, 24, 12, 3, 10, 11, 20, 21, 0, 5, 9, 2, 16, 5, 0, 9, 4, 1, 21, 11, 27, 5, 21, 13, 14, 2, 26, 0, 23, 14, 17, 28, 27, 4, 13, 6, 20, 16, 8, 9]

PAGE4_KEY = [1, 23, 19, 6, 17, 13, 0, 7, 27, 25, 20, 27, 11, 5, 27, 23, 14, 18, 8, 20, 6, 19, 23, 4, 21, 18, 11, 8, 22, 28, 9, 9, 23, 21, 8, 6, 25, 0, 28, 11, 9, 10, 20, 13, 28, 15, 19, 1, 9, 15, 2, 3, 0, 27, 18, 19, 19, 1, 10, 4, 28, 3, 15, 8, 8, 17, 3, 24, 27, 1, 25, 4, 23, 0, 8, 19, 10, 21, 2, 26, 21, 19, 16, 10, 24, 1, 24, 2, 10, 26, 12, 11, 5, 8, 13, 28, 9, 16, 1, 14, 9, 1, 0]

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                   'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                   'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def key_to_text(key):
    """Convert key indices to letters."""
    return ''.join(INDEX_TO_LETTER[i] for i in key)

def analyze_key_distribution(key, name):
    """Analyze the distribution of values in a key."""
    from collections import Counter
    
    counts = Counter(key)
    total = len(key)
    
    print(f"\n{name} (length {total}):")
    print("-" * 40)
    
    # Average value
    avg = sum(key) / len(key)
    print(f"Average value: {avg:.2f}")
    
    # Most common values
    print("Most common indices:")
    for idx, count in counts.most_common(5):
        letter = INDEX_TO_LETTER[idx]
        print(f"  {idx:2} ({letter:4}): {count} times ({count/total*100:.1f}%)")
    
    # As text
    text = key_to_text(key)
    print(f"\nAs letters: {text[:50]}...")

def check_key_as_running_key(key):
    """Check if key values form a meaningful pattern."""
    # Check for arithmetic progressions
    diffs = [key[i+1] - key[i] for i in range(len(key) - 1)]
    
    from collections import Counter
    diff_counts = Counter(diffs)
    
    return diff_counts.most_common(5)

def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def main():
    print("=" * 60)
    print("KEY PATTERN ANALYSIS")
    print("=" * 60)
    
    keys = [
        ("Page 0", PAGE0_KEY, 113),
        ("Page 1", PAGE1_KEY, 71),
        ("Page 2", PAGE2_KEY, 83),
        ("Page 3", PAGE3_KEY, 83),
        ("Page 4", PAGE4_KEY, 103),
    ]
    
    # Key lengths
    print("\nKEY LENGTHS:")
    print("-" * 40)
    for name, key, expected_len in keys:
        prime = "PRIME" if is_prime(expected_len) else ""
        print(f"{name}: {expected_len} {prime}")
    
    # Key distributions
    print("\n" + "=" * 60)
    print("KEY VALUE DISTRIBUTIONS")
    print("=" * 60)
    
    for name, key, _ in keys:
        analyze_key_distribution(key, name)
    
    # Check for patterns in key differences
    print("\n" + "=" * 60)
    print("KEY DIFFERENCE PATTERNS")
    print("=" * 60)
    
    for name, key, _ in keys:
        diffs = check_key_as_running_key(key)
        print(f"\n{name} most common differences:")
        for diff, count in diffs:
            print(f"  {diff:3}: {count} times")
    
    # Check if keys share common subsequences
    print("\n" + "=" * 60)
    print("INTER-KEY RELATIONSHIPS")
    print("=" * 60)
    
    # Pages 2 and 3 use same key length (83)
    print("\nPages 2 and 3 (both key length 83):")
    matches = sum(1 for i in range(83) if PAGE2_KEY[i] == PAGE3_KEY[i])
    print(f"  Matching positions: {matches}/83 ({matches/83*100:.1f}%)")
    
    # XOR of keys
    xor_key = [(PAGE2_KEY[i] - PAGE3_KEY[i]) % 29 for i in range(83)]
    print(f"  XOR (difference mod 29): {key_to_text(xor_key)[:50]}...")
    
    # Check if any key might encode Parable text
    print("\n" + "=" * 60)
    print("CHECKING IF KEYS ENCODE PARABLE")
    print("=" * 60)
    
    parable = "PARABLE.LIKE THE INSTAR TUNNELING TO THE SURFACE.WE MUST SHED OUR OWN CIRCUMFERENCES.FIND THE DIVINITY WITHIN AND EMERGE."
    
    # Map Parable to indices
    letter_to_idx = {
        'P': 13, 'A': 24, 'R': 4, 'B': 17, 'L': 20, 'E': 18,
        'I': 10, 'K': 5, 'T': 16, 'H': 8, 'N': 9, 'S': 15,
        'U': 1, 'G': 6, 'O': 3, 'F': 0, 'C': 5, 'W': 7,
        'M': 19, 'D': 23, 'Y': 26, 'V': 1  # V mapped to U
    }
    
    parable_indices = [letter_to_idx.get(c.upper(), -1) for c in parable if c.upper() in letter_to_idx]
    
    print(f"Parable as indices (first 50): {parable_indices[:50]}")
    
    # Check correlation with each key
    for name, key, _ in keys:
        min_len = min(len(key), len(parable_indices))
        matches = sum(1 for i in range(min_len) if key[i] == parable_indices[i])
        print(f"{name}: {matches}/{min_len} positions match ({matches/min_len*100:.1f}%)")
    
    # Sum analysis
    print("\n" + "=" * 60)
    print("KEY SUMS AND MODULAR PROPERTIES")
    print("=" * 60)
    
    for name, key, length in keys:
        key_sum = sum(key)
        print(f"\n{name}:")
        print(f"  Sum: {key_sum}")
        print(f"  Sum mod 29: {key_sum % 29}")
        print(f"  Sum mod length: {key_sum % length}")
        print(f"  Average: {key_sum / length:.2f}")

if __name__ == "__main__":
    main()

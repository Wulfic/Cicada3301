#!/usr/bin/env python3
"""
Attack Page 20: Rearranging Primes by Alphabetical Order

Based on P19 hint: "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"

The key insight: What if we sort prime numbers by their English spellings alphabetically?
- two (2) -> t...
- three (3) -> t...
- five (5) -> f...
- seven (7) -> s...
- eleven (11) -> e...

Sorted alphabetically: eleven, five, nineteen, seven, seventeen, thirteen, three, two...
This gives us a PERMUTATION of the prime indices!
"""

import os
from collections import Counter

# Gematria Primus
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X',
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

# Number to English word
ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", 
         "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
HUNDREDS = ["", "one hundred", "two hundred", "three hundred", "four hundred", 
            "five hundred", "six hundred", "seven hundred", "eight hundred", "nine hundred"]

def num_to_word(n):
    """Convert number to English word."""
    if n == 0:
        return "zero"
    if n < 0:
        return "negative " + num_to_word(-n)
    
    if n < 10:
        return ONES[n]
    elif n < 20:
        return TEENS[n - 10]
    elif n < 100:
        t, o = divmod(n, 10)
        return TENS[t] + ("-" + ONES[o] if o else "")
    elif n < 1000:
        h, r = divmod(n, 100)
        return ONES[h] + " hundred" + (" " + num_to_word(r) if r else "")
    elif n < 10000:
        th, r = divmod(n, 1000)
        return num_to_word(th) + " thousand" + (" " + num_to_word(r) if r else "")
    else:
        return str(n)

def get_primes(limit):
    """Generate primes up to limit using Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def load_runes(filepath):
    """Load runes from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def load_deor(filepath):
    """Load Deor poem as indices."""
    # Map Old English chars to Gematria
    char_map = {
        'a': 24, 'b': 17, 'c': 5, 'd': 23, 'e': 18, 'f': 0, 'g': 6, 'h': 8, 'i': 10,
        'j': 11, 'l': 20, 'm': 19, 'n': 9, 'o': 3, 'p': 13, 'r': 4, 's': 15, 't': 16,
        'u': 1, 'w': 7, 'x': 14, 'y': 26, 'æ': 25, 'þ': 2, 'ð': 2, 'k': 5
    }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Get Old English section only
    indices = []
    for line in lines:
        if "MODERN ENGLISH" in line.upper():
            break
        for c in line.lower():
            if c in char_map:
                indices.append(char_map[c])
    
    return indices

def calc_ioc(indices):
    """Calculate Index of Coincidence."""
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    """Convert indices to Latin text."""
    return ''.join(LATIN_TABLE[i] for i in indices)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    
    cipher = load_runes(p20_path)
    deor = load_deor(deor_path)
    
    print(f"Loaded {len(cipher)} runes from Page 20")
    print(f"Loaded {len(deor)} chars from Deor poem")
    
    # Generate primes up to cipher length
    primes = get_primes(len(cipher) + 100)
    primes_in_range = [p for p in primes if p < len(cipher)]
    print(f"Primes in range: {len(primes_in_range)}")
    
    # Create (prime, english_word) pairs
    prime_word_pairs = [(p, num_to_word(p)) for p in primes_in_range]
    
    # Sort by English word (alphabetically)
    sorted_pairs = sorted(prime_word_pairs, key=lambda x: x[1])
    
    print("\nFirst 20 primes sorted alphabetically:")
    for p, w in sorted_pairs[:20]:
        print(f"  {w} = {p}")
    
    # Extract the rearranged prime sequence
    rearranged_primes = [p for p, w in sorted_pairs]
    
    print(f"\nRearranged prime sequence (first 20): {rearranged_primes[:20]}")
    
    # APPROACH 1: Use rearranged primes as positions into cipher
    print("\n" + "="*60)
    print("APPROACH 1: Extract cipher runes at rearranged prime positions")
    print("="*60)
    
    extracted = []
    for p in rearranged_primes:
        if p < len(cipher):
            extracted.append(cipher[p])
    
    ioc = calc_ioc(extracted)
    latin = indices_to_latin(extracted)
    print(f"Extracted {len(extracted)} runes, IoC: {ioc:.4f}")
    print(f"Preview: {latin[:100]}")
    
    # APPROACH 2: Use rearranged primes as positions into Deor to create key
    print("\n" + "="*60)
    print("APPROACH 2: Extract Deor chars at rearranged prime positions as KEY")
    print("="*60)
    
    deor_key = []
    for p in rearranged_primes:
        if p < len(deor):
            deor_key.append(deor[p])
    
    print(f"Deor key length: {len(deor_key)}")
    deor_key_latin = indices_to_latin(deor_key[:50])
    print(f"Deor key preview: {deor_key_latin}")
    
    # Apply key to cipher (various modes)
    for mode_name, mode_fn in [
        ("SUB", lambda c, k: (c - k) % 29),
        ("ADD", lambda c, k: (c + k) % 29),
        ("BEAUFORT", lambda c, k: (k - c) % 29)
    ]:
        result = []
        for i, c in enumerate(cipher):
            k = deor_key[i % len(deor_key)]
            result.append(mode_fn(c, k))
        
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode_name}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    # APPROACH 3: Permute the cipher positions based on rearranged primes
    print("\n" + "="*60)
    print("APPROACH 3: Reorder cipher using rearranged primes as permutation")
    print("="*60)
    
    # Create a mapping: original prime position -> alphabetical rank
    original_primes = [p for p in primes if p < len(cipher)]
    
    # Create permutation: for each position i, put the rune from position rearranged_primes[i]
    if len(rearranged_primes) >= len(original_primes):
        permuted = []
        for i, p in enumerate(rearranged_primes[:len(cipher)]):
            if p < len(cipher):
                permuted.append(cipher[p])
        
        ioc = calc_ioc(permuted)
        latin = indices_to_latin(permuted)
        print(f"Permuted {len(permuted)} runes, IoC: {ioc:.4f}")
        print(f"Preview: {latin[:100]}")
    
    # APPROACH 4: Only extract prime-position runes, then reorder by alphabetical primes
    print("\n" + "="*60)
    print("APPROACH 4: Extract prime-position runes, reorder alphabetically")
    print("="*60)
    
    # First, get runes at original prime positions
    prime_runes = [(p, cipher[p]) for p in original_primes if p < len(cipher)]
    
    # Sort by the English name of the prime
    prime_runes_sorted = sorted(prime_runes, key=lambda x: num_to_word(x[0]))
    
    reordered = [r for p, r in prime_runes_sorted]
    ioc = calc_ioc(reordered)
    latin = indices_to_latin(reordered)
    print(f"Reordered {len(reordered)} runes, IoC: {ioc:.4f}")
    print(f"Preview: {latin[:100]}")
    
    # Try decrypting with Deor Beaufort after reordering
    deor_extended = (deor * ((len(reordered) // len(deor)) + 1))[:len(reordered)]
    
    for mode_name, mode_fn in [
        ("SUB", lambda c, k: (c - k) % 29),
        ("ADD", lambda c, k: (c + k) % 29),
        ("BEAUFORT", lambda c, k: (k - c) % 29)
    ]:
        result = [mode_fn(reordered[i], deor_extended[i]) for i in range(len(reordered))]
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[Reordered + Deor {mode_name}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    # APPROACH 5: The "path" - use alphabetical sort order as indices into Deor
    print("\n" + "="*60)
    print("APPROACH 5: Use alphabetical rank as index into Deor")
    print("="*60)
    
    # The rank tells us the position: e.g., "eleven" comes first alphabetically
    # So we extract Deor[11], Deor[5], Deor[19], etc.
    ranks = list(range(len(rearranged_primes)))
    
    # Actually, the rearranged_primes already ARE the sorted sequence
    # Let's try: index into Deor using each prime value
    path_key = []
    for p in rearranged_primes:
        if p < len(deor):
            path_key.append(deor[p])
    
    print(f"Path key length: {len(path_key)}")
    path_key_latin = indices_to_latin(path_key[:50])
    print(f"Path key preview: {path_key_latin}")

if __name__ == '__main__':
    main()

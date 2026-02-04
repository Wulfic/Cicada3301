#!/usr/bin/env python3
"""
Page 20: Separate by RUNE VALUE being prime or composite

P19 hint: "REARRANGING THE PRIMES NUMBERS"

Hypothesis: 
- Runes with PRIME values (2, 3, 5, 7, 11, 13, 17, 19, 23) form one message
- Runes with COMPOSITE/NON-PRIME values form another
- Each layer is encrypted differently

Prime values in Gematria (0-28): 2, 3, 5, 7, 11, 13, 17, 19, 23
Non-prime values: 0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28
"""

import os
from collections import Counter

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

PRIME_VALUES = {2, 3, 5, 7, 11, 13, 17, 19, 23}

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    indices = []
    for c in content:
        if c in RUNE_MAP:
            indices.append(RUNE_MAP[c])
    return indices

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

def load_deor_indices(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().upper()
    
    indices = []
    i = 0
    text = content.replace('\n', ' ')
    
    digraphs = {'TH': 2, 'EO': 12, 'NG': 21, 'OE': 22, 'AE': 25, 'IA': 27, 'EA': 28}
    singles = {'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 
               'N': 9, 'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 
               'B': 17, 'E': 18, 'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26}
    
    while i < len(text):
        matched = False
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in digraphs:
                indices.append(digraphs[digraph])
                i += 2
                matched = True
        if not matched:
            c = text[i]
            if c in singles:
                indices.append(singles[c])
            i += 1
    return indices

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    
    cipher = load_runes(p20_path)
    deor = load_deor_indices(deor_path)
    
    print(f"Page 20: {len(cipher)} runes")
    print(f"Deor poem: {len(deor)} indices")
    
    # Separate by rune VALUE being prime
    prime_valued = [(i, c) for i, c in enumerate(cipher) if c in PRIME_VALUES]
    non_prime_valued = [(i, c) for i, c in enumerate(cipher) if c not in PRIME_VALUES]
    
    print(f"\nRunes with PRIME values: {len(prime_valued)}")
    print(f"Runes with NON-PRIME values: {len(non_prime_valued)}")
    
    # Extract just the values
    prime_stream = [c for _, c in prime_valued]
    non_prime_stream = [c for _, c in non_prime_valued]
    
    print(f"\n=== PRIME-VALUED RUNES RAW ===")
    print(f"IoC: {calc_ioc(prime_stream):.4f}")
    print(f"Latin: {indices_to_latin(prime_stream)[:150]}")
    
    print(f"\n=== NON-PRIME-VALUED RUNES RAW ===")
    print(f"IoC: {calc_ioc(non_prime_stream):.4f}")
    print(f"Latin: {indices_to_latin(non_prime_stream)[:150]}")
    
    # Now try decrypting each stream with Deor
    print("\n=== PRIME-VALUED RUNES + DEOR ===")
    for mode in ['beaufort', 'sub', 'add']:
        stream = []
        for idx, (orig_pos, c) in enumerate(prime_valued):
            k = deor[idx % len(deor)]
            if mode == 'beaufort':
                stream.append((k - c) % 29)
            elif mode == 'sub':
                stream.append((c - k) % 29)
            else:
                stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        print(f"  {mode}: IoC={ioc:.4f} - {latin[:80]}")
    
    print("\n=== NON-PRIME-VALUED RUNES + DEOR ===")
    for mode in ['beaufort', 'sub', 'add']:
        stream = []
        for idx, (orig_pos, c) in enumerate(non_prime_valued):
            k = deor[idx % len(deor)]
            if mode == 'beaufort':
                stream.append((k - c) % 29)
            elif mode == 'sub':
                stream.append((c - k) % 29)
            else:
                stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        print(f"  {mode}: IoC={ioc:.4f} - {latin[:80]}")
    
    # Try using positions from Deor that are ALSO prime-valued
    print("\n=== PRIME-VALUED RUNES + DEOR[PRIME-VALUED] ===")
    deor_prime_valued = [c for c in deor if c in PRIME_VALUES]
    print(f"Deor prime-valued runes: {len(deor_prime_valued)}")
    
    for mode in ['beaufort', 'sub', 'add']:
        stream = []
        for idx, (orig_pos, c) in enumerate(prime_valued):
            if idx < len(deor_prime_valued):
                k = deor_prime_valued[idx]
                if mode == 'beaufort':
                    stream.append((k - c) % 29)
                elif mode == 'sub':
                    stream.append((c - k) % 29)
                else:
                    stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        print(f"  {mode}: IoC={ioc:.4f} - {latin[:80]}")
    
    # What if we interleave prime and non-prime valued back together after decryption?
    print("\n=== RECONSTITUTION TEST ===")
    # Mark each position with whether it had prime or non-prime value
    prime_positions = set(pos for pos, _ in prime_valued)
    
    # Check if "THEY" at word 17 (positions 96-98) has a pattern
    print("\nPositions 96-98 (THEY):")
    for pos in [96, 97, 98]:
        val = cipher[pos]
        is_pv = val in PRIME_VALUES
        print(f"  Position {pos}: value={val} ({LATIN_TABLE[val]}), prime-valued={is_pv}")

if __name__ == '__main__':
    main()

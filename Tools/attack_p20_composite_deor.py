#!/usr/bin/env python3
"""
Attack Page 20: Apply Deor cipher to COMPOSITE (non-prime) positions

The P19 hint says "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"

We successfully decoded prime-indexed positions using Beaufort with Deor.
Now try: What if composite-indexed positions use a DIFFERENT mapping to Deor?

Hypothesis: 
- Prime positions -> Deor at prime indices (proven to work)
- Composite positions -> Deor at composite indices?
"""

import os
from collections import Counter

# Gematria Primus mapping
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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def load_runes(filepath):
    """Load runes from file, return list of indices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    indices = []
    for c in content:
        if c in RUNE_MAP:
            indices.append(RUNE_MAP[c])
    return indices

def load_deor_runes(filepath):
    """Load Deor poem and convert to rune indices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().upper()
    
    # Handle digraphs
    indices = []
    i = 0
    text = content.replace('\n', ' ').replace('\r', '')
    
    digraphs = {'TH': 2, 'EO': 12, 'NG': 21, 'OE': 22, 'AE': 25, 'IA': 27, 'EA': 28}
    singles = {'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 
               'N': 9, 'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 
               'B': 17, 'E': 18, 'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26}
    
    while i < len(text):
        matched = False
        # Try digraphs first
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

def calc_ioc(indices):
    """Calculate Index of Coincidence for 29-letter alphabet."""
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    """Convert indices to Latin letters."""
    return ''.join(LATIN_TABLE[i] for i in indices)

def get_primes_up_to(n):
    """Get all primes up to n."""
    return [i for i in range(n) if is_prime(i)]

def get_composites_up_to(n):
    """Get all composite numbers up to n (excluding 0, 1, and primes)."""
    return [i for i in range(4, n) if not is_prime(i)]

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    
    # Load P20 runes
    cipher = load_runes(p20_path)
    print(f"Loaded {len(cipher)} runes from Page 20")
    
    # Load Deor
    deor = load_deor_runes(deor_path)
    print(f"Loaded {len(deor)} indices from Deor poem")
    
    # Get position lists
    n = len(cipher)
    primes = get_primes_up_to(n)
    composites = get_composites_up_to(n)
    
    print(f"\nPrime positions: {len(primes)}")
    print(f"Composite positions: {len(composites)}")
    print(f"Positions 0 and 1 (neither): 2")
    
    # Extract composite-position runes from P20
    composite_runes = [cipher[i] for i in composites if i < n]
    print(f"\nComposite runes extracted: {len(composite_runes)}")
    
    results = []
    
    # Approach 1: Apply Deor at composite indices (matching composite->composite)
    # i.e., P20[composite_i] decrypted with Deor[composite_i]
    print("\n=== Approach 1: P20[composite] with Deor[composite] ===")
    for mode in ['beaufort', 'sub', 'add']:
        stream = []
        for idx, pos in enumerate(composites):
            if pos < n and idx < len(deor):
                c = cipher[pos]
                k = deor[idx]  # Use Deor sequentially
                if mode == 'beaufort':
                    stream.append((k - c) % 29)
                elif mode == 'sub':
                    stream.append((c - k) % 29)
                else:  # add
                    stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        results.append(('deor_sequential_' + mode, ioc, latin))
    
    # Approach 2: Use Deor at the composite INDEX values themselves
    # i.e., P20[4] with Deor[4], P20[6] with Deor[6], etc.
    print("\n=== Approach 2: P20[composite_i] with Deor[composite_i] ===")
    for mode in ['beaufort', 'sub', 'add']:
        stream = []
        for pos in composites:
            if pos < n and pos < len(deor):
                c = cipher[pos]
                k = deor[pos]  # Use Deor at same position
                if mode == 'beaufort':
                    stream.append((k - c) % 29)
                elif mode == 'sub':
                    stream.append((c - k) % 29)
                else:
                    stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        results.append(('deor_same_pos_' + mode, ioc, latin))
    
    # Approach 3: Use Deor at prime positions for composite P20 positions
    # i.e., P20[composite_i] with Deor[prime_i]
    print("\n=== Approach 3: P20[composite] with Deor[prime] ===")
    for mode in ['beaufort', 'sub', 'add']:
        stream = []
        for idx, pos in enumerate(composites):
            if pos < n and idx < len(primes) and primes[idx] < len(deor):
                c = cipher[pos]
                k = deor[primes[idx]]  # Use Deor at corresponding prime
                if mode == 'beaufort':
                    stream.append((k - c) % 29)
                elif mode == 'sub':
                    stream.append((c - k) % 29)
                else:
                    stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        results.append(('deor_prime_pos_' + mode, ioc, latin))
    
    # Approach 4: Interleave - even composites from one source, odd from another
    print("\n=== Approach 4: Every nth composite ===")
    for skip in [2, 3, 5, 7]:
        stream = []
        for idx, pos in enumerate(composites):
            if pos < n and (idx * skip) < len(deor):
                c = cipher[pos]
                k = deor[idx * skip % len(deor)]
                stream.append((k - c) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        results.append((f'skip_{skip}_beaufort', ioc, latin))
    
    # Approach 5: Use φ(composite) as shift
    print("\n=== Approach 5: Totient of position as shift ===")
    def euler_phi(n):
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result
    
    for mode in ['sub', 'add']:
        stream = []
        for pos in composites:
            if pos < n:
                c = cipher[pos]
                k = euler_phi(pos) % 29
                if mode == 'sub':
                    stream.append((c - k) % 29)
                else:
                    stream.append((c + k) % 29)
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        results.append(('phi_composite_' + mode, ioc, latin))
    
    # Sort and display results
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*80)
    print("RESULTS (sorted by IoC, English ~1.73, Random ~1.0)")
    print("="*80)
    
    for method, ioc, text in results[:15]:
        print(f"\n[{method}] IoC: {ioc:.4f}")
        print(f"  Preview: {text[:100]}")
    
    # Check best result
    if results[0][1] > 1.3:
        print("\n" + "="*80)
        print("POTENTIAL HIT!")
        print("="*80)
        print(f"Method: {results[0][0]}")
        print(f"IoC: {results[0][1]:.4f}")
        print(f"Text: {results[0][2]}")

if __name__ == '__main__':
    main()

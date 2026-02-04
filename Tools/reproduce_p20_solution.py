#!/usr/bin/env python3
"""
Reproduce the exact Page 20 partial solution with IoC 1.89.
Carefully match the methodology from P20_Partial_Solution.md
"""

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [c for c in text if c in RUNES]

def rune_to_idx(r):
    return RUNES.index(r) if r in RUNES else -1

def load_deor():
    """Load Deor exactly as in original script"""
    filepath = 'c:/Users/tyler/Repos/Cicada3301/Analysis/Reference_Docs/deor_poem.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    alt_map = {'A': 24, 'E': 18, 'O': 4, 'Y': 28}
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph == 'TH': 
                indices.append(2)
                i += 2
                continue
            elif digraph == 'EA':
                indices.append(27)
                i += 2
                continue
            elif digraph == 'NG':
                indices.append(21)
                i += 2
                continue
        c = text[i]
        if c in mapping:
            indices.append(mapping.index(c))
        elif c in alt_map:
            indices.append(alt_map[c])
        elif c.isalpha():
            idx = ord(c) - ord('A')
            indices.append(idx % 29)
        i += 1
    return indices

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    from collections import Counter
    counts = Counter(indices)
    n = len(indices)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1) / 29) if n > 1 else 0

def indices_to_text(indices):
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    return ''.join(mapping[i % 29] for i in indices)

def main():
    print("=" * 70)
    print("REPRODUCING P20 PARTIAL SOLUTION")
    print("=" * 70)
    
    # Load data
    p20_runes = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    p20 = [rune_to_idx(r) for r in p20_runes]
    deor = load_deor()
    
    print(f"P20 length: {len(p20)}")
    print(f"Deor length: {len(deor)}")
    
    # Method from document: 0-indexed primes, limit to min length
    max_idx = min(len(p20), len(deor))
    primes = [i for i in range(max_idx) if is_prime(i)]
    
    print(f"Max index: {max_idx}")
    print(f"Prime count (0-indexed): {len(primes)}")
    print(f"First 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")
    
    # Beaufort at prime positions: stream[i] = (deor[prime[i]] - p20[prime[i]]) % 29
    stream = [(deor[p] - p20[p]) % 29 for p in primes]
    
    ioc_raw = calc_ioc(stream)
    text_raw = indices_to_text(stream)
    
    print(f"\nRAW STREAM (no transposition):")
    print(f"IoC: {ioc_raw:.4f}")
    print(f"Text: {text_raw}")
    
    # 2x83 transposition
    if len(stream) == 166:
        cols = 83
        transposed = []
        for i in range(len(stream)):
            src = (i % 2) * cols + (i // 2)
            if src < len(stream):
                transposed.append(stream[src])
        
        ioc_trans = calc_ioc(transposed)
        text_trans = indices_to_text(transposed)
        
        print(f"\nAFTER 2×83 TRANSPOSITION:")
        print(f"IoC: {ioc_trans:.4f}")
        print(f"Text: {text_trans}")
    
    # Also try 1-indexed primes for comparison
    print("\n" + "=" * 70)
    print("COMPARISON: 1-indexed primes")
    print("=" * 70)
    
    primes_1idx = [i for i in range(1, len(p20)+1) if is_prime(i)]
    print(f"Prime count (1-indexed): {len(primes_1idx)}")
    
    # For 1-indexed, position p means index p-1
    stream_1idx = []
    for p in primes_1idx:
        idx = p - 1
        if idx < len(p20) and idx < len(deor):
            stream_1idx.append((deor[idx] - p20[idx]) % 29)
    
    ioc_1idx = calc_ioc(stream_1idx)
    text_1idx = indices_to_text(stream_1idx)
    
    print(f"Stream length: {len(stream_1idx)}")
    print(f"IoC: {ioc_1idx:.4f}")
    print(f"Text: {text_1idx[:80]}...")

if __name__ == '__main__':
    main()

"""
Page 20 - Deep Dive on Prime Value Transform
=============================================
The "Prime values mod 29" gave IoC 1.39 - worth investigating further.
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

def load_deor_as_indices():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    try:
        with open(deor_path, 'r', encoding='utf-8') as f:
            text = f.read().upper()
    except:
        return []
    return [ENGLISH_TO_IDX.get(c, 0) for c in text if c in ENGLISH_TO_IDX]

def main():
    print("="*60)
    print("PAGE 20 - PRIME VALUE TRANSFORM DEEP DIVE")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    
    print(f"\nLoaded {len(runes)} runes")
    
    # Transform: Prime values mod 29
    prime_mod29 = [(IDX_TO_PRIME[r] % 29) for r in runes]
    
    print(f"\n1. Prime values mod 29:")
    print(f"   IoC: {calculate_ioc(prime_mod29):.4f}")
    print(f"   Full text:\n")
    
    # Print in lines of 80 chars
    text = runes_to_latin(prime_mod29)
    for i in range(0, len(text), 80):
        print(f"   {text[i:i+80]}")
    
    # Frequency analysis
    print(f"\n   Frequency distribution:")
    counts = collections.Counter(prime_mod29)
    for idx, cnt in counts.most_common(10):
        print(f"     {IDX_TO_LATIN[idx]:3s}: {cnt:3d} ({cnt/len(prime_mod29)*100:.1f}%)")
    
    # Now try decrypting this with Deor
    print("\n" + "="*60)
    print("APPLYING DEOR KEY TO PRIME-MOD29 TRANSFORM")
    print("="*60)
    
    deor = load_deor_as_indices()
    if not deor:
        print("Could not load Deor")
        return
    
    print(f"Deor length: {len(deor)}")
    
    # Extend key if needed
    key = deor * (len(prime_mod29) // len(deor) + 1)
    key = key[:len(prime_mod29)]
    
    # Try subtract
    result = [(prime_mod29[i] - key[i]) % 29 for i in range(len(prime_mod29))]
    ioc = calculate_ioc(result)
    print(f"\n1. (Prime mod 29) - Deor: IoC={ioc:.4f}")
    text = runes_to_latin(result)
    for i in range(0, min(400, len(text)), 80):
        print(f"   {text[i:i+80]}")
    
    # Try add
    result = [(prime_mod29[i] + key[i]) % 29 for i in range(len(prime_mod29))]
    ioc = calculate_ioc(result)
    print(f"\n2. (Prime mod 29) + Deor: IoC={ioc:.4f}")
    text = runes_to_latin(result)
    for i in range(0, min(400, len(text)), 80):
        print(f"   {text[i:i+80]}")
    
    # Try Beaufort
    result = [(key[i] - prime_mod29[i]) % 29 for i in range(len(prime_mod29))]
    ioc = calculate_ioc(result)
    print(f"\n3. Deor - (Prime mod 29) [Beaufort]: IoC={ioc:.4f}")
    text = runes_to_latin(result)
    for i in range(0, min(400, len(text)), 80):
        print(f"   {text[i:i+80]}")
    
    # Check if prime_mod29 is already partially decoded - look for word patterns
    print("\n" + "="*60)
    print("WORD PATTERN ANALYSIS")
    print("="*60)
    
    text = runes_to_latin(prime_mod29)
    
    # Common English word patterns
    patterns = {
        'THE': 0, 'AND': 0, 'ING': 0, 'TION': 0, 'THAT': 0,
        'WITH': 0, 'THIS': 0, 'HAVE': 0, 'FROM': 0, 'THEY': 0,
        'WILL': 0, 'WHAT': 0, 'WERE': 0, 'WHEN': 0, 'YOUR': 0,
        'SHALL': 0, 'WHICH': 0, 'THEIR': 0, 'WOULD': 0, 'THERE': 0,
        # Cicada-specific
        'PRIME': 0, 'PRIMES': 0, 'WISDOM': 0, 'SACRED': 0, 'DIVINE': 0,
        'TRUTH': 0, 'PATH': 0, 'SEEK': 0, 'FIND': 0, 'KNOW': 0,
        'DEOR': 0, 'KOAN': 0, 'PARABLE': 0, 'WARNING': 0,
    }
    
    for word in patterns:
        patterns[word] = text.count(word)
    
    found = {k: v for k, v in patterns.items() if v > 0}
    print(f"\nWords found in prime-mod29 text:")
    for word, count in sorted(found.items(), key=lambda x: -x[1]):
        print(f"   {word}: {count}")
    
    # Try the totient transform (phi(p) = p-1 for primes)
    print("\n" + "="*60)
    print("TOTIENT (phi) TRANSFORM")
    print("="*60)
    
    totient_mod29 = [((IDX_TO_PRIME[r] - 1) % 29) for r in runes]
    
    print(f"\nTotient (p-1) mod 29:")
    print(f"   IoC: {calculate_ioc(totient_mod29):.4f}")
    
    text = runes_to_latin(totient_mod29)
    for i in range(0, min(400, len(text)), 80):
        print(f"   {text[i:i+80]}")
    
    # Apply Deor to totient
    result = [(totient_mod29[i] - key[i]) % 29 for i in range(len(totient_mod29))]
    ioc = calculate_ioc(result)
    print(f"\n   (Totient mod 29) - Deor: IoC={ioc:.4f}")
    text = runes_to_latin(result)
    for i in range(0, min(400, len(text)), 80):
        print(f"   {text[i:i+80]}")
    
    # Try combining: first apply one transform, then another
    print("\n" + "="*60)
    print("COMBINED TRANSFORMS")
    print("="*60)
    
    # Transform 1: Map to primes, then difference from linear prime sequence
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    # Each rune has a prime value - subtract nth prime to "de-prime"
    extended_primes = []
    p = 2
    for _ in range(1000):
        extended_primes.append(p)
        p += 1
        while not all(p % i != 0 for i in range(2, int(p**0.5)+1)):
            p += 1
    
    # De-prime: rune_prime - position_prime
    de_primed = []
    for i, r in enumerate(runes):
        rune_prime = IDX_TO_PRIME[r]
        pos_prime = extended_primes[i] if i < len(extended_primes) else 2
        de_primed.append((rune_prime - pos_prime) % 29)
    
    ioc = calculate_ioc(de_primed)
    print(f"\n1. Rune_Prime - Position_Prime mod 29: IoC={ioc:.4f}")
    text = runes_to_latin(de_primed[:200])
    print(f"   {text}")
    
    # Try the other direction
    de_primed2 = [(extended_primes[i] - IDX_TO_PRIME[runes[i]]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(de_primed2)
    print(f"\n2. Position_Prime - Rune_Prime mod 29: IoC={ioc:.4f}")
    text = runes_to_latin(de_primed2[:200])
    print(f"   {text}")
    
    # Now apply Deor to de-primed
    result = [(de_primed[i] - key[i]) % 29 for i in range(len(de_primed))]
    ioc = calculate_ioc(result)
    print(f"\n3. (Rune_Prime - Pos_Prime) - Deor: IoC={ioc:.4f}")
    text = runes_to_latin(result[:200])
    print(f"   {text}")

if __name__ == "__main__":
    main()

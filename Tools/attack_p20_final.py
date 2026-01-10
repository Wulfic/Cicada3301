"""
Page 20 - Final Creative Attacks
=================================
Last-ditch creative approaches.
"""

import collections
import itertools

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

GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                   53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

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
    print("PAGE 20 - FINAL CREATIVE ATTACKS")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    rows, cols = 28, 29
    grid = [[runes[r*cols + c] for c in range(cols)] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    deor_key = [ENGLISH_TO_IDX.get(c, 0) for c in deor]
    
    # Idea 1: What if "rearranging primes" means the GEMATRIA PRIMES form a permutation?
    # The 29 Gematria primes mod 29 give: 2,3,5,7,11,13,17,19,23,0,2,8,12,14,18,24,1,3,9,13,15,21,25,2,10,14,16,20,22
    # This has duplicates... but the UNIQUE values form a partial permutation
    
    print("\n--- Idea 1: Gematria prime mod 29 as column permutation ---")
    gp_mod29 = [p % 29 for p in GEMATRIA_PRIMES]
    print(f"GP mod 29: {gp_mod29}")
    
    # Use unique values only, in order of first appearance
    seen = set()
    unique_order = []
    for v in gp_mod29:
        if v not in seen:
            unique_order.append(v)
            seen.add(v)
    # Add missing values
    for i in range(29):
        if i not in seen:
            unique_order.append(i)
    
    print(f"Unique order: {unique_order}")
    
    # Read columns in this order
    reordered = []
    for c in unique_order:
        for r in range(rows):
            reordered.append(grid[r][c])
    
    extended_deor = deor_key * (len(reordered) // len(deor_key) + 1)
    extended_deor = extended_deor[:len(reordered)]
    
    result = decrypt_vigenere(reordered, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"Unique GP order + Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Idea 2: What if the key is derived from BOTH Page 19 plaintext AND Deor?
    print("\n--- Idea 2: P19 plaintext + Deor combined ---")
    
    p19_plaintext = "REARRANGINGTHEPRIMESNUMBERSWILLSHOWAPATHTOTHEDEOR"
    p19_key = [ENGLISH_TO_IDX.get(c, 0) for c in p19_plaintext if c in ENGLISH_TO_IDX]
    
    print(f"P19 key length: {len(p19_key)}")
    
    extended_p19 = p19_key * (len(runes) // len(p19_key) + 1)
    extended_p19 = extended_p19[:len(runes)]
    
    # P19 then Deor
    step1 = decrypt_vigenere(runes, extended_p19, 'sub')
    result = decrypt_vigenere(step1, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"(C - P19) - Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Deor then P19
    step1 = decrypt_vigenere(runes, extended_deor, 'sub')
    result = decrypt_vigenere(step1, extended_p19, 'sub')
    ioc = calculate_ioc(result)
    print(f"(C - Deor) - P19: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Idea 3: XOR-like operation: (C - Deor - prime[i]) mod 29
    print("\n--- Idea 3: C - Deor - prime[i] ---")
    
    result = []
    for i, c in enumerate(runes):
        d = extended_deor[i]
        p = GEMATRIA_PRIMES[i % 29] % 29
        result.append((c - d - p) % 29)
    
    ioc = calculate_ioc(result)
    print(f"C - Deor - prime[i%%29]: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Idea 4: What if page numbers are relevant? Page 20 = 2² × 5
    print("\n--- Idea 4: Page 20 factors (2² × 5) as key ---")
    
    key_from_factors = [2, 2, 5]  # 20 = 4 × 5 = 2² × 5
    extended_factors = key_from_factors * (len(runes) // len(key_from_factors) + 1)
    extended_factors = extended_factors[:len(runes)]
    
    result = decrypt_vigenere(runes, extended_factors, 'sub')
    result = decrypt_vigenere(result, extended_deor, 'sub')
    ioc = calculate_ioc(result)
    print(f"(C - [2,2,5]) - Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Idea 5: The 7 Deor strophes as 7 different keys for 4-row blocks
    print("\n--- Idea 5: Different Deor strophe for each 4-row block ---")
    
    # Get strophe starting positions from Deor (approximate)
    strophe_starts = [0, 200, 400, 550, 700, 900, 1100]  # Approximate positions
    
    result = []
    for r in range(rows):
        strophe_idx = r // 4  # Which strophe (0-6)
        if strophe_idx < len(strophe_starts):
            start = strophe_starts[strophe_idx]
        else:
            start = 0
        
        for c in range(cols):
            pos = r * cols + c
            deor_pos = (start + c) % len(deor)
            key_val = deor_key[deor_pos]
            result.append((grid[r][c] - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Strophe-indexed Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # Idea 6: Multiplicative cipher with prime
    print("\n--- Idea 6: Multiplicative cipher C × prime⁻¹ mod 29 ---")
    
    # Multiplicative inverse of 2 mod 29 is 15 (since 2×15=30≡1 mod 29)
    def mod_inverse(a, m):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None
    
    prime = 2
    inv = mod_inverse(prime, 29)
    if inv:
        result = [(c * inv) % 29 for c in runes]
        ioc = calculate_ioc(result)
        print(f"C × {prime}⁻¹ (={inv}) mod 29: IoC={ioc:.4f}")
        print(f"Text: {runes_to_latin(result[:80])}")
    
    # Try different primes
    for p in [3, 5, 7, 11]:
        inv = mod_inverse(p, 29)
        if inv:
            result = [(c * inv) % 29 for c in runes]
            step2 = decrypt_vigenere(result, extended_deor, 'sub')
            ioc = calculate_ioc(step2)
            if ioc > 1.1:
                print(f"C × {p}⁻¹ + Deor: IoC={ioc:.4f}")

if __name__ == "__main__":
    main()

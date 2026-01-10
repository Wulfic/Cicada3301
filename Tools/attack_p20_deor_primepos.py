"""
Page 20 - Key from Deor at Prime Positions
==========================================
Extract characters from Deor poem at prime-numbered positions.
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
        text = f.read()
    return text

def main():
    print("="*60)
    print("PAGE 20 - DEOR PRIME POSITIONS")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor_text = load_deor()
    
    # Clean Deor - just alpha characters
    deor_clean = ''.join(c for c in deor_text.upper() if c.isalpha())
    print(f"Deor clean length: {len(deor_clean)}")
    
    # Extract characters at prime positions
    primes_under_1000 = [p for p in range(2, 1000) if is_prime(p)]
    
    deor_primes = []
    for p in primes_under_1000:
        if p - 1 < len(deor_clean):  # 1-indexed
            deor_primes.append(deor_clean[p - 1])
    
    prime_key_text = ''.join(deor_primes)
    print(f"\nDeor at prime positions ({len(prime_key_text)} chars):")
    print(prime_key_text[:100])
    
    # Convert to indices
    prime_key_idx = [ENGLISH_TO_IDX.get(c, 0) for c in prime_key_text]
    
    # Apply to Page 20
    extended_key = prime_key_idx * (len(runes) // len(prime_key_idx) + 1)
    extended_key = extended_key[:len(runes)]
    
    for mode in ['sub', 'add']:
        result = decrypt_vigenere(runes, extended_key, mode)
        ioc = calculate_ioc(result)
        print(f"\nDeor@primes {mode.upper()}: IoC={ioc:.4f}")
        print(f"Text: {runes_to_latin(result[:100])}")
    
    # What about extracting using the Gematria prime VALUES?
    # Rune 0 (F) has prime value 2, Rune 1 (U) has prime value 3, etc.
    print("\n" + "="*60)
    print("DEOR AT GEMATRIA PRIME VALUE POSITIONS")
    print("="*60)
    
    GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    deor_gematria_primes = []
    for p in GEMATRIA_PRIMES:
        if p - 1 < len(deor_clean):
            deor_gematria_primes.append(deor_clean[p - 1])
    
    print(f"Deor at Gematria prime positions: {''.join(deor_gematria_primes)}")
    
    gem_key_idx = [ENGLISH_TO_IDX.get(c, 0) for c in deor_gematria_primes]
    
    extended_key = gem_key_idx * (len(runes) // len(gem_key_idx) + 1)
    extended_key = extended_key[:len(runes)]
    
    for mode in ['sub', 'add']:
        result = decrypt_vigenere(runes, extended_key, mode)
        ioc = calculate_ioc(result)
        print(f"\nGematria primes {mode.upper()}: IoC={ioc:.4f}")
        print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if we use the prime VALUES of each rune as an index into Deor?
    print("\n" + "="*60)
    print("AUTOKEY: Cipher rune's prime value indexes into Deor")
    print("="*60)
    
    # For each cipher rune, its prime value P -> Deor[P] is the key char
    result = []
    for i, c in enumerate(runes):
        prime_val = GEMATRIA_PRIMES[c]  # Prime value of this rune
        if prime_val - 1 < len(deor_clean):
            key_char = deor_clean[prime_val - 1]
            key_val = ENGLISH_TO_IDX.get(key_char, 0)
        else:
            key_val = 0
        result.append((c - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Cipher prime -> Deor lookup: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What about cumulative prime sums?
    print("\n" + "="*60)
    print("CUMULATIVE PRIME SUMS")
    print("="*60)
    
    # Key[i] = sum of first i primes mod 29
    cumsum_primes = []
    s = 0
    for i in range(812):
        if i < len(GEMATRIA_PRIMES):
            s += GEMATRIA_PRIMES[i]
        cumsum_primes.append(s % 29)
    
    result = decrypt_vigenere(runes, cumsum_primes, 'sub')
    ioc = calculate_ioc(result)
    print(f"Cumulative prime sum key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if we use prime GAPS as the key?
    print("\n" + "="*60)
    print("PRIME GAPS AS KEY")
    print("="*60)
    
    prime_gaps = []
    for i in range(len(GEMATRIA_PRIMES) - 1):
        prime_gaps.append(GEMATRIA_PRIMES[i+1] - GEMATRIA_PRIMES[i])
    
    print(f"Prime gaps: {prime_gaps}")
    
    extended_gaps = prime_gaps * (len(runes) // len(prime_gaps) + 1)
    extended_gaps = extended_gaps[:len(runes)]
    gap_key = [g % 29 for g in extended_gaps]
    
    result = decrypt_vigenere(runes, gap_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Prime gaps key: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")

if __name__ == "__main__":
    main()

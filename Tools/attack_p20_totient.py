"""
Page 20 - Totient Function Attack
==================================
Pages 55 and 73 were solved with φ(prime) = prime - 1.
Try applying similar methods to Page 20.
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

def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

PRIMES = sieve_of_eratosthenes(10000)  # Generate enough primes

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

def totient(n):
    """Euler's totient function."""
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

def main():
    print("="*60)
    print("PAGE 20 - TOTIENT FUNCTION ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    
    print(f"Page 20: {len(runes)} runes")
    
    # Method 1: Standard φ(prime) key like Pages 55/73
    print("\n--- Method 1: φ(prime[i]) mod 29 key ---")
    
    phi_key = [(PRIMES[i] - 1) % 29 for i in range(len(runes))]
    
    result = [(runes[i] - phi_key[i]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(result)
    print(f"C - φ(prime[i]) mod 29: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    result = [(runes[i] + phi_key[i]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(result)
    print(f"C + φ(prime[i]) mod 29: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 2: φ(prime) combined with Deor
    print("\n--- Method 2: φ(prime) then Deor ---")
    
    deor_key = [ENGLISH_TO_IDX.get(c, 0) for c in deor]
    extended_deor = deor_key * (len(runes) // len(deor_key) + 1)
    extended_deor = extended_deor[:len(runes)]
    
    # Step 1: Apply φ(prime)
    step1 = [(runes[i] - phi_key[i]) % 29 for i in range(len(runes))]
    
    # Step 2: Apply Deor
    result = [(step1[i] - extended_deor[i]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(result)
    print(f"(C - φ) - Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 3: Deor then φ(prime)
    print("\n--- Method 3: Deor then φ(prime) ---")
    
    step1 = [(runes[i] - extended_deor[i]) % 29 for i in range(len(runes))]
    result = [(step1[i] - phi_key[i]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(result)
    print(f"(C - Deor) - φ: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 4: Use GEMATRIA prime values (not sequential primes)
    print("\n--- Method 4: φ(Gematria prime of cipher rune) ---")
    
    GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                       53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    # φ(prime) = prime - 1 for primes
    result = []
    for c in runes:
        prime_val = GEMATRIA_PRIMES[c]
        phi_val = prime_val - 1  # φ(p) = p-1 for prime p
        result.append((c - (phi_val % 29)) % 29)
    
    ioc = calculate_ioc(result)
    print(f"C - φ(GP[C]) mod 29: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 5: Use cumulative φ values
    print("\n--- Method 5: Cumulative φ(prime) ---")
    
    cumsum = 0
    result = []
    for i, c in enumerate(runes):
        cumsum += PRIMES[i] - 1  # Cumulative φ
        result.append((c - (cumsum % 29)) % 29)
    
    ioc = calculate_ioc(result)
    print(f"C - Σφ(prime[0..i]) mod 29: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 6: "Rearranging primes" = sort positions by φ value?
    print("\n--- Method 6: Read in φ-sorted order ---")
    
    # Sort positions by their φ(prime[pos]) mod 29
    positions = list(range(len(runes)))
    sorted_by_phi = sorted(positions, key=lambda i: (PRIMES[i] - 1) % 29)
    
    reordered = [runes[p] for p in sorted_by_phi]
    
    ioc = calculate_ioc(reordered)
    print(f"Read in φ-sorted order: IoC={ioc:.4f}")
    
    # Apply Deor
    result = [(reordered[i] - extended_deor[i]) % 29 for i in range(len(reordered))]
    ioc = calculate_ioc(result)
    print(f"φ-sorted then Deor: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 7: Use φ values to determine Deor offset
    print("\n--- Method 7: Deor offset = φ(prime[i]) ---")
    
    result = []
    for i, c in enumerate(runes):
        phi_offset = (PRIMES[i] - 1) % len(deor)
        key_char = deor[phi_offset]
        key_val = ENGLISH_TO_IDX.get(key_char, 0)
        result.append((c - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Deor[φ(prime[i]) mod len]: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")

if __name__ == "__main__":
    main()

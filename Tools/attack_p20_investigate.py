"""
Page 20 - Investigate High IoC Result
=====================================
The cipher-prime-to-Deor lookup gave IoC 1.7! Investigate why.
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

GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

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

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    with open(deor_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def main():
    print("="*60)
    print("PAGE 20 - INVESTIGATE HIGH IoC RESULT")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor_text = load_deor()
    deor_clean = ''.join(c for c in deor_text.upper() if c.isalpha())
    
    # Reproduce the high-IoC method
    result = []
    key_values_used = []
    for i, c in enumerate(runes):
        prime_val = GEMATRIA_PRIMES[c]  # Prime value of this rune
        if prime_val - 1 < len(deor_clean):
            key_char = deor_clean[prime_val - 1]
            key_val = ENGLISH_TO_IDX.get(key_char, 0)
        else:
            key_val = 0
        key_values_used.append(key_val)
        result.append((c - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Method: C[i] - Deor[prime(C[i])] mod 29")
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:200])}")
    
    # Check if the key is effectively constant or low-entropy
    key_counts = collections.Counter(key_values_used)
    print(f"\nKey value distribution:")
    print(f"Unique key values: {len(key_counts)}")
    print(f"Most common: {key_counts.most_common(10)}")
    
    # What Deor characters are at the prime positions?
    print("\n--- Deor chars at prime positions ---")
    for i in range(29):
        prime_val = GEMATRIA_PRIMES[i]
        if prime_val - 1 < len(deor_clean):
            char = deor_clean[prime_val - 1]
            idx = ENGLISH_TO_IDX.get(char, 0)
            print(f"Rune {i} (prime {prime_val}): Deor[{prime_val}] = '{char}' -> idx {idx}")
    
    # The problem: Each cipher rune maps to a FIXED key value
    # If cipher rune is 0 (F), always use Deor[2-1] = Deor[1]
    # If cipher rune is 1 (U), always use Deor[3-1] = Deor[2]
    # This is just a SUBSTITUTION cipher! Not Vigenère!
    
    print("\n" + "="*60)
    print("THIS IS A MONOALPHABETIC SUBSTITUTION!")
    print("="*60)
    
    # Create the substitution table
    sub_table = {}
    for i in range(29):
        prime_val = GEMATRIA_PRIMES[i]
        if prime_val - 1 < len(deor_clean):
            key_char = deor_clean[prime_val - 1]
            key_val = ENGLISH_TO_IDX.get(key_char, 0)
            sub_table[i] = (i - key_val) % 29
    
    print(f"Substitution table (input -> output):")
    for inp, out in sorted(sub_table.items()):
        print(f"  {inp} ({IDX_TO_LATIN[inp]}) -> {out} ({IDX_TO_LATIN[out]})")
    
    # Check how many unique outputs
    unique_outputs = set(sub_table.values())
    print(f"\nUnique outputs: {len(unique_outputs)}")
    
    # If there are collisions, that explains high IoC (fewer letters -> higher IoC)
    if len(unique_outputs) < 29:
        print("COLLISION DETECTED - explains artificially high IoC!")
        
        # Find which inputs map to same output
        output_sources = collections.defaultdict(list)
        for inp, out in sub_table.items():
            output_sources[out].append(inp)
        
        print("\nOutputs with multiple inputs:")
        for out, inps in output_sources.items():
            if len(inps) > 1:
                print(f"  {out} ({IDX_TO_LATIN[out]}) <- {[(i, IDX_TO_LATIN[i]) for i in inps]}")
    
    # So this method just creates a non-bijective substitution - not decryption!
    
    # Let's try the CORRECT interpretation: use Deor as running key
    # but the "path" through Deor is determined by the CIPHER'S prime values
    print("\n" + "="*60)
    print("CORRECT INTERPRETATION: Deor running key with prime-based offset")
    print("="*60)
    
    # Method 1: Start at prime(cipher[0]), step by 1
    start_pos = GEMATRIA_PRIMES[runes[0]] - 1
    result = []
    for i, c in enumerate(runes):
        pos = (start_pos + i) % len(deor_clean)
        key_char = deor_clean[pos]
        key_val = ENGLISH_TO_IDX.get(key_char, 0)
        result.append((c - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Start at prime(C[0]), step 1: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 2: Use sum of all prime values so far as position
    cumsum = 0
    result = []
    for i, c in enumerate(runes):
        cumsum += GEMATRIA_PRIMES[c]
        pos = (cumsum - 1) % len(deor_clean)
        key_char = deor_clean[pos]
        key_val = ENGLISH_TO_IDX.get(key_char, 0)
        result.append((c - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Cumulative prime sum as position: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Method 3: Use PLAINTEXT's prime values to step through Deor (Autokey)
    print("\n--- Autokey with prime step ---")
    result = []
    pos = 0
    for i, c in enumerate(runes):
        key_char = deor_clean[pos % len(deor_clean)]
        key_val = ENGLISH_TO_IDX.get(key_char, 0)
        plain = (c - key_val) % 29
        result.append(plain)
        # Step by plaintext's prime value
        pos += GEMATRIA_PRIMES[plain]
    
    ioc = calculate_ioc(result)
    print(f"Autokey prime step: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")

if __name__ == "__main__":
    main()

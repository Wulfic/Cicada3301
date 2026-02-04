"""
Deep analysis of the high-IoC totient outputs.
The IoC is 2.0+ but output is gibberish - investigate why.
"""

import os
from collections import Counter

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
             31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
             73, 79, 83, 89, 97, 101, 103, 107, 109]

def rune_to_index(rune):
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

def totient(n):
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

def load_page(page_num):
    page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    subdir = f"page_{page_num:02d}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            runes = [c for c in content if c in GP_RUNES]
            return runes
    return []

def apply_totient_cipher(runes, operation='sub'):
    result = []
    for rune in runes:
        idx = rune_to_index(rune)
        if idx is not None:
            prime_val = GP_PRIMES[idx]
            phi = totient(prime_val)
            shift = phi % 29
            if operation == 'sub':
                new_idx = (idx - shift) % 29
            else:
                new_idx = (idx + shift) % 29
            result.append(new_idx)
    return result

def indices_to_latin(indices):
    return ''.join(index_to_latin(i) for i in indices)

def calculate_ioc(indices):
    n = len(indices)
    if n <= 1:
        return 0
    counts = Counter(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29

def main():
    print("="*60)
    print("FREQUENCY ANALYSIS OF TOTIENT OUTPUTS")
    print("="*60)
    
    # Best pages
    pages = [
        (21, 'add'),
        (22, 'sub'),
        (24, 'add'),
    ]
    
    # Standard English letter frequencies (approximate, for comparison)
    english_freqs = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
        'S': 6.3, 'H': 6.1, 'R': 6.0
    }
    
    for page_num, op in pages:
        print(f"\n{'='*60}")
        print(f"PAGE {page_num} (Totient {op.upper()})")
        print(f"{'='*60}")
        
        runes = load_page(page_num)
        if not runes:
            continue
        
        # Apply totient
        result = apply_totient_cipher(runes, op)
        latin = indices_to_latin(result)
        ioc = calculate_ioc(result)
        
        print(f"IoC: {ioc:.4f}")
        print(f"Length: {len(result)}")
        print(f"\nFull text:")
        print(latin)
        
        # Frequency analysis
        counts = Counter(result)
        total = len(result)
        print(f"\nFrequency distribution (sorted):")
        for idx, count in sorted(counts.items(), key=lambda x: -x[1])[:10]:
            freq = (count / total) * 100
            latin_char = GP_LATIN[idx]
            print(f"  {latin_char:3} ({idx:2}): {count:3} = {freq:5.2f}%")
        
        # Check for English-like patterns
        print(f"\nLooking for common patterns...")
        text = latin.upper()
        
        # Common trigrams in English
        trigrams = ['THE', 'AND', 'ING', 'ION', 'ENT', 'TIO', 'FOR', 'HER']
        for trig in trigrams:
            count = text.count(trig)
            if count > 0:
                print(f"  '{trig}' appears {count} times")
        
        # Common bigrams
        bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
        for big in bigrams:
            count = text.count(big)
            if count > 1:
                print(f"  '{big}' appears {count} times")
        
        # Look for vowel patterns
        vowels = 0
        consonants = 0
        for c in result:
            if c in [24, 18, 10, 3, 1]:  # A, E, I, O, U
                vowels += 1
            else:
                consonants += 1
        print(f"\nVowel/Consonant ratio: {vowels}/{consonants} = {vowels/consonants:.2f}")
        print(f"  (English is typically around 0.40)")

if __name__ == "__main__":
    main()

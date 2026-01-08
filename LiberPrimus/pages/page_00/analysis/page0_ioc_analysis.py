#!/usr/bin/env python3
"""
Page 0 Index of Coincidence (IoC) Analysis
==========================================
Analyze Page 0 to find optimal key length using IoC.
Same method that successfully found key lengths for Pages 1-4.
"""

import math
from collections import Counter

# Gematria Primus - 29 character runic alphabet
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_RUNE = {v: k for k, v in RUNE_TO_INDEX.items()}
INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                   'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                   'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def load_runes(filepath):
    """Load runes from file, extracting only valid rune characters."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    runes = []
    for char in text:
        if char in RUNE_TO_INDEX:
            runes.append(char)
    
    return runes

def calculate_ioc(indices):
    """Calculate Index of Coincidence for a list of indices."""
    if len(indices) < 2:
        return 0.0
    
    n = len(indices)
    counts = Counter(indices)
    
    numerator = sum(count * (count - 1) for count in counts.values())
    denominator = n * (n - 1)
    
    return numerator / denominator if denominator > 0 else 0.0

def average_ioc_for_key_length(rune_indices, key_length):
    """Calculate average IoC across all columns for a given key length."""
    columns = [[] for _ in range(key_length)]
    
    for i, idx in enumerate(rune_indices):
        columns[i % key_length].append(idx)
    
    iocs = [calculate_ioc(col) for col in columns if len(col) > 1]
    
    return sum(iocs) / len(iocs) if iocs else 0.0

def find_optimal_key_lengths(rune_indices, max_length=150):
    """Find key lengths with highest IoC values."""
    results = []
    
    for key_len in range(2, min(max_length + 1, len(rune_indices) // 2)):
        avg_ioc = average_ioc_for_key_length(rune_indices, key_len)
        results.append((key_len, avg_ioc))
    
    # Sort by IoC descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def analyze_frequency(rune_indices):
    """Analyze frequency distribution of runes."""
    counts = Counter(rune_indices)
    total = len(rune_indices)
    
    freq = [(idx, count, count/total * 100, INDEX_TO_LETTER[idx]) 
            for idx, count in counts.most_common()]
    
    return freq

def main():
    # Load Page 0 runes
    filepath = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt"
    runes = load_runes(filepath)
    rune_indices = [RUNE_TO_INDEX[r] for r in runes]
    
    print("=" * 70)
    print("PAGE 0 INDEX OF COINCIDENCE ANALYSIS")
    print("=" * 70)
    print(f"\nTotal runes: {len(runes)}")
    
    # Random IoC expectation for 29-character alphabet
    random_ioc = 1/29
    # English-like IoC (higher due to letter frequency distribution)
    english_ioc = 0.0667  # Approximate for English
    
    print(f"Random IoC (29 chars): {random_ioc:.4f}")
    print(f"English-like IoC: {english_ioc:.4f}")
    
    # Frequency analysis
    print("\n" + "-" * 70)
    print("FREQUENCY ANALYSIS")
    print("-" * 70)
    freq = analyze_frequency(rune_indices)
    print(f"{'Idx':<4} {'Letter':<6} {'Count':<6} {'Freq%':<8}")
    for idx, count, pct, letter in freq[:15]:
        print(f"{idx:<4} {letter:<6} {count:<6} {pct:.2f}%")
    
    # IoC analysis for different key lengths
    print("\n" + "-" * 70)
    print("IOC ANALYSIS BY KEY LENGTH")
    print("-" * 70)
    
    results = find_optimal_key_lengths(rune_indices, max_length=150)
    
    print(f"\nTop 30 key lengths by IoC:")
    print(f"{'Rank':<5} {'KeyLen':<8} {'IoC':<10} {'Prime?':<8} {'Notes'}")
    print("-" * 60)
    
    for rank, (key_len, ioc) in enumerate(results[:30], 1):
        prime_str = "PRIME" if is_prime(key_len) else ""
        
        # Check for known patterns
        notes = ""
        if key_len == 71:
            notes = "** Page 1,5 key length **"
        elif key_len == 83:
            notes = "** Page 2,3 key length **"
        elif key_len == 103:
            notes = "** Page 4 key length **"
        elif key_len in [8, 11]:
            notes = f"Length of 'DIVINITY' or 'CIRCUMFERENCE'"
        elif ioc > english_ioc * 0.8:
            notes = "Strong candidate"
        
        print(f"{rank:<5} {key_len:<8} {ioc:.6f}  {prime_str:<8} {notes}")
    
    # Check all prime key lengths specifically
    print("\n" + "-" * 70)
    print("PRIME KEY LENGTHS (focus area based on Pages 1-4)")
    print("-" * 70)
    
    primes = [p for p in range(2, 150) if is_prime(p)]
    prime_results = []
    
    for p in primes:
        if p < len(rune_indices) // 2:
            ioc = average_ioc_for_key_length(rune_indices, p)
            prime_results.append((p, ioc))
    
    prime_results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Prime':<8} {'IoC':<12} {'Notes'}")
    print("-" * 40)
    for prime, ioc in prime_results[:20]:
        notes = ""
        if prime == 71:
            notes = "Page 1,5"
        elif prime == 83:
            notes = "Page 2,3"
        elif prime == 103:
            notes = "Page 4"
        print(f"{prime:<8} {ioc:.6f}    {notes}")
    
    # Check small key lengths (for simple ciphers like Atbash+Vigenère)
    print("\n" + "-" * 70)
    print("SMALL KEY LENGTHS (for Vigenère-type ciphers)")
    print("-" * 70)
    
    small_results = []
    for kl in range(2, 20):
        ioc = average_ioc_for_key_length(rune_indices, kl)
        small_results.append((kl, ioc))
    
    small_results.sort(key=lambda x: x[1], reverse=True)
    
    for kl, ioc in small_results:
        keyword_hint = ""
        if kl == 8:
            keyword_hint = "DIVINITY length"
        elif kl == 13:
            keyword_hint = "CIRCUMFERENCE length"
        elif kl == 6:
            keyword_hint = "INSTAR, EMERGE length"
        elif kl == 7:
            keyword_hint = "PARABLE, SURFACE length"
        
        print(f"KeyLen {kl:<3}: IoC = {ioc:.6f}  {keyword_hint}")
    
    # Direct IoC of the text (no key)
    print("\n" + "-" * 70)
    print("DIRECT TEXT IOC (no cipher)")
    print("-" * 70)
    direct_ioc = calculate_ioc(rune_indices)
    print(f"Direct IoC: {direct_ioc:.6f}")
    print(f"Expected random: {random_ioc:.4f}")
    print(f"Expected English: {english_ioc:.4f}")
    
    if direct_ioc > english_ioc * 0.7:
        print("⚠️ High IoC suggests simple substitution or plaintext!")
    elif direct_ioc < random_ioc * 1.3:
        print("IoC near random - likely polyalphabetic cipher with long key")
    
    # Save results
    output_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\analysis\PAGE0_IOC_RESULTS.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("PAGE 0 IOC ANALYSIS RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total runes: {len(runes)}\n")
        f.write(f"Direct IoC: {direct_ioc:.6f}\n")
        f.write(f"Expected random (29 chars): {random_ioc:.4f}\n")
        f.write(f"Expected English-like: {english_ioc:.4f}\n\n")
        
        f.write("TOP KEY LENGTHS BY IOC:\n")
        f.write("-" * 40 + "\n")
        for rank, (kl, ioc) in enumerate(results[:50], 1):
            prime = "P" if is_prime(kl) else " "
            f.write(f"{rank:3}. KeyLen={kl:3} {prime} IoC={ioc:.6f}\n")
        
        f.write("\nBEST PRIME KEY LENGTHS:\n")
        f.write("-" * 40 + "\n")
        for prime, ioc in prime_results[:20]:
            f.write(f"Prime {prime:3}: IoC={ioc:.6f}\n")
    
    print(f"\nResults saved to: {output_path}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()

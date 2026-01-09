#!/usr/bin/env python3
"""
INDEX OF COINCIDENCE ANALYSIS

Analyze the cipher type based on Index of Coincidence (IoC).
- English text IoC ≈ 0.065-0.068
- Random/polyalphabetic IoC ≈ 0.038
- Monoalphabetic IoC ≈ English IoC

This helps determine what type of cipher is used.
"""

from pathlib import Path
from collections import Counter
import math

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    rune_file = page_dir / "runes.txt"
    if not rune_file.exists():
        return None
    with open(rune_file, 'r', encoding='utf-8') as f:
        return f.read()

def calculate_ioc(data):
    """Calculate Index of Coincidence for a sequence of integers."""
    if len(data) < 2:
        return 0
    
    freq = Counter(data)
    n = len(data)
    
    numerator = sum(f * (f - 1) for f in freq.values())
    denominator = n * (n - 1)
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

def calculate_expected_ioc(alphabet_size, text_ioc=0.0686):
    """
    Calculate expected IoC for random text.
    Random = 1/alphabet_size = 1/29 ≈ 0.0345
    English-like = ~0.0686
    """
    random_ioc = 1.0 / alphabet_size
    return random_ioc, text_ioc

def find_likely_key_length(cipher, max_length=200):
    """Find likely key length using Kasiski examination and IoC."""
    results = []
    
    for key_len in range(1, min(max_length + 1, len(cipher) // 3)):
        # Split ciphertext into columns based on key length
        columns = [[] for _ in range(key_len)]
        for i, c in enumerate(cipher):
            columns[i % key_len].append(c)
        
        # Calculate IoC for each column and average
        column_iocs = [calculate_ioc(col) for col in columns if len(col) > 1]
        if column_iocs:
            avg_ioc = sum(column_iocs) / len(column_iocs)
            results.append((key_len, avg_ioc))
    
    # Sort by IoC (higher is better for periodic cipher)
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def analyze_page(page_num):
    """Analyze a single page's cipher characteristics."""
    rune_text = load_page(page_num)
    if not rune_text:
        return None
    
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    if len(cipher) < 20:
        return None
    
    # Calculate overall IoC
    ioc = calculate_ioc(cipher)
    
    # Find likely key lengths
    key_lengths = find_likely_key_length(cipher)
    
    # Calculate frequency distribution
    freq = Counter(cipher)
    total = len(cipher)
    freq_pct = {LETTERS[k]: v / total * 100 for k, v in freq.most_common()}
    
    return {
        'page': page_num,
        'length': len(cipher),
        'ioc': ioc,
        'top_key_lengths': key_lengths[:10],
        'freq': freq_pct
    }

def main():
    print("INDEX OF COINCIDENCE ANALYSIS")
    print("=" * 80)
    
    random_ioc, english_ioc = calculate_expected_ioc(29)
    print(f"\nReference IoC values (29-letter alphabet):")
    print(f"  Random/perfect poly:  {random_ioc:.5f}")
    print(f"  English-like mono:    {english_ioc:.5f}")
    print(f"  Vigenère with short key: between random and English")
    
    print("\n" + "=" * 80)
    print("PAGE ANALYSIS")
    print("=" * 80)
    print(f"{'Page':>4} | {'Length':>6} | {'IoC':>7} | {'Type Assessment':>25} | Top Key Lengths")
    print("-" * 80)
    
    # Analyze all pages
    for page_num in list(range(0, 75)):
        result = analyze_page(page_num)
        if result:
            ioc = result['ioc']
            
            # Assess cipher type
            if ioc > 0.055:
                assessment = "Mono/Short Key"
            elif ioc > 0.045:
                assessment = "Short Vigenère (~10)"
            elif ioc > 0.038:
                assessment = "Long Vigenère"
            else:
                assessment = "Random/Running Key"
            
            # Get top 3 key lengths
            top_keys = [str(kl[0]) for kl in result['top_key_lengths'][:3]]
            top_keys_str = ", ".join(top_keys)
            
            print(f"{result['page']:>4} | {result['length']:>6} | {ioc:.5f} | {assessment:>25} | {top_keys_str}")
    
    print("\n" + "=" * 80)
    print("UNSOLVED PAGES DETAILED ANALYSIS")
    print("=" * 80)
    
    # Focus on unsolved pages
    for page_num in [17, 18, 19, 20, 21, 22, 50, 51, 52, 53, 54]:
        result = analyze_page(page_num)
        if result:
            print(f"\n--- Page {page_num} ---")
            print(f"Length: {result['length']} runes")
            print(f"IoC: {result['ioc']:.5f}")
            
            print("\nTop 10 likely key lengths (by column IoC):")
            for kl, ioc_val in result['top_key_lengths'][:10]:
                is_prime = all(kl % i != 0 for i in range(2, int(kl**0.5)+1)) if kl > 1 else False
                prime_mark = "PRIME" if is_prime else ""
                print(f"  Key length {kl:3d}: IoC = {ioc_val:.5f} {prime_mark}")
            
            print("\nTop 5 most frequent runes:")
            for rune, pct in list(result['freq'].items())[:5]:
                print(f"  {rune}: {pct:.1f}%")

if __name__ == '__main__':
    main()

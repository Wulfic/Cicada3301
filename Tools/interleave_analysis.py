#!/usr/bin/env python3
"""
Interleave Analysis Tool

Based on the insight that pages may contain hints for other pages,
and that the cipher might use interleaving, let's test if pages
are interleaved versions of each other.

Also exploring the key derived from Page 0 - Page 56.
"""

import os
import re
from collections import Counter

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛂ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                   'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
                   'A', 'AE', 'Y', 'IA', 'EA']

INDEX_TO_PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def read_page_flat(page_num):
    """Read page as flat list of indices"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    try:
        with open(rune_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    return [RUNE_TO_INDEX[r] for r in content if r in RUNE_TO_INDEX]

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

def analyze_key_pattern():
    """Analyze the key derived from Page 0 - Page 56"""
    print("=" * 70)
    print("KEY PATTERN ANALYSIS")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    page_56 = read_page_flat(56)
    
    # Key = Page 0 - Page 56
    key = [(page_0[i] - page_56[i]) % 29 for i in range(min(len(page_0), len(page_56)))]
    key_text = indices_to_text(key)
    
    print(f"\nDerived key (Page 0 - Page 56):")
    print(f"  {key_text}")
    print(f"  Length: {len(key)}")
    
    # Frequency analysis of the key
    counter = Counter(key)
    print(f"\nKey index frequencies:")
    for idx, count in counter.most_common(10):
        print(f"  {INDEX_TO_LETTER[idx]:4s} ({idx:2d}): {count}")
    
    # Check if key looks like text
    print("\nDoes the key look like plaintext?")
    
    # Check for common digraphs in key
    common_patterns = ['THE', 'AND', 'ING', 'ION', 'ENT', 'TIO', 'FOR', 'ATE']
    for pattern in common_patterns:
        if pattern in key_text:
            print(f"  Found '{pattern}' in key")
    
    # The key might itself be encrypted - try to decrypt it
    print("\nTrying to decrypt the key with various shifts...")
    for shift in range(29):
        shifted = [(k - shift) % 29 for k in key]
        text = indices_to_text(shifted)
        score = sum(1 for p in common_patterns if p in text)
        if score >= 2:
            print(f"  Shift {shift:2d} ({INDEX_TO_LETTER[shift]:4s}): score={score}, {text[:50]}")

def test_interleave_extraction():
    """Test extracting interleaved messages from pages"""
    print("\n" + "=" * 70)
    print("INTERLEAVE EXTRACTION")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    
    # Try extracting every Nth character
    for interval in [2, 3, 5, 7, 11, 13, 29]:
        for offset in range(min(interval, 3)):
            extracted = page_0[offset::interval]
            text = indices_to_text(extracted)
            
            # Score based on common words
            score = 0
            for pattern in ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'TH']:
                score += text.count(pattern)
            
            if score >= 2:
                print(f"\n  Every {interval}th char, offset {offset}:")
                print(f"    Score: {score}")
                print(f"    Text: {text[:80]}")

def analyze_autokey():
    """Test autokey cipher where plaintext is used as key"""
    print("\n" + "=" * 70)
    print("AUTOKEY CIPHER ANALYSIS")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    page_56 = read_page_flat(56)  # Known plaintext
    
    # In autokey: C[i] = P[i] + K[i] where K[0..n] = primer, K[n+1..] = P
    # If we know the plaintext, we can derive the primer
    
    # For Page 0, assume it's encrypted with autokey using Page 56-style plaintext
    print("\nIf Page 0 uses autokey cipher with plaintext as running key:")
    
    # Try various primer lengths
    for primer_len in [1, 2, 3, 4, 5, 6, 7, 8]:
        # Assume first primer_len characters of key are the primer
        # Then key[i] = plaintext[i - primer_len] for i >= primer_len
        
        # We can iterate to find the primer
        # For now, just test with known patterns
        primers = [
            [16, 8, 18],  # THE
            [13, 10],     # PI
            [10, 13],     # IP
            [23, 10, 1, 10, 9, 10, 16, 26],  # DIVINITY
        ]
        
        for primer in primers:
            if len(primer) != primer_len:
                continue
            
            decrypted = []
            key = list(primer)
            
            for i, c in enumerate(page_0[:50]):
                k = key[i]
                p = (c - k) % 29
                decrypted.append(p)
                key.append(p)  # Autokey: plaintext becomes next key
            
            text = indices_to_text(decrypted)
            
            # Check if it looks like English
            score = 0
            for pattern in ['THE', 'AND', 'OF', 'TO', 'IN', 'IS']:
                score += text.count(pattern)
            
            if score >= 1:
                print(f"\n  Primer {indices_to_text(primer)}:")
                print(f"    Result: {text}")

def prime_position_shift():
    """Test if shift is based on prime values at each position"""
    print("\n" + "=" * 70)
    print("PRIME POSITION SHIFT TESTING")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    
    # Get sequence of primes
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]
    
    # Shift by prime[i] mod 29
    for offset in range(5):
        shifts = [(primes[i + offset]) % 29 for i in range(len(page_0))]
        decrypted = [(page_0[i] - shifts[i]) % 29 for i in range(len(page_0))]
        text = indices_to_text(decrypted[:60])
        
        score = 0
        for pattern in ['THE', 'AND', 'OF', 'TO', 'IN']:
            score += text.count(pattern)
        
        if score >= 1:
            print(f"\n  Prime offset {offset}: score={score}")
            print(f"    {text}")
    
    # Also try: shift by INDEX_TO_PRIME[plaintext_index] - i.e., shift by the prime value of the cipher rune
    print("\n  Self-referential prime shift (shift by prime value of cipher rune):")
    decrypted = [(c - INDEX_TO_PRIME[c] % 29) % 29 for c in page_0]
    text = indices_to_text(decrypted[:60])
    print(f"    {text}")

def main():
    analyze_key_pattern()
    test_interleave_extraction()
    analyze_autokey()
    prime_position_shift()

if __name__ == '__main__':
    main()

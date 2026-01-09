#!/usr/bin/env python3
"""
Page Difference Attack

Page 54 and Page 0 seem very similar. If they're the same ciphertext with different keys,
their difference might reveal the key difference.

Also looking at Page 56 vs 57 which are confirmed plaintext with identical structure.
"""

import os
import re

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛂ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                   'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
                   'A', 'AE', 'Y', 'IA', 'EA']

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

def read_page_words(page_num):
    """Read page as list of word rune sequences"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    try:
        with open(rune_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    words = re.split(r'[-\n\.\:\,\&\%\$]+', content)
    return [[RUNE_TO_INDEX[r] for r in w if r in RUNE_TO_INDEX] for w in words if any(r in RUNE_TO_INDEX for r in w)]

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

def compare_pages(page_a, page_b):
    """Compare two pages position by position"""
    indices_a = read_page_flat(page_a)
    indices_b = read_page_flat(page_b)
    
    print(f"\n{'='*70}")
    print(f"COMPARING PAGE {page_a} vs PAGE {page_b}")
    print(f"{'='*70}")
    print(f"Page {page_a} length: {len(indices_a)}")
    print(f"Page {page_b} length: {len(indices_b)}")
    
    min_len = min(len(indices_a), len(indices_b))
    
    # Calculate differences
    diffs = []
    matches = 0
    for i in range(min_len):
        diff = (indices_a[i] - indices_b[i]) % 29
        diffs.append(diff)
        if diff == 0:
            matches += 1
    
    print(f"Exact matches: {matches}/{min_len} ({100*matches/min_len:.1f}%)")
    
    # Show difference pattern
    diff_text = indices_to_text(diffs[:100])
    print(f"\nDifference pattern (first 100): {diff_text}")
    
    # Check if difference is a repeating pattern
    for period in [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 29]:
        is_periodic = True
        for i in range(period, min(len(diffs), 100)):
            if diffs[i] != diffs[i % period]:
                is_periodic = False
                break
        if is_periodic:
            pattern = diffs[:period]
            print(f"  PERIODIC with period {period}: {indices_to_text(pattern)}")
            break
    
    return diffs

def analyze_plaintext_pages():
    """Analyze Pages 56 and 57 - confirmed plaintext"""
    print("\n" + "=" * 70)
    print("PLAINTEXT PAGE ANALYSIS (56 vs 57)")
    print("=" * 70)
    
    words_56 = read_page_words(56)
    words_57 = read_page_words(57)
    
    print("\nPage 56 words:")
    for i, w in enumerate(words_56):
        print(f"  {i}: {indices_to_text(w)}")
    
    print("\nPage 57 words:")
    for i, w in enumerate(words_57):
        print(f"  {i}: {indices_to_text(w)}")
    
    # Check if they're identical
    flat_56 = read_page_flat(56)
    flat_57 = read_page_flat(57)
    
    matches = sum(1 for a, b in zip(flat_56, flat_57) if a == b)
    print(f"\nDirect comparison: {matches}/{min(len(flat_56), len(flat_57))} matches")
    
    # Show differences
    diffs = [(a - b) % 29 for a, b in zip(flat_56, flat_57)]
    print(f"Differences: {[d for d in diffs if d != 0][:20]}")

def find_page_0_key():
    """Try to find the key for Page 0 using known patterns"""
    print("\n" + "=" * 70)
    print("PAGE 0 KEY DISCOVERY")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    page_56 = read_page_flat(56)  # Plaintext
    
    # If Page 0 is encrypted Page 56 with some key, then:
    # cipher = plain + key (mod 29)
    # key = cipher - plain (mod 29)
    
    derived_key = [(page_0[i] - page_56[i]) % 29 for i in range(min(len(page_0), len(page_56)))]
    print(f"\nIf Page 0 = Page 56 encrypted:")
    print(f"  Derived key: {indices_to_text(derived_key[:50])}")
    
    # Check for periodicity in key
    for period in range(1, 30):
        is_periodic = True
        for i in range(period, len(derived_key)):
            if derived_key[i] != derived_key[i % period]:
                is_periodic = False
                break
        if is_periodic and period < len(derived_key):
            pattern = derived_key[:period]
            print(f"  KEY IS PERIODIC with period {period}: {indices_to_text(pattern)}")
            return pattern
    
    # If not perfectly periodic, check for near-periodicity
    print("\n  Checking for approximate periodicity...")
    for period in range(1, 30):
        matches = 0
        total = 0
        for i in range(period, len(derived_key)):
            total += 1
            if derived_key[i] == derived_key[i % period]:
                matches += 1
        if total > 0 and matches / total > 0.9:
            print(f"  Period {period}: {100*matches/total:.1f}% match")

def test_shift_patterns():
    """Test various shift patterns on Page 0"""
    print("\n" + "=" * 70)
    print("SHIFT PATTERN TESTING ON PAGE 0")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    page_0_words = read_page_words(0)
    
    # Test: What if each word uses its own shift based on position?
    print("\nTesting position-based shifts per word...")
    
    for base_shift in range(29):
        decrypted_words = []
        for word_idx, word in enumerate(page_0_words[:10]):
            # Try: shift = base_shift + word_position
            shift = (base_shift + word_idx) % 29
            decrypted = [(c - shift) % 29 for c in word]
            decrypted_words.append(indices_to_text(decrypted))
        
        result = ' '.join(decrypted_words)
        if 'THE' in result or 'AND' in result or 'OF' in result:
            print(f"\n  Base shift {base_shift} ({INDEX_TO_LETTER[base_shift]}):")
            print(f"    Words: {decrypted_words}")

def test_fibonacci_shifts():
    """Test Fibonacci-based shift patterns"""
    print("\n" + "=" * 70)
    print("FIBONACCI SHIFT TESTING")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    
    # Generate Fibonacci sequence
    fib = [1, 1]
    while len(fib) < 500:
        fib.append(fib[-1] + fib[-2])
    
    # Test: shift by Fibonacci mod 29
    for offset in range(10):
        shifts = [fib[i + offset] % 29 for i in range(len(page_0))]
        decrypted = [(page_0[i] - shifts[i]) % 29 for i in range(len(page_0))]
        text = indices_to_text(decrypted[:50])
        
        # Check for common words
        score = 0
        for pattern in ['THE', 'AND', 'OF', 'TO', 'IN']:
            if pattern in text:
                score += 1
        
        if score >= 1:
            print(f"\n  Fib offset {offset}: {text}")

def test_totient_shifts():
    """Test Euler's totient function based shifts - 'The primes are sacred'"""
    print("\n" + "=" * 70)
    print("TOTIENT-BASED SHIFT TESTING")
    print("=" * 70)
    
    page_0 = read_page_flat(0)
    
    # Euler's totient for small numbers
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
    
    # Calculate totients
    tots = [totient(i) for i in range(1, 200)]
    
    # Test: shift by totient(position) mod 29
    for offset in range(10):
        shifts = [tots[i + offset] % 29 for i in range(len(page_0))]
        decrypted = [(page_0[i] - shifts[i]) % 29 for i in range(len(page_0))]
        text = indices_to_text(decrypted[:50])
        
        score = 0
        for pattern in ['THE', 'AND', 'OF', 'TO', 'IN']:
            if pattern in text:
                score += 1
        
        if score >= 1:
            print(f"\n  Totient offset {offset}: {text}")

def main():
    # Compare potentially related pages
    compare_pages(0, 54)
    compare_pages(56, 57)
    
    analyze_plaintext_pages()
    find_page_0_key()
    test_shift_patterns()
    test_fibonacci_shifts()
    test_totient_shifts()

if __name__ == '__main__':
    main()

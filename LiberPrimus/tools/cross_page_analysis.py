#!/usr/bin/env python3
"""
Cross-Page Analysis Tool

Analyze relationships between pages, looking for:
1. Similar word structures
2. Pages that might contain hints for other pages
3. Pattern matching based on known plaintext pages
"""

import os
import re
from collections import Counter, defaultdict

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

def runes_to_indices(runes):
    return [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

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

def get_word_signature(word_indices):
    """Create a signature for a word based on its structure"""
    if not word_indices:
        return None
    return len(word_indices)

def analyze_word_patterns():
    """Analyze word length patterns across pages"""
    print("=" * 70)
    print("WORD LENGTH PATTERN ANALYSIS")
    print("=" * 70)
    
    # Page 56 and 57 are known plaintext
    page_57 = read_page_words(57)
    page_57_lengths = [len(w) for w in page_57]
    page_57_text = [indices_to_text(w) for w in page_57]
    
    print("\nPage 57 (PLAINTEXT) Word Structure:")
    print(f"  Lengths: {page_57_lengths}")
    print(f"  Words: {page_57_text}")
    
    # Look for pages with similar structure to plaintext pages
    print("\n\nLooking for pages with matching word length patterns...")
    
    for page_num in range(0, 75):
        words = read_page_words(page_num)
        if not words:
            continue
            
        lengths = [len(w) for w in words[:len(page_57_lengths)]]
        
        # Check similarity
        matches = sum(1 for a, b in zip(lengths, page_57_lengths) if a == b)
        if matches >= 3:
            print(f"\n  Page {page_num}: {matches}/{len(page_57_lengths)} length matches with Page 57")
            print(f"    This page: {lengths}")

def analyze_prime_hints():
    """Look for prime number patterns that might be hints"""
    print("\n" + "=" * 70)
    print("PRIME SUM ANALYSIS")
    print("=" * 70)
    
    for page_num in [0, 2, 3, 4, 56, 57]:
        words = read_page_words(page_num)
        if not words:
            continue
            
        print(f"\nPage {page_num}:")
        
        # Calculate prime sums for first few words
        for i, word in enumerate(words[:10]):
            prime_sum = sum(INDEX_TO_PRIME[idx] for idx in word)
            text = indices_to_text(word)
            print(f"  Word {i}: {text:20s} = prime sum {prime_sum:4d}")
            
            # Check if sum is prime
            if is_prime(prime_sum):
                print(f"           ^ This sum is PRIME!")

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_cross_page_hints():
    """Look for numerical hints that might reference other pages"""
    print("\n" + "=" * 70)
    print("CROSS-PAGE REFERENCE ANALYSIS")
    print("=" * 70)
    
    # From the magic square and other sources, we have key numbers
    key_numbers = {
        1033: "Magic square sum (prime)",
        3301: "Cicada identifier",
        29: "Alphabet size",
        57: "Known plaintext page",
        56: "Known plaintext page",
    }
    
    for page_num in range(0, 10):
        words = read_page_words(page_num)
        if not words:
            continue
            
        total_prime_sum = sum(INDEX_TO_PRIME[idx] for word in words for idx in word)
        print(f"\nPage {page_num}: Total prime sum = {total_prime_sum}")
        
        # Check modular relationships
        for key, desc in key_numbers.items():
            mod_result = total_prime_sum % key
            if mod_result in [0, 1, key-1] or mod_result < 10:
                print(f"  mod {key} ({desc}) = {mod_result}")

def analyze_word_positions():
    """Look for patterns based on word positions"""
    print("\n" + "=" * 70)
    print("WORD POSITION ANALYSIS")
    print("=" * 70)
    
    # Get Page 57 as reference (plaintext)
    page_57_words = read_page_words(57)
    page_57_texts = [indices_to_text(w) for w in page_57_words]
    
    # Known words from Page 57
    known_words = {
        "PARABLE": 0,
        "LICE": 1,  # LIKE with K->C
        "THE": 2,
        "INSTAR": 3,
        # etc
    }
    
    # For Page 0, analyze what shifts would produce "THE" at word 2 position
    page_0_words = read_page_words(0)
    if len(page_0_words) > 2:
        word_2_indices = page_0_words[2]
        print(f"\nPage 0, Word 2: {indices_to_text(word_2_indices)}")
        print("  Testing shifts that would make this 'THE'...")
        
        # THE = [16, 8, 18] in indices
        if len(word_2_indices) == 3:  # Could match THE
            the_indices = [16, 8, 18]
            needed_shifts = [(word_2_indices[i] - the_indices[i]) % 29 for i in range(3)]
            print(f"  Required shifts: {needed_shifts} = {[INDEX_TO_LETTER[s] for s in needed_shifts]}")

def compare_running_key():
    """Test running key cipher using another page as key"""
    print("\n" + "=" * 70)
    print("RUNNING KEY ANALYSIS (Page as Key)")
    print("=" * 70)
    
    # Test if one page decrypts another
    test_combinations = [
        (0, 54),  # Page 54 seems to be almost identical to Page 0
        (0, 56),
        (2, 57),
    ]
    
    for cipher_page, key_page in test_combinations:
        cipher_words = read_page_words(cipher_page)
        key_words = read_page_words(key_page)
        
        if not cipher_words or not key_words:
            continue
            
        # Flatten to indices
        cipher_flat = [idx for word in cipher_words for idx in word]
        key_flat = [idx for word in key_words for idx in word]
        
        # Try subtraction
        decrypted = []
        for i, c in enumerate(cipher_flat[:min(50, len(cipher_flat))]):
            k = key_flat[i % len(key_flat)]
            d = (c - k) % 29
            decrypted.append(d)
        
        result = indices_to_text(decrypted)
        print(f"\nPage {cipher_page} - Page {key_page}: {result[:80]}...")

def main():
    print("=" * 70)
    print("CROSS-PAGE ANALYSIS - Looking for Inter-Page Hints")
    print("=" * 70)
    
    analyze_word_patterns()
    analyze_prime_hints()
    find_cross_page_hints()
    analyze_word_positions()
    compare_running_key()

if __name__ == '__main__':
    main()

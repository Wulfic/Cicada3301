#!/usr/bin/env python3
"""
CREATIVE PATTERN ANALYSIS FOR PAGES 18-54

Looking for hidden patterns:
1. Acrostic patterns (first letter of each word/line)
2. Nth letter patterns
3. Word length patterns  
4. Prime position letters
5. Patterns based on word separators (- vs •)
"""

import os
import re
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(SCRIPT_DIR, "..", "pages")

# Rune to Latin mapping
RUNE_TO_LATIN = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R',
    'ᚳ': 'C', 'ᚷ': 'G', 'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N',
    'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 'ᛉ': 'X',
    'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M',
    'ᛚ': 'L', 'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A',
    'ᚫ': 'AE', 'ᛡ': 'IA', 'ᛣ': 'C', 'ᛠ': 'EA', 'ᚸ': 'G',
    'ᚣ': 'Y'
}

GP_LATIN_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4,
    'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8,
    'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18,
    'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27,
    'EA': 28
}

def load_runes(page_num: int) -> str:
    """Load raw runes from page."""
    runes_file = os.path.join(PAGES_DIR, f"page_{page_num:02d}", "runes.txt")
    if os.path.exists(runes_file):
        with open(runes_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def runes_to_latin(rune_text: str) -> str:
    """Convert runes to Latin letters."""
    result = []
    for char in rune_text:
        if char in RUNE_TO_LATIN:
            result.append(RUNE_TO_LATIN[char])
        elif char in ['-', '•', '.', '\n', ' ', '%', '&', '$', '§']:
            result.append(char)
    return ''.join(result)

def get_words(text: str) -> list[str]:
    """Split text into words using - or • as separators."""
    # Replace all separators with a common delimiter
    text = text.replace('•', '-').replace('\n', '-').replace('.', '-')
    words = [w for w in text.split('-') if w]
    return words

def analyze_acrostic(words: list[str]) -> str:
    """Get first letter of each word."""
    acrostic = ""
    for word in words:
        if word:
            acrostic += word[0]
    return acrostic

def analyze_nth_letters(words: list[str], n: int) -> str:
    """Get nth letter of each word (if word is long enough)."""
    result = ""
    for word in words:
        if len(word) >= n:
            result += word[n-1]
    return result

def analyze_last_letters(words: list[str]) -> str:
    """Get last letter of each word."""
    return "".join(word[-1] if word else "" for word in words)

def analyze_word_lengths(words: list[str]) -> list[int]:
    """Get word lengths pattern."""
    return [len(w) for w in words if w]

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def analyze_prime_positions(text: str) -> str:
    """Get characters at prime positions."""
    # Remove separators for position counting
    clean = ''.join(c for c in text if c.isalpha() or c in ['TH', 'NG', 'EA', 'IO', 'IA', 'OE', 'EO', 'AE'])
    result = ""
    for i, c in enumerate(clean, 1):
        if is_prime(i):
            result += c
    return result

def main():
    print("=" * 80)
    print("CREATIVE PATTERN ANALYSIS FOR PAGES 18-54")
    print("=" * 80)
    
    # Collect patterns across all pages
    all_acrostics = []
    all_word_lengths = []
    
    for page in range(18, 35):  # Focus on first part
        print(f"\n{'='*60}")
        print(f"PAGE {page}")
        print("=" * 60)
        
        runes = load_runes(page)
        if not runes:
            print("  No runes found")
            continue
        
        latin = runes_to_latin(runes)
        words = get_words(latin)
        
        print(f"  Total characters: {len(latin)}")
        print(f"  Total words: {len(words)}")
        
        # Acrostic analysis
        acrostic = analyze_acrostic(words)
        print(f"\n  ACROSTIC (first letters): {acrostic[:60]}...")
        all_acrostics.append(acrostic)
        
        # Last letters
        last = analyze_last_letters(words)
        print(f"  LAST LETTERS: {last[:60]}...")
        
        # 2nd letters
        second = analyze_nth_letters(words, 2)
        print(f"  2ND LETTERS: {second[:40]}...")
        
        # Word lengths
        lengths = analyze_word_lengths(words)
        print(f"  WORD LENGTHS: {lengths[:20]}...")
        all_word_lengths.extend(lengths)
        
        # Prime positions in Latin text
        prime_pos = analyze_prime_positions(latin)
        print(f"  PRIME POSITIONS: {prime_pos[:40]}...")
        
        # Check for repeating patterns in word lengths
        length_str = ''.join(str(l) for l in lengths)
        for pattern_len in range(2, 8):
            pattern = length_str[:pattern_len]
            if length_str.count(pattern) > 3:
                print(f"  ** REPEATING LENGTH PATTERN: '{pattern}' appears {length_str.count(pattern)} times")
    
    # Cross-page analysis
    print(f"\n{'='*80}")
    print("CROSS-PAGE ANALYSIS")
    print("=" * 80)
    
    # Combine all acrostics
    combined_acrostic = "".join(all_acrostics)
    print(f"\nCOMBINED ACROSTIC (first 200): {combined_acrostic[:200]}")
    
    # Word length frequency
    length_freq = Counter(all_word_lengths)
    print(f"\nWORD LENGTH FREQUENCY: {dict(sorted(length_freq.items()))}")
    
    # Check if acrostic contains common words
    common = ['THE', 'AND', 'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY',
              'DIVINE', 'WISDOM', 'TRUTH', 'PRIMES', 'SACRED', 'CICADA']
    for word in common:
        if word in combined_acrostic:
            idx = combined_acrostic.index(word)
            print(f"  ** Found '{word}' in acrostic at position {idx}!")

if __name__ == "__main__":
    main()

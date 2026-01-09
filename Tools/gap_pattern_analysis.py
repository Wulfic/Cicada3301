#!/usr/bin/env python3
"""
Gap Pattern Key Analysis
Based on community research about cyclical gap patterns in keys.

From logs:
"cyclical patterns in gaps between elements of a key that would generate low doubles"
"11 as a gap seems to be a way of generating low doubles"
"pattern is something in the form of 11, -18, 11, 11, -18, 11, X, etc"
"29-18 = 11"

This tool tests keys generated from gap patterns.
"""

import os
import sys
from pathlib import Path
from collections import Counter

# Gematria Primus mappings
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    indices = []
    for char in content:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    
    return indices

def generate_gap_key(start, gaps, length):
    """Generate a key using gap pattern."""
    key = [start]
    gap_idx = 0
    
    while len(key) < length:
        next_val = (key[-1] + gaps[gap_idx % len(gaps)]) % 29
        key.append(next_val)
        gap_idx += 1
    
    return key

def decrypt_sub(ciphertext, key):
    """Decrypt using subtraction."""
    return [(c - key[i % len(key)]) % 29 for i, c in enumerate(ciphertext)]

def indices_to_text(indices):
    """Convert to text."""
    return ''.join(LETTERS[i] for i in indices)

def score_text(text):
    """Score for English likelihood."""
    COMMON = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
              'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS',
              'HIS', 'HIM', 'HOW', 'TWO', 'WAY', 'WHO', 'ITS', 'SAY',
              'SHE', 'TWO', 'HIS', 'THAT', 'WITH', 'HAVE', 'THIS', 'WILL',
              'YOUR', 'FROM', 'THEY', 'BEEN', 'FIND', 'TRUTH', 'WITHIN',
              'THOU', 'THEE', 'THINE', 'HATH', 'UNTO', 'PATH', 'SHED',
              'WISDOM', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE', 'INSTAR'}
    
    score = 0
    for word in COMMON:
        count = text.count(word)
        score += count * len(word) * 10
    
    # Bigram scoring
    good_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'ON', 'EN', 'AT',
                    'ES', 'ED', 'OR', 'TE', 'OF', 'IT', 'IS', 'AL', 'NT', 'AR']
    for bg in good_bigrams:
        score += text.count(bg) * 2
    
    return score

def test_gap_patterns(page_num):
    """Test various gap patterns on a page."""
    print(f"\n{'='*70}")
    print(f"GAP PATTERN ANALYSIS: Page {page_num}")
    print(f"{'='*70}")
    
    ciphertext = load_runes(page_num)
    if not ciphertext:
        print(f"Could not load page {page_num}")
        return
    
    print(f"Ciphertext length: {len(ciphertext)}")
    
    # Community-mentioned gap patterns
    gap_patterns = [
        [11],                    # Simple gap of 11
        [11, -18],              # Alternating +11, -18 (where -18 mod 29 = 11)
        [11, 11, -18],          # 11, 11, -18
        [-18, 11],              # Reverse
        [11, -18, 11, 11, -18], # Longer pattern
        [11, 11, 11, -18],      # Three 11s then -18
        # Also try some prime-based gaps
        [7],
        [13],
        [17],
        [23],
        # Fibonacci-like
        [1, 1, 2, 3, 5, 8, 13],
        # Prime sequence differences
        [1, 2, 2, 4, 2, 4, 2, 4, 6],
    ]
    
    best_score = 0
    best_result = None
    
    for gaps in gap_patterns:
        print(f"\nGap pattern: {gaps}")
        
        # Try different starting values
        for start in range(29):
            key = generate_gap_key(start, gaps, len(ciphertext))
            decrypted = decrypt_sub(ciphertext, key)
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > best_score:
                best_score = score
                best_result = (gaps, start, text, key[:20])
                print(f"  New best (start={start}): score={score}")
                print(f"    Key prefix: {key[:15]}")
                print(f"    Text: {text[:80]}")
    
    print(f"\n{'='*50}")
    print(f"BEST RESULT:")
    if best_result:
        gaps, start, text, key_prefix = best_result
        print(f"Gap pattern: {gaps}")
        print(f"Start: {start}")
        print(f"Score: {best_score}")
        print(f"Key prefix: {key_prefix}")
        print(f"Text (first 200): {text[:200]}")
    
    return best_result

def analyze_discovered_key_gaps():
    """Analyze gaps in keys from discovered words."""
    print("\n" + "="*70)
    print("ANALYZING GAPS IN DISCOVERED KEYS")
    print("="*70)
    
    # From Discovery 25 - keys at specific positions
    # Page 8: word 10 (THE) at position 42-43, keys [10, 7]
    # Page 46: word 18 (AN) at positions 63-64, keys [18, 18]
    # Page 46: word 19 (I) at position 65, key [12]
    
    # The key for "AN" is [18, 18] - same value!
    # The key for consecutive positions 63,64,65 is [18, 18, 12]
    
    # Gaps: 18-18=0, 12-18=-6 (or +23 mod 29)
    
    print("\nPage 8, THE at positions 42-43:")
    print("  Keys: [10, 7]")
    print("  Gap: 7-10 = -3 (or +26 mod 29)")
    
    print("\nPage 46, AN+I at positions 63-65:")
    print("  Keys: [18, 18, 12]")
    print("  Gaps: 0, -6")
    
    # Check if gap of 11 appears
    print("\n11-based gap analysis:")
    print("  Gap of 11 would produce: 0, 11, 22, 4, 15, 26, 8, 19, 1, 12...")
    
    # Generate and check
    gap11_key = generate_gap_key(0, [11], 30)
    print(f"  Gap-11 sequence: {gap11_key}")
    
    # Check if our discovered keys fit this pattern
    print("\n  Does [10, 7] fit gap-11? ")
    print(f"    10 + 11 mod 29 = {(10+11)%29}, need 7 -> NO")
    print(f"    10 - 11 mod 29 = {(10-11)%29}, need 7 -> NO")
    
    print("\n  Does [18, 18, 12] fit gap-11?")
    print(f"    18 + 11 mod 29 = {(18+11)%29}, need 18 -> NO")
    
    # Maybe the gap pattern is per-word, not per-rune?
    print("\n\nPerhaps gaps are between WORDS, not runes...")

def main():
    print("=" * 70)
    print("GAP PATTERN KEY ANALYSIS")
    print("=" * 70)
    
    # Test gap patterns on our best pages
    for page in [8, 46, 43, 13]:
        test_gap_patterns(page)
    
    # Analyze our discovered keys
    analyze_discovered_key_gaps()

if __name__ == "__main__":
    main()

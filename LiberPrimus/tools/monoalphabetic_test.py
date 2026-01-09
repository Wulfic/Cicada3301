#!/usr/bin/env python3
"""
Apply Page 59's Monoalphabetic Cipher to Unsolved Pages
========================================================
Page 59 was solved using a monoalphabetic substitution cipher.
What if the same cipher applies to pages 18-54?
"""

import os
from collections import Counter

# Gematria Primus mapping
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# Page 59's cipher mapping (Rune/Runeglish -> English)
# From SOLUTION.md:
PAGE_59_CIPHER = {
    'R': 'A',   # ᚱ -> A
    'NG': 'W',  # ᛝ -> W
    'A': 'R',   # ᚪ -> R
    'M': 'N',   # ᛗ -> N
    'J': 'B',   # ᛄ -> B
    'I': 'E',   # ᛁ -> E
    'H': 'L',   # ᚻ -> L
    'E': 'I',   # ᛖ -> I
    'IA': 'V',  # ᛡ -> V
    'AE': 'O',  # ᚫ -> O
    'D': 'K',   # ᛞ -> K
    'OE': 'G',  # ᛟ -> G
    'C': 'D',   # ᚳ -> D
    'EO': 'T',  # ᛇ -> T
    'N': 'M',   # ᚾ -> M
    'P': 'S',   # ᛈ -> S
    'S': 'P',   # ᛋ -> P
    'X': 'X',   # ᛉ -> X
    'EA': 'F',  # ᛠ -> F
    'Y': 'TH',  # ᚣ -> TH
    'TH': 'Y',  # ᚦ -> Y
}

# Map rune index to runeglish for standard GP
INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

def read_runes(filepath):
    """Read runes from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [c for c in content if c in GP_RUNE_TO_INDEX]

def apply_page59_cipher(runes):
    """Apply Page 59's monoalphabetic cipher to runes."""
    result = []
    for rune in runes:
        idx = GP_RUNE_TO_INDEX[rune]
        runeglish = INDEX_TO_RUNEGLISH[idx]
        
        # Apply the cipher mapping
        if runeglish in PAGE_59_CIPHER:
            result.append(PAGE_59_CIPHER[runeglish])
        else:
            # For unmapped runes, keep as-is
            result.append(runeglish)
    
    return ''.join(result)

def analyze_frequencies(text):
    """Analyze letter frequencies."""
    counter = Counter(text.replace(' ', ''))
    total = sum(counter.values())
    print("\nTop 10 letter frequencies:")
    for char, count in counter.most_common(10):
        print(f"  {char}: {count/total*100:.1f}%")

def test_cipher_on_page(page_num):
    """Test Page 59's cipher on a specific page."""
    rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    
    if not os.path.exists(rune_path):
        return None
    
    runes = read_runes(rune_path)
    if not runes:
        return None
    
    # Apply Page 59's cipher
    result = apply_page59_cipher(runes)
    
    return result

# Test on pages 18-30
print("="*70)
print("APPLYING PAGE 59's MONOALPHABETIC CIPHER TO UNSOLVED PAGES")
print("="*70)

for page in [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
    result = test_cipher_on_page(page)
    if result:
        # Check for English words
        words_found = []
        for word in ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT', 'IT', 'FOR', 
                     'AS', 'WITH', 'BE', 'WAS', 'ARE', 'THIS', 'TRUTH', 'BELIEVE']:
            if word in result:
                words_found.append(word)
        
        print(f"\nPage {page:02d} ({len(result)} chars):")
        print(f"  Preview: {result[:80]}")
        print(f"  Words found: {words_found}")

# Now let's try a different approach: what if we need to FIND the right monoalphabetic cipher?
# The IoC is ~0.034 which suggests the plaintext is NOT normal English
# But what if it's encoded runeglish or a specific vocabulary?

print("\n" + "="*70)
print("FREQUENCY ANALYSIS OF UNSOLVED PAGES")
print("="*70)

# Combine all unsolved pages for frequency analysis
all_runes = []
for page in range(18, 55):
    rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page:02d}/runes.txt"
    if os.path.exists(rune_path):
        runes = read_runes(rune_path)
        all_runes.extend(runes)

print(f"Total runes in pages 18-54: {len(all_runes)}")

# Frequency analysis
rune_counter = Counter(all_runes)
print("\nRune frequency distribution:")
for rune, count in rune_counter.most_common():
    idx = GP_RUNE_TO_INDEX[rune]
    runeglish = INDEX_TO_RUNEGLISH[idx]
    pct = count / len(all_runes) * 100
    print(f"  {rune} ({runeglish:3}): {count:5} ({pct:.2f}%)")

# Compare with expected English frequencies (mapped to 29-char alphabet)
# In English: E(12.7%), T(9.1%), A(8.2%), O(7.5%), I(7.0%), N(6.7%), S(6.3%), H(6.1%), R(6.0%)
print("\n" + "="*70)
print("EXPECTED ENGLISH FREQUENCY IN RUNEGLISH")
print("="*70)
print("If pages 18-54 are monoalphabetic cipher on English:")
print("  Most common should map to: E, T, A, O, I, N, S, H, R")
print("\nMost common runes in pages 18-54:")
for i, (rune, count) in enumerate(rune_counter.most_common(10)):
    idx = GP_RUNE_TO_INDEX[rune]
    runeglish = INDEX_TO_RUNEGLISH[idx]
    pct = count / len(all_runes) * 100
    # What English letter would this represent?
    expected = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'L'][i] if i < 10 else '?'
    print(f"  {rune} ({runeglish:3}) -> might be '{expected}' | {pct:.2f}%")

# Try deriving a monoalphabetic cipher from frequency analysis
print("\n" + "="*70)
print("TESTING FREQUENCY-DERIVED MONOALPHABETIC CIPHER")
print("="*70)

english_freq_order = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'L', 'D', 'C', 'U', 
                      'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']

# Build cipher from frequency analysis
freq_cipher = {}
for i, (rune, count) in enumerate(rune_counter.most_common()):
    idx = GP_RUNE_TO_INDEX[rune]
    runeglish = INDEX_TO_RUNEGLISH[idx]
    if i < len(english_freq_order):
        freq_cipher[idx] = english_freq_order[i]
    else:
        freq_cipher[idx] = '?'

# Apply frequency cipher to page 18
rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_18/runes.txt"
runes = read_runes(rune_path)
freq_result = ''.join(freq_cipher[GP_RUNE_TO_INDEX[r]] for r in runes)

print(f"\nPage 18 with frequency-derived cipher:")
print(f"  {freq_result[:100]}")
print(f"  {freq_result[100:200]}")

# Check for common words
words_found = []
for word in ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT', 'IT', 'FOR', 'AS', 'WITH']:
    count = freq_result.count(word)
    if count > 0:
        words_found.append((word, count))

print(f"  Words found: {words_found}")

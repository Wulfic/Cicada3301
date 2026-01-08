#!/usr/bin/env python3
"""
Comprehensive Rune Decoder - Properly handles Unicode runes
"""

import os
import re
from collections import defaultdict

# Complete mapping of Unicode runes to Gematria Primus indices and letters
RUNE_TO_INDEX = {
    'ᚠ': 0,   # F (fehu)
    'ᚢ': 1,   # U (uruz)
    'ᚦ': 2,   # TH (thurisaz)
    'ᚩ': 3,   # O (ansuz - variant)
    'ᚱ': 4,   # R (raido)
    'ᚳ': 5,   # C/K (cen)
    'ᚷ': 6,   # G (gebo)
    'ᚹ': 7,   # W (wynn)
    'ᚻ': 8,   # H (hagalaz - variant)
    'ᚾ': 9,   # N (naudiz)
    'ᛁ': 10,  # I (isaz)
    'ᛄ': 11,  # J (jera)
    'ᛇ': 12,  # EO (eihwaz - variant)
    'ᛈ': 13,  # P (perthro)
    'ᛉ': 14,  # X (algiz)
    'ᛋ': 15,  # S (sowilo)
    'ᛏ': 16,  # T (tiwaz)
    'ᛒ': 17,  # B (berkano)
    'ᛖ': 18,  # E (ehwaz)
    'ᛗ': 19,  # M (mannaz)
    'ᛚ': 20,  # L (laguz)
    'ᛝ': 21,  # NG (ingwaz)
    'ᛟ': 22,  # OE (othala)
    'ᛞ': 23,  # D (dagaz)
    'ᚪ': 24,  # A (ac)
    'ᚫ': 25,  # AE (aesc)
    'ᚣ': 26,  # Y (yr)
    'ᛡ': 27,  # IA/IO (ior)
    'ᛠ': 28,  # EA (ear)
}

# Primes for each position
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Letters for display
INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Letter to index mapping for English text processing
LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6,
    'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20,
    'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26,
    'IA': 27, 'IO': 27, 'EA': 28, 'V': 1, 'Q': 5, 'Z': 15
}

def runes_to_indices(runes):
    """Convert a string of Unicode runes to indices"""
    return [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]

def indices_to_letters(indices):
    """Convert indices to displayable letter string"""
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

def text_to_indices(text):
    """Convert English text to Gematria Primus indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        # Single letter
        if text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
        i += 1
    return indices

def read_rune_words(page_num):
    """Read rune file and return list of words (hyphen-separated groups)"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Split by hyphens and newlines to get words
    words = re.split(r'[-\n]+', content)
    words = [w.strip() for w in words if w.strip()]
    return words

def decrypt_word(rune_word, key_indices, position_offset=0, operation='sub'):
    """
    Decrypt a rune word
    - operation: 'sub' = (cipher - key), 'add' = (cipher + key)
    """
    rune_indices = runes_to_indices(rune_word)
    if not rune_indices:
        return rune_word, []
    
    decrypted = []
    for i, idx in enumerate(rune_indices):
        if key_indices:
            key_idx = key_indices[(position_offset + i) % len(key_indices)]
        else:
            key_idx = 0
        
        if operation == 'sub':
            new_idx = (idx - key_idx) % 29
        else:
            new_idx = (idx + key_idx) % 29
        decrypted.append(new_idx)
    
    return indices_to_letters(decrypted), decrypted

def test_word_boundary_decryption(page_num, key_word, operation='sub'):
    """
    Test decryption with word boundaries preserved
    Key resets at each word boundary
    """
    words = read_rune_words(page_num)
    key_indices = text_to_indices(key_word)
    
    print(f"\n=== Page {page_num} | Key: {key_word} ({operation}) | Word Boundary Mode ===")
    print(f"Key indices: {key_indices}")
    print(f"Total words: {len(words)}\n")
    
    all_decrypted = []
    for i, rune_word in enumerate(words[:25]):
        # Key resets for each word
        text, indices = decrypt_word(rune_word, key_indices, position_offset=0, operation=operation)
        all_decrypted.append(text)
        
        # Show rune count
        rune_count = len(runes_to_indices(rune_word))
        print(f"  {i:2d}. ({rune_count} runes) {text}")
    
    return all_decrypted

def test_continuous_key(page_num, key_word, operation='sub'):
    """
    Test decryption with continuous key (doesn't reset at word boundaries)
    """
    words = read_rune_words(page_num)
    key_indices = text_to_indices(key_word)
    
    print(f"\n=== Page {page_num} | Key: {key_word} ({operation}) | Continuous Mode ===")
    print(f"Key indices: {key_indices}")
    
    all_decrypted = []
    position = 0
    for i, rune_word in enumerate(words[:25]):
        text, indices = decrypt_word(rune_word, key_indices, position_offset=position, operation=operation)
        all_decrypted.append(text)
        position += len(runes_to_indices(rune_word))
        
        rune_count = len(runes_to_indices(rune_word))
        print(f"  {i:2d}. ({rune_count} runes) {text}")
    
    return all_decrypted

def analyze_word_lengths(page_num):
    """Analyze the word lengths to see if they match expected English patterns"""
    words = read_rune_words(page_num)
    
    print(f"\n=== Page {page_num} Word Length Analysis ===")
    
    lengths = []
    for word in words:
        rune_count = len(runes_to_indices(word))
        lengths.append(rune_count)
    
    print(f"Total words: {len(lengths)}")
    print(f"Word lengths: {lengths[:30]}...")
    
    # English word length statistics
    print(f"\nLength distribution:")
    from collections import Counter
    dist = Counter(lengths)
    for length in sorted(dist.keys()):
        print(f"  {length} runes: {dist[length]} words")
    
    # Common patterns
    short_words = [i for i, l in enumerate(lengths) if l <= 2]
    print(f"\nShort words (1-2 runes): {len(short_words)} words at positions {short_words[:15]}...")

def main():
    print("=" * 70)
    print("COMPREHENSIVE RUNE DECODER - Proper Unicode Handling")
    print("=" * 70)
    
    # Analyze word lengths
    analyze_word_lengths(0)
    analyze_word_lengths(2)
    
    # Test various keys with word boundary mode
    keys = ['DIVINITY', 'PILGRIM', 'WISDOM', 'SACRED', 'IP', 'PI']
    
    for key in keys:
        test_word_boundary_decryption(2, key, 'sub')
    
    # Also test continuous mode for comparison
    print("\n" + "=" * 70)
    print("CONTINUOUS MODE (key doesn't reset at word boundaries)")
    print("=" * 70)
    
    test_continuous_key(2, 'DIVINITY', 'sub')

if __name__ == '__main__':
    main()

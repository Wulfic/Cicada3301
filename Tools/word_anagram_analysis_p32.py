"""
Word-Level Anagram Analysis - Page 32
Extract words and test rearrangement possibilities
"""

import os
import re
import itertools
from collections import Counter

# Gematria Primus mappings
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21,
    'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_INDEX_TO_LATIN = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N',
    'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
    'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

GP_LATIN_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5,
    'G': 6, 'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11,
    'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17,
    'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23,
    'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

# Common English words for validation
COMMON_WORDS = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
    'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM',
    'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN', 'HIM',
    'HIS', 'HOW', 'WHO', 'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'HER', 'TWO',
    'WAY', 'WHO', 'OIL', 'ITS', 'LET', 'PUT', 'END', 'WHY', 'TRY', 'ASK',
    'KNOW', 'TAKE', 'MAKE', 'COME', 'FIND', 'SEEK', 'PATH', 'TRUTH', 'WISDOM',
    'PRIMES', 'SACRED', 'ENCRYPT', 'JOURNEY', 'PILGRIMAGE', 'ANCIENT'
}

def load_page_runes(page_num):
    """Load runes from page"""
    page_dir = f"LiberPrimus/pages/page_{page_num:02d}"
    rune_file = os.path.join(page_dir, "runes.txt")
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    return text

def runes_to_indices(runes_text):
    """Convert runes to indices"""
    indices = []
    for char in runes_text:
        if char in GP_RUNE_TO_INDEX:
            indices.append(GP_RUNE_TO_INDEX[char])
    return indices

def indices_to_text(indices):
    """Convert indices to text"""
    result = []
    i = 0
    while i < len(indices):
        # Try two-character combinations
        if i < len(indices) - 1:
            two_char = GP_INDEX_TO_LATIN[indices[i]] + GP_INDEX_TO_LATIN[indices[i+1]]
            if two_char in ['TH', 'EO', 'NG', 'OE', 'IA', 'EA', 'AE']:
                # Check if this is actually a two-char rune
                result.append(two_char)
                i += 2
                continue
        
        result.append(GP_INDEX_TO_LATIN[indices[i]])
        i += 1
    
    return ''.join(result)

def caesar_decrypt(cipher, shift):
    """Caesar shift"""
    return [(c - shift) % 29 for c in cipher]

def extract_words(text, min_length=2):
    """Extract words separated by hyphens or breaks"""
    # Handle two-letter combos as single units
    words = []
    current_word = []
    i = 0
    
    while i < len(text):
        # Check for two-letter combinations
        if i < len(text) - 1:
            two_char = text[i:i+2]
            if two_char in ['TH', 'EO', 'NG', 'OE', 'IA', 'EA', 'AE']:
                current_word.append(two_char)
                i += 2
                continue
        
        current_word.append(text[i])
        i += 1
    
    # Re-join words by breaking on likely boundaries
    result = []
    current = ''
    for unit in current_word:
        current += unit
        # Heuristic: word break after common word endings or when word gets long
        if len(current) > 3 and current.endswith(('E', 'D', 'T', 'NG', 'S')):
            if len(current) >= min_length:
                result.append(current)
            current = ''
    
    if current and len(current) >= min_length:
        result.append(current)
    
    return result

def score_english_words(words):
    """Score based on known English words"""
    score = 0
    known_count = 0
    
    for word in words:
        word_upper = word.upper()
        # Remove combining elements for matching
        clean_word = word_upper.replace('TH', 'T').replace('EO', 'E').replace('NG', 'N').replace('OE', 'O').replace('IA', 'A').replace('EA', 'A').replace('AE', 'A')
        
        if word_upper in COMMON_WORDS:
            score += 10
            known_count += 1
        elif len(word) >= 4 and clean_word in COMMON_WORDS:
            score += 8
            known_count += 1
        elif word_upper.startswith('THE') or word_upper.startswith('AND') or word_upper.startswith('FOR'):
            score += 5
        else:
            score += 1
    
    return score, known_count

def analyze_patterns(text):
    """Look for patterns in scrambled text"""
    print("\n=== PATTERN ANALYSIS ===\n")
    
    # Find most common sequences
    trigrams = Counter()
    for i in range(len(text) - 2):
        trigrams[text[i:i+3]] += 1
    
    print("Top 20 Most Common 3-Char Sequences:")
    for seq, count in trigrams.most_common(20):
        print(f"  '{seq}': {count} times")
    
    # Look for likely word boundaries
    print("\nLikely Word Patterns (starting with common English):")
    
    patterns_found = []
    for i in range(len(text) - 2):
        if text[i:i+3] in ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT']:
            # Found a known pattern
            # Try to extract word around it
            start = max(0, i - 3)
            end = min(len(text), i + 6)
            context = text[start:end]
            patterns_found.append((text[i:i+3], context, i))
    
    for pattern, context, pos in patterns_found[:15]:
        print(f"  '{pattern}' at pos {pos}: context '{context}'")

def main():
    print("=" * 80)
    print("WORD-LEVEL ANAGRAM ANALYSIS - PAGE 32")
    print("=" * 80)
    print()
    
    # Load and decrypt Page 32
    runes = load_page_runes(32)
    indices = runes_to_indices(runes)
    
    print(f"Page 32: {len(indices)} runes")
    print()
    
    # Caesar 11 decryption
    caesar_11 = caesar_decrypt(indices, 11)
    text = indices_to_text(caesar_11)
    
    print(f"After Caesar 11 shift:")
    print(f"Text length: {len(text)}")
    print(f"First 200 chars: {text[:200]}")
    print()
    
    # Analyze patterns
    analyze_patterns(text)
    print()
    
    # Try different word extraction strategies
    print("\n=== WORD EXTRACTION STRATEGIES ===\n")
    
    # Strategy 1: Simple chunking
    print("Strategy 1: Fixed-size chunks")
    chunks_2 = [text[i:i+2] for i in range(0, len(text), 2)]
    chunks_3 = [text[i:i+3] for i in range(0, len(text), 3)]
    chunks_4 = [text[i:i+4] for i in range(0, len(text), 4)]
    
    score_2, known_2 = score_english_words(chunks_2)
    score_3, known_3 = score_english_words(chunks_3)
    score_4, known_4 = score_english_words(chunks_4)
    
    print(f"  2-char chunks: Score {score_2}, Known words {known_2}")
    print(f"  3-char chunks: Score {score_3}, Known words {known_3}")
    print(f"  4-char chunks: Score {score_4}, Known words {known_4}")
    
    # Strategy 2: Reverse entire text
    print("\nStrategy 2: Reversed text")
    text_rev = text[::-1]
    print(f"First 200 chars reversed: {text_rev[:200]}")
    analyze_patterns(text_rev)
    
    # Strategy 3: Every Nth character
    print("\nStrategy 3: Extracting every Nth character")
    for n in [2, 3, 5, 7]:
        extracted = text[::n]
        print(f"  Every {n}th char: {extracted[:80]}")
    
    # Strategy 4: Look for word-like sequences in original
    print("\nStrategy 4: Checking if word boundaries are encoded in runes")
    rune_text = runes
    hyphen_positions = [i for i, c in enumerate(rune_text) if c == '-']
    print(f"  Hyphens found at positions: {hyphen_positions[:20]}")
    print(f"  Total hyphens: {len(hyphen_positions)}")
    
    if hyphen_positions:
        print(f"  Average spacing between hyphens: {sum(hyphen_positions[i+1] - hyphen_positions[i] for i in range(len(hyphen_positions)-1)) / (len(hyphen_positions)-1):.1f}")

if __name__ == "__main__":
    main()

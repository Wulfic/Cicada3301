#!/usr/bin/env python3
"""
Page 20: Analyze NON-PRIME valued runes more deeply

The non-prime valued stream has IoC = 1.4426, which is higher than random.
Let's search for English words and patterns.
"""

import os
from collections import Counter
import re

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X',
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

PRIME_VALUES = {2, 3, 5, 7, 11, 13, 17, 19, 23}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    indices = []
    for c in content:
        if c in RUNE_MAP:
            indices.append(RUNE_MAP[c])
    return indices

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

# English word list
ENGLISH_WORDS = set([
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I', 'IT', 'FOR', 'NOT',
    'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT', 'THIS', 'BUT', 'HIS', 'BY', 'FROM',
    'THEY', 'WE', 'SAY', 'HER', 'SHE', 'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD',
    'THERE', 'THEIR', 'WHAT', 'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH',
    'GO', 'ME', 'WHEN', 'MAKE', 'CAN', 'LIKE', 'TIME', 'NO', 'JUST', 'HIM', 'KNOW',
    'TAKE', 'PEOPLE', 'INTO', 'YEAR', 'YOUR', 'GOOD', 'SOME', 'COULD', 'THEM', 'SEE',
    'OTHER', 'THAN', 'THEN', 'NOW', 'LOOK', 'ONLY', 'COME', 'ITS', 'OVER', 'THINK',
    'ALSO', 'BACK', 'AFTER', 'USE', 'TWO', 'HOW', 'OUR', 'WORK', 'FIRST', 'WELL',
    'WAY', 'EVEN', 'NEW', 'WANT', 'BECAUSE', 'ANY', 'THESE', 'GIVE', 'DAY', 'MOST',
    'US', 'IS', 'AM', 'ARE', 'WAS', 'WERE', 'BEEN', 'BEING', 'EACH', 'FEW', 'THOSE',
    'MUST', 'SELF', 'OWN', 'SAME', 'TELL', 'NEED', 'FEEL', 'HIGH', 'OLD', 'GREAT',
    'NAME', 'THING', 'MAN', 'WORLD', 'LIFE', 'HAND', 'PART', 'CHILD', 'EYE', 'WOMAN',
    'PLACE', 'CASE', 'WEEK', 'POINT', 'WORD', 'FIND', 'LONG', 'LITTLE', 'STILL',
    'MIGHT', 'FACE', 'LAST', 'SIDE', 'DOOR', 'HOME', 'NIGHT', 'REAL', 'HEAD', 'TEAM',
    'BEST', 'HOUR', 'LINE', 'LEFT', 'ALONE', 'LONE', 'PATH', 'TRUTH', 'LIGHT', 'DARK',
    'SOUL', 'MIND', 'BODY', 'HEART', 'DEATH', 'DEAD', 'LIVE', 'LEARN', 'TEACH', 'SHOW',
    'WALK', 'RUN', 'STAND', 'SIT', 'FALL', 'RISE', 'TURN', 'MOVE', 'WATCH', 'WAIT',
    'SPEAK', 'HEAR', 'READ', 'WRITE', 'CALL', 'LEAD', 'HOLD', 'KEEP', 'BEGIN', 'START',
    # Old English
    'EODE', 'SEFA', 'DEOR', 'WEAN', 'EORL', 'WYRD', 'FRITH',
    # Cicada words
    'DIVINITY', 'PRIMES', 'SACRED', 'TOTIENT', 'PILGRIM', 'KOAN', 'WISDOM',
])

def find_english_words(text):
    """Find all English words in the text."""
    found = []
    for word in ENGLISH_WORDS:
        if len(word) >= 3:
            idx = 0
            while True:
                idx = text.find(word, idx)
                if idx == -1:
                    break
                found.append((idx, word))
                idx += 1
    return sorted(found)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    # Extract non-prime valued runes
    non_prime_valued = [(i, c) for i, c in enumerate(cipher) if c not in PRIME_VALUES]
    non_prime_stream = [c for _, c in non_prime_valued]
    non_prime_positions = [i for i, _ in non_prime_valued]
    
    latin = indices_to_latin(non_prime_stream)
    print(f"Non-prime valued stream ({len(latin)} chars):")
    print(latin)
    print()
    
    # Find English words
    found_words = find_english_words(latin)
    print(f"\n=== ENGLISH WORDS FOUND ({len(found_words)} occurrences) ===")
    for pos, word in found_words:
        context_start = max(0, pos - 5)
        context_end = min(len(latin), pos + len(word) + 5)
        context = latin[context_start:context_end]
        marker = '...' if context_start > 0 else ''
        marker2 = '...' if context_end < len(latin) else ''
        print(f"  Position {pos}: '{word}' in '{marker}{context}{marker2}'")
    
    # Word frequency in found words
    word_counts = Counter(word for _, word in found_words)
    print(f"\n=== WORD FREQUENCY ===")
    for word, count in word_counts.most_common(20):
        print(f"  {word}: {count} times")
    
    # Check if there's a pattern in positions
    print(f"\n=== POSITION PATTERN ANALYSIS ===")
    print(f"First 20 original positions: {non_prime_positions[:20]}")
    
    # Calculate gaps between positions
    gaps = [non_prime_positions[i+1] - non_prime_positions[i] for i in range(len(non_prime_positions)-1)]
    gap_counts = Counter(gaps)
    print(f"Gap distribution (gap -> count):")
    for gap in sorted(gap_counts.keys()):
        print(f"  Gap {gap}: {gap_counts[gap]} times")
    
    # Try simple shift decryption on the non-prime stream
    print(f"\n=== CAESAR SHIFT TEST ===")
    for shift in range(29):
        shifted = [(c - shift) % 29 for c in non_prime_stream]
        shifted_latin = indices_to_latin(shifted)
        found = find_english_words(shifted_latin)
        if len(found) > len(found_words):  # More words than raw
            print(f"Shift {shift}: {len(found)} words - {shifted_latin[:50]}")
    
    # Look for repeating patterns that might indicate key
    print(f"\n=== TRIGRAM ANALYSIS ===")
    trigrams = Counter()
    for i in range(len(latin) - 2):
        trigrams[latin[i:i+3]] += 1
    
    print("Most common trigrams:")
    for tri, count in trigrams.most_common(15):
        is_word = tri in ENGLISH_WORDS
        print(f"  '{tri}': {count} times {'(WORD!)' if is_word else ''}")

if __name__ == '__main__':
    main()

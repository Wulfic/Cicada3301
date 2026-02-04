#!/usr/bin/env python3
"""
Page 20: Apply shift 2 to non-prime valued runes and analyze

Shift 2 gave the most English words (12).
"""

import os
from collections import Counter

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
    'LONE', 'PATH', 'TRUTH', 'LIGHT', 'DARK', 'SOUL', 'MIND', 'BODY', 'HEART', 'DEATH',
    'DEAD', 'LIVE', 'LEARN', 'TEACH', 'SHOW', 'WALK', 'RUN', 'FALL', 'RISE',
    'EODE', 'SEFA', 'DEOR', 'WEAN', 'EORL', 'WYRD', 'FRITH',
])

def find_english_words(text):
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
    
    # Apply shift 2 (subtract 2 mod 29)
    shifted = [(c - 2) % 29 for c in non_prime_stream]
    latin = indices_to_latin(shifted)
    
    print("=== NON-PRIME STREAM WITH SHIFT -2 ===")
    print(f"Length: {len(latin)} chars")
    print()
    print(latin)
    print()
    
    # Find English words
    found_words = find_english_words(latin)
    print(f"\n=== ENGLISH WORDS FOUND ({len(found_words)}) ===")
    for pos, word in found_words:
        context_start = max(0, pos - 10)
        context_end = min(len(latin), pos + len(word) + 10)
        context = latin[context_start:context_end]
        marker = '>>>' if word in ['THE', 'AND', 'THEY', 'EODE', 'SEFA', 'DEOR'] else ''
        print(f"  {marker} Position {pos}: '{word}' in '...{context}...'")
    
    # Also check the PRIME stream with various shifts
    print("\n\n=== NOW CHECK PRIME-VALUED STREAM ===")
    prime_valued = [(i, c) for i, c in enumerate(cipher) if c in PRIME_VALUES]
    prime_stream = [c for _, c in prime_valued]
    
    # The prime stream only has 9 unique values: 2,3,5,7,11,13,17,19,23
    # These map to: TH, O, C, W, J, P, B, M, D
    print(f"Prime stream length: {len(prime_stream)}")
    print(f"Unique values: {sorted(set(prime_stream))}")
    print(f"Letters: {[LATIN_TABLE[v] for v in sorted(set(prime_stream))]}")
    
    prime_latin = indices_to_latin(prime_stream)
    print(f"\nPrime stream raw: {prime_latin[:100]}")
    
    # Since prime values are limited, maybe they form a simpler pattern
    # Check letter frequency
    freq = Counter(prime_latin)
    print(f"\nPrime stream letter frequency:")
    for letter, count in freq.most_common():
        print(f"  {letter}: {count} ({100*count/len(prime_stream):.1f}%)")
    
    # What if prime stream is a repeating key?
    # Check for period using autocorrelation
    print(f"\n=== Prime stream as potential KEY ===")
    # Check if first N indices repeat
    for period in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53]:
        matches = sum(1 for i in range(len(prime_stream) - period) if prime_stream[i] == prime_stream[i + period])
        total = len(prime_stream) - period
        ratio = matches / total if total > 0 else 0
        if ratio > 0.15:  # Higher than random (1/9 = 11%)
            print(f"  Period {period}: {matches}/{total} matches ({100*ratio:.1f}%)")

if __name__ == '__main__':
    main()

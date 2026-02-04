#!/usr/bin/env python3
"""
Find English words hidden in Page 20's raw Gematria output.

Looking for words that appear in plaintext without decryption.
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

# Common English words (including Old English)
ENGLISH_WORDS = {
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I',
    'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT',
    'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE',
    'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR',
    'WHAT', 'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH', 'GO',
    'ME', 'WHEN', 'MAKE', 'CAN', 'LIKE', 'TIME', 'NO', 'JUST', 'HIM', 'KNOW',
    'TAKE', 'PEOPLE', 'INTO', 'YEAR', 'YOUR', 'GOOD', 'SOME', 'COULD', 'THEM',
    'SEE', 'OTHER', 'THAN', 'THEN', 'NOW', 'LOOK', 'ONLY', 'COME', 'ITS', 'OVER',
    'THINK', 'ALSO', 'BACK', 'AFTER', 'USE', 'TWO', 'HOW', 'OUR', 'WORK',
    'FIRST', 'WELL', 'WAY', 'EVEN', 'NEW', 'WANT', 'BECAUSE', 'ANY', 'THESE',
    'GIVE', 'DAY', 'MOST', 'US', 'IS', 'AM', 'ARE', 'WAS', 'WERE', 'BEEN',
    # Old English words from Deor
    'EODE', 'SEFA', 'DEOR', 'MÆTH', 'WEAN', 'SITHE', 'EORL', 'OFEREODE',
    # Cicada-specific
    'DIVINITY', 'PRIMES', 'PRIME', 'SACRED', 'TOTIENT', 'PATH', 'PILGRIM',
    'KOAN', 'WISDOM', 'CIRCUMFERENCE', 'CONSUMPTION',
    # Potential hidden words
    'LONE', 'DEATH', 'DEAD', 'LIFE', 'TRUTH', 'LIE', 'LIGHT', 'DARK',
    'SOUL', 'SELF', 'MIND', 'BODY', 'HEART', 'EYE', 'EAR', 'HAND', 'FOOT',
}

def load_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_runes = []
    for c in content:
        if c in RUNE_MAP:
            all_runes.append(RUNE_MAP[c])
    
    # Split by word boundaries (• in the file)
    words = []
    word = []
    for c in content:
        if c in RUNE_MAP:
            word.append(RUNE_MAP[c])
        elif c == '•' or c == '\n':
            if word:
                words.append(word)
                word = []
    if word:
        words.append(word)
    
    return all_runes, words

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    all_runes, words = load_words(p20_path)
    print(f"Total runes: {len(all_runes)}")
    print(f"Total words: {len(words)}")
    
    # Check each word for English matches
    print("\n=== Words that match English dictionary ===")
    matches = []
    for i, word_indices in enumerate(words):
        latin = indices_to_latin(word_indices)
        # Check if it matches exactly
        if latin in ENGLISH_WORDS:
            matches.append((i, latin, 'exact'))
            print(f"Word {i}: {latin} (EXACT MATCH)")
        # Check if it contains an English word
        for eng_word in ENGLISH_WORDS:
            if eng_word in latin and len(eng_word) >= 3 and eng_word != latin:
                matches.append((i, latin, f'contains {eng_word}'))
    
    # Also search the continuous stream for English words
    print("\n=== English words in continuous stream ===")
    full_stream = indices_to_latin(all_runes)
    print(f"Full stream length: {len(full_stream)} chars")
    
    for word in sorted(ENGLISH_WORDS, key=len, reverse=True):
        if len(word) >= 3:
            idx = 0
            while True:
                idx = full_stream.find(word, idx)
                if idx == -1:
                    break
                print(f"  '{word}' found at position {idx}")
                idx += 1
    
    # Look for 3-letter word patterns
    print("\n=== All 3-letter patterns that are words ===")
    three_letter_words = {w for w in ENGLISH_WORDS if len(w) == 3}
    found_3 = set()
    for i in range(len(full_stream) - 2):
        substr = full_stream[i:i+3]
        if substr in three_letter_words:
            found_3.add((i, substr))
    
    for pos, word in sorted(found_3):
        print(f"  Position {pos}: {word}")
    
    # Also look for any repeating 3+ letter patterns (potential key patterns)
    print("\n=== Repeating patterns (length 3+) ===")
    patterns = Counter()
    for length in [3, 4, 5, 6]:
        for i in range(len(full_stream) - length + 1):
            substr = full_stream[i:i+length]
            patterns[substr] += 1
    
    print("Most common patterns:")
    for pattern, count in patterns.most_common(20):
        if count >= 3:
            print(f"  '{pattern}' appears {count} times")

if __name__ == '__main__':
    main()

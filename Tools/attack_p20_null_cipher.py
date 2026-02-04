#!/usr/bin/env python3
"""
Page 20: NULL CIPHER hypothesis

What if the prime-valued runes (TH, O, C, W, J, P, B, M, D) are NULL characters
that should be ignored, and the actual message is in the NON-prime valued runes only?

Also test: What if non-prime runes ARE the plaintext after a simple shift?
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

def load_runes_with_words(filepath):
    """Load runes and track word boundaries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    runes = []  # (position, value, word_num)
    word_num = 0
    pos = 0
    
    for c in content:
        if c in RUNE_MAP:
            runes.append((pos, RUNE_MAP[c], word_num))
            pos += 1
        elif c in '•\n':
            word_num += 1
    
    return runes

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

def count_english_words(text):
    """Count occurrences of English words."""
    words = ['THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER',
             'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW',
             'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY', 'DID',
             'SAY', 'SHE', 'TOO', 'USE', 'HER', 'EYE', 'THEY', 'THEM', 'THEN', 'THIS',
             'THAT', 'WITH', 'HAVE', 'FROM', 'BEEN', 'WERE', 'SAID', 'EACH', 'MADE',
             'LONE', 'PATH', 'SOUL', 'MIND', 'EODE', 'SEFA', 'DEOR']
    count = 0
    for word in words:
        count += text.count(word)
    return count

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    runes = load_runes_with_words(p20_path)
    print(f"Total runes: {len(runes)}")
    
    # Separate by value
    non_prime = [(pos, val, word) for pos, val, word in runes if val not in PRIME_VALUES]
    prime = [(pos, val, word) for pos, val, word in runes if val in PRIME_VALUES]
    
    print(f"Non-prime valued: {len(non_prime)}")
    print(f"Prime valued: {len(prime)}")
    
    # Extract just values
    non_prime_vals = [val for _, val, _ in non_prime]
    
    # Test various shifts on non-prime only
    print("\n=== NULL CIPHER: Read only non-prime valued runes ===")
    best_shift = 0
    best_count = 0
    
    for shift in range(29):
        shifted = [(v - shift) % 29 for v in non_prime_vals]
        text = indices_to_latin(shifted)
        count = count_english_words(text)
        if count > best_count:
            best_count = count
            best_shift = shift
        if count >= 5:
            print(f"\nShift {shift}: {count} words found")
            print(f"  {text[:150]}")
    
    print(f"\n=== BEST RESULT: Shift {best_shift} with {best_count} words ===")
    best_text = indices_to_latin([(v - best_shift) % 29 for v in non_prime_vals])
    print(best_text[:300])
    
    # Now try preserving word structure
    print("\n\n=== WORD-PRESERVED ANALYSIS ===")
    # Group non-prime runes by word
    words_dict = {}
    for pos, val, word in non_prime:
        if word not in words_dict:
            words_dict[word] = []
        words_dict[word].append(val)
    
    print(f"Words containing non-prime runes: {len(words_dict)}")
    
    # Check which words are readable with shift -2
    print("\nWords that become readable with shift -2:")
    readable_words = []
    for word_num in sorted(words_dict.keys()):
        vals = words_dict[word_num]
        shifted = [(v - 2) % 29 for v in vals]
        text = indices_to_latin(shifted)
        if any(w in text for w in ['THE', 'AND', 'FOR', 'ONE', 'DAY', 'WAY', 'HER', 'HIM', 'EYE']):
            readable_words.append((word_num, text))
            print(f"  Word {word_num}: {text}")
    
    # Check the ratio of prime to non-prime in each word
    print("\n\n=== PRIME/NON-PRIME RATIO PER WORD ===")
    all_runes_by_word = {}
    for pos, val, word in runes:
        if word not in all_runes_by_word:
            all_runes_by_word[word] = {'prime': 0, 'nonprime': 0, 'vals': []}
        if val in PRIME_VALUES:
            all_runes_by_word[word]['prime'] += 1
        else:
            all_runes_by_word[word]['nonprime'] += 1
        all_runes_by_word[word]['vals'].append(val)
    
    # Find words with ALL non-prime values
    all_nonprime_words = []
    for word_num, data in all_runes_by_word.items():
        if data['prime'] == 0 and data['nonprime'] > 0:
            text = indices_to_latin(data['vals'])
            all_nonprime_words.append((word_num, text))
    
    print(f"\nWords with NO prime-valued runes ({len(all_nonprime_words)} words):")
    for word_num, text in all_nonprime_words[:30]:
        shifted = indices_to_latin([(v - 2) % 29 for v in all_runes_by_word[word_num]['vals']])
        print(f"  Word {word_num}: raw={text}, shift-2={shifted}")

if __name__ == '__main__':
    main()

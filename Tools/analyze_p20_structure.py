#!/usr/bin/env python3
"""
Analyze Page 20 structure to understand the rune layout better.

The page uses • as word separators. Let's analyze:
1. Word lengths
2. Line structure
3. Any patterns in word positions relative to primes
"""

import os

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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    with open(p20_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse into lines
    lines = content.strip().split('\n')
    print(f"Total lines: {len(lines)}")
    
    # Global rune position counter
    global_pos = 0
    all_runes = []
    word_boundaries = []
    line_boundaries = []
    
    for line_num, line in enumerate(lines):
        line_start = global_pos
        words = line.split('•')
        
        for word_num, word in enumerate(words):
            word_start = global_pos
            for c in word:
                if c in RUNE_MAP:
                    all_runes.append((global_pos, c, RUNE_MAP[c], line_num))
                    global_pos += 1
            if global_pos > word_start:
                word_boundaries.append((word_start, global_pos - 1, line_num, word_num))
        
        if global_pos > line_start:
            line_boundaries.append((line_start, global_pos - 1, line_num))
    
    print(f"Total runes: {len(all_runes)}")
    print(f"Total words: {len(word_boundaries)}")
    
    # Analyze words with prime lengths
    print("\n=== Word Length Analysis ===")
    word_lengths = {}
    prime_length_words = []
    for start, end, line, word_num in word_boundaries:
        length = end - start + 1
        word_lengths[length] = word_lengths.get(length, 0) + 1
        if is_prime(length):
            prime_length_words.append((start, end, length, line, word_num))
    
    print("Word length distribution:")
    for length in sorted(word_lengths.keys()):
        prime_marker = "*" if is_prime(length) else ""
        print(f"  Length {length}{prime_marker}: {word_lengths[length]} words")
    
    print(f"\nWords with prime length: {len(prime_length_words)}")
    
    # Check if positions that are prime fall at word boundaries
    print("\n=== Prime Position Analysis ===")
    primes = [p for p in range(len(all_runes)) if is_prime(p)]
    
    # Count how many primes are at word starts/ends
    word_starts = set(w[0] for w in word_boundaries)
    word_ends = set(w[1] for w in word_boundaries)
    
    primes_at_word_start = [p for p in primes if p in word_starts]
    primes_at_word_end = [p for p in primes if p in word_ends]
    
    print(f"Prime positions at word start: {len(primes_at_word_start)}/{len(primes)}")
    print(f"Prime positions at word end: {len(primes_at_word_end)}/{len(primes)}")
    
    # Look at first few words
    print("\n=== First 20 Words ===")
    for i, (start, end, line, word_num) in enumerate(word_boundaries[:20]):
        length = end - start + 1
        runes = [all_runes[j][1] for j in range(start, end + 1)]
        rune_str = ''.join(runes)
        latin = ''.join(LATIN_TABLE[all_runes[j][2]] for j in range(start, end + 1))
        prime_positions = [j for j in range(start, end + 1) if is_prime(j)]
        print(f"Word {i}: pos {start}-{end} (len={length}), primes={prime_positions}")
        print(f"  Runes: {rune_str}")
        print(f"  Latin: {latin}")
    
    # Check if "REARRANGING" relates to word order
    print("\n=== Checking if word reordering needed ===")
    # Extract the first letter of each word
    acrostic = ''.join(LATIN_TABLE[all_runes[w[0]][2]] for w in word_boundaries if w[0] < len(all_runes))
    print(f"Acrostic (first letters): {acrostic[:50]}...")
    
    # Last letters
    telestich = ''.join(LATIN_TABLE[all_runes[w[1]][2]] for w in word_boundaries if w[1] < len(all_runes))
    print(f"Telestich (last letters): {telestich[:50]}...")
    
    # Prime-indexed words only
    prime_word_indices = [i for i in range(len(word_boundaries)) if is_prime(i)]
    print(f"\nPrime-indexed words (word # is prime): {len(prime_word_indices)}")
    prime_words_text = []
    for idx in prime_word_indices[:15]:
        start, end, line, word_num = word_boundaries[idx]
        latin = ''.join(LATIN_TABLE[all_runes[j][2]] for j in range(start, end + 1))
        prime_words_text.append(latin)
        print(f"  Word {idx}: {latin}")
    
    # Try concatenating prime-indexed words
    print(f"\nPrime-indexed words concatenated: {''.join(prime_words_text)}")

if __name__ == '__main__':
    main()

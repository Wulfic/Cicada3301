#!/usr/bin/env python3
"""
Analyze if PRIME-NUMBERED WORDS in Page 20 are plaintext.

We found that Word 17 = "THEY" (plaintext).
17 is a prime number!

Hypothesis: Words at prime indices (2, 3, 5, 7, 11, 13, 17...) are plaintext,
while words at composite indices are encrypted.
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

def load_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    words = []
    current_word = []
    for c in content:
        if c in RUNE_MAP:
            current_word.append(RUNE_MAP[c])
        elif c in '•\n':
            if current_word:
                words.append(current_word)
                current_word = []
    if current_word:
        words.append(current_word)
    return words

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    words = load_words(p20_path)
    print(f"Total words: {len(words)}")
    
    # Analyze prime-indexed words
    print("\n=== PRIME-INDEXED WORDS (potential plaintext) ===")
    prime_words = []
    for i in range(len(words)):
        if is_prime(i):
            latin = indices_to_latin(words[i])
            prime_words.append(latin)
            # Highlight if it looks like English
            looks_english = any(x in latin for x in ['THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT'])
            has_vowels = sum(1 for c in latin if c in 'AEIOU') > 0
            readable = '*' if looks_english else ('+' if has_vowels else '')
            print(f"  Word {i}: {latin} {readable}")
    
    print(f"\n=== PRIME WORDS CONCATENATED ===")
    prime_text = ' '.join(prime_words)
    print(prime_text)
    
    # Analyze composite-indexed words  
    print("\n=== COMPOSITE-INDEXED WORDS (first 20) ===")
    composite_words = []
    for i in range(len(words)):
        if not is_prime(i) and i >= 4:  # Composite, not 0 or 1
            latin = indices_to_latin(words[i])
            composite_words.append(latin)
            if len(composite_words) <= 20:
                print(f"  Word {i}: {latin}")
    
    # Try reading alternate pattern - even/odd
    print("\n=== EVEN-INDEXED WORDS ===")
    even_text = ' '.join(indices_to_latin(words[i]) for i in range(0, len(words), 2))
    print(even_text[:200])
    
    print("\n=== ODD-INDEXED WORDS ===")
    odd_text = ' '.join(indices_to_latin(words[i]) for i in range(1, len(words), 2))
    print(odd_text[:200])
    
    # Check if the pattern "THEY" at word 17 continues
    # What about word indices that are prime squared? (4, 9, 25, 49...)
    print("\n=== PRIME SQUARED INDICES (4, 9, 25, 49, 121) ===")
    prime_sq = [p*p for p in [2, 3, 5, 7, 11] if p*p < len(words)]
    for i in prime_sq:
        print(f"  Word {i}: {indices_to_latin(words[i])}")
    
    # Check twin primes (p, p+2 both prime)
    print("\n=== TWIN PRIME INDEXED WORDS ===")
    for i in range(len(words) - 2):
        if is_prime(i) and is_prime(i + 2):
            print(f"  Words {i},{i+2}: {indices_to_latin(words[i])} | {indices_to_latin(words[i+2])}")
    
    # Check if word 17 "THEY" could be part of "THEY WENT" (EODE)
    # Look for patterns around word 17
    print("\n=== CONTEXT AROUND WORD 17 'THEY' ===")
    for i in range(max(0, 17-5), min(len(words), 17+6)):
        marker = "<<< THEY" if i == 17 else ""
        prime_marker = "(prime)" if is_prime(i) else "(composite)"
        print(f"  Word {i} {prime_marker}: {indices_to_latin(words[i])} {marker}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Page 20: Use PRIME-valued runes as KEY for NON-PRIME valued runes

The prime stream has only 9 values: TH, O, C, W, J, P, B, M, D
The non-prime stream is 575 runes, prime stream is 237 runes

Try using the 237-rune prime stream as a cycling key.
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

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

ENGLISH_WORDS = set([
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I', 'IT', 'FOR', 'NOT',
    'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT', 'THIS', 'BUT', 'HIS', 'BY', 'FROM',
    'THEY', 'WE', 'SAY', 'HER', 'SHE', 'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD',
    'THERE', 'THEIR', 'WHAT', 'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH',
    'GO', 'ME', 'WHEN', 'MAKE', 'CAN', 'LIKE', 'TIME', 'NO', 'JUST', 'HIM', 'KNOW',
    'LONE', 'PATH', 'TRUTH', 'LIGHT', 'DARK', 'SOUL', 'MIND', 'BODY', 'HEART', 'DEATH',
    'EODE', 'SEFA', 'DEOR', 'WAY', 'EYE', 'DAY', 'OUR', 'OWN', 'SELF',
])

def count_words(text):
    count = 0
    for word in ENGLISH_WORDS:
        if len(word) >= 3:
            count += text.count(word)
    return count

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    # Separate streams
    prime_stream = [c for c in cipher if c in PRIME_VALUES]
    non_prime_stream = [c for c in cipher if c not in PRIME_VALUES]
    
    print(f"Prime stream: {len(prime_stream)} runes")
    print(f"Non-prime stream: {len(non_prime_stream)} runes")
    
    results = []
    
    # Test: Use prime stream as cycling Vigenère key for non-prime stream
    print("\n=== PRIME STREAM AS KEY FOR NON-PRIME STREAM ===")
    for mode in ['sub', 'add', 'beaufort']:
        stream = []
        for i, c in enumerate(non_prime_stream):
            k = prime_stream[i % len(prime_stream)]
            if mode == 'sub':
                stream.append((c - k) % 29)
            elif mode == 'add':
                stream.append((c + k) % 29)
            else:
                stream.append((k - c) % 29)
        
        ioc = calc_ioc(stream)
        latin = indices_to_latin(stream)
        words = count_words(latin)
        results.append((f'prime_key_{mode}', ioc, words, latin))
        print(f"  {mode}: IoC={ioc:.4f}, words={words}")
        print(f"    {latin[:100]}")
    
    # Test: INTERLEAVE - rebuild message by putting prime and non-prime back together
    print("\n=== INTERLEAVED (prime as-is, non-prime shifted) ===")
    
    for shift in [0, 2, -2, 1, -1]:
        # Rebuild the full message with prime positions intact, non-prime shifted
        result = []
        prime_idx = 0
        non_prime_idx = 0
        
        for c in cipher:
            if c in PRIME_VALUES:
                result.append(c)
                prime_idx += 1
            else:
                result.append((c - shift) % 29)
                non_prime_idx += 1
        
        latin = indices_to_latin(result)
        words = count_words(latin)
        ioc = calc_ioc(result)
        results.append((f'interleave_shift{shift}', ioc, words, latin))
        print(f"  Shift {shift}: IoC={ioc:.4f}, words={words}")
        print(f"    {latin[:100]}")
    
    # Test: Use first prime rune to shift all subsequent non-prime runes
    print("\n=== RUNNING PRIME KEY ===")
    for mode in ['sub', 'add']:
        result = []
        prime_idx = 0
        current_key = 0
        
        for c in cipher:
            if c in PRIME_VALUES:
                current_key = c
                result.append(c)  # Keep prime as-is
            else:
                if mode == 'sub':
                    result.append((c - current_key) % 29)
                else:
                    result.append((c + current_key) % 29)
        
        latin = indices_to_latin(result)
        words = count_words(latin)
        ioc = calc_ioc(result)
        results.append((f'running_prime_{mode}', ioc, words, latin))
        print(f"  {mode}: IoC={ioc:.4f}, words={words}")
        print(f"    {latin[:100]}")
    
    # Sort by word count
    results.sort(key=lambda x: x[2], reverse=True)
    print("\n=== BEST RESULTS BY WORD COUNT ===")
    for name, ioc, words, latin in results[:5]:
        print(f"\n{name}: IoC={ioc:.4f}, words={words}")
        print(f"  {latin[:200]}")

if __name__ == '__main__':
    main()

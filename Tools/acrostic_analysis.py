#!/usr/bin/env python3
"""
Deep Dive into Promising Patterns
The acrostic (first letters) and every-7th-rune show elevated IoC (~0.07)
"""

import os
from collections import Counter
import re

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LETTER = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E',
    19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

COMMON_WORDS = {'THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'AS', 'WITH', 'WAS', 
                'HIS', 'BE', 'AT', 'BY', 'THIS', 'HAD', 'NOT', 'ARE', 'BUT', 'FROM',
                'DIVINITY', 'WITHIN', 'PRIMES', 'SACRED', 'PILGRIM', 'WISDOM', 'TRUTH',
                'CIRCUMFERENCE', 'EMERGE', 'INSTAR', 'WE', 'AN', 'THAT', 'THEY'}

def load_page_content(page_num):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_file = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if not os.path.exists(rune_file):
        return None, None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    runes = [c for c in content if c in RUNE_TO_INDEX]
    return content, runes

def calculate_ioc(text):
    counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        count = text.count(word)
        score += len(word) * 10 * count
    return score

def main():
    print("=" * 70)
    print("DEEP DIVE: ACROSTIC AND EVERY-7TH PATTERNS")
    print("=" * 70)
    
    page_data = []
    for page_num in range(18, 55):
        content, runes = load_page_content(page_num)
        if runes:
            page_data.append((page_num, content, runes))
    
    print("\n" + "=" * 70)
    print("ACROSTIC ANALYSIS (First letter of each word)")
    print("=" * 70)
    
    # Get first letters per page
    for page_num, content, runes in page_data[:5]:
        words = re.split(r'[-.\s•&§\n]+', content)
        first_letters = []
        for word in words:
            word_runes = [c for c in word if c in RUNE_TO_INDEX]
            if word_runes:
                first_letters.append(INDEX_TO_LETTER[RUNE_TO_INDEX[word_runes[0]]])
        
        acrostic = ''.join(first_letters)
        ioc = calculate_ioc(acrostic)
        score = score_text(acrostic)
        print(f"\nPage {page_num}: {len(acrostic)} chars, IoC={ioc:.4f}, Score={score}")
        print(f"  {acrostic}")
    
    print("\n" + "=" * 70)
    print("EVERY 7TH RUNE PER PAGE")
    print("=" * 70)
    
    for page_num, content, runes in page_data[:10]:
        seventh = []
        for i in range(0, len(runes), 7):
            seventh.append(INDEX_TO_LETTER[RUNE_TO_INDEX[runes[i]]])
        
        text = ''.join(seventh)
        ioc = calculate_ioc(text)
        score = score_text(text)
        print(f"Page {page_num}: IoC={ioc:.4f}, Score={score}")
        print(f"  {text[:60]}")
    
    print("\n" + "=" * 70)
    print("TESTING VIGENERE ON ACROSTIC (key length 7)")
    print("=" * 70)
    
    # Collect all first letters
    all_first = []
    for page_num, content, runes in page_data:
        words = re.split(r'[-.\s•&§\n]+', content)
        for word in words:
            word_runes = [c for c in word if c in RUNE_TO_INDEX]
            if word_runes:
                all_first.append(RUNE_TO_INDEX[word_runes[0]])
    
    # Try various key lengths on the acrostic
    print(f"Acrostic length: {len(all_first)} characters")
    
    for key_length in [3, 5, 7, 11, 13, 17, 19, 23]:
        # Calculate IoC for each column
        columns = [[] for _ in range(key_length)]
        for i, idx in enumerate(all_first):
            columns[i % key_length].append(idx)
        
        column_iocs = [calculate_ioc([INDEX_TO_LETTER[x] for x in col]) for col in columns]
        avg_ioc = sum(column_iocs) / len(column_iocs)
        print(f"Key length {key_length:2}: Avg column IoC = {avg_ioc:.4f} | {['%.3f' % x for x in column_iocs[:5]]}")
    
    print("\n" + "=" * 70)
    print("LOOKING FOR PATTERNS IN WORD BOUNDARIES")
    print("=" * 70)
    
    # Check if word boundary patterns encode something
    all_word_lengths = []
    for page_num, content, runes in page_data:
        words = re.split(r'[-.\s•&§\n]+', content)
        for word in words:
            word_runes = [c for c in word if c in RUNE_TO_INDEX]
            if word_runes:
                all_word_lengths.append(len(word_runes))
    
    # Convert to binary (odd=1, even=0)
    binary = ''.join(['1' if l % 2 else '0' for l in all_word_lengths[:80]])
    print(f"Word lengths as binary (odd=1): {binary}")
    
    # Check if groups of 5 form letters (like Bacon cipher)
    bacon_groups = [binary[i:i+5] for i in range(0, len(binary)-4, 5)]
    bacon_decode = []
    for g in bacon_groups:
        val = int(g, 2)
        if val < 26:
            bacon_decode.append(chr(ord('A') + val))
    print(f"As Bacon cipher: {''.join(bacon_decode)}")
    
    print("\n" + "=" * 70)
    print("TESTING MONOALPHABETIC ON ACROSTIC")
    print("=" * 70)
    
    # Get English letter frequencies for acrostic
    acrostic_text = ''.join([INDEX_TO_LETTER[x] for x in all_first])
    
    # Count single-char letters only
    letter_counts = Counter()
    for letter in acrostic_text:
        if len(letter) == 1:
            letter_counts[letter] += 1
    
    print("Frequency in acrostic (single letters):")
    total = sum(letter_counts.values())
    for letter, count in sorted(letter_counts.items(), key=lambda x: -x[1])[:10]:
        pct = count / total * 100
        print(f"  {letter}: {count} ({pct:.1f}%)")
    
    # English frequencies
    english_freq = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0}
    print("\nExpected English:")
    for letter, pct in list(english_freq.items())[:10]:
        print(f"  {letter}: {pct:.1f}%")

if __name__ == '__main__':
    main()

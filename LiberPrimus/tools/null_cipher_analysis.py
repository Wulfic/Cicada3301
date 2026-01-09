#!/usr/bin/env python3
"""
Null Cipher and Extraction Pattern Analysis
Testing if pages 18-54 use null cipher or specific extraction patterns

Hypotheses:
1. Only runes at PRIME positions are meaningful
2. Only runes after certain markers (F, word boundaries) matter
3. First letters of each word form the message
4. Last letters of each word form the message
5. Runes at Fibonacci positions
6. Every Nth rune (where N is prime)
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

def sieve_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

def fibonacci_sequence(max_n):
    fibs = [1, 2]
    while fibs[-1] < max_n:
        fibs.append(fibs[-1] + fibs[-2])
    return [f for f in fibs if f < max_n]

def load_page_content(page_num):
    """Load raw content including word boundaries"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_file = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if not os.path.exists(rune_file):
        return None, None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just runes
    runes = [c for c in content if c in RUNE_TO_INDEX]
    
    return content, runes

def extract_at_positions(runes, positions):
    """Extract runes at specific positions"""
    result = []
    for pos in positions:
        if pos < len(runes):
            result.append(INDEX_TO_LETTER[RUNE_TO_INDEX[runes[pos]]])
    return ''.join(result)

def calculate_ioc(text):
    counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))

def main():
    print("=" * 70)
    print("NULL CIPHER AND EXTRACTION PATTERN ANALYSIS")
    print("=" * 70)
    
    primes = sieve_primes(2000)
    fibs = fibonacci_sequence(2000)
    
    # Collect all runes from pages 18-54
    all_runes = []
    page_data = []
    
    for page_num in range(18, 55):
        content, runes = load_page_content(page_num)
        if runes:
            page_data.append((page_num, content, runes))
            all_runes.extend(runes)
    
    print(f"Loaded {len(page_data)} pages with {len(all_runes)} total runes")
    
    print("\n" + "=" * 70)
    print("STRATEGY 1: Prime-indexed runes from all pages combined")
    print("=" * 70)
    
    prime_extract = extract_at_positions(all_runes, primes)
    ioc = calculate_ioc(prime_extract)
    print(f"Extracted {len(prime_extract)} runes at prime positions")
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {prime_extract[:200]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 2: Fibonacci-indexed runes from all pages combined")
    print("=" * 70)
    
    fib_extract = extract_at_positions(all_runes, fibs)
    ioc = calculate_ioc(fib_extract)
    print(f"Extracted {len(fib_extract)} runes at Fibonacci positions")
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {fib_extract}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 3: First rune of each word (acrostic)")
    print("=" * 70)
    
    # Extract first rune of each "word" (separated by hyphens, periods, spaces, bullets)
    first_letters = []
    for page_num, content, runes in page_data:
        # Split content by separators
        words = re.split(r'[-.\s•&§\n]+', content)
        for word in words:
            word_runes = [c for c in word if c in RUNE_TO_INDEX]
            if word_runes:
                first_letters.append(INDEX_TO_LETTER[RUNE_TO_INDEX[word_runes[0]]])
    
    acrostic = ''.join(first_letters)
    ioc = calculate_ioc(acrostic)
    print(f"Extracted {len(acrostic)} first letters")
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {acrostic[:200]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 4: Last rune of each word (telestich)")
    print("=" * 70)
    
    last_letters = []
    for page_num, content, runes in page_data:
        words = re.split(r'[-.\s•&§\n]+', content)
        for word in words:
            word_runes = [c for c in word if c in RUNE_TO_INDEX]
            if word_runes:
                last_letters.append(INDEX_TO_LETTER[RUNE_TO_INDEX[word_runes[-1]]])
    
    telestich = ''.join(last_letters)
    ioc = calculate_ioc(telestich)
    print(f"Extracted {len(telestich)} last letters")
    print(f"IoC: {ioc:.4f}")
    print(f"Text: {telestich[:200]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 5: Every Nth rune (N = 2, 3, 5, 7, 11, 13)")
    print("=" * 70)
    
    for n in [2, 3, 5, 7, 11, 13]:
        extract = extract_at_positions(all_runes, list(range(0, len(all_runes), n)))
        ioc = calculate_ioc(extract)
        print(f"Every {n}th rune ({len(extract)} chars): IoC={ioc:.4f}")
        print(f"  Preview: {extract[:80]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 6: Runes immediately AFTER F (ᚠ)")
    print("=" * 70)
    
    # F might be a marker - check what comes after it
    after_f = []
    for i, rune in enumerate(all_runes[:-1]):
        if rune == 'ᚠ':
            after_f.append(INDEX_TO_LETTER[RUNE_TO_INDEX[all_runes[i+1]]])
    
    after_f_text = ''.join(after_f)
    ioc = calculate_ioc(after_f_text)
    print(f"Runes after F: {len(after_f_text)} chars, IoC={ioc:.4f}")
    print(f"Text: {after_f_text}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 7: Count of each rune across all pages")
    print("=" * 70)
    
    counts = Counter(all_runes)
    for rune, count in sorted(counts.items(), key=lambda x: -x[1]):
        letter = INDEX_TO_LETTER[RUNE_TO_INDEX[rune]]
        pct = count / len(all_runes) * 100
        print(f"  {rune} ({letter:>2}): {count:4} ({pct:.2f}%)")
    
    print("\n" + "=" * 70)
    print("STRATEGY 8: Prime-indexed runes from EACH page separately")
    print("=" * 70)
    
    all_prime_extracts = []
    for page_num, content, runes in page_data[:10]:  # First 10 pages
        prime_runes = []
        for p in primes:
            if p < len(runes):
                prime_runes.append(INDEX_TO_LETTER[RUNE_TO_INDEX[runes[p]]])
        
        prime_text = ''.join(prime_runes)
        ioc = calculate_ioc(prime_text) if len(prime_text) > 1 else 0
        print(f"Page {page_num}: {prime_text[:40]}... (IoC={ioc:.4f})")
        all_prime_extracts.append(prime_text)
    
    print("\n" + "=" * 70)
    print("STRATEGY 9: Look for repeated patterns in word structure")
    print("=" * 70)
    
    # Analyze word lengths
    all_word_lengths = []
    for page_num, content, runes in page_data:
        words = re.split(r'[-.\s•&§\n]+', content)
        for word in words:
            word_runes = [c for c in word if c in RUNE_TO_INDEX]
            if word_runes:
                all_word_lengths.append(len(word_runes))
    
    length_counts = Counter(all_word_lengths)
    print("Word length distribution:")
    for length in sorted(length_counts.keys())[:15]:
        print(f"  {length} letters: {length_counts[length]} words")
    
    # Check if word lengths encode something
    # Convert word lengths to letters (1=A, 2=B, etc.)
    length_message = []
    for length in all_word_lengths[:100]:
        if 1 <= length <= 26:
            length_message.append(chr(ord('A') + length - 1))
    print(f"\nWord lengths as letters: {''.join(length_message)[:80]}")

if __name__ == '__main__':
    main()

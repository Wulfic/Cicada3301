#!/usr/bin/env python3
"""
DEEP PATTERN ANALYSIS
=====================

Look for structural patterns in our decryptions that might reveal
the underlying cipher mechanism.
"""

import numpy as np
from pathlib import Path
import re
from collections import Counter

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                       20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                       17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                       5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                       14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def extend_key(key, length):
    return np.tile(key, (length // len(key) + 1))[:length]

def load_all_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_to_indices(runes_only)
    return pages

# English text scoring
COMMON_WORDS = {
    'THE', 'OF', 'AND', 'A', 'TO', 'IN', 'IS', 'IT', 'YOU', 'THAT', 
    'HE', 'WAS', 'FOR', 'ON', 'ARE', 'AS', 'WITH', 'HIS', 'THEY', 
    'I', 'AT', 'BE', 'THIS', 'HAVE', 'FROM', 'OR', 'ONE', 'HAD', 
    'BY', 'NOT', 'BUT', 'WHAT', 'ALL', 'WERE', 'WE', 'WHEN', 'YOUR',
    'CAN', 'SAID', 'EACH', 'WHICH', 'SHE', 'DO', 'HOW', 'THEIR',
    # Philosophical words likely in Cicada text
    'WISDOM', 'TRUTH', 'DIVINE', 'DIVINITY', 'SOUL', 'MIND', 'LIGHT',
    'DARKNESS', 'PATH', 'KNOWLEDGE', 'ENLIGHTEN', 'EMERGE', 'PRIME',
    'CIRCUMFERENCE', 'INSTAR', 'PARABLE', 'BEING', 'BECOMING'
}

def count_word_matches(text):
    count = 0
    text_upper = text.upper()
    for word in COMMON_WORDS:
        count += text_upper.count(word)
    return count

def analyze_trigram_distribution(text):
    """Analyze trigram (3-letter) distribution."""
    trigrams = Counter()
    for i in range(len(text) - 2):
        trigrams[text[i:i+3]] += 1
    return trigrams

def main():
    pages = load_all_pages()
    
    print("="*70)
    print("🔬 DEEP PATTERN ANALYSIS")
    print("="*70)
    
    # Test: What if the key rotation is based on page number?
    print("\n📊 TEST 1: Page-Number-Based Rotation")
    print("-" * 60)
    print("Testing if rotation = page_number mod 95")
    
    for pg_num, pg_idx in sorted(pages.items()):
        # Skip solved pages
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Test rotation = page_num mod 95
        rot = pg_num % 95
        rotated = np.roll(MASTER_KEY, rot)
        extended = extend_key(rotated, len(pg_idx))
        
        # Test both XOR and subtraction
        for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                            ('xor', lambda x, k: (x ^ k) % 29)]:
            decrypted = op(pg_idx, extended)
            text = indices_to_text(decrypted)
            word_count = count_word_matches(text)
            if word_count >= 10:
                print(f"  Page {pg_num}: rot={rot}, {op_name} -> {word_count} words: {text[:50]}...")
    
    # Test: What if offset is based on page number?
    print("\n📊 TEST 2: Page-Number-Based Offset")
    print("-" * 60)
    print("Testing if offset = page_number mod 29")
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Test offset = page_num mod 29
        off = pg_num % 29
        key = (MASTER_KEY + off) % 29
        extended = extend_key(key, len(pg_idx))
        
        for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                            ('xor', lambda x, k: (x ^ k) % 29)]:
            decrypted = op(pg_idx, extended)
            text = indices_to_text(decrypted)
            word_count = count_word_matches(text)
            if word_count >= 10:
                print(f"  Page {pg_num}: off={off}, {op_name} -> {word_count} words: {text[:50]}...")
    
    # Test: Key derived from page position in sequence
    print("\n📊 TEST 3: Combined Page-Based Parameters")
    print("-" * 60)
    print("Testing rotation = page, offset = 29 - (page mod 29)")
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        rot = pg_num % 95
        off = (29 - (pg_num % 29)) % 29
        
        rotated = np.roll(MASTER_KEY, rot)
        key = (rotated + off) % 29
        extended = extend_key(key, len(pg_idx))
        
        for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                            ('xor', lambda x, k: (x ^ k) % 29)]:
            decrypted = op(pg_idx, extended)
            text = indices_to_text(decrypted)
            word_count = count_word_matches(text)
            if word_count >= 8:
                print(f"  Page {pg_num}: rot={rot}, off={off}, {op_name} -> {word_count} words: {text[:50]}...")
    
    # Test: Fibonacci positions
    print("\n📊 TEST 4: Fibonacci-Based Key Selection")
    print("-" * 60)
    fib = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    print(f"Using Fibonacci positions: {fib[:5]}...")
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Use only Fibonacci positions from the key
        fib_key = MASTER_KEY[[f % 95 for f in fib]]
        extended = extend_key(fib_key, len(pg_idx))
        
        for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                            ('xor', lambda x, k: (x ^ k) % 29)]:
            decrypted = op(pg_idx, extended)
            text = indices_to_text(decrypted)
            word_count = count_word_matches(text)
            if word_count >= 8:
                print(f"  Page {pg_num}: fib_key, {op_name} -> {word_count} words: {text[:50]}...")
    
    # Test: Prime positions
    print("\n📊 TEST 5: Prime-Position Key Selection")
    print("-" * 60)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
    primes_in_range = [p for p in primes if p < 95]
    print(f"Using prime positions: {primes_in_range[:8]}...")
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Use only prime positions from the key
        prime_key = MASTER_KEY[primes_in_range]
        extended = extend_key(prime_key, len(pg_idx))
        
        for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                            ('xor', lambda x, k: (x ^ k) % 29)]:
            decrypted = op(pg_idx, extended)
            text = indices_to_text(decrypted)
            word_count = count_word_matches(text)
            if word_count >= 8:
                print(f"  Page {pg_num}: prime_key, {op_name} -> {word_count} words: {text[:50]}...")
    
    # Test: Running key cipher (autokey)
    print("\n📊 TEST 6: Autokey Cipher Variant")
    print("-" * 60)
    print("Testing if plaintext itself becomes part of key (autokey)")
    
    for pg_num, pg_idx in sorted(pages.items())[:5]:  # Test first few
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Start with master key, then use decrypted values
        decrypted = np.zeros(len(pg_idx), dtype=np.int32)
        key_pos = 0
        
        for i in range(len(pg_idx)):
            if i < len(MASTER_KEY):
                k = MASTER_KEY[i]
            else:
                k = decrypted[i - len(MASTER_KEY)]  # Use previous plaintext
            
            decrypted[i] = (pg_idx[i] - k) % 29
        
        text = indices_to_text(decrypted)
        word_count = count_word_matches(text)
        print(f"  Page {pg_num}: autokey -> {word_count} words: {text[:50]}...")
    
    # Summary analysis of top pages
    print("\n📊 ANALYSIS: Top Scoring Pages Structure")
    print("-" * 60)
    
    top_pages = [
        (29, 'xor', 6, 17),
        (47, 'xor', 52, 16),
        (28, 'xor', 34, 14),
        (52, 'xor', 21, 11),
    ]
    
    for pg_num, op, rot, off in top_pages:
        pg_idx = pages[pg_num]
        
        rotated = np.roll(MASTER_KEY, rot)
        key = (rotated + off) % 29
        extended = extend_key(key, len(pg_idx))
        
        if op == 'xor':
            decrypted = (pg_idx ^ extended) % 29
        else:
            decrypted = (pg_idx - extended) % 29
        
        text = indices_to_text(decrypted)
        
        # Analyze structure
        print(f"\nPage {pg_num} (rot={rot}, off={off}):")
        print(f"  Length: {len(text)} chars")
        
        # Trigram analysis
        trigrams = analyze_trigram_distribution(text)
        most_common = trigrams.most_common(10)
        print(f"  Top trigrams: {most_common[:5]}")
        
        # Letter frequency
        letter_counts = Counter(text)
        print(f"  Top letters: {letter_counts.most_common(5)}")
        
        # Check for interesting patterns
        if 'TRUTH' in text:
            idx = text.index('TRUTH')
            print(f"  ⭐ TRUTH found at position {idx}")
        if 'THE' in text:
            the_positions = [i for i in range(len(text)-2) if text[i:i+3] == 'THE']
            print(f"  'THE' appears at: {the_positions[:10]}...")
    
    print("\n" + "="*70)
    print("✅ DEEP ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

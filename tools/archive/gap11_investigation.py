#!/usr/bin/env python3
"""
Gap-11 Key Pattern Investigation

From community research (Profetul/mortlach):
- Cyclical gaps of 11 between key elements generate "low doubles"
- Pattern: 11, -18, 11, 11, -18, 11, X
- Note: 29 - 18 = 11, so -18 ≡ 11 (mod 29)

This creates keys like: 0, 11, 22, 4, 15, 26, 8, 19, 1, 12, 23, 5, 16, 27, 9, 20, 2, 13, 24, 6, 17, 28, 10, 21, 3, 14, 25, 7, 18

Testing if this pattern could be the cipher key.
"""

import re
import numpy as np
from collections import Counter

# =============================================================================
# RUNE DATA
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

def load_pages():
    data_file = r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py"
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[int(i) % 29] for i in indices)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def generate_gap_stream(gap, length, start=0):
    """Generate a stream with consistent gap between elements"""
    stream = []
    current = start
    for _ in range(length):
        stream.append(current % 29)
        current += gap
    return np.array(stream, dtype=np.int32)

def generate_alternating_gap_stream(gaps, length, start=0):
    """Generate stream with alternating gaps like 11, -18, 11, 11, -18..."""
    stream = []
    current = start
    gap_idx = 0
    for _ in range(length):
        stream.append(current % 29)
        current += gaps[gap_idx % len(gaps)]
        gap_idx += 1
    return np.array(stream, dtype=np.int32)

COMMON_WORDS = ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'ARE',
                'NOT', 'ME', 'WE', 'BE', 'OR', 'AN', 'HE', 'AS', 'DO', 'AT',
                'INSTAR', 'PARABLE', 'EMERGE', 'DIVINITY', 'WITHIN']

def score_text(text):
    score = 0
    text_upper = text.upper()
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word)
    return score

def main():
    print("="*70)
    print("GAP-11 KEY PATTERN INVESTIGATION")
    print("="*70)
    
    pages = load_pages()
    
    # First, visualize the gap-11 pattern
    print("\n=== GAP-11 STREAM ===\n")
    
    gap11_stream = generate_gap_stream(11, 29, start=0)
    print(f"Gap-11 sequence (first 29): {gap11_stream}")
    print(f"As letters: {indices_to_text(gap11_stream)}")
    
    # This covers all 29 values in a specific order
    print(f"\nUnique values: {len(set(gap11_stream))} (should be 29)")
    
    # Test alternating gap patterns
    print("\n=== ALTERNATING GAP PATTERNS ===\n")
    
    gap_patterns = [
        ([11], "pure-11"),
        ([11, -18], "11,-18"),
        ([11, 11, -18], "11,11,-18"),
        ([11, -18, 11, 11, -18], "11,-18,11,11,-18"),
        ([7], "pure-7"),
        ([7, -22], "7,-22"),  # 29-22=7
        ([13], "pure-13"),
        ([13, -16], "13,-16"),  # 29-16=13
    ]
    
    all_results = []
    
    for gaps, name in gap_patterns:
        print(f"\nPattern '{name}':")
        
        for page_num in sorted(pages.keys()):
            if page_num in [56, 57]:
                continue
            
            cipher = runes_to_indices(pages[page_num])
            n = len(cipher)
            
            if n < 20:
                continue
            
            best_for_page = None
            
            for start in range(29):
                key = generate_alternating_gap_stream(gaps, n, start)
                
                # Try subtraction
                decrypted = (cipher - key) % 29
                text = indices_to_text(decrypted)
                ioc = calculate_ioc(decrypted)
                word_score = score_text(text)
                
                combined = ioc + word_score / 100
                
                if best_for_page is None or combined > best_for_page[0]:
                    best_for_page = (combined, start, text[:60], ioc, word_score, 'sub')
                
                # Try addition
                decrypted = (cipher + key) % 29
                text = indices_to_text(decrypted)
                ioc = calculate_ioc(decrypted)
                word_score = score_text(text)
                
                combined = ioc + word_score / 100
                
                if combined > best_for_page[0]:
                    best_for_page = (combined, start, text[:60], ioc, word_score, 'add')
            
            if best_for_page and (best_for_page[3] > 1.1 or best_for_page[4] > 15):
                all_results.append((best_for_page[0], page_num, name, best_for_page[1], 
                                   best_for_page[2], best_for_page[3], best_for_page[4], best_for_page[5]))
    
    # Sort and display top results
    all_results.sort(reverse=True)
    
    print("\n" + "="*70)
    print("TOP 20 GAP PATTERN RESULTS")
    print("="*70 + "\n")
    
    for combined, page, pattern, start, text, ioc, word_score, op in all_results[:20]:
        found = [w for w in COMMON_WORDS if w in text.upper()]
        print(f"Page {page:2d}: pattern={pattern}, start={start:2d}, op={op}")
        print(f"  IoC={ioc:.4f}, word_score={word_score}, combined={combined:.4f}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Now test combined gap + prime approach
    print("\n" + "="*70)
    print("COMBINED GAP-11 + PRIME APPROACH")
    print("="*70 + "\n")
    
    # Like Page 56 but with gap-11 instead of consecutive primes
    all_results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        best_for_page = None
        
        for gap in [11, 7, 13, 5, 17]:
            for offset in range(100):
                # Create key: (gap_stream[i] + offset) mod 29
                key = generate_gap_stream(gap, n, start=0)
                key = (key + offset) % 29
                
                decrypted = (cipher - key) % 29
                text = indices_to_text(decrypted)
                ioc = calculate_ioc(decrypted)
                word_score = score_text(text)
                
                combined = ioc + word_score / 100
                
                if best_for_page is None or combined > best_for_page[0]:
                    best_for_page = (combined, gap, offset, text[:60], ioc, word_score)
        
        if best_for_page and (best_for_page[4] > 1.1 or best_for_page[5] > 15):
            all_results.append((best_for_page[0], page_num, best_for_page[1], best_for_page[2],
                               best_for_page[3], best_for_page[4], best_for_page[5]))
    
    all_results.sort(reverse=True)
    
    print("Top 15 gap+offset results:\n")
    for combined, page, gap, offset, text, ioc, word_score in all_results[:15]:
        found = [w for w in COMMON_WORDS if w in text.upper()]
        print(f"Page {page:2d}: gap={gap:2d}, offset={offset:2d}")
        print(f"  IoC={ioc:.4f}, word_score={word_score}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Finally, test gap-prime (gap = prime[i] mod 29)
    print("\n" + "="*70)
    print("GAP AS PRIME[i] MOD 29")
    print("="*70 + "\n")
    
    # The key is: sum of (prime[j] for j in range(i)) mod 29
    # This creates a growing offset based on prime sums
    
    all_results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        best_for_page = None
        
        # Create cumulative prime sum key
        prime_sum_key = []
        running_sum = 0
        for i in range(n):
            prime_sum_key.append(running_sum % 29)
            running_sum += PRIMES[i % 29]
        
        prime_sum_key = np.array(prime_sum_key, dtype=np.int32)
        
        for offset in range(29):
            key = (prime_sum_key + offset) % 29
            
            decrypted = (cipher - key) % 29
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            word_score = score_text(text)
            
            combined = ioc + word_score / 100
            
            if best_for_page is None or combined > best_for_page[0]:
                best_for_page = (combined, offset, text[:60], ioc, word_score)
        
        if best_for_page and (best_for_page[3] > 1.1 or best_for_page[4] > 15):
            all_results.append((best_for_page[0], page_num, best_for_page[1],
                               best_for_page[2], best_for_page[3], best_for_page[4]))
    
    all_results.sort(reverse=True)
    
    print("Top 15 cumulative-prime-sum results:\n")
    for combined, page, offset, text, ioc, word_score in all_results[:15]:
        found = [w for w in COMMON_WORDS if w in text.upper()]
        print(f"Page {page:2d}: offset={offset:2d}")
        print(f"  IoC={ioc:.4f}, word_score={word_score}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()

if __name__ == "__main__":
    main()

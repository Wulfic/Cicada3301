#!/usr/bin/env python3
"""
Cross-Page Pattern Analysis for Liber Primus

Looking for:
1. Repeated sequences across pages (might be encrypted common words/phrases)
2. Statistical anomalies that might indicate crib positions
3. Patterns in the gematria values
"""

import re
import numpy as np
from collections import Counter, defaultdict

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

def find_repeated_ngrams(pages, n):
    """Find n-grams that appear in multiple pages"""
    ngram_locations = defaultdict(list)
    
    for page_num, runes in pages.items():
        indices = runes_to_indices(runes)
        for i in range(len(indices) - n + 1):
            ngram = tuple(indices[i:i+n])
            ngram_locations[ngram].append((page_num, i))
    
    # Filter to ngrams that appear multiple times
    repeated = {k: v for k, v in ngram_locations.items() if len(v) > 1}
    
    return repeated

def main():
    print("="*70)
    print("CROSS-PAGE PATTERN ANALYSIS")
    print("="*70)
    
    pages = load_pages()
    
    # Find repeated trigrams across all pages
    print("\n=== REPEATED TRIGRAMS ACROSS PAGES ===\n")
    
    repeated_trigrams = find_repeated_ngrams(pages, 3)
    
    # Sort by frequency
    sorted_trigrams = sorted(repeated_trigrams.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"Found {len(repeated_trigrams)} unique trigrams appearing in multiple locations\n")
    
    print("Top 20 most common trigrams:")
    for i, (ngram, locations) in enumerate(sorted_trigrams[:20]):
        text = indices_to_text(ngram)
        page_list = sorted(set([loc[0] for loc in locations]))
        print(f"  {i+1}. {ngram} = '{text}' appears {len(locations)} times in pages {page_list}")
    
    # Find repeated 4-grams
    print("\n=== REPEATED 4-GRAMS ACROSS PAGES ===\n")
    
    repeated_4grams = find_repeated_ngrams(pages, 4)
    sorted_4grams = sorted(repeated_4grams.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"Found {len(repeated_4grams)} unique 4-grams appearing in multiple locations\n")
    
    print("Top 15 most common 4-grams:")
    for i, (ngram, locations) in enumerate(sorted_4grams[:15]):
        text = indices_to_text(ngram)
        page_list = sorted(set([loc[0] for loc in locations]))
        print(f"  {i+1}. {ngram} = '{text}' appears {len(locations)} times in pages {page_list}")
    
    # Find 5-grams and 6-grams (these are very significant if found)
    print("\n=== LONGER REPEATED SEQUENCES ===\n")
    
    for ngram_len in [5, 6, 7, 8]:
        repeated = find_repeated_ngrams(pages, ngram_len)
        if repeated:
            sorted_repeated = sorted(repeated.items(), key=lambda x: len(x[1]), reverse=True)
            print(f"\n{ngram_len}-grams found ({len(repeated)} unique):")
            for ngram, locations in sorted_repeated[:5]:
                text = indices_to_text(ngram)
                page_list = sorted(set([loc[0] for loc in locations]))
                positions = [(p, pos) for p, pos in locations][:5]
                print(f"  '{text}' appears {len(locations)} times: {positions[:3]}...")
    
    # Look for patterns in position differences
    print("\n" + "="*70)
    print("ANALYZING POSITION PATTERNS IN REPEATED SEQUENCES")
    print("="*70 + "\n")
    
    # For repeated sequences within the same page, look at position differences
    # This might reveal key length
    
    all_position_diffs = []
    
    for ngram_len in [3, 4, 5]:
        repeated = find_repeated_ngrams(pages, ngram_len)
        
        for ngram, locations in repeated.items():
            # Group by page
            by_page = defaultdict(list)
            for page_num, pos in locations:
                by_page[page_num].append(pos)
            
            for page_num, positions in by_page.items():
                if len(positions) > 1:
                    positions.sort()
                    for i in range(len(positions) - 1):
                        diff = positions[i+1] - positions[i]
                        if diff > 0:
                            all_position_diffs.append(diff)
    
    if all_position_diffs:
        diff_counts = Counter(all_position_diffs)
        print("Most common position differences between repeated sequences:")
        for diff, count in diff_counts.most_common(20):
            if count > 2:
                print(f"  Difference of {diff}: {count} occurrences")
        
        # GCD of common differences might indicate key period
        from math import gcd
        from functools import reduce
        
        common_diffs = [d for d, c in diff_counts.most_common(10) if c > 3]
        if len(common_diffs) >= 2:
            overall_gcd = reduce(gcd, common_diffs)
            print(f"\nGCD of top differences: {overall_gcd} (potential key period)")
    
    # Analyze differences between adjacent runes
    print("\n" + "="*70)
    print("FIRST DIFFERENCE ANALYSIS")
    print("="*70 + "\n")
    
    all_first_diffs = []
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:  # Skip plaintext
            continue
        
        indices = runes_to_indices(pages[page_num])
        
        if len(indices) < 10:
            continue
        
        # Calculate first differences (between adjacent runes)
        first_diffs = [(indices[i+1] - indices[i]) % 29 for i in range(len(indices)-1)]
        all_first_diffs.extend(first_diffs)
        
        # Check for patterns
        diff_counts = Counter(first_diffs)
        most_common_diff = diff_counts.most_common(1)[0]
        
        # High frequency of single difference might indicate pattern
        if most_common_diff[1] > len(first_diffs) * 0.15:
            print(f"Page {page_num}: Most common difference = {most_common_diff[0]} "
                  f"({most_common_diff[1]}/{len(first_diffs)} = {most_common_diff[1]/len(first_diffs):.1%})")
    
    # Global first difference distribution
    print("\n\nGlobal first difference distribution:")
    global_diff_counts = Counter(all_first_diffs)
    for diff, count in global_diff_counts.most_common(10):
        print(f"  Difference {diff:2d}: {count:4d} ({count/len(all_first_diffs)*100:.1f}%)")
    
    # Analyze second differences (acceleration)
    print("\n" + "="*70)
    print("SECOND DIFFERENCE ANALYSIS")
    print("="*70 + "\n")
    
    all_second_diffs = []
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:
            continue
        
        indices = runes_to_indices(pages[page_num])
        
        if len(indices) < 10:
            continue
        
        # Calculate second differences
        first_diffs = [(indices[i+1] - indices[i]) % 29 for i in range(len(indices)-1)]
        second_diffs = [(first_diffs[i+1] - first_diffs[i]) % 29 for i in range(len(first_diffs)-1)]
        all_second_diffs.extend(second_diffs)
    
    print("Global second difference distribution:")
    second_diff_counts = Counter(all_second_diffs)
    for diff, count in second_diff_counts.most_common(10):
        print(f"  Second difference {diff:2d}: {count:4d} ({count/len(all_second_diffs)*100:.1f}%)")
    
    # Compare with plaintext (Page 57) patterns
    print("\n" + "="*70)
    print("COMPARISON WITH PLAINTEXT (Page 57)")
    print("="*70 + "\n")
    
    if 57 in pages:
        plaintext_indices = runes_to_indices(pages[57])
        
        print(f"Page 57 (Plaintext) has {len(plaintext_indices)} runes")
        
        # First differences
        pt_first_diffs = [(plaintext_indices[i+1] - plaintext_indices[i]) % 29 
                         for i in range(len(plaintext_indices)-1)]
        pt_diff_counts = Counter(pt_first_diffs)
        
        print("\nPlaintext first difference distribution:")
        for diff, count in pt_diff_counts.most_common(10):
            print(f"  Difference {diff:2d}: {count:4d} ({count/len(pt_first_diffs)*100:.1f}%)")
        
        # Trigram distribution
        pt_trigrams = Counter()
        for i in range(len(plaintext_indices) - 2):
            pt_trigrams[tuple(plaintext_indices[i:i+3])] += 1
        
        print(f"\nMost common plaintext trigrams:")
        for trigram, count in pt_trigrams.most_common(10):
            text = indices_to_text(trigram)
            print(f"  '{text}': {count}")

if __name__ == "__main__":
    main()

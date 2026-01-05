#!/usr/bin/env python3
"""
Deep Analysis: Pages that produce "THE" when combined with Page 0/54
=====================================================================

From the previous analysis, these pages produced "THE" when subtracted 
with Page 0/54:
- Page 28, 29, 31, 44, 46, 47, 48, 51, 52, 53

This is suspicious - let's investigate further.
"""

import re
import numpy as np
from collections import Counter
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

# Common English words for scoring
COMMON_WORDS = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
                'BUT', 'FROM', 'THEY', 'WILL', 'ALL', 'THERE', 'THEIR', 'AN',
                'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'SHE', 'WE', 'OR']

CICADA_WORDS = ['INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
                'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM']

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def calculate_ioc(indices):
    n = len(indices)
    if n < 2:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    numerator = np.sum(counts * (counts - 1))
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0.0

def count_english_words(text):
    """Count common English words in text"""
    text = text.upper()
    count = 0
    words_found = []
    for word in COMMON_WORDS + CICADA_WORDS:
        occurrences = text.count(word)
        if occurrences > 0:
            count += occurrences
            words_found.append(f"{word}({occurrences})")
    return count, words_found

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
            pages[page_num] = runes_only
    return pages

def analyze_the_positions(text, key_indices, target_indices):
    """Find where 'THE' appears and what the key values are at those positions"""
    text_upper = text.upper()
    
    positions = []
    start = 0
    while True:
        pos = text_upper.find('THE', start)
        if pos == -1:
            break
        
        # Get key and target values at this position
        if pos + 3 <= len(key_indices):
            key_vals = key_indices[pos:pos+3]
            tgt_vals = target_indices[pos:pos+3]
            positions.append({
                'pos': pos,
                'key': key_vals.tolist(),
                'target': tgt_vals.tolist(),
                'key_letters': indices_to_text(key_vals),
                'target_letters': indices_to_text(tgt_vals)
            })
        start = pos + 1
    
    return positions

def main():
    print("="*70)
    print("DEEP 'THE' ANALYSIS: Page 0/54 as Key")
    print("="*70)
    
    pages = load_all_pages()
    page0_idx = runes_to_indices(pages[0])
    
    # Focus on pages that showed "THE"
    interesting_pages = [28, 29, 31, 44, 46, 47, 48, 51, 52, 53]
    
    print("\n" + "="*70)
    print("DETAILED WORD ANALYSIS")
    print("="*70)
    
    for pg_num in interesting_pages:
        if pg_num not in pages:
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        min_len = min(len(page0_idx), len(pg_idx))
        
        # Subtraction (Page - Page0)
        result = (pg_idx[:min_len] - page0_idx[:min_len]) % 29
        text = indices_to_text(result)
        ioc = calculate_ioc(result)
        
        word_count, words_found = count_english_words(text)
        
        print(f"\n📄 Page {pg_num}:")
        print(f"   IoC: {ioc:.4f}")
        print(f"   Words found: {word_count} - {', '.join(words_found)}")
        print(f"   Full text: {text}")
        
        # Find THE positions
        the_positions = analyze_the_positions(text, page0_idx[:min_len], pg_idx[:min_len])
        if the_positions:
            print(f"   'THE' positions:")
            for p in the_positions:
                print(f"     Pos {p['pos']}: Key={p['key_letters']} ({p['key']}), "
                      f"Target={p['target_letters']} ({p['target']})")
    
    # Now let's check: what if we look for patterns in THE positions?
    print("\n" + "="*70)
    print("THE POSITION PATTERN ANALYSIS")
    print("="*70)
    
    all_the_data = []
    
    for pg_num in interesting_pages:
        if pg_num not in pages:
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        min_len = min(len(page0_idx), len(pg_idx))
        result = (pg_idx[:min_len] - page0_idx[:min_len]) % 29
        text = indices_to_text(result)
        
        the_positions = analyze_the_positions(text, page0_idx[:min_len], pg_idx[:min_len])
        for p in the_positions:
            all_the_data.append({
                'page': pg_num,
                'pos': p['pos'],
                'key_vals': p['key'],
                'target_vals': p['target']
            })
    
    print(f"\nTotal 'THE' occurrences found: {len(all_the_data)}")
    
    # For 'THE' to appear (T=16, H=8, E=18), we need:
    # (target - key) mod 29 = [16, 8, 18]
    # So target = key + [16, 8, 18] mod 29
    
    print("\nExpected: For 'THE' (T=16, H=8, E=18) to appear:")
    print("  If result = target - key (mod 29)")
    print("  Then target = key + [16, 8, 18] (mod 29)")
    
    print("\nVerifying THE positions:")
    for item in all_the_data[:10]:  # Show first 10
        k = item['key_vals']
        t = item['target_vals']
        expected_t = [(k[0]+16)%29, (k[1]+8)%29, (k[2]+18)%29]
        match = (t == expected_t)
        print(f"  Page {item['page']:2d}, pos {item['pos']:3d}: "
              f"key={k}, target={t}, expected={expected_t}, match={match}")
    
    # Now check: is the appearance of THE just random, or statistically significant?
    print("\n" + "="*70)
    print("STATISTICAL SIGNIFICANCE")
    print("="*70)
    
    # For random text, P(THE) ≈ (1/29)^3 ≈ 0.000041 per position
    # For 232 positions, expected ≈ 0.0095 occurrences
    
    total_positions = 0
    the_count = 0
    
    for pg_num in pages.keys():
        if pg_num in [0, 54, 57]:  # Skip duplicates and plaintext
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        min_len = min(len(page0_idx), len(pg_idx))
        
        if min_len < 10:
            continue
        
        result = (pg_idx[:min_len] - page0_idx[:min_len]) % 29
        text = indices_to_text(result)
        
        total_positions += min_len
        the_count += text.upper().count('THE')
    
    expected_random = total_positions * (1/29)**3
    print(f"\nTotal positions checked: {total_positions}")
    print(f"'THE' occurrences found: {the_count}")
    print(f"Expected by random chance: {expected_random:.2f}")
    print(f"Ratio (found/expected): {the_count/expected_random:.2f}x")
    
    if the_count > expected_random * 3:
        print("\n⚠️ THE appearances are SIGNIFICANTLY higher than random!")
        print("   This suggests Page 0/54 may be related to a key pattern.")
    else:
        print("\n   THE appearances are within random expectations.")
    
    # Let's also try: what if Page 0/54 encodes a message directly?
    print("\n" + "="*70)
    print("DIRECT DECODE ATTEMPTS ON PAGE 0/54")
    print("="*70)
    
    page0_text = indices_to_text(page0_idx)
    print(f"\nDirect transliteration: {page0_text}")
    
    # Try Page 56 formula on Page 0
    print("\n Page 56 formula applied to Page 0:")
    for offset in [0, 29, 54, 57, 58]:
        result = []
        for i, idx in enumerate(page0_idx):
            prime = PRIMES[i % 29]
            shift = (prime + offset) % 29
            result.append((idx - shift) % 29)
        result = np.array(result, dtype=np.int32)
        text = indices_to_text(result)
        ioc = calculate_ioc(result)
        word_count, words = count_english_words(text)
        print(f"  Offset {offset:2d}: IoC={ioc:.4f}, words={word_count} | {text[:50]}...")

if __name__ == "__main__":
    main()

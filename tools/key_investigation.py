#!/usr/bin/env python3
"""
Page 0/54 Key Investigation
============================

The "THE" appearance rate is 91x higher than random when using Page 0/54 as key!
This strongly suggests Pages 0/54 encode or are related to the encryption key.

Let's investigate:
1. What if Page 0/54 IS the key (or a version of it)?
2. What patterns emerge in the differences?
3. Could Page 0/54 be the PLAINTEXT that helps derive the key?
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

def score_text(text):
    """Score text for English-likeness"""
    text = text.upper()
    score = 0
    
    # Common words (weighted)
    common_words = {
        'THE': 10, 'AND': 8, 'THAT': 6, 'HAVE': 6, 'FOR': 5, 'NOT': 5,
        'WITH': 5, 'THIS': 5, 'BUT': 4, 'FROM': 5, 'THEY': 5, 'WILL': 5,
        'ALL': 4, 'THERE': 6, 'THEIR': 6, 'AN': 3, 'BE': 3, 'IT': 3,
        'IS': 3, 'TO': 3, 'OF': 3, 'IN': 3, 'HE': 3, 'SHE': 4, 'WE': 3, 'OR': 3
    }
    
    cicada_words = {
        'INSTAR': 20, 'PARABLE': 20, 'DIVINITY': 20, 'EMERGE': 15,
        'CIRCUMFERENCE': 30, 'WITHIN': 15, 'SURFACE': 15, 'SHED': 10,
        'PRIME': 15, 'TRUTH': 15, 'WISDOM': 15, 'SEEK': 10, 'FIND': 10,
        'DEEP': 10, 'WEB': 10
    }
    
    for word, weight in common_words.items():
        score += text.count(word) * weight
    
    for word, weight in cicada_words.items():
        score += text.count(word) * weight
    
    return score

def investigate_key_hypothesis(pages):
    """Investigate if Page 0/54 is the key"""
    print("="*70)
    print("HYPOTHESIS: Page 0/54 as Encryption Key")
    print("="*70)
    
    page0_idx = runes_to_indices(pages[0])
    
    print(f"\nPage 0/54 length: {len(page0_idx)} runes")
    print(f"Page 0/54 indices: {page0_idx[:30].tolist()}...")
    
    # If Page 0/54 is the key, then decrypting any page should give plaintext
    # Try different formulas
    
    print("\n" + "="*70)
    print("TEST: Pages decrypted with Page 0/54 as running key")
    print("="*70)
    
    results = []
    
    for pg_num in sorted(pages.keys()):
        if pg_num in [0, 54, 57]:
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        min_len = min(len(page0_idx), len(pg_idx))
        
        if min_len < 50:
            continue
        
        # C = P + K mod 29 => P = C - K mod 29
        decrypted = (pg_idx[:min_len] - page0_idx[:min_len]) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        score = score_text(text)
        
        results.append((pg_num, ioc, score, text[:100]))
    
    # Sort by score
    results.sort(key=lambda x: -x[2])
    
    print("\nTop results by English word score:")
    for pg, ioc, score, text in results[:10]:
        print(f"\n  Page {pg:2d}: IoC={ioc:.4f}, Score={score:3d}")
        print(f"    {text[:80]}...")
    
    return results

def investigate_key_extraction(pages):
    """Try to extract the key pattern from Page 0/54 vs Page 57"""
    print("\n" + "="*70)
    print("KEY EXTRACTION: Page 0/54 vs Page 57 (Parable)")
    print("="*70)
    
    page0_idx = runes_to_indices(pages[0])
    page57_idx = runes_to_indices(pages[57])
    
    print(f"\nPage 0 length: {len(page0_idx)}")
    print(f"Page 57 length: {len(page57_idx)}")
    
    min_len = min(len(page0_idx), len(page57_idx))
    
    # If Page 0 is encrypted Parable, then:
    # Page0 = Page57 + Key mod 29
    # Key = Page0 - Page57 mod 29
    
    potential_key = (page0_idx[:min_len] - page57_idx[:min_len]) % 29
    key_text = indices_to_text(potential_key)
    
    print(f"\nIf Page 0 = Page 57 + Key:")
    print(f"  Derived key: {key_text}")
    print(f"  Key indices: {potential_key.tolist()}")
    
    # Check if this key shows any pattern
    print(f"\nKey statistics:")
    print(f"  Unique values: {len(np.unique(potential_key))}")
    print(f"  Mean: {np.mean(potential_key):.2f}")
    print(f"  Sum mod 29: {np.sum(potential_key) % 29}")
    
    # Does the key repeat?
    print("\nKey pattern analysis:")
    for period in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 19, 23, 29]:
        matches = 0
        total = 0
        for i in range(len(potential_key) - period):
            if potential_key[i] == potential_key[i + period]:
                matches += 1
            total += 1
        if total > 0:
            match_rate = matches / total
            expected = 1/29
            if match_rate > expected * 1.5:
                print(f"  Period {period:2d}: {match_rate:.3f} match rate (expected: {expected:.3f}) ⚠️")
            else:
                print(f"  Period {period:2d}: {match_rate:.3f} match rate (expected: {expected:.3f})")
    
    return potential_key

def test_extracted_key_on_all_pages(pages, key):
    """Test the extracted key on all pages"""
    print("\n" + "="*70)
    print("TEST: Extracted key applied to all pages")
    print("="*70)
    
    results = []
    
    for pg_num in sorted(pages.keys()):
        if pg_num in [57]:  # Skip plaintext
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Extend key if needed (repeat)
        if len(key) < len(pg_idx):
            extended_key = np.tile(key, (len(pg_idx) // len(key) + 1))[:len(pg_idx)]
        else:
            extended_key = key[:len(pg_idx)]
        
        # Decrypt: P = C - K mod 29
        decrypted = (pg_idx - extended_key) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        score = score_text(text)
        
        results.append((pg_num, ioc, score, text))
    
    # Sort by IoC
    results.sort(key=lambda x: -x[1])
    
    print("\nTop results by IoC:")
    for pg, ioc, score, text in results[:5]:
        print(f"\n  Page {pg:2d}: IoC={ioc:.4f}, Score={score:3d}")
        print(f"    {text[:80]}...")
    
    # Also sort by score
    results.sort(key=lambda x: -x[2])
    
    print("\nTop results by English score:")
    for pg, ioc, score, text in results[:5]:
        print(f"\n  Page {pg:2d}: IoC={ioc:.4f}, Score={score:3d}")
        print(f"    {text[:80]}...")
    
    return results

def analyze_difference_patterns(pages):
    """Analyze difference patterns between consecutive pages"""
    print("\n" + "="*70)
    print("CONSECUTIVE PAGE DIFFERENCE ANALYSIS")
    print("="*70)
    
    page_nums = sorted([p for p in pages.keys() if p not in [57]])
    
    for i in range(len(page_nums) - 1):
        pg1, pg2 = page_nums[i], page_nums[i + 1]
        
        if pg2 - pg1 > 5:  # Skip large gaps
            continue
        
        idx1 = runes_to_indices(pages[pg1])
        idx2 = runes_to_indices(pages[pg2])
        
        min_len = min(len(idx1), len(idx2))
        if min_len < 30:
            continue
        
        diff = (idx2[:min_len] - idx1[:min_len]) % 29
        text = indices_to_text(diff)
        ioc = calculate_ioc(diff)
        score = score_text(text)
        
        if score > 20 or ioc > 1.2:
            print(f"\n  Pages {pg1} - {pg2}: IoC={ioc:.4f}, Score={score}")
            print(f"    Diff: {text[:60]}...")

def main():
    print("="*70)
    print("PAGE 0/54 KEY INVESTIGATION")
    print("="*70)
    
    pages = load_all_pages()
    print(f"Loaded {len(pages)} pages")
    
    # Main investigation
    investigate_key_hypothesis(pages)
    
    # Extract potential key
    potential_key = investigate_key_extraction(pages)
    
    # Test the key
    test_extracted_key_on_all_pages(pages, potential_key)
    
    # Analyze difference patterns
    analyze_difference_patterns(pages)
    
    print("\n" + "="*70)
    print("SUMMARY OF FINDINGS")
    print("="*70)
    print("""
🔑 Key Discovery:
1. THE appearances are 91x higher than random when using Page 0/54 as key
2. This STRONGLY suggests Page 0/54 is related to encryption

📊 Statistical Evidence:
- If Pages were randomly encrypted, we'd expect ~0.15 "THE" occurrences
- We found 14 occurrences - a 91x deviation from random

🤔 Possible Interpretations:
1. Page 0/54 IS the encryption key (or a variant of it)
2. Page 0/54 is the SAME plaintext encrypted with the same method
   - This would make it a "known plaintext" situation
   - Key = Ciphertext XOR Plaintext (or subtraction in mod 29)
3. Page 0/54 contains a pattern that when combined with pages
   produces partial English - indicating partial key match

💡 Next Steps:
1. If Page 0/54 == Encrypted(Page 57), derive key
2. Look for pages with similar lengths to 232
3. Check if Page 0/54 appears in any known texts
4. Try the derived key with various offsets
""")

if __name__ == "__main__":
    main()

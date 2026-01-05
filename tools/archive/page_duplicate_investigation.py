#!/usr/bin/env python3
"""
Page 0/54 Duplicate Deep Investigation
======================================

Pages 0 and 54 of the Liber Primus are IDENTICAL - 232 runes each.
This is clearly deliberate. Let's investigate why.

Key Questions:
1. Why 54 pages apart? (58 total, so 54 = 58 - 4)
2. What are the pages around them?
3. Is there a pattern in page distances?
4. Could one be the key to decrypt the other (or other pages)?
"""

import re
import numpy as np
from collections import Counter
from pathlib import Path

# =============================================================================
# RUNE SYSTEM
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

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

# =============================================================================
# LOAD DATA
# =============================================================================
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

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================
def analyze_page_structure(pages):
    """Analyze the overall page structure"""
    print("="*70)
    print("PAGE STRUCTURE ANALYSIS")
    print("="*70)
    
    # Page lengths
    print("\n📊 Page Lengths:")
    for pg_num in sorted(pages.keys()):
        runes = pages[pg_num]
        length = len(runes)
        ioc = calculate_ioc(runes_to_indices(runes))
        print(f"  Page {pg_num:2d}: {length:4d} runes, IoC: {ioc:.4f}")
    
    # Pages with same length
    print("\n📏 Pages with Same Length:")
    length_groups = {}
    for pg_num, runes in pages.items():
        l = len(runes)
        if l not in length_groups:
            length_groups[l] = []
        length_groups[l].append(pg_num)
    
    for length, pgs in sorted(length_groups.items(), key=lambda x: len(x[1]), reverse=True):
        if len(pgs) > 1:
            print(f"  Length {length}: Pages {pgs}")

def find_duplicate_content(pages):
    """Find pages with identical or similar content"""
    print("\n" + "="*70)
    print("DUPLICATE CONTENT ANALYSIS")
    print("="*70)
    
    page_nums = sorted(pages.keys())
    duplicates = []
    
    for i, pg1 in enumerate(page_nums):
        for pg2 in page_nums[i+1:]:
            if pages[pg1] == pages[pg2]:
                duplicates.append((pg1, pg2, 'IDENTICAL'))
            else:
                # Check similarity
                runes1 = pages[pg1]
                runes2 = pages[pg2]
                min_len = min(len(runes1), len(runes2))
                if min_len > 0:
                    matches = sum(1 for a, b in zip(runes1[:min_len], runes2[:min_len]) if a == b)
                    similarity = matches / min_len
                    if similarity > 0.8:
                        duplicates.append((pg1, pg2, f'{similarity*100:.1f}% similar'))
    
    print("\n🔍 Duplicate/Similar Pages:")
    for pg1, pg2, status in duplicates:
        distance = pg2 - pg1
        print(f"  Pages {pg1} and {pg2}: {status} (distance: {distance} pages)")
    
    return duplicates

def analyze_page_0_54(pages):
    """Deep analysis of Pages 0 and 54"""
    print("\n" + "="*70)
    print("DEEP ANALYSIS: PAGES 0 AND 54")
    print("="*70)
    
    if 0 not in pages or 54 not in pages:
        print("ERROR: Pages 0 or 54 not found!")
        return
    
    page0 = pages[0]
    page54 = pages[54]
    
    print(f"\n📄 Page 0 Content ({len(page0)} runes):")
    print(f"   {page0[:80]}...")
    
    print(f"\n📄 Page 54 Content ({len(page54)} runes):")
    print(f"   {page54[:80]}...")
    
    # Convert to indices
    idx0 = runes_to_indices(page0)
    idx54 = runes_to_indices(page54)
    
    print(f"\n✓ Identical: {np.array_equal(idx0, idx54)}")
    
    # Numerical analysis
    print("\n📐 Numerical Properties:")
    print(f"  Sum of indices (Page 0):  {np.sum(idx0)}")
    print(f"  Mean index:               {np.mean(idx0):.2f}")
    print(f"  Gematria sum:             {sum(PRIMES[i] for i in idx0)}")
    print(f"  Gematria sum mod 29:      {sum(PRIMES[i] for i in idx0) % 29}")
    
    # Distance analysis
    print("\n📏 Distance Analysis:")
    print(f"  Page separation:          54 pages")
    print(f"  Total pages in LP:        58 (0-57)")
    print(f"  Distance from end (54):   {57 - 54} = 3 pages")
    print(f"  Distance from end (0):    57 pages")
    print(f"  54 = 58 - 4")
    print(f"  54 = 2 × 27")
    print(f"  54 = 2 × 3³")
    
    # Check if 54 has any prime significance
    print("\n🔢 Number 54 Properties:")
    print(f"  54 in binary: {bin(54)}")
    print(f"  54 mod 29:    {54 % 29}")
    print(f"  54 / 29:      {54 / 29:.4f}")
    print(f"  Factors:      2, 3, 6, 9, 18, 27, 54")
    
    return idx0, idx54

def analyze_surrounding_pages(pages, target_pages=[0, 54]):
    """Analyze pages around the duplicates"""
    print("\n" + "="*70)
    print("SURROUNDING PAGES ANALYSIS")
    print("="*70)
    
    for target in target_pages:
        print(f"\n📑 Context around Page {target}:")
        for offset in [-2, -1, 0, 1, 2]:
            pg = target + offset
            if pg in pages:
                runes = pages[pg]
                idx = runes_to_indices(runes)
                ioc = calculate_ioc(idx)
                marker = "◀ TARGET" if offset == 0 else ""
                print(f"  Page {pg:2d}: {len(runes):4d} runes, IoC={ioc:.4f}, "
                      f"sum mod 29={np.sum(idx) % 29:2d} {marker}")
            else:
                marker = "◀ TARGET (empty)" if offset == 0 else "(empty)"
                print(f"  Page {pg:2d}: {marker}")

def test_page_as_key(pages, key_page, target_page):
    """Try using one page as a key to decrypt another"""
    print(f"\n🔑 Testing Page {key_page} as key for Page {target_page}:")
    
    if key_page not in pages or target_page not in pages:
        print("  ERROR: Page not found")
        return None
    
    key_idx = runes_to_indices(pages[key_page])
    target_idx = runes_to_indices(pages[target_page])
    
    min_len = min(len(key_idx), len(target_idx))
    
    # Subtraction
    result_sub = (target_idx[:min_len] - key_idx[:min_len]) % 29
    text_sub = indices_to_text(result_sub)
    ioc_sub = calculate_ioc(result_sub)
    
    # Addition
    result_add = (target_idx[:min_len] + key_idx[:min_len]) % 29
    text_add = indices_to_text(result_add)
    ioc_add = calculate_ioc(result_add)
    
    # XOR-like (but mod 29)
    result_xor = target_idx[:min_len] ^ key_idx[:min_len]
    result_xor = result_xor % 29  # Ensure valid range
    text_xor = indices_to_text(result_xor)
    ioc_xor = calculate_ioc(result_xor)
    
    print(f"  Subtraction: IoC={ioc_sub:.4f} | {text_sub[:60]}...")
    print(f"  Addition:    IoC={ioc_add:.4f} | {text_add[:60]}...")
    print(f"  XOR mod 29:  IoC={ioc_xor:.4f} | {text_xor[:60]}...")
    
    return {
        'sub': (result_sub, ioc_sub, text_sub),
        'add': (result_add, ioc_add, text_add),
        'xor': (result_xor, ioc_xor, text_xor)
    }

def cross_page_operations(pages):
    """Try various operations between pages"""
    print("\n" + "="*70)
    print("CROSS-PAGE OPERATIONS")
    print("="*70)
    
    # Test Page 0/54 with various other pages
    page0_idx = runes_to_indices(pages[0])
    
    print("\n🔄 Using Page 0/54 as key against other pages:")
    
    interesting_results = []
    
    for pg_num in sorted(pages.keys()):
        if pg_num in [0, 54, 57]:  # Skip self and plaintext
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        min_len = min(len(page0_idx), len(pg_idx))
        
        if min_len < 50:  # Skip very short pages
            continue
        
        # Subtraction
        result = (pg_idx[:min_len] - page0_idx[:min_len]) % 29
        ioc = calculate_ioc(result)
        text = indices_to_text(result)
        
        # Check for English patterns
        has_the = 'THE' in text.upper()
        has_and = 'AND' in text.upper()
        score = (1 if has_the else 0) + (1 if has_and else 0) + (ioc - 1.0) * 5
        
        if ioc > 1.1 or has_the or has_and:
            interesting_results.append((pg_num, ioc, text[:50], has_the, has_and))
    
    if interesting_results:
        print("\n  ⚠️ Interesting results (IoC > 1.1 or contains THE/AND):")
        for pg, ioc, text, has_the, has_and in sorted(interesting_results, key=lambda x: -x[1]):
            markers = []
            if has_the: markers.append("THE")
            if has_and: markers.append("AND")
            print(f"  Page {pg:2d}: IoC={ioc:.4f} [{', '.join(markers) if markers else '-'}] | {text}...")
    else:
        print("\n  No highly interesting results found.")

def analyze_page_57_as_key(pages):
    """Use the Parable (Page 57) as key"""
    print("\n" + "="*70)
    print("PAGE 57 (PARABLE) AS KEY")
    print("="*70)
    
    page57 = pages.get(57)
    if not page57:
        print("ERROR: Page 57 not found")
        return
    
    page57_idx = runes_to_indices(page57)
    print(f"\nPage 57 length: {len(page57_idx)} runes")
    print(f"Decoded: PARABLE LIKE THE INSTAR TUNNELING TO THE SURFACE...")
    
    print("\n🔑 Testing Page 57 as running key:")
    
    for pg_num in [0, 15, 27, 40, 54]:
        if pg_num not in pages:
            continue
        
        pg_idx = runes_to_indices(pages[pg_num])
        min_len = min(len(page57_idx), len(pg_idx))
        
        # Since Page 57 is plaintext, its indices ARE the plaintext
        # If C = P + K mod 29, then P = C - K mod 29
        # Here K = Page 57 indices
        result = (pg_idx[:min_len] - page57_idx[:min_len]) % 29
        ioc = calculate_ioc(result)
        text = indices_to_text(result)
        
        print(f"\n  Page {pg_num}: IoC={ioc:.4f}")
        print(f"    {text[:80]}...")

def look_for_patterns_at_distance_54(pages):
    """Look for any patterns at distance 54"""
    print("\n" + "="*70)
    print("PATTERNS AT DISTANCE 54")
    print("="*70)
    
    print("\n📊 Checking page pairs with distance 54:")
    
    for pg1 in sorted(pages.keys()):
        pg2 = pg1 + 54
        if pg2 in pages:
            runes1 = pages[pg1]
            runes2 = pages[pg2]
            
            idx1 = runes_to_indices(runes1)
            idx2 = runes_to_indices(runes2)
            
            identical = np.array_equal(idx1, idx2)
            min_len = min(len(idx1), len(idx2))
            
            if min_len > 0:
                diff = (idx2[:min_len] - idx1[:min_len]) % 29
                diff_unique = len(np.unique(diff))
                diff_ioc = calculate_ioc(diff)
                
                print(f"  Pages {pg1} → {pg2}:")
                print(f"    Identical: {identical}")
                print(f"    Diff unique values: {diff_unique}/29")
                print(f"    Diff IoC: {diff_ioc:.4f}")

def main():
    print("="*70)
    print("PAGE 0/54 DUPLICATE DEEP INVESTIGATION")
    print("="*70)
    
    # Load data
    print("\nLoading pages...")
    pages = load_all_pages()
    print(f"Loaded {len(pages)} pages: {sorted(pages.keys())}")
    
    # Run all analyses
    analyze_page_structure(pages)
    find_duplicate_content(pages)
    analyze_page_0_54(pages)
    analyze_surrounding_pages(pages)
    
    # Cross-page key tests
    print("\n" + "="*70)
    print("KEY DERIVATION TESTS")
    print("="*70)
    
    # Test Page 0/54 as key for other pages
    cross_page_operations(pages)
    
    # Test Page 57 as key
    analyze_page_57_as_key(pages)
    
    # Look for distance-54 patterns
    look_for_patterns_at_distance_54(pages)
    
    # Final insights
    print("\n" + "="*70)
    print("CONCLUSIONS")
    print("="*70)
    print("""
🔍 Key Observations:
1. Pages 0 and 54 are EXACTLY identical (232 runes each)
2. This is the ONLY duplicate pair in the entire Liber Primus
3. Distance of 54 pages = 58 - 4 (4 pages from the end)
4. 54 = 2 × 27 = 2 × 3³

🤔 Possible Interpretations:
- Bookend structure (beginning echoes near-end)
- Same plaintext encrypted with same key
- Reference marker for navigation
- The number 54 may be significant (key offset?)
- Could indicate cyclic structure

💡 Suggested Next Steps:
- Check if Page 0/54 content appears anywhere else (books, texts)
- Look for pages that when combined with 0/54 produce high IoC
- Consider 54 as a numeric key component
- Check if removing Page 0/54 changes the overall pattern
""")

if __name__ == "__main__":
    main()

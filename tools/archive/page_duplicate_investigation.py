#!/usr/bin/env python3
"""
Investigate the Page 0 = Page 54 finding!

This is a major discovery - if these pages are identical, it tells us:
1. They might use the same key
2. Or they might be the same encrypted plaintext
3. Or it's intentional (a marker/signature)
"""

import re
import numpy as np

# =============================================================================
# RUNE DATA
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
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
    return [RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX]

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def main():
    pages = load_pages()
    
    print("="*70)
    print("INVESTIGATING PAGE 0 vs PAGE 54")
    print("="*70)
    
    page0 = pages[0]
    page54 = pages[54]
    
    print(f"\nPage 0: {len(page0)} runes")
    print(f"Page 54: {len(page54)} runes")
    
    # Check if they're identical
    if page0 == page54:
        print("\n*** PAGES 0 AND 54 ARE IDENTICAL! ***")
    else:
        print(f"\nPages are NOT identical")
        
        # Find differences
        min_len = min(len(page0), len(page54))
        diffs = []
        for i in range(min_len):
            if page0[i] != page54[i]:
                diffs.append((i, page0[i], page54[i]))
        
        print(f"Differences in first {min_len} positions: {len(diffs)}")
        if diffs:
            for pos, r0, r54 in diffs[:20]:
                print(f"  Position {pos}: Page0='{r0}', Page54='{r54}'")
    
    # Display both pages side by side
    print("\n" + "="*70)
    print("PAGE 0 RAW")
    print("="*70)
    print(page0[:100])
    
    print("\n" + "="*70)
    print("PAGE 54 RAW")
    print("="*70)
    print(page54[:100])
    
    # Check for other duplicate pages
    print("\n" + "="*70)
    print("SEARCHING FOR OTHER DUPLICATE PAGES")
    print("="*70 + "\n")
    
    page_nums = sorted(pages.keys())
    duplicates = []
    
    for i, p1 in enumerate(page_nums):
        for p2 in page_nums[i+1:]:
            if pages[p1] == pages[p2]:
                duplicates.append((p1, p2))
    
    if duplicates:
        print("Found duplicate pages:")
        for p1, p2 in duplicates:
            print(f"  Page {p1} = Page {p2} (both {len(pages[p1])} runes)")
    else:
        print("No exact duplicate pages found")
    
    # Check for similar pages (high overlap)
    print("\n" + "="*70)
    print("SEARCHING FOR SIMILAR PAGES (high overlap)")
    print("="*70 + "\n")
    
    for i, p1 in enumerate(page_nums):
        for p2 in page_nums[i+1:]:
            runes1 = pages[p1]
            runes2 = pages[p2]
            
            min_len = min(len(runes1), len(runes2))
            if min_len < 20:
                continue
            
            matches = sum(1 for k in range(min_len) if runes1[k] == runes2[k])
            overlap_pct = matches / min_len
            
            if overlap_pct > 0.5:
                print(f"Pages {p1} and {p2}: {matches}/{min_len} = {overlap_pct:.1%} overlap")
    
    # If pages 0 and 54 are identical, what does XOR reveal?
    print("\n" + "="*70)
    print("XOR ANALYSIS OF IDENTICAL/SIMILAR PAGES")
    print("="*70 + "\n")
    
    indices0 = runes_to_indices(page0)
    indices54 = runes_to_indices(page54)
    
    min_len = min(len(indices0), len(indices54))
    
    # XOR same positions
    xor_result = [(indices0[i] ^ indices54[i]) for i in range(min_len)]
    
    print(f"XOR of Page 0 and Page 54 (first 50 values):")
    print(xor_result[:50])
    
    if all(x == 0 for x in xor_result):
        print("\nAll XOR values are 0 - pages are IDENTICAL!")
    else:
        non_zero = [i for i, x in enumerate(xor_result) if x != 0]
        print(f"\nNon-zero XOR positions: {non_zero}")
    
    # Now let's look at what this means for solving
    print("\n" + "="*70)
    print("IMPLICATIONS FOR SOLVING")
    print("="*70 + "\n")
    
    if page0 == page54:
        print("If Pages 0 and 54 are identical, this suggests:")
        print("1. The same plaintext encrypted with the same key")
        print("2. A deliberate structural marker")
        print("3. Possibly the beginning and end share a theme")
        print()
        print("Try: Decrypt Page 0/54 with 'PARABLE' key since it follows Page 57")
        print("Try: Check if 54 = 58 - 4 = related to 0 in some cyclic way")
    
    # XOR Page 0 with Page 57 (the plaintext)
    print("\n" + "="*70)
    print("XOR PAGE 0/54 WITH PAGE 57 (PLAINTEXT)")
    print("="*70 + "\n")
    
    if 57 in pages:
        indices57 = runes_to_indices(pages[57])
        
        min_len = min(len(indices0), len(indices57))
        
        xor_0_57 = [(indices0[i] ^ indices57[i]) % 29 for i in range(min_len)]
        
        print(f"XOR of Page 0 and Page 57 (plaintext):")
        print(f"First 30: {xor_0_57[:30]}")
        print(f"As text: {indices_to_text(xor_0_57[:30])}")
        
        # Is this a potential key?
        print(f"\nIf Page 57 is the key for Page 0:")
        # Key = Cipher - Plaintext, so Plaintext = Cipher - Key
        # If Key = Page 57, then Plaintext = Page 0 - Page 57
        
        decrypted = [(indices0[i] - indices57[i]) % 29 for i in range(min_len)]
        print(f"Page 0 - Page 57 mod 29: {indices_to_text(decrypted)}")
        
        decrypted = [(indices0[i] + indices57[i]) % 29 for i in range(min_len)]
        print(f"Page 0 + Page 57 mod 29: {indices_to_text(decrypted)}")

if __name__ == "__main__":
    main()

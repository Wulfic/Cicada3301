#!/usr/bin/env python3
"""
CRITICAL INVESTIGATION: Page 43

Page 43 with Page 0 as key shows IoC=2.0632 (higher than English!)
This might be a breakthrough. Let's examine in detail.

Also investigating:
- Page 40 with prime shift + "IT" key
- Page 51 with "AN" key
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

def indices_to_runes(indices):
    return ''.join(RUNES[int(i) % 29] for i in indices)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def main():
    print("="*70)
    print("CRITICAL INVESTIGATION: PAGE 43")
    print("="*70)
    
    pages = load_pages()
    
    # =========================================================================
    # PAGE 43 DEEP DIVE
    # =========================================================================
    print("\n" + "="*70)
    print("PAGE 43 ANALYSIS")
    print("="*70 + "\n")
    
    page43 = pages[43]
    page0 = pages[0]
    
    print(f"Page 43 raw runes: {page43}")
    print(f"Page 43 length: {len(page43)}")
    print()
    
    cipher43 = runes_to_indices(page43)
    key0 = runes_to_indices(page0)
    
    print(f"Page 43 indices: {list(cipher43)}")
    print()
    
    # Calculate IoC of original
    ioc_original = calculate_ioc(cipher43)
    print(f"Original IoC: {ioc_original:.4f}")
    
    # Frequency of original
    freq = Counter(cipher43)
    print(f"Frequency distribution:")
    for idx, count in sorted(freq.items(), key=lambda x: -x[1]):
        print(f"  {IDX_TO_LETTER[idx]:3s}: {count}")
    
    # Try Page 0 as key
    n = len(cipher43)
    key = np.array([key0[i % len(key0)] for i in range(n)])
    
    print("\n" + "-"*50)
    print("Using Page 0 as key:")
    print("-"*50 + "\n")
    
    # Addition
    decrypted_add = (cipher43 + key) % 29
    text_add = indices_to_text(decrypted_add)
    ioc_add = calculate_ioc(decrypted_add)
    
    print(f"Addition (cipher + key) mod 29:")
    print(f"  IoC: {ioc_add:.4f}")
    print(f"  Text: {text_add}")
    print(f"  Runes: {indices_to_runes(decrypted_add)}")
    
    # Subtraction
    decrypted_sub = (cipher43 - key) % 29
    text_sub = indices_to_text(decrypted_sub)
    ioc_sub = calculate_ioc(decrypted_sub)
    
    print(f"\nSubtraction (cipher - key) mod 29:")
    print(f"  IoC: {ioc_sub:.4f}")
    print(f"  Text: {text_sub}")
    print(f"  Runes: {indices_to_runes(decrypted_sub)}")
    
    # Step-by-step for high IoC result
    if ioc_add > 1.5:
        print("\n" + "-"*50)
        print("HIGH IoC DETECTED - Step-by-step analysis:")
        print("-"*50 + "\n")
        
        for i in range(n):
            c = cipher43[i]
            k = key[i]
            p = decrypted_add[i]
            print(f"pos={i:2d}: cipher={c:2d} ({IDX_TO_LETTER[c]:3s}) + key={k:2d} ({IDX_TO_LETTER[k]:3s}) = {p:2d} ({IDX_TO_LETTER[p]:3s})")
        
        print(f"\nFrequency of decrypted:")
        freq_dec = Counter(decrypted_add)
        for idx, count in sorted(freq_dec.items(), key=lambda x: -x[1]):
            print(f"  {IDX_TO_LETTER[idx]:3s}: {count}")
    
    # =========================================================================
    # Check if Page 43 is related to Page 56 (solved page)
    # =========================================================================
    print("\n" + "="*70)
    print("PAGE 43 vs PAGE 56 RELATIONSHIP")
    print("="*70 + "\n")
    
    page56 = pages[56]
    cipher56 = runes_to_indices(page56)
    
    print(f"Page 56 length: {len(cipher56)}")
    print(f"Page 43 length: {len(cipher43)}")
    
    if len(cipher43) <= len(cipher56):
        # Use Page 56 as key
        key56 = np.array([cipher56[i % len(cipher56)] for i in range(n)])
        
        decrypted = (cipher43 - key56) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        print(f"\nUsing Page 56 as key (subtraction):")
        print(f"  IoC: {ioc:.4f}")
        print(f"  Text: {text}")
        
        decrypted = (cipher43 + key56) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        print(f"\nUsing Page 56 as key (addition):")
        print(f"  IoC: {ioc:.4f}")
        print(f"  Text: {text}")
    
    # =========================================================================
    # Try XOR and other operations
    # =========================================================================
    print("\n" + "="*70)
    print("OTHER OPERATIONS ON PAGE 43")
    print("="*70 + "\n")
    
    # XOR with Page 0
    decrypted_xor = cipher43 ^ key
    decrypted_xor = decrypted_xor % 29
    text_xor = indices_to_text(decrypted_xor)
    ioc_xor = calculate_ioc(decrypted_xor)
    
    print(f"XOR with Page 0:")
    print(f"  IoC: {ioc_xor:.4f}")
    print(f"  Text: {text_xor}")
    
    # Try all simple shifts
    print("\nSimple shift analysis:")
    best_shift = None
    for shift in range(29):
        decrypted = (cipher43 - shift) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        if 'THE' in text or ioc > 1.5:
            print(f"  Shift {shift:2d}: IoC={ioc:.4f}, {text[:40]}")
        
        if best_shift is None or ioc > best_shift[0]:
            best_shift = (ioc, shift, text)
    
    print(f"\nBest shift: {best_shift[1]} with IoC={best_shift[0]:.4f}")
    print(f"  {best_shift[2]}")
    
    # =========================================================================
    # Analyze what makes Page 43 special
    # =========================================================================
    print("\n" + "="*70)
    print("WHAT MAKES PAGE 43 SPECIAL?")
    print("="*70 + "\n")
    
    print(f"Page 43 has only {len(cipher43)} runes - it's VERY SHORT.")
    print(f"Page 0 has {len(key0)} runes.")
    
    # Check if Page 43 is a subset of other pages
    page43_str = pages[43]
    for pn in sorted(pages.keys()):
        if pn == 43:
            continue
        if page43_str in pages[pn]:
            print(f"Page 43 is contained in Page {pn}!")
    
    # Check pattern
    print("\nRepeating pattern check:")
    for period in range(1, len(cipher43)//2 + 1):
        matches = 0
        for i in range(len(cipher43) - period):
            if cipher43[i] == cipher43[i + period]:
                matches += 1
        ratio = matches / (len(cipher43) - period)
        if ratio > 0.3:
            print(f"  Period {period}: {ratio:.2%} repetition")
    
    # =========================================================================
    # PAGE 40 INVESTIGATION
    # =========================================================================
    print("\n" + "="*70)
    print("PAGE 40 WITH PRIME SHIFT + 'IT' KEY")
    print("="*70 + "\n")
    
    page40 = pages[40]
    cipher40 = runes_to_indices(page40)
    n40 = len(cipher40)
    
    print(f"Page 40: {n40} runes")
    
    # First apply prime shift
    prime_shift = np.array([PRIMES[i % 29] % 29 for i in range(n40)])
    intermediate = (cipher40 - prime_shift) % 29
    
    print(f"\nAfter prime shift:")
    print(f"  {indices_to_text(intermediate)[:60]}")
    print(f"  IoC: {calculate_ioc(intermediate):.4f}")
    
    # Then apply "IT" Vigenère key
    # I=10, T=16
    it_key = np.array([(10, 16)[i % 2] for i in range(n40)])
    
    decrypted = (intermediate - it_key) % 29
    text = indices_to_text(decrypted)
    ioc = calculate_ioc(decrypted)
    
    print(f"\nAfter 'IT' Vigenère:")
    print(f"  {text}")
    print(f"  IoC: {ioc:.4f}")
    
    # Find words
    text_upper = text.upper()
    for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'NOT', 'WE', 'AN', 'HE', 'AS', 'AT']:
        pos = text_upper.find(word)
        while pos >= 0:
            print(f"  Found '{word}' at position {pos}")
            pos = text_upper.find(word, pos + 1)
    
    # =========================================================================
    # Check all short pages (might be simpler)
    # =========================================================================
    print("\n" + "="*70)
    print("SHORT PAGES ANALYSIS (< 50 runes)")
    print("="*70 + "\n")
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        if len(cipher) > 50:
            continue
        
        ioc = calculate_ioc(cipher)
        
        print(f"\nPage {page_num}: {len(cipher)} runes, IoC={ioc:.4f}")
        print(f"  Runes: {pages[page_num]}")
        print(f"  As text: {indices_to_text(cipher)}")
        
        # Try simple shifts
        best = None
        for shift in range(29):
            dec = (cipher - shift) % 29
            text = indices_to_text(dec)
            score = sum(1 for w in ['THE', 'AND', 'IS'] if w in text.upper())
            if score > 0:
                print(f"    Shift {shift}: {text} (words={score})")
            if best is None or score > best[0]:
                best = (score, shift, text)

if __name__ == "__main__":
    main()

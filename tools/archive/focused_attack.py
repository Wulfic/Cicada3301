#!/usr/bin/env python3
"""
Focused Attack on Liber Primus

Based on all our analysis:
1. IoC ~1.0 = flat distribution = OTP-like cipher
2. Page 56 = Prime + 57 shift works
3. Page 57 = Plaintext "PARABLE..."
4. Community tested OEIS, Vigenère, simple running key - no success

New ideas to test:
1. PROGRESSIVE KEY: Each page uses a different offset/formula based on page number
2. INTER-PAGE KEY: Previous page's content is the key for next page
3. GEMATRIA SUM KEY: The gematria sum of previous page determines the shift
4. REVERSE ENGINEERING: What key would produce common English words at known positions?
"""

import re
import numpy as np
from collections import Counter
from itertools import combinations

# =============================================================================
# RUNE DATA
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

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

def text_to_indices(text):
    """Convert letter text to indices, handling digraphs"""
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        found = False
        for digraph in ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA']:
            if text[i:i+2] == digraph:
                indices.append(LETTER_TO_IDX[digraph])
                i += 2
                found = True
                break
        if not found:
            if text[i] in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[text[i]])
                i += 1
            else:
                i += 1
    return np.array(indices, dtype=np.int32)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def gematria_sum(indices):
    """Calculate the gematria sum (prime values) of indices"""
    return sum(PRIMES[int(i)] for i in indices)

ENGLISH_STARTS = [
    'THE', 'AND', 'AN', 'A', 'IN', 'OF', 'TO', 'IT', 'IS', 'I',
    'PARABLE', 'INSTAR', 'LIKE', 'WISDOM', 'TRUTH', 'DIVINITY', 'EMERGE',
    'WE', 'YOU', 'THEY', 'HE', 'SHE', 'AS', 'BE', 'FOR', 'THIS', 'THAT'
]

def main():
    print("="*70)
    print("FOCUSED LIBER PRIMUS ATTACK")
    print("="*70)
    
    pages = load_pages()
    
    # Calculate gematria sums for each page
    print("\n=== GEMATRIA SUMS PER PAGE ===\n")
    
    page_sums = {}
    for page_num in sorted(pages.keys()):
        indices = runes_to_indices(pages[page_num])
        gem_sum = gematria_sum(indices)
        page_sums[page_num] = gem_sum
        print(f"Page {page_num:2d}: {len(indices):3d} runes, gematria sum = {gem_sum:6d}, sum mod 29 = {gem_sum % 29:2d}")
    
    # Test IDEA 1: Inter-page keys
    print("\n" + "="*70)
    print("IDEA 1: Previous page as key for next page")
    print("="*70 + "\n")
    
    sorted_pages = sorted(pages.keys())
    
    for i, page_num in enumerate(sorted_pages[1:], 1):
        if page_num == 57:
            continue
        
        prev_page_num = sorted_pages[i-1]
        if prev_page_num not in pages:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        key = runes_to_indices(pages[prev_page_num])
        
        n = min(len(cipher), len(key))
        if n < 20:
            continue
        
        # Try subtraction
        decrypted = (cipher[:n] - key[:n]) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        # Count English words
        found_words = [w for w in ENGLISH_STARTS if w in text.upper()[:60]]
        
        if len(found_words) > 2 or ioc > 1.2:
            print(f"Page {page_num} (key=Page {prev_page_num}): IoC={ioc:.4f}")
            print(f"  {text[:60]}")
            if found_words:
                print(f"  Found: {', '.join(found_words)}")
            print()
    
    # Test IDEA 2: Gematria sum of previous page as offset
    print("\n" + "="*70)
    print("IDEA 2: Gematria sum of previous page as shift offset")
    print("="*70 + "\n")
    
    results = []
    
    for i, page_num in enumerate(sorted_pages[1:], 1):
        if page_num in [56, 57]:
            continue
        
        prev_page_num = sorted_pages[i-1]
        if prev_page_num not in page_sums:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        # Try gematria sum mod 29 as shift
        shift = page_sums[prev_page_num] % 29
        
        decrypted = (cipher - shift) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        found_words = [w for w in ENGLISH_STARTS if w in text.upper()[:60]]
        
        if len(found_words) > 2 or ioc > 1.2:
            print(f"Page {page_num} (shift from Page {prev_page_num} sum = {shift}): IoC={ioc:.4f}")
            print(f"  {text[:60]}")
            if found_words:
                print(f"  Found: {', '.join(found_words)}")
            print()
        
        results.append((ioc + len(found_words)*0.1, page_num, shift, text[:60], ioc))
    
    # Test IDEA 3: Page number as key formula
    print("\n" + "="*70)
    print("IDEA 3: Page-number-based formulas")
    print("="*70 + "\n")
    
    # Various formulas based on page number
    formulas = [
        ("pg mod 29", lambda pg: pg % 29),
        ("(pg + 1) mod 29", lambda pg: (pg + 1) % 29),
        ("(58 - pg) mod 29", lambda pg: (58 - pg) % 29),
        ("pg^2 mod 29", lambda pg: (pg * pg) % 29),
        ("prime[pg mod 29]", lambda pg: PRIMES[pg % 29]),
        ("prime[pg mod 29] mod 29", lambda pg: PRIMES[pg % 29] % 29),
        ("(pg * 7) mod 29", lambda pg: (pg * 7) % 29),  # 7 is a common multiplier
        ("(pg * 11) mod 29", lambda pg: (pg * 11) % 29),
    ]
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        for formula_name, formula in formulas:
            # Apply as position-dependent shift
            decrypted = np.array([(cipher[i] - formula(i + page_num)) % 29 for i in range(n)])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            found_words = [w for w in ENGLISH_STARTS if w in text.upper()[:60]]
            
            score = ioc + len(found_words)*0.2
            results.append((score, page_num, formula_name, text[:60], ioc, found_words))
    
    # Sort and display best
    results.sort(reverse=True)
    print("Top 10 page-formula results:\n")
    for score, page, formula, text, ioc, found in results[:10]:
        print(f"Page {page:2d}: {formula}, IoC={ioc:.4f}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Test IDEA 4: REVERSE ENGINEERING - what key produces common starts?
    print("\n" + "="*70)
    print("IDEA 4: Reverse engineering - find keys that produce English starts")
    print("="*70 + "\n")
    
    # For each page, calculate what key would make it start with THE, AND, etc.
    for page_num in [0, 15, 27, 28, 29, 30, 31, 40, 41, 42, 45, 46, 47, 48, 49]:
        if page_num not in pages:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        
        print(f"Page {page_num}: Required keys for English starts")
        
        for start in ['THE', 'AND', 'PARABLE', 'INSTAR']:
            target = text_to_indices(start)
            if len(target) > len(cipher):
                continue
            
            # Calculate required key: K = C - P mod 29
            required_key = (cipher[:len(target)] - target) % 29
            key_text = indices_to_text(required_key)
            key_primes = [PRIMES[int(k)] for k in required_key]
            
            print(f"  For '{start}': key = {required_key} ({key_text}), primes = {key_primes}")
        print()
    
    # Test IDEA 5: Self-referential cipher (ciphertext gematria determines shift)
    print("\n" + "="*70)
    print("IDEA 5: Self-referential - cipher rune's gematria as shift")
    print("="*70 + "\n")
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        # Use gematria prime of cipher rune as shift
        decrypted = np.array([(cipher[i] - PRIMES[cipher[i]] % 29) % 29 for i in range(n)])
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        found_words = [w for w in ENGLISH_STARTS if w in text.upper()[:60]]
        
        score = ioc + len(found_words)*0.2
        results.append((score, page_num, text[:60], ioc, found_words))
    
    results.sort(reverse=True)
    print("Top 10 self-referential results:\n")
    for score, page, text, ioc, found in results[:10]:
        print(f"Page {page:2d}: IoC={ioc:.4f}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Test IDEA 6: Combined prime stream with page offset
    print("\n" + "="*70)
    print("IDEA 6: Prime stream with page-specific offset (like Page 56)")
    print("="*70 + "\n")
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        best_for_page = None
        
        for offset in range(100):  # Test offsets 0-99
            # Apply Page 56 formula with different offsets
            decrypted = np.array([(cipher[i] - PRIMES[i % 29] - offset) % 29 for i in range(n)])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            found_words = [w for w in ['THE', 'AND', 'IN', 'IS', 'OF', 'TO', 'INSTAR', 'PARABLE'] 
                          if w in text.upper()[:30]]
            
            score = ioc + len(found_words)*0.3
            
            if best_for_page is None or score > best_for_page[0]:
                best_for_page = (score, offset, text[:60], ioc, found_words)
        
        if best_for_page:
            score, offset, text, ioc, found = best_for_page
            results.append((score, page_num, offset, text, ioc, found))
    
    results.sort(reverse=True)
    print("Top 15 prime-offset results:\n")
    for score, page, offset, text, ioc, found in results[:15]:
        print(f"Page {page:2d} (offset={offset:2d}): IoC={ioc:.4f}, score={score:.3f}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Pattern analysis: Are there related offsets?
    print("\n=== PATTERN ANALYSIS OF BEST OFFSETS ===\n")
    
    offset_pages = {}
    for score, page, offset, text, ioc, found in results:
        if offset not in offset_pages:
            offset_pages[offset] = []
        offset_pages[offset].append(page)
    
    for offset, page_list in sorted(offset_pages.items(), key=lambda x: -len(x[1])):
        if len(page_list) > 1:
            print(f"Offset {offset:2d}: Pages {page_list}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Deep Dive into Promising Leads

Based on our analysis, the most promising results are:
1. Page 32 with cumulative-prime-sum offset=28 - shows THE, AND, OF, NOT, WE, OR, AN, HE, DO, AT
2. Page 28 with gap-11 offset=21 - shows THE, IN, IT, WE, HE, AS
3. Page 52 with gap-13 - shows THE, TO, ME, AN, HE, AT

Let's examine these in detail.
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

def main():
    print("="*70)
    print("DEEP DIVE INTO PROMISING LEADS")
    print("="*70)
    
    pages = load_pages()
    
    # =========================================================================
    # PAGE 32: Cumulative prime sum with offset 28
    # =========================================================================
    print("\n" + "="*70)
    print("PAGE 32: CUMULATIVE PRIME SUM + OFFSET 28")
    print("="*70 + "\n")
    
    page32 = pages[32]
    cipher = runes_to_indices(page32)
    n = len(cipher)
    
    print(f"Page 32: {n} runes")
    print(f"Raw runes: {page32}")
    print(f"As indices: {list(cipher)}")
    
    # Create cumulative prime sum key
    offset = 28
    prime_sum_key = []
    running_sum = 0
    for i in range(n):
        prime_sum_key.append((running_sum + offset) % 29)
        running_sum += PRIMES[i % 29]
    
    prime_sum_key = np.array(prime_sum_key, dtype=np.int32)
    
    print(f"\nKey (first 30): {list(prime_sum_key[:30])}")
    print(f"Key as text: {indices_to_text(prime_sum_key[:30])}")
    
    # Decrypt
    decrypted = (cipher - prime_sum_key) % 29
    text = indices_to_text(decrypted)
    ioc = calculate_ioc(decrypted)
    
    print(f"\nDecrypted text (IoC={ioc:.4f}):")
    print(text)
    print()
    
    # Show step by step
    print("Step-by-step (first 20 positions):")
    for i in range(min(20, n)):
        c = cipher[i]
        k = prime_sum_key[i]
        p = decrypted[i]
        print(f"  pos={i:2d}: cipher={c:2d} ({IDX_TO_LETTER[c]:3s}) - key={k:2d} = {p:2d} ({IDX_TO_LETTER[p]:3s})")
    
    # Try to find word boundaries
    print("\nLooking for readable word patterns:")
    text_upper = text.upper()
    
    # Find occurrences of common words
    words_found = []
    for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'NOT', 'ARE', 
                 'WE', 'BE', 'OR', 'AN', 'HE', 'AS', 'DO', 'AT']:
        pos = text_upper.find(word)
        while pos >= 0:
            words_found.append((pos, word))
            pos = text_upper.find(word, pos + 1)
    
    words_found.sort()
    print("Words found with positions:")
    for pos, word in words_found:
        print(f"  Position {pos:3d}: '{word}'")
    
    # =========================================================================
    # PAGE 28: Gap-11 with offset 21
    # =========================================================================
    print("\n" + "="*70)
    print("PAGE 28: GAP-11 STREAM + OFFSET 21")
    print("="*70 + "\n")
    
    page28 = pages[28]
    cipher = runes_to_indices(page28)
    n = len(cipher)
    
    print(f"Page 28: {n} runes")
    
    # Create gap-11 key
    offset = 21
    gap11_key = np.array([(i * 11 + offset) % 29 for i in range(n)], dtype=np.int32)
    
    print(f"\nKey (first 30): {list(gap11_key[:30])}")
    print(f"Key as text: {indices_to_text(gap11_key[:30])}")
    
    # Decrypt
    decrypted = (cipher - gap11_key) % 29
    text = indices_to_text(decrypted)
    ioc = calculate_ioc(decrypted)
    
    print(f"\nDecrypted text (IoC={ioc:.4f}):")
    print(text)
    print()
    
    # Find words
    words_found = []
    text_upper = text.upper()
    for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'NOT', 'ARE', 
                 'WE', 'BE', 'OR', 'AN', 'HE', 'AS', 'DO', 'AT', 'INSTAR', 'WISDOM']:
        pos = text_upper.find(word)
        while pos >= 0:
            words_found.append((pos, word))
            pos = text_upper.find(word, pos + 1)
    
    words_found.sort()
    print("Words found with positions:")
    for pos, word in words_found:
        print(f"  Position {pos:3d}: '{word}'")
    
    # =========================================================================
    # Test all pages with the cumulative prime sum method
    # =========================================================================
    print("\n" + "="*70)
    print("TESTING ALL PAGES WITH CUMULATIVE PRIME SUM")
    print("="*70 + "\n")
    
    all_results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        best = None
        
        for offset in range(29):
            # Create cumulative prime sum key
            prime_sum_key = []
            running_sum = 0
            for i in range(n):
                prime_sum_key.append((running_sum + offset) % 29)
                running_sum += PRIMES[i % 29]
            
            prime_sum_key = np.array(prime_sum_key, dtype=np.int32)
            
            decrypted = (cipher - prime_sum_key) % 29
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            
            # Count words
            text_upper = text.upper()
            word_count = sum(1 for w in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 
                                         'NOT', 'ARE', 'WE', 'BE', 'OR', 'AN', 'HE'] 
                            if w in text_upper[:60])
            
            score = ioc + word_count * 0.1
            
            if best is None or score > best[0]:
                best = (score, offset, text, ioc, word_count)
        
        if best[4] >= 5 or best[3] > 1.2:  # At least 5 words or high IoC
            all_results.append((best[0], page_num, best[1], best[2], best[3], best[4]))
    
    all_results.sort(reverse=True)
    
    print("Pages with 5+ common words or IoC > 1.2:")
    for score, page, offset, text, ioc, word_count in all_results[:15]:
        print(f"\nPage {page:2d} (offset={offset:2d}): IoC={ioc:.4f}, words={word_count}")
        print(f"  {text[:80]}")
    
    # =========================================================================
    # Look for the EXACT Page 56 pattern on other pages
    # =========================================================================
    print("\n" + "="*70)
    print("APPLYING EXACT PAGE 56 FORMULA TO ALL PAGES")
    print("="*70 + "\n")
    
    # Page 56 uses: -(prime[i] + 57) mod 29 as the key
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        # Apply Page 56 formula
        key = np.array([-(PRIMES[i % 29] + 57) % 29 for i in range(n)])
        decrypted = (cipher + key) % 29
        text = indices_to_text(decrypted)
        
        # Check if it starts with readable words
        if text[:3] in ['THE', 'AND', 'PAR'] or 'THE' in text[:15]:
            print(f"Page {page_num}: {text[:60]}")
    
    # =========================================================================
    # Now apply the GEMATRIA value of primes (not index)
    # =========================================================================
    print("\n" + "="*70)
    print("GEMATRIA PRIME VALUE AS KEY (not cycling mod 29)")
    print("="*70 + "\n")
    
    # Generate enough primes
    def generate_primes(n):
        primes = []
        num = 2
        while len(primes) < n:
            is_prime = True
            for p in primes:
                if p * p > num:
                    break
                if num % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
            num += 1
        return primes
    
    all_primes = generate_primes(500)
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        best = None
        
        for offset in [0, 29, 57, 58, 87]:
            # Use actual nth prime (not cycling)
            key = np.array([(all_primes[i] + offset) % 29 for i in range(n)])
            
            decrypted = (cipher - key) % 29
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            
            text_upper = text.upper()
            word_count = sum(1 for w in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT'] 
                            if w in text_upper[:40])
            
            score = ioc + word_count * 0.2
            
            if best is None or score > best[0]:
                best = (score, offset, text[:60], ioc, word_count)
        
        if best[4] >= 2 or best[3] > 1.2:
            results.append((best[0], page_num, best[1], best[2], best[3], best[4]))
    
    results.sort(reverse=True)
    
    print("Best results with true prime stream:")
    for score, page, offset, text, ioc, word_count in results[:10]:
        print(f"Page {page:2d} (offset={offset:2d}): IoC={ioc:.4f}")
        print(f"  {text}")

if __name__ == "__main__":
    main()

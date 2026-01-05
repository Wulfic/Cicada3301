#!/usr/bin/env python3
"""
Deep investigation of the Page 56 formula and its variations.

Page 56 was solved with: -(prime[i] + 57) mod 29
which produces: "AN END WITHIN THE DEEP WEB THERE EXISTS..."

Let's:
1. Verify the Page 56 solution
2. Try variations on other pages
3. Test mathematical patterns based on page numbers
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
LETTER_TO_IDX = {l: i for i, l in enumerate(LETTERS)}

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
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

# Generate first 500 primes
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

PRIME_STREAM = generate_primes(500)

def main():
    print("="*70)
    print("PAGE 56 FORMULA INVESTIGATION")
    print("="*70)
    
    pages = load_pages()
    
    # First, verify Page 56 solution
    print("\n=== PAGE 56 VERIFICATION ===\n")
    
    page56 = pages[56]
    cipher = runes_to_indices(page56)
    n = len(cipher)
    
    print(f"Page 56 has {n} runes")
    print(f"First 10 runes: {page56[:10]}")
    print(f"First 10 as indices: {cipher[:10]}")
    
    # The formula: -(prime[i] + 57) mod 29 is the KEY
    # Then decrypt: cipher - key mod 29
    print("\nApplying formula: key[i] = -(prime[i] + 57) mod 29")
    print("Then: plaintext[i] = (cipher[i] - key[i]) mod 29")
    
    # Wait - let me re-read the formula. It might be:
    # plaintext = (cipher + (-(prime + 57))) mod 29 = (cipher - prime - 57) mod 29
    
    for formula_name, formula in [
        ("cipher + (-(prime+57)) mod 29", lambda c, p: (c + (-(p + 57))) % 29),
        ("cipher - (prime+57) mod 29", lambda c, p: (c - (p + 57)) % 29),
        ("cipher - prime - 57 mod 29", lambda c, p: (c - p - 57) % 29),
        ("(cipher - prime) - 57 mod 29", lambda c, p: ((c - p) % 29 - 57) % 29),
        ("cipher + prime + 57 mod 29", lambda c, p: (c + p + 57) % 29),
    ]:
        decrypted = np.array([formula(cipher[i], PRIMES[i % 29]) for i in range(n)])
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        # Check if it starts with English
        if 'THE' in text[:20].upper() or 'AND' in text[:20].upper() or 'END' in text[:20].upper():
            print(f"\n*** MATCH: {formula_name}")
            print(f"    IoC: {ioc:.4f}")
            print(f"    Text: {text}")
    
    print("\n" + "="*70)
    print("TESTING VARIATIONS OF PAGE 56 FORMULA ON OTHER PAGES")
    print("="*70)
    
    # The successful formula appears to be: (cipher - prime[i%29] - 57) % 29
    # or equivalently: (cipher + (-(prime + 57))) % 29
    
    # What if each page uses its own offset instead of 57?
    # Page 56 uses offset 57 -> maybe page N uses offset N+1? or offset 58-N?
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:  # Known plaintext
            continue
        
        page_runes = pages[page_num]
        cipher = runes_to_indices(page_runes)
        n = len(cipher)
        
        if n < 20:
            continue
        
        page_results = []
        
        # Test various offset relationships to page number
        for offset_formula, offset_name in [
            (lambda pg: pg + 1, "pg+1"),
            (lambda pg: pg, "pg"),
            (lambda pg: 57, "57"),
            (lambda pg: 58 - pg if pg <= 58 else pg, "58-pg"),
            (lambda pg: pg * 2, "pg*2"),
            (lambda pg: 58, "58"),
            (lambda pg: 87, "87"),
            (lambda pg: 29, "29"),
            (lambda pg: 0, "0"),
            (lambda pg: 113 - pg, "113-pg"),  # 113 is the page count
            (lambda pg: 114 - pg, "114-pg"),
        ]:
            offset = offset_formula(page_num)
            
            # Apply the formula: (cipher - prime[i%29] - offset) % 29
            decrypted = np.array([(cipher[i] - PRIMES[i % 29] - offset) % 29 for i in range(n)])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            
            # Score for English
            score = ioc
            text_upper = text.upper()
            for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'ARE', 'NOT']:
                if word in text_upper[:60]:
                    score += len(word) * 0.2
            for word in ['INSTAR', 'PARABLE', 'WISDOM', 'DIVINITY', 'WITHIN']:
                if word in text_upper[:60]:
                    score += len(word) * 0.5
            
            page_results.append((score, offset_name, offset, text[:60], ioc))
        
        # Also try with prime stream (all primes, not just cycling 29)
        for offset in [0, 29, 57, 58]:
            decrypted = np.array([(cipher[i] - PRIME_STREAM[i] - offset) % 29 for i in range(n)])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            
            score = ioc
            text_upper = text.upper()
            for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'ARE', 'NOT']:
                if word in text_upper[:60]:
                    score += len(word) * 0.2
            
            page_results.append((score, f"prime_stream-{offset}", offset, text[:60], ioc))
        
        # Get best for this page
        page_results.sort(reverse=True)
        best = page_results[0]
        results.append((best[0], page_num, best[1], best[2], best[3], best[4], n))
    
    # Sort by score
    results.sort(reverse=True)
    
    print("\nTop 20 pages by prime-based formula:\n")
    
    for score, page, offset_name, offset, text, ioc, length in results[:20]:
        found = []
        for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'INSTAR', 'WISDOM', 'WITHIN']:
            if word in text.upper():
                found.append(word)
        
        print(f"Page {page:2d} (n={length:3d}): offset={offset_name} ({offset}), IoC={ioc:.4f}, score={score:.3f}")
        print(f"  {text}")
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Let's also test gematria prime (use the prime VALUE of each cipher rune as the key)
    print("\n" + "="*70)
    print("GEMATRIA PRIME KEY: Use prime value of each cipher rune")
    print("="*70 + "\n")
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:
            continue
        
        page_runes = pages[page_num]
        cipher = runes_to_indices(page_runes)
        n = len(cipher)
        
        if n < 20:
            continue
        
        page_results = []
        
        for offset in [0, 29, 57, 58, 87]:
            # Use gematria prime of each cipher rune as key
            decrypted = np.array([(cipher[i] - PRIMES[cipher[i]] - offset) % 29 for i in range(n)])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            
            score = ioc
            text_upper = text.upper()
            for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'ARE', 'NOT']:
                if word in text_upper[:60]:
                    score += len(word) * 0.2
            
            page_results.append((score, offset, text[:60], ioc))
        
        page_results.sort(reverse=True)
        best = page_results[0]
        results.append((best[0], page_num, best[1], best[2], best[3], n))
    
    results.sort(reverse=True)
    
    for score, page, offset, text, ioc, length in results[:10]:
        found = []
        for word in ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT']:
            if word in text.upper():
                found.append(word)
        
        print(f"Page {page:2d}: offset={offset}, IoC={ioc:.4f}: {text}")
        if found:
            print(f"  Found: {', '.join(found)}")

if __name__ == "__main__":
    main()

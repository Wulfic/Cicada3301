#!/usr/bin/env python3
"""
Page 56 was solved with: -(gematria(rune) + 57) mod 29
This gives the idea that EACH PAGE might use a different offset.

Let's try:
1. Apply Page 56 formula with different offsets for each page
2. Find which offset maximizes IoC for each page
3. See if there's a pattern to the offsets
"""

import numpy as np
from collections import Counter
from pathlib import Path
from itertools import product

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

# Gematria values - consecutive primes
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def apply_page56_formula(indices, offset):
    """Apply: -(gematria(rune) + offset) mod 29"""
    result = np.zeros_like(indices)
    for i, idx in enumerate(indices):
        gem = GEMATRIA[idx]
        result[i] = (-(gem + offset)) % 29
    return result

def try_all_offsets_per_page():
    """Try different offsets for each page."""
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(lp_path, 'r', encoding='utf-8') as f:
        lp_text = f.read()
    
    # Split by page markers
    pages = lp_text.split('&')
    
    print("="*80)
    print("TESTING PAGE 56 FORMULA WITH DIFFERENT OFFSETS PER PAGE")
    print("Formula: -(gematria(rune) + offset) mod 29")
    print("="*80)
    
    results = []
    
    for page_num, page in enumerate(pages):
        runes = text_to_indices(page)
        n = len(runes)
        
        if n < 20:  # Skip very short pages
            continue
        
        original_ioc = compute_ioc_normalized(runes)
        
        best_offset = 0
        best_ioc = 0
        best_text = ""
        
        # Try offsets from -200 to 200
        for offset in range(-200, 201):
            decrypted = apply_page56_formula(runes, offset)
            ioc = compute_ioc_normalized(decrypted)
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_offset = offset
                best_text = indices_to_english(decrypted[:50])
        
        # Also try positive variant: (gematria(rune) + offset) mod 29
        for offset in range(-200, 201):
            result = np.zeros_like(runes)
            for i, idx in enumerate(runes):
                gem = GEMATRIA[idx]
                result[i] = (gem + offset) % 29
            ioc = compute_ioc_normalized(result)
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_offset = ("+" , offset)
                best_text = indices_to_english(result[:50])
        
        improved = best_ioc > original_ioc * 1.3  # Significant improvement
        
        results.append({
            'page': page_num,
            'n': n,
            'original_ioc': original_ioc,
            'best_ioc': best_ioc,
            'best_offset': best_offset,
            'improved': improved,
            'sample': best_text
        })
        
        status = "IMPROVED!" if improved else ""
        offset_str = f"{best_offset}" if not isinstance(best_offset, tuple) else f"{best_offset[0]}{best_offset[1]}"
        print(f"\nPage {page_num:2d}: {n:4d} runes")
        print(f"  Original IoC: {original_ioc:.4f}")
        print(f"  Best IoC:     {best_ioc:.4f} (offset={offset_str}) {status}")
        print(f"  Sample:       {best_text}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY - Pages with significant improvement")
    print("="*80)
    
    improved_pages = [r for r in results if r['improved']]
    for r in improved_pages:
        print(f"Page {r['page']}: IoC {r['original_ioc']:.4f} -> {r['best_ioc']:.4f} (offset={r['best_offset']})")
    
    return results

def try_position_based_keys():
    """Try using position-based keys like: key[i] = function(i)"""
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(lp_path, 'r', encoding='utf-8') as f:
        lp_text = f.read()
    
    lp_indices = text_to_indices(lp_text)
    n = len(lp_indices)
    
    print("\n" + "="*80)
    print("POSITION-BASED KEY TESTING")
    print("="*80)
    
    # Try: key[i] = (a*i + b) mod 29
    print("\nLinear key: k[i] = (a*i + b) mod 29")
    
    best_ioc = 0
    best_params = (0, 0)
    
    for a in range(1, 30):
        for b in range(30):
            key = np.array([(a * i + b) % 29 for i in range(n)])
            decrypted = (lp_indices - key) % 29
            ioc = compute_ioc_normalized(decrypted)
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_params = (a, b)
    
    print(f"Best linear: a={best_params[0]}, b={best_params[1]}, IoC={best_ioc:.4f}")
    
    # Try: key[i] = (i*i) mod 29 (quadratic)
    print("\nQuadratic key: k[i] = (i^2 + b) mod 29")
    
    best_ioc = 0
    best_b = 0
    
    for b in range(30):
        key = np.array([(i*i + b) % 29 for i in range(n)])
        decrypted = (lp_indices - key) % 29
        ioc = compute_ioc_normalized(decrypted)
        
        if ioc > best_ioc:
            best_ioc = ioc
            best_b = b
    
    print(f"Best quadratic: b={best_b}, IoC={best_ioc:.4f}")
    
    # Try: key[i] = fibonacci(i) mod 29
    print("\nFibonacci key: k[i] = fib(i) mod 29")
    
    fib = [1, 1]
    for _ in range(n):
        fib.append((fib[-1] + fib[-2]) % 29)
    
    key = np.array(fib[:n])
    decrypted = (lp_indices - key) % 29
    ioc = compute_ioc_normalized(decrypted)
    print(f"Fibonacci key IoC: {ioc:.4f}")
    
    # Try: key based on prime numbers
    print("\nPrime index key: k[i] = prime(i) mod 29")
    
    # Generate primes
    def sieve_primes(limit):
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                for j in range(i*i, limit + 1, i):
                    is_prime[j] = False
        return [i for i in range(limit + 1) if is_prime[i]]
    
    primes = sieve_primes(100000)
    
    if len(primes) >= n:
        key = np.array([primes[i] % 29 for i in range(n)])
        decrypted = (lp_indices - key) % 29
        ioc = compute_ioc_normalized(decrypted)
        print(f"Prime index key IoC: {ioc:.4f}")

def main():
    results = try_all_offsets_per_page()
    try_position_based_keys()
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("""
If no single offset dramatically improves IoC for any page, it suggests:
1. The cipher is NOT a simple prime-shift with constant offset per page
2. A more complex stream cipher or running key is used
3. Or the key varies per-word or per-position within pages

Next steps to try:
- Running key using the solved "Parable" text
- Key derived from the page number or position
- Multiple layers of encryption
""")

if __name__ == "__main__":
    main()

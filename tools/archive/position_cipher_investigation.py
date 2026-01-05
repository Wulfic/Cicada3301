#!/usr/bin/env python3
"""
Investigate the "I AM NOT ME" pattern found in Page 49 when doing idx XOR position!

This is a potentially significant finding:
Page 49: idx XOR position: "IAMNOTMEOTHTHEAEON..."

Let's investigate this across all pages.
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
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

# Common English words for detection
COMMON_WORDS = ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'YOU', 'ARE',
                'NOT', 'ME', 'WE', 'BE', 'OR', 'AN', 'HE', 'AS', 'DO', 'AT',
                'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'HAVE', 'WITH', 'WHAT']

CICADA_WORDS = ['INSTAR', 'PARABLE', 'EMERGE', 'DIVINITY', 'WITHIN', 'SURFACE', 
                'CICADA', 'PRIME', 'WISDOM', 'TRUTH', 'SEEK', 'FIND']

def score_text(text):
    """Score text for English-likeness"""
    score = 0
    text_upper = text.upper()
    
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word) * 2
    
    for word in CICADA_WORDS:
        count = text_upper.count(word)
        score += count * len(word) * 5
    
    return score

def main():
    print("="*70)
    print("PAGE 49 'I AM NOT ME' INVESTIGATION")
    print("="*70)
    
    pages = load_pages()
    
    # First, deep dive into Page 49
    print("\n=== PAGE 49 DETAILED ANALYSIS ===\n")
    
    page49 = pages[49]
    indices = runes_to_indices(page49)
    
    print(f"Page 49 has {len(indices)} runes")
    print(f"Raw runes: {page49}")
    print()
    
    # Test XOR with position
    print("Testing: idx XOR position (mod 29)")
    decrypted_xor = np.array([(idx ^ i) % 29 for i, idx in enumerate(indices)])
    text = indices_to_text(decrypted_xor)
    ioc = calculate_ioc(decrypted_xor)
    print(f"Result: {text}")
    print(f"IoC: {ioc:.4f}")
    
    # Show the step-by-step
    print("\nStep-by-step transformation:")
    for i in range(min(20, len(indices))):
        idx = indices[i]
        xor_result = idx ^ i
        mod_result = xor_result % 29
        rune = RUNES[idx]
        letter_in = LETTERS[idx]
        letter_out = LETTERS[mod_result]
        print(f"  pos={i:2d}: {rune} ({letter_in:3s}, idx={idx:2d}) XOR {i:2d} = {xor_result:3d} % 29 = {mod_result:2d} ({letter_out})")
    
    # Test variations
    print("\n=== POSITION-BASED VARIATIONS ===\n")
    
    variations = [
        ("idx - position", lambda idx, pos: (idx - pos) % 29),
        ("idx + position", lambda idx, pos: (idx + pos) % 29),
        ("position - idx", lambda idx, pos: (pos - idx) % 29),
        ("idx XOR position", lambda idx, pos: (idx ^ pos) % 29),
        ("(idx - position) mod 29", lambda idx, pos: (idx - pos) % 29),
        ("(idx - position*2) mod 29", lambda idx, pos: (idx - pos*2) % 29),
        ("(idx - fibonacci[pos]) mod 29", None),  # Special case
        ("idx - prime[pos%29] mod 29", lambda idx, pos: (idx - PRIMES[pos % 29]) % 29),
    ]
    
    # Generate fibonacci sequence
    fib = [1, 1]
    while len(fib) < 300:
        fib.append(fib[-1] + fib[-2])
    
    results = []
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:  # Skip known plaintext
            continue
        
        page_runes = pages[page_num]
        indices = runes_to_indices(page_runes)
        n = len(indices)
        
        if n < 20:
            continue
        
        # Test each variation
        page_results = []
        
        for name, func in variations:
            if func is None:
                # Fibonacci - use modular arithmetic to avoid overflow
                decrypted = np.array([(int(indices[i]) - (fib[i] % 29)) % 29 for i in range(n)])
            else:
                decrypted = np.array([func(int(indices[i]), i) for i in range(n)])
            
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            word_score = score_text(text)
            
            page_results.append((ioc + word_score/100, name, text[:60], ioc, word_score))
        
        # Get best result for this page
        page_results.sort(reverse=True)
        best = page_results[0]
        results.append((best[0], page_num, best[1], best[2], best[3], best[4], n))
    
    # Sort by combined score
    results.sort(reverse=True)
    
    print("\nTop 15 pages by position-based decryption:")
    print("-" * 80)
    
    for score, page, method, text, ioc, word_score, length in results[:15]:
        # Find words
        text_upper = text.upper()
        found_words = [w for w in COMMON_WORDS + CICADA_WORDS if w in text_upper]
        
        print(f"Page {page:2d} (n={length:3d}): {method}")
        print(f"  IoC={ioc:.4f}, word_score={word_score}, combined={score:.4f}")
        print(f"  Text: {text}")
        if found_words:
            print(f"  Found: {', '.join(found_words)}")
        print()
    
    # Now let's specifically look at simple subtraction (which is like Vigenère)
    print("\n" + "="*70)
    print("SIMPLE POSITION SUBTRACTION (Vigenère-like)")
    print("="*70)
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:
            continue
        
        page_runes = pages[page_num]
        indices = runes_to_indices(page_runes)
        n = len(indices)
        
        if n < 20:
            continue
        
        # (idx - position) mod 29
        decrypted = np.array([(indices[i] - i) % 29 for i in range(n)])
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        
        # Look for "THE " or "AND " patterns
        if 'THE' in text.upper() or 'AND' in text.upper() or 'INSTAR' in text.upper():
            print(f"Page {page_num}: IoC={ioc:.4f}")
            print(f"  {text[:70]}")
            
            found = [w for w in COMMON_WORDS + CICADA_WORDS if w in text.upper()]
            print(f"  Found: {', '.join(found)}")
            print()
    
    # Test running position through all pages combined
    print("\n" + "="*70)
    print("COMBINED PAGES WITH CONTINUOUS POSITION")
    print("="*70)
    
    # Combine all encrypted pages
    all_indices = []
    for page_num in sorted(pages.keys()):
        if page_num == 57:
            continue
        indices = runes_to_indices(pages[page_num])
        all_indices.extend(indices)
    
    all_indices = np.array(all_indices, dtype=np.int32)
    print(f"Combined length: {len(all_indices)} runes")
    
    # Test position subtraction
    decrypted = np.array([(all_indices[i] - i) % 29 for i in range(len(all_indices))])
    text = indices_to_text(decrypted)
    ioc = calculate_ioc(decrypted)
    print(f"\n(idx - position) mod 29: IoC={ioc:.4f}")
    print(f"First 100 chars: {text[:100]}")
    print(f"Last 100 chars: {text[-100:]}")
    
    # Look for words
    found = [w for w in COMMON_WORDS + CICADA_WORDS if w in text.upper()]
    print(f"Found words: {', '.join(found[:20])}")
    
    # Also try XOR
    decrypted = np.array([(all_indices[i] ^ i) % 29 for i in range(len(all_indices))])
    text = indices_to_text(decrypted)
    ioc = calculate_ioc(decrypted)
    print(f"\n(idx XOR position) mod 29: IoC={ioc:.4f}")
    print(f"First 100 chars: {text[:100]}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Multi-Layer Cipher Investigation

The flat IoC (~1.0) suggests a one-time pad or compound cipher.
Let's test multi-layer combinations:
1. Shift → Vigenère
2. Vigenère → XOR with primes
3. Prime shift → Substitution
4. Running key with known plaintexts

Also testing if Page 0 = Page 54 identity is a cipher key.
"""

import re
import numpy as np
from collections import Counter
from itertools import permutations, product

# =============================================================================
# RUNE DATA
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

# English letter frequencies for scoring
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
}

COMMON_WORDS = ['THE', 'AND', 'OF', 'TO', 'IN', 'IT', 'FOR', 'NOT', 'ARE', 'WE', 
                'BE', 'OR', 'AN', 'HE', 'AS', 'DO', 'AT', 'IS', 'THAT', 'WHICH',
                'WISDOM', 'INSTAR', 'PRIMES', 'WITHIN', 'TRUTH', 'KNOW', 'SEEK']

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

def score_english(text):
    """Score based on common English words found."""
    text_upper = text.upper()
    score = 0
    found = []
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word)  # Weight by word length
        if count > 0:
            found.append(word)
    return score, found

def main():
    print("="*70)
    print("MULTI-LAYER CIPHER INVESTIGATION")
    print("="*70)
    
    pages = load_pages()
    
    # =========================================================================
    # TEST 1: Use Page 0 (or 54) as a running key for other pages
    # =========================================================================
    print("\n" + "="*70)
    print("TEST 1: PAGE 0/54 AS RUNNING KEY FOR OTHER PAGES")
    print("="*70 + "\n")
    
    page0 = runes_to_indices(pages[0])
    
    results = []
    for page_num in sorted(pages.keys()):
        if page_num in [0, 54, 56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        # Use Page 0 indices as key (cycled if needed)
        key = np.array([page0[i % len(page0)] for i in range(n)])
        
        # Try subtraction and addition
        for op in ['sub', 'add', 'xor']:
            if op == 'sub':
                decrypted = (cipher - key) % 29
            elif op == 'add':
                decrypted = (cipher + key) % 29
            else:  # XOR
                decrypted = cipher ^ key
                decrypted = decrypted % 29
            
            text = indices_to_text(decrypted)
            score, found = score_english(text[:80])
            ioc = calculate_ioc(decrypted)
            
            if score >= 15 or ioc > 1.3:
                results.append((score, page_num, op, text[:60], ioc, found))
    
    results.sort(reverse=True)
    print("Best results using Page 0/54 as key:")
    for score, page, op, text, ioc, found in results[:10]:
        print(f"Page {page:2d} ({op:3s}): score={score:3d}, IoC={ioc:.4f}, words={found}")
        print(f"  {text}")
    
    # =========================================================================
    # TEST 2: Chain two pages as keys
    # =========================================================================
    print("\n" + "="*70)
    print("TEST 2: CHAIN DECRYPTION - PAGE[N-2] + PAGE[N-1] → PAGE[N]")
    print("="*70 + "\n")
    
    results = []
    for page_num in range(2, max(pages.keys()) + 1):
        if page_num not in pages or page_num-1 not in pages or page_num-2 not in pages:
            continue
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        prev1 = runes_to_indices(pages[page_num - 1])
        prev2 = runes_to_indices(pages[page_num - 2])
        
        n = len(cipher)
        if n < 20:
            continue
        
        # Key = prev1 + prev2 (chained)
        combined_prev = runes_to_indices(pages[page_num - 1] + pages[page_num - 2])
        key = np.array([combined_prev[i % len(combined_prev)] for i in range(n)])
        
        decrypted = (cipher - key) % 29
        text = indices_to_text(decrypted)
        score, found = score_english(text[:80])
        ioc = calculate_ioc(decrypted)
        
        if score >= 10 or ioc > 1.2:
            results.append((score, page_num, text[:60], ioc, found))
    
    results.sort(reverse=True)
    print("Best chain decryption results:")
    for score, page, text, ioc, found in results[:10]:
        print(f"Page {page:2d}: score={score:3d}, IoC={ioc:.4f}, words={found}")
        print(f"  {text}")
    
    # =========================================================================
    # TEST 3: Multi-layer - First apply prime shift, then Vigenère
    # =========================================================================
    print("\n" + "="*70)
    print("TEST 3: MULTI-LAYER - PRIME SHIFT → VIGENÈRE")
    print("="*70 + "\n")
    
    # Test short Vigenère keys after prime shift
    test_keys = ['THE', 'AND', 'BE', 'WE', 'IS', 'IT', 'AN', 'TO', 'OF', 'INSTAR', 
                 'WISDOM', 'PRIMES', 'CICADA', 'TRUTH']
    
    results = []
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 30:
            continue
        
        for offset in [0, 57]:
            # First apply prime shift
            prime_shift = np.array([(PRIMES[i % 29] + offset) % 29 for i in range(n)])
            intermediate = (cipher - prime_shift) % 29
            
            # Then try Vigenère keys
            for key_word in test_keys:
                # Convert key word to indices
                key_indices = []
                i = 0
                while i < len(key_word):
                    matched = False
                    for length in [2, 1]:
                        if i + length <= len(key_word):
                            substr = key_word[i:i+length]
                            for idx, letter in enumerate(LETTERS):
                                if letter == substr:
                                    key_indices.append(idx)
                                    i += length
                                    matched = True
                                    break
                            if matched:
                                break
                    if not matched:
                        i += 1
                
                if not key_indices:
                    continue
                
                key = np.array([key_indices[i % len(key_indices)] for i in range(n)])
                decrypted = (intermediate - key) % 29
                text = indices_to_text(decrypted)
                score, found = score_english(text[:80])
                ioc = calculate_ioc(decrypted)
                
                if score >= 20 or ioc > 1.4:
                    results.append((score, page_num, offset, key_word, text[:60], ioc, found))
    
    results.sort(reverse=True)
    print("Best multi-layer results:")
    for score, page, offset, key_word, text, ioc, found in results[:10]:
        print(f"Page {page:2d} (offset={offset}, key={key_word}): score={score:3d}, IoC={ioc:.4f}")
        print(f"  {text}")
        print(f"  Words: {found}")
    
    # =========================================================================
    # TEST 4: Reverse engineering - Find key that produces English starts
    # =========================================================================
    print("\n" + "="*70)
    print("TEST 4: REVERSE ENGINEER KEY FOR ENGLISH STARTS")
    print("="*70 + "\n")
    
    # Common starts for Cicada text: "LIKE THE", "AN END", "PARABLE", "WITHIN"
    starts = {
        'THE': [16, 8, 18],          # T, H, E
        'LIKE': [20, 10, 5, 18],     # L, I, C (CK), E  -> Actually L=20, I=10, K not in runes
        'WITHIN': [7, 10, 16, 8, 10, 9],  # W, I, T, H, I, N
        'PARABLE': [13, 24, 4, 24, 17, 20, 18],  # P, A, R, A, B, L, E
        'INSTAR': [10, 9, 15, 16, 24, 4],  # I, N, S, T, A, R
        'WISDOM': [7, 10, 15, 23, 3, 19],  # W, I, S, D, O, M
        'ANEND': [24, 9, 18, 9, 23],  # A, N, E, N, D
    }
    
    for start_word, target_indices in starts.items():
        print(f"\nLooking for pages that could start with '{start_word}':")
        
        for page_num in sorted(pages.keys()):
            if page_num in [56, 57]:
                continue
            
            cipher = runes_to_indices(pages[page_num])
            if len(cipher) < len(target_indices):
                continue
            
            # Calculate what key would produce this start
            key = []
            for i, t in enumerate(target_indices):
                k = (cipher[i] - t) % 29
                key.append(k)
            
            # Check if key has any pattern
            key_text = indices_to_text(key)
            
            # Check if key is simple (all same, or sequence)
            if len(set(key)) == 1:
                print(f"  Page {page_num}: shift by {key[0]} → '{start_word}'")
            elif key == list(range(key[0], key[0] + len(key))):
                print(f"  Page {page_num}: sequential key starting at {key[0]} → '{start_word}'")
            
            # Check if key matches primes
            prime_match = True
            for i, k in enumerate(key):
                if k != PRIMES[i % 29] % 29:
                    prime_match = False
                    break
            if prime_match:
                print(f"  Page {page_num}: PRIME KEY MATCH → '{start_word}'!")
    
    # =========================================================================
    # TEST 5: Frequency analysis for simple substitution
    # =========================================================================
    print("\n" + "="*70)
    print("TEST 5: CHECK FOR SIMPLE SUBSTITUTION CIPHER")
    print("="*70 + "\n")
    
    # Combine all unsolved pages
    all_unsolved = []
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        cipher = runes_to_indices(pages[page_num])
        all_unsolved.extend(cipher)
    
    all_unsolved = np.array(all_unsolved)
    
    # Calculate frequency
    freq = Counter(all_unsolved)
    total = len(all_unsolved)
    
    print("Rune frequency across all unsolved pages:")
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    
    # English frequency order: E T A O I N S H R D L C U M W F G Y P B V K J X Q Z
    english_order = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 
                     'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
    
    print("\nMost frequent runes:")
    for idx, count in sorted_freq[:15]:
        pct = count / total * 100
        print(f"  {IDX_TO_LETTER[idx]:3s} ({idx:2d}): {count:5d} ({pct:5.2f}%)")
    
    # IoC of combined corpus
    ioc = calculate_ioc(all_unsolved)
    print(f"\nCombined IoC: {ioc:.4f}")
    print("(English ~1.7, Random ~1.0)")
    
    if ioc < 1.2:
        print("\nIoC suggests polyalphabetic or running-key cipher, NOT simple substitution.")
    
    # =========================================================================
    # TEST 6: Look for pages with higher IoC (might be simpler cipher)
    # =========================================================================
    print("\n" + "="*70)
    print("TEST 6: PAGES WITH HIGHER IoC (SIMPLER CIPHER?)")
    print("="*70 + "\n")
    
    page_iocs = []
    for page_num in sorted(pages.keys()):
        if page_num in [56, 57]:
            continue
        cipher = runes_to_indices(pages[page_num])
        if len(cipher) < 20:
            continue
        ioc = calculate_ioc(cipher)
        page_iocs.append((ioc, page_num, len(cipher)))
    
    page_iocs.sort(reverse=True)
    
    print("Pages by IoC (higher = potentially simpler cipher):")
    for ioc, page, length in page_iocs[:15]:
        print(f"  Page {page:2d}: IoC={ioc:.4f}, length={length}")
    
    print("\nPages with IoC > 1.2 might have simpler encryption.")

if __name__ == "__main__":
    main()

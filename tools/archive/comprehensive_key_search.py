#!/usr/bin/env python3
"""
Comprehensive Key Search for Liber Primus

Based on what we know:
1. Page 56 was solved with: -(prime + 57) mod 29
2. Page 57 is plaintext: "PARABLE LIKE THE INSTAR..."
3. The unsolved pages have IoC ~1.0 (flat distribution = strong encryption)

Key insights from the document:
- IoC ~1.0 suggests either running key, one-time pad, or multi-layer encryption
- Page 56's formula uses primes, suggesting mathematical patterns
- PARABLE could be a running key

This script will test:
1. Running key with known texts (PARABLE, Liber Primus page 57, etc.)
2. Prime-based sequences
3. Gematria-based autokey
4. All combinations of known transformations
"""

import re
import numpy as np
from collections import Counter
from itertools import product

# =============================================================================
# RUNE DATA
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
IDX_TO_PRIME = {i: p for i, p in enumerate(PRIMES)}

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

def text_to_indices(text):
    """Convert letter text to indices, handling digraphs"""
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        found = False
        # Try 2-character digraphs first
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
                i += 1  # Skip unknown characters
    return np.array(indices, dtype=np.int32)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

# English quadgram statistics for scoring (simplified)
COMMON_PATTERNS = {
    'THE': 10, 'AND': 8, 'ING': 8, 'TION': 6, 'THAT': 6,
    'FOR': 5, 'ENT': 5, 'ION': 5, 'HER': 5, 'TER': 5,
    'WAS': 5, 'YOU': 5, 'ITH': 5, 'VER': 5, 'ALL': 5,
    'WITH': 4, 'INSTAR': 10, 'PARABLE': 10, 'DIVINITY': 10,
    'WITHIN': 8, 'CICADA': 8, 'PRIME': 6, 'WISDOM': 6,
    'EMERGE': 8, 'TRUTH': 6, 'SEEK': 5, 'FIND': 5,
}

def score_english(text):
    """Score text for English-likeness"""
    score = 0
    text_upper = text.upper()
    for pattern, weight in COMMON_PATTERNS.items():
        count = text_upper.count(pattern)
        score += count * weight * len(pattern)
    return score

# Page 57 PARABLE text (known plaintext)
PARABLE_TEXT = """PARABLELIKETHEINSTARAREMANYBUTWHEREONE
ISABLETOCHANGEFROMADARKANDNARROWED
CONDITIONTOWARDSTHELIFEOFTHEIMAGOAS
THENEWTHENAEONTHEPROGRESSOFALLOURLI
VESANDTHECHANGENECESSARYWITHINITHIS
ISCIRCUMFERENCEANDITISDIVINITY"""

def clean_text_for_key(text):
    """Remove non-letter characters and convert to uppercase"""
    return ''.join(c for c in text.upper() if c.isalpha())

def main():
    print("="*70)
    print("COMPREHENSIVE KEY SEARCH FOR LIBER PRIMUS")
    print("="*70)
    
    pages = load_pages()
    
    # Prepare running key from PARABLE
    parable_clean = clean_text_for_key(PARABLE_TEXT)
    parable_key = text_to_indices(parable_clean)
    
    print(f"PARABLE key length: {len(parable_key)} runes")
    print(f"PARABLE first 20 as indices: {parable_key[:20]}")
    print(f"PARABLE first 20 as text: {indices_to_text(parable_key[:20])}")
    
    # Generate prime stream
    def prime_stream(n):
        """Generate n primes"""
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
    
    primes = prime_stream(5000)
    
    results = []
    
    print("\n" + "="*70)
    print("TESTING MULTIPLE DECRYPTION METHODS")
    print("="*70 + "\n")
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:  # Skip known plaintext
            continue
        
        page_runes = pages[page_num]
        cipher = runes_to_indices(page_runes)
        n = len(cipher)
        
        if n < 20:
            continue
        
        page_results = []
        
        # Method 1: Running key with PARABLE
        if len(parable_key) >= n:
            key_slice = parable_key[:n]
            # Try subtraction
            decrypted = (cipher - key_slice) % 29
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            eng_score = score_english(text)
            page_results.append((ioc + eng_score/100, 'PARABLE-sub', text[:60], ioc, eng_score))
            
            # Try addition
            decrypted = (cipher + key_slice) % 29
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            eng_score = score_english(text)
            page_results.append((ioc + eng_score/100, 'PARABLE-add', text[:60], ioc, eng_score))
        
        # Method 2: Page 56 formula applied
        # Original: -(prime + 57) mod 29
        for offset in [0, 29, 57, 58, 87]:  # Try different offsets
            decrypted = np.array([-(PRIMES[i % 29] + offset) % 29 for i in range(n)])
            decrypted = (cipher + decrypted) % 29  # Apply to cipher
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            eng_score = score_english(text)
            page_results.append((ioc + eng_score/100, f'p56-formula-off{offset}', text[:60], ioc, eng_score))
        
        # Method 3: Prime stream (various mod operations)
        prime_key = np.array([primes[i] % 29 for i in range(n)])
        
        decrypted = (cipher - prime_key) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        eng_score = score_english(text)
        page_results.append((ioc + eng_score/100, 'prime-stream-sub', text[:60], ioc, eng_score))
        
        decrypted = (cipher + prime_key) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        eng_score = score_english(text)
        page_results.append((ioc + eng_score/100, 'prime-stream-add', text[:60], ioc, eng_score))
        
        # Method 4: Gematria-based prime key (using index->prime mapping)
        gem_prime_key = np.array([PRIMES[cipher[i % len(cipher)] % 29] % 29 for i in range(n)])
        
        decrypted = (cipher - gem_prime_key) % 29
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        eng_score = score_english(text)
        page_results.append((ioc + eng_score/100, 'gematria-prime-sub', text[:60], ioc, eng_score))
        
        # Method 5: Autokey cipher
        # Vigenère autokey: key = short_key + plaintext
        for short_key_len in [3, 5, 7]:
            # Try all possible short keys (brute force small keys)
            # For now, just try some common ones
            for key_text in ['THE', 'AND', 'INSTAR', 'PARABLE', 'DIVINI', 'CICADA']:
                key = text_to_indices(key_text)
                if len(key) == 0:
                    continue
                
                decrypted = np.zeros(n, dtype=np.int32)
                for i in range(n):
                    if i < len(key):
                        k = key[i]
                    else:
                        k = decrypted[i - len(key)]  # Autokey
                    decrypted[i] = (cipher[i] - k) % 29
                
                text = indices_to_text(decrypted)
                ioc = calculate_ioc(decrypted)
                eng_score = score_english(text)
                page_results.append((ioc + eng_score/100, f'autokey-{key_text}', text[:60], ioc, eng_score))
        
        # Method 6: Beaufort cipher (key - cipher)
        for short_key in ['THE', 'AND', 'INSTAR', 'CICADA']:
            key = text_to_indices(short_key)
            if len(key) == 0:
                continue
            decrypted = np.array([(key[i % len(key)] - cipher[i]) % 29 for i in range(n)])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            eng_score = score_english(text)
            page_results.append((ioc + eng_score/100, f'beaufort-{short_key}', text[:60], ioc, eng_score))
        
        # Method 7: Double encryption (shift then Vigenère)
        for shift in range(29):
            shifted = (cipher + shift) % 29
            for key_text in ['THE', 'AND', 'INSTAR']:
                key = text_to_indices(key_text)
                if len(key) == 0:
                    continue
                decrypted = np.array([(shifted[i] - key[i % len(key)]) % 29 for i in range(n)])
                text = indices_to_text(decrypted)
                ioc = calculate_ioc(decrypted)
                eng_score = score_english(text)
                if ioc > 1.3 or eng_score > 30:  # Only track interesting ones
                    page_results.append((ioc + eng_score/100, f'shift{shift}-vig-{key_text}', text[:60], ioc, eng_score))
        
        # Get best results for this page
        page_results.sort(reverse=True)
        
        if page_results:
            best = page_results[0]
            results.append((best[0], page_num, best[1], best[2], best[3], best[4], n))
    
    # Sort all results by combined score
    results.sort(reverse=True)
    
    print("\n" + "="*70)
    print("TOP 20 BEST DECRYPTION RESULTS")
    print("="*70 + "\n")
    
    for score, page, method, text, ioc, eng_score, length in results[:20]:
        print(f"Page {page:2d} (n={length:3d}): {method}")
        print(f"  IoC={ioc:.4f}, eng_score={eng_score}, combined={score:.4f}")
        print(f"  Text: {text}")
        
        # Highlight found words
        text_upper = text.upper()
        found = []
        for pattern in COMMON_PATTERNS:
            if pattern in text_upper:
                found.append(pattern)
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Special analysis: What if pages use different keys from the same family?
    print("\n" + "="*70)
    print("CONSISTENCY CHECK: Same method across all pages")
    print("="*70 + "\n")
    
    # Test PARABLE running key on all pages
    print("Testing PARABLE running key (subtraction) on all pages:\n")
    
    all_decrypted = []
    total_eng_score = 0
    
    for page_num in sorted(pages.keys()):
        if page_num == 57:
            continue
        
        page_runes = pages[page_num]
        cipher = runes_to_indices(page_runes)
        n = len(cipher)
        
        if n < 10:
            continue
        
        if len(parable_key) >= n:
            key_slice = parable_key[:n]
            decrypted = (cipher - key_slice) % 29
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            eng_score = score_english(text)
            total_eng_score += eng_score
            
            all_decrypted.extend(decrypted.tolist())
            
            if eng_score > 20 or ioc > 1.2:
                print(f"Page {page_num:2d}: IoC={ioc:.4f}, eng={eng_score:3d}: {text[:50]}")
    
    print(f"\nTotal english score: {total_eng_score}")
    
    if all_decrypted:
        combined_ioc = calculate_ioc(np.array(all_decrypted))
        print(f"Combined IoC: {combined_ioc:.4f}")

if __name__ == "__main__":
    main()

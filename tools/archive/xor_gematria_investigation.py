#!/usr/bin/env python3
"""
Deep investigation of XOR-Gematria cipher variant

The gpu_cipher_solver found that XOR with gematria+offset produces very high IoC (2.75+).
This warrants deeper investigation!

IoC > 2.0 often indicates:
1. Very short text (higher variance)
2. Highly repetitive pattern
3. Something unusual about the transformation

Let's investigate this thoroughly.
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

def xor_gematria_decrypt(indices, offset):
    """XOR each index with its gematria value + offset, then mod 29"""
    result = []
    for idx in indices:
        gem = PRIMES[idx]
        decrypted = (idx ^ (gem + offset)) % 29
        result.append(decrypted)
    return np.array(result, dtype=np.int32)

def main():
    print("="*70)
    print("XOR-GEMATRIA CIPHER INVESTIGATION")
    print("="*70)
    
    pages = load_pages()
    
    # Test all pages with XOR-gematria
    print("\n=== XOR-GEMATRIA RESULTS BY PAGE ===\n")
    
    all_results = []
    
    for page_num in sorted(pages.keys()):
        runes = pages[page_num]
        indices = runes_to_indices(runes)
        
        if len(indices) < 20:
            continue
        
        raw_ioc = calculate_ioc(indices)
        
        # Test various offsets
        best_ioc = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(-50, 150):
            decrypted = xor_gematria_decrypt(indices, offset)
            ioc = calculate_ioc(decrypted)
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_offset = offset
                best_text = indices_to_text(decrypted)
        
        all_results.append((best_ioc, page_num, best_offset, best_text[:80], len(indices)))
        
        if best_ioc > 1.5:
            print(f"Page {page_num:2d}: raw_IoC={raw_ioc:.4f} -> xor_gem+{best_offset:3d} -> IoC={best_ioc:.4f}")
            print(f"         {best_text[:70]}")
    
    # Sort by IoC
    all_results.sort(reverse=True)
    
    print("\n" + "="*70)
    print("TOP 10 XOR-GEMATRIA RESULTS")
    print("="*70)
    
    for ioc, page, offset, text, length in all_results[:10]:
        print(f"Page {page:2d} (n={length:3d}): xor_gem+{offset:3d} -> IoC={ioc:.4f}")
        print(f"  {text}")
        
        # Look for patterns
        text_upper = text.upper()
        
        # Check for common English words
        common_words = ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'YOU', 'ARE']
        found = [w for w in common_words if w in text_upper]
        if found:
            print(f"  Found words: {', '.join(found)}")
        
        print()
    
    # Deep analysis of the top result
    print("="*70)
    print("DEEP ANALYSIS OF TOP RESULT")
    print("="*70)
    
    best = all_results[0]
    ioc, page_num, offset, text, length = best
    
    print(f"Page {page_num}, offset {offset}")
    
    indices = runes_to_indices(pages[page_num])
    decrypted = xor_gematria_decrypt(indices, offset)
    
    # Frequency analysis
    freq = Counter(decrypted)
    print("\nFrequency distribution:")
    for idx, count in sorted(freq.items(), key=lambda x: -x[1])[:10]:
        letter = IDX_TO_LETTER[idx]
        pct = count / len(decrypted) * 100
        print(f"  {letter:3s}: {count:3d} ({pct:.1f}%)")
    
    # Check if the high IoC is due to few unique characters
    unique_chars = len(freq)
    print(f"\nUnique characters: {unique_chars}/29")
    print(f"Text length: {length}")
    
    # Show the full text
    full_text = indices_to_text(decrypted)
    print(f"\nFull decrypted text:\n{full_text}")
    
    # Analyze what XOR actually does here
    print("\n" + "="*70)
    print("UNDERSTANDING THE XOR TRANSFORMATION")
    print("="*70)
    
    print("\nRune -> XOR(idx, gem+offset) -> Result")
    for i in range(min(20, len(indices))):
        idx = indices[i]
        gem = PRIMES[idx]
        xor_result = idx ^ (gem + offset)
        mod_result = xor_result % 29
        rune = RUNES[idx]
        letter_in = LETTERS[idx]
        letter_out = LETTERS[mod_result]
        print(f"  {rune} ({letter_in:3s}, idx={idx:2d}) ^ ({gem:3d}+{offset}) = {xor_result:3d} % 29 = {mod_result:2d} ({letter_out})")
    
    # The XOR operation might be revealing a pattern
    print("\n" + "="*70)
    print("PATTERN ANALYSIS")
    print("="*70)
    
    # What if we're seeing a substitution cipher?
    # Let's see what the transformation looks like as a mapping
    print("\nEffective substitution mapping (index -> decrypted):")
    mapping = {}
    for i in range(29):
        gem = PRIMES[i]
        xor_result = i ^ (gem + offset)
        mod_result = xor_result % 29
        mapping[i] = mod_result
    
    # Check if this is a simple permutation
    values = list(mapping.values())
    if len(set(values)) == 29:
        print("This is a one-to-one mapping (permutation cipher)!")
    else:
        print(f"Not a permutation - only {len(set(values))} unique outputs")
        # Show collisions
        from collections import defaultdict
        reverse_map = defaultdict(list)
        for k, v in mapping.items():
            reverse_map[v].append(k)
        print("Collisions:")
        for v, keys in reverse_map.items():
            if len(keys) > 1:
                print(f"  Output {v} ({LETTERS[v]}): from inputs {keys}")

    # Try different XOR operations
    print("\n" + "="*70)
    print("ALTERNATIVE XOR OPERATIONS")
    print("="*70)
    
    # XOR with just the index
    for page_num in [55, 42, 32, 49]:
        if page_num not in pages:
            continue
        indices = runes_to_indices(pages[page_num])
        
        print(f"\nPage {page_num}:")
        
        # idx XOR prime_index
        decrypted = np.array([(idx ^ i) % 29 for i, idx in enumerate(indices)])
        ioc = calculate_ioc(decrypted)
        text = indices_to_text(decrypted)
        print(f"  idx XOR position: IoC={ioc:.4f}: {text[:50]}")
        
        # idx XOR (prime at position)
        decrypted = np.array([(idx ^ PRIMES[i % 29]) % 29 for i, idx in enumerate(indices)])
        ioc = calculate_ioc(decrypted)
        text = indices_to_text(decrypted)
        print(f"  idx XOR prime[pos]: IoC={ioc:.4f}: {text[:50]}")
        
        # prime[idx] XOR idx
        decrypted = np.array([(PRIMES[idx] ^ idx) % 29 for idx in indices])
        ioc = calculate_ioc(decrypted)
        text = indices_to_text(decrypted)
        print(f"  prime[idx] XOR idx: IoC={ioc:.4f}: {text[:50]}")

if __name__ == "__main__":
    main()

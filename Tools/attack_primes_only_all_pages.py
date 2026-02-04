#!/usr/bin/env python3
"""
Test hypothesis: Pages 20-54 contain message ONLY at prime positions.
Composite positions might be noise/padding.

Extract prime positions from all pages and decrypt with Deor.
"""

import os
import sys

# Gematria Primus
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [c for c in text if c in RUNES]

def rune_to_idx(r):
    return RUNES.index(r) if r in RUNES else -1

def load_deor():
    filepath = 'c:/Users/tyler/Repos/Cicada3301/Analysis/Reference_Docs/deor_poem.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    alt_map = {'A': 24, 'E': 18, 'O': 4, 'Y': 28}
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph == 'TH': 
                indices.append(2)
                i += 2
                continue
            elif digraph == 'EA':
                indices.append(27)
                i += 2
                continue
            elif digraph == 'NG':
                indices.append(21)
                i += 2
                continue
        c = text[i]
        if c in mapping:
            indices.append(mapping.index(c))
        elif c in alt_map:
            indices.append(alt_map[c])
        elif c.isalpha():
            idx = ord(c) - ord('A')
            indices.append(idx % 29)
        i += 1
    return indices

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    from collections import Counter
    counts = Counter(indices)
    n = len(indices)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1) / 29) if n > 1 else 0

def decrypt_beaufort(cipher, key):
    return [(key[i % len(key)] - c) % 29 for i, c in enumerate(cipher)]

def indices_to_text(indices):
    mapping = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
    return ''.join(mapping[i % 29] for i in indices)

def main():
    print("=" * 70)
    print("HYPOTHESIS: Message is ONLY at prime positions across Pages 20-54")
    print("=" * 70)
    
    deor = load_deor()
    print(f"Deor key length: {len(deor)}")
    
    base_path = 'c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages'
    
    # Collect prime-position runes from all pages 20-54
    all_prime_runes = []
    page_stats = []
    
    for page_num in range(20, 55):
        page_dir = os.path.join(base_path, f'page_{page_num:02d}')
        rune_file = os.path.join(page_dir, 'runes.txt')
        
        if not os.path.exists(rune_file):
            continue
            
        runes = load_runes(rune_file)
        if not runes:
            continue
        
        # Extract prime positions
        primes = [i for i in range(2, len(runes) + 1) if is_prime(i)]
        prime_runes = [runes[p-1] for p in primes if p <= len(runes)]
        
        all_prime_runes.extend(prime_runes)
        page_stats.append((page_num, len(runes), len(prime_runes)))
    
    print(f"\nPages loaded:")
    for pn, total, primes in page_stats:
        print(f"  Page {pn}: {total} runes, {primes} at prime positions")
    
    print(f"\nTotal prime-position runes: {len(all_prime_runes)}")
    
    # Convert to indices
    prime_indices = [rune_to_idx(r) for r in all_prime_runes]
    
    # Decrypt with Deor (Beaufort)
    decrypted = decrypt_beaufort(prime_indices, deor)
    ioc = calc_ioc(decrypted)
    
    print(f"\nDecrypted with Beaufort + Deor:")
    print(f"IoC: {ioc:.4f}")
    
    text = indices_to_text(decrypted)
    
    # Print in chunks
    print(f"\nDecrypted text ({len(text)} chars):")
    for i in range(0, len(text), 80):
        chunk = text[i:i+80]
        print(f"  {i:4d}: {chunk}")
    
    # Look for English words
    print("\n" + "=" * 70)
    print("WORD SEARCH in decrypted stream")
    print("=" * 70)
    
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                    'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HIS', 'HAS',
                    'LONE', 'EODE', 'SEFA', 'THAT', 'WITH', 'HAVE', 'THIS',
                    'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'HAVE', 'MANY',
                    'SOME', 'THEM', 'UNTO', 'PATH', 'SEEK', 'FIND', 'KNOW',
                    'TRUTH', 'LIGHT', 'DARK', 'MIND', 'SOUL', 'SELF', 'WISE']
    
    found = {}
    for word in common_words:
        if word in text:
            positions = []
            start = 0
            while True:
                pos = text.find(word, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            if positions:
                found[word] = positions
    
    if found:
        print("Found words:")
        for word, positions in sorted(found.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {word}: {len(positions)} occurrences at {positions[:5]}{'...' if len(positions) > 5 else ''}")
    else:
        print("No common words found directly")
    
    # Also try: maybe each PAGE's primes should be decoded separately
    print("\n" + "=" * 70)
    print("Per-page prime decryption:")
    print("=" * 70)
    
    for page_num in range(20, 55):
        page_dir = os.path.join(base_path, f'page_{page_num:02d}')
        rune_file = os.path.join(page_dir, 'runes.txt')
        
        if not os.path.exists(rune_file):
            continue
            
        runes = load_runes(rune_file)
        if not runes:
            continue
        
        primes = [i for i in range(2, len(runes) + 1) if is_prime(i)]
        prime_runes = [runes[p-1] for p in primes if p <= len(runes)]
        
        if len(prime_runes) < 10:
            continue
        
        prime_idx = [rune_to_idx(r) for r in prime_runes]
        decrypted = decrypt_beaufort(prime_idx, deor)
        ioc = calc_ioc(decrypted)
        
        text = indices_to_text(decrypted[:50])
        
        if ioc > 1.3:
            print(f"Page {page_num}: IoC = {ioc:.2f} ** {text}")
        else:
            print(f"Page {page_num}: IoC = {ioc:.2f}    {text[:30]}...")

if __name__ == '__main__':
    main()

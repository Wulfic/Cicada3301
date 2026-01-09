#!/usr/bin/env python3
"""
Solved Pages as Running Key Attack
===================================
Use the rune content from solved pages (55-74) as a running key
to decrypt unsolved pages (18-54).

Also explores prime-indexed extraction and other creative approaches.
"""

import os
from collections import Counter

GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

def read_runes(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [c for c in content if c in GP_RUNE_TO_INDEX]

def indices_to_runeglish(indices):
    return ''.join(INDEX_TO_RUNEGLISH[i] for i in indices)

def score_english(text):
    score = 0
    common_words = ['THE', 'AND', 'OF', 'TO', 'IS', 'IN', 'THAT', 'IT', 'FOR', 
                    'AS', 'WITH', 'BE', 'WAS', 'ARE', 'THIS', 'TRUTH', 'SACRED',
                    'PRIMES', 'WISDOM', 'KNOWLEDGE', 'DIVINITY', 'PILGRIM',
                    'WITHIN', 'SEEK', 'FIND', 'BELIEVE', 'NOTHING', 'WELCOME',
                    'JOURNEY', 'GREAT', 'WARNING', 'BOOK', 'TRUE', 'KNOW']
    
    for word in common_words:
        if len(word) >= 3:
            count = text.count(word)
            score += count * len(word) * 10
    
    return score

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_up_to(n):
    return [i for i in range(2, n+1) if is_prime(i)]

# Load all pages
print("="*70)
print("LOADING ALL PAGES")
print("="*70)

all_unsolved_runes = []  # Pages 18-54
all_solved_runes = []    # Pages 55-74

for page in range(18, 55):
    runes = read_runes(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page:02d}/runes.txt")
    all_unsolved_runes.extend(runes)

for page in range(55, 75):
    runes = read_runes(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page:02d}/runes.txt")
    all_solved_runes.extend(runes)

print(f"Total unsolved runes (pages 18-54): {len(all_unsolved_runes)}")
print(f"Total solved runes (pages 55-74): {len(all_solved_runes)}")

# Convert to indices
unsolved_indices = [GP_RUNE_TO_INDEX[r] for r in all_unsolved_runes]
solved_indices = [GP_RUNE_TO_INDEX[r] for r in all_solved_runes]

# Strategy 1: Use solved pages as running key
print("\n" + "="*70)
print("STRATEGY 1: Solved Pages (55-74) as Running Key for Pages 18-54")
print("="*70)

# SUB mode
plain_sub = [(unsolved_indices[i] - solved_indices[i % len(solved_indices)]) % 29 
             for i in range(len(unsolved_indices))]
runeglish_sub = indices_to_runeglish(plain_sub)
score_sub = score_english(runeglish_sub)

# ADD mode
plain_add = [(unsolved_indices[i] + solved_indices[i % len(solved_indices)]) % 29 
             for i in range(len(unsolved_indices))]
runeglish_add = indices_to_runeglish(plain_add)
score_add = score_english(runeglish_add)

print(f"SUB mode: Score={score_sub}")
print(f"  First 200 chars: {runeglish_sub[:200]}")
print(f"\nADD mode: Score={score_add}")
print(f"  First 200 chars: {runeglish_add[:200]}")

# Strategy 2: Extract only prime-indexed runes
print("\n" + "="*70)
print("STRATEGY 2: Extract Prime-Indexed Runes Only")
print("="*70)

primes = get_primes_up_to(len(all_unsolved_runes))
prime_indexed = [all_unsolved_runes[p-1] for p in primes if p <= len(all_unsolved_runes)]
prime_runeglish = indices_to_runeglish([GP_RUNE_TO_INDEX[r] for r in prime_indexed])

print(f"Extracted {len(prime_indexed)} prime-indexed runes")
print(f"  First 200 chars: {prime_runeglish[:200]}")
print(f"  Score: {score_english(prime_runeglish)}")

# Check IoC of prime-indexed extraction
prime_indices = [GP_RUNE_TO_INDEX[r] for r in prime_indexed]
counter = Counter(prime_indices)
n = len(prime_indices)
ioc = sum(c*(c-1) for c in counter.values()) / (n*(n-1)) if n > 1 else 0
print(f"  IoC of prime-indexed: {ioc:.4f}")

# Strategy 3: Interleave pages 0-17 with pages 18-54
print("\n" + "="*70)
print("STRATEGY 3: Pages 0-17 as Key for Pages 18-54")
print("="*70)

early_runes = []
for page in range(0, 18):
    runes = read_runes(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page:02d}/runes.txt")
    early_runes.extend(runes)

print(f"Total runes from pages 0-17: {len(early_runes)}")

early_indices = [GP_RUNE_TO_INDEX[r] for r in early_runes]

plain_sub2 = [(unsolved_indices[i] - early_indices[i % len(early_indices)]) % 29 
              for i in range(len(unsolved_indices))]
runeglish_sub2 = indices_to_runeglish(plain_sub2)
score_sub2 = score_english(runeglish_sub2)

print(f"Using pages 0-17 as key (SUB): Score={score_sub2}")
print(f"  First 200 chars: {runeglish_sub2[:200]}")

# Strategy 4: Fibonacci-indexed extraction
print("\n" + "="*70)
print("STRATEGY 4: Fibonacci-Indexed Extraction")
print("="*70)

def fibonacci_up_to(n):
    fibs = [1, 2]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    return [f for f in fibs if f <= n]

fibs = fibonacci_up_to(len(all_unsolved_runes))
fib_indexed = [all_unsolved_runes[f-1] for f in fibs if f <= len(all_unsolved_runes)]
fib_runeglish = indices_to_runeglish([GP_RUNE_TO_INDEX[r] for r in fib_indexed])

print(f"Extracted {len(fib_indexed)} Fibonacci-indexed runes")
print(f"  Result: {fib_runeglish}")

# Strategy 5: Reverse order attack
print("\n" + "="*70)
print("STRATEGY 5: Reversed Pages Attack")
print("="*70)

# Reverse the unsolved runes
reversed_unsolved = list(reversed(unsolved_indices))
plain_rev_sub = [(reversed_unsolved[i] - solved_indices[i % len(solved_indices)]) % 29 
                 for i in range(len(reversed_unsolved))]
runeglish_rev = indices_to_runeglish(plain_rev_sub)
score_rev = score_english(runeglish_rev)

print(f"Reversed unsolved + solved key (SUB): Score={score_rev}")
print(f"  First 200 chars: {runeglish_rev[:200]}")

# Strategy 6: Totient-based position skip
print("\n" + "="*70)
print("STRATEGY 6: Totient-Based Position Skip (φ(p) extraction)")
print("="*70)

def euler_totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

# Extract runes at positions that are totients of primes
totient_positions = [euler_totient(p) for p in get_primes_up_to(1000)]
totient_positions = sorted(set(p for p in totient_positions if p <= len(all_unsolved_runes)))
totient_indexed = [all_unsolved_runes[p-1] for p in totient_positions]
totient_runeglish = indices_to_runeglish([GP_RUNE_TO_INDEX[r] for r in totient_indexed])

print(f"Extracted {len(totient_indexed)} totient-indexed runes")
print(f"  Result: {totient_runeglish[:100]}")

# Strategy 7: Page-by-page with solved page offsets
print("\n" + "="*70)
print("STRATEGY 7: Page-by-Page with Matching Solved Pages")
print("="*70)

# Map unsolved pages 18-54 to solved pages 55+
for unsolved_page in [18, 19, 20, 21, 22]:
    solved_page = unsolved_page + 37  # Maps 18->55, 19->56, etc.
    
    unsolved_runes = read_runes(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{unsolved_page:02d}/runes.txt")
    solved_runes = read_runes(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{solved_page:02d}/runes.txt")
    
    if not unsolved_runes or not solved_runes:
        continue
    
    unsolved_idx = [GP_RUNE_TO_INDEX[r] for r in unsolved_runes]
    solved_idx = [GP_RUNE_TO_INDEX[r] for r in solved_runes]
    
    # SUB
    plain = [(unsolved_idx[i] - solved_idx[i % len(solved_idx)]) % 29 for i in range(len(unsolved_idx))]
    runeglish = indices_to_runeglish(plain)
    score = score_english(runeglish)
    
    print(f"Page {unsolved_page} XOR Page {solved_page}: Score={score}")
    print(f"  {runeglish[:80]}")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)

#!/usr/bin/env python3
"""
PRIME-BASED DECRYPTION EXPERIMENTS

Cicada loves primes. The Gematria Primus maps runes to consecutive primes.
What if the unsolved pages use prime-based shifts like Page 56?

Page 56 uses: shift = -(prime_n + 57) mod 29

Let's try variations of this.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Extended list of first 500 primes
def sieve_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

MANY_PRIMES = sieve_primes(5000)

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def word_score(text):
    WORDS = {'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
             'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
             'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
             'YOU', 'WE', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
             'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
             'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR',
             'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN', 'OF'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def decrypt_prime_shift(cipher_indices, constant, start_prime_idx=0):
    """Page 56 style: shift = -(prime_n + constant) mod 29"""
    result = []
    for i, c in enumerate(cipher_indices):
        prime_idx = (start_prime_idx + i) % len(MANY_PRIMES)
        shift = -(MANY_PRIMES[prime_idx] + constant) % 29
        decrypted = (c + shift) % 29
        result.append(idx_to_letter(decrypted))
    return ''.join(result)

def decrypt_totient_shift(cipher_indices, constant):
    """Use Euler's totient of primes as shift"""
    result = []
    for i, c in enumerate(cipher_indices):
        # totient(prime) = prime - 1
        prime = MANY_PRIMES[i % len(MANY_PRIMES)]
        shift = -(prime - 1 + constant) % 29
        decrypted = (c + shift) % 29
        result.append(idx_to_letter(decrypted))
    return ''.join(result)

def decrypt_prime_index_shift(cipher_indices, constant):
    """Use prime index as shift"""
    result = []
    for i, c in enumerate(cipher_indices):
        shift = -(i + constant) % 29  # Just use position
        decrypted = (c + shift) % 29
        result.append(idx_to_letter(decrypted))
    return ''.join(result)

def main():
    pages = load_pages()
    
    print("=" * 80)
    print("PRIME-BASED DECRYPTION TESTS")
    print("=" * 80)
    
    # First verify Page 56 method works
    if 56 in pages:
        cipher = [rune_to_idx(r) for r in pages[56]]
        text = decrypt_prime_shift(cipher, 57)
        print(f"\nPage 56 (constant=57): {text[:80]}...")
        print(f"Score: {word_score(text)}")
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("\n" + "=" * 80)
    print("TEST 1: PAGE 56 METHOD WITH DIFFERENT CONSTANTS")
    print("=" * 80)
    
    for pg_num in unsolved[:5]:
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_const = 0
        best_text = ""
        
        for constant in range(-100, 150):
            text = decrypt_prime_shift(cipher, constant)
            score = word_score(text)
            
            if score > best_score:
                best_score = score
                best_const = constant
                best_text = text
        
        print(f"\nPage {pg_num}: constant={best_const}, score={best_score}")
        print(f"  {best_text[:70]}...")
        
        # Check if constant is related to page number
        if best_const == pg_num or best_const == pg_num + 57 or best_const == pg_num - 57:
            print(f"  *** PATTERN: constant related to page number!")
    
    print("\n" + "=" * 80)
    print("TEST 2: PAGE NUMBER AS CONSTANT")
    print("=" * 80)
    
    for pg_num in unsolved:
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Try constant = page_number
        text = decrypt_prime_shift(cipher, pg_num)
        score = word_score(text)
        
        if score >= 15:
            print(f"Page {pg_num} (constant={pg_num}): score={score}")
            print(f"  {text[:70]}...")
        
        # Try constant = page_number + 57
        text = decrypt_prime_shift(cipher, pg_num + 57)
        score = word_score(text)
        
        if score >= 15:
            print(f"Page {pg_num} (constant={pg_num}+57={pg_num+57}): score={score}")
            print(f"  {text[:70]}...")
    
    print("\n" + "=" * 80)
    print("TEST 3: STARTING FROM DIFFERENT PRIME INDEX")
    print("=" * 80)
    
    for pg_num in [28]:  # Focus on Page 28
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        for constant in range(0, 100):
            for start_idx in range(100):
                text = decrypt_prime_shift(cipher, constant, start_idx)
                score = word_score(text)
                
                if score > best_score:
                    best_score = score
                    best_config = (constant, start_idx)
                    best_text = text
        
        print(f"\nPage {pg_num}: constant={best_config[0]}, start_idx={best_config[1]}, score={best_score}")
        print(f"  {best_text[:70]}...")
    
    print("\n" + "=" * 80)
    print("TEST 4: ADDITIVE PRIME CIPHER (Running sum of primes)")
    print("=" * 80)
    
    for pg_num in unsolved[:5]:
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        # Try: shift[i] = sum of first (i+offset) primes mod 29
        for offset in range(-50, 50):
            result = []
            for i, c in enumerate(cipher):
                idx = max(0, i + offset)
                if idx < len(MANY_PRIMES):
                    cumsum = sum(MANY_PRIMES[:idx+1])
                else:
                    cumsum = sum(MANY_PRIMES)
                shift = -cumsum % 29
                decrypted = (c + shift) % 29
                result.append(idx_to_letter(decrypted))
            text = ''.join(result)
            score = word_score(text)
            
            if score > best_score:
                best_score = score
                best_config = offset
                best_text = text
        
        if best_score >= 10:
            print(f"Page {pg_num}: offset={best_config}, score={best_score}")
            print(f"  {best_text[:70]}...")

if __name__ == "__main__":
    main()

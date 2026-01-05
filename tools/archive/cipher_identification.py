#!/usr/bin/env python3
"""
CIPHER IDENTIFICATION
=====================

Solved pages: Standard Vigenère with master key
Unsolved pages: Something different

Let's analyze what makes pages solvable vs unsolvable.
Then test the specific ciphers Cicada has used before:
1. Atbash
2. Running key with specific text
3. Gematria-based transformation
4. Hill cipher
5. Totient cipher
"""

import re
from pathlib import Path
import numpy as np

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def word_score(text):
    score = 0
    words = {
        'THE': 9, 'AND': 9, 'THAT': 12, 'HAVE': 12, 'FOR': 9, 'NOT': 9, 'WITH': 12, 'THIS': 12,
        'THERE': 15, 'THEIR': 15, 'THEY': 12, 'THEM': 12, 'THEN': 12, 'THESE': 15,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
        'SELF': 12, 'SOUL': 12, 'MIND': 12, 'KNOW': 12, 'KNOWLEDGE': 27, 'BEING': 15,
        'YOU': 9, 'YOUR': 12, 'YOURSELF': 24, 'ONE': 9, 'ALL': 9, 'WAY': 9,
        'MUST': 12, 'WILL': 12, 'BECOME': 18, 'UNDERSTAND': 30,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
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

def atbash(indices):
    """Atbash cipher: reverse the alphabet"""
    return (28 - indices) % 29

def totient_decrypt(indices, key_ext):
    """Totient function based decryption"""
    # Apply Euler's totient to each position
    n = len(indices)
    totients = []
    for i in range(n):
        # Totient of primes is p-1
        gem_val = GEMATRIA[indices[i]]
        if gem_val == 2:
            tot = 1
        else:
            tot = gem_val - 1  # Simplified for primes
        totients.append(tot % 29)
    
    totients = np.array(totients)
    return (indices - totients) % 29

def double_key_decrypt(indices, key_ext):
    """Apply key twice"""
    first = (indices - key_ext) % 29
    second = (first - key_ext) % 29
    return second

def affine_gematria(indices):
    """Use Gematria value as affine parameter"""
    result = []
    for idx in indices:
        gem = GEMATRIA[idx]
        # Affine: (a*x + b) mod 29
        # Use gem as 'a', position as 'b'
        a = gem % 29
        if np.gcd(a, 29) != 1:
            a = (a + 1) % 29  # Ensure coprime
        result.append((a * idx + gem) % 29)
    return np.array(result)

def gematria_mod_decrypt(indices, key_ext):
    """Subtract Gematria value from each rune"""
    gem_values = np.array([GEMATRIA[i] % 29 for i in indices])
    return (indices - gem_values - key_ext) % 29

def running_key_parable(indices, key_ext):
    """Use decoded Parable text as running key"""
    parable = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIVINITY"
    
    running_key = []
    for i, c in enumerate(parable):
        for idx, letter in enumerate(LETTERS):
            if c == letter[0]:
                running_key.append(idx)
                break
        else:
            running_key.append(0)
    
    running_key = np.array(running_key[:len(indices)], dtype=np.int32)
    if len(running_key) < len(indices):
        running_key = np.tile(running_key, (len(indices) // len(running_key) + 1))[:len(indices)]
    
    return (indices - running_key - key_ext) % 29

def main():
    pages = load_pages()
    
    print("="*70)
    print("CIPHER IDENTIFICATION")
    print("="*70)
    
    # First, analyze solved vs unsolved pages
    solved_pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]  # approximate
    unsolved_pages = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("\n--- Testing standard key on all pages ---")
    for pg_num in sorted(pages.keys())[:60]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        status = "SOLVED" if score >= 200 else ("PARTIAL" if score >= 100 else "UNSOLVED")
        if pg_num in unsolved_pages or score >= 150:
            print(f"Page {pg_num}: {score} [{status}]")
            if score >= 150:
                print(f"  {text[:60]}")
    
    # Now test different ciphers on unsolved pages
    print("\n" + "="*70)
    print("TESTING ALTERNATIVE CIPHERS ON UNSOLVED PAGES")
    print("="*70)
    
    best_results = []
    
    for pg_num in unsolved_pages:
        if pg_num not in pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        
        # 1. Atbash only
        atbashed = atbash(pg_idx)
        text = indices_to_text(atbashed)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Atbash only", text[:60]))
        
        # 2. Atbash + key
        atbashed = atbash(pg_idx)
        decrypted = (atbashed - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Atbash + key", text[:60]))
        
        # 3. Key + Atbash
        keyed = (pg_idx - key_ext) % 29
        atbashed = atbash(keyed)
        text = indices_to_text(atbashed)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Key + Atbash", text[:60]))
        
        # 4. Totient
        decrypted = totient_decrypt(pg_idx, key_ext)
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Totient + key", text[:60]))
        
        # 5. Double key
        decrypted = double_key_decrypt(pg_idx, key_ext)
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Double key", text[:60]))
        
        # 6. Gematria mod decrypt
        decrypted = gematria_mod_decrypt(pg_idx, key_ext)
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Gematria mod + key", text[:60]))
        
        # 7. Running key with Parable
        decrypted = running_key_parable(pg_idx, key_ext)
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Running key (Parable) + key", text[:60]))
        
        # 8. Reverse + key
        reversed_idx = pg_idx[::-1]
        decrypted = (reversed_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Reverse + key", text[:60]))
        
        # 9. Interleaved reading + key
        n = len(pg_idx)
        half = n // 2
        even_count = (n + 1) // 2
        odd_count = n // 2
        interleaved = np.zeros(n, dtype=np.int32)
        interleaved[0::2] = pg_idx[:even_count]
        interleaved[1::2] = pg_idx[even_count:even_count + odd_count]
        decrypted = (interleaved - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "Interleave + key", text[:60]))
        
        # 10. XOR with key instead of subtract
        xored = pg_idx ^ key_ext
        decrypted = xored % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 100:
            best_results.append((score, pg_num, "XOR key", text[:60]))
    
    # Summary
    print("\nBest results from alternative ciphers:")
    best_results.sort(reverse=True)
    for score, pg, method, text in best_results[:15]:
        print(f"Score {score}: Page {pg} - {method}")
        print(f"  {text}")
    
    # Now test if unsolved pages need a DIFFERENT key
    print("\n" + "="*70)
    print("SEARCHING FOR ALTERNATIVE KEY DERIVATION")
    print("="*70)
    
    # What if the key for unsolved pages is derived differently?
    # Maybe it's the key shifted by page number?
    
    for pg_num in [27, 30, 31, 46, 47]:
        if pg_num not in pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Shift key by page number
        shifted_key = np.roll(MASTER_KEY, pg_num)
        key_ext = np.tile(shifted_key, (n // 95 + 1))[:n]
        
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Page {pg_num} with key shifted by {pg_num}: {score}")
        
        # Try adding page number to key
        modified_key = (MASTER_KEY + pg_num) % 29
        key_ext = np.tile(modified_key, (n // 95 + 1))[:n]
        
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Page {pg_num} with key + {pg_num}: {score}")
        
        # XOR page number with key
        modified_key = (MASTER_KEY ^ pg_num) % 29
        key_ext = np.tile(modified_key, (n // 95 + 1))[:n]
        
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Page {pg_num} with key XOR {pg_num}: {score}")
        print()

if __name__ == "__main__":
    main()

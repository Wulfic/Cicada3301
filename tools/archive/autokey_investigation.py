#!/usr/bin/env python3
"""
Advanced Autokey and Gematria XOR Investigation

The flat IoC (~1.0) strongly suggests the cipher creates a one-time-pad-like effect.
This could be achieved by:
1. Autokey cipher (plaintext feeds back into key)
2. Gematria-based cipher where prime values are used for XOR/modular arithmetic
3. A combination approach

Let's systematically test these.
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
    return ''.join(IDX_TO_LETTER[int(i) % 29] for i in indices)

def text_to_indices(text):
    """Convert letter text to indices, handling digraphs"""
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        found = False
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
                i += 1
    return np.array(indices, dtype=np.int32)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

# Common words for scoring
COMMON_WORDS = ['THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'YOU', 'ARE',
                'NOT', 'ME', 'WE', 'BE', 'OR', 'AN', 'HE', 'AS', 'DO', 'AT',
                'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'HAVE', 'WITH', 'WHAT',
                'INSTAR', 'PARABLE', 'EMERGE', 'DIVINITY', 'WITHIN', 'SURFACE', 
                'CICADA', 'PRIME', 'WISDOM', 'TRUTH', 'SEEK', 'FIND', 'SHED']

def score_text(text):
    score = 0
    text_upper = text.upper()
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word)
    return score

def autokey_decrypt(cipher, initial_key):
    """
    Autokey cipher: initial_key is used first, then plaintext extends the key
    C[i] = P[i] + K[i] mod 29
    P[i] = C[i] - K[i] mod 29
    K[i] = initial_key[i] for i < len(initial_key), else P[i-len(initial_key)]
    """
    n = len(cipher)
    key_len = len(initial_key)
    plaintext = np.zeros(n, dtype=np.int32)
    
    for i in range(n):
        if i < key_len:
            k = initial_key[i]
        else:
            k = plaintext[i - key_len]
        plaintext[i] = (cipher[i] - k) % 29
    
    return plaintext

def gematria_autokey_decrypt(cipher, initial_key):
    """
    Gematria autokey: use the PRIME VALUE of the plaintext character as the key
    C[i] = P[i] + PRIME[K[i]] mod 29 (during encryption)
    P[i] = C[i] - PRIME[K[i]] mod 29 (during decryption)
    K[i] = initial_key[i] for i < len(initial_key), else P[i-len(initial_key)]
    """
    n = len(cipher)
    key_len = len(initial_key)
    plaintext = np.zeros(n, dtype=np.int32)
    
    for i in range(n):
        if i < key_len:
            k = initial_key[i]
        else:
            k = plaintext[i - key_len]
        # Use the prime value of k (mod 29)
        prime_k = PRIMES[k % 29] % 29
        plaintext[i] = (cipher[i] - prime_k) % 29
    
    return plaintext

def progressive_autokey(cipher, initial_key_text):
    """
    Test autokey with different offsets for the key
    """
    initial_key = text_to_indices(initial_key_text)
    if len(initial_key) == 0:
        return []
    
    results = []
    
    for offset in range(29):
        key_shifted = (initial_key + offset) % 29
        plaintext = autokey_decrypt(cipher, key_shifted)
        text = indices_to_text(plaintext)
        ioc = calculate_ioc(plaintext)
        score = score_text(text)
        
        if ioc > 1.1 or score > 15:
            results.append((ioc + score/100, offset, text[:60], ioc, score))
    
    return results

def main():
    print("="*70)
    print("ADVANCED AUTOKEY AND GEMATRIA INVESTIGATION")
    print("="*70)
    
    pages = load_pages()
    
    # Known good text from Page 57 (The Parable)
    parable = "PARABLELIKETHEINSTARTUNNELINGTOTHESURFACEWEMUSTSHEDO"
    
    # Common initial key guesses
    initial_keys = [
        'THE', 'AND', 'INSTAR', 'PARABLE', 'DIVINITY', 'CICADA',
        'TRUTH', 'WISDOM', 'EMERGE', 'WITHIN', 'SURFACE',
        'F', 'U', 'TH', 'A', 'I', 'E',  # Single runes
        'AN', 'IN', 'IT', 'OF', 'TO', 'IS', 'AS', 'OR',  # Common short words
    ]
    
    all_results = []
    
    print("\n" + "="*70)
    print("TESTING AUTOKEY CIPHER WITH VARIOUS INITIAL KEYS")
    print("="*70 + "\n")
    
    for page_num in sorted(pages.keys()):
        if page_num == 57 or page_num == 56:  # Skip known
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        page_best = []
        
        # Test regular autokey
        for key_text in initial_keys:
            results = progressive_autokey(cipher, key_text)
            for result in results:
                score, offset, text, ioc, word_score = result
                page_best.append((score, f'autokey-{key_text}-off{offset}', text, ioc, word_score))
        
        # Test gematria autokey
        for key_text in initial_keys:
            initial_key = text_to_indices(key_text)
            if len(initial_key) == 0:
                continue
            
            for offset in range(29):
                key_shifted = (initial_key + offset) % 29
                plaintext = gematria_autokey_decrypt(cipher, key_shifted)
                text = indices_to_text(plaintext)
                ioc = calculate_ioc(plaintext)
                score = score_text(text)
                
                if ioc > 1.1 or score > 15:
                    combined = ioc + score/100
                    page_best.append((combined, f'gem-autokey-{key_text}-off{offset}', text[:60], ioc, score))
        
        if page_best:
            page_best.sort(reverse=True)
            best = page_best[0]
            all_results.append((best[0], page_num, best[1], best[2], best[3], best[4], n))
    
    # Sort and display
    all_results.sort(reverse=True)
    
    print("TOP 15 AUTOKEY RESULTS:\n")
    for combined, page, method, text, ioc, score, n in all_results[:15]:
        print(f"Page {page:2d} (n={n:3d}): {method}")
        print(f"  IoC={ioc:.4f}, word_score={score}, combined={combined:.4f}")
        print(f"  {text}")
        
        found = [w for w in COMMON_WORDS if w in text.upper()]
        if found:
            print(f"  Found: {', '.join(found)}")
        print()
    
    # Now test if Gematria XOR might work (using prime values)
    print("\n" + "="*70)
    print("GEMATRIA XOR CIPHER (Prime-based)")
    print("="*70 + "\n")
    
    all_results = []
    
    for page_num in sorted(pages.keys()):
        if page_num == 57 or page_num == 56:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        page_best = []
        
        # Test: C[i] XOR PRIME[i % 29] / 29
        for divisor in [1, 29, 7, 11, 13]:
            for offset in range(29):
                decrypted = np.array([
                    (cipher[i] ^ (PRIMES[i % 29] // divisor + offset)) % 29 
                    for i in range(n)
                ])
                text = indices_to_text(decrypted)
                ioc = calculate_ioc(decrypted)
                score = score_text(text)
                
                if ioc > 1.1 or score > 15:
                    combined = ioc + score/100
                    page_best.append((combined, f'xor-prime-div{divisor}-off{offset}', text[:60], ioc, score))
        
        # Test: C[i] XOR (PRIME[cipher[i]] mod 29)
        for offset in range(29):
            decrypted = np.array([
                (cipher[i] ^ (PRIMES[cipher[i]] + offset)) % 29 
                for i in range(n)
            ])
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            score = score_text(text)
            
            if ioc > 1.1 or score > 15:
                combined = ioc + score/100
                page_best.append((combined, f'xor-gem-off{offset}', text[:60], ioc, score))
        
        if page_best:
            page_best.sort(reverse=True)
            best = page_best[0]
            all_results.append((best[0], page_num, best[1], best[2], best[3], best[4], n))
    
    all_results.sort(reverse=True)
    
    print("TOP 10 XOR RESULTS:\n")
    for combined, page, method, text, ioc, score, n in all_results[:10]:
        print(f"Page {page:2d} (n={n:3d}): {method}")
        print(f"  IoC={ioc:.4f}, word_score={score}")
        print(f"  {text}")
        print()
    
    # Test Hill cipher (2x2 matrix)
    print("\n" + "="*70)
    print("HILL CIPHER (2x2 matrix)")
    print("="*70 + "\n")
    
    # Hill cipher uses matrix multiplication
    # For 2x2: [a b] [c1]   [a*c1 + b*c2]
    #          [c d] [c2] = [c*c1 + d*c2]
    
    # We need to try matrices that are invertible mod 29
    def hill_decrypt_2x2(cipher, matrix):
        # Calculate inverse matrix mod 29
        a, b, c, d = matrix
        det = (a*d - b*c) % 29
        if det == 0:
            return None
        
        # Find modular inverse of determinant
        det_inv = pow(det, -1, 29)
        
        # Inverse matrix
        inv_a = (d * det_inv) % 29
        inv_b = (-b * det_inv) % 29
        inv_c = (-c * det_inv) % 29
        inv_d = (a * det_inv) % 29
        
        # Decrypt pairs
        plaintext = []
        for i in range(0, len(cipher)-1, 2):
            c1, c2 = cipher[i], cipher[i+1]
            p1 = (inv_a * c1 + inv_b * c2) % 29
            p2 = (inv_c * c1 + inv_d * c2) % 29
            plaintext.extend([p1, p2])
        
        if len(cipher) % 2 == 1:
            plaintext.append(cipher[-1])  # Last char unchanged if odd length
        
        return np.array(plaintext, dtype=np.int32)
    
    all_results = []
    
    # Test some common matrix patterns
    test_matrices = []
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    if (a*d - b*c) % 29 != 0:  # Must be invertible
                        test_matrices.append((a, b, c, d))
    
    print(f"Testing {len(test_matrices)} Hill cipher matrices...")
    
    for page_num in [0, 15, 27, 28, 29, 30, 31, 40, 41, 42]:  # Test subset
        if page_num not in pages:
            continue
        
        cipher = runes_to_indices(pages[page_num])
        n = len(cipher)
        
        if n < 20:
            continue
        
        page_best = []
        
        for matrix in test_matrices[:1000]:  # Limit for speed
            decrypted = hill_decrypt_2x2(cipher, matrix)
            if decrypted is None:
                continue
            
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            score = score_text(text)
            
            if ioc > 1.3 or score > 20:
                combined = ioc + score/50
                page_best.append((combined, f'hill-{matrix}', text[:60], ioc, score))
        
        if page_best:
            page_best.sort(reverse=True)
            best = page_best[0]
            all_results.append((best[0], page_num, best[1], best[2], best[3], best[4], n))
    
    all_results.sort(reverse=True)
    
    print("\nTOP 10 HILL CIPHER RESULTS:\n")
    for result in all_results[:10]:
        combined, page, method, text, ioc, score, n = result
        print(f"Page {page:2d} (n={n:3d}): {method}")
        print(f"  IoC={ioc:.4f}, word_score={score}")
        print(f"  {text}")
        print()

if __name__ == "__main__":
    main()

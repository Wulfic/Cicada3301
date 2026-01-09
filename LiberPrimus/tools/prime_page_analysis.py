#!/usr/bin/env python3
"""
PRIME/TOTIENT PAGE KEY ATTACK

Based on Page 05's explicit hint:
"THE PRIMES ARE SACRED"
"THE TOTIENT FUNCTION IS SACRED"

This script tests if page numbers relate to keys through prime mathematics.
"""

from pathlib import Path
import math

# Gematria Primus
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

# First 100 primes
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 
          223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 
          293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 
          463, 467, 479, 487, 491, 499, 503, 509, 521, 523]

def euler_totient(n):
    """Euler's totient function φ(n)."""
    if n <= 0:
        return 0
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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def nth_prime(n):
    """Get nth prime (1-indexed)."""
    if n <= 0:
        return 0
    if n <= len(PRIMES):
        return PRIMES[n-1]
    return 0

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def load_page_runes(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None, None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        rune_text = f.read()
    
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    words = []
    current = []
    for c in rune_text:
        if c in RUNE_MAP:
            current.append(RUNE_MAP[c])
        elif c in '-. \n\r/•':
            if current:
                words.append(current)
                current = []
    if current:
        words.append(current)
    
    return cipher, words

def decrypt_with_shift(cipher, shift):
    """Simple shift decryption."""
    return [(c - shift) % 29 for c in cipher]

def decrypt_with_key_pattern(cipher, key_pattern_func):
    """Decrypt where key at position i is given by key_pattern_func(i)."""
    plain = []
    for i, c in enumerate(cipher):
        k = key_pattern_func(i)
        plain.append((c - k) % 29)
    return plain

def count_english_words(plain, word_boundaries):
    """Count how many words match common English patterns."""
    COMMON_WORDS = {
        'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
        'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
        'WE', 'THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 
        'WAS', 'ONE', 'OUR', 'OUT', 'ARE', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY',
        'NEW', 'NOW', 'OLD', 'SAY', 'SHE', 'TOO', 'TWO', 'WAY', 'WHO', 'YET',
        'THY', 'YEA', 'NAY', 'FIND', 'SEEK', 'TRUTH', 'LIGHT', 'WITHIN',
        'SELF', 'SOUL', 'MAN', 'MEN', 'MUST', 'WITH', 'THIS', 'THAT', 'FROM', 
        'HAVE', 'BEEN', 'WILL', 'WHAT', 'WHEN', 'YOUR', 'EACH', 'EVERY', 
        'THERE', 'THEIR', 'THESE', 'OTHER', 'WOULD', 'BEING', 'THING',
        'SOME', 'END', 'LIKE', 'INTO', 'THROUGH', 'GREAT', 'TOWARD', 'PATH'
    }
    
    words_found = []
    pos = 0
    for word_indices in word_boundaries:
        wlen = len(word_indices)
        if pos + wlen > len(plain):
            break
        word_text = indices_to_text(plain[pos:pos+wlen])
        if word_text in COMMON_WORDS:
            words_found.append(word_text)
        pos += wlen
    
    return words_found

def test_prime_based_keys(page_num):
    """Test various prime-based key derivations for a page."""
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - PRIME/TOTIENT ANALYSIS")
    print("=" * 70)
    
    cipher, words = load_page_runes(page_num)
    if cipher is None:
        print("Could not load page")
        return
    
    print(f"Cipher length: {len(cipher)}, Words: {len(words)}")
    print(f"\nPrime properties of page number {page_num}:")
    print(f"  Is prime: {is_prime(page_num)}")
    print(f"  φ({page_num}) = {euler_totient(page_num)}")
    print(f"  {page_num}th prime = {nth_prime(page_num)}")
    print(f"  φ({page_num}th prime) = {euler_totient(nth_prime(page_num))}")
    
    results = []
    
    # 1. Simple shift by page number
    shift = page_num
    plain = decrypt_with_shift(cipher, shift)
    found = count_english_words(plain, words)
    results.append(('Shift by page#', shift, len(found), found, indices_to_text(plain[:50])))
    
    # 2. Shift by φ(page_num)
    shift = euler_totient(page_num)
    plain = decrypt_with_shift(cipher, shift)
    found = count_english_words(plain, words)
    results.append((f'Shift by φ({page_num})', shift, len(found), found, indices_to_text(plain[:50])))
    
    # 3. Shift by nth prime
    shift = nth_prime(page_num) % 29
    plain = decrypt_with_shift(cipher, shift)
    found = count_english_words(plain, words)
    results.append((f'Shift by {page_num}th prime mod 29', shift, len(found), found, indices_to_text(plain[:50])))
    
    # 4. Shift by φ(nth prime)
    shift = euler_totient(nth_prime(page_num)) % 29
    plain = decrypt_with_shift(cipher, shift)
    found = count_english_words(plain, words)
    results.append((f'Shift by φ({page_num}th prime) mod 29', shift, len(found), found, indices_to_text(plain[:50])))
    
    # 5. Key = sequential primes mod 29
    def seq_prime_key(i):
        return PRIMES[i % len(PRIMES)] % 29
    plain = decrypt_with_key_pattern(cipher, seq_prime_key)
    found = count_english_words(plain, words)
    results.append(('Sequential primes mod 29', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 6. Key = φ(sequential primes) mod 29
    def seq_totient_key(i):
        return euler_totient(PRIMES[i % len(PRIMES)]) % 29
    plain = decrypt_with_key_pattern(cipher, seq_totient_key)
    found = count_english_words(plain, words)
    results.append(('φ(sequential primes) mod 29', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 7. Key = prime[i] starting from page_num'th prime
    def offset_prime_key(i):
        return PRIMES[(page_num + i) % len(PRIMES)] % 29
    plain = decrypt_with_key_pattern(cipher, offset_prime_key)
    found = count_english_words(plain, words)
    results.append((f'Primes starting at {page_num}th', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 8. Key combines page and position: (page * position) mod 29
    def combined_key(i):
        return (page_num * (i + 1)) % 29
    plain = decrypt_with_key_pattern(cipher, combined_key)
    found = count_english_words(plain, words)
    results.append((f'page * position mod 29', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 9. Key = (page + prime[i]) mod 29
    def page_plus_prime(i):
        return (page_num + PRIMES[i % len(PRIMES)]) % 29
    plain = decrypt_with_key_pattern(cipher, page_plus_prime)
    found = count_english_words(plain, words)
    results.append((f'{page_num} + prime[i] mod 29', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 10. Formula from Page 56: (cipher[i] - (prime[i] + 57)) mod 29
    def page56_formula(i):
        return (PRIMES[i % len(PRIMES)] + 57) % 29
    plain = decrypt_with_key_pattern(cipher, page56_formula)
    found = count_english_words(plain, words)
    results.append(('Page 56 formula: prime + 57', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 11. Try page-specific offset: (prime[i] + page_num) mod 29
    def page_offset_formula(i):
        return (PRIMES[i % len(PRIMES)] + page_num) % 29
    plain = decrypt_with_key_pattern(cipher, page_offset_formula)
    found = count_english_words(plain, words)
    results.append((f'prime[i] + {page_num}', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # 12. φ(prime) + page
    def totient_plus_page(i):
        return (euler_totient(PRIMES[i % len(PRIMES)]) + page_num) % 29
    plain = decrypt_with_key_pattern(cipher, totient_plus_page)
    found = count_english_words(plain, words)
    results.append((f'φ(prime[i]) + {page_num}', 'varying', len(found), found, indices_to_text(plain[:50])))
    
    # Sort by number of words found
    results.sort(key=lambda x: x[2], reverse=True)
    
    print("\n--- RESULTS (sorted by word count) ---")
    for method, shift, count, found, preview in results:
        if count > 0:
            print(f"\n{method} (shift={shift}):")
            print(f"  Words found ({count}): {', '.join(found[:10])}")
            print(f"  Preview: {preview}")
    
    return results

def main():
    print("PRIME/TOTIENT KEY ANALYSIS")
    print("Based on Page 05 hint: 'THE PRIMES ARE SACRED, THE TOTIENT FUNCTION IS SACRED'")
    print("=" * 70)
    
    # Test on unsolved pages
    for page_num in [17, 18, 19, 20, 21, 25, 30, 40, 50, 55]:
        test_prime_based_keys(page_num)

if __name__ == '__main__':
    main()

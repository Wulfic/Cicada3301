"""
Verify the φ(prime) cipher implementation by testing on known-solved pages 55 and 73.
These pages are documented as using this exact method.
"""

import os
from collections import Counter

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def totient(n):
    if n == 1:
        return 1
    result = n
    p = 2
    temp_n = n
    while p * p <= temp_n:
        if temp_n % p == 0:
            while temp_n % p == 0:
                temp_n //= p
            result -= result // p
        p += 1
    if temp_n > 1:
        result -= result // temp_n
    return result

def rune_to_index(rune):
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

def load_page(page_num):
    page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    subdir = f"page_{page_num:02d}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            runes = [c for c in content if c in GP_RUNES]
            return runes
    return []

def calculate_ioc(indices):
    n = len(indices)
    if n <= 1:
        return 0
    counts = Counter(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29

def indices_to_latin(indices):
    return ''.join(index_to_latin(i) for i in indices)

def apply_phi_prime_cipher(runes, operation='sub'):
    """
    φ(prime) cipher:
    - shift[i] = φ(prime_sequence[i]) mod 29
    - For primes: φ(p) = p - 1
    """
    primes = generate_primes(len(runes) * 2)
    result = []
    prime_idx = 0
    
    for rune in runes:
        cipher_idx = rune_to_index(rune)
        if cipher_idx is None:
            continue
        
        shift = totient(primes[prime_idx]) % 29
        if operation == 'sub':
            plain_idx = (cipher_idx - shift) % 29
        else:
            plain_idx = (cipher_idx + shift) % 29
        result.append(plain_idx)
        prime_idx += 1
    
    return result

def main():
    print("="*60)
    print("VERIFYING φ(prime) CIPHER ON KNOWN-SOLVED PAGES")
    print("="*60)
    
    # Test on Pages 55 and 73 (documented as using this method)
    for page_num in [55, 73]:
        runes = load_page(page_num)
        if not runes:
            print(f"\nPage {page_num}: Could not load")
            continue
        
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}: {len(runes)} runes")
        print(f"{'='*60}")
        
        # Test both operations
        for op in ['sub', 'add']:
            result = apply_phi_prime_cipher(runes, op)
            ioc = calculate_ioc(result)
            latin = indices_to_latin(result)
            
            print(f"\n{op.upper()}: IoC = {ioc:.4f}")
            print(f"Output: {latin[:200]}")
            
            # Check for known text
            if 'WITHIN' in latin or 'DEEP' in latin or 'WEB' in latin:
                print("*** MATCHES KNOWN SOLUTION ***")
            if 'END' in latin:
                print("Found 'END'")
    
    # Let's also check page 55 decoded.txt
    print("\n" + "="*60)
    print("CHECKING KNOWN DECODED TEXT FOR PAGE 55")
    print("="*60)
    decoded_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_55\decoded.txt"
    if os.path.exists(decoded_path):
        with open(decoded_path, 'r', encoding='utf-8') as f:
            print(f.read()[:500])

if __name__ == "__main__":
    main()

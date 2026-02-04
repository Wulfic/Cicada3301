"""
Test the CORRECT φ(prime) cipher from Pages 55, 73.
The key is: shift[i] = φ(prime_sequence[i]) mod 29
Where prime_sequence is 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...

This is different from my earlier (wrong) approach that used φ(GP_PRIME[cipher_rune]).
"""

import os
from collections import Counter

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
             31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
             73, 79, 83, 89, 97, 101, 103, 107, 109]

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    """Generate first 'count' prime numbers"""
    primes = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def totient(n):
    """Euler's totient function"""
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

def find_words(text, min_len=3):
    words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS',
        'HOW', 'ITS', 'LET', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO',
        'BOY', 'DID', 'SAY', 'SHE', 'TOO', 'USE', 'ODE', 'MET', 'BID', 'ALT',
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
        'DEAD', 'EACH', 'FIND', 'GIVE', 'GOOD', 'JUST', 'KNOW', 'LIKE', 'MADE',
        'SELF', 'SUCH', 'TAKE', 'THAN', 'THEM', 'THEN', 'TRUE', 'UNTO', 'UPON',
        'BEING', 'LIGHT', 'TRUTH', 'WITHIN', 'DIVINE', 'SACRED', 'SECRET',
        'THERE', 'THEIR', 'WHICH', 'WOULD', 'OTHER', 'THESE', 'FIRST', 'COULD',
        'LONE', 'EODE', 'SEFA', 'REAPER', 'AEON', 'PRIME', 'PILGRIM', 'ADEPT',
        'WISDOM', 'SEEK', 'FIND', 'WORD', 'WORK', 'PATH',
    ]
    found = []
    text_upper = text.upper()
    for word in words:
        if len(word) >= min_len and word in text_upper:
            found.append(word)
    return list(set(found))

def apply_phi_prime_cipher(runes, operation='sub', with_literal_f=False):
    """
    Correct φ(prime) cipher:
    - Generate prime sequence: 2, 3, 5, 7, 11, ...
    - shift[i] = φ(prime[i]) mod 29
    - For primes: φ(p) = p - 1
    - Plaintext = (Cipher - shift) mod 29
    
    With literal_f rule: if cipher is ᚠ and expected plaintext is F, output F and DON'T increment key.
    """
    primes = generate_primes(len(runes) * 2)  # Extra for literal F skips
    result = []
    prime_idx = 0
    
    for rune in runes:
        cipher_idx = rune_to_index(rune)
        if cipher_idx is None:
            continue
        
        if with_literal_f and cipher_idx == 0:  # ᚠ = F
            # Check if φ(prime[prime_idx]) mod 29 would produce F (index 0)
            shift = totient(primes[prime_idx]) % 29
            expected = (cipher_idx - shift) % 29
            if expected == 0:  # Would decrypt to F anyway
                result.append(0)  # Output F
                prime_idx += 1
            else:
                # Literal F rule: output F without incrementing
                result.append(0)
                # DON'T increment prime_idx
        else:
            shift = totient(primes[prime_idx]) % 29
            if operation == 'sub':
                plain_idx = (cipher_idx - shift) % 29
            else:  # add
                plain_idx = (cipher_idx + shift) % 29
            result.append(plain_idx)
            prime_idx += 1
    
    return result

def main():
    print("="*60)
    print("CORRECT φ(prime) CIPHER TEST")
    print("Method: shift[i] = φ(prime_sequence[i]) mod 29")
    print("This worked on Pages 55 and 73!")
    print("="*60)
    
    # Test on Pages 21-30
    for page_num in range(20, 35):
        runes = load_page(page_num)
        if not runes or len(runes) < 20:
            continue
        
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}: {len(runes)} runes")
        print(f"{'='*60}")
        
        # Test without literal F
        result_sub = apply_phi_prime_cipher(runes, 'sub', with_literal_f=False)
        result_add = apply_phi_prime_cipher(runes, 'add', with_literal_f=False)
        
        ioc_sub = calculate_ioc(result_sub)
        ioc_add = calculate_ioc(result_add)
        
        latin_sub = indices_to_latin(result_sub)
        latin_add = indices_to_latin(result_add)
        
        words_sub = find_words(latin_sub)
        words_add = find_words(latin_add)
        
        print(f"SUB: IoC={ioc_sub:.4f}, words={words_sub[:5]}")
        print(f"     {latin_sub[:80]}")
        print(f"ADD: IoC={ioc_add:.4f}, words={words_add[:5]}")
        print(f"     {latin_add[:80]}")
        
        # Test WITH literal F rule
        result_sub_f = apply_phi_prime_cipher(runes, 'sub', with_literal_f=True)
        ioc_sub_f = calculate_ioc(result_sub_f)
        latin_sub_f = indices_to_latin(result_sub_f)
        words_sub_f = find_words(latin_sub_f)
        
        if ioc_sub_f != ioc_sub or words_sub_f != words_sub:
            print(f"SUB+F: IoC={ioc_sub_f:.4f}, words={words_sub_f[:5]}")
            print(f"       {latin_sub_f[:80]}")
        
        # Highlight promising results
        if ioc_sub > 1.4 or ioc_add > 1.4:
            print(f"*** ELEVATED IoC DETECTED ***")
        if len(words_sub) >= 3 or len(words_add) >= 3:
            print(f"*** MULTIPLE WORDS FOUND ***")

if __name__ == "__main__":
    main()

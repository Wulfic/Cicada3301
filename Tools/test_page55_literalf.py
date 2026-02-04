"""
Test φ(prime) cipher WITH the Literal F rule on Page 55.
The Literal F rule: If cipher = F rune AND plaintext would be F, skip the key increment.
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

def indices_to_latin(indices):
    return ''.join(index_to_latin(i) for i in indices)

def apply_phi_prime_with_literal_f(runes):
    """
    φ(prime) cipher with Literal F rule:
    - If cipher = F (index 0) AND φ(prime[prime_idx]) % 29 == 0, 
      output F and DON'T increment prime_idx
    - Otherwise, normal decryption
    """
    primes = generate_primes(len(runes) * 2)
    result = []
    prime_idx = 0
    
    for i, rune in enumerate(runes):
        cipher_idx = rune_to_index(rune)
        if cipher_idx is None:
            continue
        
        shift = totient(primes[prime_idx]) % 29
        plain_idx = (cipher_idx - shift) % 29
        
        # Check if this is a literal F
        if cipher_idx == 0 and plain_idx == 0:
            # Literal F: output F, DON'T increment prime counter
            result.append(0)
            # DON'T increment prime_idx
            print(f"  Pos {i}: Literal F detected (prime_idx stays {prime_idx})")
        else:
            result.append(plain_idx)
            prime_idx += 1
    
    return result

def apply_phi_prime_scan_for_literal_f(runes):
    """
    Try to find where literal F positions are by testing different possibilities.
    The challenge is we don't know which Fs are literal until we solve it.
    """
    primes = generate_primes(len(runes) * 2)
    
    # First, do a straight decode to see structure
    result = []
    prime_idx = 0
    for rune in runes:
        cipher_idx = rune_to_index(rune)
        if cipher_idx is None:
            continue
        shift = totient(primes[prime_idx]) % 29
        plain_idx = (cipher_idx - shift) % 29
        result.append(plain_idx)
        prime_idx += 1
    
    return result

def main():
    print("="*60)
    print("PAGE 55 WITH LITERAL F RULE")
    print("="*60)
    
    runes = load_page(55)
    print(f"Rune count: {len(runes)}")
    
    # Find all F rune positions
    f_positions = [i for i, r in enumerate(runes) if r == 'ᚠ']
    print(f"F rune positions: {f_positions}")
    
    # Test without literal F
    print("\n--- WITHOUT Literal F ---")
    primes = generate_primes(100)
    result = []
    prime_idx = 0
    for rune in runes:
        cipher_idx = rune_to_index(rune)
        if cipher_idx is None:
            continue
        shift = totient(primes[prime_idx]) % 29
        plain_idx = (cipher_idx - shift) % 29
        result.append(plain_idx)
        prime_idx += 1
    print(indices_to_latin(result))
    
    # Test WITH automatic literal F detection
    print("\n--- WITH Literal F (auto-detect) ---")
    result = apply_phi_prime_with_literal_f(runes)
    print(indices_to_latin(result))
    
    # Manual test: skip F at position 56 (the documented literal F position)
    # Note: position 56 in the message, not in the runes array
    print("\n--- MANUAL: Skip key at specific F positions ---")
    # According to README, position 56 is literal F
    primes = generate_primes(100)
    result = []
    prime_idx = 0
    for i, rune in enumerate(runes):
        cipher_idx = rune_to_index(rune)
        if cipher_idx is None:
            continue
        
        shift = totient(primes[prime_idx]) % 29
        plain_idx = (cipher_idx - shift) % 29
        result.append(plain_idx)
        
        # Check if this should be a literal F (skip increment if so)
        # According to the docs, we skip increment when cipher=F and plaintext=F
        if cipher_idx == 0 and plain_idx == 0:
            pass  # Don't increment
        else:
            prime_idx += 1
    
    print(indices_to_latin(result))
    
    # Expected: "AN END WITHIN THE DEEP WEB THERE EXISTS A PAGE..."
    expected = "ANENDWITHINTHEDEEPWEBTHEREEXISTSAPAGETHATHASHESTORE..."
    
    # Let's try various literal F skip patterns
    print("\n--- TESTING DIFFERENT SKIP PATTERNS ---")
    for skip_positions in [
        [],  # No skips
        [0],  # Skip first F only
        [1],  # Skip second F
        [0, 1],  # Skip first two Fs
        [1, 2],
    ]:
        primes = generate_primes(100)
        result = []
        prime_idx = 0
        f_count = 0
        for i, rune in enumerate(runes):
            cipher_idx = rune_to_index(rune)
            if cipher_idx is None:
                continue
            
            if cipher_idx == 0:  # F rune
                if f_count in skip_positions:
                    # Literal F - output F without key
                    result.append(0)
                    f_count += 1
                    continue  # Don't use a key
                f_count += 1
            
            shift = totient(primes[prime_idx]) % 29
            plain_idx = (cipher_idx - shift) % 29
            result.append(plain_idx)
            prime_idx += 1
        
        text = indices_to_latin(result)
        if 'ANEND' in text or 'WITHIN' in text:
            print(f"Skip {skip_positions}: MATCHES! {text[:60]}")
        else:
            print(f"Skip {skip_positions}: {text[:60]}")

if __name__ == "__main__":
    main()

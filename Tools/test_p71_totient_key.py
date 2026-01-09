
import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
ENGLISH_MAP = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H',
    9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T',
    17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A',
    25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    if not os.path.exists(path): return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '').replace(' ', '').replace('•', '')

def runes_to_vals(runes):
    return [RUNE_MAP[r] for r in runes if r in RUNE_MAP]

def vals_to_eng(vals):
    return "".join([ENGLISH_MAP[v] for v in vals])

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def totient(n):
    # For prime p, phi(p) = p - 1
    # For general n, we don't strictly need it if keys are always primes.
    # The doc says "phi(prime) Shift Cipher".
    # Assuming key is phi(P_i) where P_i is the i-th prime.
    # Since P_i is prime, phi(P_i) = P_i - 1.
    return n - 1

def generate_primes_totients(count):
    primes = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    
    totients = [(p - 1) for p in primes]
    return totients

def main():
    target_pg = "71"
    cipher_runes = load_runes(target_pg)
    cipher = runes_to_vals(cipher_runes)
    
    N = len(cipher)
    keys = generate_primes_totients(N + 100) # Buffer
    
    # Try Standard Vigenere: P = (C - K) % 29
    # Try Variant Beaufort: P = (K - C) % 29
    # Try AutoKey Vigenere? (But key is prime stream? No, running key.)
    
    target_vals = [23, 18, 5, 4, 26, 13, 16, 10, 3, 9] # DECRYPTION
    
    modes = [
        ("Vigenere (C - K)", lambda c, k: (c - k) % 29),
        ("Beaufort (K - C)", lambda c, k: (k - c) % 29),
        ("Variant (C + K)", lambda c, k: (c + k) % 29)
    ]
    
    # Check match at index 60
    # Key indices:
    # 1. Key starts at 0. (Standard)
    # 2. Key continues from previous pages? (Like Running Key across book)
    
    # Test 1: Key starts at 0 for this page.
    print("Testing Totient Key (Key starts at index 0)...")
    
    for name, func in modes:
        match = True
        for j in range(len(target_vals)):
            idx = 60 + j
            c = cipher[idx]
            k = keys[idx] # Key aligned with cipher
            p = func(c, k)
            if p != target_vals[j]:
                match = False
                break
        if match:
            print(f"MATCH FOUND with {name}!")
            
    # Test 2: Key is a sliding window of the Totient Stream (Running Key)
    # i.e. key[0] corresponds to totient(prime[offset])
    # The stream of primes is infinite.
    # Maybe we are at the N-th prime of the whole book?
    # Page 71. Previous pages have ~300 runes each?
    # 71 * 300 ~ 21000.
    # Let's verify 'DECRYPTION' against a sliding window of totients.
    
    print("Testing Totient Key Stream (Sliding Window)...")
    # Generate large stream
    MAX_PRIME_IDX = 30000 
    big_keys = generate_primes_totients(MAX_PRIME_IDX)
    
    # We look for a subsequence in 'big_keys' that decrypts the target segment
    # target segment C: ...
    # target P: ...
    # Expected K: ...
    # Look for Expected K in big_keys.
    
    cipher_segment = cipher[60:70]
    
    expected_keys_vig = [(c - p) % 29 for c, p in zip(cipher_segment, target_vals)]
    expected_keys_beau = [(p + c) % 29 for c, p in zip(cipher_segment, target_vals)] # K = P+C for K-C=P
    expected_keys_var = [(p - c) % 29 for c, p in zip(cipher_segment, target_vals)] # K = P-C? No. P = C+K => K = P-C.
    
    # Wait, Variant (C+K)=P => K = (P-C).
    # Beaufort (K-C)=P => K = (P+C).
    # Vigenere (C-K)=P => K = (C-P).
    
    search_targets = [
        ("Vigenere", expected_keys_vig),
        ("Beaufort", expected_keys_beau),
        ("Variant", [(t - c) % 29 for c, t in zip(cipher_segment, target_vals)]) # K = P - C
    ]
    
    for name, target_k in search_targets:
        # Search for target_k in big_keys
        # big_keys is list of ints
        # Naive search
        found = False
        for i in range(len(big_keys) - len(target_k)):
            if big_keys[i : i+len(target_k)] == target_k:
                print(f"MATCH FOUND for {name} Key at Prime Index {i}!")
                found = True
                
                # Decrypt preview
                start_k = i - 60
                final_plain = []
                for x in range(len(cipher)):
                    k_idx = start_k + x
                    if k_idx < 0: p=0
                    elif k_idx >= len(big_keys): p=0
                    else:
                        k = big_keys[k_idx]
                        if name == "Vigenere": p = (cipher[x] - k) % 29
                        elif name == "Beaufort": p = (k - cipher[x]) % 29
                        else: p = (cipher[x] + k) % 29 # Wait, checks are hard
                        # Just use the matched logic
                # Actually, reconstruct
                break

if __name__ == "__main__":
    main()

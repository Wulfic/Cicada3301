
import os
import sys

# GP Runes Map
GP_RUNES = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
    'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
    'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

INDEX_TO_LATIN = {v: k for k, v in GP_RUNES.items()}

# Constants
MOD = 29
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229]
PHI_DIGITS = [1, 6, 1, 8, 0, 3, 3, 9, 8, 8, 7, 4, 9, 8, 9, 4, 8, 4, 8, 2, 0, 4, 5, 8, 6, 8, 3, 4, 3, 6, 5, 6, 3, 8, 1, 1, 7, 7, 2, 0, 3, 0, 9, 1, 7, 9, 8, 0, 5, 7]

def load_runes(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return [GP_RUNES[r] for r in content.replace(' ', '').split('-') if r in GP_RUNES or (len(r) > 0 and r in GP_RUNES)]

def load_runes_str(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    # Manual parsing because raw format might be just runes
    indices = []
    i = 0
    # Create reverse map sorted by length desc
    sorted_runes = sorted(GP_RUNES.keys(), key=len, reverse=True)
    
    while i < len(content):
        match = False
        for r in sorted_runes:
            if content.startswith(r, i):
                indices.append(GP_RUNES[r])
                i += len(r)
                match = True
                break
        if not match:
            # Skip unknown chars (newlines etc)
            i += 1
    return indices

def indices_to_text(indices):
    return ''.join([INDEX_TO_LATIN.get(x, '?') for x in indices])


def decrypt_vigenere(ciphertext, key, mode='SUB'):
    res = []
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        k = key[i % key_len]
        if mode == 'SUB':
            p = (c - k) % MOD
        elif mode == 'ADD':
            p = (c + k) % MOD
        res.append(p)
    return res

def decrypt_porta(ciphertext, key):
    # Re-implement logic from master_cipher.py
    result = []
    key_len = len(key)
    half = MOD // 2 # 14
    
    for i, c in enumerate(ciphertext):
        k = key[i % key_len]
        tableau_row = k // 2
        
        if c < half:
            p = (c + tableau_row + half) % MOD
        else:
            p = (c - tableau_row - half) % MOD
        result.append(p)
    return result

def text_to_key(text):
    text = text.upper()
    return [GP_RUNES[x] for x in text if x in GP_RUNES] # Simplified assumption, assuming single chars. Actually need parsing.
    
    # Better text_to_key
    res = []
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i:i+2] in GP_RUNES:
            res.append(GP_RUNES[text[i:i+2]])
            i += 2
        elif text[i] in GP_RUNES:
            res.append(GP_RUNES[text[i]])
            i += 1
        else:
            i += 1
    return res

# --- MAIN ---

print("=== VERIFYING PAGE 55 ===")
# Key: PHI_PRIME_S0 = PRIMES[d] for d in PHI_DIGITS
key_phi_prime = [PRIMES[d] % MOD for d in PHI_DIGITS[:50] if d < len(PRIMES)]
data_55 = load_runes_str(55)
# Try SUB
if data_55:
    pt_55 = decrypt_vigenere(data_55, key_phi_prime, 'SUB')
    print(f"Page 55 (PHI_PRIME_S0, SUB): {indices_to_text(pt_55)[:100]}...")

print("\n=== INVESTIGATING PAGE 33 ===")
key_phi_prime_rev = key_phi_prime[::-1]
data_33 = load_runes_str(33)
if data_33:
    pt_33 = decrypt_vigenere(data_33, key_phi_prime_rev, 'ADD')
    print(f"Page 33 (PHI_PRIME_S0_REV, ADD): {indices_to_text(pt_33)[:200]}...")

print("\n=== INVESTIGATING PAGE 25 (High Score PORTA) ===")
# Key: DESTINY
key_destiny = text_to_key("DESTINY")
data_25 = load_runes_str(25)
if data_25:
    pt_25 = decrypt_porta(data_25, key_destiny)
    print(f"Page 25 (PORTA_DESTINY): {indices_to_text(pt_25)[:200]}...")


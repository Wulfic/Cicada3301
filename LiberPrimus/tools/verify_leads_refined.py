import os
import sys

# Define Gematria
GEMATRIA = {
    'ᚠ': (0, 'F'), 'ᚢ': (1, 'U'), 'ᚦ': (2, 'TH'), 'ᚩ': (3, 'O'), 'ᚱ': (4, 'R'), 
    'ᚳ': (5, 'C'), 'ᚷ': (6, 'G'), 'ᚹ': (7, 'W'), 'ᚻ': (8, 'H'), 'ᚾ': (9, 'N'), 
    'ᛁ': (10, 'I'), 'ᛂ': (11, 'J'), 'ᛇ': (12, 'EO'), 'ᛈ': (13, 'P'), 'ᛉ': (14, 'X'), 
    'ᛋ': (15, 'S'), 'ᛏ': (16, 'T'), 'ᛒ': (17, 'B'), 'ᛖ': (18, 'E'), 'ᛗ': (19, 'M'), 
    'ᛚ': (20, 'L'), 'ᛝ': (21, 'NG'), 'ᛟ': (22, 'OE'), 'ᛞ': (23, 'D'), 'ᚪ': (24, 'A'), 
    'ᚫ': (25, 'AE'), 'ᚣ': (26, 'Y'), 'ᛡ': (27, 'IA'), 'ᛠ': (28, 'EA'), 'ᛄ': (11, 'J')
}

RUNE_TO_INDEX = {k: v[0] for k, v in GEMATRIA.items()}
INDEX_TO_LATIN = {v[0]: v[1] for k, v in GEMATRIA.items()}
INDEX_TO_LATIN[11] = 'J'
MOD = 29

# Primes
PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
    67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
    139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 
    223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
    293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
    383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
    463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
    569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643
]

def load_runes(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return [], []
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    indices = []
    text_format = []
    for char in content:
        if char in RUNE_TO_INDEX:
            indices.append(RUNE_TO_INDEX[char])
            text_format.append(True)
        elif char in ['\n', ' ', '-', '.', '•']:
            text_format.append(char)
    return indices, text_format

def restore_format(indices, fmt):
    res = ""
    idx = 0
    for item in fmt:
        if item is True:
            if idx < len(indices):
                res += INDEX_TO_LATIN.get(indices[idx], '?')
                idx += 1
        else:
            res += item
    return res

def decrypt(cipher, key, mode='SUB'):
    plain = []
    if not key: return []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'SUB':
            plain.append((c - k) % MOD)
        else:
            plain.append((c + k) % MOD)
    return plain

def main():
    # Page 55 Test
    c55, f55 = load_runes(55)
    k_totient = [(p - 1) % MOD for p in PRIMES]
    p55 = decrypt(c55, k_totient, 'SUB')
    print("--- Page 55 (Sol) ---")
    print(restore_format(p55, f55)[:100])

    # Page 33 Test
    c33, f33 = load_runes(33)
    
    # Attempt 1: Totient Reversed (ADD)
    # Master cipher said "PHI_PRIME_S0_REVERSED" with ADD.
    # Logic: Slice totient list to cipher length, then reverse?
    k1 = k_totient[:len(c33)][::-1]
    p33_1 = decrypt(c33, k1, 'ADD')
    print("\n--- Page 33 (Totient Reversed ADD) ---")
    print(restore_format(p33_1, f33)[:200])
    
    # Attempt 2: Primes Reversed (ADD)
    k_primes = [p % MOD for p in PRIMES]
    k2 = k_primes[:len(c33)][::-1]
    p33_2 = decrypt(c33, k2, 'ADD')
    print("\n--- Page 33 (Primes Reversed ADD) ---")
    print(restore_format(p33_2, f33)[:200])

if __name__ == "__main__":
    main()

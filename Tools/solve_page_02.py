import os
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

ENG_TO_IDX = {
    'F': 0, 'U': 1, 'V': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'Q': 5,
    'G': 6, 'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'Z': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20,
    'NG': 21, 'ING': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IO': 27, 'EA': 28
}

def clean_runes(text):
    return [c for c in text if c in RUNE_MAP]

def runes_to_indices(runes):
    return [RUNE_MAP[r] for r in runes]

def indices_to_eng(indices):
    return "".join([LETTERS[i] for i in indices])

def text_to_key(text):
    key = []
    i = 0
    text = text.upper().replace(" ", "")
    while i < len(text):
        if i < len(text) - 1:
            two_char = text[i:i+2]
            if two_char in ENG_TO_IDX:
                key.append(ENG_TO_IDX[two_char])
                i += 2
                continue
        char = text[i]
        if char in ENG_TO_IDX:
            key.append(ENG_TO_IDX[char])
        i += 1
    return key

def decrypt_vigenere(cipher_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        p = (c - k) % 29
        decrypted.append(p)
    return decrypted

def run():
    runes_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_02\runes.txt"
    with open(runes_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    clean_content = clean_runes(content)
    cipher_indices = runes_to_indices(clean_content)
    
    print(f"Loaded Page 02: {len(cipher_indices)} runes.")
    
    keys_str = ["INTUS", "DIVINITY", "FIRFUMFERENFE", "INSTAR", "KNOWTHIS", "CIRCUMFERENCE", "CICADA", "3301", "WELCOME", "PILGRIM"]
    
    print("\n--- Standard Vigenere (C - K) ---")
    for k_str in keys_str:
        key = text_to_key(k_str)
        if not key: continue
        res_idx = decrypt_vigenere(cipher_indices, key)
        text = indices_to_eng(res_idx)
        print(f"Key {k_str:<15}: {text[:60]}...")

    atbash_idx = [28 - i for i in cipher_indices]
    print("\n--- Atbash + Vigenere (C' - K) ---")
    for k_str in keys_str:
        key = text_to_key(k_str)
        if not key: continue
        res_idx = decrypt_vigenere(atbash_idx, key)
        text = indices_to_eng(res_idx)
        print(f"Key {k_str:<15}: {text[:60]}...")

if __name__ == "__main__":
    run()

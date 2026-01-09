import os

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

def text_to_key(text):
    key = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Check for 2-letter runes first
        if i < len(text) - 1:
            two_char = text[i:i+2]
            if two_char in ENG_TO_IDX:
                key.append(ENG_TO_IDX[two_char])
                i += 2
                continue
        
        char = text[i]
        if char in ENG_TO_IDX:
            key.append(ENG_TO_IDX[char])
        else:
            # Default fallback for unknown chars (like space, though keys usually don't have spaces)
            pass 
        i += 1
    return key

def clean_runes(text):
    return [c for c in text if c in RUNE_MAP]

def runes_to_indices(runes):
    return [RUNE_MAP[r] for r in runes]

def indices_to_eng(indices):
    return "".join([LETTERS[i] for i in indices])

def decrypt_vigenere(cipher_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        # Standard Vigenere: P = (C - K) mod 29
        p = (c - k) % 29
        decrypted.append(p)
    return decrypted

def decrypt_vigenere_add(cipher_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        # Reverse Vigenere: P = (C + K) mod 29 ??
        # Or maybe the Encryption was P - K? 
        # Usually Encrypt = (P + K), Decrypt = (C - K).
        # But let's check both (C + K) just in case.
        p = (c + k) % 29
        decrypted.append(p)
    return decrypted

def atbash_cipher(indices):
    # Map 0->28, 1->27, ...
    return [28 - i for i in indices]

def run():
    runes_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_17\runes.txt"
    with open(runes_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    clean_content = clean_runes(content)
    cipher_indices = runes_to_indices(clean_content)
    
    keys_str = ["DIVINITY", "FIRFUMFERENFE", "INTUS", "INSTAR", "KNOWTHIS", "CIRCUMFERENCE", "CICADA", "3301", "WELCOME", "PILGRIM"]
    
    # Custom Keys from Analysis
    custom_keys_indices = [
        [21, 27, 17, 22, 26, 9, 11, 3], # NG IO B OE Y N J O
        [26, 24, 8, 12, 3, 13, 26, 11], # Y A H EO O P Y J
        [22, 10, 14, 7, 1], # OE I X W U
    ]

    
    print(f"Loaded Page 17: {len(cipher_indices)} runes.")

    # Frequency Analysis
    from collections import Counter
    counts = Counter(cipher_indices)
    total = len(cipher_indices)
    print("\n--- Frequency Analysis ---")
    sorted_counts = counts.most_common()
    for idx, count in sorted_counts:
        rune = list(RUNE_MAP.keys())[list(RUNE_MAP.values()).index(idx)]
        eng = LETTERS[idx]
        perc = (count / total) * 100
        print(f"{rune} ({eng:<2}): {count:<3} ({perc:.2f}%)")

    # Index of Coincidence
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = total * (total - 1)
    ioc = numerator / denominator if denominator > 0 else 0
    print(f"\nIndex of Coincidence (IOC): {ioc:.4f}")
    print("English IOC: ~0.0667, Random IOC: ~0.0345 (for 29 chars)\n")
    
    # 1. Try Keys (Decrypt = C - K)
    print("\n--- Standard Vigenere (C - K) ---")
    for k_str in keys_str:
        key = text_to_key(k_str)
        if not key: continue
        res_idx = decrypt_vigenere(cipher_indices, key)
        text = indices_to_eng(res_idx)
        print(f"Key {k_str:<15}: {text[:60]}...")

    # Original 9-char key from string "YAHEOOPYJ"
    # Y(26) A(24) H(8) E(18) O(3) O(3) P(13) Y(26) J(11)
    
    # Corrected 8-char key assuming EO is one rune
    # Y(26) A(24) H(8) EO(12) O(3) P(13) Y(26) J(11)
    key_8_runes = [26, 24, 8, 12, 3, 13, 26, 11]

    custom_keys_indices.append(key_8_runes)
    print("\n--- Custom Keys Analysis ---")
    ck_names = ["NGIOBOEYNJO", "YAHEOOPYJ (9)", "OEIXWU", "YAHEOOPYJ (8)"]
    for i, key in enumerate(custom_keys_indices):
        res_idx = decrypt_vigenere(cipher_indices, key)
        text = indices_to_eng(res_idx)
        
        # Calculate IOC for this result
        counts = Counter(res_idx)
        numerator = sum(n * (n - 1) for n in counts.values())
        denominator = total * (total - 1)
        res_ioc = numerator / denominator if denominator > 0 else 0
        
        print(f"Key {ck_names[i]:<15}: {text[:100]}...")
        print(f"IOC: {res_ioc:.4f}")


    # 2. Try Keys (Decrypt = C + K) - sometimes key is subtracted during encryption
    print("\n--- Reverse Vigenere (C + K) ---")
    for k_str in keys_str:
        key = text_to_key(k_str)
        if not key: continue
        res_idx = decrypt_vigenere_add(cipher_indices, key)
        text = indices_to_eng(res_idx)
        print(f"Key {k_str:<15}: {text[:60]}...")

    # 3. Atbash (Reversed Alphabet)
    print("\n--- Atbash (Reversed Gematria) ---")
    atbash_idx = atbash_cipher(cipher_indices)
    text = indices_to_eng(atbash_idx)
    print(f"Atbash         : {text[:60]}...")
    
    # 4. Atbash then Vigenere
    print("\n--- Atbash + Vigenere (C - K) ---")
    for k_str in keys_str:
        key = text_to_key(k_str)
        if not key: continue
        res_idx = decrypt_vigenere(atbash_idx, key)
        text = indices_to_eng(res_idx)
        print(f"Key {k_str:<15}: {text[:60]}...")

    # 5. Shift Cipher (Caesar)
    print("\n--- Shift Cipher (0-28) ---")
    for s in range(1, 29):
        # Shift
        shifted = [(c + s) % 29 for c in cipher_indices]
        text = indices_to_eng(shifted)
        # Check for common words "THE", "AND", "ING"
        if "THE" in text or "AND" in text:
             print(f"Shift +{s:<2}      : {text[:60]}...")

if __name__ == "__main__":
    run()

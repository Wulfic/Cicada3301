#!/usr/bin/env python3
"""
Verify which key is correct by testing decryption.
"""

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LETTER = ['F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
                 'A', 'AE', 'Y', 'IA', 'EA']

# Two different keys found in the code
KEY_VERSION_1 = [1, 16, 5, 10, 11, 22, 27, 7, 21, 13, 4, 28, 2, 18, 1, 15, 
    22, 10, 24, 3, 26, 25, 9, 11, 6, 16, 24, 22, 19, 12, 6, 27, 
    0, 12, 1, 12, 27, 4, 28, 3, 25, 23, 8, 15, 1, 25, 14, 11, 
    3, 14, 16, 22, 0, 9, 1, 17, 5, 11, 17, 2, 18, 26, 20, 18, 
    3, 11, 0, 18, 11, 25, 2, 17, 9, 6, 10, 28, 24, 0, 12, 6, 
    9, 4, 21, 7, 24, 11, 1, 26, 14, 3, 22, 5, 6, 28, 14, 5, 
    8, 23, 14, 26, 27, 17, 10, 2, 23, 5, 27, 0, 8, 27, 16, 18, 4]

KEY_VERSION_2 = [19, 6, 23, 16, 10, 22, 9, 27, 26, 11, 16, 3, 19, 0, 12, 7, 23, 17, 7, 1, 1, 5, 28, 7, 20, 21, 15, 1, 17, 20, 23, 8, 22, 9, 20, 16, 7, 8, 13, 22, 15, 10, 2, 11, 22, 22, 4, 9, 19, 24, 1, 8, 12, 18, 21, 11, 21, 22, 21, 12, 7, 6, 13, 1, 14, 12, 26, 11, 11, 5, 27, 21, 25, 8, 22, 15, 20, 4, 20, 4, 19, 26, 0, 19, 1, 6, 2, 3, 22, 26, 24, 1, 19, 22, 12, 0, 21, 18, 20, 5, 17, 4, 24, 10, 19, 14, 19, 7, 12, 12, 14, 16, 2]

# Expected output
EXPECTED_START = "AETHATAEYETHESTHESTHEAEATHEOR"

def load_cipher():
    """Load cipher from file."""
    with open(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt", 'r', encoding='utf-8') as f:
        content = f.read()
    
    indices = []
    for char in content:
        if char in RUNE_TO_IDX:
            indices.append(RUNE_TO_IDX[char])
    return indices

def decrypt(cipher, key):
    """Decrypt using SUB mod 29."""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        p = (c - k) % 29
        result.append(p)
    return result

def indices_to_text(indices):
    """Convert to text."""
    return ''.join(IDX_TO_LETTER[i] for i in indices)

def main():
    cipher = load_cipher()
    print(f"Cipher length: {len(cipher)}")
    print(f"First 30 cipher values: {cipher[:30]}")
    
    print("\n" + "=" * 70)
    print("TESTING KEY VERSION 1")
    print("=" * 70)
    
    decrypted1 = decrypt(cipher, KEY_VERSION_1)
    text1 = indices_to_text(decrypted1)
    print(f"First 80 chars: {text1[:80]}")
    print(f"Matches expected start: {'YES' if text1.startswith(EXPECTED_START) else 'NO'}")
    
    print("\n" + "=" * 70)
    print("TESTING KEY VERSION 2")
    print("=" * 70)
    
    decrypted2 = decrypt(cipher, KEY_VERSION_2)
    text2 = indices_to_text(decrypted2)
    print(f"First 80 chars: {text2[:80]}")
    print(f"Matches expected start: {'YES' if text2.startswith(EXPECTED_START) else 'NO'}")
    
    # Try to figure out what key would produce the expected output
    print("\n" + "=" * 70)
    print("DERIVING KEY FROM EXPECTED OUTPUT")
    print("=" * 70)
    
    # If plaintext = cipher - key (mod 29)
    # Then key = cipher - plaintext (mod 29)
    
    LETTER_TO_IDX = {
        'F': 0, 'V': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
        'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23,
        'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }
    
    # Parse expected output to indices
    expected_text = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLE"
    expected_indices = []
    i = 0
    while i < len(expected_text):
        if i + 2 <= len(expected_text) and expected_text[i:i+2] in LETTER_TO_IDX:
            expected_indices.append(LETTER_TO_IDX[expected_text[i:i+2]])
            i += 2
        elif expected_text[i] in LETTER_TO_IDX:
            expected_indices.append(LETTER_TO_IDX[expected_text[i]])
            i += 1
        else:
            i += 1
    
    print(f"Expected output as indices (first 30): {expected_indices[:30]}")
    
    # Derive key
    derived_key = []
    for i in range(min(len(cipher), len(expected_indices))):
        k = (cipher[i] - expected_indices[i]) % 29
        derived_key.append(k)
    
    print(f"Derived key (first 30): {derived_key[:30]}")
    print(f"Derived key as letters: {[IDX_TO_LETTER[k] for k in derived_key[:30]]}")
    
    # Verify derived key
    decrypted_check = decrypt(cipher, derived_key)
    text_check = indices_to_text(decrypted_check)
    print(f"\nVerification - decrypted with derived key:")
    print(f"First 80 chars: {text_check[:80]}")

if __name__ == "__main__":
    main()

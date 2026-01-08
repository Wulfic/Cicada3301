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

def runes_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    return indices

def indices_to_eng(indices):
    return "".join([LETTERS[i] for i in indices])

title_runes = "ᛠᚪᛄᛇᛠᛚ-ᚱᚷᛋ-ᚹᚩᛒᛁ-ᛠᚳ-ᛁᛞᛄ-ᛖᛗᚱ-ᚷ"
clean_title = title_runes.replace("-", "")

print(f"Title Runes: {title_runes}")
indices = runes_to_indices(clean_title)
print(f"Indices: {indices}")
print(f"Direct Translation: {indices_to_eng(indices)}")

# P17 Key: YAHEOOPYJ
# Runes: ᛡᚪ... 
# Let's map YAHEOOPYJ to indices.
# Y=26, A=24, H=8, E=18, O=3, O=3, P=13, Y=26, J=11
p17_key_indices = [26, 24, 8, 18, 3, 3, 13, 26, 11]
print(f"P17 Key Indices: {p17_key_indices}")

# Try Vigenere (C-K)
def decrypt_vigenere(ciphertext_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(ciphertext_indices):
        k = key_indices[i % key_len]
        p = (c - k) % 29
        decrypted.append(p)
    return decrypted

# Try Reverse Vigenere (K-C)
def decrypt_reverse_vigenere(ciphertext_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(ciphertext_indices):
        k = key_indices[i % key_len]
        p = (k - c) % 29
        decrypted.append(p)
    return decrypted

# Try Variant (C+K)
def decrypt_variant_vigenere(ciphertext_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(ciphertext_indices):
        k = key_indices[i % key_len]
        p = (c + k) % 29
        decrypted.append(p)
    return decrypted

print("\n--- Try Standard Vigenere (C-K) ---")
dec = decrypt_vigenere(indices, p17_key_indices)
print(indices_to_eng(dec))

print("\n--- Try Variant Vigenere (C+K) ---")
dec = decrypt_variant_vigenere(indices, p17_key_indices)
print(indices_to_eng(dec))

# Previous experiment showed Shift 7 C+K had "THE"
# Let's reproduce that.
shift = 7
shifted_key = [(k + shift) % 29 for k in p17_key_indices]

print(f"\n--- Try Shift {shift} Key + Variant Vigenere (C+K) ---")
dec = decrypt_variant_vigenere(indices, shifted_key)
print(indices_to_eng(dec))


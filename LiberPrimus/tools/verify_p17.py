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

def decrypt_vigenere(ciphertext_indices, key_indices):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(ciphertext_indices):
        k = key_indices[i % key_len]
        p = (c - k) % 29
        decrypted.append(p)
    return decrypted

# Key: YAHEOOPYJ
# Mapping letters to indices
# Y=26, A=24, H=8, E=18, O=3, O=3, P=13, Y=26, J=11
KEY_INDICES = [26, 24, 8, 18, 3, 3, 13, 26, 11]

# Locate Page 17 runes
base_path = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_17\runes.txt'
if not os.path.exists(base_path):
    print("Cannot find Page 17 runes.")
    exit()

with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

indices = runes_to_indices(content)
decrypted = decrypt_vigenere(indices, KEY_INDICES)
print(indices_to_eng(decrypted))

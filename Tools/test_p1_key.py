
import os

# Gematria Primus Mapping
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
# Inverse map
NUM_TO_TEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# From BATCH_RESULTS.md (Attachment)
KEY_37 = [8, 0, 10, 25, 25, 27, 23, 3, 14, 23, 22, 27, 8, 20, 23, 8, 13, 23, 9, 8, 24, 8, 24, 10, 23, 9, 16, 8, 6, 6, 16, 2, 16, 20, 8, 6, 2]

def decrypt(runes_text, key):
    decrypted_text = []
    key_idx = 0
    key_len = len(key)
    
    # Isolate runes and their original indices
    rune_indices = []
    for i, char in enumerate(runes_text):
        if char in RUNE_MAP:
            rune_indices.append((RUNE_MAP[char], i))
            
    # Decrypt
    decrypted_map = {}
    for k_i, (cipher_val, original_idx) in enumerate(rune_indices):
        key_val = key[k_i % key_len]
        plain_val = (cipher_val - key_val) % 29
        decrypted_map[original_idx] = plain_val
        
    # Reconstruct
    res = ""
    for i, char in enumerate(runes_text):
        if i in decrypted_map:
            res += NUM_TO_TEXT[decrypted_map[i]]
        else:
            res += char # Preserve punctuation
    return res

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_01\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
        
    res = decrypt(runes, KEY_37)
    print(res)

if __name__ == "__main__":
    main()

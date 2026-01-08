import os
import sys

# Rune Mapping
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

def load_runes(page_num):
    paths = [
        f"LiberPrimus/pages/page_{page_num:02d}/runes.txt",
        os.path.join(os.getcwd(), f"LiberPrimus/pages/page_{page_num:02d}/runes.txt")
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [RUNE_TO_IDX[r] for r in content if r in RUNE_TO_IDX]
    return []

def parse_key(key_str):
    key_indices = []
    i = 0
    while i < len(key_str):
        # 2-char check
        if i + 1 < len(key_str):
            sub = key_str[i:i+2]
            if sub in IDX_TO_LETTER:
                key_indices.append(IDX_TO_LETTER.index(sub))
                i += 2
                continue
        
        char = key_str[i]
        if char == 'V': char = 'U' # Common mapping
        elif char == 'K': char = 'C' # Common mapping
        elif char == 'Q': char = 'C'
        elif char == 'Z': char = 'S'
        
        if char in IDX_TO_LETTER:
            key_indices.append(IDX_TO_LETTER.index(char))
        else:
            # Fallback for strict mapping verification
            print(f"Warning: Char {char} not found in map")
        i += 1
    return key_indices

def decrypt(cipher, key_str):
    if not cipher: return "NO DATA"
    key = parse_key(key_str)
    if not key: return "KEY ERROR"

    decrypted = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        decrypted.append((c - k) % 29)
    
    return "".join([IDX_TO_LETTER[x] for x in decrypted])

SOLUTIONS_TO_CHECK = {
    61: "DIVINITY",
    62: "CONSUMPTION",
    64: "KAON", 
    67: "CICADA",
    72: "FIRFUMFERENFE"
}

print("--- VERIFICATION ---")
for page, key in SOLUTIONS_TO_CHECK.items():
    cipher = load_runes(page)
    res = decrypt(cipher, key)
    print(f"Page {page} + {key}: {res[:50]}")

print("\n--- P59 ANALYSIS ---")
cipher59 = load_runes(59)
print(f"P59 Length: {len(cipher59)}")
keys_59 = ["WARNING", "WARMING", "RNGRAMW", "WMARGN R"]
for k in keys_59:
    res = decrypt(cipher59, k)
    print(f"Key {k}: {res[:50]}")

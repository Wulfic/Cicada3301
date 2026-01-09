import os

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split Title and Body
    lines = content.split('\n')
    title_line = lines[0]
    body_lines = lines[1:]
    body_text = "\n".join(body_lines)
    
    return title_line, body_text

def get_indices(text):
    res = []
    for c in text:
        if c in RUNE_MAP:
            res.append(RUNE_MAP[c])
    return res

def decrypt(indices, key, offset):
    res = []
    key_len = len(key)
    for i, c in enumerate(indices):
        k = key[(i + offset) % key_len]
        p = (c + k) % 29
        res.append(LETTERS[p])
    return "".join(res)

# P17 Key: Y A H EO O P Y J
# [26, 24, 8, 12, 3, 13, 26, 11]
KEY = [26, 24, 8, 12, 3, 13, 26, 11]

# Load P18
path = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt'
title, body = load_runes(path)

print("--- Title Check (Offset 7 expected) ---")
title_idx = get_indices(title)
# Note: Key offset in 'decrypt' function is static rotation of key?
# No, usually stream cipher: k = key[(i) % len].
# My previous analysis: Key was ROTATED by 7.
# Meaning key sequence starts at index 7: 11, 26, 24...
# This is `offset` in my function here?
# `k = key[(i + offset) % key_len]`. 
# If offset=7, i=0 -> key[7]. Correct.

print(decrypt(title_idx, KEY, 7))

print("\n--- Body Check (All Offsets) ---")
body_idx = get_indices(body)
for off in range(8):
    dec = decrypt(body_idx, KEY, off)
    snippet = dec[:50]
    print(f"Offset {off}: {snippet}")

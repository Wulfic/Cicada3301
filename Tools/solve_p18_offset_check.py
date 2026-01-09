import os

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def text_to_rune_indices(text):
    indices = []
    for char in text:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    return indices

def decrypted_with_punctuation(text, key_indices, start_offset=0):
    res = ""
    key_len = len(key_indices)
    k_idx = start_offset
    
    for char in text:
        if char in RUNE_MAP:
            c = RUNE_MAP[char]
            k = key_indices[k_idx % key_len]
            # Try C+K (Variant) as used in Title
            # P = (C + K) % 29
            p = (c + k) % 29
            res += LETTERS[p]
            k_idx += 1
        else:
            res += char
    return res

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

# P17 Key: YAHEOOPYJ (Length 9)
KEY_P17 = [26, 24, 8, 18, 3, 3, 13, 26, 11]

# P18 Runes
PAGE_PATH = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt'
with open(PAGE_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
title_line = lines[0]
body_text = "\n".join(lines[1:])

print("--- RE-VERIFYING TITLE with Shift 7 ---")
print(decrypted_with_punctuation(title_line, KEY_P17, start_offset=7))
# Expected: INGGLJD-BOY-RIOAEOE-THE-WCH-PIOT-N

# Calculate Offset for Body
# Title had 22 runes.
# Offset was 7.
# Body starts at (7 + 22) % 9 = 29 % 9 = 2.
body_offset = (7 + 22) % 9
print(f"\n--- BODY DECRYPTION (Offset {body_offset}) ---")
print(decrypted_with_punctuation(body_text, KEY_P17, start_offset=body_offset))

print("\n--- TRYING ALL OFFSETS FOR BODY ---")
for i in range(9):
    print(f"Offset {i}: " + decrypted_with_punctuation(body_text, KEY_P17, start_offset=i)[:50])

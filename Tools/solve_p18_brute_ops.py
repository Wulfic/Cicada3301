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

ENG_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

def text_to_rune_indices(text):
    indices = []
    for char in text:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    return indices

def eng_to_indices(text):
    indices = []
    i = 0
    text = text.upper().replace("-", "").replace(" ", "")
    while i < len(text):
        if i < len(text) - 1:
            two_char = text[i:i+2]
            if two_char in ENG_TO_IDX:
                indices.append(ENG_TO_IDX[two_char])
                i += 2
                continue
        if text[i] in ENG_TO_IDX:
            indices.append(ENG_TO_IDX[text[i]])
            i += 1
        else:
            i += 1
    return indices

def decrypt(cipher, key, mode):
    res = ""
    key_len = len(key)
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        if mode == 'C-K':
            p = (c - k) % 29
        elif mode == 'C+K':
            p = (c + k) % 29
        elif mode == 'K-C':
            p = (k - c) % 29
        res += LETTERS[p]
    return res

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
PAGE_PATH = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt'
with open(PAGE_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
BODY_RUNES_TEXT = "".join(lines[1:])
BODY_INDICES = text_to_rune_indices(BODY_RUNES_TEXT)

TITLE_RUNES_TEXT = lines[0]
TITLE_INDICES = text_to_rune_indices(TITLE_RUNES_TEXT)

# Keys
KEYS = {}

# P17 Key: YAHEOOPYJ
P17_VALS = [26, 24, 8, 18, 3, 3, 13, 26, 11]
KEYS['P17_Original'] = P17_VALS
KEYS['P17_Rot8 (TitleKey)'] = [P17_VALS[(i+8)%9] for i in range(9)]
KEYS['P17_Reversed'] = list(reversed(P17_VALS))

# Title PT: "INGGLJD-BOY-RIOAEOE-THE-WCH-PIOT-N"
TITLE_PT_STR = "INGGLJDBOYRIOAEOETHEWCHPIOTN"
KEYS['Title_PT'] = eng_to_indices(TITLE_PT_STR)

# Title CT
KEYS['Title_CT'] = TITLE_INDICES

# Run Tests
MODES = ['C-K', 'C+K', 'K-C']

print(f"Testing {len(KEYS)} keys x {len(MODES)} modes on Page 18 Body snippet...")

for kname, kvals in KEYS.items():
    for mode in MODES:
        dec = decrypt(BODY_INDICES, kvals, mode)
        print(f"[{kname} | {mode}]: {dec[:50]}")

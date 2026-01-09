import os

# ------------------------------------------------------------------
# Constants & Maps
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
    # Parses English text like "INGGLJD" back to indices
    # Need to handle multi-char runes like TH, EO, NG, OE, AE, IO, EA.
    # Simple greedy parser
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

def decrypt_vigenere(cipher_indices, key_indices, mode='subtract'):
    res = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        if mode == 'subtract':
            p = (c - k) % 29
        elif mode == 'add': # C+K
            p = (c + k) % 29 # Wait, if Encryption was C+K, Decryption is P=C-K? No.
            # If Encrypt = (P+K), Decrypt = (C-K).
            # If Encrypt = (P-K), Decrypt = (C+K).
            pass
        res.append(p)
    return res

def decrypt_variant(cipher_indices, key_indices):
    # Solved Title using C+K logic with P17 Key.
    # Does that mean P = C+K? Or P = C-K?
    # Logic in analyze_p18_title.py: 
    #   p = (c + k) % 29 => Decrypted text.
    # So the transformation was P = (C + K).
    # This implies C = P - K ?
    # Regardless, let's just use the function that worked: (C + K) % 29
    res = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        p = (c + k) % 29
        res.append(p)
    return res

def indices_to_string(indices):
    return "".join(LETTERS[i] for i in indices)

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
# Page 18 Title Plaintext: INGGLJD-BOY-RIOAEOE-THE-WCH-PIOT-N
TITLE_PT_STR = "INGGLJDBOYRIOAEOETHEWCHPIOTN"
TITLE_PT_INDICES = eng_to_indices(TITLE_PT_STR)

# Page 18 Title Key: J Y A H EO O P Y (From P17 Key Shift 7)
TITLE_KEY_STR = "JYAHEOOOPY" # J=11, Y=26, A=24...
# Actually let's use the indices we derived:
# P17 Key: YAHEOOPYJ -> Shift 7 -> Starts at J.
TITLE_KEY_INDICES = [11, 26, 24, 8, 12, 3, 13, 26] # Length 8

# Page 18 Body Runes
PAGE_PATH = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt'
with open(PAGE_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
body_text = "".join(lines[1:]) # Skip title line
BODY_INDICES = text_to_rune_indices(body_text)

print(f"Title Plaintext Indices (Key Candidate): {TITLE_PT_INDICES}")
print(f"Body Length: {len(BODY_INDICES)}")

# ------------------------------------------------------------------
# Attempts
# ------------------------------------------------------------------

print("\n--- Try 1: Key = Title Plaintext (Normal Vigenere: P=C-K) ---")
dec = decrypt_vigenere(BODY_INDICES, TITLE_PT_INDICES)
print(indices_to_string(dec)[:60])

print("\n--- Try 2: Key = Title Plaintext (Variant: P=C+K) ---")
dec = decrypt_variant(BODY_INDICES, TITLE_PT_INDICES)
print(indices_to_string(dec)[:60])

# Try Autokey: Key = Title Plaintext + Decrypted Body?
# Or Key = Title Plaintext + Body Cipher?

# Try Key = Title CT (Ciphertext)
# Title CT: ᛠᚪᛄᛇᛠᛚ...
TITLE_CT_INDICES = text_to_rune_indices(lines[0])

print("\n--- Try 3: Key = Title Ciphertext (Normal Vigenere: P=C-K) ---")
dec = decrypt_vigenere(BODY_INDICES, TITLE_CT_INDICES)
print(indices_to_string(dec)[:60])

print("\n--- Try 4: Key = Title Ciphertext (Variant: P=C+K) ---")
dec = decrypt_variant(BODY_INDICES, TITLE_CT_INDICES)
print(indices_to_string(dec)[:60])


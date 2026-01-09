import os
import sys

# Configurations
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
# Reverse map
IDX_TO_RUNE = {v: k for k, v in RUNE_TO_IDX.items()}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

def english_to_runes_index(text):
    # Mapping English chars to Gematria indices (Approximation)
    # This is not perfect as 'TH' is one rune, 'NG' is one rune.
    # We must handle digraphs.
    
    mapping = {
        'F':0, 'U':1, 'TH':2, 'O':3, 'R':4, 'C':5, 'K':5, 'G':6, 'W':7, 
        'H':8, 'N':9, 'I':10, 'J':11, 'EO':12, 'P':13, 'X':14, 'S':15, 'Z':15,
        'T':16, 'B':17, 'E':18, 'M':19, 'L':20, 'NG':21, 'OE':22, 'D':23, 
        'A':24, 'AE':25, 'Y':26, 'IO':27, 'IA':27, 'EA':28
    }
    
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Check digraphs
        if i+1 < len(text) and text[i:i+2] in mapping:
            indices.append(mapping[text[i:i+2]])
            i += 2
        elif text[i] in mapping:
            indices.append(mapping[text[i]])
            i += 1
        else:
            # Skip unknown or spaces
            i += 1
    return indices

def recover_key(cipher_runes_str, english_plain_str):
    cipher_indices = []
    for r in cipher_runes_str:
        if r in RUNE_TO_IDX:
            cipher_indices.append(RUNE_TO_IDX[r])
            
    plain_indices = english_to_runes_index(english_plain_str)
    
    print(f"Analyzing: Cipher='{cipher_runes_str}' vs Plain='{english_plain_str}'")
    print(f"Cipher Idx: {cipher_indices}")
    print(f"Plain Idx:  {plain_indices}")
    
    if len(cipher_indices) != len(plain_indices):
        print(f"Mismatch lengths: {len(cipher_indices)} vs {len(plain_indices)}. Cannot simple subtract.")
        return

    key_indices = []
    key_runes = []
    key_letters = []
    
    for c, p in zip(cipher_indices, plain_indices):
        # Cipher = Plain + Key  => Key = Cipher - Plain
        k = (c - p) % 29
        key_indices.append(k)
        key_runes.append(IDX_TO_RUNE[k])
        key_letters.append(IDX_TO_LETTER[k])
        
    print(f"Recovered Key: {''.join(key_letters)} ({''.join(key_runes)})")

# P59 Title
# Cipher: ᚱ•ᛝᚱᚪᛗᚹ (R NG R A M W). Only runes: ᚱᛝᚱᚪᛗᚹ
# Plain: AN END
print("--- P59 Title Analysis ---")
recover_key("ᚱᛝᚱᚪᛗᚹ", "ANEND")
recover_key("ᚱᛝᚱᚪᛗᚹ", "WARNING") # Length check: 7 vs 6. Won't work.
recover_key("ᚱᛝᚱᚪᛗᚹ", "WISDOM") # 6 letters.

# P62 Title
# Cipher: ᛒᛗᚱᚦᚠᛈ
# 6 Runes.
print("\n--- P62 Title Analysis ---")
recover_key("ᛒᛗᚱᚦᚠᛈ", "WISDOM")

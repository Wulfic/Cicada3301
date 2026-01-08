import os
import sys

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

def text_to_indices(text):
    mapping = {
        'F':0, 'U':1, 'V':1, 'TH':2, 'O':3, 'R':4, 'C':5, 'K':5, 'G':6, 'W':7, 
        'H':8, 'N':9, 'I':10, 'J':11, 'EO':12, 'P':13, 'X':14, 'Z':14, 'S':15,
        'T':16, 'B':17, 'E':18, 'M':19, 'L':20, 'NG':21, 'OE':22, 'D':23, 
        'A':24, 'AE':25, 'Y':26, 'IO':27, 'IA':27, 'EA':28
    }
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i+1 < len(text) and text[i:i+2] in mapping:
            indices.append(mapping[text[i:i+2]])
            i += 2
        elif text[i] in mapping:
            indices.append(mapping[text[i]])
            i += 1
        else:
            i += 1
    return indices

def load_page(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Skip lines that are empty
            # content = "".join([line.strip() for line in f if line.strip()])
            return content
    return None

def decrypt_str(runes_str, key_idx):
    res = []
    # Filter runes
    runes_idx = [RUNE_TO_IDX[r] for r in runes_str if r in RUNE_TO_IDX]
    
    if not runes_idx or not key_idx: return ""
    
    decrypted_indices = [(c - k) % 29 for c, k in zip(runes_idx, key_idx * (len(runes_idx) // len(key_idx) + 1))]
    return "".join([IDX_TO_LETTER[i] for i in decrypted_indices])

def solve_page(page_num, key_text):
    print(f"Solving Page {page_num} with {key_text}...")
    content = load_page(page_num)
    if not content:
        print("Page not found.")
        return
        
    key_idx = text_to_indices(key_text)
    decrypted = decrypt_str(content, key_idx)
    
    out_path = f"LiberPrimus/pages/page_{page_num:02d}/decoded.txt"
    with open(out_path, 'w') as f:
        f.write(f"Key: {key_text}\n")
        f.write(decrypted)
    print(f"Saved to {out_path}")
    print(f"Preview: {decrypted[:100]}...")

solve_page(61, "DIVINITY")
solve_page(62, "CONSUMPTION")
solve_page(67, "CICADA")
solve_page(64, "KAON")
solve_page(72, "FIRFUMFERENFE") # A KOAN?


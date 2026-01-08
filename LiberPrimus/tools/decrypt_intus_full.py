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
    # Try both relative and absolute paths
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
        if i + 1 < len(key_str):
            sub = key_str[i:i+2]
            if sub in IDX_TO_LETTER:
                key_indices.append(IDX_TO_LETTER.index(sub))
                i += 2
                continue
        char = key_str[i]
        if char == 'V': char = 'U'
        elif char == 'K': char = 'C'
        elif char == 'Q': char = 'C'
        elif char == 'Z': char = 'S'
        
        if char in IDX_TO_LETTER:
            key_indices.append(IDX_TO_LETTER.index(char))
        else:
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

def print_result(name, text):
    print(f"\n[{name}]")
    # Print in chunks of 50
    for i in range(0, len(text), 50):
        print(text[i:i+50])

print("--- FULL DECRYPTION ---")
# P61
print_result("Page 61 (DIVINITY)", decrypt(load_runes(61), "DIVINITY"))

# P67
print_result("Page 67 (CICADA)", decrypt(load_runes(67), "CICADA"))

# P59
# Trying the suspicious RNGRAMW key
print_result("Page 59 (RNGRAMW)", decrypt(load_runes(59), "RNGRAMW"))
print_result("Page 59 (WARNING)", decrypt(load_runes(59), "WARNING"))
print_result("Page 59 (R R NG R A M W)", decrypt(load_runes(59), "RRNGRAMW")) # Maybe the R is repeated?

# P64
print_result("Page 64 (KAON)", decrypt(load_runes(64), "KAON"))
print_result("Page 64 (KOAN)", decrypt(load_runes(64), "KOAN"))
print_result("Page 64 (KAOS)", decrypt(load_runes(64), "KAOS"))


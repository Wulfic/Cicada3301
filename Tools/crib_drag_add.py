
import sys
import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def to_indices(text):
    res = []
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i:i+2] in LATIN_TABLE:
            res.append(LATIN_TABLE.index(text[i:i+2]))
            i += 2
        elif text[i] in LATIN_TABLE:
            res.append(LATIN_TABLE.index(text[i]))
            i += 1
        else:
            i += 1
    return res

def main():
    if len(sys.argv) < 3:
        print("Usage: python crib_drag_add.py <cipher_file> <crib>")
        return
        
    path = sys.argv[1]
    crib_text = sys.argv[2].upper()
    
    cipher = load_runes(path)
    crib = to_indices(crib_text)
    
    print(f"Crib: {crib_text} {crib}")
    
    for i in range(len(cipher) - len(crib) + 1):
        # Assume Plaintext = Crib at pos i
        # Mode ADD: P = (C + K) % 29  => K = (P - C) % 29
        
        key_guess = []
        for j in range(len(crib)):
            c = cipher[i+j]
            p = crib[j]
            k = (p - c) % 29
            key_guess.append(LATIN_TABLE[k])
            
        print(f"Pos {i}: {' '.join(key_guess)}")

if __name__ == "__main__":
    main()

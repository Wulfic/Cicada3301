
import sys

# Constants match previous
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

COMMON_WORDS = { 'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH' }

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

P19_TEXT = "REARRANGINGTHEPRIMESNUMBERSWILLSHOWAPATHTOTHEDEORWISHINGNOTCOERCED"
# Note: This is short. If it repeats, we use it as periodic key.

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    key_text = P19_TEXT.replace(" ", "")
    key_indices = [LATIN_TABLE.index(c) for c in key_text if c in LATIN_TABLE]
    
    # Try SUB
    plain = []
    for i, c in enumerate(cipher):
        k = key_indices[i % len(key_indices)]
        plain.append((c - k) % 29)
    
    txt = text_from_indices(plain)
    print(f"P19 Key (SUB): {txt[:200]}")
    
    # Try ADD
    plain = []
    for i, c in enumerate(cipher):
        k = key_indices[i % len(key_indices)]
        plain.append((c + k) % 29)
    
    txt = text_from_indices(plain)
    print(f"P19 Key (ADD): {txt[:200]}")

if __name__ == "__main__":
    main()

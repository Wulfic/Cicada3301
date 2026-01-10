
import os

# Rune Map
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]
COMMON_WORDS = {'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH'}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def to_latin(runes):
    return "".join([LATIN_TABLE[r] for r in runes])

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    # Candidate Keys from Deor Poem
    # 23=D, 12=EO, 4=R
    KEYS = {
        'DEOR': [23, 12, 4],
        'WELUND': [7, 18, 20, 1, 9, 23], 
        'THEODRIC': [2, 12, 23, 4, 10, 5], 
        'NITHHAD': [9, 10, 2, 8, 24, 23], 
        'BEADOHILD': [17, 28, 23, 3, 8, 10, 20, 23], 
        'MATHHILD': [19, 24, 2, 8, 10, 20, 23], 
        'EORMANRIC': [12, 4, 19, 24, 9, 4, 10, 5], 
        'HEODENINGA': [8, 12, 23, 18, 9, 10, 21, 24], 
        'HEORRENDA': [8, 12, 4, 4, 18, 9, 23, 24], 
        'HEORRENDAK': [8, 12, 4, 4, 18, 9, 23, 24, 5], # K=5 (C/K/Q)
        'DEORK': [23, 12, 4, 5],
        'PATH': [13, 24, 2, 8],
    }
    
    print(f"Testing {len(KEYS)} Deor Keys on Page 20 (Vigenere)...")
    
    for name, key in KEYS.items():
        # Standard Vigenere
        plain = []
        for i, c in enumerate(cipher):
            k = key[i % len(key)]
            plain.append((c - k) % 29)
        
        txt = to_latin(plain)
        s = score_text(txt)
        if s > 0:
            print(f"Key {name}: Score {s}")
            print(f"Preview: {txt[:60]}")
            
        # Reverse Vigenere (key backwards)
        plain_rev = []
        key_r = key[::-1]
        for i, c in enumerate(cipher):
            k = key_r[i % len(key_r)]
            plain_rev.append((c - k) % 29)
        txt_r = to_latin(plain_rev)
        s_r = score_text(txt_r)
        if s_r > 0:
            print(f"Key {name} (REV): Score {s_r}")

if __name__ == "__main__":
    main()

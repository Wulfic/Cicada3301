
import os
from collections import Counter

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

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace('-', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def to_letters(values):
    return "".join([LATIN_TABLE[v] for v in values])

def to_runes(text):
    text = text.upper()
    res = []
    i = 0
    while i < len(text):
        found = False
        # Try 2 chars
        if i+1 < len(text):
            pair = text[i:i+2]
            if pair in LATIN_TABLE:
                res.append(LATIN_TABLE.index(pair))
                i += 2
                found = True
        if not found and i < len(text):
            char = text[i]
            if char in LATIN_TABLE:
                res.append(LATIN_TABLE.index(char))
            i += 1
    return res

def decrypt_vigenere(cipher, key):
    return [(c - k) % 29 for c, k in zip(cipher, key * (len(cipher)//len(key) + 1))]

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    KEYS = [
        "DEOR", "DEORK", "DEORKEY", "PRIMES", "PRIME", "TOTIENT", "PHI", 
        "WELUND", "BEADOHILD", "MAETHHILD", "THEODRIC", "EORMANRIC", "HEORRENDA",
        "PATH", "WAY", "THEWAY", "WITHIN", "ABOVE", "BELOW", "DIVINITY",
        "HENGALLA", "HENGEST", "FINNSBURG", "WULF", "EADWACER",
        "KEY", "LOCK", "OPEN", "CICADA", "3301",
        "REARRANGE", "REARRANGING", "NUMBERS",
        "DEORPOEM", "POEM", "THEPOEM",
        "WYLFENNE", "GETHOHT", "THIRTY", "WINTERS",
        "SORROW", "PASSED", "AWAY", # from refrain
        "THATPASSED", "SOMAYTHIS",
        "THAESOFEREODE", "THISESSWAMAEG"
    ]
    
    print(f"Testing {len(KEYS)} keys on Page 20...")
    
    for k_str in KEYS:
        k_runes = to_runes(k_str)
        if not k_runes: continue
        
        dec = decrypt_vigenere(cipher, k_runes)
        ioc = calculate_ioc(dec)
        
        if ioc > 1.1: # Threshold for interest
            print(f"Key: {k_str} | IoC: {ioc:.4f}")
            print(f"Preview: {to_letters(dec)[:50]}")
    
    print("Done.")

if __name__ == "__main__":
    main()

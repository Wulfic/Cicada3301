
import os

# Rune Map
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

# Refrain: "Þæs ofereode, þisses swa mæg"
# "TH AE S O F E R EO D E TH I S S E S S W A M AE G"
# Values:
# TH=2, AE=25, S=15, O=3, F=0, E=18, R=4, EO=12, D=23, E=18, TH=2, I=10, S=15, S=15, E=18, S=15, S=15, W=7, A=24, M=19, AE=25, G=6

REFRAIN_KEY_1 = [2, 25, 15, 3, 0, 18, 4, 12, 23, 18, 2, 10, 15, 15, 18, 15, 15, 7, 24, 19, 25, 6]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def to_latin(runes):
    return "".join([LATIN_TABLE[r] for r in runes])

def index_of_coincidence(text):
    if not text: return 0
    counts = {}
    for x in text:
        counts[x] = counts.get(x, 0) + 1
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    if denominator == 0: return 0
    return numerator / denominator * 29.0

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    print(f"P20 Length: {len(cipher)}")
    
    # Test Refrain Key
    keys = {
        "Refrain Normal": REFRAIN_KEY_1,
        "Refrain Reversed": REFRAIN_KEY_1[::-1],
    }
    
    for name, key in keys.items():
        # Subtract
        plain = []
        for i, c in enumerate(cipher):
            k = key[i % len(key)]
            plain.append((c - k) % 29)
        ioc = index_of_coincidence(plain)
        print(f"Key: {name} (Sub) -> IoC: {ioc:.4f}")
        print(f"Preview: {to_latin(plain[:80])}")
        
        # Add (Vigenere sometimes adds?)
        plain_add = []
        for i, c in enumerate(cipher):
            k = key[i % len(key)]
            plain_add.append((c + k) % 29)
        ioc_add = index_of_coincidence(plain_add)
        print(f"Key: {name} (Add) -> IoC: {ioc_add:.4f}")

if __name__ == "__main__":
    main()

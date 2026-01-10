import os
import collections

# GP Mapping
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
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def calc_ioc(indices):
    if len(indices) < 2: return 0
    c = collections.Counter(indices)
    num = sum(n * (n - 1) for n in c.values())
    den = len(indices) * (len(indices) - 1)
    return num / den * 29.0

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    # Primes mod 29 (slopes)
    # 2, 3, 5, 7, 11, 13, 17, 19, 23
    # Also 29? No A=0 invalid.
    slopes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    print(f"Checking {len(slopes)*29} Affine combinations...")
    
    for a in slopes:
        for b in range(29):
            # P = (A*C + B) % 29
            # Also P = (A*(C+B)) % 29 ?
            # Standard Affine: P = (A(C-B)) % 29 (Decryption).
            # A_inv is needed for decrypt if we assume C = AP+B.
            # But here we just bruteforce the transformation.
            
            res = [(a * c + b) % 29 for c in cipher]
            ioc = calc_ioc(res)
            
            if ioc > 1.3:
                print(f"Slope {a}, Shift {b}: IoC {ioc:.4f}")

if __name__ == "__main__":
    main()

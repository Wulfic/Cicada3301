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

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

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
    p20_runes = load_runes(p20_path)
    
    # Split into Key (Primes) and Cipher (Non-Primes)
    key_runes = [r for r in p20_runes if is_prime(r)] # Using GP value as criterion
    cipher_runes = [r for r in p20_runes if not is_prime(r)]
    
    print(f"Key Length (Primes): {len(key_runes)}")
    print(f"Cipher Length (Non-Primes): {len(cipher_runes)}")
    
    # Variations of Key
    keys = {
        "Direct": key_runes,
        "Reserved": key_runes[::-1],
        "Sorted": sorted(key_runes),
        "SortedDesc": sorted(key_runes, reverse=True)
    }
    
    modes = ['C-K', 'K-C', 'C+K']
    
    for k_name, key in keys.items():
        print(f"\n--- Key: {k_name} ---")
        for mode in modes:
            res = []
            for i in range(len(cipher_runes)):
                c = cipher_runes[i]
                k = key[i % len(key)]
                
                if mode == 'C-K': val = (c - k) % 29
                elif mode == 'K-C': val = (k - c) % 29
                elif mode == 'C+K': val = (c + k) % 29
                res.append(val)
            
            ioc = calc_ioc(res)
            txt = "".join([LATIN_TABLE[x] for x in res[:60]])
            print(f"Mode {mode}: IoC={ioc:.4f} | {txt}...")

if __name__ == "__main__":
    main()

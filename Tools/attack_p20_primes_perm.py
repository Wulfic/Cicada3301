
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

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def generate_primes_perm(mod=29):
    perm = []
    seen = set()
    n = 2
    while len(perm) < mod:
        if is_prime(n):
            val = n % mod
            if val not in seen:
                perm.append(val)
                seen.add(val)
        n += 1
    return perm

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    COLS = 29
    ROWS = 28
    
    grid = []
    for r in range(ROWS):
        grid.append(cipher[r*COLS : (r+1)*COLS])
        
    def get_col(c_idx):
        return [grid[r][c_idx] for r in range(ROWS)]

    # Generate Permutations
    # 1. Primes Mod 29 sequence: [2, 3, 5, 7...]
    perm1 = generate_primes_perm(29)
    print(f"Primes Permutation: {perm1}")
    
    # Apply Permutation 1
    new_cols_1 = [get_col(p) for p in perm1]
    text_1 = []
    for r in range(ROWS):
        for c in range(COLS):
            text_1.append(new_cols_1[c][r])
            
    print(f"Permutation 1 IoC: {calculate_ioc(text_1):.4f}")
    print(f"Preview 1: {to_letters(text_1)[:100]}")
    
    # 2. Primes mapping strictly to 1..28? And 0 at end?
    # Primes Perm but 0 is fixed?
    # Let's try Perm 1 first.

if __name__ == "__main__":
    main()


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

    # Primes in 0-28
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    # Sort Alphabetically: Eleven, Five, Nineteen, Seven, Seventeen, Thirteen, Three, Twenty-three, Two
    # 11, 5, 19, 7, 17, 13, 3, 23, 2
    sorted_primes = [11, 5, 19, 7, 17, 13, 3, 23, 2]
    
    new_cols = [get_col(p) for p in sorted_primes]
    
    # Read Row by Row
    text_rows = []
    for r in range(ROWS):
        for c in range(len(sorted_primes)):
            text_rows.append(new_cols[c][r])
            
    print(f"Alphabetical Prime Sort (11, 5, 19, 7, 17, 13, 3, 23, 2)")
    print(f"IoC: {calculate_ioc(text_rows):.4f}")
    print(f"Preview: {to_letters(text_rows)[:100]}")
    
    # Try Column Read
    text_cols = []
    for c in range(len(sorted_primes)):
        for r in range(ROWS):
            text_cols.append(new_cols[c][r])
            
    print(f"Column Read IoC: {calculate_ioc(text_cols):.4f}")

if __name__ == "__main__":
    main()

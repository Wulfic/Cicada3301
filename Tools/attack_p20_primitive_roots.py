
import os
from collections import Counter
import math

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

def get_primitive_roots(modulo):
    roots = []
    required_set = set(num for num in range(1, modulo) if math.gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers, modulo) for powers in range(1, modulo))
        if required_set == actual_set:
            roots.append(g)
    return roots

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    COLS = 29
    ROWS = 28
    
    # Grid construction
    # Original Columns 0-28
    grid = []
    for r in range(ROWS):
        grid.append(cipher[r*COLS : (r+1)*COLS])
        
    def get_col(c_idx):
        return [grid[r][c_idx] for r in range(ROWS)]

    # Get primitive roots of 29
    roots = get_primitive_roots(29)
    print(f"Primitive Roots of 29: {roots}")
    
    best_ioc = 0
    best_perm = None
    best_root = -1
    best_mode = ""

    # Mode 1: Generator Power Ordering
    # New Col i = Old Col (g^i mod 29)
    # i goes from 1 to 28. What about Col 0?
    # Hypothesis: Col 0 is "Void" or "Key" or stays at 0.
    
    for g in roots:
        # Permutation: [0] + [g^1, g^2, ..., g^28]
        perm = [0] + [pow(g, i, 29) for i in range(1, 29)]
        
        # Reconstruct grid
        new_cols = [get_col(p) for p in perm]
        
        # Readout: Row by Row
        text_rows = []
        for r in range(ROWS):
            for c in range(COLS):
                text_rows.append(new_cols[c][r])
        
        ioc = calculate_ioc(text_rows)
        if ioc > best_ioc:
            best_ioc = ioc
            best_perm = perm
            best_root = g
            best_mode = "Powers (Row Read)"
            
        if ioc > 1.05:
            print(f"Found Potential (Powers): g={g}, IoC={ioc:.4f}")

    # Mode 2: Discrete Log Ordering
    # New Col i where i = g^x -> maps to x?
    # Rearrange such that columns are ordered by their discrete log base g?
    # i.e. New Col 1 is the col whose value is g^1? That's Mode 1.
    # New Col x is the col whose index is g^x? That's Mode 1.
    
    # Let's try "Sort by Value" logic
    # Arrange columns such that their indices are sorted? (0, 1, 2... is default)
    
    # Mode 3: Only Prime Columns Permuted
    # This is getting complex. Let's stick to the primitives.
    
    print("-" * 30)
    print(f"Best Result: {best_mode}")
    print(f"Root: {best_root}")
    print(f"IoC: {best_ioc:.4f}")
    if best_perm:
        # Reconstruct and print preview
        new_cols = [get_col(p) for p in best_perm]
        text_rows = []
        for r in range(ROWS):
            for c in range(COLS):
                text_rows.append(new_cols[c][r])
        print(f"Text Preview: {to_letters(text_rows)[:100]}")
        
        # Try Column Readout
        text_cols = []
        for c in range(COLS):
            for r in range(ROWS):
                text_cols.append(new_cols[c][r])
        print(f"Column Read Preview: {to_letters(text_cols)[:100]}")
        print(f"Column Read IoC: {calculate_ioc(text_cols):.4f}")

if __name__ == "__main__":
    main()

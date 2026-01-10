import os
import collections

# GP Mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
INV_RUNE_MAP = {v: k for k, v in RUNE_MAP.items()}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def score_text(indices):
    # Simple IoC
    if len(indices) < 2: return 0
    c = collections.Counter(indices)
    num = sum(n * (n - 1) for n in c.values())
    den = len(indices) * (len(indices) - 1)
    return num / den * 29.0

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    # 812 chars. 28 rows * 29 cols.
    ROWS = 28
    COLS = 29
    
    # Create Grid (Row Major)
    grid = []
    for r in range(ROWS):
        grid.append(cipher[r*COLS : (r+1)*COLS])
        
    print(f"Grid Size: {len(grid)}x{len(grid[0])}")
    
    # Identify Prime Columns (indices 0 to 28)
    prime_cols = [c for c in range(COLS) if is_prime(c)] # 2, 3, 5, 7, 11, 13, 17, 19, 23
    composite_cols = [c for c in range(COLS) if not is_prime(c)] # 0, 1, 4, 6...
    
    perms = []
    
    # Permutation 1: Primes First (Asc), then Others (Asc)
    p1 = prime_cols + composite_cols
    perms.append(("Primes_First_Asc", p1))
    
    # Permutation 2: Primes First (Asc), then Others (Desc)
    p2 = prime_cols + composite_cols[::-1]
    perms.append(("Primes_First_Desc", p2))
    
    # Permutation 3: Primes Only (discard others? No, text must come from all?)
    # Hint says "Rearranging the Primes Numbers".
    # Maybe rearrange text based on prime columns ONLY? 
    # Let's verify full permutations first.
    
    # Permutation 4: Primes Reversed, then Others
    p4 = prime_cols[::-1] + composite_cols
    perms.append(("Primes_Rev_Asc", p4))
    
    # Check Column IoCs for straight grid (No perm needed to check column coherence)
    print("\n--- Column IoC Analysis (Width 29) ---")
    avg_col_ioc = 0
    for c in range(COLS):
        col_vals = []
        for r in range(ROWS):
            col_vals.append(grid[r][c])
        ioc = score_text(col_vals)
        avg_col_ioc += ioc
        # print(f"Col {c}: IoC={ioc:.4f}")
    
    print(f"Average Column IoC (Width 29): {avg_col_ioc/COLS:.4f}")
    
    # Also check Width 28
    print("\n--- Column IoC Analysis (Width 28) ---")
    W28 = 28
    H28 = 29
    grid28 = []
    for r in range(H28):
        grid28.append(cipher[r*W28 : (r+1)*W28])
        
    avg_col_ioc_28 = 0
    for c in range(W28):
        col_vals = []
        for r in range(H28):
            col_vals.append(grid28[r][c])
        ioc = score_text(col_vals)
        avg_col_ioc_28 += ioc
    print(f"Average Column IoC (Width 28): {avg_col_ioc_28/W28:.4f}")

    for name, cols_order in perms:
        # Reconstruct grid
        # New Grid: Row r gets values from Permuted Columns
        new_text = []
        # Option A: Read row by row from new grid
        for r in range(ROWS):
            row_vals = []
            for c in cols_order:
                row_vals.append(grid[r][c])
            new_text.extend(row_vals)
            
        ioc = score_text(new_text)
        txt = "".join([LATIN_TABLE[x] for x in new_text[:60]])
        print(f"Grid Perm {name}: IoC={ioc:.4f}")
        print(f"Preview: {txt}...")
        
        # Option B: Read Column by Column
        col_text = []
        for c in cols_order:
            for r in range(ROWS):
                col_text.append(grid[r][c])
        ioc_c = score_text(col_text)
        txt_c = "".join([LATIN_TABLE[x] for x in col_text[:60]])
        print(f"Grid Perm {name} (ColRead): IoC={ioc_c:.4f}")

if __name__ == "__main__":
    main()


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

def get_primitive_roots(modulo):
    roots = []
    # simplified
    for g in range(1, modulo):
        powers = set()
        for i in range(1, modulo):
            powers.add(pow(g, i, modulo))
        if len(powers) == modulo - 1:
            roots.append(g)
    return roots

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    COLS = 29
    ROWS = 28
    
    # Extract Columns
    grid_cols = []
    for c in range(COLS):
        col_data = []
        for r in range(ROWS):
            idx = r * COLS + c
            if idx < len(cipher):
                col_data.append(cipher[idx])
        grid_cols.append(col_data)

    print(f"Grid: {COLS}x{ROWS}")
    
    roots = get_primitive_roots(29)
    print(f"Primitive Roots of 29: {roots}")
    
    for g in roots:
        # Generate Permutation 1..28
        perm = []
        for i in range(1, 29): # Powers 1 to 28
            perm.append(pow(g, i, 29))
            
        # Complete Permutation: Include 0 at start? Or end?
        # Try both: 0 + perm, perm + 0
        perms_to_test = [
            ([0] + perm, "0 + Powers"),
            (perm + [0], "Powers + 0")
        ]
        
        for p_order, label in perms_to_test:
            # Reorder columns
            # Construct Grid with new column order
            new_grid = []
            for col_idx in p_order:
                new_grid.append(grid_cols[col_idx])
            
            # Read Horizontally (Row by Row) across the NEW grid
            # new_grid is defined as list of columns
            # So new_grid[x][y] is Column x, Row y
            reordered_stream = []
            for r in range(ROWS):
                for c in range(len(p_order)):
                    reordered_stream.append(new_grid[c][r])
            
            ioc = index_of_coincidence(reordered_stream)
            if ioc > 1.05:
                print(f"ROOT {g} ({label}): IoC={ioc:.4f}")
                print(f"Preview: {to_latin(reordered_stream[:80])}")

if __name__ == "__main__":
    main()

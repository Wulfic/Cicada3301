
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

def to_latin(runes):
    return "".join([LATIN_TABLE[r] for r in runes])

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

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
    print(f"Total Runes: {len(cipher)}")
    
    # Grid 29 Cols x 28 Rows
    COLS = 29
    ROWS = 28
    
    # 0,1,2,3,5,7... (Primes are 2,3,5...)
    # Columns 0..28
    prime_col_indices = [c for c in range(COLS) if is_prime(c)]
    
    # Extract Columns
    grid = []
    for r in range(ROWS):
        grid.append(cipher[r*COLS : (r+1)*COLS])
        
    extracted_runes = []
    # Read row by row, but only prime columns
    # Or read Column by Column?
    
    # Mode A: Concatenate Prime Columns (Col 2 top-down, Col 3 top-down...)
    col_stream = []
    for c in prime_col_indices:
        for r in range(ROWS):
            col_stream.append(grid[r][c])
            
    print(f"Prime Columns (Vertical) Length: {len(col_stream)}")
    ioc_A = index_of_coincidence(col_stream)
    print(f"Prime Columns (Vertical) IoC: {ioc_A:.4f}")
    print(f"Preview: {to_latin(col_stream[:50])}")
    
    # Mode B: Read Rows, filtering only Prime Columns
    row_stream = []
    for r in range(ROWS):
        for c in prime_col_indices:
            row_stream.append(grid[r][c])
            
    print(f"Prime Columns (Horizontal) Length: {len(row_stream)}")
    ioc_B = index_of_coincidence(row_stream)
    print(f"Prime Columns (Horizontal) IoC: {ioc_B:.4f}")
    print(f"Preview: {to_latin(row_stream[:50])}")

    # Mode C: The Non-Prime Columns?
    non_prime_indices = [c for c in range(COLS) if not is_prime(c)]
    non_prime_stream = []
    for r in range(ROWS):
        for c in non_prime_indices:
            non_prime_stream.append(grid[r][c])
            
    ioc_C = index_of_coincidence(non_prime_stream)
    print(f"Non-Prime Columns (Horizontal) IoC: {ioc_C:.4f}")

    # Mode D: Rows based on Primes?
    # Rows 2, 3, 5, 7, 11, 13, 17, 19, 23 (Max 23 < 28)
    prime_rows = []
    for r in range(ROWS):
        if is_prime(r):
             prime_rows.extend(grid[r])
             
    ioc_D = index_of_coincidence(prime_rows)
    print(f"Prime Rows (Full) IoC: {ioc_D:.4f}")

if __name__ == "__main__":
    main()

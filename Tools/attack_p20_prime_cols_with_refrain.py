
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

# "Þæs ofereode, þisses swa mæg"
# TH AE S O F E R EO D E TH I S S E S S W A M AE G
REFRAIN_KEY_1 = [2, 25, 15, 3, 0, 18, 4, 12, 23, 18, 2, 10, 15, 15, 18, 15, 15, 7, 24, 19, 25, 6]

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

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
    
    # 29 x 28 Grid
    COLS = 29
    ROWS = 28
    
    prime_cols = [c for c in range(COLS) if is_prime(c)] # 2, 3, 5, 7...
    
    # Extract Horizontal Stream (Row by Row, reading only prime cols)
    # This preserves the reading order within the prime columns across rows.
    stream_horiz = []
    
    # Grid
    grid = []
    for r in range(ROWS):
        grid.append(cipher[r*COLS : (r+1)*COLS])
        
    for r in range(ROWS):
        for c in prime_cols:
            stream_horiz.append(grid[r][c])
            
    print(f"Extracted Stream Length: {len(stream_horiz)}")
    
    # Decrypt with Refrain
    key = REFRAIN_KEY_1
    plain = []
    for i, c in enumerate(stream_horiz):
        k = key[i % len(key)]
        plain.append((c - k) % 29)
        
    ioc = index_of_coincidence(plain)
    print("\n--- Decryption with Deor Refrain (Refrain Key) ---")
    print(f"Key Length: {len(key)}")
    print(f"IoC: {ioc:.4f}") # Expect > 1.5 if correct
    print(f"Preview: {to_latin(plain[:100])}")
    
    # Try Reversing the Refrain
    key_rev = key[::-1]
    plain_rev = []
    for i, c in enumerate(stream_horiz):
        k = key_rev[i % len(key_rev)]
        plain_rev.append((c - k) % 29)
        
    ioc_rev = index_of_coincidence(plain_rev)
    print("\n--- Decryption with Reversed Refrain ---")
    print(f"IoC: {ioc_rev:.4f}")
    
    # Try Vertical Stream (Column by Column)
    stream_vert = []
    for c in prime_cols:
        for r in range(ROWS):
            stream_vert.append(grid[r][c])
            
    plain_vert = []
    for i, c in enumerate(stream_vert):
        k = key[i % len(key)]
        plain_vert.append((c - k) % 29)
        
    ioc_vert = index_of_coincidence(plain_vert)
    print("\n--- Decryption Vertical Stream (Refrain Key) ---")
    print(f"IoC: {ioc_vert:.4f}")

if __name__ == "__main__":
    main()


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

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
PRIME_NAMES = {
    2: "two", 3: "three", 5: "five", 7: "seven", 11: "eleven", 
    13: "thirteen", 17: "seventeen", 19: "nineteen", 23: "twentythree"
}

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
        
    # Key Stream: Sorted Primes Columns
    sorted_primes = sorted(PRIMES, key=lambda p: PRIME_NAMES[p])
    key_stream = []
    for p in sorted_primes:
        key_stream.extend(grid_cols[p])
        
    print(f"Key Stream Length: {len(key_stream)}")
    
    # Cipher Stream: Non-Prime Columns (in numeric order?)
    non_prime_cols_idx = [c for c in range(COLS) if c not in PRIMES]
    cipher_stream = []
    for c in non_prime_cols_idx:
        cipher_stream.extend(grid_cols[c])
        
    print(f"Cipher Stream Length: {len(cipher_stream)}")
    
    # Decrypt
    plain = []
    for i, c in enumerate(cipher_stream):
        k = key_stream[i % len(key_stream)]
        plain.append((c - k) % 29)
        
    ioc = index_of_coincidence(plain)
    print(f"Result (Non-Primes decrypted by Sorted Primes): IoC={ioc:.4f}")
    print(f"Preview: {to_latin(plain[:80])}")
    
    # Add variant
    plain_add = []
    for i, c in enumerate(cipher_stream):
        k = key_stream[i % len(key_stream)]
        plain_add.append((c + k) % 29)
    ioc_add = index_of_coincidence(plain_add)
    print(f"Result (Add Variant): IoC={ioc_add:.4f}")

if __name__ == "__main__":
    main()

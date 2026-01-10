
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
    
    # Grid 29 Cols x 28 Rows
    COLS = 29
    ROWS = 28
    
    if len(cipher) != COLS * ROWS:
        print(f"Warning: Cipher length {len(cipher)} != {COLS}x{ROWS} ({COLS*ROWS})")
    
    # Extract Columns
    grid = []
    for r in range(ROWS):
        grid.append(cipher[r*COLS : (r+1)*COLS])
        
    def get_col(c_idx):
        return [grid[r][c_idx] for r in range(ROWS)]
    
    # Deor Columns Hypothesis
    # Order: Welund (7), Beadohild (17), Maethhild (19), Theodric (2), Deor (23)
    target_indices = [7, 17, 19, 2, 23]
    
    new_cols = [get_col(i) for i in target_indices]
    
    # Read row by row from new grid (5 cols x 28 rows)
    extracted_text = []
    for r in range(ROWS):
        for c in range(len(target_indices)):
            extracted_text.append(new_cols[c][r])
            
    print(f"Extracted {len(extracted_text)} runes based on Deor Name columns.")
    print(f"Indices: {target_indices} (W, B, M, TH, D)")
    print(f"IoC: {calculate_ioc(extracted_text):.4f}")
    # Try All Prime Columns decryption
    prime_cols_indices = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    prime_cols_data = [] # List of lists
    for idx in prime_cols_indices:
        prime_cols_data.append(get_col(idx))
    
    # Linearize Row by Row
    prime_text_row_wise = []
    for r in range(ROWS):
        for c_idx in range(len(prime_cols_indices)):
            prime_text_row_wise.append(prime_cols_data[c_idx][r])
            
    print(f"\nPrime Columns (Row-Read): {len(prime_text_row_wise)} chars")
    
    # Decrypt with Deor Full
    DEOR_TEXT_OLD_ENGLISH = """
Welund him be wurman wræces cunnade,
anhydig eorl earfoþa dreag,
hæfde him to gesiþþe sorge ond longaþ,
wintercealde wræce; wean oft onfond,
siþþan hine Niðhad on nede legde,
swoncre seonobende on syllan monn.
Þæs ofereode, þisses swa mæg.
"""
    # Simple tokenize
    def simple_tokenize(text):
        LATIN_TO_VAL = {
            'F': 0, 'U': 1, 'V': 1, 'TH': 2, 'P': 2, 'Þ': 2, 'Ð': 2, 
            'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9, 
            'I': 10, 'J': 11, 'EO': 12, 'Z': 14, 'S': 15, 'T': 16, 'B': 17, 
            'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 
            'A': 24, 'AE': 25, 'Æ': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
        }
        text = text.upper().replace(' ', '').replace('\n', '').replace('.', '').replace(',', '')
        vals = []
        i = 0
        while i < len(text):
            if i+1 < len(text) and text[i:i+2] in LATIN_TO_VAL:
                vals.append(LATIN_TO_VAL[text[i:i+2]])
                i+=2
            elif text[i] in LATIN_TO_VAL:
                vals.append(LATIN_TO_VAL[text[i]])
                i+=1
            else: i+=1
        return vals
        
    deor_key_full = simple_tokenize(DEOR_TEXT_OLD_ENGLISH)
    
    dec_prime_cols = [(c - k) % 29 for c, k in zip(prime_text_row_wise, deor_key_full * 10)]
    print(f"Prime Cols Decrypted with Deor (IoC: {calculate_ioc(dec_prime_cols):.4f}):")
    print(to_letters(dec_prime_cols)[:80])
    
    # Decrypt with Refrain
    refrain_key = [2, 25, 15, 3, 0, 18, 4, 12, 23, 18, 2, 10, 15, 15, 18, 15, 15, 7, 24, 19, 25, 6]
    dec_prime_cols_ref = [(c - k) % 29 for c, k in zip(prime_text_row_wise, refrain_key * 20)]
    print(f"Prime Cols Decrypted with Refrain (IoC: {calculate_ioc(dec_prime_cols_ref):.4f}):")
    print(to_letters(dec_prime_cols_ref)[:80])

    # Remaining primes: 3, 5, 11, 13
    # Try appending them?
    # W B M TH D + O C J P
    target_indices_2 = [7, 17, 19, 2, 23, 3, 5, 11, 13]
    new_cols_2 = [get_col(i) for i in target_indices_2]
    extracted_text_2 = []
    for r in range(ROWS):
        for c in range(len(target_indices_2)):
            extracted_text_2.append(new_cols_2[c][r])

    print(f"\nExtended Version (All Primes): {target_indices_2}")
    print(f"IoC: {calculate_ioc(extracted_text_2):.4f}")
    print(f"Text: {to_letters(extracted_text_2)}")

if __name__ == "__main__":
    main()

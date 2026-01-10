
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

def to_runes(text):
    text = text.upper()
    res = []
    i = 0
    while i < len(text):
        found = False
        if i+1 < len(text):
            pair = text[i:i+2]
            if pair in LATIN_TABLE:
                res.append(LATIN_TABLE.index(pair))
                i += 2
                found = True
        if not found and i < len(text):
            char = text[i]
            if char in LATIN_TABLE:
                res.append(LATIN_TABLE.index(char))
            i += 1
    return res

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
    
    # Load P18
    p18_path = os.path.join(repo, "LiberPrimus", "pages", "page_18", "runes.txt")
    cipher = load_runes(p18_path)
    print(f"Loaded {len(cipher)} runes from P18.")
    
    # Load Key Candidate (from P20 Primes analysis)
    # File "p20_prime_decrypted.txt" has the Shift 5 version (YEOT...).
    key_path = os.path.join(repo, "Analysis", "Outputs", "p20_prime_decrypted.txt")
    with open(key_path, "r") as f:
        key_text = f.read().strip()
    
    key_vals = to_runes(key_text)
    print(f"Loaded Key (P20 Prime Stream): {key_text[:50]}")
    
    # Decrypt P18 with this Key
    # P18 (excluding title?)
    # Title is first ~21 chars?
    # Title: ᛠᚪᛄᛇᛠᛚ-ᚱᚷᛋ-ᚹᚩᛒᛁ-ᛠᚳ-ᛁᛞᛄ-ᛖᛗᚱ-ᚷ
    # 7 + 3 + 4 + 2 + 3 + 3 + 1 = 23 chars. Or 24?
    # Start decryption from index 0 anyway.
    
    dec = [(c - k) % 29 for c, k in zip(cipher, key_vals * (len(cipher)//len(key_vals) + 1))]
    print(f"Decryption Output (IoC: {calculate_ioc(dec):.4f}):")
    print(to_letters(dec))
    
    # Try omitting title
    dec_body = [(c - k) % 29 for c, k in zip(cipher[26:], key_vals * (len(cipher)//len(key_vals) + 1))]
    print(f"\nDecryption Output (Body Only) (IoC: {calculate_ioc(dec_body):.4f}):")
    print(to_letters(dec_body))

if __name__ == "__main__":
    main()

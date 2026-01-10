
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

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    
    # 1. Load P20 Full
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    print(f"Loaded {len(cipher)} runes from P20.")
    
    # 2. Load the Key Candidate (Shift 5 from previous step)
    # The file has unshifted. We must load, convert to vals, shift +5.
    candidate_path = os.path.join(repo, "Analysis", "Outputs", "p20_prime_stream_candidate.txt")
    with open(candidate_path, "r") as f:
        candidate_text = f.read().strip()
    
    candidate_vals = to_runes(candidate_text)
    # Shift + 5 to align with "THE" theory
    key_vals = [(c + 5) % 29 for c in candidate_vals]
    key_text = to_letters(key_vals)
    print(f"Key Candidate (Shift 5): {key_text[:60]}")
    print(f"Key Length: {len(key_vals)}")
    
    # 3. Decrypt Full P20 with Key (Repeating)
    dec = [(c - k) % 29 for c, k in zip(cipher, key_vals * (len(cipher)//len(key_vals) + 1))]
    print(f"\nDecrypted Full P20 IoC: {calculate_ioc(dec):.4f}")
    print(f"Preview: {to_letters(dec)[:100]}")
    
    # 4. Decrypt NON-PRIME Indices only
    # Maybe the Primes hold the key for the Composites?
    # Indices that are NOT prime
    non_prime_indices = [i for i in range(len(cipher)) if i > 1 and not (all(i % p != 0 for p in range(2, int(i**0.5) + 1)))]
    # (Actually simpler is_prime check)
    def is_p(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n%i==0: return False
        return True
    
    non_prime_indices = [i for i in range(len(cipher)) if not is_p(i)]
    non_prime_cipher = [cipher[i] for i in non_prime_indices]
    
    # Decrypt Non-Primes using Key (Repeating? Or Mapping?)
    # Since we have 141 key chars and 600+ composite chars, we must repeat.
    dec_non_prime = [(c - k) % 29 for c, k in zip(non_prime_cipher, key_vals * (len(non_prime_cipher)//len(key_vals) + 1))]
    print(f"\nDecrypted Non-Primes IoC: {calculate_ioc(dec_non_prime):.4f}")
    print(f"Preview: {to_letters(dec_non_prime)[:100]}")

if __name__ == "__main__":
    main()

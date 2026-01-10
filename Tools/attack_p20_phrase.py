
import sys

# Constants match previous
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

# Gematria Primes map (Index -> Prime)
PRIME_VALS = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109
]

COMMON_WORDS = {'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO'}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    # 1. INDICES of "PRIMES NUMBERS"
    phrase = "PRIMESNUMBERS"
    indices = [LATIN_TABLE.index(c) if c in LATIN_TABLE else 0 for c in ["P", "R", "I", "M", "E", "S", "N", "U", "M", "B", "E", "R", "S"]]
    # LATIN_TABLE P=13, R=4 ...
    # indices = [13, 4, 10, 19, 18, 15, 9, 1, 19, 17, 18, 4, 15]
    
    # 2. VALUES (Prime) % 29
    values = [PRIME_VALS[i] % 29 for i in indices]
    
    # 3. SORTED Indices
    sorted_indices = sorted(indices)
    
    KEYS = {
        'PHRASE_INDICES': indices,
        'PHRASE_VALUES': values,
        'SORTED_INDICES': sorted_indices,
        'SORTED_VALUES': sorted(values),
        'REVERSE_SORTED_INDICES': sorted_indices[::-1],
        'REARRANGED_PRIMES_ASC': sorted(values), # same as sorted values
        'REARRANGED_PRIMES_DESC': sorted(values)[::-1] 
    }
    
    for name, key in KEYS.items():
        # Try as repeating key (Vigenere)
        key_len = len(key)
        
        # ADD
        plain = []
        for i, c in enumerate(cipher):
            k = key[i % key_len]
            plain.append((c + k) % 29)
        txt = text_from_indices(plain)
        print(f"{name} (ADD): {score_text(txt)} - {txt[:100]}")
        
        # SUB
        plain = []
        for i, c in enumerate(cipher):
            k = key[i % key_len]
            plain.append((c - k) % 29)
        txt = text_from_indices(plain)
        print(f"{name} (SUB): {score_text(txt)} - {txt[:100]}")

if __name__ == "__main__":
    main()

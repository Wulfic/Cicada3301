
import sys
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

COMMON_WORDS = {'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH'}

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

def get_primes(n):
    primes = []
    candidate = 2
    while candidate < n:
        is_p = True
        for p in primes:
            if candidate % p == 0:
                is_p = False
                break
        if is_p:
            primes.append(candidate)
        candidate += 1
    return primes

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    p19_path = os.path.join(repo, "LiberPrimus", "pages", "page_19", "runes.txt")
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    
    cipher = load_runes(p20_path)
    
    # 1. Deor Running Key (Old English)
    print("Testing Deor (Old English) as Running Key...")
    with open(deor_path, 'r', encoding='utf-8') as f:
        deor_lines = f.readlines()
        
    # Extract OE part (first half roughly)
    oe_text = ""
    reading_oe = True
    for line in deor_lines:
        if "MODERN ENGLISH" in line:
            break
        cleaned = "".join([c.upper() for c in line if c.isalpha()])
        oe_text += cleaned
        
    print(f"Deor OE Length: {len(oe_text)}")
    
    # Convert OE text to values (A=24, etc? Or map standard letters to Rune Values?)
    # Since we don't have a direct "Latin to Rune Value" map for standard ABCs in the script usually,
    # we need to reverse LATIN_TABLE or map letters to LATIN_TABLE entries.
    # Note: LATIN_TABLE has 'TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA'.
    # This makes naive mapping hard.
    # Let's try to map the Deor text to Rune Values assuming standard phonetic mapping.
    
    # Simple mapping for testing
    SIMPLE_MAP = {
        'F':0, 'U':1, 'TH':2, 'O':3, 'R':4, 'C':5, 'G':6, 'W':7, 'H':8, 'N':9, 'I':10, 'J':11, 'EO':12, 
        'P':13, 'X':14, 'S':15, 'T':16, 'B':17, 'E':18, 'M':19, 'L':20, 'NG':21, 'OE':22, 'D':23, 
        'A':24, 'AE':25, 'Y':26, 'IA':27, 'EA':28, 'K':5, 'V':0, 'Z':15, 'Q':5 
    }
    # Map letters to values
    key_vals = []
    i = 0
    while i < len(oe_text):
        # Check double chars first
        if i+1 < len(oe_text) and oe_text[i:i+2] in SIMPLE_MAP:
             key_vals.append(SIMPLE_MAP[oe_text[i:i+2]])
             i += 2
        elif oe_text[i] in SIMPLE_MAP:
             key_vals.append(SIMPLE_MAP[oe_text[i]])
             i += 1
        else:
             # Skip unknown or treat as 0?
             i += 1
             
    # Try SUB
    plain = []
    for i, c in enumerate(cipher):
        if i >= len(key_vals): break
        k = key_vals[i]
        plain.append((c - k) % 29)
    print(f"Deor OE Key (SUB): {text_from_indices(plain)[:100]}")
    
    # Try ADD
    plain = []
    for i, c in enumerate(cipher):
        if i >= len(key_vals): break
        k = key_vals[i]
        plain.append((c + k) % 29)
    print(f"Deor OE Key (ADD): {text_from_indices(plain)[:100]}")

    # 2. Primes from Page 19
    print("\nTesting Primes from Page 19...")
    p19_runes = load_runes(p19_path)
    primes = get_primes(len(p19_runes))
    p19_prime_runes = [p19_runes[p] for p in primes]
    
    # Try as running key
    plain = []
    for i, c in enumerate(cipher):
        k = p19_prime_runes[i % len(p19_prime_runes)]
        plain.append((c - k) % 29)
    print(f"P19 Primes (SUB): {text_from_indices(plain)[:100]}")
    
    plain = []
    for i, c in enumerate(cipher):
        k = p19_prime_runes[i % len(p19_prime_runes)]
        plain.append((c + k) % 29)
    print(f"P19 Primes (ADD): {text_from_indices(plain)[:100]}")

if __name__ == "__main__":
    main()

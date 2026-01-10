
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

CHAR_MAP = {
    'a': 24, 'b': 17, 'c': 5, 'd': 23, 'e': 18, 'f': 0, 'g': 6, 'h': 8, 'i': 10, 
    'j': 11, 'k': 5, 'l': 20, 'm': 19, 'n': 9, 'o': 3, 'p': 13, 'q': 5, 'r': 4, 
    's': 15, 't': 16, 'u': 1, 'v': 1, 'w': 7, 'x': 14, 'y': 26, 'z': 15,
    'æ': 25, 'þ': 2, 'ð': 2
}

def get_primes(n):
    primes = []
    candidates = []
    # Generous limit
    candidates = list(range(2, 5000))
    while len(primes) < n and candidates:
        p = candidates.pop(0)
        primes.append(p)
        candidates = [x for x in candidates if x % p != 0]
    return primes

def index_of_coincidence(text):
    if not text: return 0
    counts = {}
    for x in text:
        counts[x] = counts.get(x, 0) + 1
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    if denominator == 0: return 0
    return numerator / denominator * 29.0

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        clean = f.read().replace('-', '').replace(' ', '').replace('\n', '').replace('.', '')
    return [RUNE_MAP[c] for c in clean if c in RUNE_MAP]

def to_latin(runes):
    return "".join([LATIN_TABLE[r] for r in runes])

def load_deor_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    words = []
    read_mode = False
    
    for line in lines:
        if "DEOR POEM (OLD ENGLISH)" in line:
            read_mode = True
            continue
        if "MODERN ENGLISH" in line:
            break
        if read_mode and line.strip():
            # Clean punctuation
            clean_line = line.lower().replace(',', '').replace('.', '').replace(';', '')
            w = clean_line.split()
            words.extend(w)
    return words

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    
    cipher = load_runes(p20_path)
    words = load_deor_words(deor_path)
    print(f"Loaded {len(words)} Deor words.")
    
    # Primes
    primes = get_primes(len(words))
    valid_primes = [p for p in primes if p <= len(words)] # 1-based indexing for words?
    
    print(f"Using {len(valid_primes)} primes as word indices.")
    
    # Extract Words at Prime Indices (1-based: Prime 2 = Word[1])
    key_string = ""
    for p in valid_primes:
        idx = p - 1 # 0-based index
        if 0 <= idx < len(words):
            word = words[idx]
            key_string += word
            
    # Convert Key String to Values
    key_values = []
    for c in key_string:
        if c in CHAR_MAP:
            key_values.append(CHAR_MAP[c])
            
    print(f"Generated Key (len {len(key_values)}): {key_string[:50]}...")
    
    # Extend Key
    while len(key_values) < len(cipher):
        key_values.extend(key_values)
    key_values = key_values[:len(cipher)]
    
    # Decrypt
    plain = [(c - k) % 29 for c, k in zip(cipher, key_values)]
    ioc = index_of_coincidence(plain)
    
    print(f"Deor Prime Words Key (SUB) -> IoC: {ioc:.4f}")
    print(f"Preview: {to_latin(plain[:80])}")
    
    # Try ADD
    plain_add = [(c + k) % 29 for c, k in zip(cipher, key_values)]
    ioc_add = index_of_coincidence(plain_add)
    print(f"Deor Prime Words Key (ADD) -> IoC: {ioc_add:.4f}")

if __name__ == "__main__":
    main()

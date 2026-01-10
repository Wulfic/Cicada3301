
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

# Simple Map for Old English chars to Rune Values
# Handling special chars: æ -> AE(25), þ -> TH(2), ð -> TH(2)
CHAR_MAP = {
    'a': 24, 'b': 17, 'c': 5, 'd': 23, 'e': 18, 'f': 0, 'g': 6, 'h': 8, 'i': 10, 
    'j': 11, 'l': 20, 'm': 19, 'n': 9, 'o': 3, 'p': 13, 'r': 4, 's': 15, 't': 16, 
    'u': 1, 'w': 7, 'x': 14, 'y': 26,
    'æ': 25, 'þ': 2, 'ð': 2
}
# Digraph checks (if needed, but simple char mapping first)

def num_to_english(n):
    # Basic implementation for sorting primes
    # Only need up to ~2000 probably
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 10: return ones[n]
    if n < 20: return teens[n-10]
    if n < 100: return tens[n//10] + ("-" + ones[n%10] if n%10 != 0 else "")
    if n < 1000: return ones[n//100] + " hundred" + (" " + num_to_english(n%100) if n%100 != 0 else "")
    # ... expand if needed
    return "number"

def get_primes(limit):
    primes = []
    candidates = list(range(2, limit+1))
    while candidates:
        p = candidates.pop(0)
        primes.append(p)
        candidates = [x for x in candidates if x % p != 0]
    return primes

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        clean = f.read().replace('-', '').replace(' ', '').replace('\n', '').replace('.', '')
    return [RUNE_MAP[c] for c in clean if c in RUNE_MAP]

def load_deor_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Filter for Old English (stop at Modern English)
    text = ""
    for line in lines:
        if "MODERN ENGLISH" in line: break
        # Clean: keep letters, æ, þ, ð
        clean = "".join([c.lower() for c in line if c.isalpha() or c in "æþð"])
        text += clean
    return text

def index_of_coincidence(text):
    if not text: return 0
    counts = {}
    for x in text:
        counts[x] = counts.get(x, 0) + 1
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    if denominator == 0: return 0
    return numerator / denominator * 29.0  # Normalize for 29 runes

def to_latin(runes):
    return "".join([LATIN_TABLE[r] for r in runes])

def solve():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    
    cipher_runes = load_runes(p20_path)
    deor_clean = load_deor_text(deor_path)
    
    print(f"Updates: Loaded {len(cipher_runes)} runes from P20.")
    print(f"Updates: Loaded {len(deor_clean)} chars from Deor (Old English).")
    
    # Generate Primes
    # We need enough primes to cover the extraction indices.
    # If we are extracting chars, the max index must be < len(deor_clean).
    max_idx = len(deor_clean)
    primes = get_primes(max_idx)
    print(f"Generated {len(primes)} primes up to {max_idx}.")
    
    # Sort Primes Alphabetically
    primes_with_names = [(p, num_to_english(p)) for p in primes]
    primes_sorted = sorted(primes_with_names, key=lambda x: x[1])
    sorted_indices = [x[0] for x in primes_sorted]
    
    # Limit to length of cipher? Or use full sequence?
    # Let's try to build a key of length cipher using the first N sorted primes
    # But wait, the primes themselves are INDICES.
    # If we engage "The Path", maybe we traverse Deor at these indices.
    
    # Method 1: Key = Deor[sorted_prime_1], Deor[sorted_prime_2]...
    key_chars = []
    for idx in sorted_indices:
        if idx < len(deor_clean): # Primes are 1-based usually, Python 0-based.
            # Using 1-based indexing for "Primes Numbers" (2 is 2nd char? Or 2-index?)
            # Let's assume 0-based for now or Try both.
            # Usually primes are 2, 3, 5...
            # Index 2 (0,1,2 = 3rd char)
            key_chars.append(deor_clean[idx]) 
        if len(key_chars) >= len(cipher_runes):
            break
            
    print(f"Generated Key (len {len(key_chars)}): {''.join(key_chars[:50])}...")
    
    # Convert Key Chars to Values
    key_values = []
    for c in key_chars:
        if c in CHAR_MAP:
            key_values.append(CHAR_MAP[c])
        else:
            key_values.append(0) # Default F alignment
            
    # Hack: repeat key if too short (unlikely given dense primes)
    while len(key_values) < len(cipher_runes):
        key_values.extend(key_values)
    key_values = key_values[:len(cipher_runes)]
    
    # Decrypt
    plain = []
    for c, k in zip(cipher_runes, key_values):
        plain.append((c - k) % 29)
        
    ioc = index_of_coincidence(plain)
    preview = to_latin(plain[:80])
    print(f"Result (Sorted Primes Indices -> Deor Chars): IoC={ioc:.4f}")
    print(f"Preview: {preview}")
    
    # Method 2: Use Indices 1-based (idx - 1)
    key_chars_2 = []
    for idx in sorted_indices:
        real_idx = idx - 1
        if 0 <= real_idx < len(deor_clean):
            key_chars_2.append(deor_clean[real_idx])
        if len(key_chars_2) >= len(cipher_runes):
            break
            
    key_values_2 = [CHAR_MAP.get(c, 0) for c in key_chars_2]
    plain_2 = [(c - k) % 29 for c, k in zip(cipher_runes, key_values_2)]
    ioc_2 = index_of_coincidence(plain_2)
    preview_2 = to_latin(plain_2[:80])
    print(f"Result (1-based Indices): IoC={ioc_2:.4f}")
    print(f"Preview: {preview_2}")

if __name__ == "__main__":
    solve()

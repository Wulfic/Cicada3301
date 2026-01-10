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

def get_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_p = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_p = False
                break
        if is_p:
            primes.append(candidate)
        candidate += 1
    return primes

ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def num_to_word(n):
    if n == 0: return "zero"
    parts = []
    
    # Thousands
    if n >= 1000:
        th = n // 1000
        parts.append(num_to_word(th) + " thousand")
        n %= 1000
        
    # Hundreds
    if n >= 100:
        h = n // 100
        parts.append(ONES[h] + " hundred")
        n %= 100
        
    if n > 0:
        if n < 10:
            parts.append(ONES[n])
        elif n < 20:
            parts.append(TEENS[n-10])
        else:
            t = n // 10
            o = n % 10
            s = TENS[t]
            if o > 0:
                s += "-" + ONES[o]
            parts.append(s)
            
    return " ".join(parts)

def calc_ioc(indices):
    if len(indices) < 2: return 0
    c = collections.Counter(indices)
    num = sum(n * (n - 1) for n in c.values())
    den = len(indices) * (len(indices) - 1)
    return num / den * 29.0

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    limit = len(cipher)
    
    # Generate primes
    primes = get_primes(limit)
    
    # Create pairs (word, number)
    pairs = []
    for p in primes:
        w = num_to_word(p)
        pairs.append((w, p))
        
    # Sort by word (Alphabetical text)
    sorted_pairs = sorted(pairs, key=lambda x: x[0])
    
    # Extract rearranged primes
    key = [p[1] for p in sorted_pairs]
    
    # Print preview of key
    print(f"Key Preview: {key[:20]}...")
    
    modes = ['C-K', 'K-C', 'C+K']
    
    for mode in modes:
        res = []
        for i in range(limit):
            c = cipher[i]
            k = key[i] % 29 # Mod 29 for key
            
            if mode == 'C-K': val = (c - k) % 29
            elif mode == 'K-C': val = (k - c) % 29
            elif mode == 'C+K': val = (c + k) % 29
            res.append(val)
            
        ioc = calc_ioc(res)
        txt = "".join([LATIN_TABLE[x] for x in res[:60]])
        print(f"Mode {mode}: IoC={ioc:.4f} | {txt}...")

if __name__ == "__main__":
    main()

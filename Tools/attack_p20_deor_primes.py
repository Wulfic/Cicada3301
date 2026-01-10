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
# Prime GP Indices (0-28 range)
# 2, 3, 5, 7, 11, 13, 17, 19, 23
PRIME_VALUES = {2, 3, 5, 7, 11, 13, 17, 19, 23}

LATIN_TO_VAL = {
    "F": 0, "U": 1, "V": 1, "TH": 2, "O": 3, "R": 4, "C": 5, "K": 5, "Q": 5, 
    "G": 6, "W": 7, "H": 8, "N": 9, "I": 10, "J": 11, "EO": 12, "P": 13, 
    "X": 14, "Z": 15, "S": 15, "T": 16, "B": 17, "E": 18, "M": 19, "L": 20, 
    "NG": 21, "OE": 22, "D": 23, "A": 24, "AE": 25, "Y": 26, "IA": 27, "EA": 28
}

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def parse_oe_text(text):
    text = text.upper().replace('\n', '')
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LATIN_TO_VAL:
                indices.append(LATIN_TO_VAL[two])
                i += 2
                continue
            if two == "AE" or two == "Æ": 
                indices.append(25)
                i += (2 if two=="AE" else 1)
                continue
        
        c = text[i]
        if c == 'Þ' or c == 'Ð': indices.append(2)
        elif c == 'Æ': indices.append(25)
        elif c in LATIN_TO_VAL:
            indices.append(LATIN_TO_VAL[c])
        elif c == ' ': 
            pass
        elif c.isalpha():
             if c == 'Z': indices.append(15)
        i += 1
    return indices

def calc_ioc(indices):
    if len(indices) < 2: return 0
    c = collections.Counter(indices)
    num = sum(n * (n - 1) for n in c.values())
    den = len(indices) * (len(indices) - 1)
    return num / den * 29.0

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    with open(deor_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "MODERN ENGLISH" in content: content = content.split("MODERN ENGLISH")[0]
        if "DEOR POEM (OLD ENGLISH)" in content: content = content.split("DEOR POEM (OLD ENGLISH)")[1]
    
    deor_full = parse_oe_text(content)
    
    # Hyp A: Key = Runes at Prime Indices of Deor
    # 0-based indexing: index 2, 3, 5...
    # 1-based indexing: index 1 (2nd), 2 (3rd), 4 (5th)...
    
    primes_indices_0 = [i for i in range(len(deor_full)) if is_prime(i)]
    key_a0 = [deor_full[i] for i in primes_indices_0]
    
    primes_indices_1 = [i-1 for i in range(1, len(deor_full)+1) if is_prime(i)]
    key_a1 = [deor_full[i] for i in primes_indices_1]
    
    # Hyp B: Key = Runes with Prime GP Values in Deor
    key_b = [r for r in deor_full if r in PRIME_VALUES]
    
    keys = {
        "Deor_PrimeIndices_0": key_a0,
        "Deor_PrimeIndices_1": key_a1,
        "Deor_PrimeValues": key_b
    }
    
    print(f"P20 Length: {len(cipher)}")
    for name, key in keys.items():
        print(f"\n--- Key: {name} (Len: {len(key)}) ---")
        
        # Try modes
        limit = min(len(cipher), len(key))
        
        # C - K
        res = [(cipher[i] - key[i]) % 29 for i in range(limit)]
        ioc = calc_ioc(res)
        txt = "".join([LATIN_TABLE[x] for x in res[:60]])
        print(f"Mode C-K: IoC={ioc:.4f} | {txt}...")
        
        # K - C
        res = [(key[i] - cipher[i]) % 29 for i in range(limit)]
        ioc = calc_ioc(res)
        txt = "".join([LATIN_TABLE[x] for x in res[:60]])
        print(f"Mode K-C: IoC={ioc:.4f} | {txt}...")
        
        # C + K
        res = [(cipher[i] + key[i]) % 29 for i in range(limit)]
        ioc = calc_ioc(res)
        txt = "".join([LATIN_TABLE[x] for x in res[:60]])
        print(f"Mode C+K: IoC={ioc:.4f} | {txt}...")

if __name__ == "__main__":
    main()

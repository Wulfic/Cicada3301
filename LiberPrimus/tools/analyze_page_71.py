
import os
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

NUM_TO_TEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

LATIN_TO_NUM = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28,
    'V': 1, 'Q': 5, 'Z': 14
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    return runes

def get_indices(runes_text):
    return [RUNE_MAP[c] for c in runes_text if c in RUNE_MAP]

def indices_to_text(indices):
    return "".join([NUM_TO_TEXT[x] for x in indices])

def decrypt_indices(cipher_indices, key_indices):
    plain = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        p = (c - k) % 29
        plain.append(p)
    return plain

def score_text(text):
    common = ["THE", "AND", "ING", "ION", "OF", "TO", "A", "IS", "IT", "THAT", "YOU", "WEL", "COM", "BE", "ARE", "NOT"]
    score = 0
    for w in common:
        score += text.count(w) * len(w)
    return score

def calculate_ic(indices):
    N = len(indices)
    if N <= 1: return 0.0
    counts = Counter(indices)
    sum_n_n1 = sum(n*(n-1) for n in counts.values())
    return sum_n_n1 / (N*(N-1))

def main():
    print("--- PAGE 71 ANALYSIS ---")
    runes = load_runes("71")
    cipher = get_indices(runes)
    
    ic = calculate_ic(cipher)
    print(f"Index of Coincidence (Page 71): {ic:.4f}")
    if ic > 0.06:
        print("-> Likely Monoalphabetic / Shift / Transposition")
    else:
        print("-> Likely Polyalphabetic (Vigenere)")
        
    # 1. Try shifting (Caesar)
    print("\n--- CAESAR SHIFT ---")
    for s in range(29):
        plain = [(c - s) % 29 for c in cipher]
        txt = indices_to_text(plain)
        if score_text(txt) > 20: # Arbitrary threshold
             print(f"Shift {s}: {txt[:60]}")

    # 2. Try Dictionary Attack with English Words
    print("\n--- DICTIONARY ATTACK ---")
    keys = ["DIVINITY", "FIRFUMFERENFE", "CICADA", "KAON", "CONSUMPTION", "YAHEOOPYJ", "INSTAR", 
            "INTERCONNECTEDNESS", "PRIMES", "TOTIENT", "SACRED", "CIRCUMFERENCE", "SELFRELIANCE", 
            "WISDOM", "MAGUS", "MOBILIS", "GWERN", "TYLER", "DEEPWEB", "TOR", "HASH", "SHA",
            "TRUTH", "LIGHT", "DARK", "SHADOW", "ILLUMINATION", "ENLIGHTENMENT", "KNOWLEDGE",
            "CODE", "CIPHER", "KEY", "LOCK", "OPEN", "DOOR", "GATE", "PATH", "WAY",
            "LIBER", "PRIMUS", "BOOK", "FIRST", "ONE"]
    
    for k_str in keys:
        k_idxs = []
        i = 0
        text = k_str.upper()
        sorted_k = sorted(LATIN_TO_NUM.keys(), key=len, reverse=True)
        while i < len(text):
             for k in sorted_k:
                if text[i:].startswith(k):
                    k_idxs.append(LATIN_TO_NUM[k])
                    i += len(k)
                    break
        
        plain = decrypt_indices(cipher, k_idxs)
        txt = indices_to_text(plain)
        if score_text(txt) > 10:
             print(f"Key {k_str}: {txt[:60]}")

    # 3. Running Key Guess?
    # Cipher starts: A M NG D IA TH X I M (24, 19, 21, 23, 27, 2, 14, 10, 19)
    # Assume Plain starts with "A WARNING" (Like Page 1?) -> Key?
    # Assume Plain starts with "WELCOME" -> Key?
    # Assume Plain starts with "AN END" -> Key?
    
    print("\n--- CRIB ANALYSIS ---")
    cribs = ["AWARNING", "WELCOME", "ANEND", "THE", "ITIS", "IAM", "DOOR", "KEY"]
    
    for crib in cribs:
        c_idxs = []
        i = 0
        text = crib.upper()
        sorted_k = sorted(LATIN_TO_NUM.keys(), key=len, reverse=True)
        while i < len(text):
             for k in sorted_k:
                if text[i:].startswith(k):
                    c_idxs.append(LATIN_TO_NUM[k])
                    i += len(k)
                    break
        
        # plain = (c - k) => k = (c - p)
        if len(c_idxs) > len(cipher): continue
        
        derived_key = []
        for i in range(len(c_idxs)):
            k = (cipher[i] - c_idxs[i]) % 29
            derived_key.append(k)
            
        key_txt = indices_to_text(derived_key)
        print(f"Crib '{crib}': Key -> {key_txt}")

    print("\n\n--- PAGE 59 ANALYSIS ---")
    runes59 = load_runes("59")
    cipher59 = get_indices(runes59)
    ic59 = calculate_ic(cipher59)
    print(f"Index of Coincidence (Page 59): {ic59:.4f}")
    
    # Try shifts for P59
    print("--- P59 SHIFTS ---")
    for s in range(29):
        plain = [(c - s) % 29 for c in cipher59]
        txt = indices_to_text(plain)
        if score_text(txt) > 20:
             print(f"Shift {s}: {txt[:60]}")

if __name__ == "__main__":
    main()

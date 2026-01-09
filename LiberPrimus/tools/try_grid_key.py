
import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

NUM_TO_RUNETEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

TEXT_TO_RUNE = {v: k for k, v in NUM_TO_RUNETEXT.items()}

KEY_STRING = "LFNTDSAESBBRAWIOEAEEAEAIONTHLNGNUSISJNGNGHOEWPMDIAENGIONBDTHOGTNJBOEFDIOIEHLTHIEONIBNXDWIORJRUJHXGICLAHRMJLCLNIODHOEYJBMUNGEOBEC"

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    indices = [RUNE_MAP[c] for c in runes if c in RUNE_MAP]
    return indices

def parse_key(k_str):
    indices = []
    i = 0
    k_len = len(k_str)
    while i < k_len:
        # Check 2 chars (e.g. TH, EO, NG, AE, OE, IA, EA)
        if i + 1 < k_len:
            two = k_str[i:i+2]
            if two in TEXT_TO_RUNE:
                indices.append(TEXT_TO_RUNE[two])
                i += 2
                continue
        # Check 1 char
        one = k_str[i]
        if one in TEXT_TO_RUNE:
            indices.append(TEXT_TO_RUNE[one])
            i += 1
        else:
            print(f"Warning: Unknown char in key: {one}")
            i += 1
    return indices

def decrypt(cipher, key):
    res = []
    kl = len(key)
    for i, c in enumerate(cipher):
        k = key[i % kl] # Repeating key if shorter
        p = (c - k) % 29
        
        # Output English Text
        res.append(NUM_TO_RUNETEXT[p])
    return "-".join(res)

def main():
    print("Parsing Key...")
    key_indices = parse_key(KEY_STRING)
    print(f"Key Indices: {key_indices}")
    print(f"Key Length: {len(key_indices)}")
    
    # Try Page 18
    print("\n--- PAGE 18 ---")
    c18 = load_runes("18")
    d18 = decrypt(c18, key_indices)
    print(d18[:200]) # First 200 chars
    
    # Try Page 71
    print("\n--- PAGE 71 ---")
    c71 = load_runes("71")
    d71 = decrypt(c71, key_indices)
    print(d71[:200])

if __name__ == "__main__":
    main()

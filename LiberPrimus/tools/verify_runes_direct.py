
import os

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}
# Note: 'ᛂ' (J) is 11. Sometimes 'ᛄ' is J. GP says 11 is J.
# GP Table in GEMATRIA_PRIMUS.md says: 11 ᛂ J.
# But test_p1_key.py used 'ᛄ': 11.
# I will map BOTH to 11.

NUM_TO_TEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}
GP_LATIN_MAP = {v: k for k, v in RUNE_MAP.items()} 
# Reverse latin map for key:
LATIN_TO_NUM = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28,
    'V': 1, 'Q': 5, 'Z': 14
}

def decrypt(runes_text, key_latin):
    key_indices = []
    i = 0
    k_text = key_latin.upper().replace(' ','')
    # Tokenize key
    sorted_k = sorted(LATIN_TO_NUM.keys(), key=len, reverse=True)
    while i < len(k_text):
        matched = False
        for k in sorted_k:
            if k_text[i:].startswith(k):
                key_indices.append(LATIN_TO_NUM[k])
                i += len(k)
                matched = True
                break
        if not matched:
            i += 1 # Skip unknown
            
    cipher_indices = []
    for char in runes_text:
        if char in RUNE_MAP:
            cipher_indices.append(RUNE_MAP[char])
            
    plain_indices = []
    key_len = len(key_indices)
    if key_len == 0: return "No Key"
    
    ki = 0
    for c in cipher_indices:
        # Literal F Rule: If Cipher is F(0), Plain is F(0) and key not advanced?
        # Or "When plaintext is F, cipher is raw ᚠ without encryption (key counter skipped)"
        # This implies: If Plain was F, Cipher became F.
        # So in Decryption: If Cipher is F(0), output F, do NOT consume key.
        if c == 0:
            plain_indices.append(0)
            continue
            
        k = key_indices[ki % key_len]
        p = (c - k) % 29
        plain_indices.append(p)
        ki += 1
        
    return "".join([NUM_TO_TEXT[x] for x in plain_indices])

def main():
    pages = [
        ("17", "YAHEOOPYJ"),
        ("61", "DIVINITY"),
        ("62", "CONSUMPTION"),
        ("64", "KAON"),
        ("67", "CICADA"),
        ("72", "FIRFUMFERENFE")
    ]
    
    for pg, key in pages:
        path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                runes = f.read()
            res = decrypt(runes, key)
            print(f"--- Page {pg} (Key: {key}) ---")
            print(res[:300])
        else:
            print(f"Page {pg} runes not found.")

if __name__ == "__main__":
    main()


import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
INV_RUNE_MAP = {v: k for k, v in RUNE_MAP.items()}
ENGLISH_MAP = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H',
    9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T',
    17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A',
    25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    if not os.path.exists(path): return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '').replace(' ', '').replace('•', '')

def runes_to_vals(runes):
    return [RUNE_MAP[r] for r in runes if r in RUNE_MAP]

def vals_to_eng(vals):
    return "".join([ENGLISH_MAP[v] for v in vals])

def decrypt(cipher, key):
    res = []
    # If key is shorter, repeat it
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        p = (c - k) % 29
        res.append(p)
    return res

def main():
    target_pg = "71"
    cipher_runes = load_runes(target_pg)
    cipher_vals = runes_to_vals(cipher_runes)
    
    target_vals = [23, 18, 5, 4, 26, 13, 16, 10, 3, 9] # DECRYPTION
    
    print(f"Testing Ciphertext Autokey for Page {target_pg}")
    print(f"Cipher length: {len(cipher_vals)}")
    print(f"Target 'DECRYPTION' at index 60")
    
    # Try all offsets 1 to len(cipher)
    for offset in range(1, len(cipher_vals)):
        # Construct key from cipher shifted by offset
        # Key[i] = Cipher[i - offset]
        # But wait, usually Autokey starts with a keyword of length L, then streams cipher/plain.
        # This is equivalent to checking shifts.
        
        # Plain[i] = (Cipher[i] - Key[i]) % 29
        # Key[i] = Cipher[i - offset]
        # Plain[i] = (Cipher[i] - Cipher[i - offset]) % 29
        
        # Check if match at index 60
        match = True
        for j in range(len(target_vals)):
            idx = 60 + j
            if idx - offset < 0: 
                # Key would be from the 'keyword' part, which we don't know
                # So we can matches only if idx >= offset
                match = False # Can't verify
                break
            
            c = cipher_vals[idx]
            k = cipher_vals[idx - offset]
            p = (c - k) % 29
            
            if p != target_vals[j]:
                match = False
                break
        
        if match:
            print(f"MATCH FOUND with Autokey Offset {offset} (Cipher - Cipher[i-offset])")
            # Try to decrypt full
            full_plain = []
            for i in range(len(cipher_vals)):
                if i - offset < 0:
                    full_plain.append(0) # Padding
                else:
                    k = cipher_vals[i - offset]
                    full_plain.append( (cipher_vals[i] - k) % 29 )
            print(vals_to_eng(full_plain))
            
    # Try Variant Beaufort Autokey
    # Plain[i] = (Key[i] - Cipher[i]) % 29 => (Cipher[i-offset] - Cipher[i])
    for offset in range(1, len(cipher_vals)):
        match = True
        for j in range(len(target_vals)):
            idx = 60 + j
            if idx - offset < 0: 
                match = False; break
            
            c = cipher_vals[idx]
            k = cipher_vals[idx - offset]
            p = (k - c) % 29 # Beaufort
            
            if p != target_vals[j]:
                match = False
                break
        if match:
             print(f"MATCH FOUND with Variant Autokey Offset {offset} (Cipher[i-offset] - Cipher)")

if __name__ == "__main__":
    main()

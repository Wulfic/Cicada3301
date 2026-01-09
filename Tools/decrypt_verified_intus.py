
import os

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

# Standard GP Mapping for output
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

def decrypt(runes_text, key_latin, use_f_rule=True):
    key_indices = []
    i = 0
    k_text = key_latin.upper().replace(' ','')
    
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
            i += 1
            
    cipher_indices = []
    for char in runes_text:
        if char in RUNE_MAP:
            cipher_indices.append(RUNE_MAP[char])
            
    plain_indices = []
    key_len = len(key_indices)
    if key_len == 0: return "No Key"
    
    ki = 0
    # Debug print first 5 chars
    debug_cnt = 0
    for c in cipher_indices:
        if use_f_rule and c == 0:
            plain_indices.append(0)
            if debug_cnt < 5:
                print(f"DEBUG {pg}: Cipher {c} (F) -> Plain F")
                debug_cnt += 1
            continue
            
        k = key_indices[ki % key_len]
        p = (c - k) % 29
        plain_indices.append(p)
        if debug_cnt < 5:
             print(f"DEBUG: Cipher {c} Key {k} ({NUM_TO_TEXT[k]}) -> Plain {p} ({NUM_TO_TEXT[p]})")
             debug_cnt += 1
        ki += 1
        
    return "".join([NUM_TO_TEXT[x] for x in plain_indices])

def main():
    pages = [
        ("17", "YAHEOOPYJ", False),
        ("61", "DIVINITY", False), 
        ("62", "CONSUMPTION", False),
        ("64", "KAON", False),
        ("67", "CICADA", False),
        ("72", "FIRFUMFERENFE", False)
    ]
    
    # Pages that appear to be Cleartext
    # Adding 65, 66, 69, 70 to check them
    cleartext_pages = ["58", "59", "60", "63", "65", "66", "68", "69", "70", "71"]
    
    print("# VERIFIED DECRYPTED TEXT (INTUS)\n")
    
    # Process Encrypted
    for pg, key, f_rule in pages:
        path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                runes = f.read()
            
            res = decrypt(runes, key, use_f_rule=f_rule)
            header = f"## Page {pg} (Key: {key}, F-Rule: {f_rule})"
            print(header)
            print("```text")
            print(res)
            print("```\n")
        else:
            print(f"Page {pg} runes not found.")

    # Process Cleartext
    for pg in cleartext_pages:
        path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                runes = f.read()
            
            # Just map directly
            cipher_indices = []
            for char in runes:
                if char in RUNE_MAP:
                    cipher_indices.append(RUNE_MAP[char])
            res = "".join([NUM_TO_TEXT[x] for x in cipher_indices])
            
            print(f"## Page {pg} (CLEARTEXT MAPPING CHECK)")
            print("```text")
            print(res)
            print("```\n")

if __name__ == "__main__":
    main()

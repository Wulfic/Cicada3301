
import os

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

def decrypt_indices(cipher_indices, key_indices):
    plain = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        p = (c - k) % 29
        plain.append(p)
    return plain

def indices_to_text(indices):
    return "".join([NUM_TO_TEXT[x] for x in indices])

def text_to_indices(text):
    text = text.upper()
    indices = []
    i = 0
    sorted_k = sorted(LATIN_TO_NUM.keys(), key=len, reverse=True)
    while i < len(text):
        matched = False
        for k in sorted_k:
            if text[i:].startswith(k):
                indices.append(LATIN_TO_NUM[k])
                i += len(k)
                matched = True
                break
        if not matched:
            i += 1
    return indices

def main():
    runes = load_runes("61")
    cipher = get_indices(runes)
    
    key_text = "DIVINITY"
    key = text_to_indices(key_text)
    
    full_plain = decrypt_indices(cipher, key)
    full_text = indices_to_text(full_plain)
    
    print(f"Full with DIVINITY (First 100 chars): {full_text[:100]}")
    
    # Locate split
    # "TOWARD THE END"
    # T O W A R D T H E E N D
    target_text = "TOWARDTHEEND"
    
    split_index = full_text.find(target_text)
    if split_index == -1:
        print("Could not find split point 'TOWARDTHEEND'")
    else:
        split_end = split_index + len(target_text)
        print(f"Split detected at index {split_end}")
        print(f"Text before split: {full_text[:split_end]}")
        
        remaining_cipher = cipher[split_end:]
        print(f"Remaining Cipher Runes Length: {len(remaining_cipher)}")
        print(f"First 10 of remaining cipher (Indexes): {remaining_cipher[:10]}")
        print(f"First 10 of remaining cipher (Runes as Text): {indices_to_text(remaining_cipher[:10])}")
        
        # Try to guess key
        # Hypotheses:
        # 1. New Key
        # 2. Text is "OF..." or "AND..."
        
        cribs = ["OF", "AND", "THE", "IN", "IS", "IT", "TO"]
        print("\n--- CRIB ANALYSIS ---")
        for crib in cribs:
            crib_indices = text_to_indices(crib)
            # plain = (cipher - key) % 29 => key = (cipher - plain) % 29
            potential_key = []
            for i in range(len(crib_indices)):
                k = (remaining_cipher[i] - crib_indices[i]) % 29
                potential_key.append(k)
            
            key_str = indices_to_text(potential_key)
            print(f"Assuming Plain '{crib}': Key Start -> {key_str}")

    print("\n--- DIVINITY OFFSET CHECK ---")
    div_key = "DIVINITY"
    div_indices = text_to_indices(div_key)
    
    for offset in range(8):
        # Rotate key indices by offset
        shifted_key = div_indices[offset:] + div_indices[:offset]
        plain = decrypt_indices(remaining_cipher, shifted_key)
        plain_text = indices_to_text(plain)
        print(f"Offset {offset}: {plain_text}")
    
    print("\n--- KNOWN KEY CHECK ---")
    keys = ["DIVINITY", "FIRFUMFERENFE", "CICADA", "KAON", "CONSUMPTION", "YAHEOOPYJ", "INSTAR", "INTERCONNECTEDNESS", "PRIMES", "TOTIENT", "SACRED", "CIRCUMFERENCE", "SELFRELIANCE", "WISDOM", "MAGUS", "MOBILIS", "GWERN", "TYLER", "DEEPWEB", "TOR", "HASH", "SHA"]
    
    for key_latin in keys:
        try:
            key_idx = text_to_indices(key_latin)
            plain = decrypt_indices(remaining_cipher, key_idx)
            plain_text = indices_to_text(plain)
            print(f"Key {key_latin}: {plain_text[:50]}")
        except Exception as e:
            pass


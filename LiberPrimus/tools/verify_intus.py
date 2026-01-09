
import os

# Gematria Primus Mapping
GP_MAP = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22, 
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

# Reverse map for printing
GP_R_MAP = {v: k for k, v in GP_MAP.items()}
# Fix duplicates for printing preference
GP_R_MAP[5] = 'C'
GP_R_MAP[21] = 'NG'
GP_R_MAP[27] = 'IO' # or IA

def tokenize(text):
    """Tokenize the runeglish string into GP indices."""
    tokens = []
    i = 0
    text = text.upper().replace('•', '').replace(' ', '').replace('\n', '').replace('-', '')
    
    # Text replacement for some oddities if needed, but basic approach first
    sorted_keys = sorted(GP_MAP.keys(), key=lambda x: len(x), reverse=True)
    
    while i < len(text):
        matched = False
        for k in sorted_keys:
            if text[i:].startswith(k):
                tokens.append(GP_MAP[k])
                i += len(k)
                matched = True
                break
        if not matched:
            # print(f"Warning: Unknown char '{text[i]}' at index {i}")
            i += 1
            
    return tokens

def indices_to_text(indices):
    return "".join([GP_R_MAP.get(x, '?') for x in indices])

def decrypt(cipher, key):
    """Decrypt using Vigenere: Plain = (Cipher - Key) % 29"""
    plain = []
    key_len = len(key)
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        p = (c - k) % 29
        plain.append(p)
    return plain

def process_page(page_num, key_text):
    filename = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\runeglish_output\\page_{page_num}_runeglish.txt"
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    with open(filename, 'r') as f:
        content = f.read()
    
    cipher_indices = tokenize(content)
    
    # Treat key_text
    key_indices = []
    for char in key_text.upper():
        if char == 'V':
            key_indices.append(1)
        elif char == 'Z':
            key_indices.append(14)
        elif char == 'Q':
            key_indices.append(5)
        else:
            if char in GP_MAP:
                key_indices.append(GP_MAP[char])
            else:
                key_indices.append(0) 

    plain_indices = decrypt(cipher_indices, key_indices)
    plain_text = indices_to_text(plain_indices)
    
    print(f"\n--- Page {page_num} Results (Key: {key_text}) ---")
    print(plain_text[:300])

if __name__ == "__main__":
    tests = [
        ("61", "DIVINITY"),
        ("62", "CONSUMPTION"),
        ("64", "KAON"),
        ("67", "CICADA"),
        ("72", "FIRFUMFERENFE"),
        ("17", "YAHEOOPYJ")
    ]
    
    for page, key in tests:
        process_page(page, key)

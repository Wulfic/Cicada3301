
import os

# Gematria Primus Mapping
GP_MAP = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22, 
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}
GP_R_MAP = {v: k for k, v in GP_MAP.items()}
GP_R_MAP[5] = 'C'
GP_R_MAP[21] = 'NG'
GP_R_MAP[27] = 'IO' 

def tokenize(text):
    tokens = []
    i = 0
    text = text.upper().replace('•', '').replace(' ', '').replace('\n', '').replace('-', '')
    text = text.replace(',', '').replace('.', '')
    
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
            i += 1
    return tokens

def indices_to_text(indices):
    return "".join([GP_R_MAP.get(x, '?') for x in indices])

def decrypt(cipher, key):
    plain = []
    # Running key: key is as long as needed (repeat if shorter, but here we assume long enough text)
    if not key: return []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        p = (c - k) % 29
        plain.append(p)
    return plain

def main():
    p3_plain_text = "WELCOME PILGRIM TO THE GREAT JOURNEY TOWARD THE END OF ALL THINGS IT IS NOT AN EASY TRIP BUT FOR THOSE WHO FIND THEIR WAY HERE IT IS A NECESSARY ONE ALONG THE WAY YOU WILL FIND AN END TO ALL STRUGGLE AND SUFFERING YOUR INNOCENCE YOUR ILLUSIONS YOUR CERTAINTY AND YOUR REALITY ULTIMATELY YOU WILL DISCOVER AN END TO SELF"
    
    p3_key = tokenize(p3_plain_text)
    
    # Read Page 61
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\runeglish_output\page_61_runeglish.txt"
    if os.path.exists(path):
        with open(path, 'r') as f:
            cipher_text = f.read()
            
        cipher_indices = tokenize(cipher_text)
        
        # Method 1: Key = P3 Plain
        res1_idx = decrypt(cipher_indices, p3_key)
        res1 = indices_to_text(res1_idx)
        print("--- P61 (Key=P3 Plain) ---")
        print(res1[:300])
        
        # Method 2: Plain = P3 Plain? (Cipher - Key = Plain => Key = Cipher - Plain)
        # Verify if Key looks linguistic
        key_if_plain_is_p3 = []
        min_len = min(len(cipher_indices), len(p3_key))
        for i in range(min_len):
            c = cipher_indices[i]
            p = p3_key[i]
            k = (c - p) % 29
            key_if_plain_is_p3.append(k)
            
        res2 = indices_to_text(key_if_plain_is_p3)
        print("\n--- Key for P61 if Plain is P3 ---")
        print(res2[:300])

if __name__ == "__main__":
    main()


import os
import sys

# Rune to index mapping (Gematria Primus)
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4,
    'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19,
    'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M',
    20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

LETTER_TO_IDX = {}
for idx, letters in LATIN_TABLE.items():
    LETTER_TO_IDX[letters] = idx

LETTER_TO_IDX['K'] = 5
LETTER_TO_IDX['Q'] = 5
LETTER_TO_IDX['V'] = 1
LETTER_TO_IDX['Z'] = 15

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_to_indices(text):
    text = text.upper().replace(' ', '').replace('\n', '')
    indices = []
    i = 0
    digraphs = ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO', 'IA'] 
    
    while i < len(text):
        matched = False
        for dg in digraphs:
            if text[i:i+2] == dg:
                indices.append(LETTER_TO_IDX.get(dg, 0))
                i += 2
                matched = True
                break
        if not matched:
            char = text[i]
            if char in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[char])
            i += 1
    return indices

def decrypt(cipher, key, mode='SUB'):
    if not key: return ""
    dec = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'SUB': p = (c - k) % 29
        elif mode == 'ADD': p = (c + k) % 29
        elif mode == 'SUB_REV': p = (k - c) % 29
        dec.append(LATIN_TABLE[p])
    return "".join(dec)

def score_text(text):
    common = ['THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'THIS', 'NOT', 'FOR', 'BUT', 'ARE', 'ALL', 'FROM']
    score = 0
    for w in common:
        score += text.count(w) * len(w)
    return score

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    
    # Files
    p17_runes_file = os.path.join(repo, "LiberPrimus", "pages", "page_17", "runes.txt")
    p18_runes_file = os.path.join(repo, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    p17_cipher_indices = load_runes(p17_runes_file)
    p18_cipher_indices = load_runes(p18_runes_file)
    
    # Candidate Keys
    # 1. Page 17 Ciphertext (Runes)
    keys = {}
    keys['P17_Runes'] = p17_cipher_indices
    
    # 2. Page 17 Decrypted Plaintext
    p17_plaintext = "EPILOGUE WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO 36367763AB73783C7AF284446C59466B4CD653239A311CB7116D4618DEE09A84 25893DC7500B464FDAF1672D7BEF5E891C6E2274568926A49FB4F45132C2A8B4 IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE AND TO FIND IT"
    keys['P17_Plaintext'] = text_to_indices(p17_plaintext)
    
    # 3. Page 17 Key (YAHEOOPYJ)
    keys['P17_Key'] = text_to_indices("YAHEOOPYJ")
    
    # 4. P17 Plaintext Only Words (No Hash)
    p17_words = "EPILOGUE WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE AND TO FIND IT"
    keys['P17_WordsOnly'] = text_to_indices(p17_words)

    modes = ['SUB', 'ADD', 'SUB_REV']
    
    print(f"P18 Cipher Length: {len(p18_cipher_indices)}")
    
    for k_name, k_indices in keys.items():
        print(f"\n--- Testing Key: {k_name} (Len: {len(k_indices)}) ---")
        for mode in modes:
            # Try direct application
            dec = decrypt(p18_cipher_indices, k_indices, mode)
            s = score_text(dec)
            if s > 20: # Threshold
                 print(f"[{mode}] Score: {s} | {dec[:60]}...")
            
            # Try offsets if key is long enough
            if len(k_indices) > len(p18_cipher_indices):
                for offset in range(1, len(k_indices) - len(p18_cipher_indices)):
                    k_slice = k_indices[offset : offset + len(p18_cipher_indices)]
                    dec = decrypt(p18_cipher_indices, k_slice, mode)
                    s = score_text(dec)
                    if s > 40: # Higher threshold for scan
                         print(f"[{mode} Offset {offset}] Score: {s} | {dec[:60]}...")
                         
    print("\n--- Done ---")

if __name__ == "__main__":
    main()

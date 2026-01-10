
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

INDEX_TO_Runes = {v: k for k, v in RUNE_MAP.items()}

# Latin table for reference/printing
LATIN_TABLE = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M',
    20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

LETTER_TO_IDX = {}
for idx, letters in LATIN_TABLE.items():
    if len(letters) == 1:
         LETTER_TO_IDX[letters] = idx
    else:
         LETTER_TO_IDX[letters] = idx

# Additional mappings
LETTER_TO_IDX['K'] = 5 # C
LETTER_TO_IDX['Q'] = 5 # C
LETTER_TO_IDX['V'] = 1 # U
LETTER_TO_IDX['Z'] = 15 # S (Approximation)

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def load_text_as_indices(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().upper()
    
    # Clean text to only letters
    text = ''.join(c for c in text if c.isalpha())
    
    indices = []
    i = 0
    # Digraphs to check
    digraphs = ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO', 'IA'] 
    
    while i < len(text):
        matched = False
        for dg in digraphs:
            if text[i:i+2] == dg:
                if dg in LETTER_TO_IDX:
                    indices.append(LETTER_TO_IDX[dg])
                    i += 2
                    matched = True
                    break
        if not matched:
            char = text[i]
            if char in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[char])
            else:
                # Fallback for unexpected chars?
                pass
            i += 1
    return indices

def decrypt(cipher_indices, key_indices, mode='SUB'):
    decrypted = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        if mode == 'SUB':
            p = (c - k) % 29
        elif mode == 'ADD':
            p = (c + k) % 29
        elif mode == 'SUB_REV': # k - c
            p = (k - c) % 29
        decrypted.append(LATIN_TABLE[p])
    return "".join(decrypted)

def score_text(text):
    # Simple scoring based on common bigrams/trigrams or words
    common_words = ['THE', 'AND', 'OF', 'TO', 'IN', 'THAT', 'IS', 'FOR', 'NOT', 'WITH']
    score = 0
    for word in common_words:
        score += text.count(word) * len(word)
    return score

def main():
    p18_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt"
    emerson_path = r"c:\Users\tyler\Repos\Cicada3301\Tools\emerson_self_reliance.txt"
    
    if not os.path.exists(p18_path):
        print(f"Error: {p18_path} not found")
        return

    cipher_indices = load_runes(p18_path)
    key_stream = load_text_as_indices(emerson_path)
    
    print(f"Cipher length: {len(cipher_indices)}")
    print(f"Key stream length: {len(key_stream)}")
    
    best_score = 0
    best_result = ""
    
    modes = ['SUB', 'ADD', 'SUB_REV']
    
    # Try every offset
    for mode in modes:
        print(f"Testing mode: {mode}")
        for i in range(len(key_stream) - len(cipher_indices)):
            key_slice = key_stream[i : i + len(cipher_indices)]
            decrypted_text = decrypt(cipher_indices, key_slice, mode)
            score = score_text(decrypted_text)
            
            if score > best_score:
                best_score = score
                best_result = f"Score: {score} Mode: {mode} Offset: {i}\nText: {decrypted_text[:100]}..."
                print(f"New Best: {best_result}")

    print("\nFinal Best Result:")
    print(best_result)

if __name__ == "__main__":
    main()

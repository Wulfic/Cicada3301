
import sys
import random

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

COMMON_WORDS = {
    'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'THIS', 'NOT', 'FOR', 'BUT', 'ARE', 'ALL', 'FROM',
    'CICADA', 'PRIMES', 'TOTIENT', 'ENLIGHTENMENT', 'CONSUMPTION', 'WELCOME', 'PILGRIM', 'INSTRUCTION',
    'WITHIN', 'DEEP', 'WEB', 'EXISTS', 'PAGE', 'HASHES', 'DUTY', 'EVERY', 'SEEK', 'OUT', 'FIND',
    'WARNING', 'BELIEVE', 'NOTHING', 'BOOK', 'INTUS', 'CHAPTER', 'KOAN', 'MASTER', 'LIKE', 'INSTAR',
    'BEING', 'VISIBLE', 'INVISIBLE', 'OATH', 'ABOVE', 'BELOW', 'FORM', 'VOID', 'LIFE', 'DEATH',
    'WILL', 'ONE', 'WAY'
}

TRIGRAMS = {
    'THE': 50, 'AND': 40, 'THA': 30, 'ENT': 30, 'ION': 30, 'ING': 40,
    'HER': 20, 'FOR': 25, 'HIS': 20, 'OFT': 25, 'ITH': 25, 'FTH': 20, 'STH': 20
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    for t, v in TRIGRAMS.items():
        score += text.count(t) * v
    return score

def hill_climb(cipher, key_len, mode='ADD', iterations=1000):
    key = [random.randint(0, 28) for _ in range(key_len)]
    
    current_plain = []
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        if mode == 'ADD':
             # P = (C + K) % 29. Wait. In P19 P = C+K.
             # So Decrypting means finding K to maximize score of P.
             # Wait. Usually P = (C - K) or P = (C + K).
             # If Encryption was C = (P - K) then P = C + K.
             # If Encryption was C = (P + K) then P = C - K.
             # Let's try both modes by changing the decryption formula.
             p = (c + k) % 29
        else:
             p = (c - k) % 29
        current_plain.append(p)
    
    current_text = text_from_indices(current_plain)
    current_score = score_text(current_text)
    
    print(f"Initial Score ({mode}): {current_score}")

    for _ in range(iterations):
        for i in range(key_len):
            best_k = key[i]
            max_s = current_score
            
            original_k = key[i]
            
            for v in range(29):
                key[i] = v
                # Recalculate score (optimize: only check affected chars? No, trigrams overlap. Full rescore for simplicity)
                # Ideally just rescore local context, but Py is fast enough for 1000 runes.
                
                plain_indices = []
                for j, c in enumerate(cipher):
                    k_val = key[j % key_len]
                    if mode == 'ADD':
                        plain_indices.append((c + k_val) % 29)
                    else:
                        plain_indices.append((c - k_val) % 29)
                
                txt = text_from_indices(plain_indices)
                s = score_text(txt)
                
                if s > max_s:
                    max_s = s
                    best_k = v
            
            key[i] = best_k # Update to best found
            current_score = max_s
    
    return current_score, key, text_from_indices(current_plain)

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    print(f"Loaded {len(cipher)} runes.")
    
    # Try Key Length 61 (IoC peak)
    print("--- Attempting Key Length 61 (ADD) ---")
    score_add, key_add, txt_add = hill_climb(cipher, 61, 'ADD', iterations=5)
    print(f"Final Score (ADD): {score_add}")
    print(f"Key (ADD): {text_from_indices(key_add)}")
    print(f"Text (ADD): {txt_add[:200]}")
    
    print("\n--- Attempting Key Length 61 (SUB) ---")
    score_sub, key_sub, txt_sub = hill_climb(cipher, 61, 'SUB', iterations=5)
    print(f"Final Score (SUB): {score_sub}")
    print(f"Key (SUB): {text_from_indices(key_sub)}")
    print(f"Text (SUB): {txt_sub[:200]}")

if __name__ == "__main__":
    main()

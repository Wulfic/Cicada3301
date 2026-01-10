
import os
import sys

# --- Constants ---

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
    'WILL', 'ONE', 'WAY', 'REARRANGING', 'NUMBERS', 'SHOW', 'PATH', 'COVERED', 'COVER'
}

TRIGRAMS = {
    'THE': 50, 'AND': 40, 'THA': 30, 'ENT': 30, 'ION': 30, 'ING': 40,
    'HER': 20, 'FOR': 25, 'HIS': 20, 'OFT': 25, 'ITH': 25, 'FTH': 20, 'STH': 20
}

# Key from crib 'REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR'
# Indices 0-42 known (Assuming ...NOT COVERED)
LOCKED_KEY = [
    24, 15, 2, 24, 4, 21, 11, 10, 20, 16, 
    9, 19, 26, 11, 7, 5, 
    11, 6, 27, 8, 22, 25, 
    21, 16, 25, 0, 27, 9, 
    21, 7, 27, 15, 
    21, 9, 3, 16, 
    5, 22, 18, 4,
    5, 18, 23
]
# ... N O T C OE E R C E D

CURRENT_KEY = [
    24, 15, 2, 24, 4, 21, 11, 10, 20, 16, 9, 19, 26, 11, 7, 5, 
    11, 6, 27, 8, 22, 25, 21, 16, 25, 0, 27, 9, 21, 7, 27, 15, 
    21, 9, 3, 16, 5, 22, 18, 4, 5, 18, 23,
    # Remaining 4 placeholders
    5, 5, 5, 5
]
# Length must be 47
CURRENT_KEY = CURRENT_KEY[:47]
if len(CURRENT_KEY) < 47:
    CURRENT_KEY.extend([0] * (47 - len(CURRENT_KEY)))

MODE = 'ADD'

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def decrypt(cipher, key):
    key_len = len(key)
    res = []
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        if MODE == 'SUB':
            res.append((c - k) % 29)
        elif MODE == 'ADD':
            res.append((c + k) % 29)
    return res

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def score_text(text):
    score = 0
    # Add points for common words
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
            
    # Add points for common trigrams
    for t, v in TRIGRAMS.items():
        score += text.count(t) * v
        
    return score

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "LiberPrimus", "pages", "page_19", "runes.txt")
    
    cipher = load_runes(path)
    print(f"Loaded {len(cipher)} runes.")
    
    current_key = list(CURRENT_KEY)
    
    # Overwrite locked part
    for i in range(len(LOCKED_KEY)):
        current_key[i] = LOCKED_KEY[i]

    current_plain = text_from_indices(decrypt(cipher, current_key))
    current_score = score_text(current_plain)
    
    print(f"Current Score: {current_score}")
    print(f"Key: {text_from_indices(current_key)}")
    print(f"Preview: {current_plain[:200]}...")
    
    improved = True
    while improved:
        improved = False
        # Only iterate over unlocked positions
        for i in range(len(LOCKED_KEY), len(current_key)):
            best_pixel_score = current_score
            best_val = current_key[i]
            
            original = current_key[i]
            
            # Try all 29 runes
            for v in range(29):
                current_key[i] = v
                plain = text_from_indices(decrypt(cipher, current_key))
                s = score_text(plain)
                
                if s > best_pixel_score:
                    best_pixel_score = s
                    best_val = v
            
            if best_val != original:
                current_key[i] = best_val
                current_score = best_pixel_score
                improved = True
                print(f"  Improved position {i} -> {LATIN_TABLE[best_val]} (Score: {current_score})")

    print(f"Current Score: {current_score}")
    print(f"Key: {text_from_indices(current_key)}")
    print(f"Preview: {text_from_indices(decrypt(cipher, current_key))[:200]}...")

    print("--- Final Refined Key ---")
    print(f"Indices: {current_key}")

if __name__ == "__main__":
    main()

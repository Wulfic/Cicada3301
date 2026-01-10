
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
    'BEING', 'VISIBLE', 'INVISIBLE', 'OATH', 'ABOVE', 'BELOW', 'FORM', 'VOID', 'LIFE', 'DEATH'
}


TRIGRAMS = {
    'THE': 100, 'AND': 90, 'THA': 85, 'ENT': 80, 'ION': 80, 'TIO': 75,
    'FOR': 75, 'nde': 70, 'HAS': 70, 'NCE': 65, 'EDT': 65, 'TIS': 65,
    'OFT': 65, 'STH': 65, 'MEN': 65, 'ING': 100, 'HER': 70, 'ARE': 70,
    'ERE': 70, 'ALL': 65, 'WIS': 60, 'DOM': 50, 'MEA': 50, 'INT': 60,
    'OME': 50, 'BUT': 60, 'NOT': 60, 'YOU': 60, 'GHT': 60, 'VER': 50
}

# Current best key from hill climbing
START_KEY = [15, 6, 1, 20, 6, 25, 25, 26, 13, 11, 22, 10, 19, 3, 20, 28, 6, 
9, 6, 3, 25, 25, 9, 20, 8, 0, 17, 7, 13, 14, 25, 4, 4, 2, 18, 6, 3, 25, 13, 3, 21, 1, 10, 5, 14, 11, 1, 23, 3, 9, 20, 17, 10]


def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def decrypt(cipher, key, mode='SUB'):
    key_len = len(key)
    res = []
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        if mode == 'SUB':
            res.append((c - k) % 29)
        elif mode == 'ADD':
            res.append((c + k) % 29)
        elif mode == 'SUB_REV':
            res.append((k - c) % 29)
    return res

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def score_text(text):
    score = 0
    # Trigrams
    for i in range(len(text) - 2):
        tg = text[i:i+3]
        if tg in TRIGRAMS:
            score += TRIGRAMS[tg]
    
    # Common words
    for word in COMMON_WORDS:
        if word in text:
            score += 300 * len(word) # Heavy bonus for full words
            
    return score

def refine_key(cipher, key, mode='SUB'):
    improved = True
    current_key = list(key)
    
    while improved:
        improved = False
        current_plain = decrypt(cipher, current_key, mode)
        current_text = text_from_indices(current_plain)
        current_score = score_text(current_text)
        
        print(f"Current Score: {current_score}")
        print(f"Key: {text_from_indices(current_key)}")
        print(f"Preview: {current_text[:100]}...")
        
        for i in range(len(current_key)):
            best_val = current_key[i]
            best_local_score = current_score
            
            # Try all 29 possiblities for this position
            for val in range(29):
                if val == current_key[i]: continue
                
                temp_key = list(current_key)
                temp_key[i] = val
                
                temp_plain = decrypt(cipher, temp_key, mode)
                temp_text = text_from_indices(temp_plain)
                temp_score = score_text(temp_text)
                
                if temp_score > best_local_score:
                    best_local_score = temp_score
                    best_val = val
            
            if best_val != current_key[i]:
                current_key[i] = best_val
                current_score = best_local_score
                improved = True
                print(f"  Improved position {i} -> {LATIN_TABLE[best_val]} (Score: {current_score})")

    return current_key

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    cipher = load_runes(path)
    print(f"Loaded {len(cipher)} runes.")
    
    final_key = refine_key(cipher, START_KEY, mode='SUB')
    
    print("\n--- Final Refined Key ---")
    print(f"Indices: {final_key}")
    print(f"Key Text: {text_from_indices(final_key)}")
    
    plain = decrypt(cipher, final_key, mode='SUB')
    text = text_from_indices(plain)
    print("\n--- Final Plaintext ---")
    print(text)

if __name__ == "__main__":
    main()

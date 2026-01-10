
import sys
import random
from itertools import permutations

# Constants match previous
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

COMMON_WORDS = {'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'BUT', 'NOT', 'FOR'}
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

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
    return score

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    print("Testing permutations of Primes [2..23] as Key...")
    
    # Primes count = 9. Factorial 9 is 362,880. Fast enough to brute force?
    # Yes.
    
    best_score = 0
    best_perm = None
    best_text = ""
    best_mode = ""
    
    count = 0
    for p in permutations(PRIMES):
        key = list(p)
        key_len = len(key)
        
        # Test SUB
        plain = []
        for i, c in enumerate(cipher):
            k = key[i % key_len]
            plain.append((c - k) % 29)
        txt = text_from_indices(plain)
        s = score_text(txt)
        
        if s > best_score:
            best_score = s
            best_perm = key
            best_text = txt
            best_mode = 'SUB'
            
        # Test ADD
        plain = []
        for i, c in enumerate(cipher):
            k = key[i % key_len]
            plain.append((c + k) % 29)
        txt = text_from_indices(plain)
        s = score_text(txt)
        
        if s > best_score:
            best_score = s
            best_perm = key
            best_text = txt
            best_mode = 'ADD'
            
        count += 1
        if count % 50000 == 0:
            print(f"Checked {count} permutations...")

    print("\n--- Best Prime Permutation ---")
    print(f"Key: {best_perm}")
    print(f"Mode: {best_mode}")
    print(f"Score: {best_score}")
    print(f"Text: {best_text[:200]}")

if __name__ == "__main__":
    main()

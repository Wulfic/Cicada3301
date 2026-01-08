
import os
import sys
import random
from collections import Counter
import argparse

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']
IDX_TO_RUNE = list(RUNE_TO_IDX.keys())

# Runeglish bigram frequencies derived from Page 0
BIGRAM_SCORES = {
    'LE': 52, 'UI': 46, 'IL': 46, 'HE': 33, 'TH': 33, 'IC': 26, 'ET': 19,
    'HA': 19, 'EO': 19, 'WA': 19, 'AR': 19, 'EF': 19, 'AL': 19, 'LC': 13,
    'AN': 13, 'CA': 13, 'NH': 13, 'EA': 13, 'LU': 13, 'RN': 13, 'NF': 13,
    'FS': 13, 'SU': 13, 'FI': 13, 'IS': 13, 'SO': 13, 'OD': 13, 'DI': 13,
    'CE': 13, 'OM': 13, 'MU': 13, 'EU': 13, 'UY': 13, 'YD': 13, 'DN': 13,
    'NU': 13, 'UH': 13, 'AT': 13, 'EN': 13, 'NA': 13, 'AI': 13, 'WE': 6,
    'EL': 6, 'CU': 6, 'UM': 6, 'MA': 6, 'NW': 6, 'WY': 6, 'YL': 6,
}

def load_page(page_num):
    """Load runes from a page."""
    # Try multiple paths
    paths = [
        f"LiberPrimus/pages/page_{page_num:02d}/runes.txt",
        f"pages/page_{page_num:02d}/runes.txt",
        f"../pages/page_{page_num:02d}/runes.txt",
        f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{page_num:02d}\\runes.txt"
    ]
    
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Clean non-rune characters
            runes = [c for c in content if c in RUNE_TO_IDX]
            print(f"Loaded {len(runes)} runes from {path}")
            return [RUNE_TO_IDX[r] for r in runes]
    
    print(f"Could not find runes for page {page_num}")
    return None

def decrypt(cipher, key):
    """Decrypt using p = (c - k) mod 29."""
    return [(c - k) % 29 for c, k in zip(cipher, key * (len(cipher) // len(key) + 1))]

def score_text(plain_indices):
    """Score text based on Page 0 Bigrams."""
    letters = [IDX_TO_LETTER[i] for i in plain_indices]
    text = "".join(letters)
    score = 0
    # Score bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        score += BIGRAM_SCORES.get(bigram, -5) # Improved penalty
    
    # Bonus for known Page 0 words
    words = ["UILE", "EALL", "IAEO", "TH", "EO"]
    for w in words:
        if w in text:
            score += 20 * len(w)
            
    return score

def hill_climb(cipher, key_len, iterations=5000):
    # Initialize random key
    key = [random.randint(0, 28) for _ in range(key_len)]
    best_key = list(key)
    best_score = score_text(decrypt(cipher, key))
    
    no_improve = 0
    
    for i in range(iterations):
        # Mutate
        candidate_key = list(best_key)
        idx = random.randint(0, key_len - 1)
        # Try small changes first, then random
        if random.random() < 0.7:
             change = random.choice([-1, 1, -2, 2])
             candidate_key[idx] = (candidate_key[idx] + change) % 29
        else:
             candidate_key[idx] = random.randint(0, 28)
            
        plain = decrypt(cipher, candidate_key)
        score = score_text(plain)
        
        if score > best_score:
            best_score = score
            best_key = list(candidate_key)
            no_improve = 0
        else:
            no_improve += 1
            
        if no_improve > 2000: # Restart if stuck
             key = [random.randint(0, 28) for _ in range(key_len)]
             plain = decrypt(cipher, key)
             score = score_text(plain)
             if score > best_score: # Only keep if better than global best (unlikely but safe)
                 best_score = score
                 best_key = key
             no_improve = 0
             
    return best_key, best_score

def format_text(indices):
    return "".join([IDX_TO_LETTER[i] for i in indices]).lower()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('page', type=int)
    parser.add_argument('key_len', type=int)
    parser.add_argument('--iter', type=int, default=20000)
    parser.add_argument('--tries', type=int, default=5)
    args = parser.parse_args()
    
    print(f"Analyzing Page {args.page} with Key Length {args.key_len}")
    
    cipher = load_page(args.page)
    if not cipher:
        return

    best_global_score = -float('inf')
    best_global_key = None
    
    for t in range(args.tries):
        key, score = hill_climb(cipher, args.key_len, args.iter)
        print(f"Try {t+1}: Score {score}")
        
        if score > best_global_score:
            best_global_score = score
            best_global_key = key
            
            # Print intermediate best
            plain = decrypt(cipher, key)
            print(f"Intermediate: {format_text(plain)[:60]}...")

    print("="*60)
    print(f"FINAL BEST SCORE: {best_global_score}")
    print(f"KEY: {best_global_key}")
    plain = decrypt(cipher, best_global_key)
    print("TEXT:")
    print(format_text(plain))

if __name__ == "__main__":
    main()

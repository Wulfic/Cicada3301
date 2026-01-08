"""
Hill-climbing key optimization for first-layer decryption.
Based on the proven methodology from pages 0-5.
"""

import os
import random
from collections import Counter

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

# English bigram frequencies (simplified - higher is better)
BIGRAM_SCORES = {
    'TH': 100, 'HE': 80, 'IN': 75, 'ER': 70, 'AN': 68, 'RE': 65, 'ON': 62,
    'AT': 60, 'EN': 58, 'ND': 55, 'TI': 52, 'ES': 50, 'OR': 48, 'TE': 46,
    'OF': 44, 'ED': 42, 'IS': 40, 'IT': 38, 'AL': 36, 'AR': 34, 'ST': 32,
    'TO': 30, 'NT': 28, 'NG': 26, 'SE': 24, 'HA': 22, 'AS': 20, 'OU': 18,
    'IO': 16, 'LE': 14, 'VE': 12, 'CO': 10, 'ME': 8, 'DE': 6, 'HI': 4,
    'RI': 2, 'RO': 1
}

def load_page(page_num):
    """Load runes from a page."""
    path = f"../pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return None
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    runes = [c for c in content if c in RUNE_TO_IDX]
    return [RUNE_TO_IDX[r] for r in runes]

def decrypt(cipher, key):
    """Decrypt using p = (c - k) mod 29."""
    kl = len(key)
    return [(c - key[i % kl]) % 29 for i, c in enumerate(cipher)]

def to_letters(indices):
    """Convert indices to letter string (digraphs collapsed)."""
    letters = []
    for idx in indices:
        letters.append(IDX_TO_LETTER[idx])
    return ''.join(letters)

def score_plaintext(indices):
    """Score plaintext by bigram frequencies."""
    letters = to_letters(indices)
    score = 0
    
    # Bigram scoring
    for i in range(len(letters) - 1):
        bigram = letters[i:i+2]
        if bigram in BIGRAM_SCORES:
            score += BIGRAM_SCORES[bigram]
    
    # Count THE
    score += letters.count('THE') * 50
    
    # Count common words
    for word in ['AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'WAS', 'ONE']:
        score += letters.count(word) * 30
    
    return score

def find_initial_key(cipher, key_length):
    """Find initial key by frequency analysis."""
    cosets = [[] for _ in range(key_length)]
    for i, c in enumerate(cipher):
        cosets[i % key_length].append(c)
    
    key = []
    for coset in cosets:
        if not coset:
            key.append(0)
            continue
        freq = Counter(coset)
        most_common = freq.most_common(1)[0][0]
        # Assume most common maps to E (18)
        shift = (most_common - 18) % 29
        key.append(shift)
    
    return key

def hill_climb(cipher, key, max_iterations=10000):
    """Hill-climbing optimization of key."""
    current_key = list(key)
    current_plain = decrypt(cipher, current_key)
    current_score = score_plaintext(current_plain)
    
    best_key = current_key[:]
    best_score = current_score
    
    no_improve = 0
    for _ in range(max_iterations):
        # Random position to modify
        pos = random.randint(0, len(current_key) - 1)
        
        # Try a random new value
        old_val = current_key[pos]
        new_val = random.randint(0, 28)
        current_key[pos] = new_val
        
        # Score new key
        new_plain = decrypt(cipher, current_key)
        new_score = score_plaintext(new_plain)
        
        if new_score > current_score:
            current_score = new_score
            no_improve = 0
            if new_score > best_score:
                best_key = current_key[:]
                best_score = new_score
        else:
            # Revert
            current_key[pos] = old_val
            no_improve += 1
        
        # Early termination
        if no_improve > len(key) * 20:
            break
    
    return best_key, best_score

def analyze_page(page_num, key_length, num_restarts=5):
    """Analyze a page with hill-climbing."""
    cipher = load_page(page_num)
    if not cipher:
        return None
    
    print(f"\nAnalyzing page {page_num} with key length {key_length}")
    print(f"Cipher length: {len(cipher)}")
    
    # Find initial key
    initial_key = find_initial_key(cipher, key_length)
    
    # Run hill-climbing with restarts
    best_key = initial_key
    best_score = 0
    
    for restart in range(num_restarts):
        # Random perturbation for restarts
        if restart > 0:
            start_key = [random.randint(0, 28) for _ in range(key_length)]
        else:
            start_key = initial_key
        
        key, score = hill_climb(cipher, start_key)
        if score > best_score:
            best_key = key
            best_score = score
            print(f"  Restart {restart+1}: Score {score}")
    
    # Final decryption
    plain = decrypt(cipher, best_key)
    letters = to_letters(plain)
    
    print(f"\nBest score: {best_score}")
    print(f"Key (first 30): {best_key[:30]}...")
    print(f"\nDecryption (first 300 chars):")
    print(letters[:300])
    
    # Pattern counts
    th = letters.count('TH')
    the = letters.count('THE')
    and_ = letters.count('AND')
    print(f"\nPatterns - TH: {th}, THE: {the}, AND: {and_}")
    
    # Check reversibility
    re_encrypted = [(p + best_key[i % len(best_key)]) % 29 for i, p in enumerate(plain)]
    match = all(c == r for c, r in zip(cipher, re_encrypted))
    print(f"Reversibility: {'100% ✓' if match else 'FAILED'}")
    
    return {
        'page': page_num,
        'key_length': key_length,
        'score': best_score,
        'key': best_key,
        'letters': letters,
        'th': th,
        'the': the
    }

def main():
    # Test on best candidate pages
    candidates = [
        (43, 71),   # Page 43, key length 71 (prime) - best freq results
        (46, 109),  # Page 46, key length 109 (prime) - highest IoC
        (8, 101),   # Page 8, key length 101 (prime)
    ]
    
    print("="*70)
    print("HILL-CLIMBING KEY OPTIMIZATION")
    print("="*70)
    
    results = []
    for page, kl in candidates:
        result = analyze_page(page, kl)
        if result:
            results.append(result)
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    for r in results:
        print(f"Page {r['page']}: Score {r['score']}, TH={r['th']}, THE={r['the']}")

if __name__ == '__main__':
    main()

"""
Comprehensive Vigenère key recovery for unsolved pages.
Uses hill-climbing with known-good key lengths (primes).
"""

import os
import random
from collections import Counter

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# English trigram frequencies (approximate log probabilities)
TRIGRAMS = {
    'THE': 8.0, 'AND': 6.5, 'ING': 6.0, 'HER': 5.5, 'HAT': 5.0,
    'HIS': 5.0, 'THA': 5.0, 'ERE': 4.5, 'FOR': 4.5, 'ENT': 4.5,
    'ION': 4.5, 'TER': 4.5, 'WAS': 4.5, 'YOU': 4.5, 'ITH': 4.5,
    'VER': 4.5, 'ALL': 4.5, 'WIT': 4.0, 'THI': 4.0, 'TIO': 4.0,
    'OTH': 4.0, 'NOT': 4.0, 'OUT': 4.0, 'ARE': 4.0, 'BUT': 4.0,
}

def rune_to_index(rune):
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

def load_page(page_num):
    page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    subdir = f"page_{page_num:02d}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Skip note lines
            lines = content.split('\n')
            rune_lines = [l for l in lines if not l.startswith('Note:') and not l.startswith('#')]
            runes = [c for c in ''.join(rune_lines) if c in GP_RUNES]
            return runes
    return []

def calculate_ioc(indices):
    n = len(indices)
    if n <= 1:
        return 0
    counts = Counter(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29

def indices_to_latin(indices):
    return ''.join(index_to_latin(i) for i in indices)

def apply_vigenere(cipher_indices, key_indices, mode='sub'):
    """Apply Vigenère cipher"""
    result = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        if mode == 'sub':
            p = (c - k) % 29
        else:  # add
            p = (c + k) % 29
        result.append(p)
    return result

def score_text(indices):
    """Score text based on trigram frequency and IoC"""
    text = indices_to_latin(indices).upper()
    score = 0
    
    # Trigram score
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in TRIGRAMS:
            score += TRIGRAMS[trigram]
    
    # IoC bonus
    ioc = calculate_ioc(indices)
    if ioc > 1.3:
        score += (ioc - 1.0) * 50
    
    return score

def hill_climb(cipher_indices, key_length, mode='sub', iterations=10000):
    """Hill-climbing to find best key"""
    # Start with random key
    key = [random.randint(0, 28) for _ in range(key_length)]
    plain = apply_vigenere(cipher_indices, key, mode)
    best_score = score_text(plain)
    best_key = key[:]
    
    no_improvement = 0
    for _ in range(iterations):
        # Random mutation
        pos = random.randint(0, key_length - 1)
        old_val = key[pos]
        key[pos] = random.randint(0, 28)
        
        plain = apply_vigenere(cipher_indices, key, mode)
        score = score_text(plain)
        
        if score > best_score:
            best_score = score
            best_key = key[:]
            no_improvement = 0
        else:
            key[pos] = old_val  # Revert
            no_improvement += 1
            
        # Early stop if stuck
        if no_improvement > 2000:
            break
    
    return best_key, best_score

def main():
    print("="*60)
    print("VIGENÈRE KEY RECOVERY (Hill-Climbing)")
    print("="*60)
    
    # Prime key lengths to try
    key_lengths = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    
    # Pages to analyze
    pages_to_test = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    for page_num in pages_to_test:
        runes = load_page(page_num)
        if not runes or len(runes) < 50:
            continue
        
        cipher_indices = [rune_to_index(r) for r in runes if rune_to_index(r) is not None]
        
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}: {len(cipher_indices)} runes")
        print(f"{'='*60}")
        
        best_overall = None
        best_overall_score = 0
        
        for kl in key_lengths:
            if kl > len(cipher_indices) // 3:
                continue
                
            for mode in ['sub', 'add']:
                key, score = hill_climb(cipher_indices, kl, mode, iterations=5000)
                
                if score > best_overall_score:
                    best_overall_score = score
                    plain = apply_vigenere(cipher_indices, key, mode)
                    ioc = calculate_ioc(plain)
                    best_overall = {
                        'key_length': kl,
                        'mode': mode,
                        'key': key,
                        'score': score,
                        'ioc': ioc,
                        'text': indices_to_latin(plain)[:80]
                    }
        
        if best_overall:
            print(f"Best: Key Length={best_overall['key_length']}, Mode={best_overall['mode']}")
            print(f"      Score={best_overall['score']:.1f}, IoC={best_overall['ioc']:.4f}")
            print(f"      Key={best_overall['key']}")
            print(f"      Text: {best_overall['text']}")
            
            # Try to interpret key as letters
            key_latin = indices_to_latin(best_overall['key'])
            print(f"      Key as text: {key_latin}")

if __name__ == "__main__":
    main()

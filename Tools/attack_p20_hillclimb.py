"""
Page 20 - Hill Climbing Attack
===============================
Use hill climbing to find optimal column permutation + key combination.
"""

import collections
import random
import copy

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

# Quadgram statistics (approximation for English)
COMMON_BIGRAMS = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'ON', 'EN', 'AT', 'OU', 'ED', 'HA', 'TO', 'OR', 'IT', 'IS', 'HI', 'ES', 'NG']
COMMON_TRIGRAMS = ['THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE', 'FOR', 'ENT', 'ION', 'TER', 'WAS', 'YOU', 'ITH', 'VER', 'ALL', 'WIT', 'THI', 'TIO']

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def score_text(indices):
    """Score based on IoC and English patterns"""
    text = runes_to_latin(indices)
    
    # Base IoC score
    ioc = calculate_ioc(indices)
    score = ioc * 100
    
    # Bonus for common patterns
    for bg in COMMON_BIGRAMS[:10]:
        score += text.count(bg) * 2
    
    for tg in COMMON_TRIGRAMS[:10]:
        score += text.count(tg) * 5
    
    # Bonus for 'THE'
    score += text.count('THE') * 10
    
    return score

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    try:
        with open(deor_path, 'r', encoding='utf-8') as f:
            text = f.read().upper()
    except:
        return []
    return [ENGLISH_TO_IDX.get(c, 0) for c in text if c in ENGLISH_TO_IDX]

def apply_permutation(runes, col_perm, rows=28, cols=29):
    """Apply column permutation to grid"""
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    result = []
    for r in range(rows):
        for c in col_perm:
            if c < len(grid[r]):
                result.append(grid[r][c])
    return result

def decrypt_vigenere(cipher, key):
    """Vigenère decrypt"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        result.append((c - k) % 29)
    return result

def mutate_permutation(perm):
    """Mutate by swapping two random positions"""
    new_perm = list(perm)
    i, j = random.sample(range(len(new_perm)), 2)
    new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
    return new_perm

def hill_climb_permutation(runes, key, iterations=50000):
    """Hill climb to find best column permutation"""
    cols = 29
    
    # Start with identity permutation
    best_perm = list(range(cols))
    best_text = apply_permutation(runes, best_perm)
    best_decrypted = decrypt_vigenere(best_text, key)
    best_score = score_text(best_decrypted)
    
    no_improve = 0
    
    for i in range(iterations):
        # Mutate
        new_perm = mutate_permutation(best_perm)
        new_text = apply_permutation(runes, new_perm)
        new_decrypted = decrypt_vigenere(new_text, key)
        new_score = score_text(new_decrypted)
        
        if new_score > best_score:
            best_perm = new_perm
            best_text = new_text
            best_decrypted = new_decrypted
            best_score = new_score
            no_improve = 0
            
            if i % 1000 == 0:
                print(f"  Iter {i}: Score={best_score:.1f}, IoC={calculate_ioc(best_decrypted):.4f}")
        else:
            no_improve += 1
        
        # Random restart if stuck
        if no_improve > 5000:
            best_perm = list(range(cols))
            random.shuffle(best_perm)
            no_improve = 0
    
    return best_perm, best_decrypted, best_score

def main():
    print("="*60)
    print("PAGE 20 - HILL CLIMBING ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    
    print(f"Loaded {len(runes)} runes")
    print(f"Deor length: {len(deor)}")
    
    # Extend Deor key
    key = deor * (len(runes) // len(deor) + 1)
    key = key[:len(runes)]
    
    print("\n--- Hill Climbing with Deor Key ---")
    best_perm, best_decrypted, best_score = hill_climb_permutation(runes, key, iterations=30000)
    
    print(f"\nBest score: {best_score:.1f}")
    print(f"Best IoC: {calculate_ioc(best_decrypted):.4f}")
    print(f"Best permutation: {best_perm}")
    print(f"\nDecrypted text:")
    text = runes_to_latin(best_decrypted)
    for i in range(0, min(500, len(text)), 80):
        print(f"  {text[i:i+80]}")
    
    # Try without key (just find best transposition for IoC)
    print("\n--- Hill Climbing without Key (Pure Transposition) ---")
    
    def score_ioc_only(indices):
        return calculate_ioc(indices) * 100
    
    best_perm = list(range(29))
    best_text = apply_permutation(runes, best_perm)
    best_score = score_ioc_only(best_text)
    
    for i in range(20000):
        new_perm = mutate_permutation(best_perm)
        new_text = apply_permutation(runes, new_perm)
        new_score = score_ioc_only(new_text)
        
        if new_score > best_score:
            best_perm = new_perm
            best_text = new_text
            best_score = new_score
    
    print(f"Best IoC (transposition only): {calculate_ioc(best_text):.4f}")
    print(f"Best permutation: {best_perm}")
    
    # Now apply Deor to this
    decrypted = decrypt_vigenere(best_text, key)
    print(f"After Deor: IoC={calculate_ioc(decrypted):.4f}")
    print(f"Text: {runes_to_latin(decrypted[:200])}")
    
    # Try a few different key lengths based on primes
    print("\n--- Testing Different Key Lengths ---")
    
    for key_len in [29, 47, 41, 37, 31, 23, 19, 17, 13, 11, 7]:
        # Use first key_len chars of Deor, repeated
        short_key = deor[:key_len]
        extended_key = short_key * (len(runes) // key_len + 1)
        extended_key = extended_key[:len(runes)]
        
        decrypted = decrypt_vigenere(runes, extended_key)
        ioc = calculate_ioc(decrypted)
        
        print(f"Key len {key_len}: IoC={ioc:.4f}")
        if ioc > 1.1:
            print(f"  Preview: {runes_to_latin(decrypted[:80])}")

if __name__ == "__main__":
    main()

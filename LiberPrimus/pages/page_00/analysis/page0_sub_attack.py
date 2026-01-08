#!/usr/bin/env python3
"""
Page 0 SUB Attack with Hill Climbing
====================================
Test SUB mod 29 operation with key lengths 92 (best IoC) and 83 (prime, Page 2/3 key length)
Using the same approach that successfully solved Pages 1-4.
"""

import random
import math
from collections import Counter

# Gematria Primus
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_RUNE = {v: k for k, v in RUNE_TO_INDEX.items()}
INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                   'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                   'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# English trigram frequencies (log probabilities)
COMMON_TRIGRAMS = {
    'THE': 3.5, 'AND': 3.0, 'ING': 2.8, 'HER': 2.5, 'ERE': 2.5,
    'ENT': 2.4, 'THA': 2.3, 'NTH': 2.3, 'WAS': 2.2, 'ETH': 2.2,
    'FOR': 2.1, 'DTH': 2.1, 'HAT': 2.1, 'SHE': 2.1, 'HES': 2.1,
    'HIS': 2.0, 'ERS': 2.0, 'ITH': 2.0, 'ALL': 2.0, 'ATE': 2.0,
    'EST': 2.0, 'OFT': 2.0, 'STH': 2.0, 'OTH': 2.0, 'RES': 2.0,
    'NGT': 1.9, 'TIO': 1.9, 'ION': 1.9, 'TED': 1.8, 'WIT': 1.8,
    'TER': 1.8, 'HAV': 1.8, 'VER': 1.8, 'EVE': 1.8, 'HEI': 1.8
}

COMMON_BIGRAMS = {
    'TH': 2.5, 'HE': 2.4, 'IN': 2.2, 'ER': 2.1, 'AN': 2.0,
    'RE': 2.0, 'ED': 1.9, 'ON': 1.9, 'ES': 1.8, 'ST': 1.8,
    'EN': 1.8, 'AT': 1.7, 'TO': 1.7, 'NT': 1.7, 'HA': 1.6,
    'ND': 1.6, 'OU': 1.6, 'EA': 1.6, 'NG': 1.5, 'AS': 1.5,
    'OR': 1.5, 'TI': 1.5, 'IS': 1.5, 'IT': 1.5, 'AR': 1.4,
    'TE': 1.4, 'SE': 1.4, 'HI': 1.4, 'OF': 1.4, 'LE': 1.4
}

# English letter frequency weights
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5
}

def load_runes(filepath):
    """Load runes from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [RUNE_TO_INDEX[c] for c in text if c in RUNE_TO_INDEX]

def sub_decrypt(cipher_indices, key):
    """SUB operation: plaintext[i] = (cipher[i] - key[i mod len(key)]) mod 29"""
    key_len = len(key)
    return [(cipher_indices[i] - key[i % key_len]) % 29 for i in range(len(cipher_indices))]

def sub_encrypt(plain_indices, key):
    """Reverse SUB: cipher[i] = (plaintext[i] + key[i mod len(key)]) mod 29"""
    key_len = len(key)
    return [(plain_indices[i] + key[i % key_len]) % 29 for i in range(len(plain_indices))]

def indices_to_text(indices):
    """Convert indices to text representation."""
    return ''.join(INDEX_TO_LETTER[i] for i in indices)

def score_text(indices):
    """Score plaintext based on English-like patterns."""
    text = indices_to_text(indices)
    score = 0.0
    
    # Trigram scoring
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in COMMON_TRIGRAMS:
            score += COMMON_TRIGRAMS[trigram]
    
    # Bigram scoring
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in COMMON_BIGRAMS:
            score += COMMON_BIGRAMS[bigram]
    
    # Letter frequency scoring (mild)
    for idx in indices:
        letter = INDEX_TO_LETTER[idx]
        if letter in ENGLISH_FREQ:
            score += ENGLISH_FREQ[letter] * 0.01
    
    return score

def hill_climb(cipher_indices, key_length, iterations=10000):
    """Hill climbing optimization to find optimal key."""
    # Start with random key
    key = [random.randint(0, 28) for _ in range(key_length)]
    
    best_key = key[:]
    best_score = score_text(sub_decrypt(cipher_indices, key))
    
    no_improve_count = 0
    
    for iteration in range(iterations):
        # Mutate: change one key position
        pos = random.randint(0, key_length - 1)
        old_val = key[pos]
        key[pos] = random.randint(0, 28)
        
        plain = sub_decrypt(cipher_indices, key)
        score = score_text(plain)
        
        if score > best_score:
            best_score = score
            best_key = key[:]
            no_improve_count = 0
        else:
            key[pos] = old_val
            no_improve_count += 1
        
        # Early termination if stuck
        if no_improve_count > 2000:
            # Restart with random key
            key = [random.randint(0, 28) for _ in range(key_length)]
            no_improve_count = 0
    
    return best_key, best_score

def verify_reversibility(cipher_indices, key):
    """Check if decrypt->encrypt gives original ciphertext."""
    plain = sub_decrypt(cipher_indices, key)
    re_encrypted = sub_encrypt(plain, key)
    return cipher_indices == re_encrypted

def analyze_key_length(cipher_indices, key_length, runs=5):
    """Run multiple hill climbing attempts for a key length."""
    print(f"\n{'='*60}")
    print(f"TESTING KEY LENGTH: {key_length}")
    print(f"{'='*60}")
    
    best_overall_key = None
    best_overall_score = -1
    
    for run in range(runs):
        key, score = hill_climb(cipher_indices, key_length, iterations=15000)
        
        if score > best_overall_score:
            best_overall_score = score
            best_overall_key = key
        
        print(f"  Run {run+1}: Score = {score:.2f}")
    
    # Final result
    plain = sub_decrypt(cipher_indices, best_overall_key)
    text = indices_to_text(plain)
    
    reversible = verify_reversibility(cipher_indices, best_overall_key)
    
    print(f"\nBest score: {best_overall_score:.2f}")
    print(f"Reversible: {reversible}")
    print(f"\nPlaintext preview (first 200 chars):")
    print(text[:200])
    
    # Show word-like segments
    print(f"\nPlaintext (with spaces every 5 chars):")
    spaced = ' '.join(text[i:i+5] for i in range(0, min(len(text), 200), 5))
    print(spaced)
    
    return best_overall_key, best_overall_score, text, reversible

def main():
    filepath = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt"
    cipher = load_runes(filepath)
    
    print("PAGE 0 SUB ATTACK ANALYSIS")
    print("=" * 60)
    print(f"Total runes: {len(cipher)}")
    
    # Key lengths to test based on IoC analysis
    key_lengths = [
        92,   # Best IoC (0.076)
        83,   # Second best, prime (Page 2,3 key length)
        75,   # Third best IoC
        113,  # Prime candidate
        101,  # Prime candidate
        131,  # Half of 262 (total runes)
        41,   # Smaller prime with good IoC
    ]
    
    results = []
    
    for kl in key_lengths:
        if kl < len(cipher) // 2:
            key, score, text, rev = analyze_key_length(cipher, kl, runs=3)
            results.append({
                'key_length': kl,
                'score': score,
                'key': key,
                'text': text,
                'reversible': rev
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    for r in results:
        print(f"KeyLen {r['key_length']:3}: Score {r['score']:7.2f}  Reversible: {r['reversible']}")
    
    # Save best result
    best = results[0]
    output_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\analysis\PAGE0_SUB_RESULT.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"PAGE 0 SUB ATTACK RESULTS\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Best key length: {best['key_length']}\n")
        f.write(f"Best score: {best['score']:.2f}\n")
        f.write(f"Reversible: {best['reversible']}\n\n")
        f.write(f"Key:\n{best['key']}\n\n")
        f.write(f"Plaintext:\n{best['text']}\n\n")
        
        f.write("ALL RESULTS:\n")
        f.write("-" * 40 + "\n")
        for r in results:
            f.write(f"KeyLen {r['key_length']}: Score {r['score']:.2f}\n")
            f.write(f"Text preview: {r['text'][:100]}\n\n")
    
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()

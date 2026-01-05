#!/usr/bin/env python3
"""
Test Page 1 with key length 93 (IoC top rank) vs 71 (previously used)
Compare scores and reversibility
"""

import os
from collections import Counter
from pathlib import Path

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page1():
    """Load Page 1 from transcription file"""
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_runes = segments[0]
    page1_indices = [RUNE_TO_INDEX[c] for c in page1_runes if c in RUNE_TO_INDEX]
    
    return page1_indices

def decrypt_sub(cipher_indices, key_indices):
    """Decrypt with SUB"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def encrypt_sub(plaintext_indices, key_indices):
    """Encrypt with SUB"""
    cipher = []
    for i, p in enumerate(plaintext_indices):
        k = key_indices[i % len(key_indices)]
        cipher.append((p + k) % 29)
    return cipher

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """Score English-likeness"""
    text = text.upper()
    
    common_trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10
    }
    
    common_bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7
    }
    
    score = 0.0
    
    for i in range(len(text) - 2):
        if text[i:i+3] in common_trigrams:
            score += common_trigrams[text[i:i+3]]
    
    for i in range(len(text) - 1):
        if text[i:i+2] in common_bigrams:
            score += common_bigrams[text[i:i+2]]
    
    return score

def generate_frequency_key_sub(cipher_indices, key_length):
    """Generate frequency-based key for SUB"""
    key = []
    for i in range(key_length):
        coset = [cipher_indices[j] for j in range(i, len(cipher_indices), key_length)]
        if not coset:
            key.append(0)
            continue
        most_common = Counter(coset).most_common(1)[0][0]
        key_val = (most_common - 18) % 29
        key.append(key_val)
    
    return key

def check_reversibility(cipher_indices, key_indices):
    """Check reversibility"""
    plaintext = decrypt_sub(cipher_indices, key_indices)
    re_encrypted = encrypt_sub(plaintext, key_indices)
    matches = sum(1 for c1, c2 in zip(cipher_indices, re_encrypted) if c1 == c2)
    return matches, len(cipher_indices)

def local_search_quick(cipher_indices, initial_key, max_iterations=100):
    """Quick local search"""
    current_key = initial_key[:]
    current_score = score_english(indices_to_text(decrypt_sub(cipher_indices, current_key)))
    
    improvements = 0
    
    for iteration in range(max_iterations):
        improved = False
        
        for i in range(len(current_key)):
            for delta in [-1, 1]:
                test_key = current_key[:]
                test_key[i] = (current_key[i] + delta) % 29
                
                plaintext = decrypt_sub(cipher_indices, test_key)
                test_score = score_english(indices_to_text(plaintext))
                
                if test_score > current_score:
                    current_key = test_key
                    current_score = test_score
                    improvements += 1
                    improved = True
                    break
            
            if improved:
                break
        
        if not improved:
            break
    
    return current_key, current_score, improvements

def main():
    print("=" * 80)
    print("PAGE 1 - COMPARING KEY LENGTH 71 vs 93")
    print("=" * 80)
    
    cipher_indices = load_page1()
    print(f"\nPage 1 length: {len(cipher_indices)} runes")
    
    results = []
    
    for key_length in [71, 93]:
        print(f"\n{'=' * 80}")
        print(f"TESTING KEY LENGTH: {key_length}")
        print(f"{'=' * 80}")
        
        # Generate frequency key
        key = generate_frequency_key_sub(cipher_indices, key_length)
        print(f"Generated key length: {len(key)}")
        
        # Check reversibility
        matches, total = check_reversibility(cipher_indices, key)
        print(f"Reversibility (frequency key): {matches}/{total} = {100*matches/total:.1f}%")
        
        # Initial score
        plaintext = decrypt_sub(cipher_indices, key)
        plaintext_text = indices_to_text(plaintext)
        initial_score = score_english(plaintext_text)
        print(f"Initial score: {initial_score:.2f}")
        print(f"Preview: {plaintext_text[:80]}")
        
        # Quick optimization
        print(f"\nOptimizing (max 100 iterations)...")
        optimized_key, optimized_score, improvements = local_search_quick(cipher_indices, key, 100)
        
        # Final reversibility
        matches, total = check_reversibility(cipher_indices, optimized_key)
        
        print(f"\nFinal score: {optimized_score:.2f}")
        print(f"Improvements: {improvements}")
        print(f"Reversibility: {matches}/{total} = {100*matches/total:.1f}%")
        
        optimized_plaintext = decrypt_sub(cipher_indices, optimized_key)
        optimized_text = indices_to_text(optimized_plaintext)
        print(f"Preview: {optimized_text[:80]}")
        
        results.append({
            'key_length': key_length,
            'initial_score': initial_score,
            'final_score': optimized_score,
            'improvements': improvements,
            'reversibility': matches / total,
            'plaintext': optimized_text
        })
    
    # Comparison
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    
    print(f"\n{'Key Length':<12} {'Initial':<12} {'Final':<12} {'Improv':<10} {'Revers':<10}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['key_length']:<12} {r['initial_score']:<12.2f} {r['final_score']:<12.2f} {r['improvements']:<10} {r['reversibility']:<10.1%}")
    
    best = max(results, key=lambda x: x['final_score'])
    print(f"\n✓ Best key length: {best['key_length']} (score: {best['final_score']:.2f})")
    
    if best['reversibility'] == 1.0:
        print("✓ Perfect reversibility confirmed")
    
    print(f"\nBest plaintext:\n{best['plaintext']}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    if results[0]['final_score'] > results[1]['final_score']:
        print("Key length 71 performs BETTER than 93")
        print("Previous analysis was correct despite IoC ranking")
    else:
        print("Key length 93 performs BETTER than 71")
        print("Should use IoC top-ranked key length")

if __name__ == '__main__':
    main()

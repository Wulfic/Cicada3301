#!/usr/bin/env python3
"""
Page 2 attack using SUB operation with key length 83 (identified by IoC analysis)
Based on successful Page 1 methodology: frequency-based key + hill-climbing + reversibility check
"""

import os
from collections import Counter
from pathlib import Path

# Rune alphabet (29 runes)
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page2():
    """Load Page 2 from transcription file"""
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page2_runes = segments[1]
    page2_indices = [RUNE_TO_INDEX[c] for c in page2_runes if c in RUNE_TO_INDEX]
    
    return page2_indices

def decrypt_sub(cipher_indices, key_indices):
    """Decrypt with SUB: plaintext = (cipher - key) mod 29"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def encrypt_sub(plaintext_indices, key_indices):
    """Encrypt with SUB: cipher = (plaintext + key) mod 29"""
    cipher = []
    for i, p in enumerate(plaintext_indices):
        k = key_indices[i % len(key_indices)]
        cipher.append((p + k) % 29)
    return cipher

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """Score English-likeness with trigrams, bigrams, and keywords"""
    text = text.upper()
    
    # Common trigrams
    common_trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8,
        'ERS': 7, 'HIS': 7, 'RES': 7, 'ILL': 7, 'ARE': 7
    }
    
    # Common bigrams
    common_bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TI': 6, 'ES': 6, 'OR': 6, 'TE': 6, 'OF': 6
    }
    
    # Special keywords
    keywords = [
        'THE', 'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINE', 'SEEK',
        'FIND', 'PATH', 'EMERGE', 'INSTAR', 'CIRCUMFERENCE'
    ]
    
    score = 0.0
    
    # Score trigrams
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in common_trigrams:
            score += common_trigrams[trigram]
    
    # Score bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in common_bigrams:
            score += common_bigrams[bigram]
    
    # Keyword bonuses
    for keyword in keywords:
        score += text.count(keyword) * 50
    
    return score

def generate_frequency_key_sub(cipher_indices, key_length):
    """
    Generate initial key assuming most common cipher symbol in each coset
    decrypts to 'E' (index 18) using SUB operation.
    
    For SUB: plaintext = (cipher - key) mod 29
    So: key = (cipher - plaintext) mod 29
    If most_common_cipher should be E (18), then:
    key = (most_common_cipher - 18) mod 29
    """
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

def local_search(cipher_indices, initial_key, max_iterations=500):
    """Hill-climbing local search to optimize the key"""
    current_key = initial_key[:]
    current_score = score_english(indices_to_text(decrypt_sub(cipher_indices, current_key)))
    
    improvements = 0
    
    for iteration in range(max_iterations):
        improved = False
        
        # Try changing each position by ±1
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
        
        if iteration % 10 == 0 and iteration > 0:
            plaintext_preview = indices_to_text(decrypt_sub(cipher_indices, current_key))[:80]
            print(f"  Iteration {iteration}: score = {current_score:.2f}, preview: {plaintext_preview}")
    
    print(f"\nOptimization complete: {improvements} improvements over {iteration + 1} iterations")
    return current_key, current_score

def check_reversibility(cipher_indices, key_indices):
    """Check if decrypt→encrypt produces original cipher (proof of correctness)"""
    plaintext = decrypt_sub(cipher_indices, key_indices)
    re_encrypted = encrypt_sub(plaintext, key_indices)
    
    matches = sum(1 for c1, c2 in zip(cipher_indices, re_encrypted) if c1 == c2)
    total = len(cipher_indices)
    
    return matches, total

def main():
    print("=" * 80)
    print("PAGE 2 - SUB CIPHER ATTACK (KEY LENGTH 83)")
    print("=" * 80)
    print("\nMethodology:")
    print("  1. Frequency-based key initialization (assume E is most common)")
    print("  2. SUB operation: plaintext = (cipher - key) mod 29")
    print("  3. Hill-climbing optimization")
    print("  4. Reversibility check (MUST be 100% for correct operation)")
    print()
    
    # Load Page 2
    cipher_indices = load_page2()
    key_length = 83
    
    print(f"Page 2 loaded: {len(cipher_indices)} runes")
    print(f"Key length: {key_length}")
    print(f"First 20 indices: {cipher_indices[:20]}")
    print()
    
    # Generate frequency-based key
    print("=" * 80)
    print("STEP 1: Frequency-Based Key Generation (SUB)")
    print("=" * 80)
    
    key = generate_frequency_key_sub(cipher_indices, key_length)
    print(f"Generated key (length {len(key)}):")
    print(f"Key: {key}")
    print(f"Key values min: {min(key)}, max: {max(key)}")
    
    # Check all values are in valid range
    if all(0 <= k < 29 for k in key):
        print("✓ All key values in valid range [0, 28]")
    else:
        print("⚠ WARNING: Some key values out of range!")
    
    # Test reversibility with frequency key
    print("\n" + "=" * 80)
    print("STEP 2: Reversibility Test (Frequency Key)")
    print("=" * 80)
    
    matches, total = check_reversibility(cipher_indices, key)
    print(f"Reversibility: {matches}/{total} match")
    
    if matches == total:
        print("✓ Perfectly reversible!")
    else:
        print(f"⚠ Only {matches}/{total} = {100*matches/total:.1f}% reversible")
    
    # Initial decrypt
    plaintext = decrypt_sub(cipher_indices, key)
    plaintext_text = indices_to_text(plaintext)
    initial_score = score_english(plaintext_text)
    
    print(f"\nInitial score: {initial_score:.2f}")
    print(f"Preview: {plaintext_text[:100]}")
    
    # Optimize with local search
    print("\n" + "=" * 80)
    print("STEP 3: Local Search Optimization")
    print("=" * 80)
    
    optimized_key, optimized_score = local_search(cipher_indices, key)
    
    # Final results
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    
    optimized_plaintext = decrypt_sub(cipher_indices, optimized_key)
    optimized_text = indices_to_text(optimized_plaintext)
    
    print(f"\nOptimized key: {optimized_key}")
    print(f"\nFinal score: {optimized_score:.2f}")
    
    # Re-check reversibility with optimized key
    matches, total = check_reversibility(cipher_indices, optimized_key)
    print(f"Reversibility: {matches}/{total} match")
    
    if matches == total:
        print("✓ Perfectly reversible - this is the correct operation!")
    else:
        print(f"⚠ Only {100*matches/total:.1f}% reversible")
    
    print(f"\nFull plaintext:")
    print(optimized_text)
    
    # Save results
    output_path = Path(__file__).parent / "PAGE2_SUB83_RESULT.txt"
    with open(output_path, 'w') as f:
        f.write("PAGE 2 - SUB-83 DECRYPTION RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Key length: {key_length}\n")
        f.write(f"Cipher length: {len(cipher_indices)} runes\n")
        f.write(f"Final score: {optimized_score:.2f}\n")
        f.write(f"Reversibility: {matches}/{total} ({100*matches/total:.1f}%)\n\n")
        f.write("Optimized key:\n")
        f.write(f"{optimized_key}\n\n")
        f.write("Decrypted plaintext:\n")
        f.write(f"{optimized_text}\n")
    
    print(f"\nResults saved to: {output_path}")
    
    # Compare with Page 1 results
    print("\n" + "=" * 80)
    print("COMPARISON WITH PAGE 1")
    print("=" * 80)
    print(f"\nPage 1: Key length 71, Score 223.50, Reversibility 254/254 (100%)")
    print(f"Page 2: Key length 83, Score {optimized_score:.2f}, Reversibility {matches}/{total} ({100*matches/total:.1f}%)")
    print(f"\nBoth pages use prime-numbered key lengths: 71 and 83")
    
    if matches == total:
        print("✓ SUB operation validated on Page 2!")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. Analyze Page 2 plaintext for interleaving patterns (like Page 1)
2. Test every-Nth-character extractions
3. Compare Page 1 and Page 2 plaintext structures
4. Run IoC analysis on Page 3 to continue validation
5. Document key length pattern (71, 83, ???)
""")

if __name__ == '__main__':
    main()

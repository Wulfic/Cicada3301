"""
Test SUB operation with key length 71 (should be properly reversible in mod 29).

XOR doesn't play nicely with mod 29, but SUB should work perfectly.
"""

import os
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page1():
    """Load Page 1."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_indices = [RUNE_TO_INDEX[c] for c in segments[0] if c in RUNE_TO_INDEX]
    return page1_indices

def get_frequency_key_sub(key_length=71):
    """Get frequency-based key for SUB operation."""
    cipher = load_page1()
    
    cosets = [[] for _ in range(key_length)]
    for i, c in enumerate(cipher):
        cosets[i % key_length].append(c)
    
    key = []
    target_idx = 18  # E - most common in English
    
    for coset in cosets:
        if not coset:
            key.append(0)
            continue
        
        freq = Counter(coset)
        most_common_idx = freq.most_common(1)[0][0]
        
        # For SUB: plaintext = (cipher - key) mod 29
        # So: key = (cipher - plaintext) mod 29
        # If most_common_cipher should decrypt to target_idx:
        key_val = (most_common_idx - target_idx) % 29
        key.append(key_val)
    
    return key

def decrypt_sub(cipher_indices, key_indices):
    """SUB decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def encrypt_sub(plaintext_indices, key_indices):
    """SUB encrypt (for testing reversibility)."""
    ciphertext = []
    for i, p in enumerate(plaintext_indices):
        k = key_indices[i % len(key_indices)]
        ciphertext.append((p + k) % 29)
    return ciphertext

def indices_to_text(indices):
    """Convert to text."""
    return "".join(LETTERS[i] for i in indices)

def score_text(text):
    """Enhanced English scoring."""
    text_upper = text.upper()
    
    high_value_words = {
        "THE": 10, "AND": 8, "THAT": 8, "WITH": 8, "FROM": 7,
        "THIS": 7, "WITHIN": 9, "DIVINE": 10, "EMERGE": 10, "INSTAR": 12,
        "CIRCUMFERENCE": 15, "TRUTH": 8, "WISDOM": 9, "OF": 5,
        "TO": 5, "IN": 5, "FOR": 5, "SEEK": 6, "FIND": 6, "SHALL": 7
    }
    
    score = 0.0
    import re
    for word, weight in high_value_words.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = len(re.findall(pattern, text_upper))
        score += matches * weight * 2
    
    for bg in ["TH", "HE", "IN", "ER", "AN", "OF", "RE", "ON", "AT", "EN"]:
        score += text_upper.count(bg) * 1.5
    
    return score

def local_search_sub(cipher_indices, initial_key, max_iterations=500):
    """Hill-climbing search."""
    best_key = initial_key.copy()
    best_score = score_text(indices_to_text(decrypt_sub(cipher_indices, best_key)))
    
    print(f"Starting score: {best_score:.2f}")
    
    improved = True
    iteration = 0
    improvements = []
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        for pos in range(len(best_key)):
            original_val = best_key[pos]
            
            for new_val in range(29):
                if new_val == original_val:
                    continue
                
                best_key[pos] = new_val
                plaintext = decrypt_sub(cipher_indices, best_key)
                score = score_text(indices_to_text(plaintext))
                
                if score > best_score:
                    best_score = score
                    improved = True
                    improvements.append((iteration, pos, score))
                    if len(improvements) % 10 == 0:
                        print(f"  Iter {iteration}: score {score:.2f}")
                    break
                else:
                    best_key[pos] = original_val
            
            if improved:
                break
    
    print(f"Total improvements: {len(improvements)}")
    return best_key, best_score

def main():
    print("="*80)
    print("Page 1 - SUB Operation with Key Length 71")
    print("="*80)
    
    cipher = load_page1()
    print(f"\nCipher length: {len(cipher)}")
    
    # Get frequency-based key for SUB
    freq_key = get_frequency_key_sub(71)
    print(f"\nFrequency-based key (SUB, length 71):")
    print(freq_key)
    
    # Test reversibility
    plaintext = decrypt_sub(cipher, freq_key)
    re_encrypted = encrypt_sub(plaintext, freq_key)
    
    mismatches = sum(1 for i in range(len(cipher)) if cipher[i] != re_encrypted[i])
    print(f"\nReversibility: {len(cipher) - mismatches}/{len(cipher)} match")
    
    if mismatches == 0:
        print("✓ Perfectly reversible!")
    else:
        print(f"⚠️ {mismatches} mismatches (should be 0 for SUB)")
    
    # Score initial result
    text = indices_to_text(plaintext)
    score = score_text(text)
    
    print(f"\nInitial score: {score:.2f}")
    print(f"Preview:\n{text[:300]}")
    
    # Optimize with local search
    print("\n" + "="*80)
    print("Optimizing with local search...")
    print("="*80)
    
    optimized_key, optimized_score = local_search_sub(cipher, freq_key, max_iterations=500)
    
    # Final result
    final_plaintext = decrypt_sub(cipher, optimized_key)
    final_text = indices_to_text(final_plaintext)
    
    # Verify reversibility of optimized key
    re_enc_opt = encrypt_sub(final_plaintext, optimized_key)
    opt_mismatches = sum(1 for i in range(len(cipher)) if cipher[i] != re_enc_opt[i])
    
    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    
    print(f"\nOptimized key (length {len(optimized_key)}):")
    print(optimized_key)
    
    print(f"\nFinal score: {optimized_score:.2f}")
    print(f"Reversibility: {len(cipher) - opt_mismatches}/{len(cipher)} match")
    
    if opt_mismatches == 0:
        print("✓ Perfectly reversible - this is the correct operation!")
    
    print(f"\nFull plaintext:")
    print(final_text)
    
    # Save
    output_path = "tools/PAGE1_SUB71_RESULT.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("Page 1 - SUB Operation with Key Length 71\n")
        f.write("="*80 + "\n\n")
        f.write(f"Operation: plaintext = (cipher - key) mod 29\n\n")
        f.write(f"Key (length 71):\n{optimized_key}\n\n")
        f.write(f"Score: {optimized_score:.2f}\n\n")
        f.write(f"Reversibility: {len(cipher) - opt_mismatches}/{len(cipher)} match\n\n")
        f.write(f"Full plaintext:\n{final_text}\n")
    
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()

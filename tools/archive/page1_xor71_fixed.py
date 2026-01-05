"""
The frequency-based key shows value 29, which is out of range for mod 29 (0-28).
This is the bug! Let's fix it and re-run.
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

def get_frequency_key_fixed():
    """Get frequency-based key with proper mod 29."""
    cipher = load_page1()
    key_length = 71
    
    cosets = [[] for _ in range(key_length)]
    for i, c in enumerate(cipher):
        cosets[i % key_length].append(c)
    
    key = []
    target_idx = 18  # E
    for coset in cosets:
        if not coset:
            key.append(0)
            continue
        freq = Counter(coset)
        most_common_idx = freq.most_common(1)[0][0]
        key_val = (most_common_idx ^ target_idx) % 29  # FIX: Ensure mod 29
        key.append(key_val)
    
    return key

def decrypt_xor(cipher_indices, key_indices):
    """XOR decrypt with proper bounds checking."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)] % 29  # Ensure key is in range
        result = (c ^ k) % 29
        plaintext.append(result)
    return plaintext

def indices_to_text(indices):
    """Convert to text."""
    return "".join(LETTERS[i % 29] for i in indices)  # Ensure indices are in range

def score_text(text):
    """Enhanced English scoring."""
    text_upper = text.upper()
    
    high_value_words = {
        "THE": 10, "AND": 8, "THAT": 8, "WITH": 8, "FROM": 7,
        "THIS": 7, "HAVE": 7, "WHICH": 8, "THEIR": 7, "WOULD": 7,
        "WITHIN": 9, "DIVINE": 10, "EMERGE": 10, "INSTAR": 12,
        "CIRCUMFERENCE": 15, "TRUTH": 8, "WISDOM": 9, "OF": 5,
        "TO": 5, "IN": 5, "FOR": 5, "GOLD": 8, "SEEK": 6, "FIND": 6
    }
    
    score = 0.0
    import re
    for word, weight in high_value_words.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = len(re.findall(pattern, text_upper))
        score += matches * weight * 2
    
    for bg in ["TH", "HE", "IN", "ER", "AN", "OF"]:
        score += text_upper.count(bg) * 1.5
    
    return score

def local_search(cipher_indices, initial_key, max_iterations=300):
    """Hill-climbing search to optimize key."""
    best_key = [k % 29 for k in initial_key]  # Ensure all in range
    best_score = score_text(indices_to_text(decrypt_xor(cipher_indices, best_key)))
    
    improved = True
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        for pos in range(len(best_key)):
            original_val = best_key[pos]
            
            for new_val in range(29):
                if new_val == original_val:
                    continue
                
                best_key[pos] = new_val
                plaintext = decrypt_xor(cipher_indices, best_key)
                score = score_text(indices_to_text(plaintext))
                
                if score > best_score:
                    best_score = score
                    improved = True
                    print(f"  Iter {iteration}, pos {pos}: score improved to {score:.2f}")
                    break
                else:
                    best_key[pos] = original_val
            
            if improved:
                break
    
    return best_key, best_score

def main():
    print("="*80)
    print("Fixed XOR-71 Attack with Proper Mod 29")
    print("="*80)
    
    cipher = load_page1()
    print(f"\nCipher length: {len(cipher)}")
    
    # Get fixed frequency-based key
    freq_key = get_frequency_key_fixed()
    print(f"\nFrequency-based key (fixed):")
    print(freq_key)
    print(f"Key length: {len(freq_key)}")
    print(f"All values in range [0,28]: {all(0 <= k < 29 for k in freq_key)}")
    
    # Test reversibility
    plaintext = decrypt_xor(cipher, freq_key)
    re_encrypted = decrypt_xor(plaintext, freq_key)
    mismatches = sum(1 for i in range(len(cipher)) if cipher[i] != re_encrypted[i])
    
    print(f"\nReversibility test: {len(cipher) - mismatches}/{len(cipher)} match")
    
    if mismatches == 0:
        print("✓ Fully reversible!")
    else:
        print(f"⚠️ Still {mismatches} mismatches")
    
    # Score and display
    text = indices_to_text(plaintext)
    score = score_text(text)
    
    print(f"\nInitial score: {score:.2f}")
    print(f"Preview:\n{text[:300]}")
    
    # Optimize
    print("\n" + "="*80)
    print("Optimizing key with local search...")
    print("="*80)
    
    optimized_key, optimized_score = local_search(cipher, freq_key, max_iterations=500)
    
    final_plaintext = decrypt_xor(cipher, optimized_key)
    final_text = indices_to_text(final_plaintext)
    
    print(f"\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    
    print(f"\nOptimized key:")
    print(optimized_key)
    
    print(f"\nFinal score: {optimized_score:.2f}")
    print(f"\nFull text:")
    print(final_text)
    
    # Test reversibility of optimized key
    re_enc_opt = decrypt_xor(final_plaintext, optimized_key)
    opt_mismatches = sum(1 for i in range(len(cipher)) if cipher[i] != re_enc_opt[i])
    print(f"\nOptimized key reversibility: {len(cipher) - opt_mismatches}/{len(cipher)} match")
    
    # Save
    output_path = "tools/PAGE1_XOR71_FIXED.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("Page 1 - XOR-71 with Fixed Mod 29\n")
        f.write("="*80 + "\n\n")
        f.write(f"Key (length 71):\n{optimized_key}\n\n")
        f.write(f"Score: {optimized_score:.2f}\n\n")
        f.write(f"Reversibility: {len(cipher) - opt_mismatches}/{len(cipher)} match\n\n")
        f.write(f"Full plaintext:\n{final_text}\n")
    
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()

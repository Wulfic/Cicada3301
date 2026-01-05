"""
Focused attack on Page 1 using key length 71 (suggested by IoC analysis).

The frequency-based attack with length 71 XOR showed the most promising results.
This script does a more thorough search around that key.
"""

import os
from collections import Counter
import re

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page1():
    """Load Page 1 from transcription file."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_text = segments[0]
    page1_indices = [RUNE_TO_INDEX[c] for c in page1_text if c in RUNE_TO_INDEX]
    
    return page1_indices, page1_text

def decrypt_xor(cipher_indices, key_indices):
    """Decrypt with XOR."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c ^ k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert indices to readable text."""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """Score English-likeness."""
    text = text.upper()
    
    # Common words
    common_words = [
        "THE", "OF", "AND", "TO", "IN", "IS", "THAT", "IT", "FOR", "AS",
        "WITH", "WAS", "ON", "BE", "AT", "BY", "THIS", "FROM", "OR", "AN",
        "ARE", "WHICH", "ONE", "ALL", "THEIR", "THERE", "WHEN", "WHAT",
        "LIKE", "HAS", "HAD", "BUT", "NOT", "THEM", "THAN", "INTO", "OUT",
        "WITHIN", "DIVINE", "EMERGE", "INSTAR", "CIRCUMFERENCE", "TRUTH",
        "WISDOM", "KNOWLEDGE", "SEEK", "FIND", "SHALL", "WILL", "MUST"
    ]
    
    score = 0.0
    for word in common_words:
        count = text.count(word)
        score += count * len(word)
    
    # Common bigrams
    common_bigrams = {
        "TH": 3.5, "HE": 3.0, "IN": 2.5, "ER": 2.5, "AN": 2.5,
        "RE": 2.0, "ON": 2.0, "AT": 2.0, "EN": 2.0, "ND": 2.0,
        "TI": 1.5, "ES": 1.5, "OR": 1.5, "TE": 1.5, "OF": 2.5,
        "ED": 1.5, "IS": 1.5, "IT": 1.5, "AL": 1.5, "AR": 1.5,
        "ST": 1.5, "TO": 1.5, "NT": 1.5, "NG": 1.5, "SE": 1.5
    }
    
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        score += common_bigrams.get(bigram, 0.0)
    
    # Penalize excessive repetition
    if text.count("E") > len(text) * 0.20:  # More than 20% E
        score *= 0.5
    
    return score

def get_frequency_based_key(cipher_indices, key_length, target_idx=18):
    """Get initial key using frequency analysis (assume 'E' is most common)."""
    cosets = [[] for _ in range(key_length)]
    for i, c in enumerate(cipher_indices):
        cosets[i % key_length].append(c)
    
    key = []
    for coset in cosets:
        if not coset:
            key.append(0)
            continue
        
        freq = Counter(coset)
        most_common_idx = freq.most_common(1)[0][0]
        key_val = most_common_idx ^ target_idx
        key.append(key_val)
    
    return key

def local_search(cipher_indices, initial_key, max_iterations=1000):
    """Hill-climbing local search to optimize the key."""
    best_key = initial_key.copy()
    best_score = score_english(indices_to_text(decrypt_xor(cipher_indices, best_key)))
    
    improved = True
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        # Try modifying each position
        for pos in range(len(best_key)):
            original_val = best_key[pos]
            
            # Try all 29 possible values
            for new_val in range(29):
                if new_val == original_val:
                    continue
                
                best_key[pos] = new_val
                plaintext = decrypt_xor(cipher_indices, best_key)
                score = score_english(indices_to_text(plaintext))
                
                if score > best_score:
                    best_score = score
                    improved = True
                    break  # Move to next position
                else:
                    best_key[pos] = original_val
            
            if improved:
                break  # Restart from beginning
    
    return best_key, best_score

def render_with_formatting(raw_text, plaintext_indices):
    """Render plaintext with original formatting."""
    out = []
    rune_pos = 0
    
    for ch in raw_text:
        if ch in RUNE_TO_INDEX:
            if rune_pos < len(plaintext_indices):
                out.append(LETTERS[plaintext_indices[rune_pos]])
                rune_pos += 1
        elif ch == '-':
            out.append(' ')
        elif ch == '/':
            out.append('\n')
        elif ch == '.':
            out.append('. ')
        elif ch in ('\n', ' '):
            out.append(ch)
    
    return ''.join(out)

def main():
    print("="*80)
    print("Page 1 Attack - Key Length 71 (XOR)")
    print("="*80)
    
    cipher_indices, raw_text = load_page1()
    print(f"\nPage 1 cipher length: {len(cipher_indices)} runes")
    
    # Get initial frequency-based key
    print("\n--- Step 1: Frequency-based initial key ---")
    initial_key = get_frequency_based_key(cipher_indices, 71)
    plaintext = decrypt_xor(cipher_indices, initial_key)
    initial_score = score_english(indices_to_text(plaintext))
    
    print(f"Initial score: {initial_score:.2f}")
    print(f"Preview: {indices_to_text(plaintext)[:150]}")
    
    # Local search optimization
    print("\n--- Step 2: Local search optimization ---")
    print("This may take a minute...")
    
    optimized_key, optimized_score = local_search(cipher_indices, initial_key, max_iterations=500)
    
    print(f"\nOptimized score: {optimized_score:.2f}")
    print(f"Improvement: {optimized_score - initial_score:.2f}")
    
    # Decrypt with optimized key
    final_plaintext_indices = decrypt_xor(cipher_indices, optimized_key)
    final_plaintext = indices_to_text(final_plaintext_indices)
    
    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    
    print(f"\nKey (length {len(optimized_key)}):")
    print(optimized_key)
    
    print(f"\nPlaintext (compact):")
    print(final_plaintext)
    
    print(f"\nPlaintext (formatted):")
    formatted = render_with_formatting(raw_text, final_plaintext_indices)
    print(formatted)
    
    # Save results
    output_path = "tools/PAGE1_KEY71_RESULTS.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("Page 1 - Key Length 71 XOR Attack\n")
        f.write("="*80 + "\n\n")
        f.write(f"Score: {optimized_score:.2f}\n\n")
        f.write(f"Key (length {len(optimized_key)}):\n")
        f.write(str(optimized_key) + "\n\n")
        f.write("Plaintext (compact):\n")
        f.write(final_plaintext + "\n\n")
        f.write("Plaintext (formatted):\n")
        f.write(formatted + "\n")
    
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()

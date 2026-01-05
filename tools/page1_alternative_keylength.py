"""
Test Page 1 with alternative key lengths suggested by IoC analysis.

IoC peaks at 93, 138, 150, 102, suggesting possible key lengths.
This script tests simple Vigenère-style decryption with these lengths.
"""

import os
from pathlib import Path
from collections import Counter
import math

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

def decrypt_with_key(cipher_indices, key_indices, op="SUB"):
    """Decrypt cipher with a key."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if op == "SUB":
            plaintext.append((c - k) % 29)
        elif op == "ADD":
            plaintext.append((c + k) % 29)
        elif op == "XOR":
            plaintext.append((c ^ k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert indices to readable text."""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """Simple English scoring based on common bigrams."""
    text = text.upper()
    
    # Common English bigrams
    common_bigrams = {
        "TH": 3.0, "HE": 2.5, "IN": 2.0, "ER": 2.0, "AN": 2.0,
        "RE": 1.8, "ON": 1.5, "AT": 1.5, "EN": 1.5, "ND": 1.5,
        "TI": 1.3, "ES": 1.3, "OR": 1.3, "TE": 1.3, "OF": 1.2,
        "ED": 1.2, "IS": 1.2, "IT": 1.2, "AL": 1.2, "AR": 1.2,
        "ST": 1.1, "TO": 1.1, "NT": 1.1, "NG": 1.1, "SE": 1.0
    }
    
    score = 0.0
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        score += common_bigrams.get(bigram, 0.0)
    
    # Penalize rare letters appearing too often
    rare_letters = "QZJX"
    for letter in rare_letters:
        if text.count(letter) > len(text) * 0.05:  # More than 5%
            score -= 5.0
    
    return score

def test_key_length(cipher_indices, key_length, op="SUB", top_n=5):
    """Test all possible keys of given length using frequency analysis."""
    print(f"\n{'='*80}")
    print(f"Testing key length {key_length} with op={op}")
    print(f"{'='*80}")
    
    # For each position in the key, try all 29 possible values
    # Start with the most likely key: frequency-based attack
    
    # Partition ciphertext by key position
    cosets = [[] for _ in range(key_length)]
    for i, c in enumerate(cipher_indices):
        cosets[i % key_length].append(c)
    
    # For each coset, find the key value that maximizes frequency correlation with English
    # Assume 'E' (index 18) is the most common letter in plaintext
    most_common_plaintext_idx = 18  # E
    
    key_candidates = []
    for pos in range(key_length):
        coset = cosets[pos]
        if not coset:
            key_candidates.append(0)
            continue
        
        # Find most common ciphertext symbol in this coset
        freq = Counter(coset)
        most_common_cipher_idx = freq.most_common(1)[0][0]
        
        # Key value that would decrypt most_common_cipher to 'E'
        if op == "SUB":
            key_val = (most_common_cipher_idx - most_common_plaintext_idx) % 29
        elif op == "ADD":
            key_val = (most_common_plaintext_idx - most_common_cipher_idx) % 29
        elif op == "XOR":
            key_val = most_common_cipher_idx ^ most_common_plaintext_idx
        
        key_candidates.append(key_val)
    
    # Decrypt with this frequency-based key
    plaintext_indices = decrypt_with_key(cipher_indices, key_candidates, op)
    plaintext = indices_to_text(plaintext_indices)
    score = score_english(plaintext)
    
    print(f"\nFrequency-based key attempt:")
    print(f"Key: {key_candidates[:20]}... (first 20 values)")
    print(f"Score: {score:.2f}")
    print(f"Preview: {plaintext[:100]}")
    
    # Also try a few random variations around this key
    print(f"\nTrying variations...")
    
    results = [(score, key_candidates, plaintext)]
    
    # Try shifting each key position by ±1
    for shift_pos in range(min(10, key_length)):  # Only try first 10 positions
        for delta in [-1, 1]:
            test_key = key_candidates.copy()
            test_key[shift_pos] = (test_key[shift_pos] + delta) % 29
            
            plaintext_indices = decrypt_with_key(cipher_indices, test_key, op)
            plaintext = indices_to_text(plaintext_indices)
            score = score_english(plaintext)
            
            results.append((score, test_key, plaintext))
    
    # Sort and show top results
    results.sort(reverse=True, key=lambda x: x[0])
    
    print(f"\nTop {top_n} results:")
    for i, (score, key, plaintext) in enumerate(results[:top_n]):
        print(f"\n--- Rank {i+1} (score={score:.2f}) ---")
        print(f"Key: {key[:20]}... (first 20)")
        print(f"Preview: {plaintext[:150]}")

def main():
    print("="*80)
    print("Alternative Key Length Testing for Page 1")
    print("="*80)
    
    cipher_indices, raw_text = load_page1()
    print(f"\nPage 1 cipher length: {len(cipher_indices)} runes")
    
    # Test the IoC-suggested key lengths
    interesting_lengths = [93, 138, 102, 150, 71]
    
    for length in interesting_lengths:
        if length > len(cipher_indices):
            print(f"\nSkipping length {length} (longer than cipher)")
            continue
        
        for op in ["SUB", "XOR"]:
            test_key_length(cipher_indices, length, op, top_n=3)
    
    print("\n" + "="*80)
    print("Analysis complete")
    print("="*80)

if __name__ == "__main__":
    main()

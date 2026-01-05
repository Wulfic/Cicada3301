"""
Analyze the XOR-71 output for patterns suggesting a secondary cipher layer.

The current output has excessive "TH" patterns. This script:
1. Checks if there's a simple substitution cipher remaining
2. Tests columnar transpositions
3. Looks for word-boundary issues in the token mapping
"""

# The optimized key from the previous run
OPTIMIZED_KEY_71 = [16, 4, 13, 27, 4, 15, 25, 27, 16, 8, 5, 10, 22, 0, 1, 6, 24, 9, 15, 10, 0, 0, 6, 3, 10, 22, 14, 5, 16, 3, 15, 20, 27, 1, 4, 24, 0, 20, 19, 21, 4, 21, 14, 14, 6, 0, 10, 17, 24, 17, 3, 8, 17, 16, 6, 2, 12, 25, 24, 13, 7, 18, 21, 15, 19, 10, 6, 10, 27, 3, 5]

import os
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# Alternative single-character mapping
SINGLE_CHAR_LETTERS = [
    "F", "U", "D", "O", "R", "C", "G", "W", "H", "N", "I", "J", "Q", "P", "X",
    "S", "T", "B", "E", "M", "L", "K", "V", "D", "A", "Z", "Y", "L", "A"
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

def decrypt_xor(cipher_indices, key_indices):
    """XOR decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c ^ k) % 29)
    return plaintext

def indices_to_single_chars(indices):
    """Convert to single characters."""
    return "".join(SINGLE_CHAR_LETTERS[i] for i in indices)

def try_substitution_cipher(text):
    """Try to detect if there's a simple substitution cipher remaining."""
    print("\n" + "="*80)
    print("Testing for Substitution Cipher")
    print("="*80)
    
    # Analyze bigram patterns
    bigrams = {}
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        bigrams[bg] = bigrams.get(bg, 0) + 1
    
    print("\nMost common bigrams:")
    sorted_bigrams = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)
    for bg, count in sorted_bigrams[:20]:
        print(f"  {bg}: {count}")
    
    # Letter frequency
    freq = Counter(text)
    print("\nLetter frequency:")
    for letter, count in freq.most_common(15):
        pct = count / len(text) * 100
        print(f"  {letter}: {count} ({pct:.1f}%)")
    
    # Expected English: E(12.7%), T(9.1%), A(8.2%), O(7.5%), I(7.0%), N(6.7%)
    # If we're getting TH=index2 appearing as our highest single "letter", that's wrong
    
    print("\nNote: 'TH' appearing as a single letter suggests we need to reconsider")
    print("the rune-to-letter mapping or apply a different decryption operation.")

def try_columnar_transpose(indices):
    """Try simple columnar transpositions."""
    print("\n" + "="*80)
    print("Testing Columnar Transpositions")
    print("="*80)
    
    test_widths = [2, 3, 5, 7, 11, 13, 127]  # Including primes and 127=254/2
    
    for width in test_widths:
        if len(indices) % width != 0 and len(indices) < width * 2:
            continue
        
        # Read by columns, write by rows
        rows = []
        for start in range(width):
            row = [indices[i] for i in range(start, len(indices), width)]
            rows.append(row)
        
        # Flatten
        transposed = []
        for row in rows:
            transposed.extend(row)
        
        text = "".join(LETTERS[i] for i in transposed)
        
        # Quick score
        score = text.count("THE") * 3 + text.count(" OF ") * 2 + text.count(" AND ") * 2
        
        if score > 5:
            print(f"\nWidth {width} (score={score}):")
            print(f"  {text[:120]}")

def main():
    print("="*80)
    print("Post-XOR-71 Analysis - Looking for Secondary Cipher Layer")
    print("="*80)
    
    cipher_indices = load_page1()
    plaintext_indices = decrypt_xor(cipher_indices, OPTIMIZED_KEY_71)
    
    # Convert using standard token mapping
    text_standard = "".join(LETTERS[i] for i in plaintext_indices)
    
    print(f"\nDecrypted length: {len(plaintext_indices)} symbols")
    print(f"\nUsing standard rune token mapping:")
    print(text_standard[:200])
    
    # Analyze
    try_substitution_cipher(text_standard)
    
    # Try with single-char mapping
    text_single = indices_to_single_chars(plaintext_indices)
    print("\n" + "="*80)
    print("Using alternative single-character mapping:")
    print("="*80)
    print(text_single[:200])
    
    # Try transpositions
    try_columnar_transpose(plaintext_indices)
    
    # Check if reversing helps
    print("\n" + "="*80)
    print("Trying reversed text:")
    print("="*80)
    reversed_indices = list(reversed(plaintext_indices))
    reversed_text = "".join(LETTERS[i] for i in reversed_indices)
    print(reversed_text[:200])

if __name__ == "__main__":
    main()

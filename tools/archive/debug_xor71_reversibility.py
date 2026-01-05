"""
Debug the XOR-71 reversibility issue.

The XOR operation should be perfectly reversible, so 222/254 matches
suggests either:
1. The key optimization changed some positions incorrectly
2. There's a bug in the implementation
3. The cipher length doesn't evenly divide by key length
"""

import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# Original frequency-based key (before optimization)
def get_frequency_key():
    """Reconstruct the original frequency-based key."""
    from collections import Counter
    
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
        key_val = most_common_idx ^ target_idx
        key.append(key_val)
    
    return key

OPTIMIZED_KEY_71 = [16, 4, 13, 27, 4, 15, 25, 27, 16, 8, 5, 10, 22, 0, 1, 6, 24, 9, 15, 10, 0, 0, 6, 3, 10, 22, 14, 5, 16, 3, 15, 20, 27, 1, 4, 24, 0, 20, 19, 21, 4, 21, 14, 14, 6, 0, 10, 17, 24, 17, 3, 8, 17, 16, 6, 2, 12, 25, 24, 13, 7, 18, 21, 15, 19, 10, 6, 10, 27, 3, 5]

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

def indices_to_text(indices):
    """Convert to text."""
    return "".join(LETTERS[i] for i in indices)

def main():
    print("="*80)
    print("Debugging XOR-71 Reversibility")
    print("="*80)
    
    cipher = load_page1()
    print(f"\nCipher length: {len(cipher)}")
    print(f"Key length: {len(OPTIMIZED_KEY_71)}")
    print(f"Cipher mod key: {len(cipher) % len(OPTIMIZED_KEY_71)}")
    
    # Decrypt
    plaintext = decrypt_xor(cipher, OPTIMIZED_KEY_71)
    
    # Re-encrypt
    re_encrypted = decrypt_xor(plaintext, OPTIMIZED_KEY_71)  # XOR is its own inverse
    
    # Find mismatches
    mismatches = []
    for i in range(len(cipher)):
        if cipher[i] != re_encrypted[i]:
            mismatches.append({
                'pos': i,
                'original': cipher[i],
                're_encrypted': re_encrypted[i],
                'plaintext': plaintext[i],
                'key': OPTIMIZED_KEY_71[i % len(OPTIMIZED_KEY_71)],
                'key_pos': i % len(OPTIMIZED_KEY_71)
            })
    
    print(f"\nTotal mismatches: {len(mismatches)}/{len(cipher)}")
    print(f"Match rate: {(len(cipher) - len(mismatches)) / len(cipher) * 100:.1f}%")
    
    if mismatches:
        print(f"\nFirst 20 mismatches:")
        print(f"{'Pos':<6} {'Orig':<6} {'ReEnc':<6} {'Plain':<6} {'Key':<6} {'KeyPos':<6}")
        print("-"*60)
        
        for m in mismatches[:20]:
            print(f"{m['pos']:<6} {m['original']:<6} {m['re_encrypted']:<6} {m['plaintext']:<6} {m['key']:<6} {m['key_pos']:<6}")
        
        # Check if mismatches cluster
        mismatch_positions = [m['pos'] for m in mismatches]
        mismatch_key_positions = [m['key_pos'] for m in mismatches]
        
        print(f"\nMismatch position distribution:")
        print(f"First 30 positions: {mismatch_positions[:30]}")
        
        from collections import Counter
        key_pos_freq = Counter(mismatch_key_positions)
        print(f"\nMost common key positions with mismatches:")
        for kp, count in key_pos_freq.most_common(10):
            print(f"  Key position {kp}: {count} mismatches")
    
    # Test with original frequency-based key (before optimization)
    print("\n" + "="*80)
    print("Testing with original frequency-based key (pre-optimization)")
    print("="*80)
    
    freq_key = get_frequency_key()
    print(f"Frequency key: {freq_key[:20]}...")
    
    plaintext_freq = decrypt_xor(cipher, freq_key)
    re_encrypted_freq = decrypt_xor(plaintext_freq, freq_key)
    
    freq_mismatches = sum(1 for i in range(len(cipher)) if cipher[i] != re_encrypted_freq[i])
    print(f"Mismatches with frequency key: {freq_mismatches}/{len(cipher)}")
    print(f"Match rate: {(len(cipher) - freq_mismatches) / len(cipher) * 100:.1f}%")
    
    if freq_mismatches == 0:
        print("✓ Frequency key is fully reversible")
        print("\nThe optimization process introduced errors!")
        print("Recommendation: Use frequency-based key instead of optimized key")
    
    # Compare texts
    print("\n" + "="*80)
    print("Text Comparison")
    print("="*80)
    
    text_opt = indices_to_text(plaintext)
    text_freq = indices_to_text(plaintext_freq)
    
    print(f"\nOptimized key output:")
    print(text_opt[:200])
    
    print(f"\nFrequency key output:")
    print(text_freq[:200])
    
    # Character-by-character comparison
    diff_count = sum(1 for i in range(min(len(text_opt), len(text_freq))) if text_opt[i] != text_freq[i])
    print(f"\nText differences: {diff_count} characters")

if __name__ == "__main__":
    main()

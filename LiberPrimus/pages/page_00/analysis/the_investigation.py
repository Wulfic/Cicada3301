#!/usr/bin/env python3
"""
Investigate the THE pattern in our first-layer output.

Key question: Is THE a word, or is it an artifact of the cipher?

In Gematria Primus:
T = 16
H = 8
E = 18

Hypothesis: The key might produce these values frequently due to some pattern.
"""

# Page 0 discovered key (113 positions)
PAGE0_KEY = [
    1, 16, 5, 10, 11, 22, 27, 7, 21, 13, 4, 28, 2, 18, 1, 15, 
    22, 10, 24, 3, 26, 25, 9, 11, 6, 16, 24, 22, 19, 12, 6, 27, 
    0, 12, 1, 12, 27, 4, 28, 3, 25, 23, 8, 15, 1, 25, 14, 11, 
    3, 14, 16, 22, 0, 9, 1, 17, 5, 11, 17, 2, 18, 26, 20, 18, 
    3, 11, 0, 18, 11, 25, 2, 17, 9, 6, 10, 28, 24, 0, 12, 6, 
    9, 4, 21, 7, 24, 11, 1, 26, 14, 3, 22, 5, 6, 28, 14, 5, 
    8, 23, 14, 26, 27, 17, 10, 2, 23, 5, 27, 0, 8, 27, 16, 18, 4
]

IDX_TO_LETTER = ['F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
                 'A', 'AE', 'Y', 'IA', 'EA']

def analyze_key_patterns():
    """Analyze patterns in the discovered key."""
    print("KEY PATTERN ANALYSIS")
    print("=" * 70)
    
    print(f"\nKey length: {len(PAGE0_KEY)}")
    print(f"Key values: {PAGE0_KEY}")
    
    # Count frequency of each value in key
    from collections import Counter
    key_freq = Counter(PAGE0_KEY)
    
    print("\nKey value frequency:")
    for val, count in sorted(key_freq.items(), key=lambda x: -x[1]):
        letter = IDX_TO_LETTER[val]
        print(f"  {val} ({letter}): {count}x")
    
    # Check consecutive patterns
    print("\nConsecutive patterns in key:")
    for i in range(len(PAGE0_KEY) - 2):
        triplet = PAGE0_KEY[i:i+3]
        print(f"  Position {i}: {triplet} -> {[IDX_TO_LETTER[v] for v in triplet]}")
        if i > 15:
            print("  ...")
            break
    
    # Check if key values that produce T, H, E are frequent
    print("\n" + "=" * 70)
    print("VALUES THAT PRODUCE T, H, E")
    print("=" * 70)
    
    # If plaintext[i] = (cipher[i] - key[i]) mod 29
    # Then to get T=16, H=8, E=18:
    # For THE to appear, we need:
    #   cipher[i] - key[i] ≡ 16 (mod 29)
    #   cipher[i+1] - key[i+1] ≡ 8 (mod 29)
    #   cipher[i+2] - key[i+2] ≡ 18 (mod 29)
    
    print("Note: THE appearing means cipher - key ≡ 16, 8, 18 at consecutive positions")
    print("This could happen if:")
    print("  1. The plaintext actually contains THE (intentional)")
    print("  2. The cipher/key combination happens to produce T-H-E frequently")
    
    # Let's check what differences would produce THE
    print("\nKey values and what cipher values would produce THE:")
    for i in range(min(20, len(PAGE0_KEY))):
        k = PAGE0_KEY[i]
        # To get T=16: cipher = (16 + k) mod 29
        # To get H=8: cipher = (8 + k) mod 29
        # To get E=18: cipher = (18 + k) mod 29
        cipher_for_t = (16 + k) % 29
        cipher_for_h = (8 + k) % 29
        cipher_for_e = (18 + k) % 29
        print(f"  Pos {i}: key={k}, for T need cipher={cipher_for_t}, for H need {cipher_for_h}, for E need {cipher_for_e}")

def check_raw_cipher_for_the():
    """Check if THE pattern exists in raw cipher."""
    print("\n" + "=" * 70)
    print("THE PATTERN IN RAW CIPHER")
    print("=" * 70)
    
    # Load raw cipher from file
    try:
        with open(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        RUNE_TO_IDX = {
            'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
            'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
            'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
            'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
        }
        
        cipher_indices = []
        for char in content:
            if char in RUNE_TO_IDX:
                cipher_indices.append(RUNE_TO_IDX[char])
        
        print(f"Cipher length: {len(cipher_indices)}")
        
        # Convert cipher to letters
        cipher_text = ''.join(IDX_TO_LETTER[i] for i in cipher_indices)
        
        # Count THE in cipher
        the_count = cipher_text.count('THE')
        print(f"THE occurrences in raw cipher text: {the_count}")
        
        # Count in first 100 chars
        print(f"First 80 chars of cipher as text: {cipher_text[:80]}")
        
    except Exception as e:
        print(f"Error: {e}")

def verify_decryption():
    """Verify our decryption by checking a few positions."""
    print("\n" + "=" * 70)
    print("VERIFICATION OF DECRYPTION")
    print("=" * 70)
    
    # Expected first layer output
    FIRST_LAYER = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC"
    
    # Load cipher
    try:
        with open(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        RUNE_TO_IDX = {
            'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
            'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
            'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
            'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
        }
        
        cipher_indices = []
        for char in content:
            if char in RUNE_TO_IDX:
                cipher_indices.append(RUNE_TO_IDX[char])
        
        # Decrypt first 30 positions
        print("\nFirst 30 positions:")
        for i in range(30):
            c = cipher_indices[i]
            k = PAGE0_KEY[i % len(PAGE0_KEY)]
            p = (c - k) % 29
            print(f"  {i}: cipher={c}({IDX_TO_LETTER[c]}) - key={k}({IDX_TO_LETTER[k]}) = {p}({IDX_TO_LETTER[p]})")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    analyze_key_patterns()
    check_raw_cipher_for_the()
    verify_decryption()
    
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
If THE appears heavily in our output but NOT in the raw cipher:
  - The key is producing THE patterns (suspicious)
  - Our key discovery algorithm may be biased toward THE
  
If THE also appears in raw cipher:
  - THE might be intentional in the plaintext
  - The cipher preserves some THE structure
    """)

if __name__ == "__main__":
    main()


import os

# Rune Map
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
IDX_TO_RUNE = {v: k for k, v in RUNE_MAP.items()}

# Words
# Word 14: D-W-H-B-NG-F-A-C-J-U
CIPHER_14_STR = "ᛞᚹᚻᛒᛝᚠᚪᚳᛄᚢ"
# DECRYPTION (English -> Rune Indices)
# D=23, E=18, C=5, R=4, Y=26, P=13, t=16, I=10, O=3, N=9
PLAIN_14_IDXS = [23, 18, 5, 4, 26, 13, 16, 10, 3, 9]

# Word 60: EA-E-I-G-X-G-S
CIPHER_60_STR = "ᛠᛖᛁᚷᛉᚷᛋ"
# WARNING
# W=7, A=24, R=4, N=9, I=10, N=9, G=6
PLAIN_60_IDXS = [7, 24, 4, 9, 10, 9, 6]

def to_idxs(s):
    return [RUNE_MAP[c] for c in s if c in RUNE_MAP]

def idxs_to_runes(idxs):
    return "".join([IDX_TO_RUNE[i % 29] for i in idxs])

def analyze():
    c14 = to_idxs(CIPHER_14_STR)
    c60 = to_idxs(CIPHER_60_STR)
    
    modes = [
        ("Vigenere (P=C-K => K=C-P)", lambda c, p: (c - p) % 29),
        ("Variant (P=C+K => K=P-C)", lambda c, p: (p - c) % 29),
        ("Beaufort (P=K-C => K=P+C)", lambda c, p: (p + c) % 29)
    ]
    
    print(f"Word 14 (DECRYPTION): C={c14}, P={PLAIN_14_IDXS}")
    print(f"Word 60 (WARNING):    C={c60}, P={PLAIN_60_IDXS}")
    print("-" * 40)
    
    for name, func in modes:
        print(f"--- {name} ---")
        k14 = [func(c, p) for c, p in zip(c14, PLAIN_14_IDXS)]
        k60 = [func(c, p) for c, p in zip(c60, PLAIN_60_IDXS)]
        
        print(f"Key 14: {k14}")
        print(f"        {idxs_to_runes(k14)}")
        print(f"Key 60: {k60}")
        print(f"        {idxs_to_runes(k60)}")
        print()

if __name__ == "__main__":
    analyze()

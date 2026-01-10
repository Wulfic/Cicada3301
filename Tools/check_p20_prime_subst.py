
import os
import random

# Rune Map
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def to_runes(text):
    text = text.upper()
    res = []
    i = 0
    while i < len(text):
        found = False
        if i+1 < len(text):
            pair = text[i:i+2]
            if pair in LATIN_TABLE:
                res.append(LATIN_TABLE.index(pair))
                i += 2
                found = True
        if not found and i < len(text):
            char = text[i]
            if char in LATIN_TABLE:
                res.append(LATIN_TABLE.index(char))
            i += 1
    return res

def to_letters(values):
    return "".join([LATIN_TABLE[v] for v in values])

def solve_substitution(cipher_vals):
    # Genetic algorithm or similar?
    # Simple frequentist swap?
    # Known: E, T, A, O, I, N, S, H, R, D...
    # Cipher Freq: J, P, W, O, I (from previous analysis)
    
    # Let's map Top Cipher -> Top English
    # Cipher:   J(11), P(13), W(7), O(3), I(10)
    # English:  E(18), T(16), A(24), O(3), I(10) (approx)
    
    # Try 1: Map J->E, P->T, W->A, O->O, I->I
    # Map others randomly?
    pass

def atbash(vals):
    # Cyclic Atbash? 28-x?
    return [28 - v for v in vals]

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "Analysis", "Outputs", "p20_prime_stream_candidate.txt") # This has NGWJG... (unshifted)
    
    # Wait, the file I just wrote "p20_prime_decrypted.txt" has YEOT... (Shifted)
    path_shifted = os.path.join(repo, "Analysis", "Outputs", "p20_prime_decrypted.txt")
    with open(path_shifted, "r") as f:
        text = f.read().strip()
    
    vals = to_runes(text)
    
    print(f"Loaded {len(vals)} runes: {text[:50]}")
    
    # 1. Atbash
    atb = atbash(vals)
    print(f"Atbash: {to_letters(atb)[:60]}")
    
    # 2. Reverse
    rev = vals[::-1]
    print(f"Reverse: {to_letters(rev)[:60]}")
    
    # 3. Check for 'KEY'
    # K=C(5). E=18. Y=26.
    # Check for 5, 18, 26
    # Or 'CEN' (5, 18, 9)
    seq = [5, 18, 26]
    for i in range(len(vals)-2):
        if vals[i:i+3] == seq:
            print(f"HEAD FOUND KEY at index {i}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
PAGE 55 DEBUG - Step through each position
"""

from pathlib import Path

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {l: i for i, l in enumerate(LETTERS)}

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
          223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
          293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461]

def phi(n):
    return n - 1 if n >= 2 else 0

def text_to_indices(text):
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[two])
                i += 2
                continue
        one = text[i]
        if one in LETTER_TO_IDX:
            result.append(LETTER_TO_IDX[one])
        i += 1
    return result

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("PAGE 55 DEBUG - Position by position with F-skip")
    print("=" * 80)
    
    rune_text = load_page(55)
    cipher = [(RUNE_MAP[c], c) for c in rune_text if c in RUNE_MAP]
    
    # Expected: with F's correctly placed
    # AN END WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO IT IS THE DUTY OF EUERY PILGRIM TO SEEC OUT THIS PAGE
    # Positions of F: in "OF" (the word "OF" has F at second position)
    
    expected_words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
                     "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
                     "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", 
                     "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    for word in expected_words:
        expected.extend(text_to_indices(word))
    
    print(f"Expected length: {len(expected)}")
    print(f"Cipher length: {len(cipher)}")
    
    # Find F positions in expected
    f_positions_expected = [i for i, idx in enumerate(expected) if idx == 0]  # F is index 0
    print(f"F positions in expected: {f_positions_expected}")
    
    # Find F runes in cipher
    f_positions_cipher = [i for i, (idx, rune) in enumerate(cipher) if rune == 'ᚠ']
    print(f"F rune positions in cipher: {f_positions_cipher}")
    
    # The issue: Are the F positions aligned?
    print("\n--- Testing hypothesis: F runes at different positions ---")
    
    # Let's check: if F runes are at positions 35, 47, 51, 56, 74
    # And expected F's are at certain positions
    # What offset would make them align?
    
    # Actually let me think differently.
    # The formula works perfectly for positions 0-45 (first 46 chars).
    # Position 35 has an F rune. But position 35 in expected is 'A' (part of THAT).
    # 
    # Wait, let me check position 35 in expected:
    print("\n--- Position 35 analysis ---")
    print(f"Expected at 35: {expected[35]} = {LETTERS[expected[35]]}")
    print(f"Cipher at 35: {cipher[35]}")
    
    # And the decryption at position 35 with φ(prime[35]):
    c35 = cipher[35][0]
    k35 = phi(PRIMES[35]) % 29
    p35 = (c35 - k35) % 29
    print(f"Decryption: cipher={c35}, key={k35} (φ({PRIMES[35]})%29), plain={p35} = {LETTERS[p35]}")
    print(f"This matches expected? {p35 == expected[35]}")
    
    # Yes! Position 35 decrypts correctly to A (part of "THAT")
    # The F rune at position 35 decrypts to A, not F!
    
    # So the F-skip theory is WRONG for this page.
    
    print("\n--- The problem is elsewhere ---")
    print("Position 35 has F rune but decrypts to A correctly!")
    print("The F-skip theory doesn't apply here.")
    
    # Let's check what goes wrong at position 46
    print("\n--- Position 46 analysis ---")
    c46, rune46 = cipher[46]
    k46_formula = phi(PRIMES[46]) % 29
    p46_got = (c46 - k46_formula) % 29
    print(f"Cipher at 46: {c46} ({rune46})")
    print(f"Key from formula φ(prime[46])%29: {k46_formula}")
    print(f"Decrypted: {p46_got} = {LETTERS[p46_got]}")
    print(f"Expected: {expected[46]} = {LETTERS[expected[46]]}")
    
    # Calculate what key we NEED
    k46_needed = (c46 - expected[46]) % 29
    print(f"Key needed: {k46_needed}")
    
    # What prime would give this key?
    # φ(p) % 29 = k46_needed means (p-1) % 29 = k46_needed, so p = k46_needed + 1 + 29n
    print(f"Looking for prime where φ(p)%29 = {k46_needed}...")
    for i, p in enumerate(PRIMES[:100]):
        if phi(p) % 29 == k46_needed:
            print(f"  prime[{i}] = {p}: φ({p})%29 = {phi(p) % 29}")
            if i < 10:
                break

if __name__ == '__main__':
    main()

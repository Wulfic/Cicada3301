#!/usr/bin/env python3
"""
PAGE 55 KEY ANALYSIS - Find correct key for second half

Positions 0-45 work with φ(prime[i]) mod 29
Position 46+ needs a different key pattern
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
    print("PAGE 55 KEY RECOVERY")
    print("=" * 70)
    
    rune_text = load_page(55)
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    # Expected plaintext
    words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
             "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
             "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    for word in words:
        expected.extend(text_to_indices(word))
    
    print(f"Cipher: {len(cipher)} runes")
    print(f"Expected: {len(expected)} indices")
    
    # Calculate required keys for positions 46+
    print("\n--- Required keys for second half (pos 46-84) ---")
    required_keys = []
    for i in range(46, len(cipher)):
        c = cipher[i]
        p = expected[i]
        k = (c - p) % 29
        required_keys.append(k)
        print(f"Pos {i}: cipher={c}, expected={p} ({LETTERS[p]}), key={k}")
    
    print(f"\nRequired key sequence: {required_keys}")
    
    # Check if it's phi(primes) but starting from a different index
    print("\n--- Testing prime shifts ---")
    for start in range(100):
        test_keys = [(PRIMES[(start + i) % len(PRIMES)] - 1) % 29 for i in range(len(required_keys))]
        if test_keys == required_keys:
            print(f"✓ MATCH: Starts at prime index {start} (prime = {PRIMES[start]})")
            break
    else:
        print("No simple prime shift found")
    
    # Check if the key resets at some point
    print("\n--- Testing key reset at position 46 ---")
    # What if key restarts at prime[0]?
    test_keys_reset0 = [(PRIMES[i % len(PRIMES)] - 1) % 29 for i in range(len(required_keys))]
    if test_keys_reset0 == required_keys:
        print("✓ Key resets to prime[0] at position 46!")
    else:
        print("Key reset to 0 doesn't match")
        print(f"Required: {required_keys[:10]}")
        print(f"Reset 0:  {test_keys_reset0[:10]}")
    
    # Try VIGENERE with a keyword
    print("\n--- Testing keyword Vigenère ---")
    keywords = ["DIVINITY", "PILGRIM", "INSTAR", "CICADA", "CIRCUMFERENCE", "PARABLE", "PAGE", "DUTY", "EUERY"]
    
    for keyword in keywords:
        key_indices = text_to_indices(keyword)
        test_keys = [key_indices[i % len(key_indices)] for i in range(len(required_keys))]
        
        matches = sum(1 for a, b in zip(required_keys, test_keys) if a == b)
        if matches > 5:
            print(f"  '{keyword}': {matches}/{len(required_keys)} matches")
    
    # Try autokey with various seeds
    print("\n--- Testing autokey ---")
    for seed_word in ["AN", "END", "IT", "IS", "THE", "DUTY"]:
        seed = text_to_indices(seed_word)
        # Autokey: key[i] = plaintext[i-k] where k is seed length
        # For positions 46+, key comes from earlier plaintext
        
        # Key at position 46 = plaintext at position 46 - len(seed)
        # Actually let's derive what the key should be from the crib
        
        pass  # Autokey is complex, skip for now
    
    # Check if it's a simple offset
    print("\n--- Checking for patterns in required keys ---")
    diffs = [required_keys[i+1] - required_keys[i] for i in range(len(required_keys)-1)]
    print(f"Differences between consecutive keys: {diffs[:15]}")
    
    # Check against phi(prime) starting at position 46
    phi_at_46 = [(PRIMES[(46 + i) % len(PRIMES)] - 1) % 29 for i in range(len(required_keys))]
    print(f"\nφ(prime) continuing from pos 46: {phi_at_46[:10]}")
    print(f"Required keys:                    {required_keys[:10]}")
    
    # Calculate offset
    offsets = [(r - p) % 29 for r, p in zip(required_keys, phi_at_46)]
    print(f"Offsets needed: {offsets[:15]}")
    
    if len(set(offsets)) == 1:
        print(f"Constant offset: {offsets[0]}")

if __name__ == '__main__':
    main()

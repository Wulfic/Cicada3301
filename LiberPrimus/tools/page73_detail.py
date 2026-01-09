#!/usr/bin/env python3
"""
PAGE 73 DETAILED ANALYSIS

Page 73 has the same "AN END" message as Page 55.
Let's verify character by character using φ(prime) + literal F method.
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
    with open(page_dir / "runes.txt", 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("PAGE 73 DETAILED ANALYSIS")
    print("=" * 80)
    
    rune_text = load_page(73)
    
    # Remove the note line
    lines = rune_text.split('\n')
    clean_lines = [l for l in lines if not l.startswith('Note:')]
    rune_text_clean = '\n'.join(clean_lines)
    
    cipher = [RUNE_MAP[c] for c in rune_text_clean if c in RUNE_MAP]
    
    print(f"Cipher length: {len(cipher)}")
    
    # Expected plaintext
    expected_words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
                     "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
                     "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", 
                     "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    word_boundaries = []
    for word in expected_words:
        word_boundaries.append((len(expected), len(expected) + len(text_to_indices(word)), word))
        expected.extend(text_to_indices(word))
    
    print(f"Expected length: {len(expected)}")
    
    # Show word boundaries
    print("\n--- WORD BOUNDARIES ---")
    for start, end, word in word_boundaries:
        print(f"  {start:3d}-{end-1:3d}: {word}")
    
    # Find F positions
    f_cipher = [i for i, c in enumerate(cipher) if c == 0]
    f_expected = [i for i, c in enumerate(expected) if c == 0]
    
    print(f"\nF rune positions in cipher: {f_cipher}")
    print(f"F positions in expected: {f_expected}")
    
    # Position-by-position analysis
    print("\n--- POSITION-BY-POSITION ANALYSIS ---")
    print("Testing standard φ(prime) decryption:")
    
    errors = []
    prime_idx = 0
    
    for i in range(len(cipher)):
        c = cipher[i]
        k = phi(PRIMES[prime_idx]) % 29
        p = (c - k) % 29
        
        if i < len(expected):
            exp = expected[i]
            status = "✓" if p == exp else "✗"
            if p != exp:
                # Find what word this is in
                word = "?"
                for start, end, w in word_boundaries:
                    if start <= i < end:
                        word = w
                        break
                errors.append((i, c, k, p, exp, PRIMES[prime_idx], word))
                if len(errors) <= 20:
                    print(f"  {i:3d}: cipher={LETTERS[c]:3s}({c:2d}), key={k:2d} (φ({PRIMES[prime_idx]:3d})), "
                          f"plain={LETTERS[p]:3s}({p:2d}), expected={LETTERS[exp]:3s}({exp:2d}) {status} [{word}]")
        
        prime_idx += 1
    
    print(f"\n  Total errors: {len(errors)}")
    
    if len(errors) > 0:
        # Now test with literal F at position 56 (like Page 55)
        print("\n--- TESTING WITH LITERAL F AT POSITION 56 ---")
        
        literal_f = {56}  # Same as Page 55
        
        prime_idx = 0
        correct = 0
        result = []
        
        for i in range(len(cipher)):
            c = cipher[i]
            
            if i in literal_f:
                p = 0  # Literal F
            else:
                k = phi(PRIMES[prime_idx]) % 29
                p = (c - k) % 29
                prime_idx += 1
            
            result.append(p)
            if i < len(expected) and p == expected[i]:
                correct += 1
        
        print(f"  Correct with position 56 as literal F: {correct}/{len(result)}")
        
        # Find all F cipher positions and test each as literal
        print("\n--- TESTING EACH F POSITION AS LITERAL ---")
        for f_pos in f_cipher:
            literal_f = {f_pos}
            prime_idx = 0
            correct = 0
            
            for i in range(len(cipher)):
                c = cipher[i]
                
                if i in literal_f:
                    p = 0
                else:
                    k = phi(PRIMES[prime_idx]) % 29
                    p = (c - k) % 29
                    prime_idx += 1
                
                if i < len(expected) and p == expected[i]:
                    correct += 1
            
            print(f"  Position {f_pos} as literal: {correct}/{len(result)}")
        
        # Test combinations
        print("\n--- TESTING F POSITION COMBINATIONS ---")
        from itertools import combinations
        
        for combo_size in range(2, len(f_cipher) + 1):
            for combo in combinations(f_cipher, combo_size):
                literal_f = set(combo)
                prime_idx = 0
                correct = 0
                
                for i in range(len(cipher)):
                    c = cipher[i]
                    
                    if i in literal_f:
                        p = 0
                    else:
                        k = phi(PRIMES[prime_idx]) % 29
                        p = (c - k) % 29
                        prime_idx += 1
                    
                    if i < len(expected) and p == expected[i]:
                        correct += 1
                
                if correct > 60:
                    print(f"  Positions {combo} as literal: {correct}/{len(result)}")

    # Also check what keys would be needed for each position
    print("\n--- REQUIRED KEYS ANALYSIS ---")
    print("For each position, what key is needed to get expected?")
    
    for i in range(min(10, len(cipher))):
        c = cipher[i]
        exp = expected[i]
        needed = (c - exp) % 29
        
        # Find prime with φ(p)%29 = needed
        matching_primes = [p for p in PRIMES[:100] if phi(p) % 29 == needed]
        
        print(f"  {i}: cipher={LETTERS[c]:3s}, expected={LETTERS[exp]:3s}, need key={needed}, primes with φ(p)%29={needed}: {matching_primes[:5]}")

if __name__ == '__main__':
    main()

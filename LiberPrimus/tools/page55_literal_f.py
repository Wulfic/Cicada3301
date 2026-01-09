#!/usr/bin/env python3
"""
PAGE 55 - Find ALL literal F positions iteratively
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

def decrypt_with_literal_f(cipher, literal_f_positions):
    """Decrypt with specific positions treated as literal F."""
    prime_idx = 0
    result = []
    
    for i in range(len(cipher)):
        c_idx = cipher[i]
        
        if i in literal_f_positions:
            result.append(0)  # F
            # DON'T increment prime_idx
        else:
            k = phi(PRIMES[prime_idx % len(PRIMES)]) % 29
            p = (c_idx - k) % 29
            result.append(p)
            prime_idx += 1
    
    return result

def main():
    print("PAGE 55 - FINDING ALL LITERAL F POSITIONS")
    print("=" * 80)
    
    rune_text = load_page(55)
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    # F rune positions in cipher
    f_rune_positions = [i for i, c in enumerate(cipher) if c == 0]
    print(f"F rune positions in cipher: {f_rune_positions}")
    
    # Expected plaintext
    expected_words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
                     "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
                     "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", 
                     "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    for word in expected_words:
        expected.extend(text_to_indices(word))
    
    # Find F positions in expected
    f_expected_positions = [i for i, c in enumerate(expected) if c == 0]
    print(f"F positions in expected: {f_expected_positions}")
    
    # Try decrypting with no literal F's first
    print("\n--- Without any literal F ---")
    result = decrypt_with_literal_f(cipher, set())
    correct = sum(1 for i in range(len(result)) if i < len(expected) and result[i] == expected[i])
    print(f"Correct: {correct}/{len(result)}")
    
    # Try with position 56 as literal F
    print("\n--- With position 56 as literal F ---")
    result = decrypt_with_literal_f(cipher, {56})
    correct = sum(1 for i in range(len(result)) if i < len(expected) and result[i] == expected[i])
    print(f"Correct: {correct}/{len(result)}")
    
    # Find first mismatch
    for i in range(len(result)):
        if i < len(expected) and result[i] != expected[i]:
            print(f"First mismatch at {i}: got {LETTERS[result[i]]}, expected {LETTERS[expected[i]]}")
            break
    
    # Iteratively find all literal F positions
    print("\n--- Iterative search for literal F positions ---")
    literal_fs = set()
    
    for iteration in range(10):  # Max 10 iterations
        result = decrypt_with_literal_f(cipher, literal_fs)
        
        # Count correct
        correct = sum(1 for i in range(len(result)) if i < len(expected) and result[i] == expected[i])
        print(f"\nIteration {iteration}: {correct}/{len(result)} correct")
        print(f"Literal F positions: {sorted(literal_fs)}")
        
        if correct == len(result):
            print("PERFECT!")
            break
        
        # Find positions where:
        # 1. Cipher is F rune (0)
        # 2. Expected is F (0)
        # 3. Current result is NOT F
        
        found_new = False
        for i in f_rune_positions:
            if i in literal_fs:
                continue
            if i < len(expected) and expected[i] == 0 and result[i] != 0:
                print(f"  Position {i}: cipher=F, expected=F, got {LETTERS[result[i]]} -> marking as literal F")
                literal_fs.add(i)
                found_new = True
                break  # One at a time
        
        if not found_new:
            # No more literal F positions to find
            # Maybe there's a different issue
            print("  No more literal F positions found")
            
            # Show remaining mismatches
            for i in range(len(result)):
                if i < len(expected) and result[i] != expected[i]:
                    print(f"  Mismatch at {i}: got {LETTERS[result[i]]}, expected {LETTERS[expected[i]]}")
                    if i > 75:
                        break
            break
    
    # Final decryption
    print("\n" + "=" * 80)
    print("FINAL DECRYPTION:")
    print("-" * 80)
    
    result = decrypt_with_literal_f(cipher, literal_fs)
    
    # Format with word breaks
    formatted = []
    idx = 0
    for c in rune_text:
        if c in RUNE_MAP:
            if idx < len(result):
                formatted.append(LETTERS[result[idx]])
            idx += 1
        elif c == '-':
            formatted.append(' ')
        elif c == '.':
            formatted.append('. ')
        elif c == '\n':
            formatted.append('\n')
    
    print(''.join(formatted))
    
    print("\n--- EXPECTED ---")
    print(' '.join(expected_words))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
VERIFY PAGE 73 SOLUTION

Page 73 should contain the same "AN END" message as Page 55.
Let's verify it uses the same φ(prime) + literal F method.
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
    prime_idx = 0
    result = []
    for i in range(len(cipher)):
        c = cipher[i]
        if i in literal_f_positions:
            result.append(0)  # F
        else:
            k = phi(PRIMES[prime_idx % len(PRIMES)]) % 29
            result.append((c - k) % 29)
            prime_idx += 1
    return result

def main():
    print("VERIFYING PAGE 73 SOLUTION")
    print("=" * 80)
    
    rune_text = load_page(73)
    
    # Remove the note line
    lines = rune_text.split('\n')
    clean_lines = [l for l in lines if not l.startswith('Note:')]
    rune_text_clean = '\n'.join(clean_lines)
    
    cipher = [RUNE_MAP[c] for c in rune_text_clean if c in RUNE_MAP]
    
    print(f"Cipher length: {len(cipher)}")
    
    # Expected plaintext (same as Page 55)
    expected_words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
                     "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
                     "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", 
                     "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    for word in expected_words:
        expected.extend(text_to_indices(word))
    
    print(f"Expected length: {len(expected)}")
    
    # Find F rune positions in cipher
    f_rune_positions = [i for i, c in enumerate(cipher) if c == 0]
    print(f"F rune positions in cipher: {f_rune_positions}")
    
    # Find F positions in expected
    f_expected_positions = [i for i, c in enumerate(expected) if c == 0]
    print(f"F positions in expected: {f_expected_positions}")
    
    # Page 73 has an extra F at position 0 (before "AN END")
    # Let's check if the cipher starts differently
    
    print("\n--- First 10 cipher indices ---")
    print(cipher[:10])
    
    print("\n--- First 10 expected indices ---")
    print(expected[:10])
    
    # The first cipher value is 0 (F), but expected starts with A (24)
    # This suggests Page 73 has an extra F at the start
    
    # Try shifting cipher by 1
    print("\n--- Testing: Skip first rune (assumed to be literal F) ---")
    cipher_shifted = cipher[1:]  # Skip first F
    
    # Find literal F positions (where cipher=F and expected=F)
    literal_f_positions = set()
    for i in range(min(len(cipher_shifted), len(expected))):
        if cipher_shifted[i] == 0 and i < len(expected) and expected[i] == 0:
            literal_f_positions.add(i)
    
    print(f"Literal F positions (shifted cipher): {literal_f_positions}")
    
    # Decrypt
    result = decrypt_with_literal_f(cipher_shifted, literal_f_positions)
    
    # Count correct
    correct = sum(1 for i in range(min(len(result), len(expected))) if result[i] == expected[i])
    print(f"\nCorrect: {correct}/{len(result)}")
    
    if correct == len(result):
        print("✓ PERFECT MATCH!")
    else:
        # Find first mismatch
        for i in range(min(len(result), len(expected))):
            if result[i] != expected[i]:
                print(f"First mismatch at {i}: got {LETTERS[result[i]]}, expected {LETTERS[expected[i]]}")
                break
    
    # Format output
    print("\n--- DECRYPTED TEXT (Page 73) ---")
    formatted = []
    idx = 0
    for c in rune_text_clean:
        if c in RUNE_MAP:
            if idx == 0:
                formatted.append('[F] ')  # Mark the leading F
            elif idx <= len(result):
                formatted.append(LETTERS[result[idx-1]])  # -1 because we skipped first
            idx += 1
        elif c in '•-':
            formatted.append(' ')
        elif c == '\n':
            formatted.append('\n')
    
    print(''.join(formatted))

if __name__ == '__main__':
    main()

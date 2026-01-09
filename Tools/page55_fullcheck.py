#!/usr/bin/env python3
"""
PAGE 55 FULL ANALYSIS - Check all positions
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
    print("PAGE 55 - FULL POSITION CHECK")
    print("=" * 90)
    
    rune_text = load_page(55)
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    expected_words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
                     "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
                     "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", 
                     "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    for word in expected_words:
        expected.extend(text_to_indices(word))
    
    print(f"{'Pos':>4} {'C':>4} {'K':>4} {'Got':>6} {'Exp':>6} {'Match':>5}")
    print("-" * 90)
    
    decrypted = []
    correct = 0
    first_error = None
    
    for i in range(len(cipher)):
        c = cipher[i]
        k = phi(PRIMES[i % len(PRIMES)]) % 29
        p = (c - k) % 29
        decrypted.append(p)
        
        exp = expected[i] if i < len(expected) else -1
        match = "✓" if p == exp else "✗"
        
        if p == exp:
            correct += 1
        elif first_error is None:
            first_error = i
        
        # Only print first 60 and mismatches
        if i < 50 or p != exp:
            exp_str = LETTERS[exp] if exp >= 0 else "?"
            print(f"{i:>4} {c:>4} {k:>4} {LETTERS[p]:>6} {exp_str:>6} {match:>5}")
    
    print("-" * 90)
    print(f"Correct: {correct}/{len(cipher)}")
    if first_error:
        print(f"First error at position: {first_error}")
    
    # Show the decrypted text
    print("\n--- DECRYPTED TEXT ---")
    
    result = []
    idx = 0
    for c in rune_text:
        if c in RUNE_MAP:
            result.append(LETTERS[decrypted[idx]])
            idx += 1
        elif c == '-':
            result.append(' ')
        elif c == '.':
            result.append('. ')
        elif c == '\n':
            result.append('\n')
    
    print(''.join(result))
    
    print("\n--- EXPECTED TEXT ---")
    print(' '.join(expected_words))

if __name__ == '__main__':
    main()

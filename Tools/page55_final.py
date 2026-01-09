#!/usr/bin/env python3
"""
PAGE 55 FINAL SOLUTION - F-skip with correct prime counter logic

Key insight:
1. F runes (ᚠ) represent LITERAL F's in the plaintext - no decryption needed
2. When we encounter an F rune, output 'F' and DO NOT increment prime counter
3. All other runes use φ(prime[counter]) % 29 as the key
"""

from pathlib import Path

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

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
    """Euler's totient for primes: φ(p) = p - 1"""
    return n - 1 if n >= 2 else 0

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def decrypt_with_f_skip_correct(rune_text):
    """
    Decrypt using φ(prime) formula with correct F-skip logic:
    - F runes are literal, don't use a key
    - The prime counter does NOT increment for F runes
    """
    result = []
    prime_idx = 0  # This only increments for non-F runes
    
    for c in rune_text:
        if c in RUNE_MAP:
            if c == 'ᚠ':  # F rune = literal F
                result.append('F')
                # DO NOT increment prime_idx!
            else:
                cipher_val = RUNE_MAP[c]
                key = phi(PRIMES[prime_idx % len(PRIMES)]) % 29
                plain_val = (cipher_val - key) % 29
                result.append(LETTERS[plain_val])
                prime_idx += 1  # Only increment for non-F runes
        elif c == '-':
            result.append(' ')
        elif c == '.':
            result.append('. ')
        elif c == '•':
            result.append(' ')
        elif c == '\n':
            result.append('\n')
    
    return ''.join(result)

def main():
    print("PAGE 55 FINAL SOLUTION")
    print("=" * 70)
    print("Method: φ(prime) with F-skip (F runes don't increment counter)")
    print("=" * 70)
    
    # Test on Page 55
    p55 = load_page(55)
    result55 = decrypt_with_f_skip_correct(p55)
    
    print("\nPage 55 Decryption:")
    print("-" * 40)
    print(result55)
    
    # Test on Page 73 for comparison
    print("\n" + "=" * 70)
    p73 = load_page(73)
    result73 = decrypt_with_f_skip_correct(p73)
    
    print("Page 73 Decryption:")
    print("-" * 40)
    print(result73)
    
    # Expected
    print("\n" + "=" * 70)
    print("Expected (from Page 56 README):")
    print("-" * 40)
    expected = """AN END
WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO
IT IS THE DUTY OF EUERY PILGRIM TO SEEC OUT THIS PAGE"""
    print(expected)
    
    # Count F runes
    f_count = sum(1 for c in p55 if c == 'ᚠ')
    print(f"\nF rune count in Page 55: {f_count}")
    
    # Show F positions in expected text
    expected_flat = "ANENDWITHINTHEDEEPWEBTHEREEXISTSAPAGETHATHASHESTOITISTHEDUTYFOFUERYPILGRIMTOSEECOUTTHISPAGE"
    # Hmm, where are the F's?
    # "IT IS THE DUTY OF EUERY PILGRIM TO SEEC OUT THIS PAGE"
    # OF contains F
    print("\nF positions in expected plaintext:")
    print("  - 'OF' (position ~56 in continuous text)")
    
    # Also test without the initial notes in Page 73
    print("\n" + "=" * 70)
    print("Testing Page 73 runes only (no notes):")
    # Remove the note line
    p73_clean = '\n'.join(line for line in p73.split('\n') if not line.startswith('Note:'))
    result73_clean = decrypt_with_f_skip_correct(p73_clean)
    print(result73_clean)

if __name__ == '__main__':
    main()

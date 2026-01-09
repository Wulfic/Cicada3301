#!/usr/bin/env python3
"""
PAGE 55 COMPLETE SOLUTION - Using F-skip discovery

Key insight from Page 73:
"Every clear text F is an ᚠ (F), and needs to be skipped."

This means:
1. ᚠ (F rune) in ciphertext = literal F in plaintext (no encryption)
2. The key counter does NOT increment for F runes
3. Only non-F runes use the phi(prime) key

Expected plaintext (85 chars total):
"AN END WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO IT IS THE DUTY OF EUERY PILGRIM TO SEEC OUT THIS PAGE"

Note: V→U (no V in Gematria), K→C (no K in Gematria)
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
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

def phi(n):
    return n - 1 if n >= 2 else 0

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def decrypt_with_f_skip(rune_text):
    """Decrypt using phi(prime) formula, treating F runes as literals."""
    result = []
    key_idx = 0
    
    for c in rune_text:
        if c in RUNE_MAP:
            if c == 'ᚠ':  # F rune = literal F, don't use key
                result.append('F')
                # DON'T increment key_idx
            else:
                cipher_val = RUNE_MAP[c]
                key = phi(PRIMES[key_idx % len(PRIMES)]) % 29
                plain_val = (cipher_val - key) % 29
                result.append(LETTERS[plain_val])
                key_idx += 1
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
    print("PAGE 55 COMPLETE SOLUTION")
    print("=" * 70)
    
    # Test on Page 55
    p55 = load_page(55)
    result55 = decrypt_with_f_skip(p55)
    
    print("Page 55 decryption (F-skip method):")
    print(result55)
    
    # Count F positions
    f_positions = [i for i, c in enumerate([c for c in p55 if c in RUNE_MAP]) if c == 'ᚠ']
    print(f"\nF rune positions (0-indexed): {f_positions}")
    
    # Test on Page 73 for comparison
    print("\n" + "=" * 70)
    p73 = load_page(73)
    result73 = decrypt_with_f_skip(p73)
    
    print("Page 73 decryption (F-skip method):")
    print(result73)
    
    # Expected solution
    print("\n" + "=" * 70)
    print("Expected solution:")
    expected = """AN END
WITHIN THE DEEP WEB
THERE EXISTS A PAGE THAT HASHES TO
IT IS THE DUTY OF EUERY PILGRIM TO SEEC OUT THIS PAGE"""
    print(expected)
    
    # Character-by-character comparison
    print("\n" + "=" * 70)
    print("Checking if solution is correct...")
    
    # Clean results for comparison
    clean55 = ''.join(c for c in result55 if c.isalpha() or c == ' ').upper()
    clean_expected = ''.join(c for c in expected if c.isalpha() or c == ' ').upper()
    
    # Find where they differ
    min_len = min(len(clean55), len(clean_expected))
    for i in range(min_len):
        if clean55[i] != clean_expected[i]:
            print(f"Mismatch at position {i}: got '{clean55[i]}' expected '{clean_expected[i]}'")
            print(f"  Context: ...{clean55[max(0,i-10):i+10]}...")
            break
    else:
        if len(clean55) == len(clean_expected):
            print("✓ PERFECT MATCH!")
        else:
            print(f"Length mismatch: got {len(clean55)}, expected {len(clean_expected)}")

if __name__ == '__main__':
    main()

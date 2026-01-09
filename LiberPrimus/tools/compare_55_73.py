#!/usr/bin/env python3
"""
COMPARE PAGE 55 AND PAGE 73 - They have the same message!

Page 73 notes: "Every clear text F is an ᚠ (F), and needs to be skipped."
This is a HUGE hint! The F runes might not be part of the cipher!
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

def main():
    print("COMPARING PAGE 55 AND PAGE 73")
    print("=" * 70)
    
    p55 = load_page(55)
    p73 = load_page(73)
    
    print("Page 55 raw:")
    print(repr(p55))
    print()
    print("Page 73 raw:")
    print(repr(p73))
    
    # Extract just runes
    r55 = [c for c in p55 if c in RUNE_MAP]
    r73 = [c for c in p73 if c in RUNE_MAP]
    
    print(f"\nPage 55 rune count: {len(r55)}")
    print(f"Page 73 rune count: {len(r73)}")
    
    # Compare character by character
    print("\n--- Comparison ---")
    for i in range(max(len(r55), len(r73))):
        c55 = r55[i] if i < len(r55) else '-'
        c73 = r73[i] if i < len(r73) else '-'
        match = "✓" if c55 == c73 else "✗"
        if c55 != c73:
            print(f"  Position {i}: P55={c55}({RUNE_MAP.get(c55, '?')}) vs P73={c73}({RUNE_MAP.get(c73, '?')}) {match}")
    
    # Try decryption on Page 73 using phi(prime) method, SKIPPING F runes
    print("\n--- Page 73 with F-skipping ---")
    
    # Parse p73 with word boundaries, skipping F in key counter
    result = []
    key_idx = 0
    skip_next_f = False
    
    for c in p73:
        if c in RUNE_MAP:
            if c == 'ᚠ':  # F rune
                # Keep F as literal F (don't apply cipher)
                result.append('F')
                # DON'T increment key counter
            else:
                cipher_val = RUNE_MAP[c]
                key = phi(PRIMES[key_idx % len(PRIMES)]) % 29
                plain_val = (cipher_val - key) % 29
                result.append(LETTERS[plain_val])
                key_idx += 1
        elif c in '•-':
            result.append(' ')
        elif c == '\n':
            result.append('\n')
    
    print("Decrypted with F-skip:")
    print(''.join(result))
    
    # Now try the same on Page 55
    print("\n--- Page 55 with F-skipping ---")
    
    result = []
    key_idx = 0
    
    for c in p55:
        if c in RUNE_MAP:
            if c == 'ᚠ':  # F rune
                result.append('F')
            else:
                cipher_val = RUNE_MAP[c]
                key = phi(PRIMES[key_idx % len(PRIMES)]) % 29
                plain_val = (cipher_val - key) % 29
                result.append(LETTERS[plain_val])
                key_idx += 1
        elif c in '-':
            result.append(' ')
        elif c == '.':
            result.append('. ')
        elif c == '\n':
            result.append('\n')
    
    print("Decrypted with F-skip:")
    print(''.join(result))

if __name__ == '__main__':
    main()

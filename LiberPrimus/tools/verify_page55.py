#!/usr/bin/env python3
"""
VERIFY PAGE 55 SOLUTION AND TEST NEARBY PAGES

Page 55 decrypts perfectly with φ(sequential primes) mod 29!
Let's verify the full decryption and test pages around it.
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

# First 200 primes
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 
          223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 
          293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 
          463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
          569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
          647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739]

def euler_totient(n):
    """For primes, φ(p) = p - 1."""
    if n < 2:
        return 0
    # For primes: φ(p) = p - 1
    return n - 1

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def load_page_runes(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None, None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        rune_text = f.read()
    
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    # Parse with word boundaries
    words = []
    current = []
    for c in rune_text:
        if c in RUNE_MAP:
            current.append(RUNE_MAP[c])
        elif c in '-. \n\r/•':
            if current:
                words.append(current)
                current = []
    if current:
        words.append(current)
    
    return cipher, words, rune_text

def decrypt_totient_seq(cipher):
    """φ(sequential primes) mod 29."""
    plain = []
    for i, c in enumerate(cipher):
        k = euler_totient(PRIMES[i % len(PRIMES)]) % 29
        plain.append((c - k) % 29)
    return plain

def decrypt_page56_formula(cipher):
    """(cipher[i] - (prime[i] + 57)) mod 29."""
    plain = []
    for i, c in enumerate(cipher):
        k = (PRIMES[i % len(PRIMES)] + 57) % 29
        plain.append((c - k) % 29)
    return plain

def format_with_words(plain, rune_text):
    """Format plaintext preserving word boundaries from original."""
    result = []
    idx = 0
    for c in rune_text:
        if c in RUNE_MAP:
            if idx < len(plain):
                result.append(LETTERS[plain[idx]])
            idx += 1
        elif c in '-':
            result.append(' ')
        elif c in '.':
            result.append('. ')
        elif c in '\n':
            result.append('\n')
    return ''.join(result)

def test_page(page_num):
    """Test a page with the totient formula."""
    print(f"\n{'='*70}")
    print(f"PAGE {page_num}")
    print("=" * 70)
    
    data = load_page_runes(page_num)
    if data[0] is None:
        print("Could not load page")
        return None
    
    cipher, words, rune_text = data
    print(f"Cipher length: {len(cipher)}")
    
    # Method 1: φ(sequential primes) mod 29
    plain1 = decrypt_totient_seq(cipher)
    formatted1 = format_with_words(plain1, rune_text)
    
    # Method 2: Page 56 formula (prime + 57)
    plain2 = decrypt_page56_formula(cipher)
    formatted2 = format_with_words(plain2, rune_text)
    
    print("\n--- Method: φ(sequential primes) mod 29 ---")
    print(formatted1[:500])
    
    # Check if they're the same
    if plain1 == plain2:
        print("\n[Both methods give identical results]")
    else:
        print("\n--- Method: prime[i] + 57 mod 29 ---")
        print(formatted2[:500])
    
    return formatted1

def main():
    print("VERIFYING PAGE 55 AND TESTING NEARBY PAGES")
    print("=" * 70)
    
    # Test pages 50-57
    results = {}
    for page_num in [50, 51, 52, 53, 54, 55, 56, 57]:
        result = test_page(page_num)
        if result:
            results[page_num] = result
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - Pages with coherent English output")
    print("=" * 70)
    
    for page_num, text in results.items():
        # Check for common words
        words_in_text = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'THAT', 'FOR', 'WITH']
        word_count = sum(1 for w in words_in_text if w in text.upper())
        if word_count >= 3:
            print(f"\nPage {page_num} looks COHERENT ({word_count} common words):")
            print(text[:200])

if __name__ == '__main__':
    main()

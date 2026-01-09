#!/usr/bin/env python3
"""
APPLY PHI(PRIME) + LITERAL F METHOD TO ALL UNSOLVED PAGES

Now that we've solved Page 55 with:
- φ(prime) shift cipher
- Literal F handling (F runes for plaintext F don't increment counter)

Let's test this on other unsolved pages to see if any decrypt.
"""

from pathlib import Path
import re

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
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
          463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
          569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
          647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
          743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
          839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937,
          941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021]

COMMON_WORDS = {'THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'THAT', 'FOR', 'WITH',
                'AS', 'BE', 'ON', 'AT', 'BY', 'FROM', 'OR', 'AN', 'ARE', 'WAS',
                'THIS', 'ALL', 'ONE', 'WE', 'YOU', 'THEY', 'THEIR', 'WILL',
                'WHAT', 'HAS', 'HAVE', 'BEEN', 'WHICH', 'WOULD', 'THERE',
                'WITHIN', 'DEEP', 'WEB', 'EXISTS', 'PAGE', 'DUTY', 'PILGRIM',
                'LIKE', 'INSTAR', 'TUNNELING', 'SURFACE', 'MUST', 'SHED',
                'OWN', 'FIND', 'DIVINITY', 'EMERGE', 'PARABLE', 'END',
                'CIRCUMFERENCE', 'CIRCUMFERENCES', 'SELF', 'SACRED', 'PRIME',
                'PRIMES', 'TOTIENT', 'FUNCTION'}

def phi(n):
    return n - 1 if n >= 2 else 0

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None, None
    with open(runes_file, 'r', encoding='utf-8') as f:
        rune_text = f.read()
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    return rune_text, cipher

def decrypt_phi_prime(cipher, literal_f_positions=None):
    """Decrypt using φ(prime) with optional literal F handling."""
    if literal_f_positions is None:
        literal_f_positions = set()
    
    prime_idx = 0
    result = []
    
    for i, c in enumerate(cipher):
        if i in literal_f_positions:
            result.append(0)  # F
        else:
            k = phi(PRIMES[prime_idx % len(PRIMES)]) % 29
            result.append((c - k) % 29)
            prime_idx += 1
    
    return result

def format_result(result, rune_text):
    """Format result with word boundaries."""
    formatted = []
    idx = 0
    for c in rune_text:
        if c in RUNE_MAP:
            if idx < len(result):
                formatted.append(LETTERS[result[idx]])
            idx += 1
        elif c in '-':
            formatted.append(' ')
        elif c == '.':
            formatted.append('. ')
        elif c == '•':
            formatted.append(' ')
        elif c == '\n':
            formatted.append('\n')
    return ''.join(formatted)

def count_words(text):
    """Count common English words in text."""
    text_upper = text.upper()
    words = re.findall(r'[A-Z]+', text_upper)
    count = 0
    found = []
    for w in COMMON_WORDS:
        if w in words:
            count += 1
            found.append(w)
    return count, found

def find_literal_f_positions(cipher, result):
    """Find positions where F rune should be literal F."""
    # Look for positions where:
    # 1. Cipher is F (0)
    # 2. Decrypted value looks wrong
    # 3. Nearby context suggests F would fit
    
    # This is heuristic - in practice we'd need context
    f_positions = [i for i, c in enumerate(cipher) if c == 0]
    return f_positions

def test_page(page_num):
    """Test a single page with φ(prime) method."""
    rune_text, cipher = load_page(page_num)
    if cipher is None or len(cipher) == 0:
        return None
    
    # Basic φ(prime) decryption (no literal F)
    result = decrypt_phi_prime(cipher)
    formatted = format_result(result, rune_text)
    word_count, words = count_words(formatted)
    
    # Also try with different prime starting positions
    best_result = (word_count, 0, formatted, words)
    
    for start in range(1, 20):
        result_shifted = []
        for i, c in enumerate(cipher):
            k = phi(PRIMES[(start + i) % len(PRIMES)]) % 29
            result_shifted.append((c - k) % 29)
        formatted_shifted = format_result(result_shifted, rune_text)
        wc, ws = count_words(formatted_shifted)
        if wc > best_result[0]:
            best_result = (wc, start, formatted_shifted, ws)
    
    return best_result

def main():
    print("TESTING PHI(PRIME) METHOD ON ALL PAGES")
    print("=" * 80)
    
    # Pages to test (unsolved or partially solved)
    test_pages = list(range(17, 75))  # All potentially unsolved pages
    
    results = []
    
    for page_num in test_pages:
        result = test_page(page_num)
        if result is None:
            continue
        
        word_count, start, formatted, words = result
        
        if word_count >= 3:  # At least 3 common words found
            results.append((page_num, word_count, start, formatted, words))
    
    # Sort by word count
    results.sort(key=lambda x: -x[1])
    
    print("\nPages with 3+ common words found:")
    print("-" * 80)
    
    for page_num, word_count, start, formatted, words in results[:20]:
        print(f"\nPage {page_num}: {word_count} words (prime start={start})")
        print(f"  Words: {', '.join(words[:10])}")
        preview = formatted.replace('\n', ' ')[:150]
        print(f"  Preview: {preview}")
    
    print("\n" + "=" * 80)
    print("DETAILED OUTPUT FOR TOP CANDIDATES")
    print("=" * 80)
    
    for page_num, word_count, start, formatted, words in results[:5]:
        print(f"\n{'='*40}")
        print(f"PAGE {page_num} - {word_count} words found")
        print(f"Prime start index: {start}")
        print(f"{'='*40}")
        print(formatted[:500])

if __name__ == '__main__':
    main()

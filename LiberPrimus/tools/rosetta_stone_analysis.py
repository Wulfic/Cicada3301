#!/usr/bin/env python3
"""
ROSETTA STONE ANALYSIS

Use the solved Page 56 to understand and validate key generation patterns.
Page 56 is confirmed solved with: plaintext[i] = (cipher[i] - (prime[i] + 57)) mod 29

This analysis will:
1. Extract the actual keys used in Page 56
2. Check if word-index multiplier formula applies
3. Understand the relationship between position and key
"""

import os
from pathlib import Path
from math import isqrt

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

# Generate primes
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

def get_primes(count):
    primes = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

PRIMES = get_primes(200)

def load_runes(page_num):
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_rune_stream(rune_text):
    """Get all runes in order (for position-based keys)."""
    return [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]

def parse_words(rune_text):
    """Parse rune text into word structures."""
    words = []
    current_word = {'indices': [], 'start_pos': 0}
    pos = 0
    
    for char in rune_text:
        if char in RUNE_MAP:
            if not current_word['indices']:
                current_word['start_pos'] = pos
            current_word['indices'].append(RUNE_MAP[char])
            pos += 1
        elif char in '-. \n\r':
            if current_word['indices']:
                words.append(current_word)
                current_word = {'indices': [], 'start_pos': 0}
    
    if current_word['indices']:
        words.append(current_word)
    
    return words

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

# Known plaintext for Page 56 (The Parable)
PAGE_56_PLAINTEXT = """PARABLE.LIKE-THE-INSTAR-TUNNELING-TO-THE-SURFACE.WE-MUST-SHED-OUR-OWN-CIRCUMFERENCES.FIND-THE-DIVINITY-WITHIN-AND-EMERGE."""

def analyze_page_56():
    """Analyze Page 56 to understand key generation."""
    
    print("=" * 70)
    print("PAGE 56 ROSETTA STONE ANALYSIS")
    print("=" * 70)
    
    rune_text = load_runes(56)
    if not rune_text:
        print("ERROR: Could not load Page 56")
        return
    
    print(f"\nRune text:\n{rune_text[:200]}...")
    
    runes = parse_rune_stream(rune_text)
    words = parse_words(rune_text)
    
    print(f"\nTotal runes: {len(runes)}")
    print(f"Total words: {len(words)}")
    
    # Known formula: key[i] = (prime[i] + 57) mod 29
    print("\n" + "=" * 70)
    print("POSITION-BASED KEY (Known Formula)")
    print("Formula: key[i] = (prime[i] + 57) mod 29")
    print("=" * 70)
    
    # Apply known formula
    position_keys = [(PRIMES[i] + 57) % 29 for i in range(len(runes))]
    
    decrypted = [(runes[i] - position_keys[i]) % 29 for i in range(len(runes))]
    decrypted_text = indices_to_text(decrypted)
    
    print(f"\nDecrypted with position-based prime keys:")
    print(decrypted_text)
    
    # Now extract what the PER-WORD key would be
    print("\n" + "=" * 70)
    print("WORD-BY-WORD KEY ANALYSIS")
    print("=" * 70)
    
    word_keys = []
    
    for word_idx, word in enumerate(words):
        # The key for this word (using first rune's position)
        start_pos = word['start_pos']
        
        # What key does the first rune of this word use?
        first_key = position_keys[start_pos]
        
        # What about all runes in the word?
        word_positions = list(range(start_pos, start_pos + len(word['indices'])))
        keys_in_word = [position_keys[p] for p in word_positions]
        
        cipher_text = indices_to_text(word['indices'])
        plain_indices = [decrypted[p] for p in word_positions]
        plain_text = indices_to_text(plain_indices)
        
        word_keys.append({
            'word_idx': word_idx,
            'start_pos': start_pos,
            'cipher': cipher_text,
            'plain': plain_text,
            'first_key': first_key,
            'all_keys': keys_in_word
        })
        
        print(f"Word {word_idx:2d}: pos={start_pos:3d}, cipher={cipher_text:15s} -> {plain_text:15s}")
        print(f"         keys: {keys_in_word}")
    
    # Check if word-index formula fits
    print("\n" + "=" * 70)
    print("TESTING WORD-INDEX FORMULA")
    print("Does key[word_idx] = f(word_idx) ?")
    print("=" * 70)
    
    # Get just the first key of each word
    first_keys = [wk['first_key'] for wk in word_keys]
    word_indices = list(range(len(first_keys)))
    
    print(f"\nFirst keys per word: {first_keys}")
    print(f"Word indices: {word_indices}")
    
    # Test linear formula: key = a*word_idx + b (mod 29)
    print("\nSearching for formula: key = mult*word_idx + offset (mod 29)")
    
    for mult in range(1, 29):
        for offset in range(29):
            matches = 0
            for wi, key in enumerate(first_keys):
                predicted = (wi * mult + offset) % 29
                if predicted == key:
                    matches += 1
            
            if matches > 5:  # If we match more than a few
                print(f"  mult={mult:2d}, offset={offset:2d}: {matches}/{len(first_keys)} matches")
    
    # The keys vary by position, not word index!
    # Let's see the relationship between start_pos and key
    print("\n" + "=" * 70)
    print("RELATIONSHIP: start_position -> first_key")
    print("=" * 70)
    
    for wk in word_keys:
        pos = wk['start_pos']
        key = wk['first_key']
        prime_val = PRIMES[pos]
        expected = (prime_val + 57) % 29
        print(f"Word {wk['word_idx']:2d}: pos={pos:3d}, prime[pos]={prime_val:3d}, "
              f"(prime+57) mod 29 = {expected:2d}, actual key = {key:2d}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("\nPage 56 uses POSITION-based keys (not word-index based):")
    print("  key[i] = (prime(i) + 57) mod 29")
    print("where prime(i) is the i-th prime number (2, 3, 5, 7, 11, ...)")
    print("\nThis is a DIFFERENT cipher than what we tested with word-index!")
    print("The question is: do other unsolved pages use this same formula?")

def test_prime_formula_on_page(page_num, constant_offset=57):
    """Test the Page 56 formula on another page."""
    
    rune_text = load_runes(page_num)
    if not rune_text:
        return None
    
    runes = parse_rune_stream(rune_text)
    words = parse_words(rune_text)
    
    # Apply formula: key[i] = (prime[i] + constant_offset) mod 29
    keys = [(PRIMES[i] + constant_offset) % 29 for i in range(len(runes))]
    decrypted = [(runes[i] - keys[i]) % 29 for i in range(len(runes))]
    
    # Score by English words
    ENGLISH = {'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
               'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
               'WE', 'THE', 'AND', 'FOR', 'THY', 'WITH', 'THIS', 'THAT', 'PATH', 'FIND',
               'SEEK', 'TRUTH', 'LIGHT', 'DIVINE', 'WISDOM', 'SURFACE', 'EMERGE'}
    
    score = 0
    english_found = []
    
    for word in words:
        start = word['start_pos']
        length = len(word['indices'])
        word_dec = decrypted[start:start+length]
        text = indices_to_text(word_dec)
        
        if text.upper() in ENGLISH:
            score += len(text) * 100
            english_found.append(text)
    
    return {
        'score': score,
        'english': english_found,
        'decrypted': indices_to_text(decrypted)[:100]
    }

def test_prime_formula_variations():
    """Test prime formula with different offsets on all pages."""
    
    print("\n" + "=" * 70)
    print("TESTING PRIME FORMULA ON OTHER PAGES")
    print("Formula: key[i] = (prime[i] + offset) mod 29")
    print("=" * 70)
    
    for page_num in [8, 9, 10, 43, 51]:
        print(f"\n--- Page {page_num} ---")
        
        best_offset = 0
        best_score = 0
        best_words = []
        
        for offset in range(100):  # Try many offsets
            result = test_prime_formula_on_page(page_num, offset)
            if result and result['score'] > best_score:
                best_score = result['score']
                best_offset = offset
                best_words = result['english']
        
        if best_score > 0:
            print(f"Best offset: {best_offset}, score: {best_score}")
            print(f"English words: {', '.join(best_words)}")
            
            # Show decryption
            result = test_prime_formula_on_page(page_num, best_offset)
            print(f"Sample: {result['decrypted']}")
        else:
            print("No English words found with any offset (0-99)")

if __name__ == '__main__':
    analyze_page_56()
    test_prime_formula_variations()

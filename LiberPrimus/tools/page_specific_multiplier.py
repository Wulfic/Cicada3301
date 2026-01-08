#!/usr/bin/env python3
"""
Page-Specific Multiplier Discovery

Key finding: Different pages work best with different multipliers!
- Page 8: mult=17, offset=9 (best)
- Page 13: mult=13, offset=8 (best) 
- Page 43: mult=19, offset=18 (best)
- Page 46: mult=2, offset=16 (best)

Is there a pattern? Let's investigate.
"""

import os
from pathlib import Path
from collections import Counter

# Gematria Primus mappings
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

COMMON_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN',
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US',
    'WE', 'ALL', 'AND', 'ARE', 'BUT', 'CAN', 'FOR', 'HAS', 'HIM', 'HIS',
    'HOW', 'ITS', 'MAY', 'NEW', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT',
    'OWN', 'SAY', 'SHE', 'THE', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'YOU',
    'FIND', 'FROM', 'HAVE', 'INTO', 'JUST', 'KNOW', 'LIKE', 'MAKE', 'MANY',
    'MORE', 'MUST', 'ONLY', 'OVER', 'PATH', 'SELF', 'SOME', 'SUCH', 'TAKE', 
    'THAN', 'THAT', 'THEM', 'THEN', 'THIS', 'THUS', 'UNTO', 'UPON', 'WHAT', 
    'WHEN', 'WILL', 'WITH', 'YOUR', 'SEEK', 'THOU', 'THEE', 'THY', 'YE',
    'HATH', 'DOTH', 'YEA', 'NAY', 'WISDOM', 'TRUTH', 'LIGHT', 'DIVINITY'
}

GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
             59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_words(rune_text):
    """Parse rune text into word index lists."""
    words = []
    current_word = []
    
    for char in rune_text:
        if char in RUNE_MAP:
            current_word.append(RUNE_MAP[char])
        elif char in '-. \n\r':
            if current_word:
                words.append(current_word)
                current_word = []
    
    if current_word:
        words.append(current_word)
    
    return words

def decrypt_word(indices, key):
    return [(c - key) % 29 for c in indices]

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def score_word(text):
    if text.upper() in COMMON_WORDS:
        return len(text) * 100
    return 0

def find_best_multiplier_per_page():
    """Find the best (mult, offset) for each unsolved page."""
    
    print("=" * 70)
    print("OPTIMAL MULTIPLIER DISCOVERY - ALL UNSOLVED PAGES")
    print("=" * 70)
    
    results = []
    
    for page_num in range(8, 57):
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words(rune_text)
        if len(words) < 20:
            continue
        
        best_mult = 0
        best_offset = 0
        best_score = 0
        best_words = []
        
        for mult in range(1, 29):
            for offset in range(29):
                total_score = 0
                found_words = []
                
                for word_idx, word in enumerate(words):
                    key = (word_idx * mult + offset) % 29
                    decrypted = decrypt_word(word, key)
                    text = indices_to_text(decrypted)
                    score = score_word(text)
                    total_score += score
                    
                    if score > 0:
                        found_words.append((word_idx, text, key))
                
                if total_score > best_score:
                    best_score = total_score
                    best_mult = mult
                    best_offset = offset
                    best_words = found_words
        
        results.append((page_num, best_mult, best_offset, best_score, best_words))
    
    # Sort by score
    results.sort(key=lambda x: x[3], reverse=True)
    
    print("\nTop 30 pages by score:")
    print("-" * 70)
    
    for page_num, mult, offset, score, found_words in results[:30]:
        words_str = ', '.join(f"{w[1]}" for w in found_words[:5])
        print(f"Page {page_num:2d}: mult={mult:2d}, offset={offset:2d}, score={score:4d}")
        print(f"         Words: {words_str}")
    
    return results

def analyze_multiplier_pattern():
    """Analyze if multiplier relates to page number."""
    
    print("\n" + "=" * 70)
    print("MULTIPLIER vs PAGE NUMBER ANALYSIS")
    print("=" * 70)
    
    # Best multipliers found for key pages
    best_mults = {
        8: (17, 9),
        13: (13, 8),
        43: (19, 18),
        46: (2, 16),
    }
    
    print("\nPage vs Best Multiplier:")
    for page, (mult, offset) in best_mults.items():
        # Check relationships
        print(f"\nPage {page}: mult={mult}, offset={offset}")
        print(f"  page mod 29 = {page % 29}")
        print(f"  page + mult = {page + mult}, mod 29 = {(page + mult) % 29}")
        print(f"  page * mult mod 29 = {(page * mult) % 29}")
        print(f"  (29 - page) mod 29 = {(29 - page) % 29}")
        print(f"  mult is prime? {mult in [2,3,5,7,11,13,17,19,23]}")
        
        # Check if mult or offset relates to Gematria primes
        if mult < len(GP_PRIMES):
            print(f"  GP prime at index {mult} = {GP_PRIMES[mult]}")
        if page < len(GP_PRIMES):
            print(f"  GP prime at index {page} = {GP_PRIMES[page]}")

def test_prime_multiplier():
    """Test if multiplier = prime[page_index] or similar."""
    
    print("\n" + "=" * 70)
    print("PRIME-BASED MULTIPLIER TEST")
    print("=" * 70)
    
    # Test: mult = GP_PRIMES[page mod 29] mod 29
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words(rune_text)
        
        # Try various prime-based multipliers
        test_mults = [
            (GP_PRIMES[page_num % 29] % 29, f"prime[{page_num}] mod 29"),
            ((page_num + 1) % 29, "page+1"),
            ((29 - page_num) % 29, "29-page"),
            (GP_PRIMES[page_num % len(GP_PRIMES)] % 29, f"prime[{page_num} mod 29]"),
        ]
        
        print(f"\nPage {page_num}:")
        
        for mult, desc in test_mults:
            for offset in range(29):
                total_score = 0
                found_words = []
                
                for word_idx, word in enumerate(words):
                    key = (word_idx * mult + offset) % 29
                    decrypted = decrypt_word(word, key)
                    text = indices_to_text(decrypted)
                    score = score_word(text)
                    total_score += score
                    
                    if score > 0:
                        found_words.append(text)
                
                if total_score > 500:
                    print(f"  {desc}={mult:2d}, offset={offset:2d}: score={total_score:4d}, words={found_words[:5]}")

def decode_with_best_parameters():
    """Decode pages using their best (mult, offset) and show full text."""
    
    print("\n" + "=" * 70)
    print("FULL DECODE WITH OPTIMAL PARAMETERS")
    print("=" * 70)
    
    best_params = {
        8: (17, 9),
        13: (13, 8),
        43: (19, 18),
        46: (2, 16),
    }
    
    for page_num, (mult, offset) in best_params.items():
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words(rune_text)
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} - mult={mult}, offset={offset}")
        print(f"{'='*70}")
        
        decoded_words = []
        for word_idx, word in enumerate(words):
            key = (word_idx * mult + offset) % 29
            decrypted = decrypt_word(word, key)
            text = indices_to_text(decrypted)
            
            # Mark known English words
            if text.upper() in COMMON_WORDS:
                text = f"[{text}]"
            
            decoded_words.append(text)
        
        # Print in lines of ~10 words
        for i in range(0, len(decoded_words), 10):
            print(' '.join(decoded_words[i:i+10]))

def find_common_multiplier():
    """See if there's ONE multiplier that works well across all pages."""
    
    print("\n" + "=" * 70)
    print("UNIVERSAL MULTIPLIER SEARCH")
    print("=" * 70)
    
    mult_scores = {m: 0 for m in range(1, 29)}
    mult_details = {m: [] for m in range(1, 29)}
    
    for page_num in range(8, 57):
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words(rune_text)
        if len(words) < 20:
            continue
        
        for mult in range(1, 29):
            best_offset_score = 0
            
            for offset in range(29):
                total_score = 0
                
                for word_idx, word in enumerate(words):
                    key = (word_idx * mult + offset) % 29
                    decrypted = decrypt_word(word, key)
                    text = indices_to_text(decrypted)
                    score = score_word(text)
                    total_score += score
                
                if total_score > best_offset_score:
                    best_offset_score = total_score
            
            mult_scores[mult] += best_offset_score
            mult_details[mult].append((page_num, best_offset_score))
    
    # Sort multipliers by total score
    sorted_mults = sorted(mult_scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\nMultipliers ranked by total score across all pages:")
    for mult, total_score in sorted_mults[:10]:
        top_pages = sorted(mult_details[mult], key=lambda x: x[1], reverse=True)[:5]
        top_pages_str = ', '.join(f"p{p[0]}:{p[1]}" for p in top_pages)
        print(f"  mult={mult:2d}: total_score={total_score:6d}, top pages: {top_pages_str}")

if __name__ == '__main__':
    results = find_best_multiplier_per_page()
    analyze_multiplier_pattern()
    test_prime_multiplier()
    decode_with_best_parameters()
    find_common_multiplier()

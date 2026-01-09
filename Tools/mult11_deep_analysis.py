#!/usr/bin/env python3
"""
MULTIPLIER 11 DEEP ANALYSIS

Key finding from running_key_position_attack.py:
- Page 8 with mult=11, offset=10 scored 530 (highest!)
- Page 13 with mult=22 (2×11), offset=15 scored 520

The number 11 appears prominently:
- Gap of 11 discovered by community
- 11 is the 5th prime
- 29 - 18 = 11 (gap pattern)

Let's deeply investigate multiplier-11 based keys.
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
    'WHEN', 'WILL', 'WITH', 'YOUR', 'BEING', 'THEIR', 'THERE', 'THESE', 
    'THING', 'THOSE', 'TRUTH', 'WHICH', 'WITHIN', 'THEE', 'THOU', 'THY',
    'YE', 'HATH', 'DOTH', 'SEEK', 'WISDOM', 'LIGHT', 'KNOWLEDGE', 'DIVINE',
    'SHED', 'BECOME', 'INSTAR', 'EMERGE', 'SURFACE', 'PRIME', 'PRIMES',
    'CIRCUMFERENCE', 'CONSUMPTION', 'INSTRUCTION', 'ADMONITION'
}

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(LETTERS[i] for i in indices)

def score_text(text):
    """Score based on English words."""
    score = 0
    text_upper = text.upper()
    
    for word in COMMON_WORDS:
        if word in text_upper:
            score += len(word) * 10
    
    return score

def decrypt_mult_key(cipher_indices, mult, offset):
    """Decrypt using key = (position * mult + offset) mod 29."""
    plaintext = []
    for pos, c in enumerate(cipher_indices):
        key = (pos * mult + offset) % 29
        p = (c - key) % 29
        plaintext.append(p)
    return plaintext

def test_mult11_all_pages():
    """Test multiplier=11 across all unsolved pages."""
    
    print("=" * 70)
    print("MULTIPLIER 11 ANALYSIS - ALL UNSOLVED PAGES")
    print("=" * 70)
    
    # Unsolved pages (our numbering)
    unsolved_pages = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                      23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                      38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                      53, 54, 55, 56]
    
    all_results = []
    
    for page_num in unsolved_pages:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        if len(cipher_indices) < 20:
            continue
        
        # Test mult=11 with all offsets
        best_offset = 0
        best_score = 0
        best_text = ""
        
        for offset in range(29):
            plaintext_indices = decrypt_mult_key(cipher_indices, 11, offset)
            plaintext = indices_to_text(plaintext_indices)
            score = score_text(plaintext)
            
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = plaintext[:80]
        
        all_results.append((page_num, best_offset, best_score, best_text))
    
    # Sort by score
    all_results.sort(key=lambda x: x[2], reverse=True)
    
    print("\nTop 20 pages with mult=11:")
    for page_num, offset, score, text in all_results[:20]:
        print(f"  Page {page_num:2d}: offset={offset:2d}, score={score:4d}")
        print(f"           {text[:60]}")
    
    return all_results

def test_variations_of_11():
    """Test variations: 11, 2×11=22, 11 inverse, etc."""
    
    print("\n" + "=" * 70)
    print("VARIATIONS OF MULTIPLIER 11")
    print("=" * 70)
    
    # 11 is its own inverse mod 29: 11 * 11 = 121 = 4*29 + 5 ≠ 1
    # Actually find inverse of 11 mod 29
    for i in range(1, 29):
        if (11 * i) % 29 == 1:
            print(f"Inverse of 11 mod 29 = {i}")
            inv_11 = i
            break
    
    # Test multipliers related to 11
    multipliers = [11, 22, 8, 3, 6, 18]  # 8 is inverse of 11 mod 29: 11*8=88=3*29+1
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        print(f"\nPage {page_num}:")
        
        for mult in multipliers:
            best_offset = 0
            best_score = 0
            best_text = ""
            
            for offset in range(29):
                plaintext_indices = decrypt_mult_key(cipher_indices, mult, offset)
                plaintext = indices_to_text(plaintext_indices)
                score = score_text(plaintext)
                
                if score > best_score:
                    best_score = score
                    best_offset = offset
                    best_text = plaintext
            
            print(f"  mult={mult:2d}, offset={best_offset:2d}: score={best_score:4d}, text={best_text[:50]}")

def analyze_mult11_text():
    """Show full decoded text with mult=11 for best pages."""
    
    print("\n" + "=" * 70)
    print("FULL DECODED TEXT WITH MULT=11")
    print("=" * 70)
    
    best_pages = [
        (8, 10),   # Page 8, offset 10
        (13, 15),  # Page 13, offset 15 (using mult=22)
    ]
    
    for page_num, offset in best_pages:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        word_boundaries = []
        pos = 0
        
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
                pos += 1
            elif char in '-. ':
                word_boundaries.append(pos)
        
        print(f"\nPage {page_num} with mult=11, offset={offset}:")
        
        plaintext_indices = decrypt_mult_key(cipher_indices, 11, offset)
        plaintext = indices_to_text(plaintext_indices)
        
        # Add word boundaries
        formatted = []
        last_bound = 0
        for bound in word_boundaries:
            if bound > last_bound:
                formatted.append(plaintext[last_bound:bound])
            last_bound = bound
        if last_bound < len(plaintext):
            formatted.append(plaintext[last_bound:])
        
        print(' '.join(formatted[:30]))

def check_11_generates_known_keys():
    """Check if mult=11 formula generates the keys we discovered."""
    
    print("\n" + "=" * 70)
    print("DOES MULT=11 GENERATE DISCOVERED KEYS?")
    print("=" * 70)
    
    discoveries = [
        {'page': 8, 'word_pos': 3, 'rune_start': 12, 'word': 'PATH', 'key': 14},
        {'page': 8, 'word_pos': 10, 'rune_start': 40, 'word': 'THE', 'key': 1},
        {'page': 13, 'word_pos': 5, 'rune_start': 23, 'word': 'A', 'key': 2},
        {'page': 13, 'word_pos': 7, 'rune_start': 28, 'word': 'A', 'key': 6},
        {'page': 13, 'word_pos': 11, 'rune_start': 38, 'word': 'IN', 'key': 23},
        {'page': 13, 'word_pos': 13, 'rune_start': 44, 'word': 'I', 'key': 8},
        {'page': 13, 'word_pos': 17, 'rune_start': 58, 'word': 'DO', 'key': 9},
        {'page': 43, 'word_pos': 6, 'rune_start': 23, 'word': 'BE', 'key': 12},
        {'page': 43, 'word_pos': 12, 'rune_start': 55, 'word': 'THY', 'key': 25},
        {'page': 43, 'word_pos': 17, 'rune_start': 74, 'word': 'NO', 'key': 3},
        {'page': 46, 'word_pos': 6, 'rune_start': 22, 'word': 'I', 'key': 11},
        {'page': 46, 'word_pos': 10, 'rune_start': 34, 'word': 'UP', 'key': 5},
        {'page': 46, 'word_pos': 17, 'rune_start': 54, 'word': 'GO', 'key': 15},
        {'page': 46, 'word_pos': 19, 'rune_start': 63, 'word': 'AN', 'key': 18},
        {'page': 46, 'word_pos': 20, 'rune_start': 65, 'word': 'I', 'key': 12},
    ]
    
    print("\nChecking key = (rune_start * 11 + offset) mod 29:")
    
    for d in discoveries:
        rune_start = d['rune_start']
        actual_key = d['key']
        
        # Find what offset would make it work
        # key = (rune_start * 11 + offset) mod 29
        # offset = (key - rune_start * 11) mod 29
        offset_needed = (actual_key - rune_start * 11) % 29
        
        # Compute what key mult=11 would give
        key_computed = (rune_start * 11) % 29
        
        print(f"  {d['word']:4} page={d['page']:2} rune_start={rune_start:2}: "
              f"actual_key={actual_key:2}, 11*pos mod 29={key_computed:2}, "
              f"offset_needed={offset_needed:2}")
    
    # Check if offsets are consistent per page
    print("\nPer-page offset analysis:")
    for page in [8, 13, 43, 46]:
        page_discoveries = [d for d in discoveries if d['page'] == page]
        offsets = [(d['key'] - d['rune_start'] * 11) % 29 for d in page_discoveries]
        print(f"  Page {page}: offsets needed = {offsets}")

def test_page_specific_offset():
    """Test if each page has a specific offset for mult=11."""
    
    print("\n" + "=" * 70)
    print("PAGE-SPECIFIC OFFSET FOR MULT=11")
    print("=" * 70)
    
    # Try finding optimal offset per page
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        print(f"\nPage {page_num}:")
        
        for offset in range(29):
            plaintext_indices = decrypt_mult_key(cipher_indices, 11, offset)
            plaintext = indices_to_text(plaintext_indices)
            score = score_text(plaintext)
            
            if score >= 450:
                print(f"  offset={offset:2d}: score={score:4d}")
                # Show with word boundaries
                print(f"    {plaintext[:80]}")

if __name__ == '__main__':
    results = test_mult11_all_pages()
    test_variations_of_11()
    analyze_mult11_text()
    check_11_generates_known_keys()
    test_page_specific_offset()

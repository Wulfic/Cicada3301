#!/usr/bin/env python3
"""
Combined Word-Boundary + Positional Multiplier Analysis

Key findings to combine:
1. Word boundaries (hyphens) mark actual word separations
2. Multiplier 11 (and multiples) produce better scores
3. Keys vary per word but may follow a position-based pattern

Goal: Find if key = (word_start_position × multiplier + offset) mod 29 works
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

# Comprehensive English word list
COMMON_WORDS = {
    # One letter
    'A', 'I',
    # Two letters
    'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 
    'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
    # Three letters  
    'ALL', 'AND', 'ARE', 'BUT', 'CAN', 'FOR', 'HAS', 'HIM', 'HIS', 'HOW', 
    'ITS', 'MAY', 'NEW', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT', 'OWN', 
    'SAY', 'SHE', 'THE', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'YOU', 'YET',
    'THY', 'YEA', 'NAY',
    # Four letters
    'FIND', 'FROM', 'HAVE', 'INTO', 'JUST', 'KNOW', 'LIKE', 'MAKE', 'MANY',
    'MORE', 'MUST', 'ONLY', 'OVER', 'PATH', 'SELF', 'SOME', 'SUCH', 'TAKE', 
    'THAN', 'THAT', 'THEM', 'THEN', 'THIS', 'THUS', 'UNTO', 'UPON', 'WHAT', 
    'WHEN', 'WILL', 'WITH', 'YOUR', 'SEEK', 'THOU', 'THEE', 'HATH', 'DOTH',
    # Five letters
    'BEING', 'THEIR', 'THERE', 'THESE', 'THING', 'THOSE', 'TRUTH', 'WHICH', 
    'THINE', 'SHALT', 'SHALL', 'WORLD', 'LIGHT', 'WISDOM', 'PRIME',
    # Six+ letters
    'WITHIN', 'DIVINITY', 'EMERGE', 'KNOWLEDGE', 'BECOME', 'CIRCUMFERENCE',
    'CONSUMPTION', 'INSTRUCTION', 'ADMONITION', 'INSTAR', 'SURFACE'
}

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_words_with_positions(rune_text):
    """Parse rune text into words with their rune position information."""
    words = []
    current_word_indices = []
    current_word_start = 0
    rune_pos = 0
    
    for char in rune_text:
        if char in RUNE_MAP:
            if not current_word_indices:
                current_word_start = rune_pos
            current_word_indices.append(RUNE_MAP[char])
            rune_pos += 1
        elif char in '-. \n\r':
            if current_word_indices:
                words.append({
                    'indices': current_word_indices,
                    'start_pos': current_word_start,
                    'length': len(current_word_indices)
                })
                current_word_indices = []
    
    if current_word_indices:
        words.append({
            'indices': current_word_indices,
            'start_pos': current_word_start,
            'length': len(current_word_indices)
        })
    
    return words

def decrypt_word(word_indices, key):
    """Decrypt a word using a single key value."""
    return [(c - key) % 29 for c in word_indices]

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(LETTERS[i] for i in indices)

def score_word(text):
    """Score a word. Higher if it's a known English word."""
    if text.upper() in COMMON_WORDS:
        return len(text) * 100
    
    # Partial scoring for common patterns
    score = 0
    t = text.upper()
    
    # Common prefixes
    if t.startswith(('TH', 'WH', 'CH', 'SH', 'ST', 'PR', 'TR')):
        score += 10
    
    # Common suffixes  
    if t.endswith(('ING', 'ED', 'LY', 'ER', 'EST', 'TION', 'MENT')):
        score += 10
    
    # Common vowel patterns
    if any(v in t for v in ['EA', 'EE', 'OO', 'AI', 'OU']):
        score += 5
    
    return score

def test_word_position_key(pages=[8, 13, 43, 46]):
    """Test if key = f(word_start_position) for each word."""
    
    print("=" * 70)
    print("WORD-POSITION KEY TESTING")
    print("=" * 70)
    print("Testing: key = (word_start_position × mult + offset) mod 29")
    
    for page_num in pages:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words_with_positions(rune_text)
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} - {len(words)} words")
        print(f"{'='*70}")
        
        best_results = []
        
        for mult in [1, 3, 7, 8, 11, 13, 17, 22]:
            for offset in range(29):
                total_score = 0
                word_results = []
                
                for word in words:
                    # Key based on word start position
                    key = (word['start_pos'] * mult + offset) % 29
                    decrypted = decrypt_word(word['indices'], key)
                    text = indices_to_text(decrypted)
                    score = score_word(text)
                    total_score += score
                    
                    if score >= 100:  # Found a word
                        word_results.append((word['start_pos'], text, key))
                
                if total_score > 400:
                    best_results.append((mult, offset, total_score, word_results))
        
        best_results.sort(key=lambda x: x[2], reverse=True)
        
        print("\nTop 10 (mult, offset) combinations:")
        for mult, offset, score, word_results in best_results[:10]:
            print(f"  mult={mult:2d}, offset={offset:2d}: score={score:4d}")
            if word_results:
                words_found = ', '.join(f"{w[1]}@{w[0]}(key={w[2]})" for w in word_results[:5])
                print(f"    Words: {words_found}")

def test_word_index_key(pages=[8, 13, 43, 46]):
    """Test if key = f(word_index) not rune_position."""
    
    print("\n" + "=" * 70)
    print("WORD-INDEX KEY TESTING")
    print("=" * 70)
    print("Testing: key = (word_number × mult + offset) mod 29")
    
    for page_num in pages:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words_with_positions(rune_text)
        
        print(f"\nPage {page_num} ({len(words)} words):")
        
        best_results = []
        
        for mult in [1, 2, 3, 5, 7, 11, 13, 17, 19, 23]:
            for offset in range(29):
                total_score = 0
                word_results = []
                
                for word_idx, word in enumerate(words):
                    # Key based on word index (not position)
                    key = (word_idx * mult + offset) % 29
                    decrypted = decrypt_word(word['indices'], key)
                    text = indices_to_text(decrypted)
                    score = score_word(text)
                    total_score += score
                    
                    if score >= 100:
                        word_results.append((word_idx, text, key))
                
                if total_score > 400:
                    best_results.append((mult, offset, total_score, word_results))
        
        best_results.sort(key=lambda x: x[2], reverse=True)
        
        for mult, offset, score, word_results in best_results[:5]:
            print(f"  mult={mult:2d}, offset={offset:2d}: score={score:4d}")
            if word_results:
                words_found = ', '.join(f"{w[1]}#{w[0]}(k={w[2]})" for w in word_results[:5])
                print(f"    Words: {words_found}")

def test_cumulative_word_key(pages=[8, 13, 43, 46]):
    """Test if key accumulates based on word length or previous decryption."""
    
    print("\n" + "=" * 70)
    print("CUMULATIVE WORD KEY TESTING")
    print("=" * 70)
    
    for page_num in pages:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words_with_positions(rune_text)
        
        print(f"\nPage {page_num}:")
        
        best_results = []
        
        # Test: key = sum of previous word lengths mod 29
        for start_key in range(29):
            total_score = 0
            word_results = []
            cumulative = start_key
            
            for word_idx, word in enumerate(words):
                key = cumulative % 29
                decrypted = decrypt_word(word['indices'], key)
                text = indices_to_text(decrypted)
                score = score_word(text)
                total_score += score
                
                if score >= 100:
                    word_results.append((word_idx, text, key))
                
                # Accumulate word length
                cumulative += word['length']
            
            if total_score > 300:
                best_results.append(('cumlen', start_key, total_score, word_results))
        
        # Test: key = sum of previous word indices mod 29
        for start_key in range(29):
            total_score = 0
            word_results = []
            cumulative = start_key
            
            for word_idx, word in enumerate(words):
                key = cumulative % 29
                decrypted = decrypt_word(word['indices'], key)
                text = indices_to_text(decrypted)
                score = score_word(text)
                total_score += score
                
                if score >= 100:
                    word_results.append((word_idx, text, key))
                
                cumulative += sum(word['indices'])  # Sum of rune indices
            
            if total_score > 300:
                best_results.append(('cumidx', start_key, total_score, word_results))
        
        best_results.sort(key=lambda x: x[2], reverse=True)
        
        for method, start, score, word_results in best_results[:5]:
            print(f"  {method} start={start:2d}: score={score:4d}")
            if word_results:
                words_found = ', '.join(f"{w[1]}#{w[0]}" for w in word_results[:5])
                print(f"    Words: {words_found}")

def analyze_discovered_key_positions():
    """Analyze the relationship between discovered keys and word positions."""
    
    print("\n" + "=" * 70)
    print("DISCOVERED KEY POSITION ANALYSIS")
    print("=" * 70)
    
    # From word_boundary_solver.py results
    discoveries = {
        8: [
            (3, 12, 'PATH', 14),   # word_idx, rune_start, word, key
            (10, 40, 'THE', 1),
        ],
        13: [
            (5, 23, 'A', 2),
            (7, 28, 'A', 6),
            (11, 38, 'IN', 23),
            (13, 44, 'I', 8),
            (17, 58, 'DO', 9),
        ],
        43: [
            (6, 23, 'BE', 12),
            (12, 55, 'THY', 25),
            (17, 74, 'NO', 3),
        ],
        46: [
            (6, 22, 'I', 11),
            (10, 34, 'UP', 5),
            (17, 54, 'GO', 15),
            (19, 63, 'AN', 18),
            (20, 65, 'I', 12),
        ],
    }
    
    print("\nLooking for formula: key = f(word_idx, rune_start, page)")
    
    for page, disc_list in discoveries.items():
        print(f"\nPage {page}:")
        for word_idx, rune_start, word, key in disc_list:
            # Test various formulas
            f1 = (word_idx * 11) % 29
            f2 = (rune_start * 11) % 29
            f3 = (word_idx + rune_start) % 29
            f4 = (page + word_idx) % 29
            f5 = (page * word_idx) % 29
            f6 = (rune_start + page) % 29
            
            print(f"  {word:4} key={key:2d} | "
                  f"widx×11={f1:2d} | rs×11={f2:2d} | widx+rs={f3:2d} | "
                  f"p+widx={f4:2d} | p×widx={f5:2d} | rs+p={f6:2d}")

def search_for_key_formula():
    """Exhaustively search for a formula that fits discovered keys."""
    
    print("\n" + "=" * 70)
    print("EXHAUSTIVE KEY FORMULA SEARCH")
    print("=" * 70)
    
    discoveries = [
        (8, 3, 12, 14),   # (page, word_idx, rune_start, key)
        (8, 10, 40, 1),
        (13, 5, 23, 2),
        (13, 7, 28, 6),
        (13, 11, 38, 23),
        (13, 13, 44, 8),
        (13, 17, 58, 9),
        (43, 6, 23, 12),
        (43, 12, 55, 25),
        (43, 17, 74, 3),
        (46, 6, 22, 11),
        (46, 10, 34, 5),
        (46, 17, 54, 15),
        (46, 19, 63, 18),
        (46, 20, 65, 12),
    ]
    
    # Test: key = (a*page + b*widx + c*rstart + d) mod 29
    print("\nTesting: key = (a×page + b×word_idx + c×rune_start + d) mod 29")
    
    best_formulas = []
    
    for a in range(29):
        for b in range(29):
            for c in range(29):
                for d in range(29):
                    matches = 0
                    for page, widx, rstart, actual_key in discoveries:
                        predicted = (a*page + b*widx + c*rstart + d) % 29
                        if predicted == actual_key:
                            matches += 1
                    
                    if matches >= 5:  # At least 1/3 match
                        best_formulas.append((a, b, c, d, matches))
    
    best_formulas.sort(key=lambda x: x[4], reverse=True)
    
    print(f"\nTop formulas (out of {len(best_formulas)} with ≥5 matches):")
    for a, b, c, d, matches in best_formulas[:15]:
        print(f"  ({a}×p + {b}×w + {c}×r + {d}) mod 29: {matches}/15 matches")
        
        # Show which discoveries match
        matched = []
        for page, widx, rstart, actual_key in discoveries:
            predicted = (a*page + b*widx + c*rstart + d) % 29
            if predicted == actual_key:
                matched.append(f"p{page}")
        print(f"    Matched pages: {', '.join(matched)}")

if __name__ == '__main__':
    test_word_position_key()
    test_word_index_key()
    test_cumulative_word_key()
    analyze_discovered_key_positions()
    search_for_key_formula()

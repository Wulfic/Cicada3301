#!/usr/bin/env python3
"""
Word-Level Analysis - Looking for English patterns with proper digraph handling
Based on the insight that hyphens = word boundaries in the plaintext
"""

import os
import re
from collections import defaultdict

# Rune mappings
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                   'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
                   'A', 'AE', 'Y', 'IA', 'EA']

LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6,
    'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20,
    'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26,
    'IA': 27, 'IO': 27, 'EA': 28, 'V': 1, 'Q': 5, 'Z': 15
}

def text_to_indices(text):
    """Convert English text to indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        if text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
        i += 1
    return indices

def runes_to_indices(runes):
    """Convert Unicode runes to indices"""
    return [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]

def indices_to_letters(indices):
    """Convert indices to letter string"""
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

def read_rune_words(page_num):
    """Read rune file as words"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    words = re.split(r'[-\n]+', content)
    words = [w.strip() for w in words if w.strip()]
    return words

# Load English words (focus on short common words)
SHORT_WORDS = {
    # 1 rune = 1-2 letter words
    1: {'A', 'I', 'O', 'AN', 'AM', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 
        'IN', 'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 
        'US', 'WE', 'YE', 'TH', 'TH'},  # TH alone could be archaic "the"
    
    # 2 runes = 2-4 letter words  
    2: {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GOD', 'WAY', 'MAY', 'SAY',
        'THY', 'WHO', 'HOW', 'NOW', 'NEW', 'TWO', 'OLD', 'OWN', 'TOO', 'ANY',
        'MAN', 'HAS', 'HIM', 'HIS', 'LET', 'PUT', 'RUN', 'SEE', 'SHE', 'USE',
        'YEA', 'NAY', 'AYE'},
    
    # 3 runes = 3-6 letter words
    3: {'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
        'CALL', 'FIND', 'MANY', 'MOST', 'SOME', 'THAN', 'THEM', 'THEN', 'WHAT',
        'WHEN', 'EACH', 'SELF', 'PATH', 'MUST', 'LIKE', 'MAKE', 'ONLY', 'OVER',
        'SUCH', 'INTO', 'KNOW', 'JUST', 'COME', 'GOOD', 'ALSO', 'THOU', 'THEE',
        'UNTO', 'UPON', 'HATH', 'DOTH', 'SEEK', 'SOUL', 'MIND', 'BODY', 'TRUE',
        'WORD', 'LIFE', 'LOVE', 'FEAR', 'HOPE'},
}

# Digraph-aware single character count (some letters are 2 chars but 1 rune)
def count_effective_letters(text):
    """Count rune-equivalent characters in decoded text"""
    text = text.upper()
    count = 0
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'IO', 'EA']:
                count += 1
                i += 2
                continue
        count += 1
        i += 1
    return count

def test_all_shifts(page_num):
    """
    Test all possible single-value shifts (0-28) to see which produces 
    the most recognizable short words
    """
    words = read_rune_words(page_num)
    
    print(f"\n{'='*70}")
    print(f"Testing all shifts on Page {page_num}")
    print(f"{'='*70}")
    
    best_shift = 0
    best_score = 0
    best_matches = []
    
    for shift in range(29):
        matches = []
        for i, rune_word in enumerate(words):
            rune_indices = runes_to_indices(rune_word)
            if not rune_indices:
                continue
            
            # Apply simple shift
            decrypted = [(idx - shift) % 29 for idx in rune_indices]
            text = indices_to_letters(decrypted)
            
            rune_count = len(rune_indices)
            
            # Check if it's a known word
            if rune_count in SHORT_WORDS:
                if text in SHORT_WORDS[rune_count]:
                    matches.append((i, rune_count, text))
        
        if len(matches) > best_score:
            best_score = len(matches)
            best_shift = shift
            best_matches = matches
    
    print(f"\nBest shift: {best_shift} (letter '{INDEX_TO_LETTER[best_shift]}', prime {[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109][best_shift]})")
    print(f"Matches found: {best_score}")
    for pos, runes, word in best_matches:
        print(f"  Word {pos} ({runes} runes): {word}")
    
    return best_shift, best_matches

def test_two_character_keys(page_num):
    """
    Test all possible 2-character repeating keys
    """
    words = read_rune_words(page_num)
    
    print(f"\n{'='*70}")
    print(f"Testing all 2-char keys on Page {page_num}")
    print(f"{'='*70}")
    
    best_key = (0, 0)
    best_score = 0
    best_matches = []
    
    for k1 in range(29):
        for k2 in range(29):
            if k1 == k2:
                continue
            
            matches = []
            for i, rune_word in enumerate(words):
                rune_indices = runes_to_indices(rune_word)
                if not rune_indices:
                    continue
                
                key = [k1, k2]
                decrypted = [(idx - key[j % 2]) % 29 for j, idx in enumerate(rune_indices)]
                text = indices_to_letters(decrypted)
                
                rune_count = len(rune_indices)
                
                if rune_count in SHORT_WORDS:
                    if text in SHORT_WORDS[rune_count]:
                        matches.append((i, rune_count, text))
            
            if len(matches) > best_score:
                best_score = len(matches)
                best_key = (k1, k2)
                best_matches = matches
    
    print(f"\nBest 2-char key: [{best_key[0]}, {best_key[1]}] = [{INDEX_TO_LETTER[best_key[0]]}, {INDEX_TO_LETTER[best_key[1]]}]")
    print(f"Matches found: {best_score}")
    for pos, runes, word in best_matches:
        print(f"  Word {pos} ({runes} runes): {word}")
    
    return best_key, best_matches

def show_full_decryption(page_num, key_indices):
    """Show full decryption with a given key"""
    words = read_rune_words(page_num)
    
    key_str = ''.join(INDEX_TO_LETTER[k] for k in key_indices)
    print(f"\n{'='*70}")
    print(f"Full decryption of Page {page_num} with key [{key_str}]")
    print(f"{'='*70}\n")
    
    all_words = []
    for i, rune_word in enumerate(words):
        rune_indices = runes_to_indices(rune_word)
        if not rune_indices:
            all_words.append(f"[?:{rune_word}]")
            continue
        
        # Word-boundary mode: key resets for each word
        decrypted = [(idx - key_indices[j % len(key_indices)]) % 29 
                     for j, idx in enumerate(rune_indices)]
        text = indices_to_letters(decrypted)
        all_words.append(text)
    
    # Print as flowing text
    print(' '.join(all_words))
    print()
    
    # Also print with positions
    print("With positions:")
    for i, word in enumerate(all_words):
        print(f"  {i:2d}. {word}")

def main():
    # Test single shifts
    test_all_shifts(0)
    test_all_shifts(2)
    
    # Test 2-char keys (like IP)
    test_two_character_keys(0)
    test_two_character_keys(2)
    
    # Show the IP key decryption
    show_full_decryption(0, [10, 13])  # IP
    show_full_decryption(2, [10, 13])  # IP

if __name__ == '__main__':
    main()

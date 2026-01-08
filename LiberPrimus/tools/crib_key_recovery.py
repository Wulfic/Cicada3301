#!/usr/bin/env python3
"""
CRIB-BASED KEY RECOVERY

Using the English words we've identified (THE, PATH, WITH, etc.) at specific positions,
work backwards to derive what the key MUST be.

If word W at position P decrypts to English word E, then:
key = cipher - plain (mod 29)

This gives us key fragments we can analyze for patterns.
"""

import os
from pathlib import Path
from collections import Counter, defaultdict

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

# Common English words and their indices
COMMON_WORDS = {
    'THE': [16, 8, 18],
    'AND': [24, 9, 23],
    'FOR': [0, 3, 4],
    'WITH': [7, 10, 16, 8],
    'THAT': [16, 8, 24, 16],
    'THIS': [16, 8, 10, 15],
    'FROM': [0, 4, 3, 19],
    'HAVE': [8, 24, 1, 18],
    'BEEN': [17, 18, 18, 9],
    'WILL': [7, 10, 20, 20],
    'PATH': [13, 24, 16, 8],
    'FIND': [0, 10, 9, 23],
    'SEEK': [15, 18, 18, 5],
    'TRUTH': [16, 4, 1, 16, 8],
    'LIGHT': [20, 10, 6, 8, 16],
    'A': [24],
    'I': [10],
    'IN': [10, 9],
    'OF': [3, 0],
    'TO': [16, 3],
    'BE': [17, 18],
    'IS': [10, 15],
    'IT': [10, 16],
    'AS': [24, 15],
    'AT': [24, 16],
    'BY': [17, 26],
    'WE': [7, 18],
    'OR': [3, 4],
    'SO': [15, 3],
    'NO': [9, 3],
    'MY': [19, 26],
    'HE': [8, 18],
    'ME': [19, 18],
    'UP': [1, 13],
    'IF': [10, 0],
    'DO': [23, 3],
    'GO': [6, 3],
    'AN': [24, 9],
    'US': [1, 15],
    'THY': [16, 8, 26],
    'YEA': [26, 18, 24],
    'NAY': [9, 24, 26],
    'NOT': [9, 3, 16],
    'BUT': [17, 1, 16],
    'ALL': [24, 20, 20],
    'OUR': [3, 1, 4],
    'OWN': [3, 7, 9],
    'WHO': [7, 8, 3],
    'WAY': [7, 24, 26],
    'OUT': [3, 1, 16],
    'NOW': [9, 3, 7],
    'OLD': [3, 20, 23],
    'NEW': [9, 18, 7],
    'ONE': [3, 9, 18],
    'TWO': [16, 7, 3],
    'YET': [26, 18, 16],
    'SAY': [15, 24, 26],
    'HIS': [8, 10, 15],
    'HER': [8, 18, 4],
    'HATH': [8, 24, 16, 8],
    'DOTH': [23, 3, 16, 8],
    'THOU': [16, 8, 3, 1],
    'THEE': [16, 8, 18, 18],
    'THEM': [16, 8, 18, 19],
    'THEN': [16, 8, 18, 9],
    'THAN': [16, 8, 24, 9],
    'EACH': [18, 24, 5, 8],
    'BOTH': [17, 3, 16, 8],
    'THUS': [16, 8, 1, 15],
}

def load_runes(page_num):
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_words_with_positions(rune_text):
    """Parse rune text into words with their positions."""
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

def find_matching_words(cipher_word):
    """Find English words that match the length of cipher_word."""
    length = len(cipher_word)
    matching = []
    
    for word, indices in COMMON_WORDS.items():
        if len(indices) == length:
            matching.append((word, indices))
    
    return matching

def derive_key(cipher_indices, plain_indices):
    """Derive key from cipher and plaintext."""
    return [(c - p) % 29 for c, p in zip(cipher_indices, plain_indices)]

def analyze_page_cribs(page_num):
    """Analyze a page using crib-based key recovery."""
    
    print(f"\n{'='*70}")
    print(f"CRIB-BASED KEY RECOVERY: PAGE {page_num}")
    print("=" * 70)
    
    rune_text = load_runes(page_num)
    if not rune_text:
        print("Could not load page")
        return
    
    words = parse_words_with_positions(rune_text)
    print(f"Total words: {len(words)}")
    
    # For each word, find possible English matches and derive keys
    all_cribs = []
    
    for word_idx, word in enumerate(words):
        cipher = word['indices']
        start_pos = word['start_pos']
        matching = find_matching_words(cipher)
        
        for eng_word, plain_indices in matching:
            key = derive_key(cipher, plain_indices)
            all_cribs.append({
                'word_idx': word_idx,
                'start_pos': start_pos,
                'cipher': indices_to_text(cipher),
                'plain': eng_word,
                'key': key
            })
    
    print(f"\nPossible cribs found: {len(all_cribs)}")
    
    # Analyze key patterns
    # Group cribs by word position to see if keys follow a pattern
    print("\n" + "-" * 50)
    print("KEY ANALYSIS (if key = position*mult + offset)")
    print("-" * 50)
    
    # For single-rune words
    single_rune_cribs = [c for c in all_cribs if len(c['key']) == 1]
    print(f"\nSingle-rune cribs: {len(single_rune_cribs)}")
    
    for c in single_rune_cribs[:20]:
        print(f"  word_idx={c['word_idx']:2d}, pos={c['start_pos']:3d}, "
              f"cipher={c['cipher']}, plain={c['plain']}, key={c['key'][0]}")
    
    # Check if key = some function of position
    print("\n" + "-" * 50)
    print("CHECKING: key = (pos * mult + offset) mod 29")
    print("-" * 50)
    
    for mult in range(1, 29):
        for offset in range(29):
            matches = 0
            for c in single_rune_cribs:
                expected_key = (c['start_pos'] * mult + offset) % 29
                if expected_key == c['key'][0]:
                    matches += 1
            
            match_rate = matches / len(single_rune_cribs) if single_rune_cribs else 0
            if match_rate > 0.15:  # If more than 15% match
                print(f"mult={mult:2d}, offset={offset:2d}: {matches}/{len(single_rune_cribs)} "
                      f"= {match_rate:.1%}")
    
    # Check if key = some function of word_idx
    print("\n" + "-" * 50)
    print("CHECKING: key = (word_idx * mult + offset) mod 29")
    print("-" * 50)
    
    for mult in range(1, 29):
        for offset in range(29):
            matches = 0
            for c in single_rune_cribs:
                expected_key = (c['word_idx'] * mult + offset) % 29
                if expected_key == c['key'][0]:
                    matches += 1
            
            match_rate = matches / len(single_rune_cribs) if single_rune_cribs else 0
            if match_rate > 0.15:
                print(f"mult={mult:2d}, offset={offset:2d}: {matches}/{len(single_rune_cribs)} "
                      f"= {match_rate:.1%}")
    
    # Show most common key values for position analysis
    print("\n" + "-" * 50)
    print("KEY VALUE DISTRIBUTION")
    print("-" * 50)
    
    key_values = defaultdict(list)
    for c in single_rune_cribs:
        key_values[c['key'][0]].append(c['start_pos'])
    
    for key_val in sorted(key_values.keys()):
        positions = key_values[key_val]
        if len(positions) >= 2:
            diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            print(f"key={key_val:2d}: positions={positions[:8]}, diffs={diffs[:5]}")

def main():
    for page_num in [8, 9, 10, 43, 45, 51]:
        analyze_page_cribs(page_num)

if __name__ == '__main__':
    main()

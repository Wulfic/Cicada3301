#!/usr/bin/env python3
"""
WORD BOUNDARY AWARE DECRYPTION
==============================

Key Insight: The hyphens (-) between runes in the original text likely correspond
to actual word boundaries in the decrypted English text!

This means:
1. Each hyphen-separated group of runes = one English word
2. We should decrypt while preserving these boundaries
3. The resulting words should be recognizable English
"""

import os
import re
from collections import Counter

# ============================================================================
# GEMATRIA PRIMUS MAPPING
# ============================================================================

RUNE_DATA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101), 'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107), 'ᛠ': (28, 'EA', 109)
}

RUNE_TO_INDEX = {k: v[0] for k, v in RUNE_DATA.items()}
INDEX_TO_LETTER = {v[0]: v[1] for k, v in RUNE_DATA.items()}
LETTERS = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
           "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"]
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}

# Key lengths for first-layer decryption
KEY_LENGTHS = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

# ============================================================================
# FUNCTIONS
# ============================================================================

def runes_to_indices(rune_str):
    """Convert runes to list of indices"""
    return [RUNE_TO_INDEX[r] for r in rune_str if r in RUNE_TO_INDEX]

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(INDEX_TO_LETTER.get(i, '?') for i in indices)

def text_to_indices(text):
    """Convert text back to indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        matched = False
        for length in [2, 1]:
            if i + length <= len(text):
                segment = text[i:i+length]
                if segment in LETTER_TO_INDEX:
                    indices.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return indices

def apply_first_layer(indices, key_length, global_position=0):
    """Apply first-layer SUB mod 29 decryption"""
    result = []
    for i, idx in enumerate(indices):
        pos = global_position + i
        shift = pos % key_length
        new_idx = (idx - shift) % 29
        result.append(new_idx)
    return result

def apply_vigenere(indices, key_indices, operation='add', global_position=0):
    """Apply Vigenère cipher"""
    result = []
    for i, idx in enumerate(indices):
        pos = global_position + i
        k = key_indices[pos % len(key_indices)]
        if operation == 'add':
            new_idx = (idx + k) % 29
        else:  # sub
            new_idx = (idx - k) % 29
        result.append(new_idx)
    return result

def parse_rune_file(filepath):
    """Parse rune file preserving word boundaries and structure"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines first
    lines = content.strip().split('\n')
    
    # Each line contains words separated by hyphens
    # Also handle sentence markers (.) and section markers (&, $)
    all_words = []
    current_pos = 0
    
    for line in lines:
        # Split by hyphens while preserving other markers
        parts = re.split(r'(-|\.|\&|\$|/)', line)
        
        for part in parts:
            if part in ['-', '.', '&', '$', '/']:
                all_words.append({'type': 'marker', 'text': part, 'pos': current_pos})
            elif part.strip():
                # This is a word (sequence of runes)
                runes = [c for c in part if c in RUNE_TO_INDEX]
                if runes:
                    all_words.append({
                        'type': 'word',
                        'runes': ''.join(runes),
                        'indices': runes_to_indices(''.join(runes)),
                        'start_pos': current_pos,
                        'length': len(runes)
                    })
                    current_pos += len(runes)
    
    return all_words

def decrypt_with_word_boundaries(words, key_length, second_key=None, second_op='add'):
    """Decrypt preserving word boundaries"""
    result_words = []
    global_pos = 0
    
    for item in words:
        if item['type'] == 'marker':
            result_words.append({'type': 'marker', 'text': item['text']})
        else:
            indices = item['indices']
            
            # First layer: SUB with position-based key
            first_layer = apply_first_layer(indices, key_length, global_pos)
            
            # Second layer if provided
            if second_key:
                decrypted = apply_vigenere(first_layer, second_key, second_op, global_pos)
            else:
                decrypted = first_layer
            
            text = indices_to_text(decrypted)
            result_words.append({
                'type': 'word',
                'text': text,
                'indices': decrypted,
                'original_runes': item['runes']
            })
            
            global_pos += len(indices)
    
    return result_words

def format_output(words):
    """Format decrypted words into readable text"""
    result = []
    for item in words:
        if item['type'] == 'marker':
            if item['text'] == '-':
                result.append(' ')
            elif item['text'] == '.':
                result.append('. ')
            elif item['text'] == '&':
                result.append('\n[SECTION]\n')
            elif item['text'] == '/':
                result.append('\n')
            else:
                result.append(item['text'])
        else:
            result.append(item['text'])
    return ''.join(result)

def analyze_words(words):
    """Analyze decrypted words"""
    word_list = [item['text'] for item in words if item['type'] == 'word']
    
    # Common English words to check
    english_words = {
        'THE', 'A', 'AN', 'AND', 'OR', 'OF', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'AT',
        'BY', 'FOR', 'ON', 'WITH', 'HE', 'SHE', 'WE', 'YOU', 'THEY', 'THIS', 'THAT',
        'WILL', 'WOULD', 'COULD', 'SHOULD', 'HAVE', 'HAS', 'HAD', 'DO', 'DOES', 'DID',
        'FIND', 'SEEK', 'KNOW', 'WISDOM', 'TRUTH', 'PATH', 'WAY', 'ALL', 'ONE', 'SELF',
        'THOU', 'THEE', 'THY', 'THINE', 'HATH', 'DOTH', 'GOETH', 'DOETH', 'WITHIN',
        'DIVINITY', 'DIVINE', 'SACRED', 'HOLY', 'BEING', 'THING', 'NOTHING', 'SOMETHING'
    }
    
    matches = [w for w in word_list if w in english_words]
    
    print(f"\nWord count: {len(word_list)}")
    print(f"English matches: {len(matches)} ({100*len(matches)/len(word_list):.1f}%)")
    print(f"Matched words: {matches[:20]}...")
    
    # Show word length distribution
    lengths = Counter(len(w) for w in word_list)
    print(f"Word length distribution: {dict(sorted(lengths.items()))}")
    
    return word_list

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("WORD BOUNDARY AWARE DECRYPTION")
    print("=" * 70)
    
    # Test keys
    IP_KEY = [10, 13]  # I, P indices
    PI_KEY = [13, 10]  # P, I indices
    FIND_KEY = text_to_indices("FIND")  # F=0, I=10, N=9, D=23
    
    print(f"\nIP key: {IP_KEY}")
    print(f"PI key: {PI_KEY}")
    print(f"FIND key: {FIND_KEY}")
    
    for page_num in range(5):
        rune_path = os.path.join(base_path, '..', 'pages', f'page_{page_num:02d}', 'runes.txt')
        if not os.path.exists(rune_path):
            continue
            
        key_length = KEY_LENGTHS[page_num]
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} (key length: {key_length})")
        print("=" * 70)
        
        # Parse preserving word boundaries
        words = parse_rune_file(rune_path)
        word_count = sum(1 for w in words if w['type'] == 'word')
        print(f"Found {word_count} words separated by boundaries")
        
        # Test 1: First layer only
        print("\n--- FIRST LAYER ONLY ---")
        decrypted = decrypt_with_word_boundaries(words, key_length)
        output = format_output(decrypted)
        print(output[:300])
        analyze_words(decrypted)
        
        # Test 2: First layer + IP key (for pages 2-3)
        if page_num in [2, 3]:
            print("\n--- FIRST LAYER + IP (add) ---")
            decrypted = decrypt_with_word_boundaries(words, key_length, IP_KEY, 'add')
            output = format_output(decrypted)
            print(output[:300])
            analyze_words(decrypted)
        
        # Test 3: First layer + PI key (for page 4)
        if page_num == 4:
            print("\n--- FIRST LAYER + PI (add) ---")
            decrypted = decrypt_with_word_boundaries(words, key_length, PI_KEY, 'add')
            output = format_output(decrypted)
            print(output[:300])
            analyze_words(decrypted)
        
        # Test 4: First layer + FIND key (for pages 0-1)
        if page_num in [0, 1]:
            print("\n--- FIRST LAYER + FIND (sub) ---")
            decrypted = decrypt_with_word_boundaries(words, key_length, FIND_KEY, 'sub')
            output = format_output(decrypted)
            print(output[:300])
            analyze_words(decrypted)
        
        # Show individual words for first 20
        print("\n--- FIRST 20 WORDS (first layer only) ---")
        decrypted = decrypt_with_word_boundaries(words, key_length)
        word_items = [w for w in decrypted if w['type'] == 'word'][:20]
        for i, w in enumerate(word_items):
            print(f"{i+1:2d}. {w['text']:15s} (len={len(w['original_runes'])})")

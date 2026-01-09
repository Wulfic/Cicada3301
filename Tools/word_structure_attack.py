#!/usr/bin/env python3
"""
Word Structure Attack - Use word boundaries to constrain solutions

Key insight: Hyphens = word boundaries, preserved through encryption.
A 3-rune cipher word MUST decrypt to a 3-rune plaintext word.

Rune count -> Letter count mapping (considering digraphs TH, EO, NG, OE, AE, IA, EA):
- 1 rune = 1-2 letters (A, I, TH, EO, etc.)
- 2 runes = 2-4 letters (THE, AND, TO, etc.)
- 3 runes = 3-6 letters (THAT, WITH, etc.)
"""

import os
import re
from collections import defaultdict

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
    """Convert English text to Gematria Primus indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        # Single letter
        if text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
        i += 1
    return indices

def runes_to_indices(runes):
    """Convert Unicode runes to indices"""
    return [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]

def indices_to_text(indices):
    """Convert indices to text"""
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

def build_word_database():
    """Build database of English words indexed by rune count"""
    
    # Extended word list focusing on Cicada-relevant vocabulary
    all_words = """
    A I O AN AM AS AT BE BY DO GO HE IF IN IS IT ME MY NO OF ON OR SO TO UP US WE YE
    THE AND FOR ARE BUT NOT YOU ALL CAN HAD HER WAS ONE OUR OUT DAY GOD WAY MAY SAY
    THY WHO HOW NOW NEW TWO OLD OWN TOO ANY MAN HAS HIM HIS LET PUT RUN SEE SHE USE
    THAT WITH HAVE THIS WILL YOUR FROM THEY BEEN CALL FIND MANY MOST SOME THAN THEM
    THEN WHAT WHEN EACH SELF PATH MUST LIKE MAKE ONLY OVER SUCH INTO KNOW JUST COME
    GOOD ALSO THOU THEE UNTO UPON HATH DOTH SEEK SOUL MIND BODY TRUE WORD LIFE LOVE
    THEIR WHICH THERE THESE WOULD ABOUT COULD OTHER BEING TRUTH THING WORLD GREAT
    FIRST AFTER THOSE NEVER WHERE EVERY SHALL UNDER WISDOM DIVINE SACRED SPIRIT
    WITHIN EMERGE INSTAR SEEKER CIPHER SECRET HIDDEN PRIMUS LIBER THINGS TOWARD
    WELCOME PILGRIM JOURNEY DIVINITY COMMAND INSTRUCTION CIRCUMFERENCE KNOWLEDGE
    AETHEREAL CARNAL SHADOWS REALITY OUTSIDE TOTIENT MOBIUS CONSUME
    UNDERSTAND OURSELVES ENCRYPTION ENCRYPTED DECRYPT DECRYPTED FOLLOWING BECOMING
    """.split()
    
    db = defaultdict(list)
    for word in all_words:
        indices = text_to_indices(word)
        rune_count = len(indices)
        if 1 <= rune_count <= 15:
            db[rune_count].append((word, indices))
    
    return db

def find_shift_for_word(cipher_indices, target_word):
    """
    Find if there's a consistent shift that transforms cipher_indices to target_word
    Returns the shift if found, or None if no consistent shift exists
    """
    target_indices = text_to_indices(target_word)
    if len(cipher_indices) != len(target_indices):
        return None
    
    # Calculate required shift for first position
    shift = (cipher_indices[0] - target_indices[0]) % 29
    
    # Check if this shift works for all positions
    for c, t in zip(cipher_indices, target_indices):
        if (c - shift) % 29 != t:
            return None
    
    return shift

def analyze_page_with_constraints(page_num):
    """
    Analyze a page using word structure constraints
    For each cipher word, find all possible English words it could decrypt to
    """
    words = read_rune_words(page_num)
    db = build_word_database()
    
    print(f"\n{'='*70}")
    print(f"WORD STRUCTURE ANALYSIS - Page {page_num}")
    print(f"{'='*70}")
    print(f"Total words in page: {len(words)}")
    
    # Analyze each word position
    candidates_by_position = []
    
    for i, rune_word in enumerate(words[:30]):  # First 30 words
        rune_indices = runes_to_indices(rune_word)
        if not rune_indices:
            candidates_by_position.append([])
            continue
        
        rune_count = len(rune_indices)
        possible_words = db.get(rune_count, [])
        
        # For each possible English word, calculate the shift needed
        valid_candidates = []
        for word, word_indices in possible_words:
            shift = find_shift_for_word(rune_indices, word)
            if shift is not None:
                valid_candidates.append((word, shift))
        
        candidates_by_position.append(valid_candidates)
        
        # Print top candidates
        if valid_candidates:
            top_5 = valid_candidates[:5]
            words_str = ', '.join(f"{w}(shift={s})" for w, s in top_5)
            print(f"Word {i:2d} ({rune_count} runes): {words_str}")
        else:
            plain = indices_to_text(rune_indices)
            print(f"Word {i:2d} ({rune_count} runes): [no matches] raw={plain}")
    
    return candidates_by_position

def find_common_shifts(page_num):
    """
    Find which shift values appear most frequently across all words
    If a single shift works for many words, it might be the correct one
    """
    words = read_rune_words(page_num)
    db = build_word_database()
    
    print(f"\n{'='*70}")
    print(f"SHIFT FREQUENCY ANALYSIS - Page {page_num}")
    print(f"{'='*70}")
    
    shift_counts = defaultdict(list)  # shift -> list of (position, word) pairs
    
    for i, rune_word in enumerate(words):
        rune_indices = runes_to_indices(rune_word)
        if not rune_indices:
            continue
        
        rune_count = len(rune_indices)
        possible_words = db.get(rune_count, [])
        
        for word, word_indices in possible_words:
            shift = find_shift_for_word(rune_indices, word)
            if shift is not None:
                shift_counts[shift].append((i, word))
    
    # Sort shifts by how many words they work for
    sorted_shifts = sorted(shift_counts.items(), key=lambda x: -len(x[1]))
    
    print("\nMost common shifts (shift -> count of words it produces):")
    for shift, word_list in sorted_shifts[:15]:
        letter = INDEX_TO_LETTER[shift]
        print(f"  Shift {shift:2d} ({letter:>2s}): {len(word_list)} words")
        if len(word_list) <= 10:
            print(f"         Words: {', '.join(w for _, w in word_list)}")
    
    return sorted_shifts

def test_caesar_shift(page_num, shift):
    """Apply a single Caesar shift to all words in a page"""
    words = read_rune_words(page_num)
    
    print(f"\n{'='*70}")
    print(f"Page {page_num} with Caesar shift {shift} (letter {INDEX_TO_LETTER[shift]})")
    print(f"{'='*70}")
    
    all_decrypted = []
    for rune_word in words:
        rune_indices = runes_to_indices(rune_word)
        if not rune_indices:
            all_decrypted.append("?")
            continue
        
        decrypted = [(idx - shift) % 29 for idx in rune_indices]
        text = indices_to_text(decrypted)
        all_decrypted.append(text)
    
    print(' '.join(all_decrypted))
    return all_decrypted

def main():
    # Analyze Pages 0-4
    for page_num in [0, 2]:
        analyze_page_with_constraints(page_num)
        find_common_shifts(page_num)
    
    # Test the most promising shifts
    print("\n\nTesting most common shifts:")
    for page_num in [0, 2]:
        # Get the most common shift for this page
        sorted_shifts = find_common_shifts(page_num)
        if sorted_shifts:
            best_shift = sorted_shifts[0][0]
            test_caesar_shift(page_num, best_shift)

if __name__ == '__main__':
    main()

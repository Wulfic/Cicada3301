#!/usr/bin/env python3
"""
DEEP PARABLE WORD ANALYSIS

"Its words are the map, their meaning is the road, and their NUMBERS are the direction."

What if "numbers" means:
1. Word positions (1st word, 2nd word, etc.)
2. Letter counts per word
3. Cumulative position

Let's build a complete word-by-word analysis.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def letter_to_idx(letter):
    """Convert English letter(s) to rune index"""
    letter = letter.upper()
    mapping = {
        'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
        'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
        'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
        'Y': 26, 'Z': 15
    }
    return mapping.get(letter, -1)

def word_gematria(word):
    """Calculate Gematria value of a word"""
    total = 0
    for char in word.upper():
        idx = letter_to_idx(char)
        if idx >= 0:
            total += PRIMES[idx]
    return total

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

# The Parable as spoken
PARABLE_SPOKEN = """PARABLE LIKE THE INSTAR TUNNELING TO THE SURFACE WE MUST SHED 
OUR OWN CIRCUMFERENCES FIND THE DIVINITY WITHIN AND EMERGE"""

# The Parable as encoded (different - "LICE" not "LIKE", no spaces)
PARABLE_ENCODED = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

def main():
    pages = load_pages()
    
    # Parse the Parable into words
    words = PARABLE_SPOKEN.replace('\n', ' ').split()
    
    print("=" * 80)
    print("PARABLE WORD ANALYSIS")
    print("=" * 80)
    
    print(f"\n{'#':>2} {'Word':<15} {'Len':>3} {'Start':>5} {'Gem':>5} {'Gem%95':>6} {'Gem%29':>6}")
    print("-" * 60)
    
    cumulative_pos = 0
    for i, word in enumerate(words, 1):
        gem = word_gematria(word)
        start_pos = cumulative_pos
        print(f"{i:2} {word:<15} {len(word):3} {start_pos:5} {gem:5} {gem % 95:6} {gem % 29:6}")
        cumulative_pos += len(word)
    
    print(f"\nTotal: {len(words)} words, {cumulative_pos} letters")
    
    print("\n" + "=" * 80)
    print("TESTING: WORD POSITION AS KEY OFFSET FOR CORRESPONDING PAGE")
    print("=" * 80)
    
    # Theory: Page N uses offset = position of word N in the Parable
    # Or: Page N uses the Gematria of word N as offset
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    def decrypt_with_offset(cipher_indices, offset):
        result = []
        for i, c in enumerate(cipher_indices):
            k = MASTER_KEY[(i + offset) % 95]
            p = (c - k) % 29
            result.append(idx_to_letter(p))
        return ''.join(result)
    
    def word_score(text):
        WORDS = {'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
                 'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
                 'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
                 'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
                 'YOU', 'WE', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
                 'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
                 'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR',
                 'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN'}
        score = 0
        for word in WORDS:
            count = text.count(word)
            if count > 0:
                score += count * len(word)
        return score
    
    print("\nTheory 1: Page number = word index, use word's Gematria mod 95 as offset")
    for pg_num in unsolved:
        if pg_num < len(words):
            word = words[pg_num]
            gem = word_gematria(word)
            offset = gem % 95
            
            cipher = [rune_to_idx(r) for r in pages[pg_num]]
            text = decrypt_with_offset(cipher, offset)
            score = word_score(text)
            
            print(f"Page {pg_num}: word='{word}' (gem={gem}, offset={offset}), score={score}")
            if score >= 20:
                print(f"  {text[:60]}...")
    
    print("\nTheory 2: Page number - 20 = word index (since pages 27-31 might map to words 7-11)")
    # Words 7-11 are: SHED (actually position 7 is HAVE), etc.
    # Let me recalculate with 0-indexing
    
    for pg_num in unsolved:
        word_idx = pg_num - 20  # Hypothesis: Page 27 = word 7
        if 0 <= word_idx < len(words):
            word = words[word_idx]
            gem = word_gematria(word)
            offset = gem % 95
            
            cipher = [rune_to_idx(r) for r in pages[pg_num]]
            text = decrypt_with_offset(cipher, offset)
            score = word_score(text)
            
            print(f"Page {pg_num} -> word {word_idx}='{word}' (gem={gem}, offset={offset}), score={score}")
            if score >= 20:
                print(f"  {text[:60]}...")
    
    print("\n" + "=" * 80)
    print("THE ACTUAL ENCODED PARABLE (from Page 57)")
    print("=" * 80)
    
    # The encoded version might be different - let's parse it
    page57 = pages[57]
    page57_indices = [rune_to_idx(r) for r in page57]
    page57_text = ''.join(idx_to_letter(idx) for idx in page57_indices)
    print(f"Encoded text: {page57_text}")
    print(f"Length: {len(page57_text)}")
    
    # Analyze the actual encoded text structure
    print("\nKey positions in encoded Parable:")
    words_in_encoded = ['PARABLE', 'LICE', 'THE', 'INSTAR', 'TUNNE', 'LNG', 'TO', 'THE', 'SURFACE',
                        'WE', 'MUST', 'SHED', 'OUR', 'OWN', 'CIRCUMFERENCES', 'FIND', 'THE', 
                        'DIUINITY', 'WITHIN', 'AND', 'EMERGE']
    
    pos = 0
    for i, word in enumerate(words_in_encoded):
        idx = page57_text.find(word, pos)
        if idx >= 0:
            print(f"{i:2}: '{word}' at position {idx}")
            pos = idx + len(word)
    
    print("\n" + "=" * 80)
    print("THEORY: USE CUMULATIVE WORD POSITIONS")
    print("=" * 80)
    
    # Build cumulative positions based on actual encoded text
    word_positions = {
        'PARABLE': 0,
        'LICE': 7,      # PARABLE(7)
        'THE': 11,      # +4
        'INSTAR': 14,   # +3
        # etc.
    }
    
    # Calculate positions from encoded text
    encoded_words = []
    current_word = ""
    for i, char in enumerate(page57_text):
        if char in ['L', 'T', 'S', 'W', 'O', 'C', 'F', 'D', 'A', 'E']:
            # Check for word boundaries (this is imprecise)
            pass
        current_word += char
    
    # Let's try a different approach - use the first 95 positions as key indices
    print("\nTrying: Offset = Page number's Gematria mod 95")
    
    # Page number itself has a Gematria interpretation if we think of digits
    for pg_num in unsolved:
        # Convert page number to string and calculate gematria
        pg_str = str(pg_num)
        # Map digits: 0-9 to positions or just use the number directly
        offset = pg_num % 95
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        text = decrypt_with_offset(cipher, offset)
        score = word_score(text)
        
        if score >= 20:
            print(f"Page {pg_num}: offset={offset}, score={score}")
            print(f"  {text[:60]}...")

if __name__ == "__main__":
    main()

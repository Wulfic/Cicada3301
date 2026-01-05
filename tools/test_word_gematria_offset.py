#!/usr/bin/env python3
"""
TEST WORD GEMATRIA AS OFFSET

Hypothesis: Each page's offset is determined by the Gematria value 
of a word from the Parable (modulo 95).

The 2016 clue says "their NUMBERS are the direction" - 
Gematria gives us numbers from words!
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Gematria Primus values
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

# English to rune conversion for gematria
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

# All words from the Parable
PARABLE_WORDS = [
    "PARABLE", "AN", "INSTAR", "EMERGENCE", "LIKE", "THE", "OTHERS", "HAVE",
    "SHED", "MY", "SKIN", "MANY", "TIMES", "BEFORE", "WISDOMS", "BODY", "IS",
    "COVERED", "WITH", "EYES", "SOME", "OF", "WHICH", "ARE", "DEAD", "THOUGH",
    "THEY", "STILL", "SEE", "AND", "THERE", "SOME", "THAT", "REMAIN", "AWAKE",
    "THERE", "COME", "A", "TIME", "WHEN", "ONE", "MUST", "ABANDON", "THE",
    "IDEA", "OF", "SELF", "THE", "SURFACE", "WE", "MUST", "SHED", "OUR",
    "EGOS", "AND", "THEN", "BE", "REBORN", "UNTO", "THE", "DIVINE", "WITHIN",
    "OURSELVES", "COMMAND"
]

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
             'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def main():
    print("=" * 70)
    print("WORD GEMATRIA VALUES FROM PARABLE")
    print("=" * 70)
    
    word_gemvalues = []
    for i, word in enumerate(PARABLE_WORDS):
        gem = word_gematria(word)
        mod95 = gem % 95
        word_gemvalues.append((i, word, gem, mod95))
        print(f"{i:2}: {word:12} = {gem:4} (mod 95 = {mod95:2})")
    
    print("\n" + "=" * 70)
    print("TESTING: DOES WORD GEMATRIA MOD 95 = BEST OFFSET?")
    print("=" * 70)
    
    # Best offsets from previous analysis
    best_offsets = {
        27: 59, 28: 13, 29: 91, 30: 1, 31: 9,
        40: 81, 41: 49, 44: 23, 45: 50, 46: 56,
        47: 67, 48: 12, 52: 72
    }
    
    pages = load_pages()
    
    for pg_num, expected_offset in sorted(best_offsets.items()):
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Find which word's gematria mod 95 matches the best offset
        matches = []
        for i, word, gem, mod95 in word_gemvalues:
            if mod95 == expected_offset:
                matches.append(f"word {i}: '{word}' (gem={gem})")
        
        match_str = ", ".join(matches) if matches else "NO MATCH"
        print(f"Page {pg_num}: offset={expected_offset} -> {match_str}")
    
    print("\n" + "=" * 70)
    print("ALTERNATIVE: TEST ALL WORD GEMATRIA VALUES AS OFFSETS")
    print("=" * 70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_word = None
        best_text = ""
        
        for i, word in enumerate(PARABLE_WORDS):
            gem = word_gematria(word)
            offset = gem % 95
            
            text = decrypt_with_offset(cipher, offset)
            score = word_score(text)
            
            if score > best_score:
                best_score = score
                best_word = (i, word, gem, offset)
                best_text = text[:80]
        
        if best_word:
            i, word, gem, offset = best_word
            print(f"Page {pg_num}: Best word={word} (#{i}, gem={gem}, offset={offset}), score={best_score}")
            print(f"  Text: {best_text}...")
    
    print("\n" + "=" * 70)
    print("SPECIAL TEST: USE PAGE NUMBER AS WORD INDEX")
    print("=" * 70)
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Try using word at index (pg_num - some_constant)
        for const in range(0, 40):
            word_idx = (pg_num - const) % len(PARABLE_WORDS)
            word = PARABLE_WORDS[word_idx]
            gem = word_gematria(word)
            offset = gem % 95
            
            text = decrypt_with_offset(cipher, offset)
            score = word_score(text)
            
            if score >= 20:  # Decent threshold
                print(f"Page {pg_num}: word_idx={word_idx} (pg-{const}), word='{word}', gem={gem}, offset={offset}, score={score}")
                print(f"  {text[:60]}...")

if __name__ == "__main__":
    main()

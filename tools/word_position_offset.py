#!/usr/bin/env python3
"""
WORD POSITION AS OFFSET

In the encoded Parable:
- Word 9 "WE" is at position 40
- Word 10 "MUST" is at position 42
- Word 11 "SHED" is at position 46
- Word 12 "OUR" is at position 50

What if Page N uses offset = position of word (N - some_constant) in the Parable?

Let's find the constant that works best.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# Word positions in the encoded Parable (from previous analysis)
WORD_POSITIONS = {
    0: ('PARABLE', 0),
    1: ('LICE', 7),
    2: ('THE', 11),
    3: ('INSTAR', 14),
    4: ('TUNNE', 20),
    5: ('LNG', 25),
    6: ('TO', 28),
    7: ('THE', 30),
    8: ('SURFACE', 33),
    9: ('WE', 40),
    10: ('MUST', 42),
    11: ('SHED', 46),
    12: ('OUR', 50),
    13: ('OWN', 53),
    14: ('CIRCUMFERENCES', 56),
    15: ('FIND', 70),
    16: ('THE', 74),
    17: ('DIUINITY', 77),
    18: ('WITHIN', 85),
    19: ('AND', 91),
    20: ('EMERGE', 94),
}

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

def main():
    pages = load_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("=" * 80)
    print("FINDING THE OFFSET CONSTANT")
    print("=" * 80)
    
    # For each constant c, check if using word_position(page - c) as offset works
    for const in range(0, 50):
        total_score = 0
        details = []
        
        for pg_num in [27, 28, 29, 30, 31]:  # Test consecutive pages first
            word_idx = pg_num - const
            if word_idx in WORD_POSITIONS:
                word, pos = WORD_POSITIONS[word_idx]
                
                cipher = [rune_to_idx(r) for r in pages[pg_num]]
                text = decrypt_with_offset(cipher, pos)
                score = word_score(text)
                total_score += score
                details.append((pg_num, word_idx, word, pos, score))
        
        if total_score > 50:
            print(f"\nConstant = {const}: Total score = {total_score}")
            for pg, widx, word, pos, score in details:
                print(f"  Page {pg} -> word {widx} '{word}' at pos {pos}: score={score}")
    
    print("\n" + "=" * 80)
    print("BRUTE FORCE: FIND BEST OFFSET FOR EACH PAGE")
    print("=" * 80)
    
    # Record best offset for each page
    best_offsets = {}
    
    for pg_num in unsolved:
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(95):
            text = decrypt_with_offset(cipher, offset)
            score = word_score(text)
            
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = text
        
        best_offsets[pg_num] = (best_offset, best_score, best_text)
        
        # Check if this offset matches any word position
        matching_word = None
        for widx, (word, pos) in WORD_POSITIONS.items():
            if pos == best_offset:
                matching_word = (widx, word)
                break
        
        match_str = f" (word {matching_word[0]} '{matching_word[1]}')" if matching_word else ""
        print(f"Page {pg_num}: best offset = {best_offset}{match_str}, score = {best_score}")
        print(f"  {best_text[:70]}...")
    
    print("\n" + "=" * 80)
    print("OFFSET PATTERN ANALYSIS")
    print("=" * 80)
    
    print("\nPage | Best Offset | pg - offset | pg + offset | pg % offset")
    print("-" * 60)
    for pg_num, (offset, score, _) in sorted(best_offsets.items()):
        if offset > 0:
            print(f"{pg_num:4} | {offset:11} | {pg_num - offset:11} | {pg_num + offset:11} | {pg_num % offset if offset else 'N/A':11}")
    
    print("\n" + "=" * 80)
    print("LOOKING FOR FORMULA: offset = f(page_number)")
    print("=" * 80)
    
    # Check various formulas
    for pg_num, (offset, score, _) in sorted(best_offsets.items()):
        formulas = []
        
        # Check multiplication relationships
        for mult in range(1, 20):
            if (pg_num * mult) % 95 == offset:
                formulas.append(f"offset = ({mult} * page) mod 95")
        
        # Check addition relationships
        for add in range(-50, 50):
            if (pg_num + add) % 95 == offset:
                formulas.append(f"offset = (page + {add}) mod 95")
        
        # Check if offset is related to page digits
        digit_sum = sum(int(d) for d in str(pg_num))
        if digit_sum == offset or digit_sum * 10 == offset:
            formulas.append(f"offset related to digit sum {digit_sum}")
        
        formula_str = "; ".join(formulas[:3]) if formulas else "no simple formula"
        print(f"Page {pg_num}: offset={offset} -> {formula_str}")

if __name__ == "__main__":
    main()

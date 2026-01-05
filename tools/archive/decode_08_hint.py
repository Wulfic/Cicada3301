#!/usr/bin/env python3
"""
DECODE THE 08.jpg HINT
=======================

The hint says "For those who have fallen behind" and gives:

TL BE IE OV UT HT RE ID TS EO ST PO SO YR 
SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M

This looks like a KEY or INSTRUCTION for decryption!
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def load_all_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def word_score(text):
    score = 0
    words = {
        'THE': 9, 'AND': 9, 'THAT': 12, 'HAVE': 12, 'FOR': 9, 'NOT': 9, 'WITH': 12, 'THIS': 12,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

def main():
    print("="*70)
    print("DECODING THE 08.jpg HINT")
    print("="*70)
    
    # The hint pairs
    line1 = ['TL', 'BE', 'IE', 'OV', 'UT', 'HT', 'RE', 'ID', 'TS', 'EO', 'ST', 'PO', 'SO', 'YR']
    line2 = ['SL', 'BT', 'II', 'IY', 'T4', 'DG', 'UQ', 'IM', 'NU', '44', '2I', '15', '33', '9M']
    
    # Hypothesis 1: These are letter pairs that need to be swapped
    print("\nHypothesis 1: Read vertically to spell a message")
    
    # Take first letter of each pair
    first_letters_1 = ''.join(p[0] for p in line1)
    first_letters_2 = ''.join(p[0] for p in line2)
    print(f"First letters line 1: {first_letters_1}")
    print(f"First letters line 2: {first_letters_2}")
    
    # Take second letter of each pair  
    second_letters_1 = ''.join(p[1] for p in line1)
    second_letters_2 = ''.join(p[1] if len(p) > 1 else '?' for p in line2)
    print(f"Second letters line 1: {second_letters_1}")
    print(f"Second letters line 2: {second_letters_2}")
    
    # Hypothesis 2: These represent a SUBSTITUTION TABLE
    print("\n" + "="*70)
    print("Hypothesis 2: Substitution table (line1 -> line2)")
    print("="*70)
    
    # Maybe TL -> SL means T becomes S when followed by L?
    # Or TL as a digraph maps to SL as a digraph?
    
    print("Digraph mappings:")
    for p1, p2 in zip(line1, line2):
        print(f"  {p1} -> {p2}")
    
    # Hypothesis 3: Numbers in line2 are KEY POSITIONS
    print("\n" + "="*70)
    print("Hypothesis 3: Numbers as positions")
    print("="*70)
    
    # Extract just the numbers
    numbers = []
    for p in line2:
        num = ''.join(c for c in p if c.isdigit())
        if num:
            numbers.append(int(num))
    
    print(f"Numbers found: {numbers}")
    # [4, 44, 2, 15, 33, 9] or [4, 44, 21, 15, 33, 9]?
    
    # These could be positions in the master key or reading positions
    
    # Hypothesis 4: This spells something when read differently
    print("\n" + "="*70)
    print("Hypothesis 4: Interleaved reading")
    print("="*70)
    
    # Interleave line1 and line2
    interleaved = []
    for p1, p2 in zip(line1, line2):
        interleaved.append(p1)
        interleaved.append(p2)
    
    print(f"Interleaved: {''.join(interleaved)}")
    
    # What if we read all first letters, then all second letters?
    all_pairs = line1 + line2
    first_all = ''.join(p[0] for p in all_pairs)
    second_all = ''.join(p[1] if len(p) > 1 else '?' for p in all_pairs)
    print(f"All first letters: {first_all}")
    print(f"All second letters: {second_all}")
    
    # Hypothesis 5: This is the KEY for the solved pages
    print("\n" + "="*70)
    print("Hypothesis 5: Use as key for decryption")
    print("="*70)
    
    pages = load_all_pages()
    
    # Convert hint letters to indices
    # Line 1 only (clean letters)
    key_str = ''.join(line1)  # TLBEIEOVUTHTREIDTSEOSTPOSOYR
    print(f"Line 1 as string: {key_str}")
    
    # Map to indices
    key_indices = []
    i = 0
    while i < len(key_str):
        # Try 2-char runes first
        if i + 1 < len(key_str):
            two_char = key_str[i:i+2]
            if two_char in LETTER_TO_IDX:
                key_indices.append(LETTER_TO_IDX[two_char])
                i += 2
                continue
        # Single char
        one_char = key_str[i]
        if one_char in LETTER_TO_IDX:
            key_indices.append(LETTER_TO_IDX[one_char])
        i += 1
    
    print(f"As indices: {key_indices}")
    print(f"Key length: {len(key_indices)}")
    
    # Apply as Vigenère key
    key = np.array(key_indices, dtype=np.int32)
    
    for pg_num in [27, 28, 29, 30, 31]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key_ext = np.tile(key, (n // len(key) + 1))[:n]
        
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"\nPage {pg_num} with 08.jpg hint key | Score: {score}")
        print(f"  {text[:80]}")
    
    # Hypothesis 6: The second line contains BASE-36 numbers
    print("\n" + "="*70)
    print("Hypothesis 6: Base-36 decoding")
    print("="*70)
    
    for p in line2:
        try:
            val = int(p, 36)
            print(f"  {p} (base36) = {val} (decimal)")
        except:
            print(f"  {p} - not valid base36")
    
    # Hypothesis 7: Combined with master key
    print("\n" + "="*70)
    print("Hypothesis 7: 08.jpg hint modifies master key")
    print("="*70)
    
    MASTER_KEY = np.array([
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ], dtype=np.int32)
    
    # XOR hint key with master key
    hint_key_padded = np.array((key_indices * 10)[:95], dtype=np.int32)
    combined_key = (MASTER_KEY + hint_key_padded) % 29
    
    print(f"Combined key (first 20): {list(combined_key[:20])}")
    
    for pg_num in [30, 47]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key_ext = np.tile(combined_key, (n // len(combined_key) + 1))[:n]
        
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} with combined key | Score: {score}")
        print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

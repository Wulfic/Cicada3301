#!/usr/bin/env python3
"""
ANALYZING CICADA'S ACTUAL CLUES
================================

Key clue from 2016:
"Its words are the map, their meaning is the road, and their NUMBERS are the direction"

This suggests the NUMBERS embedded in the runes (Gematria Primus) are the key!

Also analyzing the hint from 08.jpg.txt:
TL BE IE OV UT HT RE ID TS EO ST PO SO YR 
SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Gematria Primus - the NUMBERS!
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

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

def main():
    print("="*70)
    print("ANALYZING CICADA'S CLUES")
    print("="*70)
    
    # CLUE 1: The 08.jpg hint
    print("\n" + "="*70)
    print("CLUE FROM 08.jpg.txt:")
    print("="*70)
    
    hint_line1 = "TL BE IE OV UT HT RE ID TS EO ST PO SO YR"
    hint_line2 = "SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M"
    
    print(f"Line 1: {hint_line1}")
    print(f"Line 2: {hint_line2}")
    
    pairs1 = hint_line1.split()
    pairs2 = hint_line2.split()
    
    print(f"\nLine 1 pairs: {pairs1}")
    print(f"Line 2 pairs: {pairs2}")
    
    # If we read vertically (pair line1 with line2):
    print("\nVertical pairing (line1[i] + line2[i]):")
    for i, (p1, p2) in enumerate(zip(pairs1, pairs2)):
        print(f"  {i+1}: {p1} + {p2} = {p1}{p2}")
    
    # What if each pair represents a transposition?
    # TL -> read as T, L (columns 16, 20 in our alphabet?)
    print("\nInterpreting as rune indices:")
    letter_to_idx = {l: i for i, l in enumerate(LETTERS)}
    
    for pair in pairs1:
        if len(pair) == 2:
            l1, l2 = pair[0], pair[1]
            idx1 = letter_to_idx.get(l1, '?')
            idx2 = letter_to_idx.get(l2, '?')
            print(f"  {pair}: {l1}={idx1}, {l2}={idx2}")
    
    # CLUE 2: "Numbers are the direction"
    print("\n" + "="*70)
    print("CLUE: 'NUMBERS ARE THE DIRECTION'")
    print("="*70)
    
    pages = load_all_pages()
    
    # For each page, sum the Gematria values
    print("\nGematria sums for each unsolved page:")
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        gematria_values = [GEMATRIA[i] for i in pg_idx]
        total = sum(gematria_values)
        
        # Check for patterns
        print(f"Page {pg_num}: {len(pg_idx)} runes, Gematria sum = {total}")
        print(f"    {total} mod 29 = {total % 29}")
        print(f"    {total} mod 95 = {total % 95}")
        print(f"    {total} // 29 = {total // 29}")
    
    # What if the "direction" means we should READ in a certain direction?
    # Or use the numbers to determine reading order?
    
    print("\n" + "="*70)
    print("TESTING: USE GEMATRIA VALUES AS READING ORDER")
    print("="*70)
    
    # For each page, sort positions by their Gematria value
    for pg_num in [30]:  # Test on best scoring page
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Create (position, gematria_value, rune_idx) tuples
        data = [(i, GEMATRIA[pg_idx[i]], pg_idx[i]) for i in range(n)]
        
        # Sort by Gematria value
        sorted_by_gematria = sorted(data, key=lambda x: x[1])
        
        # Read in this order
        reordered = [d[2] for d in sorted_by_gematria]
        text = indices_to_text(reordered)
        
        print(f"Page {pg_num} reordered by Gematria value:")
        print(f"  {text[:100]}")
    
    # What about the POSITION within Gematria?
    print("\n" + "="*70)
    print("TESTING: GEMATRIA VALUE AS KEY FOR EACH POSITION")
    print("="*70)
    
    # The "numbers" of each rune could be subtracted from ciphertext
    for pg_num in [30, 47]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Subtract the Gematria value of the SAME position
        # i.e., decrypt C[i] using C[i]'s own Gematria value
        gematria_key = np.array([GEMATRIA[idx] for idx in pg_idx], dtype=np.int32)
        
        decrypted = (pg_idx - gematria_key) % 29
        text = indices_to_text(decrypted)
        
        print(f"Page {pg_num} decrypted using own Gematria as key:")
        print(f"  {text[:100]}")
    
    # CLUE 3: Page structure / design
    print("\n" + "="*70)
    print("PAGE STRUCTURE ANALYSIS")
    print("="*70)
    
    # How many runes per page?
    for pg_num in unsolved:
        rune_count = len(pages[pg_num])
        
        # Check if it factors nicely
        factors = []
        for i in range(2, int(rune_count**0.5) + 1):
            if rune_count % i == 0:
                factors.append((i, rune_count // i))
        
        print(f"Page {pg_num}: {rune_count} runes")
        if factors:
            print(f"    Factors: {factors}")
        
        # Check if it's a prime
        is_prime = all(rune_count % i != 0 for i in range(2, int(rune_count**0.5) + 1))
        if is_prime and rune_count > 1:
            print(f"    {rune_count} is PRIME!")
    
    # CLUE 4: The magic squares from pages 10-13
    print("\n" + "="*70)
    print("MAGIC SQUARES HINT")
    print("="*70)
    
    print("""
From pages 10-13, magic squares with different border digits:
- Page 10: 3s (3333333333333333)
- Page 11: 3s (3333333333333333)  
- Page 12: 0s (0000000000000000)
- Page 13: 1s (1111111111111111)

The squares contain:
  10    12    10
  12    14    12
  10    12    10

These could be:
1. Column widths for transposition
2. Key indices
3. Reading pattern directions
""")
    
    # Test: Use 10, 12, 14 as key or column structure
    print("Testing magic square numbers as transposition key:")
    
    magic_key = [10, 12, 10, 12, 14, 12, 10, 12, 10]  # Reading the square
    print(f"Magic square as key: {magic_key}")
    
    for pg_num in [30]:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Use magic key as Vigenère
        key = np.array(magic_key * (n // len(magic_key) + 1), dtype=np.int32)[:n]
        decrypted = (pg_idx - key) % 29
        text = indices_to_text(decrypted)
        
        print(f"Page {pg_num} with magic square Vigenère:")
        print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

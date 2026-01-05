#!/usr/bin/env python3
"""
DEEP ANALYSIS OF 08.jpg HINT
=============================

The hint shows pairs:
Line 1: TL BE IE OV UT HT RE ID TS EO ST PO SO YR 
Line 2: SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M

This could be:
1. Column transposition order (14 pairs = 14 columns)
2. A substitution table
3. Reading instructions
4. A rebus/encoded message

Let's decode "THE" as reference:
T -> E (value?)
H -> ?
E -> ?
"""

import re
from pathlib import Path
import numpy as np

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

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

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

def load_pages():
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
    print("DEEP ANALYSIS OF 08.jpg HINT")
    print("="*70)
    
    # The hint pairs
    line1 = ['TL', 'BE', 'IE', 'OV', 'UT', 'HT', 'RE', 'ID', 'TS', 'EO', 'ST', 'PO', 'SO', 'YR']
    line2 = ['SL', 'BT', 'II', 'IY', 'T4', 'DG', 'UQ', 'IM', 'NU', '44', '2I', '15', '33', '9M']
    
    # Read the actual 08.jpg page content for context
    # Page 8 (0-indexed) corresponds to what content?
    
    print("\nHypothesis: The pairs indicate a COLUMNAR TRANSPOSITION ORDER")
    print("14 pairs = 14 columns")
    print()
    
    # Extract column order from the numbers in line2
    # The numeric portions might be column indices
    col_order = []
    for i, p in enumerate(line2):
        # Try to extract numbers
        nums = ''.join(c for c in p if c.isdigit())
        if nums:
            col_order.append((i, int(nums)))
        else:
            # For pure letter pairs, use alphabetical position
            alpha_val = sum(ord(c.upper()) - ord('A') for c in p if c.isalpha())
            col_order.append((i, alpha_val))
    
    print("Extracted values from line2:")
    for i, (orig_pos, val) in enumerate(col_order):
        print(f"  Position {i} ({line2[i]}): value = {val}")
    
    # Sort by value to get reading order
    sorted_order = sorted(col_order, key=lambda x: x[1])
    read_order = [x[0] for x in sorted_order]
    print(f"\nReading order (sorted by value): {read_order}")
    
    # Apply this as a 14-column transposition
    pages = load_pages()
    
    print("\n" + "="*70)
    print("TESTING 14-COLUMN TRANSPOSITION WITH HINT ORDER")
    print("="*70)
    
    for pg_num in [27, 28, 29, 30, 31, 44, 45, 46, 47, 48]:
        if pg_num not in pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Arrange into 14 columns
        cols = 14
        rows = (n + cols - 1) // cols
        
        # Pad
        padded = np.zeros(rows * cols, dtype=np.int32)
        padded[:n] = pg_idx
        grid = padded.reshape(rows, cols)
        
        # Read columns in the hint order
        reordered = []
        for col_idx in read_order:
            reordered.extend(grid[:, col_idx])
        
        reordered = np.array(reordered[:n], dtype=np.int32)
        
        # Apply master key
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (reordered - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} 14-col hint order + key: {score}")
        print(f"  {text[:70]}")
    
    # Try different interpretation: read_order as row skip pattern
    print("\n" + "="*70)
    print("ALTERNATIVE: Use hint as ROW-SKIP PATTERN")
    print("="*70)
    
    # The values [4, 44, 2, 15, 33, 9] from the numbers
    skip_values = [4, 44, 2, 15, 33, 9]
    
    for pg_num in [27, 30]:
        if pg_num not in pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        # Use skip values cyclically to determine reading positions
        result = []
        pos = 0
        skip_idx = 0
        visited = set()
        
        while len(result) < n and len(visited) < n:
            if pos not in visited:
                result.append(pg_idx[pos % n])
                visited.add(pos)
            pos = (pos + skip_values[skip_idx % len(skip_values)]) % n
            skip_idx += 1
        
        # Fill remaining
        for i in range(n):
            if i not in visited:
                result.append(pg_idx[i])
        
        result = np.array(result[:n], dtype=np.int32)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (result - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} skip pattern [{', '.join(map(str, skip_values))}]: {score}")
        print(f"  {text[:70]}")
    
    # Hypothesis: The letter pairs spell a message
    print("\n" + "="*70)
    print("DECODING LETTER PAIRS AS MESSAGE")
    print("="*70)
    
    # Read column by column
    for read_mode in ["top-bottom", "bottom-top", "alternating"]:
        msg = []
        if read_mode == "top-bottom":
            for p1, p2 in zip(line1, line2):
                msg.append(p1[0] if len(p1) > 0 else '')
                msg.append(p2[0] if len(p2) > 0 else '')
        elif read_mode == "bottom-top":
            for p1, p2 in zip(line1, line2):
                msg.append(p2[0] if len(p2) > 0 else '')
                msg.append(p1[0] if len(p1) > 0 else '')
        else:  # alternating
            for i, (p1, p2) in enumerate(zip(line1, line2)):
                if i % 2 == 0:
                    msg.append(p1)
                else:
                    msg.append(p2)
        
        print(f"{read_mode}: {''.join(msg)}")
    
    # What if we read: T-S, L-L, B-B, E-T, ...
    print("\nInterleaved vertically:")
    interleaved = []
    for p1, p2 in zip(line1, line2):
        interleaved.append(p1[0] + p2[0] if len(p1) > 0 and len(p2) > 0 else '')
    print(''.join(interleaved))
    
    # What does the message say if decoded?
    # "THE LIBER PRIMUS IS THE WAY"?
    
    # Try: Take first letters of line1 and decode as runes
    line1_first = ''.join(p[0] for p in line1)
    line1_second = ''.join(p[1] for p in line1 if len(p) > 1)
    
    print(f"\nLine 1 first letters: {line1_first}")
    print(f"Line 1 second letters: {line1_second}")
    
    # What about treating these as positional hints for the master key?
    print("\n" + "="*70)
    print("USING HINT AS KEY MODIFIER")
    print("="*70)
    
    # Convert line1 to indices (A=0, B=1, etc.)
    hint_indices = []
    for p in line1:
        for c in p:
            if c.isalpha():
                hint_indices.append(ord(c.upper()) - ord('A'))
    
    print(f"Hint as indices: {hint_indices}")
    
    # XOR with master key
    hint_key = np.array((hint_indices * 10)[:95], dtype=np.int32)
    modified_key = (MASTER_KEY ^ hint_key) % 29
    
    print(f"Modified key (first 20): {list(modified_key[:20])}")
    
    for pg_num in [27, 30, 31, 47]:
        if pg_num not in pages:
            continue
            
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        key_ext = np.tile(modified_key, (n // 95 + 1))[:n]
        decrypted = (pg_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} with XOR-modified key: {score}")
        print(f"  {text[:70]}")

if __name__ == "__main__":
    main()

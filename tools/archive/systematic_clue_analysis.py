"""
SYSTEMATIC CLUE ANALYSIS
=========================

The 2016 signed message says:
"Liber Primus is the way. Its words are the map, their meaning is the road, 
and their NUMBERS are the direction."

This is a clear cryptographic hint. Let's analyze:
1. "words are the map" - the rune words give us the framework/structure
2. "meaning is the road" - understanding/semantics guide interpretation
3. "NUMBERS are the direction" - Gematria values give us operational direction

KEY INSIGHT: Maybe the numbers (Gematria) tell us HOW to read/process the text
rather than WHAT cipher to use.
"""

import numpy as np
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

# Gematria Primus values
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
         'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
         'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def indices_to_text(indices):
    return ''.join(LATIN[i % 29] for i in indices)

def word_score(text):
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST',
             'SURFACE', 'TUNNEL', 'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        score += text_upper.count(word) * len(word)
    return score

# Pages to test - let's focus on partial success cases
UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

print("=" * 70)
print("GEMATRIA-BASED READING DIRECTION ANALYSIS")
print("=" * 70)
print()
print("Testing if Gematria values control reading direction...")
print()

key = np.array(MASTER_KEY)

for pg_num in [27, 28, 29, 30, 31]:
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    print(f"\n{'='*60}")
    print(f"PAGE {pg_num} - {n} runes")
    print(f"{'='*60}")
    
    # Get Gematria values for each rune
    gematria_vals = [GEMATRIA[i] for i in pg_idx]
    
    # Analyze Gematria patterns
    total_gematria = sum(gematria_vals)
    avg_gematria = total_gematria / n
    
    print(f"Gematria sum: {total_gematria}")
    print(f"Sum mod 29: {total_gematria % 29}")
    print(f"Sum mod 95 (key length): {total_gematria % 95}")
    print(f"Average Gematria: {avg_gematria:.2f}")
    
    # Key extension
    key_ext = np.tile(key, (n // len(key)) + 1)[:n]
    
    # Standard decryption
    standard = (pg_idx - key_ext) % 29
    standard_text = indices_to_text(standard)
    standard_score = word_score(standard_text)
    print(f"\nStandard decryption score: {standard_score}")
    print(f"Text: {standard_text[:60]}...")
    
    # Try reading in order of Gematria values (smallest to largest)
    gematria_order = np.argsort(gematria_vals)
    reordered = pg_idx[gematria_order]
    decrypted = (reordered - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"\nGematria ascending order + key: score {score}")
    if score > standard_score:
        print(f">>> BETTER! Text: {text[:60]}...")
    
    # Try reading in DESCENDING order
    gematria_order_desc = np.argsort(gematria_vals)[::-1]
    reordered = pg_idx[gematria_order_desc]
    decrypted = (reordered - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"Gematria descending order + key: score {score}")
    if score > standard_score:
        print(f">>> BETTER! Text: {text[:60]}...")
    
    # Try using Gematria as step direction
    # "Numbers are the direction" - maybe walk through indices based on gematria?
    result = []
    pos = 0
    visited = set()
    for i in range(n):
        if pos not in visited and 0 <= pos < n:
            result.append(pg_idx[pos])
            visited.add(pos)
            # Move by gematria value
            step = gematria_vals[pos] % n
            pos = (pos + step) % n
            while pos in visited and len(visited) < n:
                pos = (pos + 1) % n
        else:
            # Find next unvisited
            for j in range(n):
                if j not in visited:
                    result.append(pg_idx[j])
                    visited.add(j)
                    pos = (j + gematria_vals[j]) % n
                    break
    
    if len(result) == n:
        result = np.array(result)
        decrypted = (result - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        print(f"Gematria walk + key: score {score}")
        if score > standard_score:
            print(f">>> BETTER! Text: {text[:60]}...")
    
    # Try cumulative Gematria as index
    cumsum = np.cumsum(gematria_vals) % n
    result = pg_idx[cumsum]
    decrypted = (result - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"Cumulative Gematria index + key: score {score}")
    if score > standard_score:
        print(f">>> BETTER! Text: {text[:60]}...")
    
    # Try Gematria-modulated key
    # Each key element is shifted by the corresponding Gematria
    gematria_key_ext = np.array(gematria_vals) % 29
    decrypted = (pg_idx - key_ext - gematria_key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"Double key (standard + Gematria): score {score}")
    if score > standard_score:
        print(f">>> BETTER! Text: {text[:60]}...")
    
    # Try Gematria XOR key
    gematria_xor_key = np.array([g ^ k for g, k in zip(gematria_vals, key_ext)])
    decrypted = (pg_idx - gematria_xor_key) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"Gematria XOR key: score {score}")
    if score > standard_score:
        print(f">>> BETTER! Text: {text[:60]}...")

print("\n" + "=" * 70)
print("COLUMNAR WITH GEMATRIA-ORDERED READING")
print("=" * 70)

for pg_num in [30, 31]:  # These had higher scores with transposition
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    print(f"\nPage {pg_num}:")
    
    key_ext = np.tile(key, (n // len(key)) + 1)[:n]
    
    for cols in [7, 8, 9, 10, 11, 12, 13]:
        rows = (n + cols - 1) // cols
        # Pad
        padded = list(pg_idx) + [0] * (rows * cols - n)
        grid = np.array(padded).reshape(rows, cols)
        
        # Read columns, but order columns by sum of Gematria in each
        col_gematria = []
        for c in range(cols):
            col_sum = sum(GEMATRIA[i] for i in grid[:, c] if i < n)
            col_gematria.append((col_sum, c))
        
        col_gematria.sort()  # Sort by Gematria sum
        col_order = [c for _, c in col_gematria]
        
        result = []
        for c in col_order:
            for r in range(rows):
                if r * cols + c < n:
                    result.append(grid[r, c])
        
        result = np.array(result[:n])
        decrypted = (result - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score >= 50:
            print(f"  Cols={cols}, Gematria-ordered columns: score {score}")
            print(f"    {text[:60]}...")

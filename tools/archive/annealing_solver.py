#!/usr/bin/env python3
"""
Advanced transposition cipher solver using simulated annealing.
For the Cicada 3301 authenticated cipher discovered by XOR.

IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO
UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ
"""

import random
import math
from collections import Counter

# The cipher (67 letters after removing 7, 5, 4)
CIPHER = "IDGTKUMLOOARWOERTHISUTETLHUTIATSLLOUIMNITELNJTFYVOIUAUSNOCOJIMEODZZ"

# English letter frequencies
ENGLISH_FREQS = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# Common English bigrams
BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.20, 'OF': 1.17,
    'ED': 1.17, 'IS': 1.13, 'IT': 1.12, 'AL': 1.09, 'AR': 1.07,
    'ST': 1.05, 'TO': 1.05, 'NT': 1.04, 'NG': 0.95, 'SE': 0.93,
    'HA': 0.93, 'AS': 0.87, 'OU': 0.87, 'IO': 0.83, 'LE': 0.83,
    'VE': 0.83, 'CO': 0.79, 'ME': 0.79, 'DE': 0.76, 'HI': 0.76,
    'RI': 0.73, 'RO': 0.73, 'IC': 0.70, 'NE': 0.69, 'EA': 0.69,
    'RA': 0.69, 'CE': 0.65, 'LI': 0.62, 'CH': 0.60, 'LL': 0.58,
    'BE': 0.58, 'MA': 0.57, 'SI': 0.55, 'OM': 0.55, 'UR': 0.54,
}

# Common trigrams
TRIGRAMS = {
    'THE': 3.51, 'AND': 1.59, 'ING': 1.15, 'ENT': 0.85, 'ION': 0.79,
    'HER': 0.76, 'FOR': 0.76, 'THA': 0.73, 'NTH': 0.73, 'INT': 0.69,
    'ERE': 0.65, 'TIO': 0.65, 'TER': 0.62, 'EST': 0.59, 'ERS': 0.59,
    'ATI': 0.57, 'HAT': 0.57, 'ATE': 0.55, 'ALL': 0.54, 'ETH': 0.52,
    'HES': 0.52, 'VER': 0.50, 'HIS': 0.50, 'OFT': 0.48, 'ITH': 0.48,
    'FTH': 0.46, 'STH': 0.44, 'OTH': 0.44, 'RES': 0.43, 'ONT': 0.43,
}

# Cicada-related words to look for
CICADA_WORDS = [
    'UNTO', 'THE', 'INITIATED', 'LIKE', 'INSTAR', 'TUNNELING', 'SURFACE',
    'MUST', 'SHED', 'OUR', 'OWN', 'CIRCUMFERENCE', 'FIND', 'DIVINITY',
    'WITHIN', 'EMERGE', 'TRUTH', 'WISDOM', 'SEEK', 'LIBER', 'PRIMUS',
    'CICADA', 'RUNE', 'THIS', 'KEY', 'PATH', 'WAY', 'ALL', 'YOU'
]

def score_text(text):
    """Score decryption attempt based on English-likeness."""
    text = text.upper()
    score = 0
    
    # Bigram scoring
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        if bg in BIGRAMS:
            score += BIGRAMS[bg] * 10
    
    # Trigram scoring
    for i in range(len(text) - 2):
        tg = text[i:i+3]
        if tg in TRIGRAMS:
            score += TRIGRAMS[tg] * 20
    
    # Word bonus
    for word in CICADA_WORDS:
        if word in text:
            score += len(word) * 50
    
    return score

def apply_transposition(text, key):
    """Apply columnar transposition with given key (list of column indices)."""
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    
    # Pad text if necessary
    padded = text + 'X' * (num_cols * num_rows - len(text))
    
    # Arrange in grid row by row
    grid = []
    for r in range(num_rows):
        grid.append(list(padded[r*num_cols:(r+1)*num_cols]))
    
    # Read columns in key order
    result = []
    for col in key:
        for row in range(num_rows):
            if col < len(grid[row]):
                result.append(grid[row][col])
    
    return ''.join(result)[:len(text)]

def decrypt_transposition(text, key):
    """Decrypt columnar transposition given key (column reading order)."""
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    
    # Calculate column lengths
    full_cols = len(text) % num_cols
    if full_cols == 0:
        full_cols = num_cols
    
    # Determine which columns are full based on key order
    col_lengths = [0] * num_cols
    for i, col in enumerate(sorted(range(num_cols), key=lambda x: key[x])):
        col_lengths[col] = num_rows if i < full_cols else num_rows - 1
    
    # Fill columns in key order
    columns = [[] for _ in range(num_cols)]
    idx = 0
    for col in sorted(range(num_cols), key=lambda x: key[x]):
        length = col_lengths[col]
        columns[col] = list(text[idx:idx+length])
        idx += length
    
    # Read row by row
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(columns[col]):
                result.append(columns[col][row])
    
    return ''.join(result)

def simulated_annealing(text, num_cols, iterations=100000):
    """Use simulated annealing to find the best transposition key."""
    # Start with random key
    best_key = list(range(num_cols))
    random.shuffle(best_key)
    best_decryption = decrypt_transposition(text, best_key)
    best_score = score_text(best_decryption)
    
    current_key = best_key.copy()
    current_score = best_score
    
    temperature = 1.0
    cooling = 0.99999
    
    for i in range(iterations):
        # Make a small change (swap two positions)
        new_key = current_key.copy()
        a, b = random.sample(range(num_cols), 2)
        new_key[a], new_key[b] = new_key[b], new_key[a]
        
        new_decryption = decrypt_transposition(text, new_key)
        new_score = score_text(new_decryption)
        
        # Decide whether to accept
        delta = new_score - current_score
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_key = new_key
            current_score = new_score
            
            if current_score > best_score:
                best_key = current_key.copy()
                best_score = current_score
                best_decryption = new_decryption
                print(f"  Iter {i}: Score {best_score:.1f} | {best_decryption[:50]}...")
        
        temperature *= cooling
    
    return best_key, best_decryption, best_score

print("="*70)
print("SIMULATED ANNEALING TRANSPOSITION SOLVER")
print("="*70)
print(f"\nCipher: {CIPHER[:40]}... ({len(CIPHER)} chars)")

# Try different column counts
for num_cols in [5, 7, 11, 13, 14]:
    print(f"\n{'='*50}")
    print(f"Trying {num_cols} columns:")
    print(f"{'='*50}")
    
    key, decryption, score = simulated_annealing(CIPHER, num_cols, iterations=50000)
    print(f"\nBest for {num_cols} cols:")
    print(f"  Key: {key}")
    print(f"  Score: {score}")
    print(f"  Decryption: {decryption}")

# Also try brute force for small column counts
print("\n" + "="*70)
print("BRUTE FORCE FOR 5-COLUMN TRANSPOSITION")
print("="*70)

from itertools import permutations

best_score = 0
best_result = ""
best_key = None

for perm in permutations(range(5)):
    result = decrypt_transposition(CIPHER, list(perm))
    score = score_text(result)
    if score > best_score:
        best_score = score
        best_result = result
        best_key = perm
        if score > 100:
            print(f"Key {perm}: {result[:40]}... (score={score})")

print(f"\nBest 5-column result:")
print(f"  Key: {best_key}")
print(f"  Score: {best_score}")
print(f"  Text: {best_result}")

# Try 7 columns brute force
print("\n" + "="*70)
print("BRUTE FORCE FOR 7-COLUMN TRANSPOSITION")
print("="*70)

best_score = 0
best_result = ""
best_key = None

for perm in permutations(range(7)):
    result = decrypt_transposition(CIPHER, list(perm))
    score = score_text(result)
    if score > best_score:
        best_score = score
        best_result = result
        best_key = perm
        if score > 150:
            print(f"Key {perm}: {result[:40]}... (score={score})")

print(f"\nBest 7-column result:")
print(f"  Key: {best_key}")
print(f"  Score: {best_score}")
print(f"  Text: {best_result}")

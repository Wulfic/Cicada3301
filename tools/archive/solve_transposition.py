#!/usr/bin/env python3
"""
Advanced transposition cipher solver for the XOR-discovered message.

Message: IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ

14 groups of 5 characters = 70 characters (67 letters + 3 numbers)
"""

import itertools
from collections import Counter
import re

# The cipher text
GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', '7TFYV', 'OIUAU', 'SNOCO', '5JI4M', 'EODZZ']
CIPHER = ''.join(GROUPS)

# Common English words for scoring
COMMON_WORDS = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'THIS', 'THAT', 'WITH',
    'THEY', 'FROM', 'HAVE', 'BEEN', 'WERE', 'SOME', 'WHAT', 'WHEN', 'WHICH',
    'DIVINITY', 'WITHIN', 'RUNE', 'RUNES', 'CICADA', 'PRIMUS', 'LIBER',
    'INSTAR', 'EMERGE', 'TUNNEL', 'SURFACE', 'SHED', 'TRUTH', 'WISDOM',
    'KEY', 'FIND', 'PATH', 'WAY', 'SEEK', 'KNOW', 'UNDERSTAND'
]

# English bigram frequencies (simplified)
COMMON_BIGRAMS = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ES', 'ON', 'ST', 'NT',
                  'EN', 'AT', 'ED', 'ND', 'TO', 'OR', 'EA', 'TI', 'AR', 'TE']

def score_text(text):
    """Score text based on English patterns."""
    text = text.upper()
    score = 0
    
    # Word matches
    for word in COMMON_WORDS:
        score += text.count(word) * len(word) * 10
    
    # Bigram matches
    for bigram in COMMON_BIGRAMS:
        score += text.count(bigram) * 2
    
    # Letter frequency (E, T, A, O, I, N should be common)
    common_letters = Counter(text)
    expected_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    for i, letter in enumerate(expected_order[:10]):
        if letter in common_letters:
            score += common_letters[letter] * (10 - i)
    
    return score

def columnar_decipher(text, key):
    """Decode columnar transposition with given key order."""
    n = len(key)
    rows = (len(text) + n - 1) // n
    
    # Create grid
    grid = [['' for _ in range(n)] for _ in range(rows)]
    
    # Fill by columns in key order
    idx = 0
    for col_idx in sorted(range(n), key=lambda x: key[x]):
        for row in range(rows):
            if idx < len(text):
                grid[row][col_idx] = text[idx]
                idx += 1
    
    # Read row by row
    return ''.join(''.join(row) for row in grid)

def rail_fence_decipher(text, rails):
    """Decode rail fence cipher."""
    if rails <= 1:
        return text
    
    # Calculate pattern length
    pattern_len = 2 * (rails - 1)
    
    # Build the fence pattern
    fence = [[None] * len(text) for _ in range(rails)]
    
    # Mark positions
    rail = 0
    direction = 1
    for i in range(len(text)):
        fence[rail][i] = '*'
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    # Fill with text
    idx = 0
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c] == '*':
                fence[r][c] = text[idx]
                idx += 1
    
    # Read in zigzag
    result = []
    rail = 0
    direction = 1
    for i in range(len(text)):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    return ''.join(result)

def route_cipher_decode(text, rows, cols, route='spiral_cw'):
    """Decode route cipher - reading grid in different patterns."""
    if len(text) > rows * cols:
        return None
    
    # Pad text
    text = text.ljust(rows * cols)
    
    # Fill grid row by row
    grid = []
    for r in range(rows):
        grid.append(list(text[r*cols:(r+1)*cols]))
    
    result = []
    
    if route == 'cols':
        for c in range(cols):
            for r in range(rows):
                result.append(grid[r][c])
    elif route == 'cols_reverse':
        for c in range(cols-1, -1, -1):
            for r in range(rows):
                result.append(grid[r][c])
    elif route == 'rows_reverse':
        for r in range(rows-1, -1, -1):
            for c in range(cols):
                result.append(grid[r][c])
    elif route == 'zigzag':
        for r in range(rows):
            if r % 2 == 0:
                for c in range(cols):
                    result.append(grid[r][c])
            else:
                for c in range(cols-1, -1, -1):
                    result.append(grid[r][c])
    elif route == 'diagonal':
        for d in range(rows + cols - 1):
            for r in range(rows):
                c = d - r
                if 0 <= c < cols:
                    result.append(grid[r][c])
    
    return ''.join(result)

def try_group_reordering():
    """Try different orderings of the 5-letter groups."""
    print("\n--- Group Reordering Analysis ---")
    
    # Try prime-indexed groups
    primes = [2, 3, 5, 7, 11, 13]
    
    # The numbers 7, 5, 4 might indicate group positions
    # Group with '7' is at index 9 (7TFYV)
    # Group with '5' is at index 12 (5JI4M) 
    # Group with '4' is also at index 12 (5JI4M)
    
    print("Groups with numbers:")
    for i, g in enumerate(GROUPS):
        if any(c.isdigit() for c in g):
            print(f"  Index {i}: {g}")
    
    # Try reading groups in numeric order
    print("\nIf 7, 5, 4 indicate positions to swap or reorder:")
    print("  Original positions: 9 (7TFYV) and 12 (5JI4M)")
    
    # Try swapping these groups to different positions
    test_orders = [
        list(range(14)),  # Original
        [0,1,2,3,4,5,6,7,8,12,10,11,9,13],  # Swap 9 and 12
        [9,12] + list(range(14)) [:-2],  # Move numbered groups to front
    ]
    
    for order in test_orders:
        if len(order) == 14:
            reordered = ''.join(GROUPS[i] for i in order)
            score = score_text(reordered)
            if score > 50:
                print(f"  Order {order[:5]}...: score={score}")

def search_transpositions():
    """Search for the correct transposition."""
    print("="*70)
    print("TRANSPOSITION CIPHER ANALYSIS")
    print("="*70)
    
    text = CIPHER.replace('7', '').replace('5', '').replace('4', '')  # Remove numbers for now
    print(f"Text (no numbers): {text}")
    print(f"Length: {len(text)}")
    
    best_results = []
    
    # Try columnar transposition with different key lengths
    print("\n--- Columnar Transposition ---")
    for key_len in range(2, 15):
        if len(text) % key_len == 0 or True:  # Try all
            for key in itertools.permutations(range(key_len)):
                result = columnar_decipher(text, key)
                score = score_text(result)
                if score > 80:
                    best_results.append((score, f"Columnar key={key}", result))
    
    # Try rail fence
    print("\n--- Rail Fence ---")
    for rails in range(2, 10):
        result = rail_fence_decipher(text, rails)
        score = score_text(result)
        if score > 50:
            best_results.append((score, f"Rail Fence rails={rails}", result))
    
    # Try route ciphers
    print("\n--- Route Ciphers ---")
    for rows in range(2, 15):
        for cols in range(2, 15):
            if rows * cols >= len(text):
                for route in ['cols', 'cols_reverse', 'rows_reverse', 'zigzag', 'diagonal']:
                    result = route_cipher_decode(text, rows, cols, route)
                    if result:
                        score = score_text(result)
                        if score > 60:
                            best_results.append((score, f"Route {rows}x{cols} {route}", result))
    
    # Sort by score
    best_results.sort(reverse=True)
    
    print("\n--- Top 20 Results ---")
    for score, method, result in best_results[:20]:
        print(f"  [{score:3d}] {method}: {result[:60]}...")
    
    return best_results

def anagram_search():
    """Search for meaningful anagrams."""
    print("\n" + "="*70)
    print("ANAGRAM SEARCH")
    print("="*70)
    
    text = CIPHER.replace('7', '').replace('5', '').replace('4', '').upper()
    
    # Check for known Cicada phrases
    target_phrases = [
        "WITHIN THE DIVINITY",
        "FIND THE KEY WITHIN",
        "LIBER PRIMUS SOLUTION",
        "THE TRUTH IS OUT THERE",
        "LIKE THE INSTAR",
        "SHED OUR CIRCUMFERENCES",
        "THIS IS THE KEY",
        "UNTO THE INITIATED",
    ]
    
    text_sorted = ''.join(sorted(text))
    print(f"Sorted cipher letters: {text_sorted}")
    
    for phrase in target_phrases:
        phrase_clean = phrase.replace(' ', '')
        phrase_sorted = ''.join(sorted(phrase_clean))
        
        # Check if phrase could fit in cipher
        text_counter = Counter(text)
        phrase_counter = Counter(phrase_clean)
        
        can_contain = all(text_counter.get(c, 0) >= phrase_counter[c] for c in phrase_counter)
        
        if can_contain:
            print(f"  Could contain: '{phrase}'")
            # What letters remain?
            remaining = text
            for c in phrase_clean:
                remaining = remaining.replace(c, '', 1)
            print(f"    Remaining letters: {remaining}")

def main():
    print("="*70)
    print("SOLVING THE XOR-DISCOVERED CIPHER")
    print("="*70)
    print(f"\nOriginal: {' '.join(GROUPS)}")
    print(f"Combined: {CIPHER}")
    print(f"Length: {len(CIPHER)} chars")
    
    try_group_reordering()
    search_transpositions()
    anagram_search()
    
    # Try with 14x5 grid (14 groups of 5)
    print("\n" + "="*70)
    print("14x5 GRID ANALYSIS (as presented)")
    print("="*70)
    
    for i, g in enumerate(GROUPS):
        print(f"  {i+1:2d}: {g}")
    
    # Read columns
    print("\nReading by columns (1st letter of each group, 2nd, etc.):")
    for col in range(5):
        letters = ''.join(g[col] if col < len(g) else ' ' for g in GROUPS)
        print(f"  Column {col+1}: {letters}")
    
    print("\nCombined column reading: ", end='')
    col_read = ''
    for col in range(5):
        for g in GROUPS:
            if col < len(g):
                col_read += g[col]
    print(col_read)
    
    # Check score
    score = score_text(col_read)
    print(f"Score: {score}")
    
    # Try reading diagonal
    print("\nDiagonal reading (SE direction):")
    diag = ''
    for start in range(14):
        row, col = start, 0
        while row < 14 and col < 5:
            if col < len(GROUPS[row]):
                diag += GROUPS[row][col]
            row += 1
            col += 1
    print(f"  {diag}")

if __name__ == "__main__":
    main()

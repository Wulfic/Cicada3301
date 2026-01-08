#!/usr/bin/env python3
"""
Combined Hill-Climbing + Interleaving Solver
First applies hill-climbing to find optimal first-layer key,
then tests interleaving/transposition for second layer.
"""

import os
import sys
import random
from pathlib import Path

# Gematria Primus mappings
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

# Bigram scores for English
BIGRAM_SCORES = {
    ('T','H'): 50, ('H','E'): 45, ('A','N'): 35, ('I','N'): 35, ('E','R'): 30,
    ('N','D'): 25, ('O','N'): 25, ('R','E'): 25, ('E','D'): 25, ('E','S'): 25,
    ('T','O'): 25, ('O','R'): 20, ('I','T'): 20, ('I','S'): 20, ('O','F'): 20,
    ('E','N'): 20, ('A','T'): 20, ('N','T'): 20, ('T','I'): 20, ('S','T'): 20,
    ('A','R'): 15, ('N','G'): 15, ('A','L'): 15, ('O','U'): 15, ('F','O'): 15,
    ('L','E'): 15, ('T','E'): 15, ('W','I'): 15, ('H','I'): 15, ('Y','O'): 12,
    ('W','E'): 12, ('M','E'): 12, ('B','E'): 12, ('H','A'): 12, ('S','O'): 12,
}

def load_runes(page_num):
    """Load runes from a page."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Extract only rune characters
    indices = []
    for r in content:
        if r in RUNE_MAP:
            indices.append(RUNE_MAP[r])
    
    return indices

def index_to_letter(idx):
    """Convert index to letter."""
    if 0 <= idx < 29:
        return LETTERS[idx]
    return '?'

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(index_to_letter(i) for i in indices)

def decrypt_sub(ciphertext, key):
    """Decrypt using SUB: p = (c - k) mod 29"""
    return [(c - key[i % len(key)]) % 29 for i, c in enumerate(ciphertext)]

def score_bigrams(text):
    """Score text based on English bigram frequency."""
    # Flatten digraphs to single chars for scoring
    flat = text.replace('TH', 'Z').replace('NG', 'Q').replace('IO', 'V').replace('EO', 'K').replace('EA', 'W').replace('AE', 'X').replace('OE', 'Y')
    
    score = 0
    for i in range(len(flat) - 1):
        pair = (flat[i], flat[i+1])
        score += BIGRAM_SCORES.get(pair, 0)
    return score

def score_text(text):
    """Comprehensive scoring for English text."""
    score = 0
    
    # High-value trigrams and words
    TRIGRAMS = {
        'THE': 100, 'AND': 80, 'ING': 70, 'HER': 60, 'HAT': 50,
        'HIS': 50, 'THA': 50, 'ERE': 50, 'FOR': 50, 'ENT': 40,
        'ION': 40, 'TER': 40, 'WAS': 40, 'YOU': 40, 'ITH': 40,
        'VER': 35, 'ALL': 35, 'WIT': 35, 'THI': 35, 'TIO': 35,
    }
    
    WORDS = {
        'TRUTH': 200, 'WITHIN': 200, 'DIVINITY': 250, 'WISDOM': 180,
        'EMERGE': 180, 'CIRCUMFERENCE': 300, 'SURFACE': 180,
        'BEING': 150, 'INSTAR': 200, 'SHED': 120, 'UNTO': 100,
        'THOU': 100, 'THEE': 100, 'HATH': 100, 'THINE': 100,
    }
    
    for tri, val in TRIGRAMS.items():
        score += text.count(tri) * val
    
    for word, val in WORDS.items():
        score += text.count(word) * val
    
    # Bigrams
    score += score_bigrams(text)
    
    return score

def hill_climb(ciphertext, key_length, iterations=2000):
    """Hill-climbing optimization to find the best key."""
    # Initialize with random key
    best_key = [random.randint(0, 28) for _ in range(key_length)]
    best_decrypted = decrypt_sub(ciphertext, best_key)
    best_text = indices_to_text(best_decrypted)
    best_score = score_text(best_text)
    
    for iteration in range(iterations):
        # Random modification
        new_key = best_key.copy()
        pos = random.randint(0, key_length - 1)
        new_key[pos] = random.randint(0, 28)
        
        new_decrypted = decrypt_sub(ciphertext, new_key)
        new_text = indices_to_text(new_decrypted)
        new_score = score_text(new_text)
        
        if new_score > best_score:
            best_key = new_key
            best_text = new_text
            best_score = new_score
    
    return best_key, best_text, best_score

def deinterleave(text, num_streams):
    """Deinterleave text."""
    streams = ['' for _ in range(num_streams)]
    for i, char in enumerate(text):
        streams[i % num_streams] += char
    return ''.join(streams)

def columnar_read(text, num_cols):
    """Read text as if written in rows, read in columns."""
    pad_len = (num_cols - len(text) % num_cols) % num_cols
    padded = text + 'X' * pad_len
    num_rows = len(padded) // num_cols
    
    result = ''
    for col in range(num_cols):
        for row in range(num_rows):
            idx = row * num_cols + col
            if idx < len(text):
                result += padded[idx]
    return result[:len(text)]

def reverse_columnar(text, num_cols):
    """Reverse columnar (written in columns, read in rows)."""
    pad_len = (num_cols - len(text) % num_cols) % num_cols
    padded = text + 'X' * pad_len
    num_rows = len(padded) // num_cols
    
    grid = [[''] * num_cols for _ in range(num_rows)]
    idx = 0
    for col in range(num_cols):
        for row in range(num_rows):
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    result = ''
    for row in grid:
        result += ''.join(row)
    return result[:len(text)]

def try_interleaving(text, key_length):
    """Try various interleaving methods and score results."""
    results = []
    
    # Test parameters based on key length and primes
    test_params = [2, 3, 4, 5, 6, 7, 11, 13, 17, 19, 23, 29, key_length]
    
    for n in test_params:
        # Deinterleave
        result = deinterleave(text, n)
        score = score_text(result)
        results.append(('deinterleave', n, result, score))
        
        # Columnar
        result = columnar_read(text, n)
        score = score_text(result)
        results.append(('columnar', n, result, score))
        
        # Reverse columnar
        result = reverse_columnar(text, n)
        score = score_text(result)
        results.append(('rev_columnar', n, result, score))
    
    # Sort by score
    results.sort(key=lambda x: x[3], reverse=True)
    return results

def analyze_page(page_num, key_length):
    """Full analysis: hill-climb + interleave."""
    print(f"\n{'='*70}")
    print(f"ANALYZING PAGE {page_num} (Key Length: {key_length})")
    print(f"{'='*70}")
    
    ciphertext = load_runes(page_num)
    if not ciphertext:
        print(f"Could not load page {page_num}")
        return
    
    print(f"Ciphertext length: {len(ciphertext)}")
    
    # Phase 1: Hill-climbing with multiple restarts
    print("\nPhase 1: Hill-climbing optimization (5 restarts)...")
    
    best_overall_key = None
    best_overall_text = None
    best_overall_score = 0
    
    for restart in range(5):
        key, text, score = hill_climb(ciphertext, key_length, iterations=3000)
        if score > best_overall_score:
            best_overall_key = key
            best_overall_text = text
            best_overall_score = score
        print(f"  Restart {restart+1}: Score = {score}")
    
    print(f"\nBest first-layer score: {best_overall_score}")
    print(f"First-layer output (first 150 chars):")
    print(best_overall_text[:150])
    
    # Count patterns
    th_count = best_overall_text.count('TH')
    the_count = best_overall_text.count('THE')
    print(f"\nPattern counts: TH={th_count}, THE={the_count}")
    
    # Phase 2: Try interleaving
    print("\nPhase 2: Testing interleaving/transposition...")
    
    interleave_results = try_interleaving(best_overall_text, key_length)
    
    print("\nTop 10 second-layer results:")
    for i, (method, param, result, score) in enumerate(interleave_results[:10]):
        print(f"{i+1}. {method}(n={param}): score={score}")
        print(f"   {result[:80]}")
    
    # Check best result for readable words
    best_method, best_param, best_result, best_second_score = interleave_results[0]
    
    print(f"\n{'='*50}")
    print(f"BEST COMBINATION:")
    print(f"First layer: score={best_overall_score}, TH={th_count}, THE={the_count}")
    print(f"Second layer: {best_method}(n={best_param}), score={best_second_score}")
    print(f"\nFinal output (first 200 chars):")
    print(best_result[:200])
    
    # Look for actual words
    print("\n--- Searching for known words ---")
    words_found = []
    search_words = ['THE', 'AND', 'TRUTH', 'WITHIN', 'DIVINITY', 'WISDOM', 
                   'BEING', 'UNTO', 'THOU', 'THEE', 'HATH', 'SHED', 'EMERGE',
                   'CIRCUMFERENCE', 'INSTAR', 'SURFACE', 'FIND', 'MUST', 
                   'OUR', 'THAT', 'THIS', 'WHAT', 'FROM', 'LIKE', 'INTO']
    
    for word in search_words:
        if word in best_result:
            count = best_result.count(word)
            words_found.append((word, count))
    
    if words_found:
        print(f"Words found: {words_found}")
    else:
        print("No target words found in best result.")
    
    return best_overall_key, best_overall_text, best_result

def main():
    print("=" * 70)
    print("COMBINED HILL-CLIMBING + INTERLEAVING SOLVER")
    print("=" * 70)
    
    # Test our best pages with prime key lengths
    pages_to_test = [
        (46, 109),  # Highest scoring page
        (8, 101),   # Second highest
        (43, 71),   # Third
        (13, 83),   # Also prime
    ]
    
    for page, key_len in pages_to_test:
        analyze_page(page, key_len)

if __name__ == "__main__":
    main()

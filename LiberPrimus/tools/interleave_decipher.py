#!/usr/bin/env python3
"""
Interleave Decipher Tool
Tests various interleaving and transposition methods on first-layer decrypted output.

The hill-climbing produces TH-rich output that's fragmented ("THEATHE...").
This tool attempts to find the second transformation layer.
"""

import os
import sys
from pathlib import Path

# Gematria Primus alphabet
GP_ALPHABET = "FUÞORC.GWHNIJEOPXSTBEMLD-YAENGOE"  # 29 chars (0-28)
# Simplified for analysis
SIMPLE_ALPHABET = "FUTHORCGWHNIJEOPXSTBEMLDEYNGAO"  # 29 chars

def load_runes(page_num):
    """Load runes from a page."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def rune_to_index(rune):
    """Convert rune to Gematria Primus index."""
    RUNE_MAP = {
        'ᚠ': 0,  # F
        'ᚢ': 1,  # U  
        'ᚦ': 2,  # TH
        'ᚩ': 3,  # O
        'ᚱ': 4,  # R
        'ᚳ': 5,  # C/K
        'ᚷ': 6,  # G
        'ᚹ': 7,  # W
        'ᚻ': 8,  # H
        'ᚾ': 9,  # N
        'ᛁ': 10, # I
        'ᛄ': 11, # J
        'ᛇ': 12, # EO
        'ᛈ': 13, # P
        'ᛉ': 14, # X
        'ᛋ': 15, # S/Z
        'ᛏ': 16, # T
        'ᛒ': 17, # B
        'ᛖ': 18, # E
        'ᛗ': 19, # M
        'ᛚ': 20, # L
        'ᛝ': 21, # NG/ING
        'ᛟ': 22, # OE
        'ᛞ': 23, # D
        'ᚪ': 24, # A
        'ᚫ': 25, # AE
        'ᚣ': 26, # Y
        'ᛡ': 27, # IO/IA
        'ᛠ': 28, # EA
    }
    return RUNE_MAP.get(rune, -1)

def index_to_letter(idx):
    """Convert index to letter representation."""
    LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
               'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
               'A', 'AE', 'Y', 'IO', 'EA']
    if 0 <= idx < 29:
        return LETTERS[idx]
    return '?'

def decrypt_sub(ciphertext_indices, key):
    """Decrypt using subtraction: p = (c - k) mod 29"""
    result = []
    for i, c in enumerate(ciphertext_indices):
        k = key[i % len(key)]
        p = (c - k) % 29
        result.append(p)
    return result

def indices_to_text(indices):
    """Convert indices to text representation."""
    return ''.join(index_to_letter(i) for i in indices)

def read_every_nth(text, n, offset=0):
    """Read every nth character starting at offset."""
    return text[offset::n]

def columnar_transposition(text, num_cols):
    """Apply columnar transposition (read by columns)."""
    # Pad to make even grid
    pad_len = (num_cols - len(text) % num_cols) % num_cols
    padded = text + 'X' * pad_len
    
    num_rows = len(padded) // num_cols
    
    # Read by columns
    result = ''
    for col in range(num_cols):
        for row in range(num_rows):
            idx = row * num_cols + col
            if idx < len(text):
                result += padded[idx]
    
    return result

def reverse_columnar(text, num_cols):
    """Reverse columnar transposition (text was written by columns, read by rows)."""
    pad_len = (num_cols - len(text) % num_cols) % num_cols
    padded = text + 'X' * pad_len
    
    num_rows = len(padded) // num_cols
    
    # Text was written by columns, we read by rows
    grid = [[''] * num_cols for _ in range(num_rows)]
    
    idx = 0
    for col in range(num_cols):
        for row in range(num_rows):
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    result = ''
    for row in range(num_rows):
        for col in range(num_cols):
            result += grid[row][col]
    
    return result[:len(text)]

def deinterleave(text, num_streams):
    """Deinterleave text that was combined from multiple streams."""
    streams = ['' for _ in range(num_streams)]
    for i, char in enumerate(text):
        streams[i % num_streams] += char
    return ''.join(streams)

def score_english(text):
    """Score text for English likelihood."""
    # Common English words
    COMMON_WORDS = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                   'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS',
                   'HIS', 'HIM', 'HOW', 'MAN', 'NEW', 'NOW', 'OLD', 'SEE',
                   'WAY', 'WHO', 'ITS', 'SAY', 'SHE', 'TWO', 'HOW', 'ITS',
                   'LET', 'PUT', 'SAY', 'TOO', 'USE', 'THAT', 'WITH', 'HAVE',
                   'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'HAVE',
                   'MANY', 'SOME', 'THEM', 'THESE', 'WOULD', 'MAKE', 'LIKE',
                   'INTO', 'JUST', 'KNOW', 'TAKE', 'COME', 'COULD', 'THAN',
                   'FIND', 'DIVINITY', 'WITHIN', 'EMERGE', 'TRUTH', 'SHED',
                   'CIRCUMFERENCE', 'SURFACE', 'WISDOM', 'BEING', 'UNTO',
                   'THOU', 'THEE', 'THINE', 'HATH', 'DOTH', 'DOETH', 'ART',
                   'SELF', 'PRIMUS', 'CICADA', 'LIBER']
    
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    
    # Penalize repeated patterns
    for i in range(len(text) - 10):
        chunk = text[i:i+5]
        if text.count(chunk) > 5:
            score -= 50
    
    return score

def analyze_page(page_num, key_length, key=None):
    """Analyze a page with various interleaving methods."""
    runes = load_runes(page_num)
    if not runes:
        print(f"Could not load page {page_num}")
        return
    
    # Convert to indices
    indices = []
    for r in runes:
        idx = rune_to_index(r)
        if idx >= 0:
            indices.append(idx)
    
    print(f"\n{'='*70}")
    print(f"INTERLEAVE ANALYSIS: Page {page_num} (Key Length: {key_length})")
    print(f"{'='*70}")
    print(f"Rune count: {len(indices)}")
    
    # If no key provided, generate optimized key using hill-climbing
    if key is None:
        # Use a simple frequency-based initial key
        key = [0] * key_length
        print("\nUsing zero key (for pattern analysis)")
    
    # First layer decryption
    decrypted = decrypt_sub(indices, key)
    first_layer = indices_to_text(decrypted)
    
    print(f"\nFirst layer output (first 100 chars):")
    print(first_layer[:100])
    
    results = []
    
    # Test various interleaving methods
    print("\n--- INTERLEAVING TESTS ---")
    
    # 1. Every Nth character
    for n in range(2, 10):
        for offset in range(n):
            text = read_every_nth(first_layer, n, offset)
            score = score_english(text)
            if score > 0:
                results.append(('every_nth', n, offset, text[:50], score))
    
    # 2. Columnar transposition
    for cols in [7, 11, 13, 17, 19, 23, 29, key_length]:
        try:
            text = columnar_transposition(first_layer, cols)
            score = score_english(text)
            if score > 0:
                results.append(('columnar', cols, 0, text[:50], score))
        except:
            pass
    
    # 3. Reverse columnar
    for cols in [7, 11, 13, 17, 19, 23, 29, key_length]:
        try:
            text = reverse_columnar(first_layer, cols)
            score = score_english(text)
            if score > 0:
                results.append(('rev_columnar', cols, 0, text[:50], score))
        except:
            pass
    
    # 4. Deinterleave
    for num_streams in range(2, 10):
        text = deinterleave(first_layer, num_streams)
        score = score_english(text)
        if score > 0:
            results.append(('deinterleave', num_streams, 0, text[:50], score))
    
    # 5. Key-length based columnar
    if key_length > 1:
        text = columnar_transposition(first_layer, key_length)
        score = score_english(text)
        results.append(('key_columnar', key_length, 0, text[:50], score))
        
        text = reverse_columnar(first_layer, key_length)
        score = score_english(text)
        results.append(('key_rev_col', key_length, 0, text[:50], score))
    
    # Sort by score
    results.sort(key=lambda x: x[4], reverse=True)
    
    print("\nTop 10 results by English score:")
    for i, (method, param, offset, sample, score) in enumerate(results[:10]):
        print(f"{i+1}. {method}(n={param}, off={offset}): score={score}")
        print(f"   Sample: {sample}")
    
    return results

def test_with_hill_climb_key():
    """Test interleaving with our best hill-climbing results."""
    # Page 46 best key from hill-climbing (simplified - we'd load from results)
    # For now, just test the pattern with zero key
    
    pages_to_test = [
        (46, 109),  # Best score
        (8, 101),   # Second best
        (43, 71),   # Third
    ]
    
    for page, key_len in pages_to_test:
        analyze_page(page, key_len)

def main():
    print("=" * 70)
    print("INTERLEAVE DECIPHER TOOL")
    print("Testing second-layer transformation hypotheses")
    print("=" * 70)
    
    # Test with our best pages
    test_with_hill_climb_key()
    
    # Special test: read every 2nd char from known good output
    print("\n" + "=" * 70)
    print("SPECIAL: Testing THE-pattern extraction")
    print("=" * 70)
    
    # The "THEATHE" pattern suggests interleaving
    test_pattern = "THEATHENATHTHUETHEOUAEEPATHEATHEOWIOAEPTHENGNGE"
    
    print(f"Original: {test_pattern}")
    print(f"Every 2nd (off=0): {read_every_nth(test_pattern, 2, 0)}")
    print(f"Every 2nd (off=1): {read_every_nth(test_pattern, 2, 1)}")
    print(f"Every 3rd (off=0): {read_every_nth(test_pattern, 3, 0)}")
    print(f"Every 3rd (off=1): {read_every_nth(test_pattern, 3, 1)}")
    print(f"Every 3rd (off=2): {read_every_nth(test_pattern, 3, 2)}")
    
    # Deinterleave
    for n in range(2, 6):
        print(f"Deinterleave(n={n}): {deinterleave(test_pattern, n)}")

if __name__ == "__main__":
    main()

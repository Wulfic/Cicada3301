#!/usr/bin/env python3
"""
Autokey Cipher Attack Tool
Tests if the Liber Primus uses an autokey cipher where the key
is extended using the plaintext.

Autokey formula:
- Encryption: c[i] = (p[i] + k[i]) mod 29, where k[i] = primer[i] for i < len(primer), else p[i-len(primer)]
- Decryption: p[i] = (c[i] - k[i]) mod 29

We test if known English words at specific positions reveal consistent autokey behavior.
"""

import os
import sys
from pathlib import Path
from collections import Counter
import random

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

# Known words from Discovery 25
KNOWN_WORDS = {
    8: {3: ('PATH', 14), 10: ('THE', 1)},
    13: {5: ('A', 2), 11: ('IN', 23), 17: ('DO', 9)},
    43: {6: ('BE', 12), 12: ('THY', 25), 17: ('NO', 3)},
    46: {6: ('I', 11), 10: ('UP', 5), 17: ('GO', 15), 18: ('AN', 18), 19: ('I', 12)},
}

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_runes_with_structure(rune_text):
    """Parse runes keeping track of positions and word boundaries."""
    result = {
        'indices': [],      # All rune indices in order
        'words': [],        # List of (start_pos, indices) tuples
        'word_starts': [],  # Position where each word starts
    }
    
    pos = 0
    current_word = []
    word_start = 0
    
    for char in rune_text:
        if char in RUNE_MAP:
            if not current_word:
                word_start = pos
            idx = RUNE_MAP[char]
            result['indices'].append(idx)
            current_word.append(idx)
            pos += 1
        elif char in '-.•\n\r ':
            if current_word:
                result['words'].append((word_start, current_word.copy()))
                result['word_starts'].append(word_start)
                current_word = []
    
    if current_word:
        result['words'].append((word_start, current_word.copy()))
        result['word_starts'].append(word_start)
    
    return result

def word_to_indices(word):
    """Convert English word to Gematria indices."""
    indices = []
    i = 0
    while i < len(word):
        found = False
        for j, letter in enumerate(LETTERS):
            if word[i:].startswith(letter):
                indices.append(j)
                i += len(letter)
                found = True
                break
        if not found:
            print(f"Warning: Unknown letter at {word[i:]}")
            i += 1
    return indices

def autokey_decrypt_with_primer(ciphertext, primer):
    """Decrypt using autokey cipher with given primer."""
    plaintext = []
    key = list(primer)
    
    for i, c in enumerate(ciphertext):
        if i < len(primer):
            k = primer[i]
        else:
            k = plaintext[i - len(primer)]
        
        p = (c - k) % 29
        plaintext.append(p)
    
    return plaintext

def test_autokey_hypothesis(page_num):
    """Test if discovered words are consistent with autokey cipher."""
    print(f"\n{'='*70}")
    print(f"AUTOKEY ANALYSIS: Page {page_num}")
    print(f"{'='*70}")
    
    rune_text = load_runes(page_num)
    if not rune_text:
        print(f"Could not load page {page_num}")
        return
    
    parsed = parse_runes_with_structure(rune_text)
    ciphertext = parsed['indices']
    
    print(f"Total runes: {len(ciphertext)}")
    print(f"Total words: {len(parsed['words'])}")
    
    if page_num not in KNOWN_WORDS:
        print("No known words for this page")
        return
    
    known = KNOWN_WORDS[page_num]
    
    # For each known word, calculate what the key values would be
    print("\n--- Known word analysis ---")
    
    key_constraints = {}  # position -> required key value
    
    for word_idx, (word_text, expected_key) in known.items():
        if word_idx >= len(parsed['words']):
            continue
            
        start_pos, word_cipher = parsed['words'][word_idx]
        word_plain = word_to_indices(word_text)
        
        if len(word_plain) != len(word_cipher):
            print(f"Word {word_idx}: Length mismatch! plain={len(word_plain)}, cipher={len(word_cipher)}")
            continue
        
        print(f"\nWord {word_idx}: '{word_text}' at position {start_pos}")
        print(f"  Cipher: {word_cipher}")
        print(f"  Plain:  {word_plain}")
        
        # Calculate required key for each position
        for i, (c, p) in enumerate(zip(word_cipher, word_plain)):
            k = (c - p) % 29
            pos = start_pos + i
            key_constraints[pos] = k
            print(f"  Position {pos}: cipher={c}, plain={p}, key={k} ({LETTERS[k]})")
    
    # Check if key positions follow autokey pattern
    print("\n--- Checking autokey consistency ---")
    
    sorted_positions = sorted(key_constraints.keys())
    
    # For autokey, key[i] should equal plaintext[i - primer_len]
    # Let's try different primer lengths
    
    for primer_len in range(1, 20):
        print(f"\nTesting primer length {primer_len}:")
        
        # Build partial plaintext from constraints
        partial_plain = {}
        for pos, k in key_constraints.items():
            # In autokey: k[i] = p[i - primer_len] for i >= primer_len
            source_pos = pos - primer_len
            if source_pos >= 0:
                partial_plain[source_pos] = k
        
        # Check consistency
        conflicts = 0
        matches = 0
        
        for pos, plain_val in partial_plain.items():
            if pos in key_constraints:
                # This position has both a known plaintext AND a key constraint
                # Check if they're consistent
                if key_constraints[pos] == partial_plain.get(pos - primer_len, -1):
                    matches += 1
                else:
                    conflicts += 1
        
        print(f"  Derived plaintext positions: {sorted(partial_plain.items())[:10]}...")
        print(f"  Matches: {matches}, Conflicts: {conflicts}")
    
    return parsed, key_constraints

def brute_force_primer(page_num, primer_len=3):
    """Try all possible primers for autokey decryption."""
    print(f"\n{'='*70}")
    print(f"BRUTE FORCE AUTOKEY: Page {page_num}, Primer Length {primer_len}")
    print(f"{'='*70}")
    
    rune_text = load_runes(page_num)
    if not rune_text:
        return
    
    parsed = parse_runes_with_structure(rune_text)
    ciphertext = parsed['indices']
    
    # Common English word scoring
    COMMON_WORDS = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
                   'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIM', 'HIS',
                   'HOW', 'TWO', 'WAY', 'WHO', 'ITS', 'SAY', 'SHE', 'HIS',
                   'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM',
                   'THEY', 'BEEN', 'FIND', 'TRUTH', 'WITHIN', 'WISDOM',
                   'THOU', 'THEE', 'THINE', 'HATH', 'UNTO', 'PATH', 'SHED'}
    
    def score_text(indices):
        text = ''.join(LETTERS[i] for i in indices)
        score = 0
        for word in COMMON_WORDS:
            score += text.count(word) * len(word)
        return score, text
    
    best_score = 0
    best_primer = None
    best_text = None
    
    # Try systematic primers
    tested = 0
    
    if primer_len == 1:
        primers = [[i] for i in range(29)]
    elif primer_len == 2:
        primers = [[i, j] for i in range(29) for j in range(29)]
    elif primer_len == 3:
        # Sample subset for speed
        primers = [[i, j, k] for i in range(0, 29, 3) for j in range(0, 29, 3) for k in range(0, 29, 3)]
    else:
        # Random sampling
        primers = [[random.randint(0, 28) for _ in range(primer_len)] for _ in range(1000)]
    
    for primer in primers:
        plaintext = autokey_decrypt_with_primer(ciphertext, primer)
        score, text = score_text(plaintext)
        tested += 1
        
        if score > best_score:
            best_score = score
            best_primer = primer
            best_text = text
            print(f"New best (score={score}): primer={primer}")
            print(f"  First 100 chars: {text[:100]}")
    
    print(f"\nTested {tested} primers")
    print(f"Best score: {best_score}")
    print(f"Best primer: {best_primer}")
    if best_text:
        print(f"Best text (first 200): {best_text[:200]}")
    
    return best_primer, best_text

def main():
    print("=" * 70)
    print("AUTOKEY CIPHER ATTACK TOOL")
    print("=" * 70)
    
    # Analyze each page with known words
    for page in [8, 13, 43, 46]:
        test_autokey_hypothesis(page)
    
    # Brute force test on one page
    print("\n" + "="*70)
    print("BRUTE FORCE AUTOKEY TEST")
    print("="*70)
    
    for primer_len in [1, 2, 3]:
        brute_force_primer(46, primer_len)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Comprehensive Key Pattern Analysis

Based on confirmed English words found by word_boundary_solver.py:
- Page 8: PATH (key=14), THE (key=1)
- Page 13: A (key=2,6), IN (key=23), I (key=8), DO (key=9)
- Page 43: BE (key=12), THY (key=25), NO (key=3)
- Page 46: I (key=11), UP (key=5), GO (key=15), AN (key=18), I (key=12)

Goal: Find the pattern that generates these keys.
"""

import os
from pathlib import Path
from collections import Counter, defaultdict

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

# Gematria prime values (first 29 primes)
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
             59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Discovered words with their positions and keys
DISCOVERIES = {
    8: [
        {'word_pos': 3, 'word': 'PATH', 'key': 14, 'rune_letter': 'X'},
        {'word_pos': 10, 'word': 'THE', 'key': 1, 'rune_letter': 'U'},
    ],
    13: [
        {'word_pos': 5, 'word': 'A', 'key': 2, 'rune_letter': 'TH'},
        {'word_pos': 7, 'word': 'A', 'key': 6, 'rune_letter': 'G'},
        {'word_pos': 11, 'word': 'IN', 'key': 23, 'rune_letter': 'D'},
        {'word_pos': 13, 'word': 'I', 'key': 8, 'rune_letter': 'H'},
        {'word_pos': 17, 'word': 'DO', 'key': 9, 'rune_letter': 'N'},
    ],
    43: [
        {'word_pos': 6, 'word': 'BE', 'key': 12, 'rune_letter': 'EO'},
        {'word_pos': 12, 'word': 'THY', 'key': 25, 'rune_letter': 'AE'},
        {'word_pos': 17, 'word': 'NO', 'key': 3, 'rune_letter': 'O'},
    ],
    46: [
        {'word_pos': 6, 'word': 'I', 'key': 11, 'rune_letter': 'J'},
        {'word_pos': 10, 'word': 'UP', 'key': 5, 'rune_letter': 'C'},
        {'word_pos': 17, 'word': 'GO', 'key': 15, 'rune_letter': 'S'},
        {'word_pos': 19, 'word': 'AN', 'key': 18, 'rune_letter': 'E'},
        {'word_pos': 20, 'word': 'I', 'key': 12, 'rune_letter': 'EO'},
    ],
}

def analyze_key_sequences():
    """Analyze patterns in the discovered keys."""
    
    print("=" * 70)
    print("KEY SEQUENCE ANALYSIS")
    print("=" * 70)
    
    for page, discoveries in DISCOVERIES.items():
        print(f"\nPage {page}:")
        
        sorted_disc = sorted(discoveries, key=lambda x: x['word_pos'])
        
        word_positions = [d['word_pos'] for d in sorted_disc]
        keys = [d['key'] for d in sorted_disc]
        primes = [GP_PRIMES[k] for k in keys]
        
        print(f"  Word positions: {word_positions}")
        print(f"  Keys (indices): {keys}")
        print(f"  Keys (letters): {[LETTERS[k] for k in keys]}")
        print(f"  Keys (primes):  {primes}")
        
        # Analyze differences between consecutive keys
        if len(keys) > 1:
            key_diffs = [(keys[i+1] - keys[i]) % 29 for i in range(len(keys)-1)]
            print(f"  Key differences (mod 29): {key_diffs}")
            
            word_pos_diffs = [word_positions[i+1] - word_positions[i] for i in range(len(word_positions)-1)]
            print(f"  Word position gaps: {word_pos_diffs}")
            
            # Check if key difference = word position gap (mod 29)
            matches = [key_diffs[i] == (word_pos_diffs[i] % 29) for i in range(len(key_diffs))]
            print(f"  Key diff == Word gap? {matches}")

def analyze_word_position_key_relationship():
    """Check if key is related to word position."""
    
    print("\n" + "=" * 70)
    print("WORD POSITION vs KEY RELATIONSHIP")
    print("=" * 70)
    
    all_data = []
    
    for page, discoveries in DISCOVERIES.items():
        for d in discoveries:
            all_data.append({
                'page': page,
                'word_pos': d['word_pos'],
                'key': d['key'],
                'word': d['word']
            })
    
    # Test various relationships
    print("\nTesting: key = (word_pos * constant) mod 29")
    for mult in range(1, 29):
        correct = sum(1 for d in all_data if d['key'] == (d['word_pos'] * mult) % 29)
        if correct > 2:
            print(f"  Multiplier {mult}: {correct}/{len(all_data)} matches")
    
    print("\nTesting: key = (word_pos + constant) mod 29")
    for add in range(29):
        correct = sum(1 for d in all_data if d['key'] == (d['word_pos'] + add) % 29)
        if correct > 2:
            print(f"  Additive {add}: {correct}/{len(all_data)} matches")
    
    print("\nTesting: key = (page + word_pos + constant) mod 29")
    for add in range(29):
        correct = sum(1 for d in all_data if d['key'] == (d['page'] + d['word_pos'] + add) % 29)
        if correct > 2:
            print(f"  Page+WordPos+{add}: {correct}/{len(all_data)} matches")
    
    print("\nTesting: key = (page * word_pos + constant) mod 29")
    for add in range(29):
        correct = sum(1 for d in all_data if d['key'] == (d['page'] * d['word_pos'] + add) % 29)
        if correct > 2:
            print(f"  Page*WordPos+{add}: {correct}/{len(all_data)} matches")

def analyze_cumulative_key():
    """Check if key is cumulative within a page."""
    
    print("\n" + "=" * 70)
    print("CUMULATIVE KEY HYPOTHESIS")
    print("=" * 70)
    
    for page, discoveries in DISCOVERIES.items():
        print(f"\nPage {page}:")
        sorted_disc = sorted(discoveries, key=lambda x: x['word_pos'])
        
        cumsum = 0
        for i, d in enumerate(sorted_disc):
            cumsum += d['key']
            print(f"  Word {d['word_pos']:2d}: key={d['key']:2d}, cumulative={cumsum:3d}, cum mod 29={cumsum % 29}")

def analyze_prime_relationships():
    """Check if keys relate to prime positions or values."""
    
    print("\n" + "=" * 70)
    print("PRIME NUMBER RELATIONSHIPS")
    print("=" * 70)
    
    # First 50 primes for reference
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    for page, discoveries in DISCOVERIES.items():
        print(f"\nPage {page}:")
        sorted_disc = sorted(discoveries, key=lambda x: x['word_pos'])
        
        for d in sorted_disc:
            key = d['key']
            word_pos = d['word_pos']
            prime_value = GP_PRIMES[key]
            
            # Check various relationships
            print(f"  Word {word_pos}: key={key}, prime={prime_value}")
            
            # Is word_pos a prime index?
            if word_pos < len(primes):
                print(f"    Prime at position {word_pos} = {primes[word_pos]}")
                print(f"    Prime at position {word_pos} mod 29 = {primes[word_pos] % 29}")
            
            # Is key related to page number?
            print(f"    page mod 29 = {page % 29}")
            print(f"    (page + word_pos) mod 29 = {(page + word_pos) % 29}")

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_rune_position_keys():
    """Check if key relates to actual rune position (not word position)."""
    
    print("\n" + "=" * 70)
    print("RUNE POSITION ANALYSIS")
    print("=" * 70)
    
    for page_num in DISCOVERIES.keys():
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        # Parse into words and track rune positions
        words = []
        current_word = []
        current_word_start = 0
        rune_pos = 0
        
        for char in rune_text:
            if char in RUNE_MAP:
                if not current_word:
                    current_word_start = rune_pos
                current_word.append(RUNE_MAP[char])
                rune_pos += 1
            elif char in '-. \n\r':
                if current_word:
                    words.append({
                        'indices': current_word,
                        'start_pos': current_word_start,
                        'end_pos': rune_pos - 1
                    })
                    current_word = []
        
        if current_word:
            words.append({
                'indices': current_word,
                'start_pos': current_word_start,
                'end_pos': rune_pos - 1
            })
        
        print(f"\nPage {page_num}:")
        
        discoveries = DISCOVERIES[page_num]
        for d in discoveries:
            word_pos = d['word_pos'] - 1  # Adjust for 0-indexing
            if word_pos < len(words):
                word_data = words[word_pos]
                rune_start = word_data['start_pos']
                
                print(f"  Word '{d['word']}' at word_pos={d['word_pos']}: "
                      f"rune_start={rune_start}, key={d['key']}")
                print(f"    rune_start mod 29 = {rune_start % 29}")
                print(f"    key - rune_start mod 29 = {(d['key'] - rune_start) % 29}")

def check_fibonacci_key():
    """Check if keys follow Fibonacci-like sequence."""
    
    print("\n" + "=" * 70)
    print("FIBONACCI/LUCAS KEY CHECK")
    print("=" * 70)
    
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
    lucas = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199]
    
    fib_mod29 = [f % 29 for f in fib]
    lucas_mod29 = [l % 29 for l in lucas]
    
    print(f"Fibonacci mod 29: {fib_mod29}")
    print(f"Lucas mod 29: {lucas_mod29}")
    
    for page, discoveries in DISCOVERIES.items():
        keys = [d['key'] for d in sorted(discoveries, key=lambda x: x['word_pos'])]
        print(f"\nPage {page} keys: {keys}")
        
        # Check if keys appear in Fibonacci/Lucas
        fib_matches = [k in fib_mod29 for k in keys]
        lucas_matches = [k in lucas_mod29 for k in keys]
        
        print(f"  In Fibonacci mod 29? {fib_matches} ({sum(fib_matches)}/{len(keys)})")
        print(f"  In Lucas mod 29? {lucas_matches} ({sum(lucas_matches)}/{len(keys)})")

def reverse_engineer_key_source():
    """Try to find what text could generate these keys."""
    
    print("\n" + "=" * 70)
    print("REVERSE ENGINEERING KEY SOURCE")
    print("=" * 70)
    
    # All discovered keys across all pages
    all_keys = []
    for page, discoveries in DISCOVERIES.items():
        sorted_disc = sorted(discoveries, key=lambda x: x['word_pos'])
        for d in sorted_disc:
            all_keys.append(d['key'])
    
    print(f"All discovered keys in order: {all_keys}")
    print(f"As rune letters: {''.join(LETTERS[k] for k in all_keys)}")
    
    # Check if this spells anything
    key_string = ''.join(LETTERS[k] for k in all_keys)
    print(f"\nKey string: {key_string}")
    print("Could this be part of a meaningful phrase?")
    
    # Check unique keys
    unique_keys = sorted(set(all_keys))
    print(f"\nUnique keys: {unique_keys}")
    print(f"As letters: {[LETTERS[k] for k in unique_keys]}")

if __name__ == '__main__':
    analyze_key_sequences()
    analyze_word_position_key_relationship()
    analyze_cumulative_key()
    analyze_prime_relationships()
    analyze_rune_position_keys()
    check_fibonacci_key()
    reverse_engineer_key_source()

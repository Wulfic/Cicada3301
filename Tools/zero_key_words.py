#!/usr/bin/env python3
"""
ZERO-KEY WORD ANALYSIS

Find words where key=0 (no encryption) across all pages.
These may be intentionally revealed plaintext words or hints.
"""

import os
from pathlib import Path
import json

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def load_runes(page_num):
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_words(rune_text):
    words = []
    current_word = []
    for char in rune_text:
        if char in RUNE_MAP:
            current_word.append(RUNE_MAP[char])
        elif char in '-. \n\r':
            if current_word:
                words.append(current_word)
                current_word = []
    if current_word:
        words.append(current_word)
    return words

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def find_zero_key_words():
    """
    For each page with optimal (mult, offset), find words where key=0.
    These words are not encrypted!
    """
    
    # Load results
    results_file = Path(__file__).parent / "results" / "word_mult_decode" / "all_results.json"
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    print("=" * 70)
    print("ZERO-KEY WORDS (UNENCRYPTED)")
    print("=" * 70)
    print("\nThese words have key=0 with their optimal (mult, offset).")
    print("Key = (word_index × mult + offset) mod 29 = 0")
    print("This means: word_index × mult ≡ -offset (mod 29)")
    print()
    
    all_zero_key_words = []
    
    for page_str, data in sorted(results.items(), key=lambda x: int(x[0])):
        page_num = int(page_str)
        mult = data['multiplier']
        offset = data['offset']
        
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words(rune_text)
        
        # Find word indices where key = 0
        # key = (word_idx * mult + offset) % 29 = 0
        # word_idx * mult ≡ -offset (mod 29)
        
        for word_idx, word in enumerate(words):
            key = (word_idx * mult + offset) % 29
            if key == 0:
                text = indices_to_text(word)
                all_zero_key_words.append({
                    'page': page_num,
                    'word_idx': word_idx,
                    'text': text,
                    'mult': mult,
                    'offset': offset
                })
                print(f"Page {page_num:2d}, word {word_idx:2d}: {text}")
    
    print("\n" + "=" * 70)
    print("COLLECTED ZERO-KEY WORDS")
    print("=" * 70)
    
    all_texts = [w['text'] for w in all_zero_key_words]
    print("\nAll zero-key words:")
    print(' '.join(all_texts))
    
    # Look for patterns in word positions
    print("\n" + "=" * 70)
    print("PATTERN ANALYSIS")
    print("=" * 70)
    
    print("\nWord index where key=0:")
    for w in all_zero_key_words:
        # key = 0 when word_idx * mult + offset ≡ 0 (mod 29)
        # word_idx ≡ (-offset / mult) (mod 29)
        print(f"  Page {w['page']}: word_idx={w['word_idx']}, "
              f"mult={w['mult']}, offset={w['offset']}")

if __name__ == '__main__':
    find_zero_key_words()

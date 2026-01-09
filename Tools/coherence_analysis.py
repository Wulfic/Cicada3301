#!/usr/bin/env python3
"""
COHERENCE-BASED DECRYPTION ANALYSIS

Instead of just counting English words, look for CONSECUTIVE English words
which would indicate correct decryption of phrases.
"""

import os
from pathlib import Path
from collections import Counter
from itertools import combinations

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

COMMON_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
    'WE', 'ALL', 'AND', 'ARE', 'BUT', 'CAN', 'FOR', 'HAS', 'HIM', 'HIS', 
    'HOW', 'ITS', 'MAY', 'NEW', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT', 
    'OWN', 'SAY', 'SHE', 'THE', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'YOU', 
    'YET', 'THY', 'YEA', 'NAY', 'ANY', 'OWE', 'FIND', 'FROM', 'HAVE', 'INTO', 
    'JUST', 'KNOW', 'LIKE', 'MAKE', 'MANY', 'MORE', 'MUST', 'ONLY', 'OVER', 
    'PATH', 'SELF', 'SOME', 'SUCH', 'TAKE', 'THAN', 'THAT', 'THEM', 'THEN', 
    'THIS', 'THUS', 'UNTO', 'UPON', 'WHAT', 'WHEN', 'WILL', 'WITH', 'YOUR', 
    'SEEK', 'THOU', 'THEE', 'HATH', 'DOTH', 'THEY', 'ALSO', 'BEEN', 'EACH', 
    'WERE', 'SAID', 'MADE', 'BOTH', 'BEING', 'THEIR', 'THERE', 'THESE', 
    'THING', 'THOSE', 'TRUTH', 'WHICH', 'THINE', 'SHALT', 'SHALL', 'WORLD', 
    'LIGHT', 'WISDOM', 'PRIME', 'PRIMES', 'WITHIN', 'DIVINITY', 'EMERGE', 
    'KNOWLEDGE', 'BECOME', 'CIRCUMFERENCE', 'CONSUMPTION', 'INSTRUCTION', 
    'ADMONITION', 'INSTAR', 'SURFACE', 'PILGRIM', 'JOURNEY', 'SACRED', 
    'SECRET', 'HIDDEN', 'AWAKEN', 'PARABLE', 'LICE', 'FIRST', 'SECOND',
    'THIRD', 'LAST', 'NEXT', 'BEFORE', 'AFTER', 'ABOVE', 'BELOW', 'HERE',
    'THERE', 'WHERE', 'WHEN', 'WHAT', 'HOW', 'WHY', 'WORD', 'WORDS',
    'BODY', 'MIND', 'SOUL', 'SPIRIT', 'LIFE', 'DEATH', 'LOVE', 'HATE',
    'GOOD', 'EVIL', 'TRUE', 'FALSE', 'REAL', 'FAKE', 'DEEP', 'HIGH',
    'LOW', 'NEAR', 'FAR', 'LONG', 'SHORT', 'WIDE', 'NARROW', 'OPEN',
    'CLOSED', 'FULL', 'EMPTY', 'RICH', 'POOR', 'YOUNG', 'OLD', 'NEW',
    'COME', 'CAME', 'GONE', 'GOING', 'CAME', 'WENT', 'SEEN', 'KNOW',
    'KNOWN', 'THINK', 'THOUGHT', 'FEEL', 'FELT', 'HEAR', 'HEARD', 'SEE',
    'SAW', 'SPEAK', 'SPOKE', 'TAKE', 'TOOK', 'GIVE', 'GAVE', 'FIND',
    'FOUND', 'LOSE', 'LOST', 'KEEP', 'KEPT', 'LET', 'LEAVE', 'LEFT'
}

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

def decrypt_word(indices, key):
    return [(c - key) % 29 for c in indices]

def is_english(text):
    return text.upper() in COMMON_WORDS

def find_consecutive_pairs(words, mult, offset):
    """Find consecutive English word pairs."""
    consecutive_pairs = []
    
    for i in range(len(words) - 1):
        key1 = (i * mult + offset) % 29
        key2 = ((i+1) * mult + offset) % 29
        
        dec1 = indices_to_text(decrypt_word(words[i], key1))
        dec2 = indices_to_text(decrypt_word(words[i+1], key2))
        
        if is_english(dec1) and is_english(dec2):
            consecutive_pairs.append((i, dec1, dec2))
    
    return consecutive_pairs

def find_best_consecutive(words):
    """Find (mult, offset) that produces the most consecutive pairs."""
    best_mult = 1
    best_offset = 0
    best_count = 0
    best_pairs = []
    
    for mult in range(1, 29):
        for offset in range(29):
            pairs = find_consecutive_pairs(words, mult, offset)
            if len(pairs) > best_count:
                best_count = len(pairs)
                best_mult = mult
                best_offset = offset
                best_pairs = pairs
    
    return best_mult, best_offset, best_count, best_pairs

def find_triplets(words, mult, offset):
    """Find 3 consecutive English words."""
    triplets = []
    
    for i in range(len(words) - 2):
        keys = [(i * mult + offset) % 29,
                ((i+1) * mult + offset) % 29,
                ((i+2) * mult + offset) % 29]
        
        decs = [indices_to_text(decrypt_word(words[i+j], keys[j])) for j in range(3)]
        
        if all(is_english(d) for d in decs):
            triplets.append((i, decs))
    
    return triplets

def analyze_page(page_num):
    """Analyze a single page for coherent sequences."""
    rune_text = load_runes(page_num)
    if not rune_text:
        return None
    
    words = parse_words(rune_text)
    if len(words) < 10:
        return None
    
    # Find best for consecutive pairs
    mult, offset, count, pairs = find_best_consecutive(words)
    
    # Also check for triplets
    triplets = find_triplets(words, mult, offset)
    
    return {
        'page': page_num,
        'mult': mult,
        'offset': offset,
        'pair_count': count,
        'pairs': pairs,
        'triplets': triplets
    }

def main():
    print("=" * 70)
    print("COHERENCE-BASED ANALYSIS: CONSECUTIVE ENGLISH WORDS")
    print("=" * 70)
    
    results = []
    
    for page_num in range(8, 57):
        result = analyze_page(page_num)
        if result and result['pair_count'] > 0:
            results.append(result)
            
            print(f"\nPage {page_num}: mult={result['mult']}, offset={result['offset']}, "
                  f"pairs={result['pair_count']}")
            
            if result['triplets']:
                print("  TRIPLETS FOUND:")
                for idx, decs in result['triplets']:
                    print(f"    [{idx}]: {' '.join(decs)}")
            
            if result['pairs'] and not result['triplets']:
                print("  Pairs:")
                for idx, w1, w2 in result['pairs'][:5]:
                    print(f"    [{idx}]: {w1} {w2}")
    
    print("\n" + "=" * 70)
    print("PAGES WITH TRIPLETS (3+ consecutive English words)")
    print("=" * 70)
    
    triplet_pages = [r for r in results if r['triplets']]
    if triplet_pages:
        for r in triplet_pages:
            print(f"\nPage {r['page']}: mult={r['mult']}, offset={r['offset']}")
            for idx, decs in r['triplets']:
                print(f"  [{idx}]: {' '.join(decs)}")
    else:
        print("No pages with 3+ consecutive English words found.")
    
    # Sort by pair count
    print("\n" + "=" * 70)
    print("TOP PAGES BY CONSECUTIVE PAIR COUNT")
    print("=" * 70)
    
    sorted_results = sorted(results, key=lambda x: x['pair_count'], reverse=True)
    for r in sorted_results[:10]:
        print(f"Page {r['page']}: {r['pair_count']} pairs (mult={r['mult']}, offset={r['offset']})")

if __name__ == '__main__':
    main()
